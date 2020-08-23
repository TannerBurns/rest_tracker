from modutils import BaseSession

class ES_Session(BaseSession):

    def __init__(self, host:str='elasticsearch', port:str='9200'):
        super().__init__()
        self.host = host
        self.port = port
        self.base_url = f'http://{host}:{port}'
        self.initialized = True if self.get(self.base_url).status_code == 200 else False
        self.index_created = False

    def set_host(self, host:str):
        self.host = host
        self.base_url = f'http://{host}:{self.port}'
        self.initialized = True if self.get(self.base_url).status_code == 200 else False

    def set_port(self, port: str):
        self.port = port
        self.base_url = f'http://{self.host}:{port}'
        self.initialized = True if self.get(self.base_url).status_code == 200 else False

    def create_index(self, index: str, mapping: dict):
        return self.put(f'{self.base_url}/{index}', json=mapping)

    def add_content(self, index:str, content: dict):
        return self.post(f'{self.base_url}/{index}/_doc', json=content)


ELASTIC_SESSION = ES_Session()