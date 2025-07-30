from .forms import ApplicationForm
from .models import Application
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    application, created = Application.objects.get_or_create(user=request.user, defaults={
        'email': request.user.email,
        'full_name': request.user.get_full_name() or request.user.username,
        'project_title': '',
        'cycle': '',
    })
    if request.method == 'POST':
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            return render(request, 'core/profile.html', {
                'form': form,
                'application': application,
                'user': request.user,
                'success': True
            })
    else:
        form = ApplicationForm(instance=application)
    return render(request, 'core/profile.html', {
        'form': form,
        'application': application,
        'user': request.user
    })
def logout_view(request):
    auth_logout(request)
    return redirect('home')
from django.shortcuts import render

# Create your views here.

from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Home page
def home(request):
    return render(request, 'core/home.html')

# Register page
def register(request):
    from django.contrib.auth.models import User
    from django import forms
    class CustomRegisterForm(forms.ModelForm):
        password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
        password2 = forms.CharField(label='Re-enter Password', widget=forms.PasswordInput)
        class Meta:
            model = User
            fields = ['username', 'email']
        def clean_password2(self):
            password1 = self.cleaned_data.get('password1')
            password2 = self.cleaned_data.get('password2')
            if password1 and password2 and password1 != password2:
                raise forms.ValidationError("Passwords don't match")
            return password2
        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password1'])
            user.is_active = False  # Not active until 'verified'
            if commit:
                user.save()
            return user

    show_verification_message = False
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Simulate verification: set a flag in session
            request.session['verified_user_id'] = user.id
            show_verification_message = True
            return render(request, 'core/register.html', {'form': form, 'show_verification_message': show_verification_message})
    else:
        form = CustomRegisterForm()
    return render(request, 'core/register.html', {'form': form})
def register_confirm(request):
    # Simulate verification: set user as active
    from django.contrib.auth.models import User
    user_id = request.session.get('verified_user_id')
    if user_id:
        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            del request.session['verified_user_id']
        except User.DoesNotExist:
            pass
    return render(request, 'core/register_confirm.html')

# Login page
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required
def dashboard(request):
    application, created = Application.objects.get_or_create(user=request.user, defaults={
        'email': request.user.email,
        'full_name': request.user.get_full_name() or request.user.username,
        'project_title': '',
        'cycle': '',
    })
    progress = 0
    if request.method == 'POST':
        if 'full_name' in request.POST and 'email' in request.POST:
            application.full_name = request.POST.get('full_name', '')
            application.email = request.POST.get('email', '')
            application.phone = request.POST.get('phone', '')
            application.address = request.POST.get('address', '')
            application.save()
        if 'project_title' in request.POST:
            application.project_title = request.POST.get('project_title', '')
            application.supervisor = request.POST.get('supervisor', '')
            application.save()
        if 'cycle' in request.POST:
            application.cycle = request.POST.get('cycle', '')
            application.save()
    if application.full_name and application.email:
        progress += 33
    if application.project_title:
        progress += 33
    if application.cycle:
        progress += 34
    application.progress = progress
    application.save()
    next_steps = [
        'Complete personal information',
        'Enter project details',
        'Specify fellowship cycle/year',
        'Upload required documents (CV, PhD certificate, publications) once available',
        'Request reference letters after saving above details',
        'Submit your application',
    ]
    useful_links = [
        {'name': 'IIA Official Fellowship Guidelines', 'url': 'https://www.iiap.res.in/opportunities/fellowships'},
        {'name': 'Contact Email', 'url': 'mailto:fellowships@iiap.res.in'},
        {'name': 'Previous Year Fellowship Results', 'url': 'https://www.iiap.res.in/opportunities/results'},
    ]
    context = {
        'user_name': request.user.get_username(),
        'application': application,
        'next_steps': next_steps,
        'useful_links': useful_links,
    }
    return render(request, 'core/dashboard.html', context)

# About page
def about(request):
    return render(request, 'core/about.html')
