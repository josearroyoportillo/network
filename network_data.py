import pandas as pd
import re

df_f = pd.read_excel('data.xlsx', sheet_name='Masterkopf_Eingefügt')
df_f['edge_class'] = df_f['edge_class'].str.lower()
df_f['edge_class'] = df_f['edge_class'].str.replace(' ', '')
df_f['target'] = df_f['target'].str.replace(" ", "")
df_f['target'] = df_f['target'].astype(str)
df_f['source'] = df_f['source'].astype(str)
df_f['name'] = df_f['name'].astype(str)
df_f['class'] = df_f['source'].astype(str).replace(".", "_")
df_f['beeinflusst'] = 'nothing'
df_f['beeinflusst_neg'] = 'nothing'
df_f['node_class'] = ''
df_f = df_f.astype(str)

# the next section is for dash
df = df_f

# the for-loop that organises each node into its parent node according to rules
for index, content in df.iterrows():
    child = re.search(r"([a-z]+\_[0-9]+\_(NI|N)\_[0-9]+\.[0-9]+)", content['target'])
    # this is for the rows with one period
    if child is not None:
        parent = re.search(r"([a-z]+\_[0-9]+\_(NI|N)\_[0-9]+)", content['target'])
        content['source'] = parent.group()
        continue

    # this is for the rows with three digits after the period,
    child = re.search(r"([a-z]+\_[0-9]+\_(NI|N)\_[0-9]+\.[0-9][0-9][0-9])", content['target'])
    if child is not None:
        parent = re.search("[a-z]+\_[0-9]+\_(NI|N)\_[0-9]+\.[0-9][0-9]", content['target'])
        content['source'] = parent.group()
        continue

    # this is for the rows with a zero after the non one digits
    child = re.search(r"([a-z]+\_[0-9]+\_(NI|N)\_[0-9]+\.[2-9]0)", content['target'])
    if child is not None:
        parent = re.search("[a-z]+\_[0-9]+\_(NI|N)\_[0-9]+\.[2-9]", content['target'])
        content['source'] = parent.group()
        continue

    # this is for the rows that are the parent rows of all the sub cats
    temp_source = re.search(r"[TP]", content['source'])
    child = re.search(r"([a-z]+\_[0-9]+\_(NI|N)\_[0-9]+)", content['target'])
    if temp_source is not None and child is not None:
        parent = re.search("[a-z]+\_[0-9]+\_(NI|N)", content['target'])
        content['source'] = parent.group()
        continue

    # this is for the rows that have have three digits at the end but no period
    child = re.search(r"([a-z]+\_[0-9]+\_(NI|N)\_[0-9][0-9][0-9])", content['target'])
    if child is not None:
        parent = re.search("[a-z]+\_[0-9]+\_(NI|N)\_[0-9][0-9]", content['target'])
        content['source'] = parent.group()
        continue


# this is to create a part of the dataframe that is specifically for positive add_ons
for index, content in df.iterrows():
    child_assoc = re.search(r"(Beeinflusst: | Wird beeinflusst von:)", content['Wirkt positiv auf?'])
    if child_assoc is not None:
        parent_assoc_str = content['Wirkt positiv auf?'].split('+')
        sections = []
        for section in parent_assoc_str:
            if 'Entspricht' in section:
                continue
            if re.search(r'(Beeinflusst|beeinflusst)', section) is not None:
                section = section.replace('Beeinflusst:', '')
                section = section.replace('Wird beeinflusst von:', '')
                section = section.replace('Beinflusst/Wird beeinflusst:', '')
                section = section.replace(' ', '')
                section = section.replace(' (=Respekt)', '')
                section = section.replace('(=Respekt)', '')
                section = section.split(';')
                sections.extend(section)
        sections = list(filter(None, sections))
        content['beeinflusst'] = sections

# this is to create a part of the dataframe that is specifically for negative add_ons
for index, content in df.iterrows():
    child_assoc = re.search(r"(Beeinflusst (neg.): | Wird beeinflusst (neg.):)", content['Wirkt negativ auf?'])
    if child_assoc is not None:
        parent_assoc_str = content['Wirkt negative auf?'].split('+')
        sections = []
        for section in parent_assoc_str:
            if 'Entspricht' in section:
                continue
            if re.search(r'(Beeinflusst|beeinflusst)', section) is not None:
                section = section.replace('Beeinflusst (neg.):', '')
                section = section.replace('Wird beeinflusst (neg.):', '')
                section = section.replace('Beinflusst/Wird beeinflusst:', '')
                section = section.replace(' ', '')
                section = section.replace(' (=Respekt)', '')
                section = section.replace('(=Respekt)', '')
                section = section.split(';')
                sections.extend(section)
        sections = list(filter(None, sections))
        content['beeinflusst_neg'] = sections

