from display_driver_utils import driver

# 初始化显示驱动
drv = driver(width=1356, height=705)

import ui
import time
def read_data():
    # 读取命名管道数据
    try:
        with open('/tmp/mypipe', 'r') as pipe:
            data = pipe.read().strip()
            print(data)
            return data
    except OSError as e:
        print("Error reading pipe:", e)
        return None

def read_data2():
    # 读取命名管道数据
    try:
        with open('/tmp/mypipe3', 'r') as pipe:
            data = pipe.read().strip()
            print(data)
            return data
    except OSError as e:
        print("Error reading pipe:", e)
        return None

def read_data3():
    # 读取命名管道数据
    try:
        with open('/tmp/mypipe5', 'r') as pipe:
            data = pipe.read().strip()
            print(data)
            return data
    except OSError as e:
        print("Error reading pipe:", e)
        return None

def read_data4():
    # 读取命名管道数据
    try:
        with open('/tmp/mypipe6', 'r') as pipe:
            data = pipe.read().strip()
            print(data)
            return data
    except OSError as e:
        print("Error reading pipe:", e)
        return None
        
ui.lv.scr_load(ui.ui_Screen1)
while True:
    fen_data = read_data()
    message_data=read_data2()
    go_data=read_data3()
    back_data=read_data4()
    if fen_data:
        ui.update_chess_pieces_from_fen(fen_data)

    if message_data:
    	ui.updateMessage(message_data)
    	
    if go_data:
    	ui.showGo(go_data)
    if back_data:
    	ui.backGo(back_data)
    time.sleep(0.2)
