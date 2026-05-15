"""Pie chart: 10 municipalities with lowest mortality."""
import plotly.graph_objects as go

from data.processor import bottom10_mortality_cities

_OCRE_PALETTE = ["#FDBE21", "#FED87C", "#FDCC53", "#FEE19A", "#E8D273",
                 "#DE9F02", "#A27402", "#654801", "#332400", "#1A1200"]

_COLOR_DARK = "#332400"
_FONT = "Poppins, Segoe UI"


def pie_chart() -> go.Figure:
    df = bottom10_mortality_cities()
    fig = go.Figure(
        go.Pie(
            labels=df["MUNICIPIO"],
            values=df["TOTAL"],
            hole=0.35,
            marker=dict(colors=_OCRE_PALETTE, line=dict(color="white", width=2)),
            hovertemplate="<b>%{label}</b><br>%{value} casos (%{percent})<extra></extra>",
            textfont={"family": _FONT, "size": 11},
        )
    )
    fig.update_layout(
        title="MUNICIPIOS CON MENOR ÍNDICE DE MORTALIDAD",
        height=420,
        margin={"t": 60, "b": 40},
        title_font={"size": 16, "color": _COLOR_DARK, "family": _FONT, "weight": "bold"},
        title_x=0.05,
        legend={"orientation": "v", "yanchor": "middle", "y": 0.5, "font": {"size": 11, "family": _FONT}},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": _FONT, "color": _COLOR_DARK},
    )
    return fig
