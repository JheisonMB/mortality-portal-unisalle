"""Stacked bar: deaths by sex per department."""
import plotly.graph_objects as go

from data.processor import deaths_by_sex_department

_SEX_COLORS = {
    "Masculino": "#654801",
    "Femenino": "#FDBE21",
    "Indeterminado": "#FEE19A",
}

_COLOR_DARK = "#332400"
_FONT = "Poppins, Segoe UI"


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
                hovertemplate=f"<b>{sexo}</b> — %{{x}}<br>%{{y:,.0f}}<extra></extra>",
            )
        )

    fig.update_layout(
        barmode="stack",
        title="MORTALIDAD POR SEXO Y DEPARTAMENTO",
        xaxis_title="DEPARTAMENTO",
        yaxis_title="TOTAL",
        xaxis_tickangle=-45,
        height=480,
        margin={"t": 60, "b": 140, "l": 60, "r": 40},
        title_font={"size": 16, "color": _COLOR_DARK, "family": _FONT, "weight": "bold"},
        title_x=0.05,
        legend_title_text="SEXO",
        xaxis={"showgrid": False, "tickfont": {"size": 10, "family": _FONT}},
        yaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "rgba(51, 36, 0, 0.08)", "tickfont": {"size": 11, "family": _FONT}},
        plot_bgcolor="rgba(255, 255, 255, 0.5)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": _FONT, "color": _COLOR_DARK},
    )
    return fig
