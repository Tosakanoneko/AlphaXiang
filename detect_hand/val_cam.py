import os
import cv2
import argparse
import torch
import sys
import numpy as np
import zmq
import base64
current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(current_dir)
sys.path.append(modules_dir)
import utils.utils
def resize_and_pad_image(original_image):
    # 调整大小到128x128
    resized_image = cv2.resize(original_image, (128, 128), interpolation=cv2.INTER_AREA)

    # 创建一个新的352x352的黑色背景图像
    black_background = np.zeros((352, 352, 3), dtype=np.uint8)

    # 计算128x128图像的左上角位置，以使其居中
    x_offset = (352 - 128) // 2
    y_offset = (352 - 128) // 2

    # 将128x128图像粘贴到黑色背景图像的中心
    black_background[y_offset:y_offset+128, x_offset:x_offset+128] = resized_image
    return black_background

def write_data(data):
    # 写入命名管道
    with open('./mypipe', 'w') as pipe:
        pipe.write(data)
    print(f"send to ui: {data}")

class hand_detector:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        modules_dir = os.path.join(current_dir)
        sys.path.append(modules_dir)
        import model.detector
        #指定训练配置文件
        parser = argparse.ArgumentParser()
        parser.add_argument('--data', type=str, default='/home/aidlux/Chinese-chess-GHT2/detect_hand/data/category.data', 
               help='Specify training profile *.data')
        parser.add_argument('--weights', type=str, default='/home/aidlux/Chinese-chess-GHT2/detect_hand/weights/train5/hand-290-epoch-0.273143ap-model.pth', 
                            help='The path of the .pth model to be transformed')

        self.opt = parser.parse_args()
        self.cfg = utils.utils.load_datafile(self.opt.data)
        # assert os.path.exists(self.opt.weights), "请指定正确的模型路径"
        #模型加载
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # self.model = model.detector.Detector(self.cfg["classes"], self.cfg["anchor_num"], True).to(self.device)
        self.model = model.detector.Detector(1, 3, True).to(self.device)
        self.model.load_state_dict(torch.load(self.opt.weights, map_location=self.device)) 
        self.model.eval()

        # self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        self.frame_count = 0
        self.detect_list = []
        self.hand_detected = False

        # 创建 ZMQ 的上下文和 socket
        context = zmq.Context()
        self.socket = context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5556")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, '')  # 订阅所有消息


    def hand_detect(self, frame):
        res_img = resize_and_pad_image(frame)
        cv2.imshow('res_img', res_img)
        # ori_img = cv2.resize(ori_img, (352, 352))
        img = res_img.reshape(1, 352, 352, 3)  # 使用resize_and_pad_image的输出大小
        img = torch.from_numpy(img.transpose(0, 3, 1, 2))
        img = img.to(self.device).float() / 255.0
        # 模型推理
        preds = self.model(img)

        # 特征图后处理
        output = utils.utils.handel_preds(preds, self.cfg, self.device)
        output_boxes = utils.utils.non_max_suppression(output, conf_thres=0.3, iou_thres=0.4)   
        
        hand_detected = False
        for box in output_boxes[0]:
            box = box.tolist()
            obj_score = box[4]
            if obj_score > 0.1:
                self.detect_list.append('hand')
                hand_detected = True
                break
        if not hand_detected:
            self.detect_list.append('nothand')
            

    def run_hand_detect(self):
        while True:
            jpg_as_text = self.socket.recv()
            # 解码图片数据
            jpg_original = base64.b64decode(jpg_as_text)
            jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
            frame = cv2.imdecode(jpg_as_np, flags=1)
            if frame is not None:
                frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.frame_count += 1
                self.hand_detect(frame)
                if self.frame_count % 10 == 0:
                    if self.detect_list.count("hand") > 1:
                        self.hand_detected = True
                    else:
                        self.hand_detected = False
                    self.frame_count = 0
                    self.detect_list = []
                if self.hand_detected:
                    cv2.putText(frame, "hand detected", (10, 35), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) , 2, cv2.LINE_AA)
                frame = cv2.resize(frame, (480, 640))
                cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

if __name__ == '__main__':
    hand_det = hand_detector()
    hand_det.run_hand_detect()
    

