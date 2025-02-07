from django import forms
from django.contrib.auth.models import User  # ✅ นำเข้า User
from django.contrib.auth.forms import UserCreationForm
from .models import Car, UserProfile, Booking

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'brand', 'seats', 'price_per_day', 'image', 'description', 'type', 'model', 'year']

class UserForm(forms.ModelForm):
    class Meta:
        model = User  # ✅ เปลี่ยนจาก UserProfile -> User
        fields = ['username', 'email']  # ✅ ฟิลด์จาก Django User

class UserProfileForm(forms.ModelForm):  # ✅ เพิ่มฟอร์มสำหรับ UserProfile
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'profile_picture']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    display_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ["username", "email", "display_name", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            UserProfile.objects.create(user=user, display_name=self.cleaned_data["display_name"])
        return user
    
class BookingForm(forms.ModelForm):
        class Meta:
            model = Booking
            fields = ['car', 'pickup_location', 'dropoff_location', 'pickup_date', 'dropoff_date', 'full_name', 'email', 'phone']
            widgets = {
                'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ชื่อจริง'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'อีเมล'}),
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'เบอร์โทรศัพท์'}),
            }