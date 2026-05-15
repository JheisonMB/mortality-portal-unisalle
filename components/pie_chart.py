"""Pie chart: 10 municipalities with lowest mortality."""
import plotly.graph_objects as go

from data.processor import bottom10_mortality_cities


def pie_chart() -> go.Figure:
    df = bottom10_mortality_cities()
    fig = go.Figure(
        go.Pie(
            labels=df["MUNICIPIO"],
            values=df["TOTAL"],
            hole=0.35,
            hovertemplate="%{label}: %{value} muertes (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        title="10 municipios con menor índice de mortalidad — Colombia 2019",
        height=420,
        margin={"t": 60},
        legend={"orientation": "v"},
    )
    return fig
