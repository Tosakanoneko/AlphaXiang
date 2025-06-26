from model.hand_det import *
import threading
from multiprocessing import Process, Queue
import cv2
if __name__ == '__main__':
    frame_queue = Queue()
    hand_det = hand_detector(frame_queue)
    cap =cv2.VideoCapture(2, cv2.CAP_V4L2)
    process = Process(target=hand_det.run_hand_detect)
    process.start()
    while True:
        try:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('frame', frame)
                frame_queue.put(frame)
                # hand_det.frame = frame.copy()
                # cv2.imshow('Frrrame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            print("Exit")
            frame_queue.put(None)
            process.kill()
            break
    cap.release()
    cv2.destroyAllWindows()
    
