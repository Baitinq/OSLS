import fuel

class Engine():
    def __init__(self, name: str, isp: int, max_flow_rate: int):
        self.name = name
        self.max_flow_rate = max_flow_rate
        self.isp = isp

    def thrust(self, throttle: int):
        return self.flow_rate(throttle) * self.isp

    def flow_rate(self, throttle: int):
        return self.max_flow_rate * (throttle / 100)