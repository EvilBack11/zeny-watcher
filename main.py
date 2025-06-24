from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time

# --- الإعدادات ---
TARGET_PRICE = 2.0  # ⬅️ السعر المستهدف الجديد
CHECK_INTERVAL = 60  # عدد الثواني بين كل تحقق
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1387142473738096681/DvjHP0gqxdZfG6PJCiM8hWM4KU6LnR14EftaJVsRvvvO5vsmchsnICPmZxLsTMHi8b-V"
ITEM_NAME = "Zeny Pocket 1000000"
ITEM_URL = "https://apps-genesis.maxion.gg/roverse-genesis?cat=usable_item&searchID=1500117"

# --- إعداد المتصفح ---
options = Options()
options.add_argument("--headless")  # تشغيل بدون واجهة
options.add_argument("--disable-gpu")
driver = webdriver.Chrome(service=Service("chromedriver.exe"), options=options)

# --- قراءة السعر ---
def get_zeny_price():
    try:
        driver.get(ITEM_URL)
        wait = WebDriverWait(driver, 15)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "price")))
        price_element = driver.find_element(By.CLASS_NAME, "price")
        price_text = price_element.text.strip()
        return float(price_text)
    except Exception as e:
        print(f"[❌] خطأ أثناء قراءة السعر: {e}")
        return None

# --- إرسال إلى ديسكورد ---
def send_discord_alert(price):
    message = {
        "content": f"🎯 السعر الحالي للقطعة **{ITEM_NAME}** هو `{price} ION`\n🔗 رابط السوق: {ITEM_URL}"
    }
    response = requests.post(DISCORD_WEBHOOK, json=message)
    print(f"📩 تم إرسال تنبيه إلى Discord. Status Code: {response.status_code}")

# --- مراقبة مستمرة ---
print(f"⏳ بدأ المراقبة للقطعة {ITEM_NAME} ...")
while True:
    price = get_zeny_price()
    if price:
        print(f"🔍 السعر الحالي: {price} ION")
        if price <= TARGET_PRICE:
            print("✅ السعر مناسب! إرسال تنبيه...")
            send_discord_alert(price)
    else:
        print("⚠️ لم يتم العثور على السعر، إعادة المحاولة...")
    time.sleep(CHECK_INTERVAL)
