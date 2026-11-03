import os
import sys
import glob

# 1. Add application directory to python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# 2. Auto-switch to Virtual Environment Python if current Python is too old (< 3.10)
# Django 5 requires Python 3.10+. If Apache launches with system Python (e.g. 3.8/3.9), re-exec with virtualenv.
if sys.version_info < (3, 10):
    home_dir = os.path.expanduser('~')
    candidate_pythons = [
        *glob.glob(os.path.join(home_dir, 'virtualenv', '*', '*', 'bin', 'python3*')),
        *glob.glob(os.path.join(home_dir, 'virtualenv', '*', 'bin', 'python3*')),
        *glob.glob(os.path.join(BASE_DIR, 'venv', 'bin', 'python3*')),
        *glob.glob(os.path.join(BASE_DIR, '.venv', 'bin', 'python3*')),
    ]
    for py_bin in candidate_pythons:
        if os.path.isfile(py_bin) and os.access(py_bin, os.X_OK) and py_bin != sys.executable:
            try:
                os.execl(py_bin, py_bin, *sys.argv)
            except Exception:
                pass
            break

# 3. Add Virtual Environment site-packages to sys.path
home_dir = os.path.expanduser('~')
for sp in [
    *glob.glob(os.path.join(BASE_DIR, 'venv', 'lib', 'python*', 'site-packages')),
    *glob.glob(os.path.join(BASE_DIR, '.venv', 'lib', 'python*', 'site-packages')),
    *glob.glob(os.path.join(home_dir, 'virtualenv', '*', '*', 'lib', 'python*', 'site-packages')),
    *glob.glob(os.path.join(home_dir, 'virtualenv', '*', 'lib', 'python*', 'site-packages')),
]:
    if os.path.isdir(sp) and sp not in sys.path:
        sys.path.insert(0, sp)

# 4. Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clm_backend.settings')

# 5. Load Django WSGI application with self-diagnosing fallback
_django_app = None
_startup_error = None

try:
    from django.core.wsgi import get_wsgi_application
    _django_app = get_wsgi_application()
except Exception as e:
    import traceback
    _startup_error = traceback.format_exc()

def application(environ, start_response):
    """
    Primary WSGI Application.
    Includes built-in health check and error trap with CORS headers
    to prevent Apache from showing a blind 503 error page.
    """
    path = environ.get('PATH_INFO', '')
    
    # Built-in live health check (does not require database or Django views)
    if path in ['/health/', '/health', '/api/health/', '/api/health']:
        status = '200 OK'
        body = b'{"status": "healthy", "service": "compassionate-love-backend", "passenger": true}'
        headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(body))),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ]
        start_response(status, headers)
        return [body]

    # If Django failed to start, return the diagnostic error as JSON with CORS headers
    if _startup_error is not None:
        status = '500 Internal Server Error'
        import json
        error_json = json.dumps({
            'error': 'Django Backend Startup Failed on Hosting Server',
            'python_executable': sys.executable,
            'python_version': sys.version,
            'base_dir': BASE_DIR,
            'traceback': _startup_error
        }, indent=2).encode('utf-8')
        headers = [
            ('Content-Type', 'application/json'),
            ('Content-Length', str(len(error_json))),
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization'),
        ]
        start_response(status, headers)
        return [error_json]

    # Normal Django execution
    return _django_app(environ, start_response)
