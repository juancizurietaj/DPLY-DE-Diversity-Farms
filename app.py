import pandas as pd

from helpers import *

# App constructor
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server

# Contents
## Insects
i_methods_a = html.Div([html.Div(html.Label("¿De dónde provienen estos datos?", className="labels-white"),
                                 className="heading-container"),
                        insects_methods,
                        html.Div(html.Img(src="assets/Base.png", height=400), style={"text-align": "center",
                                                                                     "margin-bottom": "8rem"})])

i_methods_b = html.Div([html.Br(),
                        html.Label("Colectamos en campo, identificamos en laboratorio", className="labels-white",
                                   style={"margin-top": "8rem"}),
                        insects_methods_2,
                        html.P(total_insects, className="indicator-white"),
                        html.P("Total de insectos analizados", className="p-texts-white",
                               style={"margin-top": "0",
                                      "padding": "0 calc(2rem + 1vw) calc(2rem + 1vw) calc(2rem + 1vw)"}),
                        html.Br(style={"margin-bottom": "8rem"})
                        ], className="sky-background")

i_main = html.Div([html.Br(),
                   html.Label("¿Qué tipo de insectos encontramos?", className="labels-white",
                              style={"margin-top": "8rem"}),
                   insects_methods_4,
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Div(
                       [
                           html.Div(
                               [dbc.Button(id="all-sectors", children="Ver todos", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="santa-rosa", children="Santa Rosa", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="el-carmen", children="El Carmen", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="occidente", children="Occidente", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="aguacatal", children="Aguacatal", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                ], className="buttons-map-column"),
                           html.Div(html.Img(id="map-buttons", width="90%", height="90%",
                                             className="map-image"),
                                    style={"width": "50%", "text-align": "center", "align-self": "center"}),
                           html.Div(
                               [dbc.Button(id="media-luna", children="Media Luna", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="camote", children="Camote", outline=True, color="info", n_clicks=0,
                                           className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="cascajo", children="Cascajo", outline=True, color="info", n_clicks=0,
                                           className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="bellavista", children="Bellavista", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="guayabillos", children="Guayabillos", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-right": "2rem"}),
                                ], className="buttons-map-column")
                       ], className="buttons-map-container"
                   ),
                   html.Div(dcc.Store(id="i-buttons-prev-sel")),
                   html.Br(),
                   html.Br(),
                   html.Div(id="i-main-chart-title", style={"text-align": "center"}),
                   html.Div([dbc.Checklist(id="show-species",
                                           options=[{"label": "Ver por nombres científicos", "value": False}],
                                           value=False,
                                           switch=True)],
                            style={"display": "flex", "justify-content": "center", "font-size": "3rem",
                                   "padding": "2rem"}),
                   html.Br(),
                   html.Div(id="i-main-chart", style={"margin-bottom": "8rem"}),
                   ])

i_endemic_tab_contents = html.Div([create_meter_layout_origin(data[data["Origen"] == "Endémico"], "Especie",
                                                              "Numero de individuos", "ENDEMICOS", color_success,
                                                              "success", def_endemic)])
i_native_tab_contents = html.Div([create_meter_layout_origin(data[data["Origen"] == "Nativo"], "Especie",
                                                             "Numero de individuos", "NATIVOS", color_warning,
                                                             "warning", def_native)])
i_introduced_tab_contents = html.Div([create_meter_layout_origin(data[data["Origen"] == "Introducido"], "Especie",
                                                                 "Numero de individuos", "INTRODUCIDOS", color_danger,
                                                                 "danger", def_introduced)])
i_unknown_tab_contents = html.Div([create_meter_layout_origin(data[data["Origen"] == "Desconocido"], "Especie",
                                                              "Numero de individuos", "ORIGEN DESCONOCIDO",
                                                              color_secondary, "secondary", def_unknown)])

i_origin = html.Div([html.Br(),
                     html.Label("¿Cuál es el origen de estos insectos?", className="labels-white",
                                style={"margin-top": "8rem"}),
                     html.Div(html.P("Número de individuos según origen:", className="p-texts-white")),
                     html.Div([
                         html.Div([html.P("1340", className="pie-values",
                                          style={"color": color_success, "font-size": "3rem"}),
                                   html.P("Endémicos", className="pie-values-sm", style={"color": color_success}),
                                   html.P("(8.11%)", className="pie-values", style={"color": color_success}),
                                   ],
                                  className="pie-values-col"),
                         html.Div([html.P("865", className="pie-values",
                                          style={"color": color_warning, "font-size": "3rem"}),
                                   html.P("Nativos", className="pie-values-sm", style={"color": color_warning}),
                                   html.P("(5.23%)", className="pie-values", style={"color": color_warning}),
                                   ],
                                  className="pie-values-col"),
                         html.Div([html.P("6774", className="pie-values",
                                          style={"color": color_danger, "font-size": "3rem"}),
                                   html.P("Introducidos", className="pie-values-sm", style={"color": color_danger}),
                                   html.P("(41.00%)", className="pie-values", style={"color": color_danger}),
                                   ],
                                  className="pie-values-col"),
                         html.Div([html.P("7554", className="pie-values",
                                          style={"color": color_secondary, "font-size": "3rem"}),
                                   html.P("Desconocido", className="pie-values-sm", style={"color": color_secondary}),
                                   html.P("(45.70%)", className="pie-values", style={"color": color_secondary})],
                                  className="pie-values-col")
                     ], className="pie-values-row"),
                     html.Br(),
                     html.P("Seleccione los botones debajo para ver los insectos más comunes según su origen:",
                            className="p-texts-white"),
                     html.Br(),
                     dbc.Tabs([
                         tab_creator("END", i_endemic_tab_contents, color_success),
                         tab_creator("NAT", i_native_tab_contents, color_warning),
                         tab_creator("INT", i_introduced_tab_contents, color_danger),
                         tab_creator("DES", i_unknown_tab_contents, color_secondary)
                     ]),
                     ], className="gray-container", style={"margin-bottom": "8rem"})

i_importance = importance_insectos(data_importance)

## Plants
p_methods_a = html.Div([html.Div(html.Label("¿De dónde provienen estos datos?", className="labels-white"),
                                 className="heading-container"),
                        plants_methods,
                        html.Div(html.Img(src="assets/Base.png", height=400), style={"text-align": "center"})],
                       style={"background-color": "#2c3948"})

p_methods_b = html.Div([html.Br(),
                        html.Label("Colectamos en campo, identificamos en laboratorio", className="labels-white",
                                   style={"margin-top": "8rem"}),
                        plants_methods_2,
                        html.P(total_plants, className="indicator-white"),
                        html.P("Total de plantas analizadas", className="p-texts-white",
                               style={"margin-top": "0",
                                      "padding": "0 calc(2rem + 1vw) calc(2rem + 1vw) calc(2rem + 1vw)"}),
                        html.Br(style={"margin-bottom": "8rem"})
                        ], style={"background-color": "#3c5c81"})

p_main = html.Div([html.Br(),
                   html.Label("¿Qué tipo de plantas encontramos?", className="labels-white",
                              style={"margin-top": "8rem"}),
                   insects_methods_4,
                   html.Br(),
                   html.Br(),
                   html.Br(),
                   html.Div(
                       [
                           html.Div(
                               [dbc.Button(id="p-all-sectors", children="Ver todos", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="p-santa-rosa", children="Santa Rosa", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="p-el-carmen", children="El Carmen", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="p-occidente", children="Occidente", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                dbc.Button(id="p-aguacatal", children="Aguacatal", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-left": "2rem"}),
                                ], className="buttons-map-column"),
                           html.Div(html.Img(id="p-map-buttons", width="90%", height="90%",
                                             className="map-image"),
                                    style={"width": "50%", "text-align": "center", "align-self": "center"}),
                           html.Div(
                               [dbc.Button(id="p-media-luna", children="Media Luna", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="p-camote", children="Camote", outline=True, color="info", n_clicks=0,
                                           className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="p-cascajo", children="Cascajo", outline=True, color="info", n_clicks=0,
                                           className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="p-bellavista", children="Bellavista", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-right": "2rem"}),
                                dbc.Button(id="p-guayabillos", children="Guayabillos", outline=True, color="info",
                                           n_clicks=0, className="btn-map", style={"margin-right": "2rem"}),
                                ], className="buttons-map-column")
                       ], className="buttons-map-container"
                   ),
                   html.Div(dcc.Store(id="p-buttons-prev-sel")),
                   html.Br(),
                   html.Br(),
                   html.Div(id="p-main-chart-title", style={"text-align": "center"}),
                   html.Div([dbc.Checklist(id="p-show-species",
                                           options=[{"label": "Ver ejemplos por nombres científicos", "value": False}],
                                           value=False,
                                           switch=True)],
                            style={"display": "flex", "justify-content": "center", "font-size": "2.25rem",
                                   "padding": "2rem"}),
                   html.Br(),
                   html.Div(id="p-main-chart", style={"margin-bottom": "8rem"}),
                   ], style={"background-color": "#2c3948"})

# plants_contents = [p_methods_section, p_origin, p_diversity, p_diversity_per_sector]

footer_buttons = html.Div(
    [dbc.Button("INSECTOS", size="lg", outline=True, color="success", id="i-btn", n_clicks=1,
                style={"width": "50%", "height": "calc(8rem + 1vw)", "font-size": "5rem"}),
     dbc.Button("PLANTAS", size="lg", outline=True, color="success", id="p-btn", n_clicks=0,
                style={"width": "50%", "height": "calc(8rem + 1vw)", "font-size": "5rem"})],
    className="footer-buttons")

# App layout
app.layout = html.Div(
    [
        header,
        html.Div(id="i-contents", children=[i_methods_a,
                                            i_methods_b,
                                            i_main,
                                            i_origin,
                                            i_importance]),
        html.Div(id="p-contents", children=[p_methods_a,
                                            p_methods_b,
                                            p_main], style={"background-color": "#2c482c"}),
        footer,
        footer_buttons
    ]
)


# Main section callback
@app.callback(
    Output("i-main-chart-title", "children"),
    Output("i-main-chart", "children"),
    Output("all-sectors", "n_clicks"),
    Output("santa-rosa", "n_clicks"),
    Output("el-carmen", "n_clicks"),
    Output("occidente", "n_clicks"),
    Output("aguacatal", "n_clicks"),
    Output("media-luna", "n_clicks"),
    Output("camote", "n_clicks"),
    Output("cascajo", "n_clicks"),
    Output("bellavista", "n_clicks"),
    Output("guayabillos", "n_clicks"),
    Output("i-buttons-prev-sel", "data"),
    Output("map-buttons", "src"),
    Input("show-species", "value"),
    Input("all-sectors", "n_clicks"),
    Input("santa-rosa", "n_clicks"),
    Input("el-carmen", "n_clicks"),
    Input("occidente", "n_clicks"),
    Input("aguacatal", "n_clicks"),
    Input("media-luna", "n_clicks"),
    Input("camote", "n_clicks"),
    Input("cascajo", "n_clicks"),
    Input("bellavista", "n_clicks"),
    Input("guayabillos", "n_clicks"),
    Input("i-buttons-prev-sel", "data"),
    # prevent_initial_call = True
)
def update_layout(show_species, i_all_sectors, i_santa_rosa, i_el_carmen, i_occidente, i_aguacatal, i_media_luna,
                  i_camote, i_cascajo, i_bellavista, i_guayabillos, sector_to_filter):
    x = pd.DataFrame({"value": [i_all_sectors, i_santa_rosa, i_el_carmen, i_occidente, i_aguacatal, i_media_luna,
                                i_camote, i_cascajo, i_bellavista, i_guayabillos],
                      "label": ["all", "Santa Rosa", "El Carmen", "Occidente", "Aguacatal", "Media Luna", "Camote",
                                "Cascajo", "Bellavista", "Guayabillos"]})

    # print(x)
    # print("input:")
    # print(sector_to_filter)

    if sector_to_filter is None:
        sector_to_filter = "all"
    else:
        sector_to_filter = sector_to_filter
    # print("logic None:")
    # print(sector_to_filter)

    prev_sector_to_filter = sector_to_filter

    if x['value'].sum() == 0:
        sector_to_filter = prev_sector_to_filter
    else:
        sector_to_filter = x["label"][x['value'].idxmax()]
    # print("logic max == prev:")
    # print(sector_to_filter)

    if sector_to_filter == "all":
        df = data
    else:
        df = data[data["Sector"] == sector_to_filter]

    # Grouping data
    if not show_species:
        label_column = "Nombre comun"
        df_grouped = df.groupby(["Nombre comun", "Sector"])["Numero de individuos"].sum().reset_index()
    else:
        label_column = "Especie"
        df_grouped = df.groupby(["Especie", "Sector"])["Numero de individuos"].sum().reset_index()

    # Title definition

    if len(df_grouped["Sector"].unique()) > 1:
        title = "todos los sectores"
    else:
        title = df_grouped["Sector"].unique()

    i_main_chart_title = html.Label("Resultados para " + title, className="labels-white", style={"font-size": "4rem"})

    i_main_chart = create_meter_layout(df_grouped, label_column, "Numero de individuos")

    i_all_sectors = 0
    i_santa_rosa = 0
    i_el_carmen = 0
    i_occidente = 0
    i_aguacatal = 0
    i_media_luna = 0
    i_camote = 0
    i_cascajo = 0
    i_bellavista = 0
    i_guayabillos = 0

    # Define map image:
    map_image = ""

    if sector_to_filter == "all":
        map_image = "assets/map_all.png"
    elif sector_to_filter == "Aguacatal":
        map_image = "assets/map_aguacatal.png"
    elif sector_to_filter == "Bellavista":
        map_image = "assets/map_bellavista.png"
    elif sector_to_filter == "Cascajo":
        map_image = "assets/map_cascajo.png"
    elif sector_to_filter == "Camote":
        map_image = "assets/map_camote.png"
    elif sector_to_filter == "El Carmen":
        map_image = "assets/map_el_carmen.png"
    elif sector_to_filter == "Guayabillos":
        map_image = "assets/map_guayabillos.png"
    elif sector_to_filter == "Media Luna":
        map_image = "assets/map_media_luna.png"
    elif sector_to_filter == "Occidente":
        map_image = "assets/map_occidente.png"
    elif sector_to_filter == "Santa Rosa":
        map_image = "assets/map_santa_rosa.png"

    # print("output: " + sector_to_filter)

    return i_main_chart_title, i_main_chart, i_all_sectors, i_santa_rosa, i_el_carmen, i_occidente, i_aguacatal, \
           i_media_luna, i_camote, i_cascajo, i_bellavista, i_guayabillos, sector_to_filter, map_image


@app.callback(
    Output("p-main-chart-title", "children"),
    Output("p-main-chart", "children"),
    Output("p-all-sectors", "n_clicks"),
    Output("p-santa-rosa", "n_clicks"),
    Output("p-el-carmen", "n_clicks"),
    Output("p-occidente", "n_clicks"),
    Output("p-aguacatal", "n_clicks"),
    Output("p-media-luna", "n_clicks"),
    Output("p-camote", "n_clicks"),
    Output("p-cascajo", "n_clicks"),
    Output("p-bellavista", "n_clicks"),
    Output("p-guayabillos", "n_clicks"),
    Output("p-buttons-prev-sel", "data"),
    Output("p-map-buttons", "src"),
    Input("p-show-species", "value"),
    Input("p-all-sectors", "n_clicks"),
    Input("p-santa-rosa", "n_clicks"),
    Input("p-el-carmen", "n_clicks"),
    Input("p-occidente", "n_clicks"),
    Input("p-aguacatal", "n_clicks"),
    Input("p-media-luna", "n_clicks"),
    Input("p-camote", "n_clicks"),
    Input("p-cascajo", "n_clicks"),
    Input("p-bellavista", "n_clicks"),
    Input("p-guayabillos", "n_clicks"),
    Input("p-buttons-prev-sel", "data"),
    # prevent_initial_call = True
)
def update_layout(show_species, p_all_sectors, p_santa_rosa, p_el_carmen, p_occidente, p_aguacatal, p_media_luna,
                  p_camote, p_cascajo, p_bellavista, p_guayabillos, sector_to_filter):
    x = pd.DataFrame({"value": [p_all_sectors, p_santa_rosa, p_el_carmen, p_occidente, p_aguacatal, p_media_luna,
                                p_camote, p_cascajo, p_bellavista, p_guayabillos],
                      "label": ["all", "Santa Rosa", "El Carmen", "Occidente", "Aguacatal", "Media Luna", "Camote",
                                "Cascajo", "Bellavista", "Guayabillos"]})

    if sector_to_filter is None:
        sector_to_filter = "all"
    else:
        sector_to_filter = sector_to_filter

    prev_sector_to_filter = sector_to_filter

    if x['value'].sum() == 0:
        sector_to_filter = prev_sector_to_filter
    else:
        sector_to_filter = x["label"][x['value'].idxmax()]

    if sector_to_filter == "all":
        df = data_p
    else:
        df = data_p[data_p["Sector"] == sector_to_filter]

    # Grouping data
    if not show_species:
        label_column = "Nombre comun"
        df_grouped = df.groupby(["Familia", label_column, "Sector"])["Numero de individuos"].sum().reset_index()
    else:
        label_column = "Especie"
        df_grouped = df.groupby(["Familia", label_column, "Sector"])["Numero de individuos"].sum().reset_index()

    # Title definition

    if len(df_grouped["Sector"].unique()) > 1:
        title = "todos los sectores"
    else:
        title = df_grouped["Sector"].unique()

    p_main_chart_title = html.Label("Resultados para " + title, className="labels-white", style={"font-size": "4rem"})

    # p_main_chart = create_meter_layout(df_grouped, label_column, "Numero de individuos")

    p_main_chart = create_plants_meter_layout(df_grouped, "Familia", "Numero de individuos", label_column)

    p_all_sectors = 0
    p_santa_rosa = 0
    p_el_carmen = 0
    p_occidente = 0
    p_aguacatal = 0
    p_media_luna = 0
    p_camote = 0
    p_cascajo = 0
    p_bellavista = 0
    p_guayabillos = 0

    # Define map image:
    map_image = ""

    if sector_to_filter == "all":
        map_image = "assets/map_all.png"
    elif sector_to_filter == "Aguacatal":
        map_image = "assets/map_aguacatal.png"
    elif sector_to_filter == "Bellavista":
        map_image = "assets/map_bellavista.png"
    elif sector_to_filter == "Cascajo":
        map_image = "assets/map_cascajo.png"
    elif sector_to_filter == "Camote":
        map_image = "assets/map_camote.png"
    elif sector_to_filter == "El Carmen":
        map_image = "assets/map_el_carmen.png"
    elif sector_to_filter == "Guayabillos":
        map_image = "assets/map_guayabillos.png"
    elif sector_to_filter == "Media Luna":
        map_image = "assets/map_media_luna.png"
    elif sector_to_filter == "Occidente":
        map_image = "assets/map_occidente.png"
    elif sector_to_filter == "Santa Rosa":
        map_image = "assets/map_santa_rosa.png"

    return p_main_chart_title, p_main_chart, p_all_sectors, p_santa_rosa, p_el_carmen, p_occidente, p_aguacatal, \
           p_media_luna, p_camote, p_cascajo, p_bellavista, p_guayabillos, sector_to_filter, map_image


@app.callback(
    Output("i-contents", "style"),
    Output("p-contents", "style"),
    Output("i-btn", "n_clicks"),
    Output("p-btn", "n_clicks"),
    Input("i-btn", "n_clicks"),
    Input("p-btn", "n_clicks"),
)
def update_main_layout(i_btn, p_btn):
    i_style = {}
    p_style = {}

    if p_btn > 0:
        i_style = {"display": "None"}
        p_btn = 0

    elif i_btn > 0:
        p_style = {"display": "None"}
        i_btn = 0

    return i_style, p_style, i_btn, p_btn


if __name__ == '__main__':
    app.run_server(debug=True)
