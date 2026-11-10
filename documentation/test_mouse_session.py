import pyautogui
with open('mouse_result.txt', 'w') as f:
    f.write(str(pyautogui.position()))
