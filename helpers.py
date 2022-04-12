import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, State, html, dash_table
import numpy as np

# Data load
data = pd.read_csv(r"assets/data_insectos_simp.csv")
data_p = pd.read_csv(r"assets/data_plantas_simp.csv")
data_importance = pd.read_csv(r"assets/importance_insects.csv")

## Main chart
total_insects = 16533
total_plants = 4584

# Colors
color_success = "#62c462"
color_info = "#5bc0de"
color_primary = "#2c3e50"
color_secondary = "#7a8288"
color_warning = "#f89406"
color_danger = "#ee5f5b"

# Header
header = html.Div(
    [
        html.Img(src=r"./assets/fcd_white.png",
                 width="550px",
                 style={'display': 'inline-block', "padding": "10px"}),
        html.H2("Diversidad de insectos y plantas en fincas con Acuerdos de Conservación en Santa Cruz",
                style={"color": "white", "font-size": "5rem"})
    ], className="header-container"
)

# Footer
footer = html.Div(
    [
        html.Img(src="assets/fcd_logo.png",
                 width="550px",
                 style={"padding": "0px 15px", "display": "inline-block", "margin-top": "0px"}),
        html.P("©Fundación Charles Darwin", className="footer-fcd"),
        html.P("Creado por el Departamento de Tecnologías, Información, Investigación y Desarrollo (TIID)",
               className="footer-fcd")
    ], className="footer-container"
)


# Helper functions
def tab_creator(label_name, content, font_color):
    tab = dbc.Tab(content, label=label_name,
                  tab_style={"text-align": "center", "width": "25%"},
                  active_label_style={'color': '#fff', 'fontWeight': 'bold', "height": "100%"},
                  label_style={"color": font_color, "fontSize": "calc(2.75rem + 1vw)"})
    return tab


def origin_tab_contents(category, text, df, color, color_heading):
    df_a = df[df["Origen"].isin([category])]
    df_a = df_a[df_a["Especie"] != "Indeterminado"]
    df_a = pd.DataFrame(df_a.groupby(["Especie", "Nombre comun"])["Numero de individuos"].sum()).sort_values(
        "Numero de individuos", ascending=False)
    df_a.reset_index(inplace=True)
    df_b = df_a[0:5]

    max_value = max(df_b["Numero de individuos"])
    min_value = min(df_b["Numero de individuos"])

    labels = []
    values = []

    for i in range(len(df_b.index)):
        labels.append(df_b["Especie"][i])
        values.append(df_b["Numero de individuos"][i])

    scoring_layout = []

    for i in range(len(labels)):
        scoring_layout.append(
            html.Div([html.Div(html.P(labels[i]), style={"text-align": "right", "padding": "0px 5px", "width": "50%"}),
                      create_meter(values[i], color, "#fff", "60%", "colored")], className="meter-container"))

    layout = html.Div([
        html.Div(html.Label(category.upper() + "S", className="labels-white"),
                 style={"background-color": color_heading}),
        html.Div(text, className="p-text"),
        html.Div(scoring_layout)
    ])

    return layout


def create_meter_layout_origin(df, label_column, value_column, title, color_heading, color_bars, text):
    df = df.groupby([label_column])[value_column].sum().reset_index()
    df = df.sort_values(by=value_column, ascending=False).reset_index()

    labels = df[label_column][0:5]
    values = df[value_column][0:5]

    percentages = np.round(values / sum(df["Numero de individuos"]) * 100, 2)

    children = []
    for i in range(len(labels)):
        children.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(labels[i], className="meter-labels")
                                ], style={"display": "flex", "justify-content": "flex-start", "align-items": "center",
                                          "width": "50%"}
                            ),
                            html.Div(
                                [
                                    html.P(str(values[i]) + " individuos ", className="meter-values",
                                           style={"color": color_heading}),
                                    html.P(" | " + str(percentages[i]) + "% ", className="percentages")
                                ], style={"display": "flex", "justify-content": "flex-end", "align-items": "center",
                                          "width": "50%"}
                            )
                        ], style={"display": "flex", "justify-content": "space-between"}
                    ),
                    html.Div(
                        html.Div(create_meter(percentages[i], color_bars, "#43484e", "100%", "colored"),
                                 className="meter-container")
                    )
                ], style={"padding": "0rem 5rem"}
            )
        )

    layout = html.Div([
        html.Div(html.Label(title, className="labels-white"),
                 style={"background-color": color_heading}),
        html.Div(text, className="p-text"),
        html.Div(children, style={"margin-bottom": "8rem"})
    ])

    return layout


