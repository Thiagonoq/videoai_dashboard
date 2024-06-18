from pymongo import MongoClient
import config
from datetime import datetime

uri = config.uri

client = MongoClient(uri)
db = client['videoai']
collection = db['analytics']

gpt_prices = {
        "gpt-3.5-turbo-1106": {
            "completionTokens": 0.002,
            "promptTokens": 0.001
        },
        "gpt-3.5-turbo-0125": {
            "completionTokens": 0.0015,
            "promptTokens": 0.0005
        },
        "gpt-4-1106-preview": {
            "completionTokens": 0.03,
            "promptTokens": 0.01
        },
    }

def update_expenses():
    data = collection.find()

    for item in data:
        _id = item['_id']
        templates = item['templates']

        for temp_index, template in enumerate(templates):
            gpt_usage = template['gpt']['usage']

            for usage_index, usage in enumerate(gpt_usage):
                usage_model = usage['name']

                if usage_model not in gpt_prices:
                    continue

                completion_value = usage['completionTokens'] * gpt_prices[usage_model]['completionTokens'] / 1000
                prompt_value = usage['promptTokens'] * gpt_prices[usage_model]['promptTokens'] / 1000
                usage_expense = completion_value + prompt_value
                field_path = f'templates.{temp_index}.gpt.usage.{usage_index}.expense'

                collection.update_one(
                    {'_id': _id},
                    {'$set': {field_path: usage_expense}},
                )
                print(f'Gastos atualizados: {_id} - {field_path}')

def update_catalogue():
    analytics = collection.find()
    max_date = datetime(2024, 2, 27)

    for analytics_item in analytics:

        if analytics_item['created_at'] < max_date:
            templates = analytics_item['templates']

            for template in templates:
                if template['requestedCatalog'] == 0:
                    continue

                _id = analytics_item['_id']
                collection.update_one(
                    {'_id': _id},
                    {'$set': {'requestedCatalog': 0}},
                )


if __name__ == '__main__':
    update_expenses()
    # update_catalogue()