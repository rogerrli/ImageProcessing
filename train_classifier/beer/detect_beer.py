import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=True, help="path to the input image")
ap.add_argument("-c", "--cascade", default="cascade.xml", help="path to beer detector haar cascade")
args = vars(ap.parse_args())

path = args["path"]

for i in range(2, 652):
    if i < 10:
        zeros = "000"
    elif i < 100:
        zeros = "00"
    elif i < 1000:
        zeros = "0"
    else:
        zeros = ""
    full_path = path + "not_beer" + zeros + str(i) + ".jpg"
    image = cv2.imread(full_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    detector = cv2.CascadeClassifier(args["cascade"])
    rects = detector.detectMultiScale(gray, scaleFactor=4, minNeighbors=15, minSize=(100, 100))

    for (i, (x, y, w, h)) in enumerate(rects):
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(image, "Beer #{}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

    cv2.imshow("Beer Bottles", image)
    cv2.waitKey(0)