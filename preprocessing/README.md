# Módulo de preprocesamiento

Esta carpeta contiene funciones auxiliares reutilizables para el pipeline de preprocesamiento de EDA/GSR y PPG.

## Archivos

- `filtering.py`
  - `gaussian_gsr`: suaviza una señal EDA/GSR con un filtro gaussiano.
  - `butterworth_bvp`: aplica un filtro Butterworth paso banda de 1-15 Hz a PPG/BVP.
  - `DigitalFilter`: filtro IIR simple de un polo, paso bajo/paso alto, basado en la lógica del firmware de EmotiBit.

- `hr.py`
  - `hr_emotibit`: detecta picos PPG con NeuroKit2 y estima la frecuencia cardiaca latido a latido usando la implementación local de `DigitalFilter`.

- `outliers.py`
  - `IQR`: reemplaza los valores atípicos detectados por IQR con `NaN`, interpola linealmente los valores faltantes y rellena los huecos restantes con la media de la columna.

- `resampling.py`
  - `resample_with_spline`: remuestrea una señal con marcas temporales a una frecuencia objetivo usando interpolación spline.

## Forma esperada de los datos

La mayoría de las funciones operan sobre entradas `pandas.DataFrame` con:

- una columna de tiempo, normalmente `Timestamp`
- una columna de señal, por ejemplo `EA`, `PG`, `Ppg` o `Signal`

Los notebooks pasan nombres de columnas explícitos cuando difieren de los valores por defecto.
