import fuel

class Engine():
    def __init__(self, name: str, thrust: int, flow_rate: float):
        self.name = name
        self.thrust = thrust
        self.flow_rate = flow_rate