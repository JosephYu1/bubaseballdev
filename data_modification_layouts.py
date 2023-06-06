from app import app
import pandas as pd
import base64
import io
from dash.dependencies import Input, Output, State
from dash import html, dcc, dash_table, dash, callback_context
import dash_bootstrap_components as dbc
import os
import time
import data as DATA
from src.tools import data_processing as dp


DATA_FOLDER_PATH = "data_raw"



def get_file_creation_time(filepath):
    created_at = os.path.getctime(filepath)
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(created_at))


def list_csv_files(folder_path):
    return [f for f in os.listdir(folder_path) if f.endswith('.csv')]

@app.callback(
    Output('uploaded-data-table', 'data'),
    Output('uploaded-data-table', 'columns'),
    Output('alerts', "children"),
    Input('upload-data', 'contents'),
    Input('selected-file', 'children'),
    Input('url', 'pathname'),  # Keep this input
    State('upload-data', 'filename'),
    Input('select-date-format', 'value')
)
def update_data_table(contents, selected_file, pathname, filename, date_format_key):
    ctx = callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_input == 'upload-data' and contents:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'csv' in filename:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

                # --- update date format and other things like unit correction here ---
                df = dp.process_w_date(df, filename, DATA.DATE_DICT.get(date_format_key))

                columns = [{"name": i, "id": i} for i in df.columns]
                data = df.to_dict('records')
                msg = dbc.Alert("File read and processing successful!", 
                            color = "success",
                            dismissable=True,
                            fade = False,
                            is_open = True
                            )

                return data, columns, msg
        except Exception as e:
            print(e)
            msg = dbc.Alert(f'File read failed, error: {e}', 
                            color = "danger",
                            dismissable=True,
                            fade = False,
                            is_open = True
                            )
            return [{}], [], msg
    elif triggered_input == 'edit-selected-file' and pathname == '/edit-data' and selected_file:
        folder_path = "data_raw"
        file_path = os.path.join(folder_path, selected_file)

        df = pd.read_csv(file_path)
        
        # --- update date format and other things like unit correction here ---
        df = dp.process_w_date(df, file_path, DATA.DATE_DICT.get(date_format_key))

        columns = [{"name": i, "id": i} for i in df.columns]
        data = df.to_dict('records')
        return data, columns, html.Div("")

    return dash.no_update, dash.no_update, html.Div("")




import os

format_selection = html.Div(
    [
        dbc.Row(
            children = [
                dbc.Col(
                    html.Div(
                        children=["Please select a Date format BEFORE uploading the file"]
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id='select-date-format',
                        options = [{"label" : k, "value" : k} for k in DATA.DATE_DICT.keys()],
                        value = list(DATA.DATE_DICT.keys())[0] # default to yyyy/mm/dd
                    )
                )
            ]
        ),
    ]
)

upload_layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }
    ),
    html.Div(id='output-data-upload'),
    dcc.Loading(
        id='loading-icon',
        type='circle',
        children=[
            dash_table.DataTable(
                id='uploaded-data-table',
                editable=True,
                page_action='native',  # Add page_action
                page_size=15,  # Add page_size
                style_table={'overflowX': 'auto', 'height': '450px', 'overflowY': 'auto'},
                css=[{"selector": ".dash-cell div.dash-cell-value", "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;"}]
            )
        ]
    ),
    html.Div(id = 'alerts',),
    html.Button('Save File', id='save-file-button', n_clicks=0, style={'display': 'none'}),  # Set the initial style to 'none'
    html.Div(id='save-file-output'),
    html.Div(id='selected-file', style={'display': 'none'})  # Add this line
])


edit_layout = html.Div([
    html.Div(id='csv-file-list'),
    html.Div(id='selected-file-output'),
    dash_table.DataTable(
        id='file-table',
        columns=[
            {"name": "Name", "id": "name"},
            {"name": "Uploaded at", "id": "uploaded_at"},
        ],
        data=[],
        row_selectable="multi",  # Change to multi
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'minWidth': '100px', 'whiteSpace': 'normal'},
        page_size=10,
    ),
    html.Div(id='selected-file', style={'display': 'none'}), 
    html.Div(id='edit-selected-file'),
    dash_table.DataTable(
        id='edit-csv-table',
        editable=True,
        page_action='native',
        page_size=15,
        style_table={'overflowX': 'auto', 'height': '450px', 'overflowY': 'auto', 'display': 'none'},
        css=[{"selector": ".dash-cell div.dash-cell-value", "rule": "display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;"}]
    ),
    html.Button('Edit', id='edit-file-button', disabled=True),  # Add this button
    html.Button('Delete', id='delete-file-button', disabled=True)  # Add this button
])

