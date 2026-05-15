"""Histogram: deaths by DANE age-group category."""
import plotly.graph_objects as go

from data.processor import deaths_by_age_group

_COLOR_ACCENT = "#A27402"
_COLOR_DARK = "#332400"


def histogram_age() -> go.Figure:
    df = deaths_by_age_group()
    fig = go.Figure(
        go.Bar(
            x=df["CATEGORIA"],
            y=df["TOTAL"],
            marker=dict(
                color=df["TOTAL"],
                colorscale=[[0, "#FFF5DC"], [0.5, "#FED87C"], [1, _COLOR_ACCENT]],
                showscale=False,
            ),
            hovertemplate="%{x}: %{y:,.0f} muertes<extra></extra>",
        )
    )
    fig.update_layout(
        title="Distribución por grupo de edad",
        xaxis_title="Categoría de edad",
        yaxis_title="Total",
        xaxis_tickangle=-30,
        height=420,
        margin={"t": 60, "b": 120},
        title_font={"size": 18, "color": _COLOR_DARK, "family": "Segoe UI"},
        xaxis={"showgrid": False},
        yaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.05)"},
        plot_bgcolor="rgba(255, 245, 220, 0.3)",
    )
    return fig
