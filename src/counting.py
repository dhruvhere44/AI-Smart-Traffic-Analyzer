COUNT_LINE_Y = 650

counted_ids = set()

total_cars = 0
total_bikes = 0
total_buses = 0
total_trucks = 0


def process_count(track_id, class_name, center_y):

    global total_cars
    global total_bikes
    global total_buses
    global total_trucks

    if center_y > COUNT_LINE_Y:

        if track_id not in counted_ids:

            counted_ids.add(track_id)

            if class_name == "car":
                total_cars += 1

            elif class_name == "motorcycle":
                total_bikes += 1

            elif class_name == "bus":
                total_buses += 1

            elif class_name == "truck":
                total_trucks += 1


def get_counts():

    return (
        total_cars,
        total_bikes,
        total_buses,
        total_trucks
    )