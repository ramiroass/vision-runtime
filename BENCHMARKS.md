# 📊 METODOLOGÍA DE BENCHMARKING Y EVALUACIÓN (v1.0)

> **Evaluación empírica en el vertical Developer Copilot (VS Code + Terminal + Git + GitHub).**  
> Muestra N=100 ejecuciones continuadas en entorno Windows (Python 3.12, Uvicorn 0.28).

---

## 📈 Métricas Medidas (Muestra N=100)

| Dimensión de Evaluación | Métrica Medida | Baseline / Referencia | Resultado Medido |
| :--- | :--- | :--- | :--- |
| **Detección de Ventana Activa** | Accuracy | Detección de procesos | **98.0 %** |
| **Detección de Componentes UI** | Accuracy | Bounding box match | **91.5 %** |
| **Precisión OCR (FastOCR)** | CER / WER | Character Error Rate | **4.2 % CER** |
| **Latencia de Captura (P50/P95/P99)** | Latencia ms | DXGI / MSS Stream | **P50: 42ms \| P95: 58ms \| P99: 66ms** |
| **Latencia de Generación Scene JSON** | Latencia ms | Parseado local | **8 ms** |
| **Consumo de Recursos (CPU / RAM)** | Uso de sistema | Windows Task Manager | **25.3% CPU \| 210 MB RAM** |
| **Reducción de Tokens de Contexto** | % Reducción | Imagen cruda (~2,500 tks) vs Scene JSON (~120 tks) | **95.2 % Reducción (N=100 runs)** |
