from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import config
import json
import conserta_json
import atualiza_devs
import google_drive_api
from pathlib import Path

abs_path = Path(__file__).parent.parent

# Acessar a URI sob a seção MongoDB
uri = config.uri
analytics_file = config.analytics_json_path

client = MongoClient(uri)
db = client['videoai']
collections = ['clients','cta_list_response', 'analytics']

json_path = abs_path / analytics_file

def import_json(client, db, collections):
    jsons_list = []
    for collection in collections:
        # if collection == 'clients':
        #     atualiza_devs.update_dev_info(db)

        date_name = 'created_at' if collection != 'cta_list_response' else 'date'
        date = datetime.combine(datetime.now(), datetime.min.time())

        document = db[collection].find({date_name: {"$lte": date}})
        data_path = abs_path / f'videoai.{collection}.json'
        
        with open(data_path, 'w', encoding='utf-8') as file:
            json.dump(list(document), file, default=str, ensure_ascii=False)

        jsons_list.append(data_path)

        if collection == 'analytics':
            empty_entries = conserta_json.data_handling()

            if empty_entries:
                del_entries_db(db, collection, date)
    upload_to_google_drive(jsons_list)
    print('Importação concluida')
    client.close()

def del_entries_db(db, collection, date):
    print(f'Removendo entradas anteriores a {date} em {collection}...')
    
    db[collection].delete_many({
        'templates': { '$size': 0 },
        'created_at': { '$lte': date }
})

def export_json_to_mongodb(client, db, json_path):
    collection = db['analytics']
    json_data = conserta_json.load_json(json_path)
    data = [convert_types(document) for document in json_data]

    if isinstance(data, list):
        collection.insert_many(data)
        print('Exportação concluida')
    else:
        print('Exportação falhou')

    client.close()

def convert_types(document):
    if '_id' in document and isinstance(document['_id'], str):
        document['_id'] = ObjectId(document['_id'])

    for date_field in ['created_at', 'updated_at']:
        if document.get(date_field, None) is not None:
            document[date_field] = datetime.strptime(document[date_field], '%Y-%m-%d %H:%M:%S.%f')

    if 'templates' in document:
        for template, in document['templates']:
            if 'flows' in template:
                for flow in template['flows']:
                    for key in ['started', 'ended']:
                        if flow.get(key, None) is not None:
                            flow[key] = datetime.strptime(flow[key], '%Y-%m-%d %H:%M:%S.%f')
    return document

def atualiza_produtos(db):
    collection = db['hortifruti_products']
    tips_path = 'C:\\Users\\thiag\\Desktop\\Video AI\\Banco de Imagens\\tips.json'
    tips = conserta_json.load_json(tips_path)

    for tip in tips:
        collection.update_one(
            {"product": tip['product']}, 
            {"$set": {"tips": tip['tips']}}
        )
        print(f'Produto atualizado: {tip["product"]}')
    
    print('Produtos atualizados')
    
def upload_to_google_drive(jsons_list):
    drive = google_drive_api.auth_drive()
    google_json_folder_id = '1WUNM-yF2zgDwDCKe-qX5Wl8lI-cC0A71'
    
    for json_path in jsons_list:
        try:
            file_name = json_path.name

            files_list = drive.ListFile({
                'q': f"title = '{file_name}' and '{google_json_folder_id}' in parents and trashed=false"
            }).GetList()

            if files_list:
                for file in files_list:
                    print(f"Deleting {file['title']}...")
                    file.Delete()

            file_drive = drive.CreateFile({
                'title': file_name,
                'parents': [{'id': google_json_folder_id}]})

            file_drive.SetContentFile(json_path)

            file_drive.Upload()

            print(f'Arquivo {file_name} enviado com sucesso!')

        except Exception as e:
            print(e)
            continue

if __name__ == '__main__':
    import_json(client, db, collections)
    # export_json_to_mongodb(client, db, json_path)
    # atualiza_produtos(db)