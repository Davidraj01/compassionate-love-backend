import os
import sys
import glob

# 1. Add project directory to system path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. Auto-detect and add virtual environment site-packages if present
home_dir = os.path.expanduser('~')
possible_site_packages = [
    # Local project virtual environments
    *glob.glob(os.path.join(BASE_DIR, 'venv', 'lib', 'python*', 'site-packages')),
    *glob.glob(os.path.join(BASE_DIR, '.venv', 'lib', 'python*', 'site-packages')),
    *glob.glob(os.path.join(BASE_DIR, 'env', 'lib', 'python*', 'site-packages')),
    # cPanel / CloudLinux virtual environments
    *glob.glob(os.path.join(home_dir, 'virtualenv', '*', '*', 'lib', 'python*', 'site-packages')),
    *glob.glob(os.path.join(home_dir, 'virtualenv', '*', 'lib', 'python*', 'site-packages')),
]

for sp in possible_site_packages:
    if os.path.isdir(sp) and sp not in sys.path:
        sys.path.insert(0, sp)

# 3. Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clm_backend.settings')

# 4. Expose WSGI application with diagnostic fallback
try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    import traceback
    err_text = traceback.format_exc()
    
    # Fallback WSGI application so Passenger doesn't return blind 503
    def application(environ, start_response):
        status = '500 Internal Server Error'
        output = (
            f"<!DOCTYPE html><html><head><title>Backend Startup Error</title></head>"
            f"<body style='font-family:sans-serif;padding:2rem;background:#0B192C;color:#fff;'>"
            f"<h2 style='color:#FFD700;'>Compassionate Love of Calvary Ministries - Backend Startup Error</h2>"
            f"<p><strong>Python Executable:</strong> {sys.executable}</p>"
            f"<p><strong>Base Directory:</strong> {BASE_DIR}</p>"
            f"<h3>Error Traceback:</h3>"
            f"<pre style='background:rgba(255,255,255,0.08);padding:1rem;border-radius:8px;color:#ff7b72;overflow-x:auto;'>{err_text}</pre>"
            f"</body></html>"
        ).encode('utf-8')
        response_headers = [
            ('Content-Type', 'text/html; charset=utf-8'),
            ('Content-Length', str(len(output))),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With'),
        ]
        start_response(status, response_headers)
        return [output]


