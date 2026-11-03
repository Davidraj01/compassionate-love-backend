import os
import sys

# 1. Add project directory to system path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clm_backend.settings')

# 3. Expose WSGI application callable for Phusion Passenger / Apache / cPanel
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

