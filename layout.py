"""Dashboard layout — assembles all chart components."""
from dash import dash_table, dcc, html

from components.bar_chart import bar_chart_violent
from components.histogram import histogram_age
from components.line_chart import line_chart
from components.map_chart import map_chart
from components.pie_chart import pie_chart
from components.stacked_bar import stacked_bar_chart
from data.processor import top10_causes

_CARD = {
    "background": "#ffffff",
    "borderRadius": "8px",
    "boxShadow": "0 2px 6px rgba(0,0,0,.12)",
    "padding": "16px",
    "marginBottom": "24px",
}


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
            "backgroundColor": "#1d3557",
            "color": "white",
            "fontWeight": "bold",
            "textAlign": "center",
        },
        style_cell={
            "textAlign": "left",
            "padding": "8px 12px",
            "fontFamily": "sans-serif",
            "fontSize": "13px",
            "whiteSpace": "normal",
            "height": "auto",
        },
        style_data_conditional=[
            {"if": {"row_index": "odd"}, "backgroundColor": "#f1f3f5"}
        ],
        page_action="none",
    )


def build_layout() -> html.Div:
    return html.Div(
        style={"fontFamily": "sans-serif", "backgroundColor": "#f8f9fa", "padding": "24px"},
        children=[
            # Header
            html.Div(
                style={
                    "background": "linear-gradient(135deg, #1d3557 0%, #457b9d 100%)",
                    "color": "white",
                    "padding": "28px 32px",
                    "borderRadius": "10px",
                    "marginBottom": "28px",
                },
                children=[
                    html.H1(
                        "Mortalidad en Colombia — 2019",
                        style={"margin": "0 0 8px 0", "fontSize": "2rem"},
                    ),
                    html.P(
                        "Análisis interactivo de datos de mortalidad no fetal. "
                        "Fuente: DANE — Estadísticas Vitales.",
                        style={"margin": 0, "opacity": "0.85"},
                    ),
                ],
            ),

            # Row 1 — Map (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=map_chart())]),

            # Row 2 — Line chart (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=line_chart())]),

            # Row 3 — Bar (violent cities) | Pie (lowest mortality)
            html.Div(
                style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "24px"},
                children=[
                    html.Div(style=_CARD, children=[dcc.Graph(figure=bar_chart_violent())]),
                    html.Div(style=_CARD, children=[dcc.Graph(figure=pie_chart())]),
                ],
            ),

            # Row 4 — Table (top 10 causes)
            html.Div(
                style={**_CARD, "overflowX": "auto"},
                children=[
                    html.H3(
                        "Top 10 causas de muerte — Colombia 2019",
                        style={"marginTop": 0, "color": "#1d3557"},
                    ),
                    _causes_table(),
                ],
            ),

            # Row 5 — Stacked bar (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=stacked_bar_chart())]),

            # Row 6 — Histogram (full width)
            html.Div(style=_CARD, children=[dcc.Graph(figure=histogram_age())]),

            # Footer
            html.Div(
                style={"textAlign": "center", "color": "#6c757d", "paddingTop": "8px"},
                children=[
                    html.Small("Datos: DANE NoFetal2019 · Desarrollado con Dash & Plotly")
                ],
            ),
        ],
    )