# creating the default data for dash
elements_list = [
    # base nodes
    {'data': {'id': 'voss', 'label': 'Vossloh'},
     'position': {'x': 450, 'y': 50},
     'locked': True,
     'selectable': False,
     'grabbable': False
     },
    {'data': {'id': 'TP1', 'label': 'TP1'},
     'classes': 'tp1'},
    {'data': {'id': 'TP2', 'label': 'TP2'},
     'classes': 'tp2'},
    {'data': {'id': 'TP3', 'label': 'TP3'},
     'classes': 'tp3'},
    {'data': {'id': 'TP4', 'label': 'TP4'},
     'classes': 'tp4'},
    {'data': {'id': 'TP5.1', 'label': 'TP5.1'},
     'classes': 'tp5_1'},
    {'data': {'id': 'TP5.2', 'label': 'TP5.2'},
     'classes': 'tp5_2'},
    {'data': {'id': 'TP6', 'label': 'TP6'},
     'classes': 'tp6'},
    # base edges
    {'data': {'source': 'voss', 'target': 'TP1'}},
    {'data': {'source': 'voss', 'target': 'TP2'}, 'classes': 'tp2'},
    {'data': {'source': 'voss', 'target': 'TP3'}, 'classes': 'tp3'},
    {'data': {'source': 'voss', 'target': 'TP4'}, 'classes': 'tp4'},
    {'data': {'source': 'voss', 'target': 'TP5.1'}, 'classes': 'tp5_1'},
    {'data': {'source': 'voss', 'target': 'TP5.2'}},
    {'data': {'source': 'voss', 'target': 'TP6'}, 'classes': 'tp6'}]

temp_node_dict = {}
temp_edge_dict = {}
add_node_dict = {}
add_edge_dict = {}

nodes = set()

cy_edges = []
cy_nodes = []

# creates all data into dictionaries that will be used as reference within dash
for index, content in df.iterrows():
    idl = content['target']
    sourcel = content['source']
    targetl = content['target']
    labell = content['name'][0:100]
    edge_c = content['edge_class']

    node_class_regex = re.search(r"([a-z]+)", targetl)
    node_class = str(node_class_regex.group())

    cy_edge = {'data': {'id': str(sourcel) + str(targetl), 'source': str(sourcel), 'target': str(targetl)},
               'classes': edge_c}
    cy_source = {'data': {'id': str(sourcel), 'label': str(labell)},
                 'classes': node_class}
    cy_target = {'data': {'id': str(targetl), 'label': str(labell) + ' - ' + str(idl)},
                 'classes': node_class}

    if sourcel not in elements_list:
        nodes.add(sourcel)
        cy_nodes.append(cy_source)
    if targetl not in elements_list:
        nodes.add(targetl)
        cy_nodes.append(cy_target)

    if not temp_node_dict.get(sourcel):
        temp_node_dict[sourcel] = []
    if not temp_edge_dict.get(sourcel):
        temp_edge_dict[sourcel] = []

    temp_node_dict[sourcel].append(cy_target)
    temp_edge_dict[sourcel].append(cy_edge)

    if not temp_node_dict.get(targetl):
        temp_node_dict[targetl] = []
    if not temp_edge_dict.get(targetl):
        temp_edge_dict[targetl] = []

    temp_node_dict[targetl].append(cy_source)
    temp_edge_dict[targetl].append(cy_edge)

    # additional edges to show positive cross formations
    if content['beeinflusst'] != 'nothing':
        for item in content['beeinflusst']:
            try:
                add_label = df[df['target'] == item]['name'].values[0]
            except Exception:
                continue
            add_node_class_regex = re.search(r"([a-z]+)", item)
            add_node_class = str(add_node_class_regex.group())
            cy_edge_add = {'data': {'source': targetl, 'target': item},
                           'classes': 'treiberrelativ'}
            cy_node_add = {'data': {'id': item, 'label': add_label + ' - ' + item},
                           'classes': add_node_class}

            if not add_node_dict.get(item):
                add_node_dict[item] = []
            if not add_node_dict.get(targetl):
                add_node_dict[targetl] = []

            add_node_dict[item].append(cy_node_add)
            add_node_dict[targetl].append(cy_node_add)
            cy_nodes.append(cy_node_add)

            if not add_edge_dict.get(targetl):
                add_edge_dict[targetl] = []

            add_edge_dict[targetl].append(cy_edge_add)

    # additional edges to show negative cross formations
    if content['beeinflusst_neg'] != 'nothing':
        for item in content['beeinflusst_neg']:
            add_node_class_regex = re.search(r"([a-z]+)", item)
            add_node_class = str(add_node_class_regex.group())
            cy_edge_add = {'data': {'source': targetl, 'target': item},
                           'classes': 'barriererelativ'}
            cy_node_add = {'data': {'id': item, 'label': item},
                           'classes': add_node_class}

            if not add_node_dict.get(item):
                add_node_dict[item] = []
            if not add_node_dict.get(targetl):
                add_node_dict[targetl] = []

            add_node_dict[item].append(cy_node_add)
            add_node_dict[targetl].append(cy_node_add)
            cy_nodes.append(cy_node_add)

            if not add_edge_dict.get(targetl):
                add_edge_dict[targetl] = []

            add_edge_dict[targetl].append(cy_edge_add)

default_elements = elements_list