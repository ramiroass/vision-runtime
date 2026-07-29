# 👁️ Desktop Agent Runtime for Perception, Planning and Verified Execution (v1.0)

> **Un runtime de escritorio modular para percepción visual, planificación supervisada y ejecución verificada en bucle cerrado (Closed-Loop Agentic OS).**

---

## 🏛️ Arquitectura del Sistema

```text
Desktop Agent Runtime
├── Vision Runtime (Captura DXGI/MSS 20 FPS + Scene Builder JSON + OCR)
├── Action Runtime (Ejecución de procesos, mouse, teclado, URLs)
├── Memory Runtime (Slotted 5-min Memory + SQLite events.db + Replay)
├── World State (Instantánea viva del estado del escritorio)
├── Planner (Task Planner estructurado multi-paso)
├── Goal Manager (Trazabilidad de objetivos a largo plazo)
├── Skills Engine (Habilidades compuestas de alto nivel)
├── Safety Guardian (Permission Manager + Emergency Stop Circuit Breaker)
├── Verification Engine (Validación de ExpectedState visual)
└── Recovery & Learning Engine (Estrategias de fallback y telemetría)
```

---

## 🎯 Vertical Principal: Developer Copilot (VS Code + Terminal + Git + GitHub + Docker)

El sistema enfoca su validación empírica exclusivamente en el entorno de desarrollo de software para responder a preguntas situacionales complejas:

* **`"¿Por qué falló este test en la terminal?"`**
* **`"¿Qué cambió exactamente desde el último commit?"`**
* **`"¿Qué ventana o popup apareció justo antes del error?"`**
* **`"¿Qué comando ejecuté hace 5 minutos?"`**

---

## ⚡ Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar el servidor Uvicorn
uvicorn app.api.server:app --host 127.0.0.1 --port 8080
```

Acceso a la Consola de Observabilidad en Vivo:
👉 **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

---

## 📊 Medición y Evaluación Empírica

| Tarea de Ejemplo | Tasa de Éxito (%) | Tiempo Promedio | Reintentos | Intervención Humana |
| :--- | :--- | :--- | :--- | :--- |
| **Abrir VS Code y verificar** | Pending (N=100) | ~1.8 s | 0 | No |
| **Ejecutar pytest en terminal** | Pending (N=100) | ~2.1 s | 0 | No |
| **Navegar a repositorio GitHub** | Pending (N=100) | ~1.4 s | 0 | No |
