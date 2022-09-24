import time
import EyeDr4
import cv2
import os
import tracemalloc
import string_split as js
import api_http as api
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
flag = 0
def on_created(event):
    global flag
    flag = 1
    name = event.src_path.split('\\')[1]
    
    print(f"{name} has been created!")
    '''
    global flag
    flag = 1
    img = cv2.imread(name)
    height, width, channels = img.shape
    result, s, n, t, i, x_c, y_c, w_c, h_c, x_d, y_d, w_d, h_d =  EyeDr4.EyeDr(name, img, height, width)
    #cv2.imwrite(os.path.join('Labeled_GLC/' , name), result)
    send_api(name, width, height, s, n, t, i, x_c, y_c, w_c, h_c, x_d, y_d, w_d, h_d)
    os.remove(name)
    flag = 0
    '''
def on_deleted(event):
    global flag
    flag = 0
    print(f"{event.src_path} deleted!")
def on_modified(event):
    global flag
    if flag == 1:
        print("Being process")
        name = event.src_path.split('\\')[1]
        img = cv2.imread(name)
        height, width, channels = img.shape
        result, s, n, t, i, x_c, y_c, w_c, h_c, x_d, y_d, w_d, h_d =  EyeDr4.EyeDr(name, img, height, width)
        #cv2.imwrite(os.path.join('Labeled_GLC/' , name), result)
        send_api(name, width, height, s, n, t, i, x_c, y_c, w_c, h_c, x_d, y_d, w_d, h_d)
        os.remove(name)
    else:
        print(f"{event.src_path} has been modified")
def on_moved(event):
    print(f"{event.src_path} moved to {event.dest_path}")
def send_api(name, width, height, s, n, t, i, x_c, y_c, w_c, h_c, x_d, y_d, w_d, h_d):
    x_c = x_c + int(w_c/2)
    y_c = y_c + int(h_c/2)
    x_d = x_d + int(w_d/2)
    y_d = y_d + int(h_d/2)
    name, jstxt = js.stringsplit(name, (width,height), s, n, t, i,
                   float("{:.6f}".format(x_c)), float("{:.6f}".format(y_c)), float("{:.6f}".format(w_c)),
                    float("{:.6f}".format(h_c)), float("{:.6f}".format(x_d)), float("{:.6f}".format(y_d)),
                    float("{:.6f}".format(w_d)), float("{:.6f}".format(h_d)))
    api.api_send(name ,jstxt)
if __name__ == "__main__":
    tracemalloc.start()
    patterns = ["*.JPG","*.PNG"]
    ignore_patterns = None
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    my_event_handler.on_created = on_created
    my_event_handler.on_deleted = on_deleted
    my_event_handler.on_modified = on_modified
    my_event_handler.on_moved = on_moved
    path = "."
    go_recursively = False
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
       while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
    current, peak = tracemalloc.get_traced_memory()
    print("Peak : ", peak)

