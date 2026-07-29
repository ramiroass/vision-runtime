# 🏗️ Arquitectura Completa: Desktop Agentic OS (Vision Runtime Platform)

> **Filosofía Fundamental:**  
> El Modelo de Lenguaje (LLM) NO es la aplicación entera; es un motor modular de razonamiento dentro de un Sistema Operativo para Agentes de Escritorio.

---

## 🏛️ El Pipeline de 10 Pasos Desacoplado

```text
                 Usuario
                    │
          Lenguaje natural
                    │
                    ▼
            Goal Manager (¿Qué quiere lograr?)
                    │
                    ▼
             Task Planner (¿Cómo lo hago?)
                    │
                    ▼
           Skill / Capability (¿Qué sé hacer?)
                    │
                    ▼
            Action Runtime (mouse, teclado, procesos)
                    │
                    ▼
           Vision Runtime (¿Qué pasó realmente?)
                    │
                    ▼
          Verification Engine (¿Coincide con lo esperado?)
                    │
        Sí ─────────┴──────── No
                    │                │
                    ▼                ▼
             siguiente paso    Recovery Engine (intenta otra estrategia)
                                     │
                                     ▼
                              Learning Engine
```

---

## 🧩 La Matriz de Decisión de Capacidades

```text
Objetivo del Usuario
  │
  ├── ¿Existe Plugin Especializado? (ej. VS Code Plugin)
  │     └── SÍ ➔ Ejecutar vía Plugin Especializado (Confianza 96%, Menor Latencia)
  │
  └── NO ➔ Usar Capability Genérica de Escritorio (Detección UI + Fallback OCR)
```

---

## 🔄 El Bucle Continuo Agentic

$$\text{OBSERVE} \longrightarrow \text{PLAN} \longrightarrow \text{ACT} \longrightarrow \text{VERIFY} \longrightarrow \text{LEARN} \longrightarrow \text{OBSERVE}$$

1. **`Vision Runtime` (Ojos):** Observación continua a 20 FPS (DXGI / MSS).
2. **`Action Runtime` (Manos):** Brazo robótico para mouse, teclado y procesos.
3. **`Memory Runtime` (Memoria):** Búfer rodante de 5 min y SQLite.
4. **`Planner` (Cerebro):** Descomposición de intenciones en Habilidades Compuestas (`Skills`).
5. **`Goal Manager` (Objetivo):** Control de metas a largo plazo.
6. **`LLM (AntiGravity Core)`:** Motor de razonamiento modular reemplazable (Gemini, Claude, GPT).
