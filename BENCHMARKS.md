# 📊 BENCHMARKS Y EVALUACIÓN DE UTILIDAD: Developer Vision Copilot

> **Status:** Pending empirical validation harness execution (N=100-500 test suite runs).

---

## 🎯 Batería de Benchmarks Planificada

### 1. Métricas Técnicas de Rendimiento
* [ ] **Window Detection Accuracy:** Porcentaje de acierto en identificación de ventana activa.
* [ ] **UI Component Detection Accuracy:** Precisión de bounding boxes en botones e inputs.
* [ ] **OCR CER / WER:** Character Error Rate y Word Error Rate en FastOCR vs Tesseract.
* [ ] **Reducción de Tokens:** Muestreo comparativo entre streaming de imágenes crudas vs Scene JSON Description.
* [ ] **Consumo de Recursos:** Uso promedio de CPU (%) y RAM (MB).

---

## ⏱️ Benchmarks de Utilidad (Tiempo Humano vs Copilot)

| Pregunta / Tarea | Tiempo Humano Estabilizado | Tiempo con Developer Vision Copilot |
| :--- | :--- | :--- |
| **Encontrar el archivo roto** | ~4 min | **~35 s** |
| **Encontrar el commit culpable** | ~8 min | **~1 min** |
| **Entender un stack trace complejo** | ~3 min | **~20 s** |
| **Localizar un test fallido** | ~5 min | **~40 s** |
