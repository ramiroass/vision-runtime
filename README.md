# 👁️ Vision Runtime Platform v1.0

> **Plataforma de percepción, memoria, razonamiento y automatización supervisada para aplicaciones de escritorio, independiente de APIs y basada en observación de la interfaz gráfica.**

---

## 🎯 Problema que Resuelve

Muchas aplicaciones de escritorio (VS Code, Photoshop, Discord, Blender, Terminales, MetaTrader) carecen de APIs públicas abiertas o requieren configuraciones complejas. **Vision Runtime** observa la interfaz gráfica en tiempo real a 20 FPS, construye un árbol estructurado en JSON de lo que ocurre en pantalla, mantiene memoria histórica de 5 minutos y permite a motores de IA (AntiGravity, Gemini, GPT, Claude) responder preguntas y planificar asistencias sin tomar el control de tu PC.

---

## ⚡ Cómo Funciona (Pipeline de 6 Capas)

```text
Desktop (Windows)
   ↓
1. Capture Layer (DXGI / MSS continuous capture)
   ↓
2. Perception Layer (Scene Builder JSON + OCR Multi-provider)
   ↓
3. World State & Memory Layer (events.db + timeline.jsonl + 5-min Memory)
   ↓
4. Reasoning Runtime (AntiGravity Core Q&A)
   ↓
5. Planner & Policy Guardian (OBSERVE -> PLAN -> SIMULATE -> APPROVAL)
   ↓
6. Action Runtime & Plugins (Supervised Action Simulator)
```

---

## 🚀 Inicio Rápido

```bash
# 1. Clonar el repositorio e instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la plataforma
uvicorn app.api.server:app --host 127.0.0.1 --port 8080
```

Accede a la Consola de Observabilidad en Vivo:
👉 **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

---

## 💻 Ejemplo Real con Plugin VS Code

```python
import httpx

# Invocación al plugin especializado para VS Code
res = httpx.post("http://127.0.0.1:8080/api/plugins/run", json={"plugin_name": "plugin_vscode"})
print(res.json())
```

**Respuesta:**
```json
{
  "plugin": "plugin_vscode",
  "vscode_active": true,
  "active_file": "server.py",
  "terminal_status": "clean",
  "failing_test": "None",
  "git_status": "2 modified files, clean working tree",
  "confidence": 0.95
}
```
