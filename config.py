from env_loading import load_env_variable

API_TOKEN = load_env_variable("API_TOKEN")
API_URL = f'https://api.telegram.org/bot{API_TOKEN}' + '/{method_name}'
CSV_MIME_TYPE = 'text/csv'
