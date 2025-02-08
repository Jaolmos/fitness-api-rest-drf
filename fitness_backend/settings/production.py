from .base import *

DEBUG = False

ALLOWED_HOSTS = []  # Añadir dominios permitidos en producción

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS
CORS_ALLOWED_ORIGINS = [
    # Añadir orígenes permitidos
]