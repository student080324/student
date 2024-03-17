from django.db import models
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django import forms

from django.contrib.auth.models import User

# Модели отображают информацию о данных, с которыми вы работаете.
# Они содержат поля и поведение ваших данных.
# Обычно одна модель представляет одну таблицу в базе данных.
# Каждая модель это класс унаследованный от django.db.models.Model.
# Атрибут модели представляет поле в базе данных.
# Django предоставляет автоматически созданное API для доступа к данным

# choices (список выбора). Итератор (например, список или кортеж) 2-х элементных кортежей,
# определяющих варианты значений для поля.
# При определении, виджет формы использует select вместо стандартного текстового поля
# и ограничит значение поля указанными значениями.

# Читабельное имя поля (метка, label). Каждое поле, кроме ForeignKey, ManyToManyField и OneToOneField,
# первым аргументом принимает необязательное читабельное название.
# Если оно не указано, Django самостоятельно создаст его, используя название поля, заменяя подчеркивание на пробел.
# null - Если True, Django сохранит пустое значение как NULL в базе данных. По умолчанию - False.
# blank - Если True, поле не обязательно и может быть пустым. По умолчанию - False.
# Это не то же что и null. null относится к базе данных, blank - к проверке данных.
# Если поле содержит blank=True, форма позволит передать пустое значение.
# При blank=False - поле обязательно.


# Факультеты
class Faculty(models.Model):
    title = models.CharField(_('faculty_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'faculty'
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{}".format(self.title)

# Специальности 
class Speciality(models.Model):
    cipher = models.CharField(_('speciality_cipher'), max_length=32, unique=True)
    title = models.CharField(_('speciality_title'), max_length=256)
    faculty = models.ForeignKey(Faculty, related_name='speciality_faculty', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'speciality'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['faculty', 'title']),
        ]
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{} - {}".format(self.cipher, self.title)

# Группа 
class Gruppa(models.Model):
    cipher = models.CharField(_('gruppa_cipher'), max_length=32, unique=True)
    speciality = models.ForeignKey(Speciality, related_name='gruppa_speciality', on_delete=models.CASCADE)
    language = models.CharField(_('language'), max_length=32)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'gruppa'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['cipher', 'speciality']),
        ]
        # Сортировка по умолчанию
        ordering = ['cipher']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{} - {}".format(self.cipher, self.speciality)

# Студенты 
class Student(models.Model):
    SEX_CHOICES = (
        ('М','М'),
        ('Ж', 'Ж'),
    )    
    full_name = models.CharField(_('full_name'), max_length=128)
    sex = models.CharField(_('sex'), max_length=1, choices=SEX_CHOICES, default='М')
    iin = models.CharField(_('iin'), unique=True, max_length=12)
    birthday = models.DateTimeField(_('birthday'))
    phone = models.CharField(_('phone'), max_length=64)    
    address = models.CharField(_('address'), max_length=96)    
    gruppa = models.ForeignKey(Gruppa, related_name='student_gruppa', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'student'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['full_name']),
            models.Index(fields=['gruppa']),
        ]
        # Сортировка по умолчанию
        ordering = ['full_name']
    def __str__(self):
        # Вывод в тег Select 
        return "{}, {}".format(self.full_name, self.gruppa)

# Учебные дисциплины
class Discipline(models.Model):
    title = models.CharField(_('discipline_title'), max_length=128, unique=True)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'discipline'
        # Сортировка по умолчанию
        ordering = ['title']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{}".format(self.title)

# Расписание 
class Schedule(models.Model):
    dates = models.DateTimeField(_('dates'))
    discipline = models.ForeignKey(Discipline, related_name='schedule_discipline', on_delete=models.CASCADE)
    gruppa = models.ForeignKey(Gruppa, related_name='gruppa', on_delete=models.CASCADE)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'schedule'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['discipline']),
            models.Index(fields=['gruppa']),
        ]
        # Сортировка по умолчанию
        ordering = ['discipline']
    def __str__(self):
        # Вывод названия в тег SELECT 
        return "{} - {}".format(self.dates.strftime('%d.%m.%Y %H:%M'), self.discipline)

# Посещение 
class Visit(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='visit_schedule', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='visit_student', on_delete=models.CASCADE)
    visited = models.BooleanField(_('visited'), default = False)
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'visit'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['schedule']),
            models.Index(fields=['student']),
        ]
        # Сортировка по умолчанию
        ordering = ['schedule']
    def __str__(self):
        # Вывод в тег Select 
        return "{}, {} - {}".format(self.schedule, self.student, self.visited)

# Успеваемость 
class Rating(models.Model):
    dater = models.DateTimeField(_('dater'))
    course = models.IntegerField(_('course'))
    semester = models.IntegerField(_('semester'))
    discipline = models.ForeignKey(Discipline, related_name='rating_discipline', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='rating_student', on_delete=models.CASCADE)
    value = models.IntegerField(_('value'))
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'rating'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['dater']),
            models.Index(fields=['discipline']),
            models.Index(fields=['student']),
        ]
        # Сортировка по умолчанию
        ordering = ['dater']
    def __str__(self):
        # Вывод в тег Select 
        return "{}: {}, {} - {}".format(self.dater, self.discipline, self.student, self.value)

# Новости 
class News(models.Model):
    daten = models.DateTimeField(_('daten'))
    title = models.CharField(_('news_title'), max_length=256)
    details = models.TextField(_('news_details'))
    photo = models.ImageField(_('news_photo'), upload_to='images/', blank=True, null=True)    
    class Meta:
        # Параметры модели
        # Переопределение имени таблицы
        db_table = 'news'
        # indexes - список индексов, которые необходимо определить в модели
        indexes = [
            models.Index(fields=['daten']),
        ]
        # Сортировка по умолчанию
        ordering = ['daten']
