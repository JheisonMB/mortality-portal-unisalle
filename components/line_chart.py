"""Line chart: total deaths per month."""
import plotly.graph_objects as go

from data.processor import deaths_by_month

_MONTH_NAMES = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

_COLOR_BRIGHT = "#FDBE21"
_COLOR_DARK = "#332400"
_FONT = "Poppins, Segoe UI"


def line_chart() -> go.Figure:
    df = deaths_by_month()
    labels = [_MONTH_NAMES[int(m) - 1] for m in df["MES"]]
    fig = go.Figure(
        go.Scatter(
            x=labels,
            y=df["TOTAL"],
            mode="lines+markers",
            line={"color": _COLOR_BRIGHT, "width": 3},
            marker={"size": 9, "color": _COLOR_BRIGHT, "symbol": "circle", "line": {"width": 2, "color": "white"}},
            fill="tozeroy",
            fillcolor="rgba(253, 190, 33, 0.12)",
            hovertemplate="<b>%{x}</b><br>%{y:,.0f} muertes<extra></extra>",
        )
    )
    fig.update_layout(
        title="EVOLUCIÓN MENSUAL DE MUERTES",
        xaxis_title="MES",
        yaxis_title="TOTAL",
        hovermode="x unified",
        height=400,
        margin={"t": 60, "b": 50, "l": 60, "r": 40},
        title_font={"size": 16, "color": _COLOR_DARK, "family": _FONT, "weight": "bold"},
        title_x=0.05,
        xaxis={"showgrid": False, "tickfont": {"size": 11, "family": _FONT}},
        yaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.08)", "tickfont": {"size": 11, "family": _FONT}},
        plot_bgcolor="rgba(255, 255, 255, 0.6)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": _FONT, "color": _COLOR_DARK},
    )
    return fig
