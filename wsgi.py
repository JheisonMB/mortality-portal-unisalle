"""WSGI entry point for gunicorn."""
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO,
                    format="%(levelname)s %(name)s: %(message)s")

try:
    from app import server as application
    logging.info("app imported successfully; server=%s callable=%s",
                 type(application).__name__, callable(application))
except Exception:
    logging.exception("Failed to import app — check data files and dependencies")
    raise
