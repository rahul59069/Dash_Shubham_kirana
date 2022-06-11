import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input , Output
import pandas as pd
import dash_table


app = dash.Dash(__name__,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=0.8, maximum-scale=1.0, minimum-scale=0.5,'}])
server = app.server
# df = pd.read_csv(open('item_list_11_april.csv', errors='replace'))
df = pd.read_csv("item_list_11_april.csv",engine='python')
df = df[['Item name*','MRP']]
df['MRP'] = u"\u20B9"+' ' + df['MRP'].astype('str')

app.layout = html.Div(children=[
    html.H1('Shubham Kirana',style={'textAlign':'center'}),
    html.H3('Discount upto 40% on MRP Please contact 7858893934 for Home Delivery',style={'textAlign':'center'}),
    html.H4(children='You can search Items Available in our store.'),
    dcc.Dropdown(
        id='dropdown',
        options=[{"label": i, "value": i} 
                  for i in df['Item name*']],
        multi=True,
        value='',
        placeholder="Search Products"
    ),
    html.Button('Clear Search', id='btn', n_clicks=0),
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} 
                  for i in df.columns],
        data=df.to_dict('records'),
        style_cell=dict(textAlign='center'),
        page_action='none',
        page_size = 50,
        fixed_rows={'headers': True},
        style_table={'height': '500px','OverflowY' : 'auto'},
        style_data_conditional=[
            {'if': {'column_id': 'Item name*'},
         'width': '50%'},
        {'if': {'column_id': 'MRP'},
         'width': '50%'},
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)'
        }
    ],
    style_header={
        'backgroundColor': 'rgb(230, 230, 230)',
        'fontWeight': 'bold'
    }
    ),
])

@app.callback(
    Output('table', 'data'),
    Output('dropdown', 'value'),
    Input('dropdown', 'value'),
    Input('btn', 'n_clicks')
    )
def update_output(value,n_click):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'btn' in changed_id:
        return df.to_dict('records'),''
    if value == '':
        dff = df
    else:
        dff = df[df['Item name*'].isin(value)]
    return dff.to_dict('records'),value


if __name__ == '__main__':
    app.run_server(debug=True,host="192.168.1.9")