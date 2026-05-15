"""Line chart: total deaths per month."""
import plotly.graph_objects as go

from data.processor import deaths_by_month

_MONTH_NAMES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

_COLOR_BRIGHT = "#FDBE21"
_COLOR_DARK = "#332400"


def line_chart() -> go.Figure:
    df = deaths_by_month()
    labels = [_MONTH_NAMES[int(m) - 1] for m in df["MES"]]
    fig = go.Figure(
        go.Scatter(
            x=labels,
            y=df["TOTAL"],
            mode="lines+markers",
            line={"color": _COLOR_BRIGHT, "width": 3},
            marker={"size": 8, "color": _COLOR_BRIGHT, "symbol": "circle"},
            fill="tozeroy",
            fillcolor="rgba(253, 190, 33, 0.15)",
            hovertemplate="%{x}: %{y:,.0f} muertes<extra></extra>",
        )
    )
    fig.update_layout(
        title="Evolución mensual de muertes",
        xaxis_title="Mes",
        yaxis_title="Total",
        hovermode="x unified",
        height=400,
        margin={"t": 50},
        title_font={"size": 18, "color": _COLOR_DARK, "family": "Segoe UI"},
        xaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.05)"},
        yaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.05)"},
        plot_bgcolor="rgba(255, 245, 220, 0.5)",
    )
    return fig
