from pathlib import Path
import google_drive_api

abs_path = Path(__file__).parent.parent
json_path = abs_path / 'videoai.analytics.json'

def upload_json(json_path):
    drive = google_drive_api.auth_drive()
    google_json_folder_id = '1WUNM-yF2zgDwDCKe-qX5Wl8lI-cC0A71'
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

if __name__ == '__main__':
    upload_json(json_path)