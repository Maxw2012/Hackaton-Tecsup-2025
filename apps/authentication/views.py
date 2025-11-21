from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from web_project import TemplateLayout
from web_project.template_helpers.theme import TemplateHelper


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to auth/urls.py file for more pages.
"""


class AuthView(TemplateView):
    # Predefined function
    def get_context_data(self, **kwargs):
        # A function to init the global layout. It is defined in web_project/__init__.py file
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Update the context
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context


def login_view(request):
    """
    Vista funcional de login que aparece en la raíz
    """
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    
    # Inicializar el layout
    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
    })
    
    if request.method == 'POST':
        username = request.POST.get('email-username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me')
        
        if username and password:
            # Intentar autenticar al usuario
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Login exitoso
                login(request, user)
                
                # Si no marcó "Remember Me", la sesión expirará al cerrar el navegador
                if not remember_me:
                    request.session.set_expiry(0)
                
                messages.success(request, f'¡Bienvenido, {user.username}!')
                next_url = request.GET.get('next', '/dashboard/')
                return redirect(next_url)
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        else:
            messages.error(request, 'Por favor, completa todos los campos.')
    
    return render(request, 'auth_login_basic.html', context)


def register_view(request):
    """
    Vista funcional de registro
    """
    # Si el usuario ya está autenticado, redirigir al dashboard
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    
    # Inicializar el layout
    context = TemplateLayout.init(request, {})
    context.update({
        "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
    })
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        terms = request.POST.get('terms')
        
        # Validaciones
        errors = []
        
        if not username:
            errors.append('El nombre de usuario es requerido.')
        elif len(username) < 3:
            errors.append('El nombre de usuario debe tener al menos 3 caracteres.')
        elif User.objects.filter(username=username).exists():
            errors.append('Este nombre de usuario ya está en uso.')
        
        if not email:
            errors.append('El email es requerido.')
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors.append('Por favor, ingresa un email válido.')
            else:
                if User.objects.filter(email=email).exists():
                    errors.append('Este email ya está registrado.')
        
        if not password:
            errors.append('La contraseña es requerida.')
        elif len(password) < 8:
            errors.append('La contraseña debe tener al menos 8 caracteres.')
        
        if not terms:
            errors.append('Debes aceptar los términos y condiciones.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            # Crear el usuario
            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                # Autenticar y hacer login automáticamente
                login(request, user)
                messages.success(request, f'¡Cuenta creada exitosamente! Bienvenido, {username}!')
                return redirect('/dashboard/')
            except Exception as e:
                messages.error(request, f'Error al crear la cuenta: {str(e)}')
    
    return render(request, 'auth_register_basic.html', context)


def logout_view(request):
    """
    Vista funcional de logout
    """
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('/')
