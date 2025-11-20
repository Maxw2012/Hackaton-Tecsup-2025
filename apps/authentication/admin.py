from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
import csv
import io


class UserAdmin(BaseUserAdmin):
    """
    Admin personalizado para el modelo User con funcionalidad de importar CSV
    """
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.admin_site.admin_view(self.import_csv_view), name='auth_user_import_csv'),
        ]
        return custom_urls + urls
    
    def import_csv_view(self, request):
        """
        Vista para importar usuarios desde un archivo CSV
        """
        if request.method == 'POST':
            csv_file = request.FILES.get('csv_file')
            
            if not csv_file:
                messages.error(request, 'Por favor, selecciona un archivo CSV.')
                return render(request, 'admin/import_csv.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            # Verificar que sea un archivo CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'El archivo debe ser un CSV (.csv)')
                return render(request, 'admin/import_csv.html', {
                    'opts': self.model._meta,
                    'has_view_permission': True,
                })
            
            try:
                # Leer el archivo CSV
                decoded_file = csv_file.read().decode('utf-8')
                io_string = io.StringIO(decoded_file)
                reader = csv.DictReader(io_string)
                
                created_count = 0
                updated_count = 0
                errors = []
                
                for row_num, row in enumerate(reader, start=2):  # Empezar en 2 porque la fila 1 es el header
                    try:
                        username = row.get('username', '').strip()
                        email = row.get('email', '').strip()
                        password = row.get('password', '').strip()
                        first_name = row.get('first_name', '').strip()
                        last_name = row.get('last_name', '').strip()
                        is_staff = row.get('is_staff', 'False').strip().lower() == 'true'
                        is_superuser = row.get('is_superuser', 'False').strip().lower() == 'true'
                        
                        # Validaciones básicas
                        if not username:
                            errors.append(f'Fila {row_num}: Username es requerido')
                            continue
                        
                        if not email:
                            errors.append(f'Fila {row_num}: Email es requerido')
                            continue
                        
                        if not password:
                            errors.append(f'Fila {row_num}: Password es requerido')
                            continue
                        
                        # Verificar si el usuario ya existe
                        user, created = User.objects.get_or_create(
                            username=username,
                            defaults={
                                'email': email,
                                'first_name': first_name,
                                'last_name': last_name,
                                'is_staff': is_staff,
                                'is_superuser': is_superuser,
                            }
                        )
                        
                        if created:
                            user.set_password(password)
                            user.save()
                            created_count += 1
                        else:
                            # Actualizar usuario existente
                            user.email = email
                            user.first_name = first_name
                            user.last_name = last_name
                            user.is_staff = is_staff
                            user.is_superuser = is_superuser
                            if password:  # Solo actualizar password si se proporciona
                                user.set_password(password)
                            user.save()
                            updated_count += 1
                            
                    except Exception as e:
                        errors.append(f'Fila {row_num}: Error - {str(e)}')
                        continue
                
                # Mostrar mensajes de resultado
                if created_count > 0:
                    messages.success(request, f'Se crearon {created_count} usuario(s) exitosamente.')
                if updated_count > 0:
                    messages.info(request, f'Se actualizaron {updated_count} usuario(s) existente(s).')
                if errors:
                    for error in errors[:10]:  # Mostrar solo los primeros 10 errores
                        messages.warning(request, error)
                    if len(errors) > 10:
                        messages.warning(request, f'... y {len(errors) - 10} error(es) más.')
                
                return redirect('admin:auth_user_changelist')
                
            except Exception as e:
                messages.error(request, f'Error al procesar el archivo CSV: {str(e)}')
        
        # GET request - mostrar formulario
        return render(request, 'admin/import_csv.html', {
            'opts': self.model._meta,
            'has_view_permission': True,
        })
    
    def changelist_view(self, request, extra_context=None):
        """
        Sobrescribir la vista de lista para agregar el botón de importar
        """
        extra_context = extra_context or {}
        extra_context['show_import_button'] = True
        extra_context['import_url'] = reverse('admin:auth_user_import_csv')
        return super().changelist_view(request, extra_context=extra_context)


# Desregistrar el UserAdmin por defecto y registrar el personalizado
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
