"""Choropleth map: total deaths per department."""
import json

import plotly.express as px
import plotly.graph_objects as go

from data.loader import geojson_path
from data.processor import deaths_by_department

_COLOR_BRIGHT = "#FDBE21"
_COLOR_ACCENT = "#DE9F02"
_COLOR_DARK = "#332400"
_FONT = "Poppins, Segoe UI"


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
        color_continuous_scale=[[0, "#FFF9E6"], [0.4, "#FED87C"], [0.7, _COLOR_ACCENT], [1, "#654801"]],
        title="DISTRIBUCIÓN DE MUERTES POR DEPARTAMENTO",
        labels={"TOTAL": "Total"},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin={"r": 0, "t": 60, "l": 0, "b": 0},
        height=500,
        title_font={"size": 16, "color": _COLOR_DARK, "family": _FONT, "weight": "bold"},
        title_x=0.05,
        coloraxis_colorbar=dict(
            title="<b>Muertes</b>",
            tickfont={"size": 11, "color": _COLOR_DARK, "family": _FONT},
            thickness=14,
            len=0.7,
            tickformat=",",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": _FONT, "color": _COLOR_DARK},
    )
    return fig
