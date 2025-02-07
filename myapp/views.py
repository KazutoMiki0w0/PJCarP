from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_backends
from .models import Car, UserProfile, Location, Booking
from .forms import CarForm, UserForm, CustomUserCreationForm, BookingForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
from django.conf import settings
from django.utils.dateparse import parse_date



# ✅ Helper function: ตรวจสอบว่าเป็นแอดมิน
def is_admin(user):
    return user.is_staff  # Django ใช้ `is_staff` สำหรับแอดมิน


# ✅ ฟังก์ชันเข้าสู่ระบบ (Login)
def login_view(request):
    """
    ฟังก์ชันเข้าสู่ระบบ รองรับ next parameter และแสดงข้อความแจ้งเตือนเมื่อใส่รหัสผิด
    """
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, "⚠️ กรุณากรอกชื่อผู้ใช้และรหัสผ่าน!")
            return redirect('login')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "✅ เข้าสู่ระบบสำเร็จ!")
            
            # ✅ เช็คพารามิเตอร์ next
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "❌ ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง!")

    return render(request, 'myapp/login.html', {'next': request.GET.get('next', '')})


def select_car(request):
    cars = Car.objects.all()
    return render(request, 'select_car.html', {'cars': cars})

def booking_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    pickup_date = request.GET.get('pickup_date')
    return_date = request.GET.get('return_date')

    if pickup_date and return_date:
        days = (parse_date(return_date) - parse_date(pickup_date)).days
        total_price = car.price_per_day * days
    else:
        total_price = 0

    return render(request, 'myapp/booking_details.html', {
        'car': car,
        'pickup_date': pickup_date,
        'return_date': return_date,
        'total_price': total_price
    })

def confirm_booking(request):
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        pickup_date = request.POST.get("pickup_date")
        return_date = request.POST.get("return_date")
        total_price = request.POST.get("total_price")

        car = get_object_or_404(Car, id=car_id)

        return render(request, "myapp/confirm_booking.html", {
            "car": car,
            "pickup_date": pickup_date,
            "return_date": return_date,
            "total_price": total_price
        })
    return redirect("home") 

def booking_form(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.car = car
            booking.save()
            return redirect('payment', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'booking_form.html', {'form': form, 'car': car})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Booking

from django.shortcuts import render, redirect, get_object_or_404
from myapp.models import Car, Booking  # เปลี่ยนเป็นชื่อแอปของคุณ

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, Booking

from django.shortcuts import render

def receipt(request):
    if request.method == "POST":
        pickup_location = request.POST.get('pickup_location', 'ไม่ระบุ')
        return_location = request.POST.get('return_location', 'ไม่ระบุ')
        first_name = request.POST.get('first_name', 'ไม่ระบุ')
        last_name = request.POST.get('last_name', 'ไม่ระบุ')
        email = request.POST.get('email', 'ไม่ระบุ')
        phone = request.POST.get('phone', 'ไม่ระบุ')

        context = {
            'pickup_location': pickup_location,
            'return_location': return_location,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
        }

        return render(request, 'receipt.html', context)

    return render(request, 'receipt.html', {})





def payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'payment.html', {'booking': booking})

# ✅ ฟังก์ชันออกจากระบบ (Logout)
def logout_view(request):
    logout(request)
    messages.success(request, "👋 ออกจากระบบสำเร็จ!")
    return redirect('login')


# ✅ ฟังก์ชันสมัครสมาชิก (Register)
def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password1 = request.POST.get("password1").strip()
        password2 = request.POST.get("password2").strip()
        email = request.POST.get("email").strip()
        display_name = request.POST.get("display_name").strip()

        if User.objects.filter(username=username).exists():
            messages.error(request, "⚠️ ชื่อบัญชีนี้ถูกใช้ไปแล้ว!")
            return redirect("register")

        if password1 != password2:
            messages.error(request, "❌ รหัสผ่านไม่ตรงกัน!")
            return redirect("register")

        if len(password1) < 6:
            messages.error(request, "🔑 รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร!")
            return redirect("register")

        user = User.objects.create_user(username=username, password=password1, email=email)
        user.first_name = display_name
        user.save()

        # ✅ ใช้ get_or_create ป้องกันข้อผิดพลาด
        UserProfile.objects.get_or_create(user=user)

        login(request, user)  # ✅ ใช้ login(request, user) ตามปกติ ไม่ต้องกำหนด backend

        messages.success(request, "🎉 สมัครสมาชิกสำเร็จ! ยินดีต้อนรับ 🚗💨")
        return redirect("home")

    return render(request, "myapp/register.html")


