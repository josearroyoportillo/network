import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from network_data import default_elements, temp_node_dict, temp_edge_dict, add_edge_dict, add_node_dict

# load extra layouts
cyto.load_extra_layouts()

network = html.Div([
    html.Button('Reset', id='reset_button', n_clicks=0),
    html.Div(id='content', children=[]),
    html.Div([
        cyto.Cytoscape(
            id='cytoscape',  # id is used for callbacks
            style={'width': '100%', 'height': '800px'},
            elements=default_elements,
            layout={'name': 'cola'},
            # styles for nodes and edges depending on teilprojekt
            stylesheet=[
                {
                    'selector': 'nodes',
                    'style': {
                        'label': 'data(label)',
                        'text-wrap': 'wrap',
                        'font-size': '10px',
                        'text-max-width': '5px',
                        'width': '13px',
                        'height': '13px'
                    }
                },
                {
                    'selector': 'edge',
                    'style': {
                        'width': '2px',
                    }
                },
                {
                    'selector': '.tp1',
                    'style': {
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.tp2',
                    'style': {
                        'background-color': '#b49f28',
                        'line-color': '#b49f28',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.wm',
                    'style': {
                        'background-color': '#b49f28',
                        'line-color': '#b49f28',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.tp3',
                    'style': {
                        'background-color': '#3c1e5a',
                        'line-color': '#3c1e5a',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.shm',
                    'style': {
                        'background-color': '#3c1e5a',
                        'line-color': '#3c1e5a',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.tp4',
                    'style': {
                        'background-color': '#003c28',
                        'line-color': '#003c28',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.p',
                    'style': {
                        'background-color': '#003c28',
                        'line-color': '#003c28',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.tp5_1',
                    'style': {
                        'background-color': '#3c140a',
                        'line-color': '#3c140a',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.cm',
                    'style': {
                        'background-color': '#3c140a',
                        'line-color': '#3c140a',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.tp5_2',
                    'style': {
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.tp6',
                    'style': {
                        'background-color': '#142850',
                        'line-color': '#142850',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.co',
                    'style': {
                        'background-color': '#142850',
                        'line-color': '#142850',
                        'font-size': '8px'
                    }
                },
                {
                    'selector': '.treiberrelativ',
                    'style': {
                        'line-color': '#00c81e',
                    }
                },
                {
                    'selector': '.treiberabsolut',
                    'style': {
                        'line-color': '#00c81e',
                    }
                },
                {
                    'selector': '.barriererelativ',
                    'style': {
                        'line-color': '#e6001f',
                    }
                },
                {
                    'selector': '.barriereabsolut',
                    'style': {
                        'line-color': '#e6001f',
                    }
                },
            ]
        )
    ])
])


# callbacks for updating the nodes
@app.callback(
    Output('cytoscape', 'elements'),
    [Input('cytoscape', 'tapNodeData'),
     Input('reset_button', 'n_clicks')],
    State('cytoscape', 'elements'))
def generate_elements(nodeData, n_clicks, elements):
    # reset button functionality
    if n_clicks > 0:
        return default_elements

    if not nodeData:
        return default_elements

    # If the node has already been expanded, we don't expand it again
    if nodeData.get('expanded') is True:
        selected_nodes = temp_node_dict.get(nodeData['id'])
        add_selected_nodes = add_node_dict.get(nodeData['id'])

        if selected_nodes:
            elements = [elem for elem in elements if elem not in selected_nodes]
        if add_selected_nodes:
            elements = [elem for elem in elements if elem not in add_selected_nodes]

        for element in elements:
            if nodeData['id'] == element.get('data').get('id'):
                # noinspection PyTypeChecker
                element['data']['expanded'] = False
                break

        return elements

    # remove these if-statements for full node network view - start
    if nodeData['id'] == 'TP1':
        elements = [elements[1]]
    elif nodeData['id'] == 'TP2':
        elements = [elements[2]]
    elif nodeData['id'] == 'TP3':
        elements = [elements[3]]
    elif nodeData['id'] == 'TP4':
        elements = [elements[4]]
    elif nodeData['id'] == 'TP5.1':
        elements = [elements[5]]
    elif nodeData['id'] == 'TP5.2':
        elements = [elements[6]]
    elif nodeData['id'] == 'TP6':
        elements = [elements[7]]
    # end

    # retrieves normal nodes and edges
    selected_nodes = temp_node_dict.get(nodeData['id'])
    selected_edges = temp_edge_dict.get(nodeData['id'])

    if selected_nodes:
        elements.extend(selected_nodes)

    if selected_edges:
        elements.extend(selected_edges)

    # retrieves connections that lay outside of the original teilprojekt
    add_selected_nodes = add_node_dict.get(nodeData['id'])
    add_selected_edges = add_edge_dict.get(nodeData['id'])

    if add_selected_nodes:
        elements.extend(add_selected_nodes)

    if add_selected_edges:
        elements.extend(add_selected_edges)

    # This retrieves the currently selected element, and tag it as expanded
    for element in elements:
        if nodeData['id'] != element.get('data').get('id'):
            continue
        # noinspection PyTypeChecker
        element['data']['expanded'] = True
        break

    return elements
