import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import textwrap

# Data for the squares graph
df = pd.read_csv('crying.csv')
categories = ['Light', 'Medium', 'Heavy']
values = {"Light": 20, "Medium": 20, "Heavy": 20}
colors = {"Light": "lightblue", "Heavy": "darkblue", "Medium": "blue"}
colorsCategory = {"Visual Media": "yellow", "Family": "orange", "Friends": "red",
                  "Surroundings (people/places/things/news)": "purple", "Crisis": "pink", "Random": "green",
                  "Music": "black"}
categoryCounts = {"Visual Media": 0, "Family": 0, "Friends": 0,
                  "Surroundings (people/places/things/news)": 0, "Crisis": 0, "Random": 0, "Music": 0}

# Create a figure with square markers
fig = go.Figure()
for ind, row in df.iterrows():
    if "Jan" in row['Date']:
        fig.add_trace(go.Scatter(
            y=[100 - values[row['Degree']]], x=[categories.index(row['Degree']) + 0.5],
            marker=dict(size=10, symbol="square", color=colors[row["Degree"]]),
            mode="markers",
            name=categories[categories.index(row['Degree'])],
        ))
        values[row['Degree']] += 50

fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    xaxis=dict(
        showgrid=False,  # Hide the grid
        zeroline=False,  # Hide the zero line
        showticklabels=False,  # Hide tick labels
    ),
    yaxis=dict(
        showgrid=False,  # Hide the grid
        zeroline=False,  # Hide the zero line
        showticklabels=False,  # Hide tick labels
    ),
    margin=dict(l=0, r=0, t=0, b=0),  # Minimize margin to utilize maximum screen area
    showlegend=False
)

# Create a Dash app and add the graph
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        #html.Img(src='eyesal.png', style={'width': '80%', 'height': 'auto', 'padding-top': '20px', 'padding-bottom': '20px' '<br>'}),  # Fixing image size
        html.Div([
            html.Img(src='assets/eyesal.png', style={'width': '80%', 'height': 'auto', 'max-width': '500px', 'display': 'block', 'padding-top': '500px', 'margin': '0 auto'}),  # Fixing image size
                    dcc.Graph(
                        id='squares-graph',
                        figure=fig,
                        style={'width': '80%', 'display': 'inline-block', 'margin': '20px'}
                    ), 
                    ], style={'textAlign': 'center', 'margin': '0 auto'}),

    #     dcc.Graph(
    #         id='squares-graph',
    #         figure=fig,
    #         style={'width': '26%', 'display': 'inline-block', 'margin': '0 auto'}
    #     ),
    # ], style={'textAlign': 'center'}
],),
    dcc.Dropdown(
        id='color-dropdown',
        options=[
            {'label': 'Jan', 'value': 'Jan'},
            {'label': 'Feb', 'value': 'Feb'},
            {'label': 'Mar', 'value': 'Mar'},
        ],
        value='Jan',  # Default value
        style={'width': '50%', 'margin': '0 auto'}  # Center the dropdown and adjust width
    ),
    html.Div([
        dcc.Graph(id="pie-chart", style={'width': '50%', 'display': 'inline-block', 'margin': '0 auto'})
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'width': '100%'})
], style={
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'center',
    'height': '100vh',
})


def wrap_hovertext(hovertext, width=20):
    wrapped_hovertext = ["<br>".join(textwrap.wrap(text, width=width)) for text in hovertext]
    s = ""
    for x in wrapped_hovertext:
        s += x
    return s


# Callback to update graph based on dropdown selection
@app.callback(
    Output('squares-graph', 'figure'),
    [Input('color-dropdown', 'value')]
)
def update_figure(selected_month):
    fig = go.Figure()
    values = {"Light": 20, "Medium": 20, "Heavy": 20}
    for ind, row in df.iterrows():
        htext = f"Date: {row['Date']}<br>Feeling: {row['Feeling']}<br>Story: {row['Story']}<br>Category: {row['Category']}"
        if selected_month in row['Date']:
            fig.add_trace(go.Scatter(
                y=[100 - values[row['Degree']]], x=[categories.index(row['Degree']) + 0.5],
                marker=dict(size=20, symbol="square", color=colors[row["Degree"]],
                            line=dict(width=2, color=colorsCategory[row["Category"]])),
                mode="markers",
                name=categories[categories.index(row['Degree'])],
                hoverinfo='text',
                hovertext=wrap_hovertext(htext),
            ))
            values[row['Degree']] += 0.5
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
        xaxis=dict(
            showgrid=False,  # Hide the grid
            zeroline=False,  # Hide the zero line
            showticklabels=False,  # Hide tick labels
        ),
        yaxis=dict(
            showgrid=False,  # Hide the grid
            zeroline=False,  # Hide the zero line
            showticklabels=False,  # Hide tick labels
        ),
        margin=dict(l=0, r=0, t=0, b=0),  # Minimize margin to utilize maximum screen area
        showlegend=False
    )
    return fig


# Callback to update pie chart based on dropdown selection
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('color-dropdown', 'value')]
)
def update_pie_figure(selected_month):
    # Simulate updating pie values based on the selected color
    categoryCounts = {"Visual Media": 0, "Family": 0, "Friends": 0,
                      "Surroundings (people/places/things/news)": 0, "Crisis": 0, "Random": 0, "Music": 0}
    fig = go.Figure()
    for ind, row in df.iterrows():
        htext = f"Date: {row['Date']}<br>Feeling: {row['Feeling']}<br>Story: {row['Story']}<br>Category: {row['Category']}"
        if selected_month in row['Date']:
            categoryCounts[row['Category']] += 1
    labels = []
    vals = []
    c = []
    for k in categoryCounts:
        labels.append(k)
        vals.append(categoryCounts[k])
        c.append(colorsCategory[k])
    fig = go.Figure(data=go.Pie(labels=labels, values=vals, marker_colors=c))
    fig.update_traces(textinfo='percent+label')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)