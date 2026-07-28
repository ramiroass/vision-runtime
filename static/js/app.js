// ==========================================================================
// Vision Runtime - Application Logic (Sprint 5 & Dynamic Multi-Step Execution)
// ==========================================================================

let isAutonomous = false;
let currentGoal = "";

document.addEventListener("DOMContentLoaded", () => {
  startMetricsPolling();
  startFrameStream();
  fetchScene();
  fetchIntents();

  document.getElementById("intent-form").addEventListener("submit", handleIntentSubmit);
  document.getElementById("question-form").addEventListener("submit", handleQuestionSubmit);
  document.getElementById("planner-form").addEventListener("submit", handlePlannerSubmit);
  document.getElementById("btn-approve-execute").addEventListener("click", handleApproveAndExecute);
  document.getElementById("ocr-selector").addEventListener("change", handleOCRChange);
  document.getElementById("btn-replay").addEventListener("click", handleReplayFetch);
  document.getElementById("btn-emergency-stop").addEventListener("click", handleEmergencyStop);
  document.getElementById("btn-toggle-auto").addEventListener("click", handleToggleAutonomous);
});

// Stream de Pantalla en Directo
function startFrameStream() {
  const img = document.getElementById("screen-stream");
  setInterval(() => {
    img.src = "/api/frame?t=" + new Date().getTime();
  }, 250);
}

// Telemetría en vivo
function startMetricsPolling() {
  setInterval(async () => {
    try {
      const res = await fetch("/api/metrics");
      if (!res.ok) return;
      const data = await res.json();

      document.getElementById("meter-fps").textContent = `${data.actual_fps} / ${data.target_fps}`;
      document.getElementById("meter-latency").textContent = `${data.latency_ms} ms`;
      document.getElementById("meter-ocr").textContent = data.ocr_provider || "FastOCR";
      document.getElementById("meter-memory").textContent = `${data.memory_snapshots_count || 0} Cuadros`;
      document.getElementById("meter-ram").textContent = `${data.ram_usage_mb} MB`;

      isAutonomous = data.autonomous;
      const autoMeter = document.getElementById("meter-autonomous");
      if (data.emergency_stop) {
        autoMeter.textContent = "EMERGENCY STOP 🚨";
        autoMeter.className = "val highlight-red";
      } else if (isAutonomous) {
        autoMeter.textContent = "AUTONOMOUS: ON 🟢";
        autoMeter.className = "val highlight-green";
      } else {
        autoMeter.textContent = "AUTONOMOUS: OFF 🔴";
        autoMeter.className = "val highlight-red";
      }
    } catch (err) {
      console.error("Error cargando métricas:", err);
    }
  }, 1000);

  setInterval(fetchScene, 2000);
}

// Emergency Stop
async function handleEmergencyStop() {
  try {
    const res = await fetch("/api/security/emergency-stop", { method: "POST" });
    if (res.ok) {
      const data = await res.json();
      alert(data.message);
    }
  } catch (err) {
    console.error("Error activando emergency stop:", err);
  }
}

// Toggle Autonomous
async function handleToggleAutonomous() {
  isAutonomous = !isAutonomous;
  try {
    const res = await fetch("/api/security/autonomous", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ enable: isAutonomous })
    });
    if (res.ok) {
      alert(`Modo Autónomo Experimental: ${isAutonomous ? "ACTIVADO 🟢" : "DESACTIVADO 🔴"}`);
    }
  } catch (err) {
    console.error("Error cambiando modo autónomo:", err);
  }
}

// Task Planner Submit
async function handlePlannerSubmit(e) {
  e.preventDefault();
  const input = document.getElementById("planner-input");
  const goal = input.value.trim();
  if (!goal) return;

  currentGoal = goal;
  const output = document.getElementById("planner-output");
  output.textContent = "⏳ Generando plan seguro estructurado...";

  try {
    const res = await fetch("/api/planner/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal })
    });
    if (res.ok) {
      const plan = await res.json();
      output.textContent = JSON.stringify(plan, null, 2);
      input.value = "";

      const approveBtn = document.getElementById("btn-approve-execute");
      approveBtn.style.display = "inline-flex";
    }
  } catch (err) {
    output.textContent = "Error generando plan.";
  }
}

