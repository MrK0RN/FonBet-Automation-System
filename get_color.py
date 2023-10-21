import pyautogui
import time
import position

def pixel(x, y):
    change = pyautogui.pixel(x, y)
    answer = [(int(change.red)), (int(change.green)), (int(change.blue))]
    return answer

def log(color, k):
    s = k + "|" + str(color[0]) + "||" + str(color[1]) + "||" + str(color[2]) + "|"
    return s

def color_for_check(k):
    time.sleep(1)
    pos = position.get_position()
    answer = pixel(int(pos[0]), int(pos[1]))

    return answer
    #return log(answer, k)


