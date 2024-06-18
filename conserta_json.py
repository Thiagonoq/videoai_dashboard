from datetime import datetime
from pathlib import Path
import json
import re
import config

abs_path = Path(__file__).parent.parent
script_path = abs_path / 'Scripts'

analytics_file = config.analytics_json_path
new_analytics_file = config.new_analytics_json_path
new_list_file = config.list_json_path
clients_file = config.clients_json_path

analytics_path = abs_path / analytics_file
# file2_path = 'C:\\Users\\thiag\\Desktop\\Video AI\\Dashboard\\videoai.analytics2.json'
new_analytics_path = abs_path / new_analytics_file
list_path = abs_path / new_list_file
clients_path = abs_path / clients_file

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def equal_entries(entry1, entry2):
    return entry1 == entry2

def remove_structural_duplicates(data):
    unique_data = {}
    json_data = load_json(data)

    for entry in json_data:
        serialized_entry = json.dumps(entry, sort_keys=True)

        if serialized_entry not in unique_data:
            unique_data[serialized_entry] = entry

    return list(unique_data.values())

def remove_repeated_entries(data):
    print('Removendo entradas repetidas...')
    unique_data = remove_structural_duplicates(data)
    save_json(new_analytics_path, unique_data)

    seen_ids = set()
    repeated_ids = set()
    for entry in unique_data:
        if entry["_id"] in seen_ids:
            repeated_ids.add(entry["_id"])
        else:
            seen_ids.add(entry["_id"])

    # Retorna a lista de _ids repetidos
    return list(repeated_ids)

def combine_templates(templates):
    combined = {}
    for template in templates:
        name = template['name']
        if name not in combined:
            combined[name] = template
        else:
            # Soma dos dados numéricos e concatenação dos arrays
            combined[name]['published'] += template['published']
            combined[name]['requestedCatalog'] += template['requestedCatalog']
            for key in ['text', 'audio', 'image']:
                combined[name]['sended'][key] += template['sended'][key]
            for status in ['created', 'edited']:
                for result in ['failed', 'success', 'cancelled']:
                    combined[name]['usage'][status][result] += template['usage'][status][result]
            combined[name]['gpt']['usage'] += template['gpt']['usage']
            combined[name]['flows'] += template['flows']
    return list(combined.values())

def combine_clients(data):
    combined = {}
    for item in data:
        client = item['client']
        date = item['created_at'][:10] # Extrai apenas a data, ignorando o horário
        key = (client, date)
        if key not in combined:
            combined[key] = item
            combined[key]['templates'] = combine_templates(item['templates'])
        else:
            combined[key]['templates'] += item['templates']
            combined[key]['templates'] = combine_templates(combined[key]['templates'])
            # Mantem a data mais antiga
            combined[key]['updated_at'] = min(item['updated_at'], combined[key]['updated_at'], key=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"))
            # Mantém a data mais recente
            combined[key]['updated_at'] = max(item['updated_at'], combined[key]['updated_at'], key=lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"))
    return list(combined.values())

def merge_repeated_entries(json):
    print('Unificando entradas repetidas...')
    data = load_json(json)
    # Primeiro, combine os templates dentro de cada estrutura
    for item in data:
        item['templates'] = combine_templates(item['templates'])

    # Depois, combine as estruturas por cliente e data
    data_combined = combine_clients(data)

    save_json(new_analytics_path, data_combined)

def update_template_name(json):
    data = load_json(json)
    uuid_regex = re.compile(r'[a-f\d]{8}[a-f\d]{4}[a-f\d]{4}[a-f\d]{4}[a-f\d]{12}', re.IGNORECASE)
    hortifruti_remove = re.compile(r'Hortifruti - ')
    for item in data:
        for template in item['templates']:
            if uuid_regex.match(template['name']):
                template['name'] = 'NotIdentified'
            else:
                if hortifruti_remove.search(template['name']):
                    template['name'] = template['name'].replace('Hortifruti - ', '')
                
                template['name'] = template['name'].replace('Vídeo', 'Video')

    save_json(new_analytics_path, data)      

def list_clients(json):
    data = load_json(json)
    clients = []
    for item in data:
        if item['client'] not in clients:
            clients.append(item['client'])

    print(clients)

def delete_entry(json):
    data = load_json(json)
    for item in data:
        if item['client'] == '00000000000':
            data.remove(item)
            print('Entrada deletada: ', item['client'])
    save_json(json, data)

def list_del_empty_entries(json):
    print('Removendo entradas vazias...')
    empty_entries = False
    data = load_json(json)
    for item in data:
        if len(item['templates']) == 0:
            print('Entrada vazia: ', item['client'])
            data.remove(item)
            empty_entries = True
    save_json(new_analytics_path, data)
    return empty_entries

def verify_clients(analytics_json, clients_json):
    analytics_json = load_json(analytics_json)
    clients_json = load_json(clients_json)
    clients = [client['client'] for client in clients_json]

    unexisted_clients = []
    for index, item in enumerate(analytics_json):
        client = item['client']

        if client not in clients:
            if client not in unexisted_clients:
                unexisted_clients.append(client)
    
    print(unexisted_clients)

def data_handling():
    # 1º Passo: Remover entradas duplicadas(exatamente iguais)
    print('IDs repetidos: ', remove_repeated_entries(analytics_path))

    # 2º Passo: Remover entradas vazias
    empty_entries = list_del_empty_entries(new_analytics_path)

    # 3º Passo: Juntar estruturas repetidas(mesmo cliente, mesmo horário)
    merge_repeated_entries(new_analytics_path)

    # 4º Passo: Listar clientes e remover entradas do cliente "00000000000"
    # list_clients(new_analytics_path)
    # delete_entry(new_analytics_path)

    # 5º Passo: Retirar "Hortifruti - " do nome dos templates
    update_template_name(new_analytics_path)     

    # Extra: verificar se todos os clientes de analytics existem no clients
    # verify_clients(new_analytics_path, clients_path)

    return empty_entries, new_analytics_path

if __name__ == '__main__':
    update_template_name(new_analytics_path)