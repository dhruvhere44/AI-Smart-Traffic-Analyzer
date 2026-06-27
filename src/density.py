MAX_CAPACITY = 100

def calculate_density(current_vehicles):

    density = (current_vehicles / MAX_CAPACITY) * 100

    density = min(density, 100)

    return round(density, 2)


def classify_congestion(density):

    if density < 25:
        return "LOW"

    elif density < 50:
        return "MEDIUM"

    elif density < 75:
        return "HIGH"

    else:
        return "SEVERE"