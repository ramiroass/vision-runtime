# 👁️ Developer Vision Copilot v1.0

> **Un copiloto que entiende el contexto completo del entorno de desarrollo observando la pantalla y combinándolo con información estructurada. No intenta reemplazar VS Code, GitHub o ChatGPT; los conecta.**

---

## 🌟 Las 5 Capacidades Estrellas

1. **🛠️ Build Analyzer ("¿Por qué falló el build?"):**  
   Analiza terminales, stack traces, el archivo abierto y los últimos cambios para indicar exactamente por dónde empezar.
2. **🔀 Git Context ("¿Qué cambió desde ayer?"):**  
   No solo muestra un diff, sino que explica el impacto potencial de los cambios en el proyecto.
3. **🔍 Pull Request Inspector ("Inspeccioná este PR"):**  
   Lee GitHub, checks de CI/CD, comentarios y tests para generar un diagnóstico inmediato.
4. **🧠 Workspace Memory ("¿En qué estaba trabajando hace media hora?"):**  
   Recupera el contexto de trabajo y las ventanas activas tras interrupciones.
5. **📼 Error Replay ("Mostrame cómo llegué a este error"):**  
   Reconstruye cuadro por cuadro el historial visual y de eventos previa a la excepción.

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
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la plataforma
uvicorn app.api.server:app --host 127.0.0.1 --port 8080
```

Accede a la Consola de Observabilidad en Vivo:
👉 **[http://127.0.0.1:8080](http://127.0.0.1:8080)**
