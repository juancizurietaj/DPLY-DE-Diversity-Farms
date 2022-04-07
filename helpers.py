import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, State, html, dash_table
import numpy as np

# Data load
data = pd.read_csv(r"assets/data_insectos_simp.csv")
data_p = pd.read_csv(r"assets/data_plantas_simp.csv")

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
                  label_style={"color": font_color, "fontSize": "calc(5rem + 1vw)"})
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
                    html.Div(
                        html.Div(create_meter(percentages[i], "info", "#43484e", "100%", "colored"),
                                 className="meter-container")
                    )
                ], style={"padding": "0rem 5rem"}
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
    examples = ex_df[examples_column][0:5]
    print(examples)


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
                    html.Div(
                        html.Div(create_meter(percentages[i], "info", "#43484e", "100%", "colored"),
                                 className="meter-container")
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


# Methods
insects_methods = html.P(
    "Aquí se presentan los datos obtenidos en 40 fincas que se encuentran bajo Acuerdos de Conservación en Santa Cruz. "
    "Se colectaron insectos utilizando aspiradores y redes entomológicas en transectos ubicados en áreas cultivadas y no cultivadas. ",
    className="p-texts-white")
insects_methods_2 = html.P(
    "Los insectos colectados en el campo fueron almacenados en frascos con alcohol al 75% (colección húmeda) "
    "o acetato de etilo (colección seca) y transportados hacia la Estación Científica Charles Darwin (FCD). "
    "En el laboratorio, se limpió, clasificó e identificó cada individuo hasta el nivel taxonómico posible. "
    "En esta herramienta se muestran los resultados de:",
    className="p-texts-white")
insects_methods_3 = html.P(
    "La información publicada refleja los datos obtenidos en 41 fincas que se encuentran bajo Acuerdos de Conservación en Santa Cruz. Para esto, se trazó transectos en las áreas cultivadas y no cultivadas para realizar colecta manual, utilizando aspiradores y redes entomológicas. Los insectos colectados fueron almacenados en frascos con alcohol al 75% (colección húmeda) o acetato de etilo (colección seca) y transportados hacia la Estación Científica Charles Darwin (FCD). En el laboratorio, se limpió, clasificó e identificó cada individuo hasta el nivel taxonómico posible.",
    className="p-texts-white")
insects_methods_4 = html.P(
    "Utilice los botones debajo para mostrar los insectos más frecuentes por sector. "
    "Los resultados se pueden ver por nombre común o por nombre científico. "
    "Recuerde que un nombre común puede referirse a uno o varios nombres científicos.",
    className="p-texts-white")
insects_methods_5 = html.P(
    "La mayoría de los individuos analizados tienen origen desconocido y casi la misma proporción son insectos introducidos."
    "Menos del 10% de los individuos que encontramos son endémicos o nativos.",
    className="p-texts-white")

insects_methods_6 = html.P(
    "El 100% de estos insectos ha sido identificado hasta algún nivel texonómico, y el 55% (1690 individuos) "
    "han sido identificado hasta nivel de especie.",
    className="p-texts-white")

def_endemic = html.P(
    "Una especie endémica es una especie que sólo habita en Galápagos y no se encuentra naturalmente en otras partes del mundo.",
    className="p-texts")
def_introduced = html.P(
    "Una especie introducida es una especie que llegó a Galápagos a través de actividades humanas desde otras partes del mundo.",
    className="p-texts")
def_native = html.P(
    "Una especie nativa es una especie que llegó de manera natural a Galápagos y que se encuentra en otros lugares del mundo.",
    className="p-texts")
def_unknown = html.P("Cuando no existe certeza del orígen de una especie, se la cataloga como de origen desconocido.",
                     className="p-texts")

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
    "Los resultados se pueden ver por nombre común o por nombre científico. "
    "Recuerde que un nombre común puede referirse a uno o varios nombres científicos.",
    className="p-texts-white")
