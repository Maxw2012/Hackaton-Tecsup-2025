from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.db import transaction
from .models import Curso, StudentCharacteristics, DropoutPrediction


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'activo', 'created_at']
    list_filter = ['activo', 'created_at']
    search_fields = ['codigo', 'nombre', 'descripcion']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(StudentCharacteristics)
class StudentCharacteristicsAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'age_at_enrollment', 'gender', 'created_at']
    list_filter = ['course', 'gender', 'marital_status', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Información del Usuario', {
            'fields': ('user', 'course')
        }),
        ('Información Personal', {
            'fields': (
                'marital_status', 'application_mode', 'application_order',
                'daytime_evening_attendance', 'previous_qualification',
                'nacionality', 'gender', 'age_at_enrollment'
            )
        }),
        ('Información Familiar', {
            'fields': (
                'mother_qualification', 'father_qualification',
                'mother_occupation', 'father_occupation'
            )
        }),
        ('Estado Académico', {
            'fields': (
                'displaced', 'educational_special_needs', 'debtor',
                'tuition_fees_up_to_date', 'scholarship_holder', 'international'
            )
        }),
        ('Unidades Curriculares - Primer Semestre', {
            'fields': (
                'curricular_units_1st_sem_credited',
                'curricular_units_1st_sem_enrolled',
                'curricular_units_1st_sem_evaluations',
                'curricular_units_1st_sem_approved',
                'curricular_units_1st_sem_grade',
                'curricular_units_1st_sem_without_evaluations',
            ),
            'classes': ('collapse',)
        }),
        ('Unidades Curriculares - Segundo Semestre', {
            'fields': (
                'curricular_units_2nd_sem_credited',
                'curricular_units_2nd_sem_enrolled',
                'curricular_units_2nd_sem_evaluations',
                'curricular_units_2nd_sem_approved',
                'curricular_units_2nd_sem_grade',
                'curricular_units_2nd_sem_without_evaluations',
            ),
            'classes': ('collapse',)
        }),
        ('Indicadores Económicos', {
            'fields': ('unemployment_rate', 'inflation_rate', 'gdp'),
            'classes': ('collapse',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DropoutPrediction)
class DropoutPredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'risk_percentage', 'risk_level', 'prediction_label', 'created_at']
    list_filter = ['risk_level', 'prediction', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    change_list_template = 'admin/prediction/dropoutprediction/change_list.html'
    
    fieldsets = (
        ('Información del Estudiante', {
            'fields': ('user', 'student_characteristics')
        }),
        ('Resultados de la Predicción', {
            'fields': (
                'risk_score', 'risk_percentage', 'risk_level',
                'prediction', 'prediction_label'
            )
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('predict-all-students/', self.admin_site.admin_view(self.predict_all_students_view), name='prediction_dropoutprediction_predict_all'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_predict_all_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

    def predict_all_students_view(self, request):
        """Vista para ejecutar predicción de todos los estudiantes"""
        if not request.user.is_staff:
            messages.error(request, 'No tienes permisos para realizar esta acción.')
            return redirect('admin:prediction_dropoutprediction_changelist')
        
        from django.contrib.auth.models import User
        from .models import StudentCharacteristics
        from .views import load_model
        import pandas as pd
        
        try:
            # Obtener todos los usuarios que no son staff (estudiantes)
            students = User.objects.filter(is_staff=False)
            
            if not students.exists():
                messages.warning(request, 'No hay estudiantes registrados.')
                return redirect('admin:prediction_dropoutprediction_changelist')
            
            # Cargar el modelo
            model = load_model()
            
            predictions_created = 0
            predictions_updated = 0
            errors = []
            
            with transaction.atomic():
                for student in students:
                    try:
                        # Obtener o crear características del estudiante
                        characteristics, created = StudentCharacteristics.objects.get_or_create(
                            user=student,
                            defaults={
                                'marital_status': 1,
                                'application_mode': 1,
                                'application_order': 1,
                                'daytime_evening_attendance': 1,
                                'previous_qualification': 1,
                                'nacionality': 1,
                                'mother_qualification': 1,
                                'father_qualification': 1,
                                'mother_occupation': 1,
                                'father_occupation': 1,
                                'gender': 1,
                                'age_at_enrollment': 20,
                            }
                        )
                        
                        # Validar que tenga curso asignado
                        if not characteristics.course:
                            errors.append(f"Estudiante {student.username} no tiene curso asignado")
                            continue
                        
                        # Convertir características al formato que espera el modelo
                        student_data = {
                            "Marital status": characteristics.marital_status,
                            "Application mode": characteristics.application_mode,
                            "Application order": characteristics.application_order,
                            "Course": characteristics.course.codigo,
                            "Daytime/evening attendance": characteristics.daytime_evening_attendance,
                            "Previous qualification": characteristics.previous_qualification,
                            "Nacionality": characteristics.nacionality,
                            "Mother's qualification": characteristics.mother_qualification,
                            "Father's qualification": characteristics.father_qualification,
                            "Mother's occupation": characteristics.mother_occupation,
                            "Father's occupation": characteristics.father_occupation,
                            "Displaced": characteristics.displaced,
                            "Educational special needs": characteristics.educational_special_needs,
                            "Debtor": characteristics.debtor,
                            "Tuition fees up to date": characteristics.tuition_fees_up_to_date,
                            "Gender": characteristics.gender,
                            "Scholarship holder": characteristics.scholarship_holder,
                            "Age at enrollment": characteristics.age_at_enrollment,
                            "International": characteristics.international,
                            "Curricular units 1st sem (credited)": characteristics.curricular_units_1st_sem_credited,
                            "Curricular units 1st sem (enrolled)": characteristics.curricular_units_1st_sem_enrolled,
                            "Curricular units 1st sem (evaluations)": characteristics.curricular_units_1st_sem_evaluations,
                            "Curricular units 1st sem (approved)": characteristics.curricular_units_1st_sem_approved,
                            "Curricular units 1st sem (grade)": characteristics.curricular_units_1st_sem_grade,
                            "Curricular units 1st sem (without evaluations)": characteristics.curricular_units_1st_sem_without_evaluations,
                            "Curricular units 2nd sem (credited)": characteristics.curricular_units_2nd_sem_credited,
                            "Curricular units 2nd sem (enrolled)": characteristics.curricular_units_2nd_sem_enrolled,
                            "Curricular units 2nd sem (evaluations)": characteristics.curricular_units_2nd_sem_evaluations,
                            "Curricular units 2nd sem (approved)": characteristics.curricular_units_2nd_sem_approved,
                            "Curricular units 2nd sem (grade)": characteristics.curricular_units_2nd_sem_grade,
                            "Curricular units 2nd sem (without evaluations)": characteristics.curricular_units_2nd_sem_without_evaluations,
                            "Unemployment rate": characteristics.unemployment_rate,
                            "Inflation rate": characteristics.inflation_rate,
                            "GDP": characteristics.gdp,
                        }
                        
                        # Convertir a DataFrame
                        student_df = pd.DataFrame([student_data])
                        
                        # Hacer predicción
                        risk_score = model.predict_proba(student_df)[0][1]
                        prediction = model.predict(student_df)[0]
                        
                        # Clasificar el riesgo
                        if risk_score < 0.3:
                            risk_level = "Bajo"
                        elif risk_score < 0.6:
                            risk_level = "Medio"
                        else:
                            risk_level = "Alto"
                        
                        # Crear o actualizar predicción
                        prediction_obj, created = DropoutPrediction.objects.update_or_create(
                            user=student,
                            defaults={
                                'student_characteristics': characteristics,
                                'risk_score': float(risk_score),
                                'risk_percentage': float(risk_score * 100),
                                'risk_level': risk_level,
                                'prediction': int(prediction),
                                'prediction_label': 'Deserción' if prediction == 1 else 'No deserción',
                            }
                        )
                        
                        if created:
                            predictions_created += 1
                        else:
                            predictions_updated += 1
                            
                    except Exception as e:
                        errors.append(f"Error con estudiante {student.username}: {str(e)}")
                        continue
            
            # Mostrar mensajes
            if predictions_created > 0:
                messages.success(request, f'Se crearon {predictions_created} nuevas predicciones.')
            if predictions_updated > 0:
                messages.info(request, f'Se actualizaron {predictions_updated} predicciones existentes.')
            if errors:
                messages.warning(request, f'Se encontraron {len(errors)} errores durante el proceso.')
                for error in errors[:10]:  # Mostrar solo los primeros 10 errores
                    messages.warning(request, error)
            
        except Exception as e:
            messages.error(request, f'Error al procesar las predicciones: {str(e)}')
        
        return redirect('admin:prediction_dropoutprediction_changelist')
