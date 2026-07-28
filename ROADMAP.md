# 🗺️ ROADMAP DE DESARROLLO: Vision Runtime

## ✅ Implementado en la Versión 1.0

* [x] **Capture Layer:** Captura continuada DXGI/MSS a FPS configurables (10, 20, 30, 60 FPS).
* [x] **Vision Runtime:** Frame diffing, OCR Multi-proveedor (FastOCR, Tesseract, EasyOCR), detector UI y Scene Builder JSON.
* [x] **World State:** Instantánea viva del estado del escritorio en memoria.
* [x] **Memory Runtime:** Base de datos SQLite (`events.db`), Stream log (`timeline.jsonl`), Memoria rodante de 5 minutos y Session Replay.
* [x] **Reasoning Runtime:** antiGravity Core v3.0 Q&A sobre contextos JSON.
* [x] **Task Planner:** Planificación segura en 4 fases (`OBSERVE` ➔ `PLAN` ➔ `SIMULATE` ➔ `APPROVAL`).
* [x] **Guardian & Action Runtime:** Permission Manager, Emergency Stop Circuit Breaker e integrador de acciones supervisadas.
* [x] **Plugins:** Plugin especializado para VS Code, Terminal y GitHub.

---

## 🔮 Planificado para Próximos Releases

* [ ] **Plugin Excel:** Analizador de hojas de cálculo y tablas.
* [ ] **Plugin Photoshop / Blender:** Observador de proyectos de diseño y canvas.
* [ ] **Soporte Multi-Monitor:** Captura simultánea de pantallas secundarias.
* [ ] **Soporte Linux & macOS:** Adaptadores de captura nativos para X11/Wayland y Quartz.
