"""Bar chart: top 5 most violent cities (firearm homicides X95*)."""
import plotly.graph_objects as go

from data.processor import top5_violent_cities

_COLOR_BRIGHT = "#FDBE21"
_COLOR_ACCENT = "#DE9F02"
_COLOR_DARK = "#332400"


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
            ),
            hovertemplate="%{y}: %{x:,.0f} homicidios<extra></extra>",
        )
    )
    fig.update_layout(
        title="Ciudades con mayor índice de homicidios",
        xaxis_title="Homicidios (arma de fuego)",
        yaxis_title="",
        height=380,
        margin={"t": 60, "l": 180},
        title_font={"size": 18, "color": _COLOR_DARK, "family": "Segoe UI"},
        xaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.05)"},
        plot_bgcolor="rgba(255, 245, 220, 0.3)",
    )
    return fig
