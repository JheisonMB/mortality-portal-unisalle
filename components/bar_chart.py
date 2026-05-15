"""Bar chart: top 5 most violent cities (firearm homicides X95*)."""
import plotly.graph_objects as go

from data.processor import top5_violent_cities

_COLOR_BRIGHT = "#FDBE21"
_COLOR_ACCENT = "#DE9F02"
_COLOR_DARK = "#332400"
_FONT = "Poppins, Segoe UI"


def bar_chart_violent() -> go.Figure:
    df = top5_violent_cities().sort_values("HOMICIDIOS")
    fig = go.Figure(
        go.Bar(
            x=df["HOMICIDIOS"],
            y=df["MUNICIPIO"],
            orientation="h",
            marker=dict(
                color=df["HOMICIDIOS"],
                colorscale=[[0, _COLOR_ACCENT], [1, "#654801"]],
                showscale=False,
                line={"width": 0},
            ),
            hovertemplate="<b>%{y}</b><br>%{x:,.0f} homicidios<extra></extra>",
            text=df["HOMICIDIOS"],
            textposition="outside",
            textfont={"size": 12, "family": _FONT, "color": _COLOR_DARK},
        )
    )
    fig.update_layout(
        title="CIUDADES CON MAYOR ÍNDICE DE HOMICIDIOS",
        xaxis_title="HOMICIDIOS (ARMA DE FUEGO)",
        yaxis_title="",
        height=380,
        margin={"t": 60, "l": 200, "b": 50, "r": 40},
        title_font={"size": 16, "color": _COLOR_DARK, "family": _FONT, "weight": "bold"},
        title_x=0.05,
        xaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.08)", "tickfont": {"size": 11, "family": _FONT}},
        yaxis={"tickfont": {"size": 11, "family": _FONT}},
        plot_bgcolor="rgba(255, 255, 255, 0.5)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": _FONT, "color": _COLOR_DARK},
    )
    return fig
