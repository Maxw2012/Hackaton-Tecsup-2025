from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
import json
import joblib
import pandas as pd
from pathlib import Path
from .models import StudentCharacteristics, DropoutPrediction

# Ruta al modelo
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODEL_PATH = BASE_DIR / "análisis" / "svm_model.pkl"

# Cargar el modelo una vez al iniciar (cache)
_model = None

def load_model():
    """Cargar el modelo una sola vez"""
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Modelo no encontrado en {MODEL_PATH}")
        _model = joblib.load(MODEL_PATH)
    return _model

@csrf_exempt
@require_http_methods(["POST"])
def predict_dropout_risk(request):
    """
    API endpoint para predecir el índice de riesgo de deserción estudiantil
    
    Recibe un JSON con los datos del estudiante y devuelve el índice de riesgo.
    """
    try:
        # Parsear JSON
        data = json.loads(request.body)
        
        # Validar y extraer datos
        student_data = {
            "Marital status": data.get("marital_status"),
            "Application mode": data.get("application_mode"),
            "Application order": data.get("application_order"),
            "Course": data.get("course"),
            "Daytime/evening attendance": data.get("daytime_evening_attendance"),
            "Previous qualification": data.get("previous_qualification"),
            "Nacionality": data.get("nacionality"),
            "Mother's qualification": data.get("mother_qualification"),
            "Father's qualification": data.get("father_qualification"),
            "Mother's occupation": data.get("mother_occupation"),
            "Father's occupation": data.get("father_occupation"),
            "Displaced": data.get("displaced", 0),
            "Educational special needs": data.get("educational_special_needs", 0),
            "Debtor": data.get("debtor", 0),
            "Tuition fees up to date": data.get("tuition_fees_up_to_date", 0),
            "Gender": data.get("gender"),
            "Scholarship holder": data.get("scholarship_holder", 0),
            "Age at enrollment": data.get("age_at_enrollment"),
            "International": data.get("international", 0),
            "Curricular units 1st sem (credited)": data.get("curricular_units_1st_sem_credited", 0),
            "Curricular units 1st sem (enrolled)": data.get("curricular_units_1st_sem_enrolled", 0),
            "Curricular units 1st sem (evaluations)": data.get("curricular_units_1st_sem_evaluations", 0),
            "Curricular units 1st sem (approved)": data.get("curricular_units_1st_sem_approved", 0),
            "Curricular units 1st sem (grade)": data.get("curricular_units_1st_sem_grade", 0.0),
            "Curricular units 1st sem (without evaluations)": data.get("curricular_units_1st_sem_without_evaluations", 0),
            "Curricular units 2nd sem (credited)": data.get("curricular_units_2nd_sem_credited", 0),
            "Curricular units 2nd sem (enrolled)": data.get("curricular_units_2nd_sem_enrolled", 0),
            "Curricular units 2nd sem (evaluations)": data.get("curricular_units_2nd_sem_evaluations", 0),
            "Curricular units 2nd sem (approved)": data.get("curricular_units_2nd_sem_approved", 0),
            "Curricular units 2nd sem (grade)": data.get("curricular_units_2nd_sem_grade", 0.0),
            "Curricular units 2nd sem (without evaluations)": data.get("curricular_units_2nd_sem_without_evaluations", 0),
            "Unemployment rate": data.get("unemployment_rate", 0.0),
            "Inflation rate": data.get("inflation_rate", 0.0),
            "GDP": data.get("gdp", 0.0),
        }
        
        # Validar campos requeridos
        required_fields = [
            "marital_status", "application_mode", "application_order", "course",
            "daytime_evening_attendance", "previous_qualification", "nacionality",
            "mother_qualification", "father_qualification", "mother_occupation",
            "father_occupation", "gender", "age_at_enrollment"
        ]
        
        missing_fields = [field for field in required_fields if data.get(field) is None]
        if missing_fields:
            return JsonResponse({
                'success': False,
                'error': f'Campos requeridos faltantes: {", ".join(missing_fields)}'
            }, status=400)
        
        # Convertir a DataFrame
        student_df = pd.DataFrame([student_data])
        
        # Cargar modelo y hacer predicción
        try:
            model = load_model()
            risk_score = model.predict_proba(student_df)[0][1]  # Probabilidad de deserción
            prediction = model.predict(student_df)[0]  # 0 = No deserta, 1 = Desertará
            
            # Clasificar el riesgo
            if risk_score < 0.3:
                risk_level = "Bajo"
            elif risk_score < 0.6:
                risk_level = "Medio"
            else:
                risk_level = "Alto"
            
            # Guardar predicción si se proporciona user_id o si el usuario está autenticado
            user_id = data.get("user_id")
            save_prediction = data.get("save_prediction", False)
            
            prediction_saved = False
            if save_prediction and user_id:
                try:
                    user = User.objects.get(id=user_id, is_staff=False)
                    # Buscar características del estudiante
                    try:
                        characteristics = StudentCharacteristics.objects.get(user=user)
                    except StudentCharacteristics.DoesNotExist:
                        characteristics = None
                    
                    # Crear o actualizar predicción
                    DropoutPrediction.objects.update_or_create(
                        user=user,
                        defaults={
                            'student_characteristics': characteristics,
                            'risk_score': float(risk_score),
                            'risk_percentage': float(risk_score * 100),
                            'risk_level': risk_level,
                            'prediction': int(prediction),
                            'prediction_label': 'Deserción' if prediction == 1 else 'No deserción',
                        }
                    )
                    prediction_saved = True
                except User.DoesNotExist:
                    pass
                except Exception as e:
                    # No fallar la respuesta si hay error al guardar
                    pass
            
            response_data = {
                'success': True,
                'risk_score': round(float(risk_score), 4),
                'risk_percentage': round(float(risk_score * 100), 2),
                'risk_level': risk_level,
                'prediction': int(prediction),
                'prediction_label': 'Deserción' if prediction == 1 else 'No deserción',
                'message': f'Índice de riesgo de deserción: {risk_score:.2%} ({risk_level})',
                'prediction_saved': prediction_saved
            }
            
            return JsonResponse(response_data)
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error al procesar la predicción: {str(e)}'
            }, status=500)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Formato JSON inválido'
        }, status=400)
    except FileNotFoundError as e:
        return JsonResponse({
            'success': False,
            'error': f'Modelo no encontrado: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }, status=500)

