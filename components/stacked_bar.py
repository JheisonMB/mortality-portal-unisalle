"""Stacked bar: deaths by sex per department."""
import plotly.graph_objects as go

from data.processor import deaths_by_sex_department

_SEX_COLORS = {
    "Masculino": "#654801",
    "Femenino": "#FDBE21",
    "Indeterminado": "#FEE19A",
}

_COLOR_DARK = "#332400"


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
        title="Mortalidad por sexo y departamento",
        xaxis_title="Departamento",
        yaxis_title="Total",
        xaxis_tickangle=-45,
        height=480,
        margin={"t": 60, "b": 140},
        title_font={"size": 18, "color": _COLOR_DARK, "family": "Segoe UI"},
        legend_title="Sexo",
        xaxis={"showgrid": False},
        yaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.05)"},
        plot_bgcolor="rgba(255, 245, 220, 0.3)",
    )
    return fig
