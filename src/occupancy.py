ROAD_AREA = 800000

def calculate_occupancy(vehicle_area):

    occupancy = (vehicle_area / ROAD_AREA) * 100

    occupancy = min(occupancy, 100)

    return round(occupancy, 2)