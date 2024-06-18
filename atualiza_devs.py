from pymongo import MongoClient
import config


uri = config.uri

client = MongoClient(uri)
db = client['videoai']

dev_phones = [
    "553598213600", # Lucia
    "553588176806", # Átila
    "553588896391", # Robert
    "553588516667", # Julio
    "553591929626", # Clever
    "553198929068", # Thiago
    "00000000000", # Teste Átila
]

no_logo = [
    '00000000000',
    '12345778041',
    '13349503246',
    '13512986392',
    '447710173736',
    '553171428818',
    '553171881279',
    '553186980142',
    '553195210643',
    '553196818216',
    '553197980002',
    '553198929068',
    '553199671788',
    '553298414647',
    '553398382063',
    '553491618409',
    '553499917851',
    '553588055538',
    '553588176806',
    '553588359784',
    '553588598904',
    '553588950830',
    '553597016087',
    '553597073566',
    '553597084666',
    '553597232382',
    '553597352837',
    '553597415328',
    '553598119038',
    '553788040536',
    '553798415103',
    '553899713624',
    '554188252980',
    '554191315011',
    '554196078774',
    '554199323568',
    '554298163863',
    '554299931989',
    '554391135670',
    '554699108620',
    '554699761218',
    '554796162662',
    '554797882607',
    '554799597088',
    '554884950191',
    '554891845666',
    '554892074455',
    '554899067355',
    '555192745082',
    '555197141416',
    '555198313565',
    '555384481994',
    '555399442873',
    '555492667562',
    '555493759828',
    '555499678296',
    '555591072360',
    '555599320284',
    '556192407495',
    '556196609528',
    '556295093510',
    '556295509728',
    '556392202717',
    '556392590659',
    '556392904325',
    '556399562912',
    '556481260918',
    '556493202764',
    '556592708191',
    '556596200123',
    '556684055749',
    '556699185357',
    '556699989292',
    '556791717453',
    '556792111944',
    '556792876709',
    '556796283405',
    '556796405358',
    '556796528201',
    '556796789031',
    '556798057726',
    '556799415775',
    '556899750181',
    '556981037920',
    '556992966202',
    '557188948127',
    '557191676328',
    '557398473460',
    '557399231434',
    '557488157813',
    '557591187729',
    '558179168103',
    '558182950321',
    '558187438855',
    '558194697274',
    '558381065937',
    '558381070569',
    '558399446597',
    '558488175867',
    '558494038575',
    '558496859660',
    '558588251088',
    '558588669032',
    '558592111350',
    '558592701476',
    '558599312999',
    '558599382082',
    '558695600182',
    '558695639435',
    '558698134633',
    '558699746911',
    '558781704228',
    '558788359625',
    '558791687140',
    '558881120893',
    '558888587368',
    '558894929884',
    '558897842333',
    '559185536953',
    '559193690751',
    '559284270330',
    '559284920602',
    '559284950529',
    '559292057409',
    '559292786066',
    '559491324024',
    '559492469167',
    '559884757436',
    '559885776074',
    '559888023928',
    '559888935620',
    '559891171936',
    '559892032455',
    '559899856119',
    '559981034876',
    '559981202799',
    '559984105415',
    '559984462462',
    '559984519119',
    '559984986309',
    '559991319506',
    '5511917069843',
    '5511966534233',
    '5511990172401',
    '5512982473289',
    '5512988312478',
    '5512988886336',
    '5512991859080',
    '5512997429378',
    '5513982185731',
    '5514991449444',
    '5514996404048',
    '5514997132107',
    '5516992282596',
    '5516992516146',
    '5516992570068',
    '5516996237428',
    '5517992095437',
    '5517996444783',
    '5517997071951',
    '5519981832496',
    '5519988122861',
    '5519988810613',
    '5519994389787',
    '5519997327148',
    '5521972593619',
    '5521975565882',
    '5521979718000',
    '5521991352821',
    '5521991994042',
    '5521992769964',
    '5521994109000',
    '5521997821275',
    '5521999395274',
    '5522998529807',
    '5522999687668',
    '5524999296686',
    '5527988398058',
    '5527997395230',
    '5527998601705',
    '5528999195723',
    '5528999939650',
    '5535888963912'    
]

