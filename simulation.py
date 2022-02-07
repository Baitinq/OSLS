from dataclasses import dataclass

from universe import Universe
from body import Body
from rocket import Rocket

@dataclass
class Simulation_Snapshot:
    universe: type[Universe]
    body: type[Body]
    rocket: type[Rocket]

class Simulation():
    def __init__(self, universe: type[Universe], body: type[Body], rocket: type[Rocket]):
        self.ticks = 0
        self.time = 0
        self.universe = universe
        self.body = body
        self.rocket = rocket
        self.y = 0
        self.speed_y = 0
        self.acceleration_y = 0

    #simulation logic
    def tick(self, delta: int) -> None:
        #calculate upwards force by fuel       
        # TODO able to turn engine on and off 
        fuel_used = self.rocket.total_fuel_used(delta)
        if self.rocket.fuel_mass < fuel_used:
            fuel_used = self.rocket.fuel_mass
        self.rocket.fuel_mass -= fuel_used
        print("Fuel remaining: " + str(self.rocket.fuel_mass))
        
        #upwards_force = fuel_used * self.rocket.fuel_type.energy_density #we should calculate thrust based on this
        upwards_force = 0
        if fuel_used > 0:
            upwards_force = self.rocket.total_thrust()
        print("Upwards force: " + str(upwards_force))

        print("g: " + str(self.body.g(G=self.universe.G, height=self.y)))

        #calculate downwards force by drag and gravity
        gravitational_force = self.body.g(G=self.universe.G, height=self.y) * self.rocket.total_mass()
        print("Gravity: " + str(gravitational_force))

        print("BODY MASS: " + str(self.body.mass()))
        print("ROCKET TOTAL MASS: " + str(self.rocket.total_mass()))

        print("Atmosphere density: " + str(self.body.atmosphere.density_at_height(self.y, self.body.g(G=self.universe.G, height=self.y))))

        #https://www.grc.nasa.gov/www/k-12/airplane/drageq.html
        drag_force = (1/2) * self.body.atmosphere.density_at_height(self.y, self.body.g(G=self.universe.G, height=self.y)) * (self.speed_y ** 2) * self.rocket.drag_coefficient * self.rocket.cross_sectional_area
        print("Drag: " + str(drag_force)) #drag can be negative too?

        downwards_force = gravitational_force + drag_force #shouldnt delta influence, TODO: WAIT DRAG COULD BE POSITIVE OR NEGATIVE
        print("Downwards force: " + str(downwards_force))

        #update velocity based on resultant force
        total_force = upwards_force - downwards_force
        print("Total force: " + str(total_force))

        self.acceleration_y = total_force / self.rocket.total_mass() #mayb we need momentum??
        print("Acceleration: " + str(self.acceleration_y))
        self.speed_y = self.speed_y + (self.acceleration_y * delta) #i think thir swrong

        #update position based on velocity and delta
        self.y += self.speed_y * delta
        if self.y < 0:
            self.y = 0
            self.speed_y = 0
            
        print("Speed: " + str(self.speed_y))
        print("Height: " + str(self.y))

        print("Total Simulation Time: " + str(self.time))
        print("")

        self.ticks += 1
        self.time += delta

    def snapshot(self) -> Simulation_Snapshot:
        return Simulation_Snapshot(self.universe, self.body, self.rocket)

    def str_snapshot(self) -> str:
        return str(self.universe) + "\n" + \
               str(self.body) + "\n" + \
               str(self.rocket)