"""Line chart: total deaths per month."""
import plotly.graph_objects as go

from data.processor import deaths_by_month

_MONTH_NAMES = [
    "Ene", "Feb", "Mar", "Abr", "May", "Jun",
    "Jul", "Ago", "Sep", "Oct", "Nov", "Dic",
]


def line_chart() -> go.Figure:
    df = deaths_by_month()
    labels = [_MONTH_NAMES[int(m) - 1] for m in df["MES"]]
    fig = go.Figure(
        go.Scatter(
            x=labels,
            y=df["TOTAL"],
            mode="lines+markers",
            line={"color": "#e63946", "width": 2},
            marker={"size": 8},
            hovertemplate="%{x}: %{y:,.0f} muertes<extra></extra>",
        )
    )
    fig.update_layout(
        title="Total de muertes por mes — Colombia 2019",
        xaxis_title="Mes",
        yaxis_title="Total muertes",
        hovermode="x unified",
        height=400,
        margin={"t": 50},
    )
    return fig