# ✅ ฟังก์ชันแสดงรถทั้งหมด
@login_required
def home(request):
    locations = Location.objects.all()
    print(type(Location))
    cars = Car.objects.all()

    # ✅ ดึงยี่ห้อทั้งหมดจากฐานข้อมูล
    brands = Car.objects.values_list('brand', flat=True).distinct()

    # 🔹 รับค่าตัวกรอง
    brand = request.GET.get('brand')
    if brand:
        cars = cars.filter(brand=brand)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price and max_price:
        cars = cars.filter(price_per_day__gte=min_price, price_per_day__lte=max_price)

    seats = request.GET.get('seats')
    if seats:
        cars = cars.filter(seats=seats)

    # 🔹 คำนวณราคารวมตามจำนวนวัน
    pickup_date = request.GET.get('pickup_date')
    return_date = request.GET.get('return_date')
    total_days = 1  # ค่าเริ่มต้น = 1 วัน (กันข้อผิดพลาด)

    if pickup_date and return_date:
        try:
            pickup_date = datetime.strptime(pickup_date, "%Y-%m-%dT%H:%M")
            return_date = datetime.strptime(return_date, "%Y-%m-%dT%H:%M")
            total_days = max((return_date - pickup_date).days, 1)  # อย่างน้อยต้องมี 1 วัน
        except ValueError:
            pass  # ถ้าค่าไม่ถูกต้องจะไม่คำนวณ

    # 🔹 คำนวณราคาและเพิ่มฟิลด์ให้ `cars`
    for car in cars:
        car.total_price = car.price_per_day * total_days  # คำนวณราคารวม

    return render(request, "myapp/home.html", {
        'cars': cars,
        'brands': brands,  
        'seat_options': [2, 4, 7, 10],
        'total_days': total_days,
        'locations': locations,  # ✅ เพิ่มตรงนี้
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY
    })


   
# ✅ ฟังก์ชันเพิ่มรถ (เฉพาะแอดมิน)
@login_required
def add_car(request):
    if not is_admin(request.user):
        print(request.POST)
        messages.error(request, "❌ คุณไม่มีสิทธิ์เพิ่มรถ!")
        return redirect('home')

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "🚗 เพิ่มรถสำเร็จ!")
            return redirect(reverse('home'))
    else:
        form = CarForm()

    return render(request, 'myapp/add_car.html', {'form': form})


# ✅ ฟังก์ชันลบรถ (เฉพาะแอดมิน)
@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if not is_admin(request.user):
        messages.error(request, "❌ คุณไม่มีสิทธิ์ลบรถ!")
        return redirect('home')

    if request.method == 'POST':
        print(request.POST)
        car.delete()
        messages.success(request, "🚗 ลบรถสำเร็จ!")
        return redirect(reverse('admin_panel'))

    return render(request, 'myapp/delete_car.html', {'car': car})


# ✅ ฟังก์ชันแก้ไขข้อมูลรถ (เฉพาะแอดมิน)
@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if not is_admin(request.user):
        messages.error(request, "❌ คุณไม่มีสิทธิ์แก้ไขรถ!")
        return redirect('home')

    if request.method == 'POST':
        print(request.POST)
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ แก้ไขข้อมูลรถสำเร็จ!")
            return redirect(reverse('admin_panel'))
    else:
        form = CarForm(instance=car)

    return render(request, 'myapp/edit_car.html', {'form': form, 'car': car})


# ✅ ฟังก์ชันจองรถ
@login_required
def purchase(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    if request.method == "POST":
        rental_duration = request.POST.get("rental_duration")

        try:
            rental_days = max(float(rental_duration), 0.5)  # ✅ ใช้ float() แทน isdigit() และกำหนดขั้นต่ำ 0.5 วัน
            messages.success(request, f"✅ จองรถ {car.name} สำเร็จเป็นเวลา {rental_days} วัน! 🎉")
            return redirect("home")
        except ValueError:
            messages.error(request, "⚠️ กรุณาระบุระยะเวลาเช่าที่ถูกต้อง!")

    return render(request, "myapp/purchase.html", {"car": car})



# ✅ แผงควบคุมแอดมิน
@login_required
def admin_panel(request):
    if not is_admin(request.user):
        messages.error(request, "❌ คุณไม่มีสิทธิ์เข้าถึงหน้านี้!")
        return redirect('home')

    cars = Car.objects.all()
    users = UserProfile.objects.all()
    return render(request, 'myapp/admin_panel.html', {'cars': cars, 'users': users})


# ✅ แก้ไขข้อมูลสมาชิก (เฉพาะแอดมิน)
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if not is_admin(request.user):
        messages.error(request, "❌ คุณไม่มีสิทธิ์แก้ไขข้อมูลสมาชิก!")
        return redirect('home')

    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ แก้ไขข้อมูลสมาชิกสำเร็จ!")
            return redirect(reverse('admin_panel'))
    else:
        form = UserForm(instance=user)

    return render(request, 'myapp/edit_user.html', {'form': form, 'user': user})


# ✅ ลบสมาชิก (เฉพาะแอดมิน)
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)

    if not is_admin(request.user):
        messages.error(request, "❌ คุณไม่มีสิทธิ์ลบสมาชิก!")
        return redirect("home")

    if request.user == user.user:
        messages.error(request, "⚠️ คุณไม่สามารถลบบัญชีของตัวเองได้!")
        return redirect("admin_panel")

    if request.method == "POST":
        user.delete()
        messages.success(request, "🗑️ ลบสมาชิกสำเร็จ!")
        return redirect("admin_panel")

    return render(request, "myapp/delete_user.html", {"user": user})


