# API de Predicción de Deserción Estudiantil

## Endpoint

**URL:** `http://127.0.0.1:8000/api/predict-dropout-risk/`  
**Método:** `POST`  
**Content-Type:** `application/json`

## Descripción

Esta API permite predecir el índice de riesgo de deserción estudiantil utilizando un modelo de machine learning (RandomForestClassifier) entrenado.

## Campos Requeridos

- `marital_status` (int): Estado civil
- `application_mode` (int): Modo de aplicación
- `application_order` (int): Orden de aplicación
- `course` (int): Curso
- `daytime_evening_attendance` (int): Asistencia diurna/nocturna
- `previous_qualification` (int): Calificación previa
- `nacionality` (int): Nacionalidad
- `mother_qualification` (int): Calificación de la madre
- `father_qualification` (int): Calificación del padre
- `mother_occupation` (int): Ocupación de la madre
- `father_occupation` (int): Ocupación del padre
- `gender` (int): Género
- `age_at_enrollment` (int): Edad al momento de inscripción

## Campos Opcionales

- `displaced` (int, default: 0): Desplazado
- `educational_special_needs` (int, default: 0): Necesidades educativas especiales
- `debtor` (int, default: 0): Deudor
- `tuition_fees_up_to_date` (int, default: 0): Matrícula al día
- `scholarship_holder` (int, default: 0): Beca
- `international` (int, default: 0): Internacional
- `curricular_units_1st_sem_credited` (int, default: 0)
- `curricular_units_1st_sem_enrolled` (int, default: 0)
- `curricular_units_1st_sem_evaluations` (int, default: 0)
- `curricular_units_1st_sem_approved` (int, default: 0)
- `curricular_units_1st_sem_grade` (float, default: 0.0)
- `curricular_units_1st_sem_without_evaluations` (int, default: 0)
- `curricular_units_2nd_sem_credited` (int, default: 0)
- `curricular_units_2nd_sem_enrolled` (int, default: 0)
- `curricular_units_2nd_sem_evaluations` (int, default: 0)
- `curricular_units_2nd_sem_approved` (int, default: 0)
- `curricular_units_2nd_sem_grade` (float, default: 0.0)
- `curricular_units_2nd_sem_without_evaluations` (int, default: 0)
- `unemployment_rate` (float, default: 0.0): Tasa de desempleo
- `inflation_rate` (float, default: 0.0): Tasa de inflación
- `gdp` (float, default: 0.0): PIB

## Ejemplo de Request

```json
{
    "marital_status": 1,
    "application_mode": 2,
    "application_order": 1,
    "course": 33,
    "daytime_evening_attendance": 1,
    "previous_qualification": 3,
    "nacionality": 1,
    "mother_qualification": 2,
    "father_qualification": 3,
    "mother_occupation": 4,
    "father_occupation": 5,
    "displaced": 0,
    "educational_special_needs": 0,
    "debtor": 1,
    "tuition_fees_up_to_date": 0,
    "gender": 1,
    "scholarship_holder": 0,
    "age_at_enrollment": 20,
    "international": 0,
    "curricular_units_1st_sem_credited": 2,
    "curricular_units_1st_sem_enrolled": 6,
    "curricular_units_1st_sem_evaluations": 5,
    "curricular_units_1st_sem_approved": 2,
    "curricular_units_1st_sem_grade": 12.5,
    "curricular_units_1st_sem_without_evaluations": 1,
    "curricular_units_2nd_sem_credited": 1,
    "curricular_units_2nd_sem_enrolled": 5,
    "curricular_units_2nd_sem_evaluations": 4,
    "curricular_units_2nd_sem_approved": 2,
    "curricular_units_2nd_sem_grade": 11.3,
    "curricular_units_2nd_sem_without_evaluations": 1,
    "unemployment_rate": 6.5,
    "inflation_rate": 2.1,
    "gdp": 1.7
}
```

## Ejemplo de Response (Éxito)

```json
{
    "success": true,
    "risk_score": 0.5933,
    "risk_percentage": 59.33,
    "risk_level": "Medio",
    "prediction": 1,
    "prediction_label": "Deserción",
    "message": "Índice de riesgo de deserción: 59.33% (Medio)"
}
```

## Ejemplo de Response (Error)

```json
{
    "success": false,
    "error": "Campos requeridos faltantes: marital_status, course"
}
```

## Niveles de Riesgo

- **Bajo:** risk_score < 0.3 (< 30%)
- **Medio:** 0.3 ≤ risk_score < 0.6 (30% - 60%)
- **Alto:** risk_score ≥ 0.6 (≥ 60%)

## Prueba con cURL

```bash
curl -X POST http://127.0.0.1:8000/api/predict-dropout-risk/ \
  -H "Content-Type: application/json" \
  -d '{
    "marital_status": 1,
    "application_mode": 2,
    "application_order": 1,
    "course": 33,
    "daytime_evening_attendance": 1,
    "previous_qualification": 3,
    "nacionality": 1,
    "mother_qualification": 2,
    "father_qualification": 3,
    "mother_occupation": 4,
    "father_occupation": 5,
    "gender": 1,
    "age_at_enrollment": 20
  }'
```

## Prueba con Python

```python
import requests
import json

url = "http://127.0.0.1:8000/api/predict-dropout-risk/"
data = {
    "marital_status": 1,
    "application_mode": 2,
    "application_order": 1,
    "course": 33,
    "daytime_evening_attendance": 1,
    "previous_qualification": 3,
    "nacionality": 1,
    "mother_qualification": 2,
    "father_qualification": 3,
    "mother_occupation": 4,
    "father_occupation": 5,
    "gender": 1,
    "age_at_enrollment": 20
}

response = requests.post(url, json=data)
print(response.json())
```

