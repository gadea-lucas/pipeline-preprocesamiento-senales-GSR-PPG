# Pipeline de preprocesamiento GSR/PPG

Este repositorio contiene un flujo de trabajo reproducible para preprocesar señales EDA/GSR y PPG recogidas con un dispositivo wearable EmotiBit.

El proyecto se organiza alrededor de dos notebooks:

- `reproducible_pipeline.ipynb`: carga las señales locales, segmenta cada sujeto por tarea, aplica el preprocesamiento, estima la frecuencia cardiaca a partir de PPG y compara métricas de calidad de señal antes y después del preprocesamiento.
- `relax_activation_dataset.ipynb`: construye datasets binarios de activación a partir de segmentos de relajación y activación, extrae características de series temporales y evalúa un clasificador Random Forest con validación cruzada agrupada por sujeto.

## 🗂️ Estructura del repositorio

- `data/`: archivos locales de señales, archivos de marcas temporales y datasets derivados para aprendizaje automático. Ver `data/README.md`.
- `data_layout.py`: funciones auxiliares compartidas para detectar sujetos, cargar señales, cargar marcas temporales y segmentar tareas.
- `preprocessing/`: funciones reutilizables de preprocesamiento para filtrado, tratamiento de valores atípicos, remuestreo y estimación de frecuencia cardiaca.
- `metrics/`: métricas de calidad de señal para EDA y PPG.
- `reproducible_pipeline.ipynb`: notebook de preprocesamiento completo y análisis de calidad.
- `relax_activation_dataset.ipynb`: notebook para generar y evaluar el dataset de clasificación binaria de activación.

## 📊 Supuestos sobre los datos

Los datos utilizados en este trabajo proceden del _dataset_ publicado en Zenodo:

**Physiological signals from three wearable devices recorded in real-world conditions**  

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.17985866-blue.svg)](https://doi.org/10.5281/zenodo.19218368)

> Los datos no se incluyen en el repositorio. Para reproducir los experimentos, debe descargarse el dataset original y colocar localmente en `data/` como se describe a continuación.

Los notebooks esperan un CSV de EDA, un CSV de PPG y un TXT de marcas temporales por sujeto:

- Archivos EDA: `data/eda/S01.csv` ... `data/eda/S10.csv`
- Archivos PPG: `data/ppg/S01.csv` ... `data/ppg/S10.csv`
- Archivos de marcas temporales: `data/stamps/S01.txt` ... `data/stamps/S10.txt`

Las señales deben incluir una columna de tiempo llamada `Timestamp` o `LocalTimestamp`. Los valores EDA se esperan en la columna `EA`; los valores PPG se esperan en la columna `PG`.

Los intervalos de cada tarea se reconstruyen a partir de los archivos de marcas temporales usando las etiquetas definidas en `data_layout.TASK_SEGMENTS`:

- `baseline`: `relax_start` hasta `relax_end`
- `squat`: `squat_test_start` hasta `squat_test_end`
- `video1`: `video1_start` hasta `video1_end`
- `video2`: `video2_start` hasta `video2_end`

## ⚙️ Pasos principales de procesamiento

El flujo de preprocesamiento combina:

- Suavizado de EDA con un filtro gaussiano.
- Filtrado paso banda de PPG con un filtro Butterworth de 1-15 Hz.
- Sustitución e interpolación de valores atípicos basada en IQR.
- Remuestreo mediante splines a rejillas temporales regulares.
- Estimación de frecuencia cardiaca latido a latido a partir de picos PPG.
- Métricas de calidad de EDA basadas en Bottcher et al. y Kleckner et al.
- Métrica de calidad de PPG basada en Maki et al.

El notebook de aprendizaje automático construye ventanas de 5 segundos y exporta tablas de características crudas y procesadas en `data/ml/`.

## 🐍 Dependencias de Python

Los notebooks y módulos auxiliares usan:

- `numpy`
- `pandas`
- `scipy`
- `neurokit2`
- `matplotlib`
- `seaborn`
- `tsfresh`
- `scikit-learn`
- `jupyterlab`
- `ipykernel`

Instala estas dependencias en tu entorno antes de ejecutar los notebooks:

```bash
pip install -r requirements.txt
```

## 🚀 Orden de ejecución sugerido

1. Abre `reproducible_pipeline.ipynb` para comprobar que los datos crudos se cargan y segmentan correctamente.
2. Ejecuta las secciones de preprocesamiento y calidad para revisar el impacto de los pasos de procesamiento.
3. Abre `relax_activation_dataset.ipynb` para generar los datasets crudos y procesados de aprendizaje automático.
4. Revisa los resultados de validación cruzada agrupada para comparar características crudas frente a procesadas.


## 👥 Autores
- David Martínez-Acha
- Gadea Lucas-Pérez
- Rodrigo Pacual-García
- Ana Serrano-Mamolar
- Álvar Arnaiz-González


## 📌 Cómo citar este software
Under review

[![status](https://img.shields.io/badge/status-under_review-yellow)]()

## 🏛️ Agradecimientos

Este trabajo es parte del proyecto de I+D+i PID2023-150694OA-I00, financiado por MICIU/AEI/10.13039/501100011033 y "FEDER/UE".

<p align="center" style="background-color: white; padding: 10px; border-radius: 15px;">
  <img src="img/MICIU.png" alt="MICIU Logo" width="350" />
</p>
