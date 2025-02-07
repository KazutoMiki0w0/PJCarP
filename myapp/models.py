from django.db import models
from django.contrib.auth.models import User


class Location(models.Model):
    """
    โมเดลสำหรับสถานที่รับ-คืนรถ
    """
    name = models.CharField(max_length=100, verbose_name="ชื่อสถานที่")
    latitude = models.FloatField(verbose_name="ละติจูด")
    longitude = models.FloatField(verbose_name="ลองจิจูด")

    def __str__(self):
        return self.name


class Car(models.Model):
    """
    โมเดลสำหรับรถยนต์ที่ให้เช่า
    """
    name = models.CharField(max_length=255, verbose_name="ชื่อรถ")
    brand = models.CharField(max_length=100, verbose_name="ยี่ห้อ")
    model = models.CharField(max_length=255, verbose_name="รุ่น")
    year = models.PositiveIntegerField(verbose_name="ปีที่ผลิต")
    type = models.CharField(
        max_length=50,
        choices=[
            ('Sedan', 'Sedan'),
            ('SUV', 'SUV'),
            ('Truck', 'Truck'),
            ('Van', 'Van'),
        ],
        verbose_name="ประเภทรถ"
    )
    seats = models.PositiveIntegerField(default=5, verbose_name="จำนวนที่นั่ง")
    doors = models.PositiveIntegerField(default=4, verbose_name="จำนวนประตู")
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="ราคา/วัน")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="ส่วนลด (%)")
    image = models.ImageField(upload_to='cars/', blank=True, null=True, verbose_name="รูปภาพ")
    description = models.TextField(default="ไม่มีข้อมูล", verbose_name="รายละเอียด")
    available = models.BooleanField(default=True, verbose_name="พร้อมให้เช่า")

    class Meta:
        verbose_name = "รถยนต์"
        verbose_name_plural = "รถยนต์ทั้งหมด"
        ordering = ['-year']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"

    def get_price(self):
        """
        คำนวณราคาหลังหักส่วนลด
        """
        discounted_price = self.price_per_day * (1 - (self.discount / 100))
        return f"฿{discounted_price:,.2f} / วัน"


class UserProfile(models.Model):
    """
    โมเดลสำหรับจัดเก็บข้อมูลผู้ใช้เพิ่มเติม
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="ผู้ใช้")
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="เบอร์โทรศัพท์")
    address = models.TextField(blank=True, null=True, verbose_name="ที่อยู่")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, verbose_name="รูปโปรไฟล์")
    is_admin = models.BooleanField(default=False, verbose_name="เป็นแอดมิน")

    class Meta:
        verbose_name = "โปรไฟล์ผู้ใช้"
        verbose_name_plural = "โปรไฟล์ผู้ใช้ทั้งหมด"

    def __str__(self):
        return f"{self.user.username} ({'Admin' if self.is_admin else 'User'})"


class Booking(models.Model):
    """
    โมเดลสำหรับการจองรถ
    """
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name="รถที่จอง")
    pickup_location = models.ForeignKey(
        'Location', on_delete=models.CASCADE, related_name='pickup', verbose_name="สถานที่รับรถ"
    )
    dropoff_location = models.ForeignKey(
        'Location', on_delete=models.CASCADE, related_name='dropoff', verbose_name="สถานที่คืนรถ"
    )
    pickup_date = models.DateTimeField(verbose_name="วันที่รับรถ")
    dropoff_date = models.DateTimeField(verbose_name="วันที่คืนรถ")
    full_name = models.CharField(max_length=100, verbose_name="ชื่อผู้จอง")
    email = models.EmailField(verbose_name="อีเมล")
    phone = models.CharField(max_length=15, verbose_name="เบอร์โทรศัพท์")
    status = models.CharField(
        default='pending',
        max_length=20,
        choices=[
            ('pending', 'รอดำเนินการ'),
            ('confirmed', 'ยืนยันแล้ว'),
            ('cancelled', 'ยกเลิก'),
        ],
        verbose_name="สถานะ"
    )

    class Meta:
        verbose_name = "การจอง"
        verbose_name_plural = "การจองทั้งหมด"
        ordering = ['-pickup_date']

    def __str__(self):
        return f"{self.full_name} - {self.car.name}"
