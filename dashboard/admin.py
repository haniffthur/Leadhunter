from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from django.urls import reverse
from .models import Lead

@admin.register(Lead)
class LeadAdmin(ImportExportModelAdmin):
    
    # --- 1. OVERRIDE TAMPILAN ROBOT HUNTER ---
    # Fungsi ini maksa Django pake template robot kita, biar gak dicuekin Jazzmin
    def changelist_view(self, request, extra_context=None):
        self.change_list_template = 'robot_hunter.html'
        return super().changelist_view(request, extra_context)

    # --- 2. FUNGSI LINK WEBSITE (BIRU) ---
    def website_link(self, obj):
        if obj.website:
            return format_html('<a href="{}" target="_blank" style="color: #3498db; text-decoration: none; font-weight: bold;">🔗 Buka Web</a>', obj.website)
        return "-"
    website_link.short_description = "Website"

    # --- 3. FUNGSI TOMBOL PROPOSAL PDF (MERAH) ---
    def proposal_button(self, obj):
        # Ambil URL download berdasarkan ID
        url = reverse('download_proposal', args=[obj.id])
        return format_html(
            '<a href="{}" style="background-color: #e74c3c; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-weight: bold; font-size: 11px;">📄 PDF</a>',
            url
        )
    proposal_button.short_description = "Proposal"
    
    # --- 4. FUNGSI BADGE STATUS (WARNA-WARNI) ---
    def status_badge(self, obj):
        # Tentukan warna hex code berdasarkan status lead
        if obj.status == 'NEW':
            color = '#3498db'   # Biru
        elif obj.status == 'CONTACTED':
            color = '#f39c12' # Kuning
        elif obj.status == 'MEETING':
            color = '#9b59b6' # Ungu
        elif obj.status == 'DEAL':
            color = '#2ecc71' # Hijau (Sukses)
        elif obj.status == 'REJECTED':
            color = '#e74c3c' # Merah (Gagal)
        else:
            color = '#95a5a6' # Abu-abu

        # Render kotak rounded
        return format_html(
            '<span style="background-color: {}; color: white; padding: 4px 10px; border-radius: 50px; font-weight: bold; font-size: 11px;">{}</span>',
            color,
            obj.status
        )
    status_badge.short_description = "Status"

    # --- 5. PENGATURAN TABEL (LIST DISPLAY) ---
    list_display = (
        'name', 
        'phone', 
        'website_link',    # Kolom Link Web
        'proposal_button', # Kolom Tombol PDF
        'tech_stack', 
        'status_badge',    # Kolom Status Warna-warni
        'whatsapp_button'
    )
    
    search_fields = ('name', 'address', 'category', 'tech_stack')
    list_filter = ('status', 'has_website', 'category', 'created_at')
    
    # PENTING: list_editable saya matikan (comment) karena kolom 'status' aslinya
    # sudah digantikan oleh 'status_badge'. Kalau dinyalakan akan error.
    # list_editable = ('status',)
    
    list_per_page = 20