"""Choropleth map: total deaths per department."""
import json

import plotly.express as px
import plotly.graph_objects as go

from data.loader import geojson_path
from data.processor import deaths_by_department


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
        color_continuous_scale="Reds",
        title="Distribución total de muertes por departamento — Colombia 2019",
        labels={"TOTAL": "Total muertes"},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0}, height=500)
    return fig
