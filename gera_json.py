import random
import json
from datetime import datetime, timedelta

# Configurações iniciais
quantidade_entradas = 100  # Você pode ajustar esse valor conforme necessário
nomes_templates = ["Hortifruti - Benefícios",
                   "Hortifruti - Dica de receita",
                   "Hortifruti - Dica do dia",
                   "Hortifruti - Estabelecimento",
                   "Hortifruti - Oferta do dia",
                   "Hortifruti - Preço 1",
                   "Hortifruti - Preço 2",
                   "Hortifruti - Preço 3",
                   "Hortifruti - Preço 4",
                   "Hortifruti - Rico em vitamina"
                   ]

def gerar_id_aleatorio():
    return ''.join(random.choices('abcdef0123456789', k=24))

def gerar_data_aleatoria(inicio, fim):
    delta = fim - inicio
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return inicio + timedelta(seconds=random_second)

def gerar_flows(quantidade):
    inicio = datetime.now() - timedelta(days=30)
    fim = datetime.now()
    flows = []
    for _ in range(quantidade):
        start = gerar_data_aleatoria(inicio, fim)
        end = start + timedelta(seconds=random.randint(60, 120))
        flows.append({
            "started": {"$date": start.isoformat() + "Z"},
            "ended": {"$date": end.isoformat() + "Z"}
        })
    return flows

def gerar_gpt_usage():
    usage_models = [
        {
            "name": "whisper-1",
            "seconds": round(random.uniform(0.5, 15.0), 3),
            "expense": round(random.uniform(0.0001, 0.01), 10)
        },
        {
            "name": "gpt-3.5-turbo-1106",
            "completionTokens": random.randint(100, 500),
            "promptTokens": random.randint(500, 6000),
            "expense": round(random.uniform(0.001, 0.01), 12)
        },
        {
            "name": "gpt-4-1106-preview",
            "completionTokens": random.randint(50, 150),
            "promptTokens": random.randint(100, 400),
            "expense": round(random.uniform(0.001, 0.005), 16)
        }
    ]
    return random.sample(usage_models, 3)  # Retorna uma amostra de todos os 3 modelos


def gerar_template(name):
    success_created = random.randint(3, 10)
    failed_created = random.randint(0, 2)
    cancelled_created = random.randint(0, 3)
    success_edited = random.randint(1, 6)
    failed_edited = random.randint(0, 2)
    cancelled_edited = random.randint(0, 3)

    total_success = success_created + failed_created + cancelled_created + success_edited + failed_edited + cancelled_edited

    flows = gerar_flows(total_success)
    usage_created = {"failed": failed_created, "success": success_created, "cancelled": cancelled_created}
    usage_edited = {"failed": failed_edited, "success": success_edited, "cancelled": cancelled_edited}
    template = {
        "name": name,
        "published": random.randint(0, 2),
        "requestedCatalog": random.randint(0, 1),
        "sended": {"text": random.randint(0, 10), "audio": random.randint(0, 5), "image": random.randint(0, 5)},
        "usage": {"created": usage_created, "edited": usage_edited},
        "gpt": {"usage": gerar_gpt_usage()},
        "flows": flows
    }
    return template

def gerar_templates():
    num_templates = random.randint(3, len(nomes_templates))
    nomes_escolhidos = random.sample(nomes_templates, num_templates)
    templates = [gerar_template(name) for name in nomes_escolhidos]
    return templates

def gerar_entradas(quantidade):
    entradas = []
    for _ in range(quantidade):
        
        data = {
            "_id": {"$oid": gerar_id_aleatorio()},
            "id": gerar_id_aleatorio(),
            "client": f"55{str(random.randint(10000000000, 99999999999))}",
            "templates": gerar_templates(),
            "created_at": {"$date": datetime.now().isoformat() + "Z"},
            "updated_at": {"$date": datetime.now().isoformat() + "Z"}
        }
        entradas.append(data)
    return json.dumps(entradas, indent=4, ensure_ascii=False)

# Gerar o JSON com a quantidade especificada de entradas
json_saida = gerar_entradas(quantidade_entradas)

# Escrever o JSON no arquivo
with open("output.json", "w", encoding="utf-8") as file:
    file.write(json_saida)
    print("Arquivo gerado com sucesso!")