def create_meter_layout(df, label_column, value_column):
    df = df.groupby([label_column])[value_column].sum().reset_index()
    df = df.sort_values(by=value_column, ascending=False).reset_index()

    labels = df[label_column][0:5]
    values = df[value_column][0:5]

    percentages = np.round(values / sum(df["Numero de individuos"]) * 100, 2)

    children = []
    for i in range(len(labels)):
        children.append(
            html.Div(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.P(labels[i], className="meter-labels")
                                    ], style={"display": "flex", "justify-content": "flex-start",
                                              "align-items": "center",
                                              "width": "50%"}
                                ),
                                html.Div(
                                    [
                                        html.P(str(values[i]) + " individuos ", className="meter-values",
                                               style={"color": color_info}),
                                        html.P(" | " + str(percentages[i]) + "% ", className="percentages")
                                    ], style={"display": "flex", "justify-content": "flex-end",
                                              "align-items": "center",
                                              "width": "50%"}
                                )
                            ], style={"display": "flex", "justify-content": "space-between"}
                        ),
                        html.Div(
                            html.Div(create_meter(percentages[i], "info", "#43484e", "100%", "colored"),
                                     className="meter-container")
                        )
                    ], style={"padding": "0rem 4rem", "align-self": "center"}
                )
            )
        )

    layout = html.Div(children)

    return layout


def create_plants_meter_layout(df, label_column, value_column, examples_column):
    ex_df = df.groupby([label_column, examples_column])[value_column].sum().reset_index()
    ex_df = ex_df.dropna(subset=[examples_column])

    df = df.groupby([label_column])[value_column].sum().reset_index()
    df = df.sort_values(by=value_column, ascending=False).reset_index()

    labels = df[label_column][0:5]
    values = df[value_column][0:5]
    # TODO: Show the top 3 examples instead of first 3 examples:
    examples_0 = data_p[data_p[label_column] == labels[0]][examples_column].dropna().unique()[0:3]
    examples_1 = data_p[data_p[label_column] == labels[1]][examples_column].dropna().unique()[0:3]
    examples_2 = data_p[data_p[label_column] == labels[2]][examples_column].dropna().unique()[0:3]
    examples_3 = data_p[data_p[label_column] == labels[3]][examples_column].dropna().unique()[0:3]
    examples_4 = data_p[data_p[label_column] == labels[4]][examples_column].dropna().unique()[0:3]

    examples_array = [examples_0, examples_1, examples_2, examples_3, examples_4]

    # print(labels)
    # print(examples_0)

    percentages = np.round(values / sum(df["Numero de individuos"]) * 100, 2)

    children = []
    for i in range(len(labels)):
        children.append(
            html.Div(
                [
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.P(labels[i], className="meter-labels")
                                ], style={"display": "flex", "justify-content": "flex-start", "align-items": "center",
                                          "width": "50%"}
                            ),
                            html.Div(
                                [
                                    html.P(str(values[i]) + " individuos ", className="meter-values",
                                           style={"color": color_info}),
                                    html.P(" | " + str(percentages[i]) + "% ", className="percentages")
                                ], style={"display": "flex", "justify-content": "flex-end", "align-items": "center",
                                          "width": "50%"}
                            )
                        ], style={"display": "flex", "justify-content": "space-between"}
                    ),
                    html.Div([
                        html.P("Ej: " + ", ".join(map(str, examples_array[i])), className="meter-labels",
                               style={"font-size": "1.25rem"})],
                        style={"display": "flex", "flex-direction": "row"}),
                    html.Div(
                        [html.Div(create_meter(percentages[i], "info", "#43484e", "100%", "colored"),
                                  className="meter-container"),
                         html.Br(),
                         html.Br(), ]
                    )
                ], style={"padding": "0rem 5rem"}
            )
        )

    layout = html.Div(children)

    return layout


