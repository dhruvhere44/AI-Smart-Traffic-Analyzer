from ultralytics import YOLO

# Load YOLOv11 model
model = YOLO("models/yolo11n.pt")

# Vehicle classes from COCO dataset
VEHICLE_CLASSES = {
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}


def detect_vehicles(frame):
    """
    Detect vehicles in a frame
    Returns YOLO results
    """

    results = model(frame, verbose=False)

    return results