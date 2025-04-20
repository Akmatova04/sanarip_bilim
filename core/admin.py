# core/admin.py (ТОЛУК ВЕРСИЯ - BlogPost кошулду)

from django.contrib import admin
from .models import Course, Resource, ContactMessage, BlogPost # BlogPost моделин импортко кошобуз
from django.utils.html import format_html # HTML тегдерди коопсуз форматтоо үчүн
from django.utils.text import Truncator # Узун текстти кыскартуу үчүн
from django.contrib.auth.models import User # BlogPost'то автор үчүн User модели керек

# --- КУРС МОДЕЛИ ҮЧҮН АДМИН ПАНЕЛЬ ---
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview', 'created_at', 'updated_at')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 80px; object-fit: cover;" />'.format(obj.image.url))
        return "-"
    image_tag.short_description = 'Сүрөтү'

    def image_preview(self, obj):
         if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 300px; object-fit: contain;" />'.format(obj.image.url))
         return "Сүрөт жүктөлгөн эмес"
    image_preview.short_description = 'Сүрөттүн көрүнүшү'

# --- РЕСУРС МОДЕЛИ ҮЧҮN АДМИН ПАНЕЛЬ ---
@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'added_at')
    search_fields = ('title', 'description', 'link')
    list_filter = ('added_at',)

# --- КАЙРЫЛУУ (БАЙЛАНЫШ) МОДЕЛИ ҮЧҮН АДМИН ПАНЕЛЬ ---
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'short_message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'message_display', 'created_at')

    def short_message(self, obj):
        return Truncator(obj.message).chars(70, truncate='...')
    short_message.short_description = 'Билдирүүсү (кыскача)'

    def message_display(self, obj):
        return format_html("<p>{}</p>", obj.message)
    message_display.short_description = "Толук билдирүү"

    def has_add_permission(self, request):
        return False

# --- БЛОГ ПОСТТОРУ ҮЧҮН АДМИН ПАНЕЛЬ ---
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'published_date_formatted') # Авторго шилтеме, форматталган дата
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    # Мазмунду редакциялоону ыңгайлуу кылуу үчүн (милдеттүү эмес)
    # fields = ('title', 'content', 'author', 'published_date', 'image') # Талаалардын тартиби
    # Админкадан пост кошуп жатканда авторду тандоо үчүн
    autocomplete_fields = ['author'] # Авторду издөө мүмкүнчүлүгүн кошот

    # Функциялар (Функционалдуулукту жакшыртуу үчүн)
    def author_link(self, obj):
        """Автордун атына басканда User админкасына өтүүчү шилтеме."""
        if obj.author:
            url = f"/admin/auth/user/{obj.author.pk}/change/" # Колдонуучуну түзөтүү барагына URL
            return format_html('<a href="{}">{}</a>', url, obj.author.get_full_name() or obj.author.username)
        return "-"
    author_link.short_description = 'Автору'
    author_link.admin_order_field = 'author' # Бул колонка боюнча сорттоо

    def published_date_formatted(self, obj):
        """Датаны ыңгайлуу форматта көрсөтөт."""
        return obj.published_date.strftime("%Y-%m-%d %H:%M") # Мисал формат: 2025-04-18 15:30
    published_date_formatted.short_description = 'Жарыяланган күнү'
    published_date_formatted.admin_order_field = 'published_date' # Бул колонка боюнча сорттоо

    # Постту админкадан сактаганда авторду автоматтык коюу
    def save_model(self, request, obj, form, change):
        """ Пост сакталып жатканда авторду текшерип, керек болсо учурдагы колдонуучуну коёт. """
        if not obj.author_id and request.user.is_authenticated: # Эгер автор жок болсо жана учурдагы колдонуучу админ болсо
            obj.author = request.user # Учурдагы админди автор кылуу
        super().save_model(request, obj, form, change) # Кадимки сактоо процесси