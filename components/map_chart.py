"""Choropleth map: total deaths per department."""
import json

import plotly.express as px
import plotly.graph_objects as go

from data.loader import geojson_path
from data.processor import deaths_by_department

_COLOR_BRIGHT = "#FDBE21"
_COLOR_ACCENT = "#DE9F02"
_COLOR_DARK = "#332400"


def map_chart() -> go.Figure:
    df = deaths_by_department()
    with open(geojson_path(), encoding="utf-8") as f:
        geo = json.load(f)

    fig = px.choropleth(
        df,
        geojson=geo,
        locations="COD_DEPT",
        featureidkey="properties.DPTO",
        color="TOTAL",
        hover_name="DEPARTAMENTO",
        hover_data={"TOTAL": True, "COD_DEPT": False},
        color_continuous_scale=[[0, "#FFF5DC"], [0.5, "#FED87C"], [1, _COLOR_ACCENT]],
        title="Distribución de muertes por departamento",
        labels={"TOTAL": "Total"},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        height=500,
        title_font={"size": 18, "color": _COLOR_DARK, "family": "Segoe UI"},
        coloraxis_colorbar=dict(
            title="Muertes",
            tickfont={"size": 12, "color": _COLOR_DARK},
            thickness=12,
            len=0.7,
        ),
    )
    return fig
