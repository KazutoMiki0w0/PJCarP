from django.contrib import admin
from django.utils.html import format_html
from .models import Car, UserProfile

# 🎨 ปรับแต่ง Header Django Admin
admin.site.site_header = "🚗 ระบบจัดการรถเช่า"
admin.site.site_title = "Admin | ระบบรถเช่า"
admin.site.index_title = "📊 จัดการข้อมูลระบบ"

# ✅ ปรับแต่งหน้า Admin ของ Car
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'name', 'brand', 'model', 'year', 'doors', 'seats', 'price_per_day', 'discount', 'available')
    search_fields = ('name', 'brand', 'model', 'year')
    list_filter = ('brand', 'year', 'available', 'doors', 'seats')
    list_editable = ('price_per_day', 'discount', 'available')
    
    fieldsets = (
        ('🚗 ข้อมูลรถ', {'fields': ('name', 'brand', 'model', 'year', 'doors', 'seats', 'image')}),
        ('💰 การกำหนดราคา', {'fields': ('price_per_day', 'discount')}),
        ('✅ สถานะ', {'fields': ('available',)}),
    )

    def thumbnail(self, obj):
        """แสดงภาพตัวอย่างรถ"""
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="80" height="50" style="border-radius:5px;">')
        return "ไม่มีภาพ"
    thumbnail.short_description = 'ภาพตัวอย่าง'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

# ✅ ปรับแต่งหน้า Admin ของ UserProfile
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'is_active')  
    search_fields = ('user__username', 'phone', 'address')
    list_filter = ('user__is_active',)  
    ordering = ('-user__date_joined',)  

    def is_active(self, obj):
        """แสดงสถานะผู้ใช้"""
        return obj.user.is_active
    is_active.boolean = True
    is_active.short_description = "Active"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
