# core/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Убакыт менен иштөө үчүн

# Курс модели
class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Аталышы") # Текст талаасы (макс. 200 символ)
    description = models.TextField(verbose_name="Сүрөттөмөсү", blank=True, null=True) # Чоң текст талаасы (милдеттүү эмес)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Түзүлгөн күнү") # Автоматтык түрдө кошулуучу дата/убакыт
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Жаңыланган күнү") # Автоматтык түрдө жаңыртылуучу дата/убакыт
    # is_active = models.BooleanField(default=True, verbose_name="Активдүүбү?") # Кошумча: Курсту көрсөтүү/жашыруу
    image = models.ImageField(
        upload_to='course_images/', 
        verbose_name="Сүрөтү", 
        blank=True, # Милдеттүү эмес кылуу
        null=True )  # Базада бош болушу мүмкүн
    def __str__(self):
        # Админ панелде жана башка жерлерде объекттин аталышын көрсөтүү үчүн
        return self.title 

    class Meta:
        verbose_name = "Курс"          # Моделдин жалгыз сандагы аталышы (админка үчүн)
        verbose_name_plural = "Курстар" # Моделдин көптүк сандагы аталышы (админка үчүн)
        ordering = ['title']          # Демейки сорттоо тартиби (аталышы боюнча)

# Ресурс модели
class Resource(models.Model):
    title = models.CharField(max_length=255, verbose_name="Аталышы")
    link = models.URLField(max_length=500, verbose_name="Шилтеме") # URL даректер үчүн талаа
    description = models.TextField(verbose_name="Сүрөттөмөсү", blank=True, null=True)
    added_at = models.DateTimeField(default=timezone.now, verbose_name="Кошулган күнү") # Белгилүү бир убакытты коюу

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Ресурс"
        verbose_name_plural = "Ресурстар"
        ordering = ['-added_at'] # Кошулган күнү боюнча тескери сорттоо (жаңылары үстүндө)
class ContactMessage(models.Model):
    name = models.CharField(max_length=150, verbose_name="Аты-жөнү")
    email = models.EmailField(verbose_name="Электрондук почтасы")
    message = models.TextField(verbose_name="Билдирүүсү")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Келген убактысы")
    is_read = models.BooleanField(default=False, verbose_name="Окулдубу?") # Админка үчүн

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        verbose_name = "Кайрылуу (Байланыш)"
        verbose_name_plural = "Кайрылуулар (Байланыш)"
        ordering = ['-created_at'] # Жаңылары үстүндө турушу үчүн
# Бул жерге Блог Посттору, Сабактар (Lessons) ж.б. моделдерди да кошсоңуз болот.
class BlogPost(models.Model):
    title = models.CharField(max_length=250, verbose_name="Аталышы")
    content = models.TextField(verbose_name="Мазмуну")
    published_date = models.DateTimeField(default=timezone.now, verbose_name="Жарыяланган күнү")
    # Авторду Django'нун User моделине байланыштыруу (жөнөкөй вариант)
    # null=True, blank=True - авторду көрсөтпөсө да болот
    # on_delete=models.SET_NULL - эгер автор өчүрүлсө, пост өчпөй, автору бош калат
    author = models.ForeignKey( User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автору")
    # Кошумча: Сүрөт үчүн талаа (кийин кошсок болот)
    # image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Сүрөтү")
    image = models.ImageField(
        upload_to='course_images/', 
        verbose_name="Сүрөтү", 
        blank=True, # Милдеттүү эмес кылуу
        null=True )
    def __str__(self):
        # Админкада посттун аталышын көрсөтөт
        return self.title

    class Meta:
        verbose_name = "Блог Посту"
        verbose_name_plural = "Блог Посттору"
        ordering = ['-published_date'] # Жаңылары үстүндө турушу үчүн