from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.prediction.models import Curso, StudentCharacteristics, DropoutPrediction


class Command(BaseCommand):
    help = 'Crea datos por defecto para cursos, estudiantes y características'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina todos los datos existentes antes de crear nuevos',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Eliminando datos existentes...'))
            DropoutPrediction.objects.all().delete()
            StudentCharacteristics.objects.all().delete()
            Curso.objects.all().delete()
            # No eliminamos usuarios para evitar problemas

        # Crear cursos
        self.stdout.write(self.style.SUCCESS('Creando cursos...'))
        cursos_data = [
            {'codigo': 33, 'nombre': 'Bioinformática', 'descripcion': 'Curso de Bioinformática'},
            {'codigo': 171, 'nombre': 'Veterinaria', 'descripcion': 'Curso de Veterinaria'},
            {'codigo': 8014, 'nombre': 'Matemática', 'descripcion': 'Curso de Matemática'},
            {'codigo': 9003, 'nombre': 'Ingeniería Informática', 'descripcion': 'Curso de Ingeniería Informática'},
            {'codigo': 9070, 'nombre': 'Psicología', 'descripcion': 'Curso de Psicología'},
            {'codigo': 9085, 'nombre': 'Comunicación', 'descripcion': 'Curso de Comunicación'},
            {'codigo': 9119, 'nombre': 'Enfermería', 'descripcion': 'Curso de Enfermería'},
            {'codigo': 9130, 'nombre': 'Medicina', 'descripcion': 'Curso de Medicina'},
            {'codigo': 9147, 'nombre': 'Derecho', 'descripcion': 'Curso de Derecho'},
            {'codigo': 9238, 'nombre': 'Arquitectura', 'descripcion': 'Curso de Arquitectura'},
        ]

        cursos_created = 0
        for curso_data in cursos_data:
            curso, created = Curso.objects.get_or_create(
                codigo=curso_data['codigo'],
                defaults={
                    'nombre': curso_data['nombre'],
                    'descripcion': curso_data['descripcion'],
                    'activo': True
                }
            )
            if created:
                cursos_created += 1

        self.stdout.write(self.style.SUCCESS(f'✓ {cursos_created} cursos creados'))

        # Crear usuarios estudiantes si no existen
        self.stdout.write(self.style.SUCCESS('Creando usuarios estudiantes...'))
        estudiantes_data = [
            {
                'username': 'estudiante1',
                'email': 'estudiante1@tecsup.edu',
                'first_name': 'Juan',
                'last_name': 'Pérez',
                'password': 'estudiante123'
            },
            {
                'username': 'estudiante2',
                'email': 'estudiante2@tecsup.edu',
                'first_name': 'María',
                'last_name': 'García',
                'password': 'estudiante123'
            },
            {
                'username': 'estudiante3',
                'email': 'estudiante3@tecsup.edu',
                'first_name': 'Carlos',
                'last_name': 'López',
                'password': 'estudiante123'
            },
            {
                'username': 'estudiante4',
                'email': 'estudiante4@tecsup.edu',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'password': 'estudiante123'
            },
            {
                'username': 'estudiante5',
                'email': 'estudiante5@tecsup.edu',
                'first_name': 'Luis',
                'last_name': 'Rodríguez',
                'password': 'estudiante123'
            },
        ]

        estudiantes_created = 0
        for est_data in estudiantes_data:
            user, created = User.objects.get_or_create(
                username=est_data['username'],
                defaults={
                    'email': est_data['email'],
                    'first_name': est_data['first_name'],
                    'last_name': est_data['last_name'],
                    'is_staff': False,
                    'is_superuser': False,
                }
            )
            if created:
                user.set_password(est_data['password'])
                user.save()
                estudiantes_created += 1

        self.stdout.write(self.style.SUCCESS(f'✓ {estudiantes_created} estudiantes creados'))

        # Crear características de estudiantes
        self.stdout.write(self.style.SUCCESS('Creando características de estudiantes...'))
        estudiantes = User.objects.filter(is_staff=False)[:5]  # Tomar los primeros 5
        cursos = list(Curso.objects.all())

        caracteristicas_created = 0
        for i, estudiante in enumerate(estudiantes):
            curso = cursos[i % len(cursos)] if cursos else None
            
            characteristics, created = StudentCharacteristics.objects.get_or_create(
                user=estudiante,
                defaults={
                    'marital_status': 1,
                    'application_mode': 1 + (i % 3),
                    'application_order': 1,
                    'course': curso,
                    'daytime_evening_attendance': 1,
                    'previous_qualification': 1 + (i % 5),
                    'nacionality': 1,
                    'mother_qualification': 1 + (i % 4),
                    'father_qualification': 1 + (i % 4),
                    'mother_occupation': 1 + (i % 5),
                    'father_occupation': 1 + (i % 5),
                    'gender': 1 if i % 2 == 0 else 0,
                    'age_at_enrollment': 18 + (i % 5),
                    'displaced': 0 if i % 3 == 0 else 1,
                    'educational_special_needs': 0,
                    'debtor': 1 if i % 4 == 0 else 0,
                    'tuition_fees_up_to_date': 1 if i % 2 == 0 else 0,
                    'scholarship_holder': 1 if i % 3 == 0 else 0,
                    'international': 0,
                    'curricular_units_1st_sem_credited': 2 + (i % 3),
                    'curricular_units_1st_sem_enrolled': 5 + (i % 4),
                    'curricular_units_1st_sem_evaluations': 4 + (i % 3),
                    'curricular_units_1st_sem_approved': 2 + (i % 3),
                    'curricular_units_1st_sem_grade': 10.0 + (i * 1.5),
                    'curricular_units_1st_sem_without_evaluations': 1,
                    'curricular_units_2nd_sem_credited': 1 + (i % 2),
                    'curricular_units_2nd_sem_enrolled': 5 + (i % 3),
                    'curricular_units_2nd_sem_evaluations': 4 + (i % 2),
                    'curricular_units_2nd_sem_approved': 2 + (i % 2),
                    'curricular_units_2nd_sem_grade': 11.0 + (i * 1.2),
                    'curricular_units_2nd_sem_without_evaluations': 1,
                    'unemployment_rate': 5.5 + (i * 0.3),
                    'inflation_rate': 2.0 + (i * 0.1),
                    'gdp': 1.5 + (i * 0.2),
                }
            )
            if created:
                caracteristicas_created += 1

        self.stdout.write(self.style.SUCCESS(f'✓ {caracteristicas_created} características creadas'))

        self.stdout.write(self.style.SUCCESS('\n✓ Datos de prueba creados exitosamente!'))
        self.stdout.write(self.style.SUCCESS(f'  - Cursos: {Curso.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'  - Estudiantes: {User.objects.filter(is_staff=False).count()}'))
        self.stdout.write(self.style.SUCCESS(f'  - Características: {StudentCharacteristics.objects.count()}'))

