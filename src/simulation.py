import math
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
        self.y = self.body.radius #TODO: we need to make it so there is height() to calc height based on x and y
        self.speed_x = 0
        self.speed_y = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

        self.heading = 0

    #simulation logic
    def tick(self, delta: int) -> None:
        current_stage = self.rocket.current_stage()
        #calculate upwards force by fuel       
        fuel_used = current_stage.total_fuel_used(delta)
        if current_stage.fuel_mass < fuel_used:
            fuel_used = current_stage.fuel_mass
        current_stage.fuel_mass -= fuel_used
        print("Fuel remaining: " + str(current_stage.fuel_mass))

        g = self.body.g(G=self.universe.G, height=self.rocket_altitude())
        print("g: " + str(g))
                
        force_x = 0
        force_y = 0
        if fuel_used > 0:
            total_thrust = current_stage.current_thrust(g, self.heading)
            force_x = total_thrust[0]
            force_y = total_thrust[1]
        
        print("Thrust X: " + str(force_x))
        print("Thrust Y: " + str(force_y))

        print("BODY MASS: " + str(self.body.mass()))
        print("ROCKET TOTAL MASS: " + str(self.rocket.total_mass()))

        #calculate downwards force by drag and gravity
        gravitational_force_y = g * self.rocket.total_mass()
        print("Gravity Y: " + str(gravitational_force_y))

        #Remove gravity from force
        force_y -= gravitational_force_y

        curr_atmospheric_density = self.body.atmosphere.density_at_height(self.rocket_altitude(), g)
        print("Atmosphere density: " + str(curr_atmospheric_density))

        #TODO: cross sectional area and drag coef for x should b different
        drag_force_x = (1/2) * curr_atmospheric_density * (self.speed_x ** 2) * self.rocket.rocket_x_drag_coefficient() * self.rocket.rocket_x_cross_sectional_area()
        #drag goes against speed
        if force_x < 0:
            drag_force_x *= -1
        print("Drag X: " + str(drag_force_x))

        #https://www.grc.nasa.gov/www/k-12/airplane/drageq.html
        drag_force_y = (1/2) * curr_atmospheric_density * (self.speed_y ** 2) * self.rocket.rocket_y_drag_coefficient() * self.rocket.rocket_y_cross_sectional_area()
        #drag goes against speed
        if force_y < 0:
            drag_force_y *= -1
        print("Drag Y: " + str(drag_force_y))

        #remove drag
        force_x -= drag_force_x
        force_y -= drag_force_y

        print("Total Force X: " + str(force_x))
        print("Total Force Y: " + str(force_y))

        self.acceleration_x = force_x / self.rocket.total_mass()
        self.acceleration_y = force_y / self.rocket.total_mass()
        print("Acceleration x: " + str(self.acceleration_x))
        print("Acceleration y: " + str(self.acceleration_y))
        
        self.speed_x = self.speed_x + (self.acceleration_x * delta)
        self.speed_y = self.speed_y + (self.acceleration_y * delta)

        print("Speed x: " + str(self.speed_x))
        print("Speed y: " + str(self.speed_y))

        #TODO: WELL CALCULATED? (angle well?)
        ref_vec = (0, 1)
        acc_vec = (self.speed_x, self.speed_y)
        dot = (acc_vec[0] * ref_vec[0]) + (acc_vec[1] * ref_vec[1])
        det = (acc_vec[0] * ref_vec[1]) - (acc_vec[1] * ref_vec[0])
        self.heading = math.degrees(math.atan2(det, dot))
        print("Heading: " + str(self.heading))
        
        #update position based on velocity and delta
        self.x += self.speed_x * delta
        self.y += self.speed_y * delta
        if self.rocket_altitude() < 0:
            #undo positional changes
            self.x -= self.speed_x * delta
            self.y -= self.speed_y * delta
            self.speed_x = 0
            self.speed_y = 0
            
        print("X: " + str(self.x))
        print("Y: " + str(self.y))

        print("Total Simulation Time: " + str(self.time))
        print("")

        self.ticks += 1
        self.time += delta

    def rocket_altitude(self):
        #take into account body and allow for 360 height
        altitude = math.sqrt(self.x**2 + self.y**2)
        altitude -= self.body.radius
        return altitude 

    def snapshot(self) -> Simulation_Snapshot:
        return Simulation_Snapshot(self.universe, self.body, self.rocket)

    def str_snapshot(self) -> str:
        return str(self.universe) + "\n" + \
               str(self.body) + "\n" + \
               str(self.rocket)