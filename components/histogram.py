"""Histogram: deaths by DANE age-group category."""
import plotly.graph_objects as go

from data.processor import deaths_by_age_group


def histogram_age() -> go.Figure:
    df = deaths_by_age_group()
    fig = go.Figure(
        go.Bar(
            x=df["CATEGORIA"],
            y=df["TOTAL"],
            marker_color="#457b9d",
            hovertemplate="%{x}: %{y:,.0f} muertes<extra></extra>",
        )
    )
    fig.update_layout(
        title="Distribución de muertes por grupo de edad — Colombia 2019",
        xaxis_title="Categoría de edad",
        yaxis_title="Total muertes",
        xaxis_tickangle=-30,
        height=420,
        margin={"t": 60, "b": 120},
    )
    return fig