def create_meter(value, color, background_color, width, mode):
    # Compensating visually small values
    if value < 1:
        value = 1
    else:
        value = value

    if mode == "one-color":
        meter = html.Meter(
            min=0,
            max=100,
            value=str(value),
            style={"width": "100%", "height": "3rem", "background-color": background_color}
        )
    elif mode == "colored":
        meter = dbc.Progress(
            label="",
            value=value,
            max=100,
            min=0,
            color=color,
            style={"height": "3rem", "width": width, "border-radius": "2rem", "background-color": background_color})

    return meter


def create_dropdown_buttons(label):
    dropdown = html.Div(
        [
            dbc.DropdownMenu(
                [
                    dbc.DropdownMenuItem("Todos", id="i-all-sectors", n_clicks=1),
                    dbc.DropdownMenuItem("Aguacatal", id="i-aguacatal", n_clicks=0),
                    dbc.DropdownMenuItem("Bellavista", id="i-bellavista", n_clicks=0),
                    dbc.DropdownMenuItem("Camote", id="i-camote", n_clicks=0),
                    dbc.DropdownMenuItem("Cascajo", id="i-cascajo", n_clicks=0),
                    dbc.DropdownMenuItem("El Carmen", id="i-el-carmen", n_clicks=0),
                    dbc.DropdownMenuItem("Guayabillos", id="i-guayabillos", n_clicks=0),
                    dbc.DropdownMenuItem("Media Luna", id="i-media-luna", n_clicks=0),
                    dbc.DropdownMenuItem("Occidente", id="i-occidente", n_clicks=0),
                    dbc.DropdownMenuItem("Santa Rosa", id="i-santa-rosa", n_clicks=0),
                ],
                label=label,
            )
        ]
    )

    return dropdown


def buttons_array(btn_clicks, btn_values):
    selections = btn_values
    for i in range(len(btn_clicks)):
        if btn_clicks[i] > 0:
            selections = []
            selections.append(btn_values[i])
            btn_clicks[i] = 0
    return btn_clicks, selections


def importance_insectos(df):
    intro = html.Div([html.Label("Insectos de importancia agrícola", className="labels-white"),
                      html.P("Debajo mostramos insectos de importancia agrícola que se pueden encontrar "
                             "en las fincas de Santa Cruz", className="-texts-white")])

    styles_two_column_lab = {"margin-right": "1rem", "padding": "0", "font-weight": "bold", "width": "50%", "text-align": "right"}
    styles_two_column_val = {"padding": "0", "width": "50%", "text-align": "left"}
    children = []

    for i in range(len(df.index)):

        if df["Origen"][i] == "Endémico":
            back_color = color_success
        elif df["Origen"][i] == "Nativo":
            back_color = color_warning
        elif df["Origen"][i] == "Introducido":
            back_color = color_danger
        elif df["Origen"][i] == "Desconocido":
            back_color = color_secondary

        children.append(
            html.Div(
                [
                    html.Label(df["Nombre comun"][i], className="labels-white"),
                    html.P(df["Especie"][i], className="p-texts-white", style={"padding": "0", "font-style": "italic"}),
                    html.Br(),
                    html.P(df["Descripcion"][i], className="p-texts-white"),
                    html.Br(),
                    html.Div(html.Img(src=df["Ubicacion imagen"][i], width=600), style={"text-align": "center"}),
                    html.P("Créditos fotográficos: " + df["Creditos fotograficos"][i], className="p-texts-small",
                           style={"text-align": "center", "font-size": "1.75rem"}),
                    # Two columns
                    html.Div([
                        html.P("Origen:", className="p-texts-white",
                               style=styles_two_column_lab),
                        html.P(df["Origen"][i], className="p-texts-white",
                               style={"padding": "0", "color": back_color, "text-align": "left", "width": "50%"}),
                    ], style={"display": "flex", "justify-content": "center"}),
                    html.Br(),
                    html.Div([
                        html.P("Importancia agrícola:", className="p-texts-white",
                               style=styles_two_column_lab),
                        html.P(df["Importancia agricola"][i], className="p-texts-white",
                               style=styles_two_column_val),
                    ], style={"display": "flex", "justify-content": "center"}),
                    html.Br(),
                    html.Div([
                        html.P("Hábito alimenticio:", className="p-texts-white",
                               style=styles_two_column_lab),
                        html.P(df["Habito alimenticio"][i], className="p-texts-white",
                               style=styles_two_column_val),
                    ], style={"display": "flex", "justify-content": "center"}),
                    # One column
                    html.Br(),
                    dbc.Button(
                        "Más información",
                        href=df["Checklist"][i],
                        target="_blank",
                        color="info",
                        outline=True
                    ),
                    # html.P("Más información:", className="p-texts-white",
                    #        style={"margin-bottom": "0", "padding": "0"}),
                    # html.P(df["Checklist"][i], className="p-texts-white"),
                    html.Br(),
                    html.Br(),
                    html.Hr(),
                ], style={"text-align": "center"}
            )
        )

    layout = html.Div(children)

    return layout


