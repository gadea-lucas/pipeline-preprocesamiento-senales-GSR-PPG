# Módulo de métricas

Esta carpeta contiene las métricas de calidad de señal utilizadas por el notebook de preprocesamiento.

## Métricas EDA

`eda_metrics.py` implementa:

- `bottcher_quality`: puntuación de calidad de EDA basada en comprobaciones de línea cero y reglas de tasa de cambio de amplitud inspiradas en Bottcher et al.
- `kleckner_quality`: proporción de muestras EDA válidas usando reglas de rango, pendiente, temperatura opcional y vecindario inválido inspiradas en Kleckner et al.
- `kleckner_quality_filter`: envoltorio práctico que aplica la métrica de Kleckner con una ventana de suavizado de 2 segundos.

## Métricas PPG

`ppg_metrics.py` implementa:

- `maki_quality`: puntuación de fiabilidad Q_PHV basada en la varianza normalizada de la altura de los picos, tomada de la implementación RemotePPG en MATLAB de Maki et al.

## Interpretación

- Las puntuaciones de calidad EDA son proporciones en el rango `[0, 1]`, donde valores más altos indican mejor calidad.
- `maki_quality` devuelve una puntuación de varianza de altura de picos, donde valores más bajos indican amplitudes de picos PPG más estables.

Estas métricas se usan en `reproducible_pipeline.ipynb` para comparar la calidad de las señales crudas y preprocesadas.
