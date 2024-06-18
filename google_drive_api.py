from pathlib import Path
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

abs_path = Path(__file__).parent.parent
google_creds = abs_path / 'Scripts' / 'google_drive_creds.json'
client_secrets = abs_path / 'Scripts' / 'client_secrets.json'

def auth_drive():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(str(client_secrets))

    gauth.LoadCredentialsFile(str(google_creds))

    if not gauth.credentials:
        # Se não houver credenciais ou se estiverem expiradas, autentique via navegador
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile(str(google_creds))
    elif gauth.access_token_expired:
        # Se o token de acesso estiver expirado, atualize-o
        gauth.Refresh()
        gauth.SaveCredentialsFile(str(google_creds))
    else:
        # Caso contrário, autorize com as credenciais carregadas
        gauth.Authorize()

    gauth.SaveCredentialsFile(google_creds)
    drive = GoogleDrive(gauth)

    return drive, gauth.credentials