def update_no_logo():
    collection = db['clients']
    no_client = []
    for client in no_logo:
        client_data = collection.find_one({"client": client})
        if client_data is not None:    
            if client_data['has_logo'] == False:
                print(client, 'já está atualizado')
                continue
                    
            collection.update_one(
                {"client": client},
                {"$set": {"has_logo": False}},
            )
            print(client, 'atualizado com variavel logo')
        else:
            no_client.append(client)
    
    #save no logo clients in txt
    with open('no_logo_clients.txt', 'w') as f:
        for client in no_client:
            f.write(f'{client}\n')

def update_logos():
    collection = db['clients']
    clients = collection.find()
    for client in clients:
            try:
                print(client['client'])
                if client['has_logo']:
                    continue
                
                collection.update_one(
                    {"client": client['client']},
                    {"$set": {"has_logo": True}},
                )
                print(client, 'atualizado com variavel logo')
                
            except:
                collection.update_one(
                        {"client": client['client']},
                        {"$set": {"has_logo": True}},
                    )
                print(client['client'], 'atualizado com variavel logo')
                
    print('Desenvolvedores atualizados')

def update_dev_info(db):
    print('Atualizando lista de desenvolvedores...')
    collection = db['clients']
    clients = collection.find()
    for client in clients:
        if client.get('is_dev') is not None:
            if client['client'] not in dev_phones:
                continue

        is_dev = False

        if client['client'] in dev_phones:
            is_dev = True

        client_phone = client['client']
        collection.update_one(
            {"client": client_phone},
            {"$set": {"is_dev": is_dev}},
        )

def update_clients(db, templates):
    print('Atualizando templates de clientes...')
    collection = db['clients']
    collection.update_many({
        'niche': 'hortifruti'}, {
        '$set': {'templates': templates}
        })
    print('Templates de clientes atualizados')

def update_purcharse_info(db):
    print('Atualizando informação de compra...')
    client_collection = db['clients']
    purcharse_colection = db['cta_not_purchased']

    purcharse = purcharse_colection.find()

    for item in purcharse:
        client = item['client']
        date = item['date']
        print(client, date)

        current_client = client_collection.find({"client": client})
        current_date = current_client[0].get('purchase',{}).get('free_trial_started_date', None)
        if current_date is None:
            print('Não existe free trial, adicionando informação...')
            client_collection.update_one(
                {"client": client},
                {"$set": {"purchase.free_trial_started_date": date}}
            )

        elif current_date < date:
            print('Atualizando informação...')
            client_collection.update_one(
                {"client": client},
                {"$set": {"purchase.free_trial_started_date": date}}
            )


templates = [
    "Hortifruti - Benefícios",
    "Hortifruti - Carrossel dica de receita 1",
    "Hortifruti - Carrossel dica de receita 2",
    "Hortifruti - Carrossel dica de receita 3",
    "Hortifruti - Dica de receita",
    "Hortifruti - Dica do dia",
    "Hortifruti - Encarte ofertas 1",
    "Hortifruti - Encarte ofertas 2",
    "Hortifruti - Encarte ofertas 3",
    "Hortifruti - Encarte ofertas 4",
    "Hortifruti - Encarte ofertas 5",
    "Hortifruti - Encarte ofertas 6",
    "Hortifruti - Encarte ofertas da semana 1",
    "Hortifruti - Encarte ofertas da semana 2",
    "Hortifruti - Encarte ofertas da semana 3",
    "Hortifruti - Encarte ofertas de verão",
    "Hortifruti - Encarte ofertas do dia 1",
    "Hortifruti - Encarte ofertas do dia 2",
    "Hortifruti - Encarte super ofertas",
    "Hortifruti - Estabelecimento",
    "Hortifruti - Oferta do dia",
    "Hortifruti - Preço 1",
    "Hortifruti - Preço 2",
    "Hortifruti - Preço 3",
    "Hortifruti - Preço 4",
    "Hortifruti - Rico em vitamina",
    "Hortifruti - Vídeo Preço 1",
    "Hortifruti - Vídeo Preço 2",
    "Hortifruti - Vídeo Preço 3",
]

if __name__ == '__main__':
    update_purcharse_info(db)
    # update_dev_info(db)
    # update_no_logo()
    # update_clients(db, templates)