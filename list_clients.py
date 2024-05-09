import json

json_path = 'C:\\Users\\thiag\\Desktop\\Video AI\\Dashboard\\videoai.clients.json'
clients_path = 'C:\\Users\\thiag\\Desktop\\Video AI\\Dashboard\\clients.txt'
def load_json(json_path):
    with open(json_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def save_txt(clients_path, clients):
    with open(clients_path, 'w', encoding='utf-8') as file:
        for client in clients:
            file.write(f'{client["number"]} - {client["name"]}\n')

data = load_json(json_path)
clients = []

for item in data:
    number = item['client']
    name = item['info']['name']

    client_info = {
        'number': number,
        'name': name
    }

    clients.append(client_info)

save_txt(clients_path, clients)

