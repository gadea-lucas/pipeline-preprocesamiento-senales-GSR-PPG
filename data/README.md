# Carpeta de datos

Esta carpeta contiene los datos locales utilizados por los notebooks de la raíz del repositorio.

Fuente actual:
- Dispositivo: plataforma de sensores wearable EmotiBit
- Sitio oficial: https://www.emotibit.com/
- Documentación: https://docs.emotibit.com/

## Entradas crudas

- `eda/`: una señal EDA completa por sujeto, guardada como `<user>.csv` con `Timestamp` y `EA`
- `ppg/`: una señal PPG completa por sujeto, guardada como `<user>.csv` con `Timestamp` y `PG`
- `stamps/`: un archivo de marcas temporales por sujeto, guardado como `<user>.txt`

Cada carpeta de señales contiene un CSV por sujeto (`S01.csv` a `S10.csv`).

El cargador de `data_layout.py` también acepta `LocalTimestamp` y lo normaliza a `Timestamp`.

## Segmentos de tareas

Los segmentos de tareas se reconstruyen a partir de los archivos locales de marcas temporales en `data/stamps/`:
- `baseline`: desde `relax_start` hasta `relax_end`
- `squat`: desde `squat_test_start` hasta `squat_test_end`
- `video1`: desde `video1_start` hasta `video1_end`
- `video2`: desde `video2_start` hasta `video2_end`

## Datasets derivados de aprendizaje automático

- `ml/emotion_2class_activation_raw_5s.csv`: tabla de características generada a partir de ventanas crudas de 5 segundos.
- `ml/emotion_2class_activation_processed_5s.csv`: tabla de características generada a partir de ventanas procesadas de 5 segundos.

Ambos archivos de aprendizaje automático incluyen:

- `user_id`: identificador del sujeto.
- `target`: etiqueta binaria de activación.
- `eda__...` y `ppg__...`: columnas de características generadas a partir de las ventanas EDA y PPG.

Estos archivos se generan con `relax_activation_dataset.ipynb`.
