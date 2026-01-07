from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .utils import run_hunter
from django.db.models import Count # <--- Import ini buat ngitung data
from django.contrib import admin
from .models import Lead
import json
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.shortcuts import get_object_or_404


# Decorator ini mastiin cuma admin yang bisa akses
@staff_member_required
def hunt_leads(request):
    if request.method == "POST":
        keyword = request.POST.get('keyword')
        if keyword:
            # Panggil fungsi robot yang tadi kita buat
            count = run_hunter(keyword)
            messages.success(request, f"Sukses! Robot berhasil menangkap {count} leads baru.")
        else:
            messages.error(request, "Keyword tidak boleh kosong!")
            
    # Balikin lagi ke halaman list Leads
    return redirect('/admin/dashboard/lead/')

@staff_member_required
def dashboard_analytics(request):
    """
    View ini akan menggantikan halaman depan Admin (Dashboard)
    """
    
    # 1. Ambil Data Status (Untuk Pie Chart)
    # Hasilnya: [{'status': 'NEW', 'total': 10}, {'status': 'DEAL', 'total': 2}]
    status_data = Lead.objects.values('status').annotate(total=Count('id'))
    
    # Pisahkan Label dan Angka biar gampang dibaca Chart.js
    status_labels = [item['status'] for item in status_data]
    status_counts = [item['total'] for item in status_data]

    # 2. Ambil Data Tech Stack (Untuk Bar Chart)
    # Kita filter yang punya web aja
    tech_data = Lead.objects.filter(has_website=True).values('tech_stack').annotate(total=Count('id')).order_by('-total')[:5] # Ambil Top 5
    
    tech_labels = [item['tech_stack'] if item['tech_stack'] else 'Unknown' for item in tech_data]
    tech_counts = [item['total'] for item in tech_data]

    # 3. Data Ringkasan Atas (Scorecard)
    total_leads = Lead.objects.count()
    total_deals = Lead.objects.filter(status='DEAL').count()
    potential_revenue = total_deals * 5000000 # Anggap 1 project 5 Juta (Estimasi Kasar)

    # 4. Gabungkan dengan Context Admin Asli (Biar Sidebar Jazzmin gak ilang)
    context = admin.site.each_context(request)
    context.update({
        'status_labels': status_labels,
        'status_counts': status_counts,
        'tech_labels': tech_labels,
        'tech_counts': tech_counts,
        'total_leads': total_leads,
        'total_deals': total_deals,
        'potential_revenue': potential_revenue,
    })

    return render(request, 'admin/index.html', context)

@staff_member_required
def download_proposal(request, lead_id):
    # 1. Ambil data lead yang mau diprospek
    lead = get_object_or_404(Lead, pk=lead_id)
    
    # 2. Tentukan Template Surat (Nanti kita buat file html-nya)
    template_path = 'proposal_pdf.html'
    
    # 3. Masukkan data lead ke dalam surat (Context)
    context = {
        'lead': lead,
        'my_agency': 'Hanif Creative Agency', # Ganti nama agency lo
        'price': 'Rp 5.000.000', # Harga default
    }
    
    # 4. Proses Sulap HTML jadi PDF
    response = HttpResponse(content_type='application/pdf')
    # Biar pas diklik langsung download (attachment)
    response['Content-Disposition'] = f'attachment; filename="Proposal_{lead.name}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Maaf, gagal bikin PDF <pre>' + html + '</pre>')
        
    return response

