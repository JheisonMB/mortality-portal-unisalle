"""Dash application entry point."""
import dash

from layout import build_layout

app = dash.Dash(
    __name__,
    title="Mortalidad Colombia 2019",
    update_title=None,
)
server = app.server  # expose Flask server for gunicorn

# Pass function reference; Dash calls it on first request.
# Data functions use @lru_cache so aggregations compute only once.
app.layout = build_layout

# Re-assign so Render's auto-detection (gunicorn app:app) gets a callable Flask WSGI app.
app = server

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8050)
