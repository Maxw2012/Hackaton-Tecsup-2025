# Hackathon TECSUP - Proyecto Django

Este es un proyecto de Django creado para el Hackathon TECSUP.

## Configuración del Proyecto

- **Python**: 3.13.5
- **Django**: 5.2.7
- **Base de datos**: SQLite (por defecto)

## Estructura del Proyecto

```
hackathon_tecsup/
├── __init__.py
├── asgi.py          # Configuración ASGI para despliegue
├── settings.py      # Configuración principal del proyecto
├── urls.py          # URLs principales del proyecto
└── wsgi.py          # Configuración WSGI para despliegue
```

## Comandos Útiles

### Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

### Crear una nueva aplicación
```bash
python manage.py startapp nombre_app
```

### Aplicar migraciones
```bash
python manage.py migrate
```

### Crear migraciones
```bash
python manage.py makemigrations
```

### Acceder al panel de administración
- URL: http://127.0.0.1:8000/admin/
- Usuario: admin
- Contraseña: admin123

## Próximos Pasos

1. Crear aplicaciones específicas para tu proyecto
2. Definir modelos de datos
3. Crear vistas y templates
4. Configurar URLs
5. Personalizar el panel de administración

¡Listo para comenzar el desarrollo!
