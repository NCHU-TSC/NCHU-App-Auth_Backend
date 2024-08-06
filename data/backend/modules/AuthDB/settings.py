import os

host = os.getenv('AUTHDB_HOSTNAME')
port = int(os.getenv('AUTHDB_PORT'))
user = os.getenv('AUTHDB_USERNAME')
password = os.getenv('AUTHDB_PASSWORD')
db_name = os.getenv('AUTHDB_DATABASE')

states_file = os.path.dirname(__file__) + "/states.json"
default_client_id = "31ad0231-d981-11ee-be58-74563c0a381d"

domain_protocol = 'https'
domain_name = 'auth.' + os.getenv('MAIN_DOMAIN') # 'auth.nchu.app'

api_domain_name = 'api.' + domain_name # 'api.auth.nchu.app'

def get_domain_url() -> str:
    return f'{domain_protocol}://{domain_name}'

def get_api_domain_url() -> str:
    return f'{domain_protocol}://{api_domain_name}'

def belongs_to_domain(url: str) -> bool:
    return domain_name in url[0: len(domain_name) + 12]