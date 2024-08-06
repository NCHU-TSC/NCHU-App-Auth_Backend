import json

class StatusCode:
    def __init__(self, info: dict | str = {}):
        self.namespace = None
        self.code = None
        self.description = None
        self.detail = None
        self.load_states_json(info) if isinstance(info, str) else self.load_states(info)

    def __str__(self):
        return "{}.{}: {}\r\n{}".format(self.namespace, self.code, self.description, self.detail)
    
    def setStatus(self, code: str, detail_args: tuple = ()):
        self.code = code
        self.description = self.states[code][0]
        self.detail = self.states[code][1].format(*detail_args)

    def toDictionary(self) -> dict[str, str]:
        return {"code": self.namespace + '.' + self.code, "description": self.description, "detail": self.detail}

    def toJSON(self) -> str:
        return json.dumps(self.toDictionary())

    def load_states(self, info: dict):
        self.namespace = info.get("namespace", "")
        self.states = info.get("states", {})

    def load_states_json(self, file: str):
        with open(file, 'r') as o:
            info = json.loads(o.read())
            self.namespace = info.get("namespace", "")
            self.states = info.get("states", {})

    def get_description(self, code: str):
        return self.states[code][0]
    
    def get_raw_detail(self, code: str):
        return self.states[code][1]
    
class StatusException(Exception):
    def __init__(self, status: StatusCode):
        self.status = status
        super().__init__(status) 
