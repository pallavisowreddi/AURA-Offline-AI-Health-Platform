import os
import sys
import traceback

# Ensure project root directory is at the beginning of sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app import app
    
    class VercelPathFix:
        """WSGI middleware to strip /api/index prefix added by Vercel serverless rewrites."""
        def __init__(self, wsgi_app):
            self.wsgi_app = wsgi_app

        def __call__(self, environ, start_response):
            path = environ.get('PATH_INFO', '')
            if path.startswith('/api/index'):
                path = path[len('/api/index'):]
                if not path or not path.startswith('/'):
                    path = '/' + path
                environ['PATH_INFO'] = path
            return self.wsgi_app(environ, start_response)

    app.wsgi_app = VercelPathFix(app.wsgi_app)
    application = app

except Exception as e:
    err_msg = traceback.format_exc()
    sys.stderr.write(f"[AURA STARTUP ERROR]\n{err_msg}\n")
    from flask import Flask, Response
    app = Flask(__name__)

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        return Response(
            f"<h2>AURA AI - Vercel Serverless Initialization Error</h2><pre style='background:#f4f4f4;padding:15px;border-radius:6px;border:1px solid #ccc;font-size:13px;'>{err_msg}</pre>",
            status=500,
            mimetype="text/html"
        )
    application = app
