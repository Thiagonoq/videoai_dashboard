from dotenv import load_dotenv
from pathlib import Path
import os

abs_path = Path(__file__).parent.parent
script_path = abs_path / 'Scripts'

load_dotenv(f'{script_path}\\.env', override=True)

uri = os.getenv('MONGODB_URI')

analytics_json_path = "videoai.analytics.json"
new_analytics_json_path = "new_analytics.json"
list_json_path = "new_list.json"
clients_json_path = "videoai.clients.json"


