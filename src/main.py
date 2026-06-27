import cv2

from tracking import track_vehicles
from counting import *
from density import *
from occupancy import *
from report import generate_report

VIDEO_PATH = "../videos/traffic.mp4"

cap = cv2.VideoCapture(VIDEO_PATH)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

out = cv2.VideoWriter(
    "../output/traffic_output.mp4",
    fourcc,
    20.0,
    (
        int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    )
)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    results = track_vehicles(frame)

    annotated = frame.copy()

    cv2.line(
        annotated,
        (0, COUNT_LINE_Y),
        (annotated.shape[1], COUNT_LINE_Y),
        (0, 255, 255),
        3
    )

    if results[0].boxes.id is not None:

        boxes = results[0].boxes

        ids = boxes.id.cpu().numpy()

        classes = boxes.cls.cpu().numpy()

        coords = boxes.xyxy.cpu().numpy()

        vehicle_area = 0

        for box, track_id, cls in zip(coords, ids, classes):

            x1, y1, x2, y2 = map(int, box)
            width = x2 - x1
            height = y2 - y1
            vehicle_area += width * height

            center_y = int((y1 + y2) / 2)

            track_id = int(track_id)

            cls = int(cls)

            class_names = {
                2: "car",
                3: "motorcycle",
                5: "bus",
                7: "truck"
            }

            if cls in class_names:

                class_name = class_names[cls]
                print(class_name)

                process_count(
                    track_id,
                    class_name,
                    center_y
                )

                cv2.rectangle(
                    annotated,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    annotated,
                    f"{class_name} ID:{track_id}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0,255,0),
                    2
                )
    current_visible_vehicles = len(ids)
    cars, bikes, buses, trucks = get_counts()
    density = calculate_density(current_visible_vehicles)
    congestion = classify_congestion(density)
    occupancy = calculate_occupancy(vehicle_area)

    if occupancy > 70:
        traffic_alert_active = "SEVERE CONGESTION"

    elif occupancy > 50:
        traffic_alert_active = "MODERATE TRAFFIC"

    else:
        traffic_alert_active = None

    cv2.putText(
        annotated,
        f"Cars: {cars}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    cv2.putText(
        annotated,
        f"Bikes: {bikes}",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    cv2.putText(
        annotated,
        f"Buses: {buses}",
        (20,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    cv2.putText(
        annotated,
        f"Trucks: {trucks}",
        (20,160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )
    cv2.putText(
        annotated,
        f"Density: {density}%",
        (20,210),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,255),
        2
    )
    
    cv2.putText(
        annotated,
        f"Occupancy: {occupancy}%",
        (20,290),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,255,0),
        2
    )
    if traffic_alert_active=="SEVERE CONGESTION":
        cv2.rectangle(
            annotated,
            (20, 330),
            (850, 410),
            (0, 0, 255),
            -1
        )

        cv2.putText(
            annotated,
            "TRAFFIC ALERT: SEVERE CONGESTION",
            (40, 380),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255,255,255),
            3
        )
    elif traffic_alert_active =="MODERATE TRAFFIC":
        cv2.rectangle(
            annotated,
            (20,330),
            (750,410),
            (0,255,255),
            -1
        )
        cv2.putText(
            annotated,
            "TRAFFIC ALERT: MODERATE TRAFFIC",
            (40,380),
            cv2.FONT_HERSHEY_COMPLEX,
            1,
            (0,0,0),
            3
        )
    cv2.putText(
        annotated,
        f"Traffic: {congestion}",
        (20,250),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,0,255),
        2
    ) 

    out.write(annotated)
    cv2.imshow("Traffic Counting", annotated)

    if cv2.waitKey(1) == 27:
        break
    cars, bikes, buses, trucks = get_counts()

generate_report(
    cars,
    bikes,
    buses,
    trucks,
    density,
    occupancy,
    congestion
)
out.release()
cap.release()
cv2.destroyAllWindows()