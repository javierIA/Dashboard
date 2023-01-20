import dash
from dash import dcc
from dash import html
from utils import covert_to_df, get_knowledge_area_data
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Cargar datos en un DataFrame
df = covert_to_df()


# Cargar datos en un DataFrame

# Crear una función para obtener los datos agrupados y contados por área de conocimiento

# Crear una aplicación de Dash
app = dash.Dash()

# Agregar una barra de navegación y una descripción del dashboard
app.layout = html.Div([
   
    # Agregar una lista desplegable para seleccionar el tipo de aprendizaje
    dcc.Dropdown(id="learning-type-dropdown",
                
                 options=[{"label": learning_type, "value": learning_type} for learning_type in df["KnowledgeType"].unique().tolist() + ["All"] if learning_type != "KnowledgeDiscipline"],
                 value="All"),
    # Agregar un componente de salida para mostrar la gráfica de barras
    dcc.Graph(id="knowledge-area-bar-chart"),
])

# Crear una función de devolución de llamada que se ejecute cuando el usuario seleccione una opción de la lista desplegable
@app.callback(
    dash.dependencies.Output("knowledge-area-bar-chart", "figure"),
    [dash.dependencies.Input("learning-type-dropdown", "value")])
def update_knowledge_area_bar_chart(learning_type):
    if learning_type == "All":
        data = df.groupby("Knowledge")["Researcher"].count()
        return {
            "data": [go.Bar(x=data.index, y=data.values)],
            "layout": go.Layout(title="Áreas de Conocimiento", xaxis={"title": "Área de Conocimiento"}, yaxis={"title": "Numero de Investigadores"})
            
            }
    else:
        data = get_knowledge_area_data(learning_type,df)
        return {
            "data": [go.Bar(x=data.index, y=data.values)],
            "layout": go.Layout(title="Áreas de Conocimiento", xaxis={"title": "Área de Conocimiento"}, yaxis={"title": "Numero de Investigadores"})
        }
    

# Ejecutar la aplicación
if  __name__ == "__main__":
    app.run_server(debug=True)
