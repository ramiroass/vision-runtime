// ==========================================================================
// Vision Runtime - Application Logic (Sprint 5 & Action Sync)
// ==========================================================================

let isAutonomous = false;
let currentPlan = null;

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

  generateAndDisplayPlan(goal);
  input.value = "";
}

async function generateAndDisplayPlan(goalText) {
  const output = document.getElementById("planner-output");
  output.textContent = "⏳ Generando plan seguro estructurado...";

  try {
    const res = await fetch("/api/planner/plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ goal: goalText })
    });
    if (res.ok) {
      currentPlan = await res.json();
      output.textContent = JSON.stringify(currentPlan, null, 2);

      const approveBtn = document.getElementById("btn-approve-execute");
      approveBtn.style.display = "inline-flex";
    }
  } catch (err) {
    output.textContent = "Error generando plan.";
  }
}

// Aprobar y Ejecutar Secuencia desde el Plan Backend
async function handleApproveAndExecute() {
  if (!currentPlan) return;

  const output = document.getElementById("planner-output");
  const approveBtn = document.getElementById("btn-approve-execute");
  approveBtn.textContent = "⏳ Ejecutando en PC...";

  const actionTarget = currentPlan.final_command || `start ${currentPlan.resolved_url}`;
  const actionType = currentPlan.action_type || "OPEN_PROCESS";

  try {
    const res = await fetch("/api/actions/authorize-execute", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        action_type: actionType,
        target: actionTarget,
        auth_token: "USER_APPROVED_TOKEN"
      })
    });

    if (res.ok) {
      const result = await res.json();
      output.textContent = `✅ TRACE DE EJECUCIÓN SINCRO EN PC:\n` +
        `INPUT DEL USUARIO: ${currentPlan.input_user}\n` +
        `URL RESUELTA:     ${currentPlan.resolved_url}\n` +
        `COMANDO FINAL:    ${currentPlan.final_command}\n\n` +
        JSON.stringify(result, null, 2);

      approveBtn.textContent = "✅ APROBAR Y EJECUTAR EN PC";
      approveBtn.style.display = "none";

      fetch("/api/intent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: `Ejecutado '${currentPlan.input_user}' -> ${currentPlan.resolved_url}`, status: "SUCCESS" })
      }).then(() => fetchIntents());
    }
  } catch (err) {
    output.textContent = "Error ejecutando acción en PC.";
    approveBtn.textContent = "✅ APROBAR Y EJECUTAR EN PC";
  }
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

// AntiGravity Question + Auto Router a Task Planner si es una Orden de Acción
async function handleQuestionSubmit(e) {
  e.preventDefault();
  const input = document.getElementById("question-input");
  const question = input.value.trim();
  if (!question) return;

  const output = document.getElementById("reasoning-output");
  output.textContent = "🤔 AntiGravity procesando contexto...";

  // Si la pregunta es una orden de acción (ej. "abri...", "anda a..."), disparar también el Task Planner
  const qLower = question.toLowerCase();
  if (qLower.includes("abri") || qLower.includes("abrir") || qLower.includes("anda a") || qLower.includes("ir a")) {
    generateAndDisplayPlan(question);
  }

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
