"""Dashboard layout — assembles all chart components."""
from dash import dash_table, dcc, html

from components.bar_chart import bar_chart_violent
from components.histogram import histogram_age
from components.line_chart import line_chart
from components.map_chart import map_chart
from components.pie_chart import pie_chart
from components.stacked_bar import stacked_bar_chart
from data.processor import top10_causes

# Ocre palette
_COLOR_DARK = "#332400"
_COLOR_DARKER = "#654801"
_COLOR_MED = "#A27402"
_COLOR_ACCENT = "#DE9F02"
_COLOR_BRIGHT = "#FDBE21"
_COLOR_LIGHT = "#FEECBD"
_COLOR_LIGHTER = "#FEE19A"
_COLOR_BG = "#FFF5DC"

_CARD = {
    "background": _COLOR_LIGHT,
    "borderRadius": "12px",
    "boxShadow": "0 4px 12px rgba(51, 36, 0, 0.1)",
    "padding": "24px",
    "marginBottom": "24px",
    "border": f"1px solid {_COLOR_LIGHTER}",
}

_FONT_FAMILY = '"Segoe UI", "Trebuchet MS", sans-serif'


def _causes_table() -> dash_table.DataTable:
    df = top10_causes()
    return dash_table.DataTable(
        id="causes-table",
        columns=[
            {"name": "Código", "id": "COD_MUERTE"},
            {"name": "Causa de muerte", "id": "NOMBRE_MUERTE"},
            {"name": "Total casos", "id": "TOTAL", "type": "numeric",
             "format": {"specifier": ","}},
        ],
        data=df.to_dict("records"),
        style_header={
            "backgroundColor": _COLOR_DARKER,
            "color": "#ffffff",
            "fontWeight": "600",
            "textAlign": "center",
            "fontFamily": _FONT_FAMILY,
            "fontSize": "14px",
            "borderBottom": f"2px solid {_COLOR_ACCENT}",
            "padding": "12px",
        },
        style_cell={
            "textAlign": "left",
            "padding": "12px",
            "fontFamily": _FONT_FAMILY,
            "fontSize": "13px",
            "whiteSpace": "normal",
            "height": "auto",
            "color": _COLOR_DARK,
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": _COLOR_LIGHTER}
        ],
        page_action="none",
    )


def build_layout() -> html.Div:
    return html.Div(
        style={
            "fontFamily": _FONT_FAMILY,
            "backgroundColor": _COLOR_BG,
            "padding": "32px 24px",
            "minHeight": "100vh",
        },
        children=[
            # Header
            html.Div(
                style={
                    "background": f"linear-gradient(135deg, {_COLOR_DARK} 0%, {_COLOR_DARKER} 100%)",
                    "color": "#ffffff",
                    "padding": "40px 36px",
                    "borderRadius": "16px",
                    "marginBottom": "36px",
                    "boxShadow": "0 8px 24px rgba(51, 36, 0, 0.15)",
                },
                children=[
                    html.H1(
                        "Mortalidad en Colombia",
                        style={
                            "margin": "0 0 12px 0",
                            "fontSize": "2.4rem",
                            "fontWeight": "700",
                            "letterSpacing": "-0.5px",
                        },
                    ),
                    html.H2(
                        "Análisis de Estadísticas Vitales — 2019",
                        style={
                            "margin": "0 0 8px 0",
                            "fontSize": "1rem",
                            "fontWeight": "300",
                            "color": _COLOR_BG,
                        },
                    ),
                    html.P(
                        "Fuente: DANE — Estadísticas Vitales de Mortalidad No Fetal",
                        style={
                            "margin": 0,
                            "opacity": "0.85",
                            "fontSize": "13px",
                        },
                    ),
                ],
            ),

            # Row 1 — Map (full width)
            html.Div(
                style=_CARD,
                children=[dcc.Graph(figure=map_chart())],
            ),

            # Row 2 — Line chart (full width)
            html.Div(
                style=_CARD,
                children=[dcc.Graph(figure=line_chart())],
            ),

            # Row 3 — Bar (violent cities) | Pie (lowest mortality)
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "24px",
                    "marginBottom": "24px",
                },
                children=[
                    html.Div(style=_CARD, children=[dcc.Graph(figure=bar_chart_violent())]),
                    html.Div(style=_CARD, children=[dcc.Graph(figure=pie_chart())]),
                ],
            ),

            # Row 4 — Table (top 10 causes)
            html.Div(
                style=_CARD,
                children=[
                    html.H3(
                        "Principales causas de muerte",
                        style={
                            "marginTop": 0,
                            "color": _COLOR_DARK,
                            "fontSize": "1.2rem",
                            "fontWeight": "600",
                            "borderBottom": f"3px solid {_COLOR_BRIGHT}",
                            "paddingBottom": "12px",
                        },
                    ),
                    _causes_table(),
                ],
            ),

            # Row 5 — Stacked bar (full width)
            html.Div(
                style=_CARD,
                children=[dcc.Graph(figure=stacked_bar_chart())],
            ),

            # Row 6 — Histogram (full width)
            html.Div(
                style=_CARD,
                children=[dcc.Graph(figure=histogram_age())],
            ),
        ],
    )
