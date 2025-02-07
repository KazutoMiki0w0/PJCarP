from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    
    path('accounts/', include('allauth.urls')),  # เพิ่ม URL ของ allauth สำหรับการสมัครและล็อกอิน
    path('', include('myapp.urls')),  # รวม URL ของแอป myapp สำหรับหน้า Home และอื่น ๆ
    
]
