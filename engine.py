import fuel

class Engine():
    def __init__(self, name: str, isp: int, max_flow_rate: int):
        self.name = name
        self.max_flow_rate = max_flow_rate
        self.isp = isp

    def thrust(self, throttle: int, g: float):
        #https://www.grc.nasa.gov/www/k-12/airplane/specimp.html
        return self.flow_rate(throttle) * self.isp * g

    def flow_rate(self, throttle: int):
        return self.max_flow_rate * (throttle / 100)