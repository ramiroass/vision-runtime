# 🗺️ ROADMAP ESTRATÉGICO: Vision Runtime Platform

## 🎯 Vertical Principal: Developer Copilot (VS Code + Terminal + Git + GitHub)

En lugar de dispersar esfuerzos en decenas de plugins genéricos, la plataforma enfoca su evolución en el vertical **Developer Copilot** para resolver problemas reales de desarrollo de software.

---

## ✅ Versión 1.0 (Congelada)

* [x] **Core Observabilidad:** 5 Capas de Pipeline desacopladas con Event Bus Pub/Sub.
* [x] **Capa de Percepción:** Scene Builder JSON, OCR Multi-proveedor (FastOCR, Tesseract, EasyOCR), Frame Diffing.
* [x] **World State & Memoria:** Búfer rodante de 5 minutos, `events.db` y Session Replay.
* [x] **Task Planner & Safety Guardian:** Flujo seguro `OBSERVE ➔ PLAN ➔ SIMULATE ➔ APPROVAL` con Emergency Stop.
* [x] **Vertical Developer Copilot Plugin v1:** Plugin especializado para VS Code (`plugin_vscode`), Terminal (`plugin_terminal`) y GitHub (`plugin_github`).

---

## 🔮 Fases de Validación e Iteración (v1.1)

1. **Fase 1: Estabilización v1.0 (Sin nuevos módulos):**  
   * Mantenimiento y corrección de bugs únicamente.
2. **Fase 2: Ejecución de 100 a 500 Tareas Reales:**  
   * Medición empírica de CER/WER en OCR y latencias P50/P95/P99 en escenarios reales de código.
3. **Fase 3: Refinamiento del Developer Copilot:**  
   * Inspección profunda de stack traces, errores de pytest y logs de Docker en pantalla.
