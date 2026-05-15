"""Bar chart: top 5 most violent cities (firearm homicides X95*)."""
import plotly.graph_objects as go

from data.processor import top5_violent_cities


def bar_chart_violent() -> go.Figure:
    df = top5_violent_cities().sort_values("HOMICIDIOS")
    fig = go.Figure(
        go.Bar(
            x=df["HOMICIDIOS"],
            y=df["MUNICIPIO"],
            orientation="h",
            marker_color="#e63946",
            hovertemplate="%{y}: %{x:,.0f} homicidios<extra></extra>",
        )
    )
    fig.update_layout(
        title="Top 5 ciudades más violentas — homicidios con arma de fuego (X95) 2019",
        xaxis_title="Homicidios",
        yaxis_title="Ciudad",
        height=380,
        margin={"t": 60, "l": 150},
    )
    return fig
