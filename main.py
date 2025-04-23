from ultralytics import YOLO
import cv2
import math 
import pyfirmata
import time

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# model
model = YOLO("models/best.pt")

print(model.names)
classNames = []
temp = {0: 'Aluminium foil', 1: 'Battery', 2: 'Aluminium blister pack', 3: 'Carded blister pack', 4: 'Other plastic bottle', 5: 'Clear plastic bottle', 6: 'Glass bottle', 7: 'Plastic bottle cap', 8: 'Metal bottle cap', 9: 'Broken glass', 10: 'Food Can', 11: 'Aerosol', 12: 'Drink can', 13: 'Toilet tube', 14: 'Other carton', 15: 'Egg carton', 16: 'Drink carton', 17: 'Corrugated carton', 18: 'Meal carton', 19: 'Pizza box', 20: 'Paper cup', 21: 'Disposable plastic cup', 22: 'Foam cup', 23: 'Glass cup', 24: 'Other plastic cup', 25: 'Food waste', 26: 'Glass jar', 27: 'Plastic lid', 28: 'Metal lid', 29: 'Other plastic', 30: 'Magazine paper', 31: 'Tissues', 32: 'Wrapping paper', 33: 'Normal paper', 34: 'Paper bag', 35: 'Plastified paper bag', 36: 'Plastic film', 37: 'Six pack rings', 38: 'Garbage bag', 39: 'Other plastic wrapper', 40: 'Single-use carrier bag', 41: 'Polypropylene bag', 42: 'Crisp packet', 43: 'Spread tub', 44: 'Tupperware', 45: 'Disposable food container', 46: 'Foam food container', 47: 'Other plastic container', 48: 'Plastic glooves', 49: 'Plastic utensils', 50: 'Pop tab', 51: 'Rope & strings', 52: 'Scrap metal', 53: 'Shoe', 54: 'Squeezable tube', 55: 'Plastic straw', 56: 'Paper straw', 57: 'Styrofoam piece', 58: 'Unlabeled litter', 59: 'Cigarette'}
for object in temp:
    classNames.append(temp[object])

# object classes
# may need to add cans here
# classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
#               "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
#               "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
#               "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
#               "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
#               "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
#               "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
#               "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
#               "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
#               "teddy bear", "hair drier", "toothbrush"
#               ]
global pin9
    
board=pyfirmata.Arduino('/dev/ttyUSB0')

iter8 = pyfirmata.util.Iterator(board)
iter8.start()

pin9 = board.get_pin('d:9:s')

def move_servo(angle):
    pin9.write(angle)

move_servo(90)

while True:
    success, img = cap.read()
   # prediction = model.predict(img, imgsz=img.size, show=True, save=False)

    results = model(img, stream=True)

    # coordinates
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->",confidence)

            # class name
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])


            # if the object name is lets say drink carton, move servo to left
            if classNames[cls] == "Meal carton" or classNames[cls] == "Crisp packet":
                move_servo(160)
                time.sleep(2)
                move_servo(90)

            
            elif classNames[cls] == "Paper cup":
                move_servo(20)
                time.sleep(2)
                move_servo(90)

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()