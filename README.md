# Predicción del nivel de desempeño en Saber 11

Proyecto integrador de Aprendizaje de Máquinas (metodología CRISP-DM).
Autor: Joan Camilo Galvis Barranco.

## Descripción
Modelo de clasificación que estima el nivel del puntaje global de un estudiante en la prueba
Saber 11 (**Bajo**: 0 a 199, **Medio**: 200 a 296, **Alto**: 297 a 500) usando solo información
sobre el estudiante, su familia y su colegio, sin usar los puntajes por materia.

- **Datos:** resultados de Saber 11, periodo 2020-2 (ICFES), publicados en datos.gov.co.
- **Modelo final:** XGBoost dentro de un pipeline completo (submuestreo aleatorio, imputación,
  codificación, escalado y modelo). Hiperparámetros: `max_depth=6`, `learning_rate=0.1`, `n_estimators=400`.
- **Desempeño en prueba:** F1 macro = 0,544; recall de 73 % en nivel Bajo y 75 % en nivel Alto.

## Archivos
| Archivo | Contenido |
|---|---|
| `app.py` | Aplicación web en Streamlit |
| `modelo_saber11.pkl` | Pipeline completo entrenado (serializado con joblib) |
| `label_encoder.pkl` | Codificador de la variable objetivo |
| `requirements.txt` | Librerías y versiones necesarias |
| `notebook/` | Notebook con todo el proceso CRISP-DM |

## Aplicación en línea
URL: https://saber11icfes-sintymmn5xcdqhfaobhk5m.streamlit.app/

## Limitaciones
- Los índices socioeconómicos del ICFES (INSE y nivel del colegio) no los conoce un usuario común;
  en la aplicación se sugiere un valor típico.
- Tiende a clasificar como Bajo o Alto a parte de los estudiantes de nivel Medio.
