# core/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout # logout кошулду
from django.db import IntegrityError
# BlogPost моделиңизди туура импорт кылыңыз:
from .models import Course, Resource, ContactMessage, BlogPost

# --- Башкы бет ---
def index_view(request):
    try:
        latest_courses = Course.objects.all().order_by('-created_at')[:3]
    except Exception as e:
        print(f"Башкы бет үчүн курстарды алууда ката: {e}")
        latest_courses = []
    context = {'page_title': 'Башкы бет', 'latest_courses': latest_courses}
    return render(request, 'core/index.html', context)

# --- Биз жөнүндө ---
def about_view(request):
    context = {'page_title': 'Биз жөнүндө'}
    return render(request, 'core/about.html', context)

# --- Курстар ---
def courses_view(request):
    try:
        all_courses = Course.objects.all().order_by('title')
    except Exception as e:
        print(f"Курстарды алууда ката: {e}")
        all_courses = []
    context = {'page_title': 'Биздин Курстар', 'courses': all_courses}
    return render(request, 'core/courses.html', context)

# --- Курстун деталдуу барагы ---
def course_detail_view(request, pk):
    course = get_object_or_404(Course, pk=pk)
    context = {'page_title': course.title, 'course': course}
    return render(request, 'core/course_detail.html', context)

# --- Ресурстар ---
def resources_view(request):
    try:
        all_resources = Resource.objects.all().order_by('-added_at')
    except Exception as e:
        print(f"Ресурстарды алууда ката: {e}")
        all_resources = []
    context = {'page_title': 'Пайдалуу Ресурстар', 'resources': all_resources}
    return render(request, 'core/resources.html', context)

# --- БЛОГ ПОСТТОРУНУН ТИЗМЕСИ ---
def blog_view(request):
    """ Бардык блог постторун жарыяланган күнү боюнча иреттеп көрсөтөт. """
    try:
        all_posts = BlogPost.objects.all().order_by('-published_date')
    except Exception as e:
        print(f"Блог постторун алууда ката: {e}")
        all_posts = []
    context = {
        'page_title': 'Биздин Блог',
        'posts': all_posts # Шаблонго 'posts' деген ат менен жөнөтүү
    }
    return render(request, 'core/blog.html', context)

# --- БЛОГ ПОСТУНУН ДЕТАЛДУУ БАРАГЫ (ЖАҢЫ ФУНКЦИЯ) ---
def post_detail_view(request, pk):
    """ Белгилүү бир посттун деталдуу барагын көрсөтөт. """
    post = get_object_or_404(BlogPost, pk=pk)
    context = {
        'page_title': post.title,
        'post': post
    }
    # Бул үчүн өзүнчө шаблон керек болот ('core/post_detail.html')
    return render(request, 'core/post_detail.html', context)
# ----------------------------------------------------

# --- Суроо-Жооп ---
def faq_view(request):
    context = {'page_title': 'Суроо-Жооп'}
    return render(request, 'core/faq.html', context)

# --- Байланыш ---
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_text = request.POST.get('message')
        if not all([name, email, message_text]):
             messages.error(request, 'Сураныч, бардык талааларды толтуруңуз.')
             return redirect('contact')
        try:
            ContactMessage.objects.create(name=name, email=email, message=message_text)
            messages.success(request, 'Сиздин билдирүүңүз ийгиликтүү жөнөтүлдү!')
            return redirect('contact')
        except Exception as e:
            print(f"Кайрылууну сактоодо ката: {e}")
            messages.error(request, 'Ката кетти! Билдирүүңүз жөнөтүлгөн жок.')
            return redirect('contact')
    context = {'page_title': 'Биз менен байланышыңыз'}
    return render(request, 'core/contact.html', context)

# --- Катталуу ---
def register_view(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if not all([fullname, email, password, confirm_password]):
             messages.error(request, 'Сураныч, бардык талааларды толтуруңуз.')
             context = {'page_title': 'Аккаунт түзүү', 'email': email, 'fullname': fullname}
             return render(request, 'core/register.html', context)
        if password != confirm_password:
            messages.error(request, 'Сырсөздөр дал келген жок!')
            context = {'page_title': 'Аккаунт түзүү', 'email': email, 'fullname': fullname}
            return render(request, 'core/register.html', context)
        if len(password) < 8:
             messages.error(request, 'Сырсөз кеминде 8 символдон турушу керек.')
             context = {'page_title': 'Аккаунт түзүү', 'email': email, 'fullname': fullname}
             return render(request, 'core/register.html', context)
        if User.objects.filter(username=email).exists():
             messages.error(request, 'Бул электрондук почта дареги мурунтан эле катталган.')
             context = {'page_title': 'Аккаунт түзүү', 'fullname': fullname}
             return render(request, 'core/register.html', context)
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.first_name = fullname.strip()
            user.save()
            login(request, user)
            messages.success(request, f"Кош келиңиз, {user.first_name}! Сиз ийгиликтүү катталдыңыз.")
            return redirect('index')
        except IntegrityError:
             messages.error(request, 'Бул электрондук почта дареги катталган (IntegrityError).')
             context = {'page_title': 'Аккаунт түзүү', 'fullname': fullname}
             return render(request, 'core/register.html', context)
        except Exception as e:
            print(f"Каттоодо күтүлбөгөн ката: {e}")
            messages.error(request, 'Каттоо учурунда белгисиз ката кетти.')
            context = {'page_title': 'Аккаунт түзүү', 'email': email, 'fullname': fullname}
            return render(request, 'core/register.html', context)
    context = {'page_title': 'Аккаунт түзүү'}
    return render(request, 'core/register.html', context)

# --- Кирүү ---
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if not all([email, password]):
             messages.error(request, 'Email жана сырсөздү киргизиңиз.')
             return redirect('login')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Кош келиңиз, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
        else:
            messages.error(request, 'Email же сырсөз туура эмес.')
            context = {'page_title': 'Сайтка кирүү', 'email': email}
            return render(request, 'core/login.html', context)
    context = {'page_title': 'Сайтка кирүү'}
    return render(request, 'core/login.html', context)

# --- Чыгуу ---
def logout_view(request):
    logout(request)
    messages.info(request, "Сиз системадан ийгиликтүү чыктыңыз.")
    return redirect('index')