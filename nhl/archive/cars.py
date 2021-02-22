from collections import namedtuple

class StoreCar:
   def __init__(self, id_,name):
       self.id_ = id_
       self.name= name
       self.fc_list= []

   # If you're *setting* the fuel capacity, it shouldn't be a list.
   # (assuming that's what FC stands for)
   def add_fuel(self, fuel):
       self.fc_list.append(fuel)

class Machine:
   def __init__(self):
       self.cars = []
       # Assuming that the vehicle ID shouldn't 
       # be public knowledge. It can still be got
       # from outside the class, but it's more difficult now
       self.__vehicle_id = 0

   def calculation(self):
        self.__vehicle_id += 1
        fuel = 15 # this is also calculated automatically from system.
        car = cars.StoreCar(self.__vehicle_id, 'car')
        # Typically, I'd actually have `fuel` as a parameter
        # for the constructor, i.e.
        #    cars.StoreCar(self.__vehicle_id, 'car', fuel)
        car.add_fuel(fuel)
        self.cars.append(car)


# Note, that if I were unconstrained by any kind of assignment, I would probably just do something like this:


Car = namedtuple('Car', ('id', 'fuel_capacity', 'name'))


def gen_vehicle_ids():
    id = 0
    while True:
        id += 1
        yield id

vehicle_id = gen_vehicle_ids()


def build_car():
    return Car(id=next(vehicle_id), name='car', fuel_capacity=15)
    # If you don't want a namedtuple, you *could* just
    # use a dict instead
    return {'id': next(vehicle_id), 'type': 'car', 'fuel_capacity': 15}

cars = []
for _ in range(20): # build 20 cars
    cars.append(build_car())

# an alternative approach, use a list comprehension
cars = [build_car() for _ in range(20)]

print(cars)   # or do whatever you want with them.
# For a comparison between what you can do with the namedtuple approach vs. dict approach:

# dict approach
# for car in cars:
#     print('Car(id={}, name={}, fuel_capacity={})'.format(
#           car['id'], car['name'], car['fuel_capacity']))

# namedtuple approach
for car in cars:
    print('Car(id={}, name={}, fuel_capacity{})'.format(
          car.id, car.name, car.fuel_capacity))