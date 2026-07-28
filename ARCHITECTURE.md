# 🏗️ Arquitectura del Sistema: Vision Runtime v1.0

```text
Desktop

↓

Capture Runtime (DXGI / MSS)

↓

Vision Runtime (Frame Diff, OCR, UI Detector, Scene Builder)

↓

World State (Estado global vivo del escritorio)

↓

Memory Runtime (events.db, timeline.jsonl, 5-Min Rolling Memory, Session Replay)

↓

Reasoning Runtime (AntiGravity Engine)

↓

Planner (Task Planner de Asistencia)

↓

Guardian (Policy Engine & Emergency Stop Circuit Breaker)

↓

Action Runtime (Ejecución Supervisada de Acciones)

↓

Plugins (VS Code, GitHub, Terminal)
```

## 🧩 Descripción de Componentes Desacoplados

1. **Capture Runtime:** Motor puro de captura en baja latencia. Emite eventos pub/sub (`FRAME_CAPTURED`, `WINDOW_CHANGED`).
2. **Vision Runtime:** Procesa cuadros y construye el objeto ligero `JSON Scene Description`.
3. **World State:** Mantiene una instantánea viva del estado del escritorio para consultas inmediatas del Planner.
4. **Memory Runtime:** Almacena eventos en SQLite, stream en `timeline.jsonl` y búfer circular de 5 minutos.
5. **Reasoning Runtime:** Motor AntiGravity que razona sobre contexto JSON sin procesar píxeles crudos.
6. **Guardian & Action Runtime:** Cortafuegos de seguridad con token del usuario y botón `🚨 EMERGENCY STOP`.