# Methods & contents
insects_methods = html.P(
    "Se presentan los datos obtenidos en 40 fincas que se encuentran bajo Acuerdos de Conservación en Santa Cruz. "
    "Se colectaron insectos utilizando aspiradores y redes en áreas cultivadas y no cultivadas. ",
    className="p-texts-white")
insects_methods_2 = html.P(
    "Los insectos colectados en el campo fueron almacenados en frascos y transportados hacia la Estación Científica "
    "Charles Darwin (FCD). "
    "En el laboratorio, se limpió, clasificó e identificó cada individuo. ",
    className="p-texts-white")
insects_methods_3 = html.P(
    "La información publicada refleja los datos obtenidos en 41 fincas que se encuentran bajo Acuerdos de Conservación "
    "en Santa Cruz. Para esto, se trazó transectos en las áreas cultivadas y no cultivadas para realizar colecta manual, utilizando aspiradores y redes entomológicas. ",
    className="p-texts-white")
insects_methods_4 = html.P(
    "Utilice los botones debajo para mostrar los insectos más frecuentes por sector. "
    "Los resultados se pueden ver por nombre común o por nombre científico. "
    "Recuerde que un nombre común puede referirse a uno o varios nombres científicos.",
    className="p-texts-white")
insects_methods_5 = html.P(
    "La mayoría de los individuos analizados tienen origen desconocido y casi la misma proporción son insectos introducidos. "
    "Menos del 10% de los individuos que encontramos son endémicos o nativos.",
    className="p-texts-white")

insects_methods_6 = html.P(
    "El 100% de estos insectos ha sido identificado hasta algún nivel, y el 55% (9093 individuos) "
    "ha sido identificado hasta nivel de especie.",
    className="p-texts-white")

def_endemic = html.P(
    "Especie que sólo habita en Galápagos y no se encuentra naturalmente en otras partes del mundo.",
    className="p-texts")
def_introduced = html.P(
    "Especie que llegó a Galápagos a través de actividades humanas desde otras partes del mundo.",
    className="p-texts")
def_native = html.P(
    "Especie que llegó de manera natural a Galápagos y que se encuentra en otros lugares del mundo.",
    className="p-texts")
def_unknown = html.P("Cuando no existe certeza del origen de una especie.",
                     className="p-texts")

insects_importance_1 = html.P(
    "Los insectos mostrados debajo han sido seleccionados por su importancia para la zona agrícola,"
    "", className="p-texts-white")

plants_methods = html.P(
    "Aquí se presentan los datos obtenidos en 40 fincas que se encuentran bajo Acuerdos de Conservación en Santa Cruz. "
    "se recorrió las diferentes zonas de cada finca (bordes de caminos, pastizales, áreas cultivadas y no cultivadas, "
    "zonas habitadas y otras partes especificas) y se registraron todas las especies de plantas vasculares encontradas.",
    className="p-texts-white")

plants_methods_2 = html.P(
    "En caso de encontrar nuevas especies para Galápagos, plantas desconocidas o especies sin especímenes en el herbario, "
    "se tomó registros fotográficos y se colectó especímenes botánicos. Se procesó y se identificó los especímenes "
    "hasta el nivel taxonómico posible y se los procesó para su ingreso a la colección del herbario custodiado por la FCD.",
    className="p-texts-white")

plants_methods_3 = html.P(
    "Utilice los botones debajo para mostrar las plantas más frecuentes por sector. "
    "Los resultados se pueden ver por nombre común o científico. "
    "Recuerde que un nombre común puede referirse a una o varias especies.",
    className="p-texts-white")