@app.callback(
    Output('edit-csv-table', 'data'),
    Output('edit-csv-table', 'columns'),
    Input('edit-file-button', 'n_clicks'),
    State('selected-file', 'children'),
    prevent_initial_call=True
)
def display_selected_csv(n_clicks, selected_file):
    if n_clicks and selected_file:
        folder_path = "data_raw"
        file_path = os.path.join(folder_path, selected_file[0])  # Get the first selected file

        df = pd.read_csv(file_path)
        columns = [{"name": i, "id": i} for i in df.columns]
        data = df.to_dict('records')
        return data, columns
    return dash.no_update, dash.no_update


@app.callback(
    Output('save-file-output', 'children'),
    Input('save-file-button', 'n_clicks'),
    State('uploaded-data-table', 'data'),
    State('uploaded-data-table', 'columns'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def save_edited_file(n_clicks, data, columns, filename):
    print("SAVING")
    if n_clicks and data and columns and filename:
        df = pd.DataFrame(data, columns=[col['name'] for col in columns])

        file_path = os.path.join(DATA_FOLDER_PATH, filename)
        df.to_csv(file_path, index=False)

        return dbc.Alert(f"File saved as {filename} in the 'data_raw' folder.", color="success", dismissable=True, fade=False, is_open=True)
    return dash.no_update

@app.callback(
    Output('upload-data', 'style'),
    Output('save-file-button', 'style'),
    Input('uploaded-data-table', 'data'))
def toggle_upload_button(data):
    if data and len(data) > 0 and data[0]:
        print(data, len(data), data[0])
        return {'display': 'none'}, {'display': 'block'}
    else:
        return {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }, {'display': 'none'}

@app.callback(
    Output('file-table', 'style'),
    Output('edit-csv-table', 'style'),
    Input('selected-file', 'children')
)
def toggle_table_visibility(selected_file):
    if selected_file:
        # If selected-file has content, hide file-table and show edit-csv-table
        return {'display': 'none'}, {'display': 'block'}
    else:
        # If selected-file is empty, show file-table and hide edit-csv-table
        return {'display': 'block'}, {'display': 'none'}




@app.callback(
    Output('file-table', 'data'),
    Input('selected-file-output', 'children')
)
def update_file_table(current_files):
    folder_path = "data_raw"
    file_list = list_csv_files(folder_path)
    files = []

    for f in file_list:
        file_path = os.path.join(folder_path, f)
        uploaded_at = get_file_creation_time(file_path)
        files.append({'name': f, 'uploaded_at': uploaded_at})

    return files


@app.callback(
    Output('selected-file-output', 'children'),
    Input('delete-file-button', 'n_clicks'),
    State('file-table', 'selected_rows'),
    State('file-table', 'data'),
    prevent_initial_call=True
)
def delete_files(n_clicks, selected_rows, files):
    if n_clicks and selected_rows:
        folder_path = "data_raw"
        for row in selected_rows:
            file_to_delete = files[row]['name']
            file_path = os.path.join(folder_path, file_to_delete)
            if os.path.exists(file_path):
                os.remove(file_path)

        # Add this line to trigger the update_file_table callback
        return 'Files deleted'
    return dash.no_update




@app.callback(
    Output('edit-file-button', 'disabled'),
    Output('delete-file-button', 'disabled'),
    Input('file-table', 'selected_rows')
)
def update_button_states(selected_rows):
    if selected_rows:
        if len(selected_rows) == 1:
            return False, False
        else:
            return True, False
    else:
        return True, True


@app.callback(
    Output('selected-file', 'children'),
    Input('file-table', 'selected_rows'),
    Input('edit-file-button', 'n_clicks'),
    State('file-table', 'data'),
    prevent_initial_call=True
)
def set_or_edit_selected_file(selected_rows, n_clicks, files):
    ctx = callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]

    # If triggered by selecting rows in the file-table
    if triggered_input == 'file-table':
        if selected_rows:
            return [files[i]['name'] for i in selected_rows]
        return None

    # If triggered by clicking the edit-file-button
    elif triggered_input == 'edit-file-button':
        if n_clicks and selected_rows:
            return files[selected_rows[0]]['name']
        return None

    return dash.no_update


# @app.callback(
#     Output('file-table', 'data'),
#     Input('delete-file-button', 'n_clicks'),
#     State('file-table', 'selected_rows'),
#     State('file-table', 'data'),
#     prevent_initial_call=True
# )
# def delete_csv(n_clicks, selected_rows, files):
#     if n_clicks and selected_rows:
#         for i in selected_rows:
#             file_path = os.path.join(DATA_FOLDER_PATH, files[i]['name'])
#             if os.path.exists(file_path):
#                 os.remove(file_path)
#         return update_file_table(None)  # Refresh the file table
#     return dash.no_update

