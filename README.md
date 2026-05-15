# Mortalidad Colombia 2019 — Dashboard Interactivo

Aplicación web desarrollada con **Dash** y **Plotly** para analizar la mortalidad en Colombia (año 2019). Datos fuente: DANE — Estadísticas Vitales.

## Visualizaciones

| # | Tipo | Descripción |
|---|------|-------------|
| 1 | Mapa coroplético | Distribución total de muertes por departamento |
| 2 | Líneas | Total de muertes por mes |
| 3 | Barras horizontales | Top 5 ciudades más violentas (homicidios X95) |
| 4 | Circular (donut) | 10 municipios con menor índice de mortalidad |
| 5 | Tabla | Top 10 causas de muerte (código, nombre, total) |
| 6 | Barras apiladas | Muertes por sexo en cada departamento |
| 7 | Histograma | Distribución por grupo de edad (categorías DANE) |

## Desarrollo local

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
# → http://localhost:8050
```

## Despliegue en Render

1. Push el repositorio a GitHub.
2. Crea un nuevo **Web Service** en [render.com](https://render.com).
3. Conecta el repositorio — Render detecta `render.yaml` automáticamente.
4. Deploy.

## Despliegue en Railway

1. Push a GitHub.
2. Crea proyecto en [railway.app](https://railway.app) → **Deploy from GitHub repo**.
3. Railway detecta `Procfile` y ejecuta gunicorn.
4. En *Variables*, agrega `PORT=8050` si es necesario (Railway lo inyecta automáticamente).

## Estructura del proyecto

```
analytics/
├── app.py                  # Punto de entrada Dash
├── layout.py               # Ensamblaje del dashboard
├── data/
│   ├── loader.py           # Carga y caché de CSVs
│   └── processor.py        # Todas las agregaciones
├── components/
│   ├── map_chart.py
│   ├── line_chart.py
│   ├── bar_chart.py
│   ├── pie_chart.py
│   ├── stacked_bar.py
│   └── histogram.py
├── requirements.txt
├── Procfile                # Render / Railway / Heroku
└── render.yaml             # Render blueprint
```
