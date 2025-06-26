import cv2
exit_mark = False
while not exit_mark:
    for i in range(0,4):
        try:
            print("try",i,"camera")
            cap=cv2.VideoCapture(i,cv2.CAP_V4L2)
            if cap.isOpened():
                print(i,"success!")
                exit_mark = True
                break
        except Exception:
            print(i,"failed")