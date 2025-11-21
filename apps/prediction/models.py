from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Curso(models.Model):
    """Modelo para representar los cursos disponibles"""
    codigo = models.IntegerField(unique=True, verbose_name="Código del Curso")
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Curso")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['codigo']

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class StudentCharacteristics(models.Model):
    """Modelo para almacenar las características de un estudiante"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_characteristics',
        verbose_name="Usuario",
        limit_choices_to={'is_staff': False}  # Solo usuarios que no son staff
    )
    
    # Información personal
    marital_status = models.IntegerField(verbose_name="Estado Civil")
    application_mode = models.IntegerField(verbose_name="Modo de Aplicación")
    application_order = models.IntegerField(verbose_name="Orden de Aplicación")
    course = models.ForeignKey(
        Curso,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        verbose_name="Curso"
    )
    daytime_evening_attendance = models.IntegerField(verbose_name="Asistencia Diurna/Nocturna")
    previous_qualification = models.IntegerField(verbose_name="Calificación Previa")
    nacionality = models.IntegerField(verbose_name="Nacionalidad")
    mother_qualification = models.IntegerField(verbose_name="Calificación de la Madre")
    father_qualification = models.IntegerField(verbose_name="Calificación del Padre")
    mother_occupation = models.IntegerField(verbose_name="Ocupación de la Madre")
    father_occupation = models.IntegerField(verbose_name="Ocupación del Padre")
    gender = models.IntegerField(verbose_name="Género")
    age_at_enrollment = models.IntegerField(verbose_name="Edad al Momento de Inscripción")
    
    # Campos opcionales
    displaced = models.IntegerField(default=0, verbose_name="Desplazado")
    educational_special_needs = models.IntegerField(default=0, verbose_name="Necesidades Educativas Especiales")
    debtor = models.IntegerField(default=0, verbose_name="Deudor")
    tuition_fees_up_to_date = models.IntegerField(default=0, verbose_name="Matrícula al Día")
    scholarship_holder = models.IntegerField(default=0, verbose_name="Becario")
    international = models.IntegerField(default=0, verbose_name="Internacional")
    
    # Unidades curriculares - Primer Semestre
    curricular_units_1st_sem_credited = models.IntegerField(default=0, verbose_name="Unidades Curriculares 1er Sem (Acreditadas)")
    curricular_units_1st_sem_enrolled = models.IntegerField(default=0, verbose_name="Unidades Curriculares 1er Sem (Inscritas)")
    curricular_units_1st_sem_evaluations = models.IntegerField(default=0, verbose_name="Unidades Curriculares 1er Sem (Evaluaciones)")
    curricular_units_1st_sem_approved = models.IntegerField(default=0, verbose_name="Unidades Curriculares 1er Sem (Aprobadas)")
    curricular_units_1st_sem_grade = models.FloatField(default=0.0, verbose_name="Unidades Curriculares 1er Sem (Nota)")
    curricular_units_1st_sem_without_evaluations = models.IntegerField(default=0, verbose_name="Unidades Curriculares 1er Sem (Sin Evaluaciones)")
    
    # Unidades curriculares - Segundo Semestre
    curricular_units_2nd_sem_credited = models.IntegerField(default=0, verbose_name="Unidades Curriculares 2do Sem (Acreditadas)")
    curricular_units_2nd_sem_enrolled = models.IntegerField(default=0, verbose_name="Unidades Curriculares 2do Sem (Inscritas)")
    curricular_units_2nd_sem_evaluations = models.IntegerField(default=0, verbose_name="Unidades Curriculares 2do Sem (Evaluaciones)")
    curricular_units_2nd_sem_approved = models.IntegerField(default=0, verbose_name="Unidades Curriculares 2do Sem (Aprobadas)")
    curricular_units_2nd_sem_grade = models.FloatField(default=0.0, verbose_name="Unidades Curriculares 2do Sem (Nota)")
    curricular_units_2nd_sem_without_evaluations = models.IntegerField(default=0, verbose_name="Unidades Curriculares 2do Sem (Sin Evaluaciones)")
    
    # Indicadores económicos
    unemployment_rate = models.FloatField(default=0.0, verbose_name="Tasa de Desempleo")
    inflation_rate = models.FloatField(default=0.0, verbose_name="Tasa de Inflación")
    gdp = models.FloatField(default=0.0, verbose_name="PIB")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Características del Estudiante"
        verbose_name_plural = "Características de los Estudiantes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Características de {self.user.username}"

    def to_dict(self):
        """Convierte las características a un diccionario para la predicción"""
        return {
            "marital_status": self.marital_status,
            "application_mode": self.application_mode,
            "application_order": self.application_order,
            "course": self.course.codigo if self.course else None,
            "daytime_evening_attendance": self.daytime_evening_attendance,
            "previous_qualification": self.previous_qualification,
            "nacionality": self.nacionality,
            "mother_qualification": self.mother_qualification,
            "father_qualification": self.father_qualification,
            "mother_occupation": self.mother_occupation,
            "father_occupation": self.father_occupation,
            "displaced": self.displaced,
            "educational_special_needs": self.educational_special_needs,
            "debtor": self.debtor,
            "tuition_fees_up_to_date": self.tuition_fees_up_to_date,
            "gender": self.gender,
            "scholarship_holder": self.scholarship_holder,
            "age_at_enrollment": self.age_at_enrollment,
            "international": self.international,
            "curricular_units_1st_sem_credited": self.curricular_units_1st_sem_credited,
            "curricular_units_1st_sem_enrolled": self.curricular_units_1st_sem_enrolled,
            "curricular_units_1st_sem_evaluations": self.curricular_units_1st_sem_evaluations,
            "curricular_units_1st_sem_approved": self.curricular_units_1st_sem_approved,
            "curricular_units_1st_sem_grade": self.curricular_units_1st_sem_grade,
            "curricular_units_1st_sem_without_evaluations": self.curricular_units_1st_sem_without_evaluations,
            "curricular_units_2nd_sem_credited": self.curricular_units_2nd_sem_credited,
            "curricular_units_2nd_sem_enrolled": self.curricular_units_2nd_sem_enrolled,
            "curricular_units_2nd_sem_evaluations": self.curricular_units_2nd_sem_evaluations,
            "curricular_units_2nd_sem_approved": self.curricular_units_2nd_sem_approved,
            "curricular_units_2nd_sem_grade": self.curricular_units_2nd_sem_grade,
            "curricular_units_2nd_sem_without_evaluations": self.curricular_units_2nd_sem_without_evaluations,
            "unemployment_rate": self.unemployment_rate,
            "inflation_rate": self.inflation_rate,
            "gdp": self.gdp,
        }


class DropoutPrediction(models.Model):
    """Modelo para almacenar las predicciones de deserción de los estudiantes"""
    RISK_LEVEL_CHOICES = [
        ('Bajo', 'Bajo'),
        ('Medio', 'Medio'),
        ('Alto', 'Alto'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='dropout_predictions',
        verbose_name="Usuario",
        limit_choices_to={'is_staff': False}
    )
    student_characteristics = models.ForeignKey(
        StudentCharacteristics,
        on_delete=models.CASCADE,
        related_name='predictions',
        verbose_name="Características del Estudiante",
        null=True,
        blank=True
    )
    
    risk_score = models.FloatField(verbose_name="Índice de Riesgo")
    risk_percentage = models.FloatField(verbose_name="Porcentaje de Riesgo")
    risk_level = models.CharField(
        max_length=10,
        choices=RISK_LEVEL_CHOICES,
        verbose_name="Nivel de Riesgo"
    )
    prediction = models.IntegerField(verbose_name="Predicción")  # 0 = No deserta, 1 = Desertará
    prediction_label = models.CharField(max_length=50, verbose_name="Etiqueta de Predicción")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Predicción")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

    class Meta:
        verbose_name = "Predicción de Deserción"
        verbose_name_plural = "Predicciones de Deserción"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['risk_level']),
        ]

    def __str__(self):
        return f"Predicción de {self.user.username} - {self.risk_percentage:.2f}% ({self.risk_level})"
