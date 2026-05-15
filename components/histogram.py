"""Histogram: deaths by DANE age-group category."""
import plotly.graph_objects as go

from data.processor import deaths_by_age_group

_COLOR_ACCENT = "#A27402"
_COLOR_DARK = "#332400"
_FONT = "Poppins, Segoe UI"


def histogram_age() -> go.Figure:
    df = deaths_by_age_group()
    fig = go.Figure(
        go.Bar(
            x=df["CATEGORIA"],
            y=df["TOTAL"],
            marker=dict(
                color=df["TOTAL"],
                colorscale=[[0, "#FFF9E6"], [0.4, "#FED87C"], [0.7, "#DE9F02"], [1, "#654801"]],
                showscale=False,
                line={"width": 0},
            ),
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} muertes<extra></extra>",
        )
    )
    fig.update_layout(
        title="DISTRIBUCIÓN POR GRUPO DE EDAD",
        xaxis_title="CATEGORÍA DE EDAD",
        yaxis_title="TOTAL",
        xaxis_tickangle=-30,
        height=420,
        margin={"t": 60, "b": 120, "l": 60, "r": 40},
        title_font={"size": 16, "color": _COLOR_DARK, "family": _FONT, "weight": "bold"},
        title_x=0.05,
        xaxis={"showgrid": False, "tickfont": {"size": 10, "family": _FONT}},
        yaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.08)", "tickfont": {"size": 11, "family": _FONT}},
        plot_bgcolor="rgba(255, 255, 255, 0.5)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": _FONT, "color": _COLOR_DARK},
    )
    return fig
