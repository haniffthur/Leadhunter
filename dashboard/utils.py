import requests
import json
import google.generativeai as genai
from .models import Lead

# ==========================================
# 🔑 AREA ISI BENSIN (API KEY)
# ==========================================
# Paste API Key Serper lo di sini (Jangan hapus tanda kutipnya)
SERPER_API_KEY = "3179953178ed5b6270b07d33fbc1c98623123371"

# Paste API Key Gemini lo di sini
GEMINI_API_KEY = "AIzaSyBMocYXMa70vHR98oRRVvqejv_1UXJVVoE"
# ==========================================

# Setup Otak Gemini
genai.configure(api_key=GEMINI_API_KEY)

def search_google_maps(keyword):
    """
    MATA ROBOT: Nyari data di Google Maps via Serper
    """
    url = "https://google.serper.dev/places"
    payload = json.dumps({
        "q": keyword,
        "gl": "id", # Lokasi Indonesia
        "hl": "id"  # Bahasa Indonesia
    })
    headers = {
        'X-API-KEY': SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        results = response.json().get("places", [])
        return results
    except Exception as e:
        print(f"Error Serper: {e}")
        return []

def analyze_with_ai(place_data):
    """
    OTAK ROBOT: Gemini menganalisa data mentah
    """
    # Kita pake model Gemini Pro yang gratis & cepat
    model = genai.GenerativeModel('gemini-1.5-flash') 
    
    nama_bisnis = place_data.get("title", "Bisnis ini")
    alamat = place_data.get("address", "")
    kategori_google = place_data.get("category", "")
    
    prompt = f"""
    Analisa data bisnis ini:
    Nama: {nama_bisnis}
    Alamat: {alamat}
    Kategori Google: {kategori_google}
    
    Tugasmu:
    1. Tentukan kategori bisnis yang lebih spesifik (Contoh: 'Coffee Shop', 'Barbershop', 'Law Firm').
    2. Perkirakan Tech Stack website mereka (jika ada). Jika tidak tahu, jawab 'Unknown'.
    
    Jawab HANYA dalam format JSON valid seperti ini tanpa markdown:
    {{
        "kategori_fix": "...",
        "tech_stack_prediksi": "..."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Bersihkan format markdown ```json ... ``` kalau ada
        text_bersih = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text_bersih)
    except Exception as e:
        print(f"Error Gemini: {e}")
        # Fallback kalau AI pusing
        return {
            "kategori_fix": kategori_google,
            "tech_stack_prediksi": "Unknown"
        }

def run_hunter(keyword):
    """
    Fungsi Utama yang dipanggil tombol 'Start Hunting'
    """
    # 1. MATA: Cari data mentah
    print(f"🤖 Robot mencari: {keyword}...")
    raw_places = search_google_maps(keyword)
    
    leads_count = 0
    
    for place in raw_places:
        title = place.get("title")
        
        # Cek duplikat (Kalau nama sama persis, skip)
        if Lead.objects.filter(name=title).exists():
            continue
            
        # 2. OTAK: Analisa pakai AI
        print(f"🧠 Menganalisa: {title}...")
        ai_analysis = analyze_with_ai(place)
        
        # 3. SIMPAN: Masukkan ke Database
        Lead.objects.create(
            name=title,
            address=place.get("address", "-"),
            phone=place.get("phoneNumber", "-"),
            website=place.get("website", ""), # Kalau gak ada website, otomatis kosong
            has_website=True if place.get("website") else False,
            
            # Data dari AI
            category=ai_analysis.get('kategori_fix', 'Umum'),
            tech_stack=ai_analysis.get('tech_stack_prediksi', 'Unknown'),
            
            status='NEW'
        )
        leads_count += 1
        
    return leads_count