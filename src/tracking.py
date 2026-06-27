from ultralytics import YOLO

model = YOLO("../models/yolo11s.pt")

def track_vehicles(frame):
    
    results = model.track(
        frame,
        persist=True,
        tracker="botsort.yaml",
        classes=[2,3,5,7],
        conf=0.20,
        imgsz=1280,
        verbose=False
    )

    return results