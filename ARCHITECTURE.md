# 🏛️ Arquitectura: Agent Runtime Platform Infrastructure (v1.0)

> **Principios Fundamentales:**  
> Los Agentes Cambian (`Developer Agent`, `Browser Agent`, `Terminal Agent`).  
> La Plataforma Permanece (`Perception`, `Planning`, `Verified Execution`, `Knowledge`).

---

## 🏗️ La Arquitectura en Capas Completa

```text
                  Agentes de Aplicación
      ┌─────────────────┬─────────────────┬─────────────────┐
      │ Developer Agent │  Browser Agent  │ Terminal Agent  │
      └────────┬────────┴────────┬────────┴────────┬────────┘
               │                 │                 │
               ▼                 ▼                 ▼
─────────────────────────────────────────────────────────────────
                   Agent Runtime Platform
─────────────────────────────────────────────────────────────────
  ├── 1. Intent Router (Enrutador de 5 Vías: UI, Memoria, Plan, Acción, LLM)
  ├── 2. Goal Manager & Task Planner (Planificación Estructurada)
  ├── 3. Simulation Engine (Predicción de Escenas y Riesgo)
  ├── 4. Verification & Recovery Engine (Bucle Cerrado ExpectedState)
  ├── 5. Memory Runtime (Memoria 5-min + SQLite)
  ├── 6. Knowledge Runtime (Conocimiento Persistente L.P.)
  ├── 7. World State & Scene Graph (Contrato de Percepción Estable)
  ├── 8. Vision Runtime (DXGI/MSS 20 FPS + OCR)
  └── 9. Action Runtime (Ejecución Supervisada de Procesos y UI)
─────────────────────────────────────────────────────────────────
```

---

## 🧩 El Contrato Estable de SceneGraph

```json
{
  "windows": [{"title": "VS Code", "process": "Code.exe", "focused": true}],
  "browser": {
    "tabs": [{"index": 0, "title": "Vision Runtime", "active": true}],
    "url": "http://127.0.0.1:8080"
  },
  "terminal": {"cwd": "C:/vision_runtime", "last_command": "pytest", "status": "running"},
  "buttons": ["Run", "Stop", "Commit"],
  "inputs": [],
  "notifications": [],
  "dialogs": []
}
```

---

## 🧠 Knowledge Runtime vs Memory Runtime

* **`Memory Runtime` (Corto Plazo):** *"Hace 2 minutos la terminal arrojó una excepción."*
* **`Knowledge Runtime` (Largo Plazo):** *"La semana pasada este mismo error de Dockerfile se solucionó ajustando los permisos en el contenedor."*

---

## 🔄 El Bucle Continuo de la Plataforma

$$\text{OBSERVE} \longrightarrow \text{SIMULATE} \longrightarrow \text{PLAN} \longrightarrow \text{ACT} \longrightarrow \text{VERIFY} \longrightarrow \text{LEARN}$$
