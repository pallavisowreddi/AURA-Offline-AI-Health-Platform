import os
import sys
import traceback

# Ensure project root directory is at the beginning of sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

try:
    from app import app
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

# Vercel Serverless WSGI Handler
application = app

