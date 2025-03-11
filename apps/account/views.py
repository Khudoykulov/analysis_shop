from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, View
from .form import UserRegisterForm, UserLoginForm


class RegisterView(View):
    form_class = UserRegisterForm  # Noto‘g‘ri yozilgan nom to‘g‘irlandi
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        """Ro‘yxatdan o‘tish sahifasini ko‘rsatish"""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        """Foydalanuvchini ro‘yxatdan o‘tkazish"""
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.is_active = True  # Foydalanuvchini aktiv qilish
            user.save()
            login(request, user)  # Foydalanuvchini avtomatik login qilish
            messages.success(request, 'Successfully registered')
            return redirect(reverse_lazy('main:index'))  # Login sahifasiga yo‘naltirish

        messages.error(request, 'Registration failed. Please check the form.')
        return render(request, self.template_name, {'form': form})  # Formani qayta chiqarish


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    return redirect('main:index')  # Change 'home' to your desired redirect URL
                else:
                    messages.error(request, 'Please activate your account first.')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


# def logout_view(request):
#     logout(request)
#     messages.success(request, 'You have been successfully logged out.')
#     return redirect('account:login')


def logout_view(request):
    if request.method == 'POST':
        if 'confirm_logout' in request.POST:  # Tasdiqlash tugmasi bosilganligini tekshirish
            logout(request)
            messages.success(request, 'Siz muvaffaqiyatli chiqdingiz!')
            return redirect('account:login')  # Logoutdan keyin bosh sahifaga yo‘naltirish
        else:
            return redirect('account:logout')  # Agar tasdiqlash bo‘lmasa, qayta shablonni ko‘rsatish
    else:
        if request.user.is_authenticated:  # Faqat login qilingan foydalanuvchilar uchun
            return render(request, 'logout.html')
        else:
            messages.error(request, 'Siz allaqachon chiqqansiz!')
            return redirect('main:index')
