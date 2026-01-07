from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from dashboard.models import Lead
import time

class Command(BaseCommand):
    help = 'Robot V2: Pencari leads detail (Phone + Website status)'

    def add_arguments(self, parser):
        parser.add_argument('keyword', type=str, help='Kata kunci pencarian')

    def handle(self, *args, **kwargs):
        keyword = kwargs['keyword']
        self.stdout.write(f"🤖 Robot V2 Memulai Misi: {keyword}...")

        # Setup Chrome (Headless: False biar lo bisa liat prosesnya)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        try:
            driver.get("https://www.google.com/maps")
            time.sleep(3)

            # 1. Cari Keyword
            search_box = driver.find_element(By.ID, "searchboxinput")
            search_box.send_keys(keyword)
            search_box.send_keys(Keys.ENTER)
            time.sleep(5) # Tunggu hasil load

            # 2. Scroll Panel ke Bawah (Biar dapet minimal 10-20 data)
            self.stdout.write("Sedang scroll mencari target...")
            
            # Kita cari panel scroll-nya (biasanya role='feed')
            try:
                scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
                # Scroll 3 kali
                for _ in range(3):
                    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
                    time.sleep(2)
            except:
                self.stdout.write("Warning: Gagal scroll otomatis, mengambil data yang terlihat saja.")

            # 3. Ambil List Element
            # Class 'hfpxzc' adalah link transparan yang menutupi card bisnis di maps
            items = driver.find_elements(By.CLASS_NAME, "hfpxzc")
            self.stdout.write(f"Menemukan {len(items)} target. Mulai ekstraksi detail...")

            count = 0
            
            # Kita loop satu per satu
            for item in items:
                try:
                    name = item.get_attribute("aria-label")
                    
                    # Cek duplikat dulu biar hemat waktu
                    if Lead.objects.filter(name=name).exists():
                        print(f"⏩ SKIP: {name} (Sudah ada)")
                        continue

                    # KLIK ITEMNYA (Biar panel detail di kiri update)
                    item.click()
                    time.sleep(2) # Kasih napas buat loading detail

                    # --- LOGIC NYARI WEBSITE & TLP ---
                    phone = "-"
                    website = ""
                    has_web = False
                    address = ""

                    # 1. Cari Tombol Website (Biasanya punya data-item-id="authority")
                    try:
                        web_btn = driver.find_element(By.CSS_SELECTOR, '[data-item-id="authority"]')
                        website = web_btn.get_attribute("href")
                        has_web = True
                    except:
                        has_web = False # Yess! Ini target market kita

                    # 2. Cari Tombol Telepon (Biasanya data-item-id start with "phone")
                    try:
                        phone_btn = driver.find_element(By.CSS_SELECTOR, '[data-item-id^="phone"]')
                        # Biasanya formatnya "Phone: 0812..." di aria-label
                        raw_phone = phone_btn.get_attribute("aria-label")
                        phone = raw_phone.replace("Phone:", "").strip() if raw_phone else "-"
                    except:
                        phone = "-"
                    
                    # 3. Simpan ke Database
                    Lead.objects.create(
                        name=name,
                        category=keyword,
                        phone=phone,
                        website=website,
                        has_website=has_web,
                        status='NEW' # Status awal selalu NEW
                    )
                    
                    status_icon = "❌ No Web (TARGET!)" if not has_web else "✅ Punya Web"
                    self.stdout.write(self.style.SUCCESS(f"SAVE: {name} | {status_icon} | 📞 {phone}"))
                    count += 1

                except Exception as e:
                    print(f"Error extracting item: {e}")

            self.stdout.write(self.style.SUCCESS(f"🏁 Misi Selesai! Berhasil menangkap {count} leads lengkap."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Fatal Error: {e}"))
        
        finally:
            driver.quit()