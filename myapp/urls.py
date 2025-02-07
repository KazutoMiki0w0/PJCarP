from django.urls import path, include
from django.contrib import admin
from . import views
from .views import login_view, car_rental_view, receipt, confirm_booking, booking_details, rental_form
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_url = None  # ป้องกัน namespace 'admin' ซ้ำซ้อน

urlpatterns = [
    # 🏠 หน้าแรก
    path('', views.home, name='home'),

    # 🔑 ระบบล็อกอิน/ลงทะเบียน
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path("receipt/<int:booking_id>/", views.receipt, name="receipt"),

    # 🚗 ระบบเช่ารถ
    path("car_rental/", views.car_rental_view, name="car_rental"),
    path("rental/<int:car_id>/", views.rental_form, name="rental_form"),
    path('booking/<int:car_id>/', views.booking_details, name='booking_details'),
    path('form/<int:car_id>/', views.booking_form, name='booking_form'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path("confirm-booking/", confirm_booking, name="confirm_booking"),
    path("receipt/", receipt, name="receipt"),
    path("receipt/", views.receipt, name="receipt"),

    
    # 🏪 จัดการรถยนต์
    path('add_car/', views.add_car, name='add_car'),
    path('edit_car/<int:car_id>/', views.edit_car, name='edit_car'),
    path('delete_car/<int:car_id>/', views.delete_car, name='delete_car'),
    path('purchase/<int:car_id>/', views.purchase, name='purchase'),
    path('receipt/', views.receipt, name='receipt'),
    


    # 🔧 แผงควบคุม (Admin Panel)
    path('dashboard/', views.admin_panel, name='custom_admin_panel'),
    path('dashboard/edit-car/<int:car_id>/', views.edit_car, name='edit_car_dashboard'),
    path('dashboard/delete-car/<int:car_id>/', views.delete_car, name='delete_car_dashboard'),
    path('dashboard/edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('dashboard/delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    # 🎨 Django Grappelli (ถ้ามีใช้)
    path('grappelli/', include('grappelli.urls')),

    # ⚙️ Django Admin
    path('admin/', admin.site.urls),  
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('payment-success/', views.payment_success, name='payment_success'),
]

# ⚠️ เสิร์ฟไฟล์มีเดียในโหมด Debug
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


