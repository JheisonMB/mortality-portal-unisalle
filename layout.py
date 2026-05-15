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
_COLOR_DARKER = "#1A1200"
_COLOR_MED = "#A27402"
_COLOR_ACCENT = "#DE9F02"
_COLOR_BRIGHT = "#FDBE21"
_COLOR_LIGHT = "#FEECBD"
_COLOR_LIGHTER = "#FEE19A"

_CARD = {
    "background": "#ffffff",
    "borderRadius": "12px",
    "borderLeft": f"5px solid {_COLOR_DARK}",
    "boxShadow": "0 6px 20px rgba(51, 36, 0, 0.12), 4px 8px 16px rgba(51, 36, 0, 0.06)",
    "padding": "28px",
    "marginBottom": "28px",
    "transition": "all 0.3s ease",
}

_FONT_FAMILY = '"Poppins", "Segoe UI", sans-serif'


def _causes_table() -> dash_table.DataTable:
    df = top10_causes()
    return dash_table.DataTable(
        id="causes-table",
        columns=[
            {"name": "CÓDIGO", "id": "COD_MUERTE"},
            {"name": "CAUSA DE MUERTE", "id": "NOMBRE_MUERTE"},
            {"name": "TOTAL", "id": "TOTAL", "type": "numeric",
             "format": {"specifier": ","}},
        ],
        data=df.to_dict("records"),
        style_header={
            "backgroundColor": _COLOR_DARKER,
            "color": "#ffffff",
            "fontWeight": "700",
            "textAlign": "center",
            "fontFamily": _FONT_FAMILY,
            "fontSize": "13px",
            "letterSpacing": "1px",
            "borderBottom": f"3px solid {_COLOR_BRIGHT}",
            "padding": "14px",
            "textTransform": "uppercase",
        },
        style_cell={
            "textAlign": "left",
            "padding": "14px",
            "fontFamily": _FONT_FAMILY,
            "fontSize": "13px",
            "whiteSpace": "normal",
            "height": "auto",
            "color": _COLOR_DARK,
            "borderBottom": "1px solid #f0f0f0",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#fafafa"}
        ],
        page_action="none",
    )


def build_layout() -> html.Div:
    return html.Div(
        style={
            "fontFamily": _FONT_FAMILY,
            "backgroundColor": "#ffffff",
            "padding": "40px 28px",
            "minHeight": "100vh",
        },
        children=[
            # Header
            html.Div(
                style={
                    "background": f"linear-gradient(135deg, {_COLOR_DARKER} 0%, {_COLOR_DARK} 50%, {_COLOR_MED} 100%)",
                    "color": "#ffffff",
                    "padding": "48px 42px",
                    "borderRadius": "16px",
                    "marginBottom": "42px",
                    "boxShadow": "0 12px 36px rgba(51, 36, 0, 0.2), 0 6px 18px rgba(51, 36, 0, 0.12)",
                    "position": "relative",
                    "overflow": "hidden",
                },
                children=[
                    # Línea decorativa sutil
                    html.Div(
                        style={
                            "position": "absolute",
                            "top": 0,
                            "left": 0,
                            "right": 0,
                            "height": "4px",
                            "background": f"linear-gradient(90deg, transparent, {_COLOR_BRIGHT}, transparent)",
                        }
                    ),
                    html.H1(
                        "MORTALIDAD EN COLOMBIA",
                        style={
                            "margin": "0 0 14px 0",
                            "fontSize": "2.6rem",
                            "fontWeight": "700",
                            "letterSpacing": "-0.8px",
                            "textTransform": "uppercase",
                            "position": "relative",
                            "zIndex": 1,
                        },
                    ),
                    html.H2(
                        "Análisis Estadísticas Vitales — 2019",
                        style={
                            "margin": "0 0 12px 0",
                            "fontSize": "0.95rem",
                            "fontWeight": "500",
                            "letterSpacing": "1.2px",
                            "textTransform": "uppercase",
                            "color": _COLOR_BRIGHT,
                            "position": "relative",
                            "zIndex": 1,
                        },
                    ),
                    html.Div(
                        style={
                            "width": "50px",
                            "height": "3px",
                            "background": _COLOR_BRIGHT,
                            "marginBottom": "16px",
                        }
                    ),
                    html.P(
                        "Fuente: DANE — Estadísticas Vitales de Mortalidad No Fetal",
                        style={
                            "margin": 0,
                            "opacity": "0.9",
                            "fontSize": "13px",
                            "fontWeight": "300",
                            "position": "relative",
                            "zIndex": 1,
                        },
                    ),
                ],
            ),

            # Row 1 — Map (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=map_chart())]),

            # Row 2 — Line chart (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=line_chart())]),

            # Row 3 — Bar (violent cities) | Pie (lowest mortality)
            html.Div(
                style={
                    "display": "grid",
                    "gridTemplateColumns": "1fr 1fr",
                    "gap": "28px",
                    "marginBottom": "28px",
                },
                children=[
                    html.Div(style=_CARD, children=[dcc.Graph(figure=bar_chart_violent())]),
                    html.Div(style=_CARD, children=[dcc.Graph(figure=pie_chart())]),
                ],
            ),

            # Row 4 — Table (top 10 causes)
            html.Div(
                style={**_CARD, "paddingTop": "0"},
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "alignItems": "center",
                            "gap": "16px",
                            "marginBottom": "24px",
                        },
                        children=[
                            html.Div(
                                style={
                                    "width": "4px",
                                    "height": "28px",
                                    "background": _COLOR_BRIGHT,
                                }
                            ),
                            html.H3(
                                "PRINCIPALES CAUSAS DE MUERTE",
                                style={
                                    "margin": 0,
                                    "color": _COLOR_DARK,
                                    "fontSize": "1.1rem",
                                    "fontWeight": "700",
                                    "letterSpacing": "0.5px",
                                    "textTransform": "uppercase",
                                },
                            ),
                        ],
                    ),
                    _causes_table(),
                ],
            ),

            # Row 5 — Stacked bar (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=stacked_bar_chart())]),

            # Row 6 — Histogram (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=histogram_age())]),
        ],
    )
