"""Stacked bar: deaths by sex per department."""
import plotly.graph_objects as go

from data.processor import deaths_by_sex_department

_SEX_COLORS = {
    "Masculino": "#1d3557",
    "Femenino": "#e63946",
    "Indeterminado": "#a8dadc",
}


def stacked_bar_chart() -> go.Figure:
    df = deaths_by_sex_department()
    depts = df["DEPARTAMENTO"].unique()

    fig = go.Figure()
    for sexo, color in _SEX_COLORS.items():
        subset = df[df["SEXO_LABEL"] == sexo].set_index("DEPARTAMENTO").reindex(depts)
        fig.add_trace(
            go.Bar(
                name=sexo,
                x=depts,
                y=subset["TOTAL"].fillna(0),
                marker_color=color,
                hovertemplate=f"{sexo} — %{{x}}: %{{y:,.0f}}<extra></extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        title="Total de muertes por sexo en cada departamento — Colombia 2019",
        xaxis_title="Departamento",
        yaxis_title="Total muertes",
        xaxis_tickangle=-45,
        height=480,
        margin={"t": 60, "b": 140},
        legend_title="Sexo",
    )
    return fig
