import glob
import os
import sys
import time
import math
import threading

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla


def get_actor_display_name(actor):
    name = ' '.join(actor.type_id.replace('_', '.').title().split('.')[1:])
    return name


actor_list = []

def number_of_vehicle():
    all_vehicles = world.get_actors().filter('vehicle.*')
    threading.Timer(0.1, number_of_vehicle).start()
    transform_location = dropped_vehicle.get_transform()

    if len(all_vehicles) > 1:
        distance = lambda data: math.sqrt(
            (data.x - transform_location.location.x) ** 2 + (data.y - transform_location.location.y) ** 2 + (
                        data.z - transform_location.location.z) ** 2)

        get_distance_of_bot_vehicles = []
        for each_car in all_vehicles:
            if each_car.id != world.id:
                get_distance_of_bot_vehicles.append((distance(each_car.get_location()), each_car))

        vehicle_data = {}
        final_vehicle_result = []

        sorted_vehicles = sorted(get_distance_of_bot_vehicles)

        #start coding from here

        if distance_in_meter['distance'] > 10 and distance_in_meter['distance'] < 15:
        	dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.2))
        	time.sleep(3)
        	dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.2,steer=-0.2))
        	time.sleep(2)
        	dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.2,steer=0.1))
        	time.sleep(2)
        	dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.2))
        	time.sleep(3)
        	print(distance_in_meter['vehicle_name'])

def car_control():
    dropped_vehicle.apply_control(carla.VehicleControl(throttle=0.5))
    time.sleep(10)

try:
    client = carla.Client('127.0.0.1', 2000)
    client.set_timeout(10.0)
    world = client.get_world()

    get_blueprint_of_world = world.get_blueprint_library()
    car_model = get_blueprint_of_world.filter('model3')[0]
    spawn_point = (world.get_map().get_spawn_points()[1])
    dropped_vehicle = world.spawn_actor(car_model, spawn_point)
    simulator_camera_location_rotation = carla.Transform(spawn_point.location, spawn_point.rotation)
    simulator_camera_location_rotation.location += spawn_point.get_forward_vector() * 30
    simulator_camera_location_rotation.rotation.yaw += 180
    simulator_camera_view = world.get_spectator()
    simulator_camera_view.set_transform(simulator_camera_location_rotation)
    actor_list.append(dropped_vehicle)

    collision_sensor = get_blueprint_of_world.find('sensor.other.collision')
    sensor_collision_spawn_point = carla.Transform(carla.Location(x=2.5, z=0.7))
    sensor = world.spawn_actor(collision_sensor, sensor_collision_spawn_point, attach_to=dropped_vehicle)

    sensor.listen(lambda data: _on_collision(data))

    actor_list.append(sensor)


    def _on_collision(data):
        print("Collision is there")
        actor_type = get_actor_display_name(data.other_actor)
        print("Collision with", actor_type)
        Collision_event_record = data.normal_impulse
        intensity_of_collision = math.sqrt(
            Collision_event_record.x ** 2 + Collision_event_record.y ** 2 + Collision_event_record.z ** 2)
        print("Intensity of collision", intensity_of_collision)
        dropped_vehicle.apply_control(carla.VehicleControl(hand_brake=True))
        time.sleep(5)


    number_of_vehicle()
    car_control()
    time.sleep(1000)
finally:
    print('destroying actors')
    for actor in actor_list:
        actor.destroy()
    print('done.')
