"""Pie chart: 10 municipalities with lowest mortality."""
import plotly.graph_objects as go

from data.processor import bottom10_mortality_cities

_OCRE_PALETTE = ["#FDBE21", "#FED87C", "#FDCC53", "#FEE19A", "#FEECBD",
                 "#DE9F02", "#A27402", "#654801", "#332400", "#FFF5DC"]

_COLOR_DARK = "#332400"


def pie_chart() -> go.Figure:
    df = bottom10_mortality_cities()
    fig = go.Figure(
        go.Pie(
            labels=df["MUNICIPIO"],
            values=df["TOTAL"],
            hole=0.35,
            marker=dict(colors=_OCRE_PALETTE, line=dict(color="#FEECBD", width=2)),
            hovertemplate="%{label}: %{value} (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        title="Municipios con menor índice de mortalidad",
        height=420,
        margin={"t": 60},
        title_font={"size": 18, "color": _COLOR_DARK, "family": "Segoe UI"},
        legend={"orientation": "v", "yanchor": "middle", "y": 0.5},
        paper_bgcolor="#FFF5DC",
    )
    return fig
