from django.db import models
from django.utils.html import format_html # Import ini penting buat tombol WA

class Lead(models.Model):
    # --- PILIHAN STATUS LEAD ---
    STATUS_CHOICES = [
        ('NEW', 'New Lead (Belum Diapa-apain)'),
        ('CONTACTED', 'Sudah Dihubungi'),
        ('PROPOSAL', 'Kirim Proposal'),
        ('DEAL', 'Deal / Closing'),
        ('REJECT', 'Ditolak'),
    ]

    # --- DATA UTAMA ---
    name = models.CharField(max_length=200, verbose_name="Nama Bisnis")
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kategori")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="No. HP/WA")
    
    # --- DATA WEBSITE & INTELIJEN ---
    website = models.URLField(blank=True, null=True, verbose_name="Link Website")
    has_website = models.BooleanField(default=False, verbose_name="Punya Web?")
    
    # Hasil Deep Scan (Robot V3)
    email = models.EmailField(blank=True, null=True, verbose_name="Email Kantor")
    tech_stack = models.CharField(max_length=200, blank=True, null=True, verbose_name="Teknologi Web")

    # --- DATA TAMBAHAN ---
    rating = models.FloatField(default=0.0, verbose_name="Rating GMaps")
    reviews_count = models.IntegerField(default=0, verbose_name="Jml Review")
    
    # --- MANAJEMEN ---
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at'] # Data terbaru selalu paling atas

    def __str__(self):
        return self.name

    # --- LOGIC WA OTOMATIS ---

    def clean_phone(self):
        """Membersihkan nomor HP jadi format 62xxx"""
        if not self.phone or self.phone == "-":
            return None
        
        # Ambil angkanya saja
        clean_number = ''.join(filter(str.isdigit, self.phone))
        
        # Ubah 08xx jadi 628xx
        if clean_number.startswith('0'):
            return '62' + clean_number[1:]
        
        # Kalau sudah 62, biarkan
        if clean_number.startswith('62'):
            return clean_number
            
        return clean_number

    def whatsapp_button(self):
        """Membuat Tombol WA Hijau di Admin Panel"""
        phone = self.clean_phone()
        
        if not phone:
            return format_html('<span style="color:red;">No Phone</span>')
            
        # Pesan Otomatis (Ganti kata-katanya di sini)
        # %0A = Enter (Baris Baru)
        sapaan = f"Halo {self.name},"
        isi_pesan = "Saya lihat bisnis Kakak belum punya website resmi ya? Kebetulan kami dari Tech Agency bisa bantu buatkan."
        
        # Kalau dia punya web tapi jadul (WordPress/Unknown), bedakan pesannya
        if self.has_website and self.tech_stack != "Laravel/PHP":
             isi_pesan = "Saya lihat websitenya bisa kita optimalkan biar lebih kencang dan modern."

        full_message = f"{sapaan}%0A%0A{isi_pesan}"
        
        url = f"https://wa.me/{phone}?text={full_message}"
        
        return format_html(
            '<a href="{}" target="_blank" style="background-color:#25D366; color:white; padding:5px 12px; border-radius:15px; text-decoration:none; font-weight:bold; font-size:12px;">'
            '<i class="fas fa-paper-plane"></i> Chat WA'
            '</a>',
            url
        )
    
    whatsapp_button.short_description = "Action"
    whatsapp_button.allow_tags = True
    
    def email_button(self):
        """Tombol Kirim Email"""
        if not self.email:
            return "-"
            
        subject = f"Penawaran Kerjasama Web Development untuk {self.name}"
        body = f"Halo Tim {self.name},%0A%0ASaya lihat website Anda saat ini..."
        
        # Link mailto: biar otomatis buka aplikasi email (Gmail/Outlook)
        url = f"mailto:{self.email}?subject={subject}&body={body}"
        
        return format_html(
            '<a href="{}" target="_blank" style="color:#007bff; text-decoration:none; font-weight:bold;">'
            '<i class="fas fa-envelope"></i> {}'
            '</a>',
            url,
            self.email
        )
    
    email_button.short_description = "Email Kantor"
    email_button.allow_tags = True