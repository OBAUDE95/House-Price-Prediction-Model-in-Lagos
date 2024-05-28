import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import pickle

# Load the model and column names from the pickle file
with open('best_model.pkl', 'rb') as f:
    loaded_model, loaded_columns = pickle.load(f)

# Define the house title mapping
title_mapping = {
    'Block of Flats': 0,
    'Detached Bungalow': 1,
    'Detached Duplex': 2,
    'Semi Detached Bungalow': 3,
    'Semi Detached Duplex': 4,
    'Terraced Bungalow': 5,
    'Terraced Duplexes': 6
}

# Initialize the Dash app with dark theme
app = dash.Dash( external_stylesheets=[dbc.themes.DARKLY])

server = app.server
# #setting password
# x = [['deji','ignore']]
# i = dash_auth.BasicAuth(app,x)

# Define the layout of the app using Bootstrap components
app.layout = dbc.Container([
    html.H1("Model Interface", className='mb-4 mt-5 text-center text-white'),
    html.P(
        "Welcome to the House Price Prediction Dashboard! "
        "Enter the details of the house below and click 'Submit' to get a predicted price. "
        "Use the dropdown to select the type of house, and fill in the number of bedrooms, bathrooms, toilets, and parking spaces. "
        "This tool uses a machine learning model trained on real estate data to provide you with an estimate.",
        className='text-center text-white'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Label("Bedrooms:", width=4, className='text-white'),
                dbc.Col(dbc.Input(id='bedrooms', type='number', value=2.0), width=8),
            ], className='mb-3'),
            dbc.Row([
                dbc.Label("Bathrooms:", width=4, className='text-white'),
                dbc.Col(dbc.Input(id='bathrooms', type='number', value=2.0), width=8),
            ], className='mb-3'),
            dbc.Row([
                dbc.Label("Toilets:", width=4, className='text-white'),
                dbc.Col(dbc.Input(id='toilets', type='number', value=2.0), width=8),
            ], className='mb-3'),
            dbc.Row([
                dbc.Label("Parking Space:", width=4, className='text-white'),
                dbc.Col(dbc.Input(id='parking_space', type='number', value=2.0), width=8),
            ], className='mb-3'),
            dbc.Row([
                dbc.Col(
                    html.Div([
                        html.Label("House Type:", className='text-white'),
                        dcc.Dropdown(
                            id='title',
                            options=[{'label': k, 'value': v} for k, v in title_mapping.items()],
                            value=6,  # Default value
                            clearable=False,
                            className='mb-3'
                        ),
                    ]), width=8, className='mb-3'
                ),
            ]),
            dbc.Row([
                dbc.Col(dbc.Button('Submit', id='submit-val', n_clicks=0, color='primary'), width={"size": 6, "offset": 3}),
            ])
        ], width=6)  # Adjust width as needed
    ], justify='center'),
    html.Div(id='output-container-button', className='text-center text-white')
], className='py-5')

# Define callback to update output based on input
@app.callback(
    Output('output-container-button', 'children'),
    [Input('submit-val', 'n_clicks')],
    [Input('bedrooms', 'value'),
     Input('bathrooms', 'value'),
     Input('toilets', 'value'),
     Input('parking_space', 'value'),
     Input('title', 'value')]
)
def update_output(n_clicks, bedrooms, bathrooms, toilets, parking_space, title):
    if n_clicks > 0:  # Only predict after the button is clicked
        # Create a DataFrame for prediction
        new_data = pd.DataFrame({
            'bedrooms': [bedrooms],
            'bathrooms': [bathrooms],
            'toilets': [toilets],
            'parking_space': [parking_space],
            'title': [title]
        })

        # Ensure that the new data contains the same columns as the training data
        new_data = new_data[loaded_columns]

        # Use the loaded model to make predictions
        prediction = loaded_model.predict(new_data)

        return html.H4(f'Prediction: #{prediction[0]}', className='text-primary mt-4')

    return ''  # Return an empty string if button not clicked

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