@login_required
def car_rental_view(request):
    locations = [
        {"name": "สนามบินภูเก็ต", "latitude": 8.1132, "longitude": 98.3165},
        {"name": "ตัวเมืองภูเก็ต", "latitude": 7.8804, "longitude": 98.3923},
        {"name": "หาดกะตะ", "latitude": 7.8168, "longitude": 98.3031},
        {"name": "หาดกมลา", "latitude": 7.9527, "longitude": 98.2827},
        {"name": "หาดสุรินทร์", "latitude": 7.9813, "longitude": 98.2806},
        {"name": "หาดกะรน", "latitude": 7.8442, "longitude": 98.2933},
        {"name": "หาดในหาน", "latitude": 7.7750, "longitude": 98.3056},
        {"name": "หาดในทอน", "latitude": 8.0581, "longitude": 98.2752},
        {"name": "หาดในยาง", "latitude": 8.1100, "longitude": 98.3063},
        {"name": "ป่าตอง", "latitude": 7.8965, "longitude": 98.2982},
        {"name": "หาดราไวย์", "latitude": 7.7766, "longitude": 98.3285},
        {"name": "เชิงเลลากูน่า", "latitude": 8.0088, "longitude": 98.2966},
    ]

    context = {
        "locations": locations,
        "google_maps_api_key": settings.GOOGLE_MAPS_API_KEY,
    }
    
    print("📌 Context ที่ส่งไป:", context)  # ตรวจสอบค่าที่ส่งไปยัง Template
    
    return render(request, "myapp/car_rental.html", context)

# แสดงรายละเอียดรถ
def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)

    pickup_date = request.GET.get('pickup_date', request.session.get('pickup_date'))
    return_date = request.GET.get('return_date', request.session.get('return_date'))

    total_price = None
    if pickup_date and return_date:
        try:
            # ✅ เปลี่ยน str เป็น datetime
            pickup_date_obj = datetime.strptime(pickup_date, "%Y-%m-%dT%H:%M")
            return_date_obj = datetime.strptime(return_date, "%Y-%m-%dT%H:%M")

            rental_days = (return_date_obj - pickup_date_obj).days
            total_price = rental_days * car.price_per_day  # total_price เป็น Decimal

            # ✅ แปลง Decimal เป็น float ก่อนเก็บใน session
            request.session['pickup_date'] = pickup_date
            request.session['return_date'] = return_date
            request.session['total_price'] = float(total_price)  # 🔹 Fix JSON error
        except ValueError as e:
            print(f"❌ Error: {e}")  # Debugging

    return render(request, 'myapp/car_detail.html', {
        'car': car,
        'pickup_date': pickup_date,
        'return_date': return_date,
        'total_price': total_price
    })

# หน้าชำระเงินสำเร็จ (ใบเสร็จ)
def payment_success(request):
    return render(request, 'myapp/payment_success.html')

def confirm_booking(request):
    if request.method == 'POST':
        # ดำเนินการจอง เช่น บันทึกข้อมูล หรือประมวลผลการชำระเงิน
        return redirect('receipt')  # เปลี่ยนเป็นหน้าที่ต้องการไป
    return redirect('home')  # กรณีเปิด URL ตรง ๆ

def rental_form(request, car_id):
    car = get_object_or_404(Car, id=car_id)  # ✅ ค้นหารถจาก database
    context = {
        "car": car,
        "pickup_location": "สนามบินเชียงใหม่",
        "pickup_date": "07/02/2025",
        "pickup_time": "10:00 น.",
        "dropoff_location": "สนามบินเชียงใหม่",
        "dropoff_date": "09/02/2025",
        "dropoff_time": "10:00 น.",
        "rental_shop_name": "Local",
        "rental_shop_code": "C00325",
    }
    return render(request, "myapp/rental_form.html", context)


def store_rental_data(request):
    request.session['pickup_date'] = request.GET.get('pickup_date')
    request.session['return_date'] = request.GET.get('return_date')
    request.session['pickup_location'] = request.GET.get('pickup_location')
    request.session['total_price'] = request.GET.get('total_price')

def confirm_rental(request):
    if request.method == "POST":
        # เก็บค่าข้อมูลจากฟอร์มลง session
        request.session['rental_data'] = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'car_name': request.POST.get('car_name'),
            'pickup_date': request.POST.get('pickup_date'),
            'return_date': request.POST.get('return_date'),
            'total_price': request.POST.get('total_price'),
        }
        return redirect('receipt')  # ไปหน้าใบเสร็จ

    return render(request, "confirm.html")

def receipt_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    context = {
        "booking_id": booking.id,
        "car_name": booking.car.name if booking.car else "ไม่พบชื่อรถ",
        "first_name": booking.first_name,
        "last_name": booking.last_name,
        "email": booking.email,
        "phone": booking.phone,
        "pickup_location": booking.pickup_location,
        "return_location": booking.return_location,
        "pickup_date": booking.pickup_date,
        "return_date": booking.return_date,
        "total_price": booking.total_price,
    }
    return render(request, "myapp/receipt.html", context)