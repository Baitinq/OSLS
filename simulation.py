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
        self.x = 0#TODO
        self.y = 0 #TODO: we need to make it so there is height() to calc height based on x and y
        self.speed_x = 0#TODO
        self.speed_y = 0
        self.acceleration_x = 0#TODO
        self.acceleration_y = 0

    #simulation logic
    def tick(self, delta: int) -> None:
        current_stage = self.rocket.current_stage()
        #calculate upwards force by fuel       
        fuel_used = current_stage.total_fuel_used(delta)
        if current_stage.fuel_mass < fuel_used:
            fuel_used = current_stage.fuel_mass
        current_stage.fuel_mass -= fuel_used
        print("Fuel remaining: " + str(current_stage.fuel_mass))
        
        #TODO: FORCE_X AND FORCE_Y
        
        force_x = 0
        force_y = 0
        if fuel_used > 0:
            total_thrust = current_stage.current_thrust(self.body.g(self.universe.G, self.y))
            force_x = total_thrust[0]
            force_y = total_thrust[1]
        
        print("Thrust X: " + str(force_x))
        print("Thrust Y: " + str(force_y))

        #print("Y THRUST: " + str(upwards_force))
        #print("TOTAL THRUST: " + str(current_stage.convert_y_component_to_total_with_gimbal(upwards_force)))

        print("BODY MASS: " + str(self.body.mass()))
        print("ROCKET TOTAL MASS: " + str(self.rocket.total_mass()))

        #calculate downwards force by drag and gravity
        print("g: " + str(self.body.g(G=self.universe.G, height=self.y)))

        gravitational_force = self.body.g(G=self.universe.G, height=self.y) * self.rocket.total_mass()
        print("Gravity: " + str(gravitational_force))

        #Remove gravity from force
        force_y -= gravitational_force

        print("Atmosphere density: " + str(self.body.atmosphere.density_at_height(self.y, self.body.g(G=self.universe.G, height=self.y))))

        #TODO: cross sectional area and drag coef for x should b different
        drag_force_x = (1/2) * self.body.atmosphere.density_at_height(self.y, self.body.g(G=self.universe.G, height=self.y)) * (self.speed_x ** 2) * self.rocket.s_drag_coefficient() * self.rocket.s_cross_sectional_area()
        #drag goes against speed
        if force_x < 0:
            drag_force_x *= -1
        print("Drag X: " + str(drag_force_x))

        #https://www.grc.nasa.gov/www/k-12/airplane/drageq.html
        drag_force_y = (1/2) * self.body.atmosphere.density_at_height(self.y, self.body.g(G=self.universe.G, height=self.y)) * (self.speed_y ** 2) * self.rocket.s_drag_coefficient() * self.rocket.s_cross_sectional_area()
        #drag goes against speed
        if force_y < 0:
            drag_force_y *= -1
        print("Drag Y: " + str(drag_force_y))

        #remove drag
        force_x -= drag_force_x
        force_y -= drag_force_y

        print("Total Force X: " + str(force_x))
        print("Total Force Y: " + str(force_y))

        self.acceleration_y = force_y / self.rocket.total_mass() #mayb we need momentum??
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