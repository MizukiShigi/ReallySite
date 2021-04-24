"""
WSGI config for ReallySite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
import sys
sys.path.append('/home/bitnami/htdocs/tbs/TBSblog/ReallySite')
# os.environ.setdefault("PYTHON_EGG_CACHE", "/home/bitnami/htdocs//tbs/TBSblog/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ReallySite.settings")
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ReallySite.settings')

application = get_wsgi_application()
