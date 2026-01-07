from django.contrib import admin
from django.urls import path
from dashboard import views
from django.views.generic import RedirectView

urlpatterns = [
    # 1. Dashboard Analytics (Halaman Depan)
    path('admin/', views.dashboard_analytics, name='admin_dashboard'),

    # 2. Robot Hunter
    path('admin/hunt/', views.hunt_leads, name='hunt_leads'),

    # --- 3. TAMBAHKAN INI (JALUR PDF) ---
    # Pastikan baris ini ada biar tombolnya berfungsi!
    path('admin/proposal/<int:lead_id>/', views.download_proposal, name='download_proposal'),

    # 4. Admin Bawaan (Wajib di Bawah)
    path('admin/', admin.site.urls),

    # 5. Redirect ke Admin
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
]