// Extrae dinámicamente sitios web o nombres de programas sin harcodear
function parseGoalToActions(goalText) {
  const goalLower = goalText.toLowerCase();
  const actions = [];

  // Palabras clave ignorables
  const cleanText = goalLower
    .replace(/abri|abrir|anda a|ir a|buscar|navega a|entrar a|open/g, "")
    .trim();

  // Buscar URLs o nombres de dominios/servicios
  const words = cleanText.split(/\s+y\s+|\s+e\s+|,|;/);

  for (let w of words) {
    let token = w.trim();
    if (!token) continue;

    if (token.includes("facebook")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.facebook.com" });
    } else if (token.includes("youtube")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.youtube.com" });
    } else if (token.includes("instagram")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.instagram.com" });
    } else if (token.includes("twitter") || token.includes("x.com")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.twitter.com" });
    } else if (token.includes("reddit")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.reddit.com" });
    } else if (token.includes("twitch")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.twitch.tv" });
    } else if (token.includes("deeeep") || token.includes("deeep")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://deeeep.io" });
    } else if (token.includes("google")) {
      actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.google.com" });
    } else if (token.includes(".") || token.startsWith("http")) {
      let url = token.startsWith("http") ? token : "https://" + token;
      actions.push({ action_type: "OPEN_PROCESS", target: "start " + url });
    } else {
      // Intento dinámico genérico para sitios o procesos
      let url = `https://www.${token}.com`;
      actions.push({ action_type: "OPEN_PROCESS", target: "start " + url });
    }
  }

  if (actions.length === 0) {
    actions.push({ action_type: "OPEN_PROCESS", target: "start https://www.google.com" });
  }

  return actions;
}

// Aprobar y Ejecutar Secuencia Completa Dinámica en PC
async function handleApproveAndExecute() {
  const output = document.getElementById("planner-output");
  const approveBtn = document.getElementById("btn-approve-execute");
  approveBtn.textContent = "⏳ Ejecutando en PC...";

  const actionsToRun = parseGoalToActions(currentGoal);
  let executionResults = [];

  for (let act of actionsToRun) {
    try {
      const res = await fetch("/api/actions/authorize-execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          action_type: act.action_type,
          target: act.target,
          auth_token: "USER_APPROVED_TOKEN"
        })
      });
      if (res.ok) {
        const data = await res.json();
        executionResults.push(data);
      }
    } catch (err) {
      console.error("Error ejecutando paso:", err);
    }
  }

  output.textContent = `✅ SECUENCIA DINÁMICA COMPLETADA EN PC:\n` + JSON.stringify(executionResults, null, 2);
  approveBtn.textContent = "✅ APROBAR Y EJECUTAR EN PC";
  approveBtn.style.display = "none";

  fetch("/api/intent", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ description: `Ejecutado dinámicamente '${currentGoal}' en PC`, status: "SUCCESS" })
  }).then(() => fetchIntents());
}

// OCR Provider Selector
async function handleOCRChange(e) {
  const provider = e.target.value;
  try {
    const res = await fetch("/api/ocr/provider", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ provider })
    });
    if (res.ok) {
      fetchScene();
    }
  } catch (err) {
    console.error("Error cambiando proveedor OCR:", err);
  }
}

// Replay de Sesión
async function handleReplayFetch() {
  try {
    const res = await fetch("/api/replay");
    if (!res.ok) return;
    const replay = await res.json();
    alert(`📼 Replay de Sesión [${replay.session_id}]\nPasos grabados en memoria: ${replay.total_frames_recorded} cuadros.`);
  } catch (err) {
    console.error("Error obteniendo replay:", err);
  }
}

// Scene Description JSON
async function fetchScene() {
  try {
    const res = await fetch("/api/scene");
    if (!res.ok) return;
    const scene = await res.json();
    document.getElementById("scene-json").textContent = JSON.stringify(scene, null, 2);
  } catch (err) {
    console.error("Error cargando scene JSON:", err);
  }
}

// Log de Intenciones
async function fetchIntents() {
  try {
    const res = await fetch("/api/intents");
    if (!res.ok) return;
    const intents = await res.json();
    renderIntents(intents);
  } catch (err) {
    console.error("Error cargando intenciones:", err);
  }
}

function renderIntents(intents) {
  const container = document.getElementById("intents-list");
  if (!intents || intents.length === 0) {
    container.innerHTML = `<div style="font-size:10px; color:var(--text-dim);">Sin intenciones registradas.</div>`;
    return;
  }
  container.innerHTML = intents.map(i => `
    <div class="intent-item">
      <span class="intent-desc">${escapeHtml(i.description)}</span>
      <span class="intent-status">[${i.status}]</span>
    </div>
  `).join("");
}

async function handleIntentSubmit(e) {
  e.preventDefault();
  const input = document.getElementById("intent-input");
  const description = input.value.trim();
  if (!description) return;

  try {
    const res = await fetch("/api/intent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ description, status: "OK" })
    });
    if (res.ok) {
      input.value = "";
      fetchIntents();
    }
  } catch (err) {
    console.error("Error registrando intención:", err);
  }
}

// AntiGravity Question
async function handleQuestionSubmit(e) {
  e.preventDefault();
  const input = document.getElementById("question-input");
  const question = input.value.trim();
  if (!question) return;

  const output = document.getElementById("reasoning-output");
  output.textContent = "🤔 AntiGravity procesando contexto...";

  try {
    const res = await fetch("/api/question", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    if (res.ok) {
      const data = await res.json();
      output.textContent = `${data.answer}\n\nPlan Propuesto:\n` + data.proposed_plan.map(p => `  • Step ${p.step}: ${p.action} -> ${p.target} [${p.status}]`).join("\n");
      input.value = "";
    }
  } catch (err) {
    output.textContent = "Error consultando AntiGravity.";
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}
