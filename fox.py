import subprocess
import sys

# قائمة المكتبات المطلوبة
required_libraries = ['requests']

# دالة لتثبيت المكتبات المفقودة
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# تثبيت المكتبات المفقودة
for library in required_libraries:
    try:
        __import__(library)
    except ImportError:
        print(f"مكتبة {library} غير مثبتة. جاري تثبيتها...")
        install_package(library)

# استيراد المكتبات
import random
import string
import threading
import requests

# ألوان للتنسيق
B = '\x1b[38;5;208m'  # برتقالي
E = '\033[1;31m'  # أحمر
F = '\033[2;32m'  # أخضر

# إدخال بيانات المستخدم
ID = input(F + 'ID: ')
token = input(B + 'TOKEN: ')

# دالة لفحص الأسماء على روبلوكس
def Roblox(user):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        }

        response = requests.get(f'https://www.roblox.com/user.aspx?username={user}', headers=headers, timeout=10)

        if response.status_code == 404:
            print(f"{F}صح: {user}")
            message = f'''
*جبت لك يوزر روبلوكس*
**يوزر:** `{user}`
_حسابي: @xxxxxthefox1_
            '''
            requests.post(f'https://api.telegram.org/bot{token}/sendMessage', data={
                'chat_id': ID,
                'text': message,
                'parse_mode': 'Markdown'
            })

        elif response.status_code == 200:
            if "This username is already taken" in response.text:
                print(f"{E}Taken Username: {user}")
            else:
                print(f"{E}خطا: {user}")
        else:
            print(f"")

    except requests.exceptions.RequestException as e:
        print(E + f"404")
    except Exception as e:
        print(E + f"404")

# دالة توليد أسماء نادرة ومناسبة
def generate_usernames():
    while True:
        part1 = ''.join(random.choices(string.ascii_letters, k=random.randint(2, 3)))  # حروف فقط
        part2 = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 2)))  # حروف مع أرقام
        username = f"{part1}{random.choice(['_', '', ''])}{part2}"  # قد يحتوي على "_" أو لا
        if 3 <= len(username) <= 20:  # التأكد من أن الاسم مناسب لطول روبلوكس
            Roblox(username)

# إنشاء وتشغيل الخيوط
Threads = []
for _ in range(10):  # عدد الخيوط
    t = threading.Thread(target=generate_usernames)
    t.start()
    Threads.append(t)

# انتظار جميع الخيوط حتى تنتهي
for thread in Threads:
    thread.join()