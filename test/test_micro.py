import os
import time
import threading

def read_data():
    tmp_msg = ''
    # 从命名管道读取数据
    try:
        while True:
            try:
                with open('/tmp/mypipe1', 'r') as pipe:
                    data = pipe.read()
                    if data:
                        print(f"{data}")
                time.sleep(1)
                        # return data
            except OSError:
                time.sleep(1)
    except KeyboardInterrupt:
        exit()

def write_data():
    with open('./mypipe1', 'w') as pipe:
        pipe.write('')
    while True:
        data = input("Write data to mypipe1:")
        with open('./mypipe1', 'w') as pipe:
            pipe.write(data)


# write_thread = threading.Thread(target=write_data)
# write_thread.setDaemon(True)
# write_thread.start()
read_data()

