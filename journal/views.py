from django.shortcuts import render, redirect

# Класс HttpResponse из пакета django.http, который позволяет отправить текстовое содержимое.
from django.http import HttpResponse, HttpResponseNotFound
# Конструктор принимает один обязательный аргумент – путь для перенаправления. Это может быть полный URL (например, 'https://www.yahoo.com/search/') или абсолютный путь без домена (например, '/search/').
from django.http import HttpResponseRedirect

from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages

from django.db.models import Max
from django.db.models import Q

from datetime import datetime, timedelta

# Отправка почты
from django.core.mail import send_mail

# Подключение моделей
from .models import Faculty, Speciality, Gruppa, Student, Discipline, Schedule, Visit, Rating, News
# Подключение форм
from .forms import FacultyForm, SpecialityForm, GruppaForm, StudentForm, DisciplineForm, ScheduleForm, VisitForm, RatingForm, NewsForm, SignUpForm

from django.db.models import Sum

from django.db import models

import sys

import math

#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _

from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.contrib.auth import login as auth_login

from django.db.models.query import QuerySet

import csv
import xlwt
from io import BytesIO

# Create your views here.
# Групповые ограничения
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated:
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups, login_url='403')

###################################################################################################

# Стартовая страница 
def index(request):
    try:
        schedule = Schedule.objects.all().order_by('-dates')[0:15]
        news14 = News.objects.all().order_by('-daten')[0:4]
        return render(request, "index.html", {"schedule": schedule, "news14": news14, })            
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)    

# Контакты
def contact(request):
    try:
        return render(request, "contact.html")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################
# Отчеты
@login_required
@group_required("Managers")
def report_index(request):
    try:        
        return render(request, "report/index.html")        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 1
@login_required
@group_required("Managers")
def report_1(request):
    try:
        # Группы (для поиска)
        gruppa = Gruppa.objects.all().order_by('cipher')
        selected_item_gruppa = ""
        if 'searchBtn' in request.POST:
            start_date = request.POST.get("start_date")
            print(start_date)
            finish_date = request.POST.get("finish_date")
            finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
            print(finish_date)
            # Расписание
            schedule = Schedule.objects.filter(dates__range=[start_date, finish_date]).order_by('dates')
            # Поиск по группе
            selected_item_gruppa = request.POST.get('item_gruppa')
            print(selected_item_gruppa)
            if selected_item_gruppa != '-----':
                gruppa_query = Gruppa.objects.filter(cipher = selected_item_gruppa).only('id').all()
                schedule = schedule.filter(gruppa_id__in = gruppa_query).all()
            finish_date = request.POST.get("finish_date")            
        else:
            start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
            finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59).strftime('%Y-%m-%d') 
            # Расписание
            schedule = Schedule.objects.all().order_by('dates')
        return render(request, "report/report_1.html", {"schedule": schedule, "start_date": start_date, "finish_date": finish_date, "gruppa": gruppa, "selected_item_gruppa": selected_item_gruppa})        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 2
@login_required
@group_required("Managers")
def report_2(request):
    try:
        # Группы (для поиска)
        gruppa = Gruppa.objects.all().order_by('cipher')
        selected_item_gruppa = ""
        if 'searchBtn' in request.POST:
            start_date = request.POST.get("start_date")
            print(start_date)
            finish_date = request.POST.get("finish_date")
            finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
            print(finish_date)
            # Расписание
            schedule = Schedule.objects.filter(dates__range=[start_date, finish_date]).order_by('dates')
            # Поиск по группе
            selected_item_gruppa = request.POST.get('item_gruppa')
            print(selected_item_gruppa)
            if selected_item_gruppa != '-----':
                gruppa_query = Gruppa.objects.filter(cipher = selected_item_gruppa).only('id').all()
                schedule_query = schedule.filter(gruppa_id__in = gruppa_query).all()
            else:
                schedule_query = Schedule.objects.only('id').filter(dates__range=[start_date, finish_date])
            # Посещение
            visit = Visit.objects.filter(schedule_id__in = schedule_query).all().order_by('-schedule__dates', 'student__full_name')
            finish_date = request.POST.get("finish_date")            
        else:
            start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
            finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59).strftime('%Y-%m-%d') 
            # Посещение
            visit = Visit.objects.all().order_by('-schedule__dates', 'student__full_name')
        return render(request, "report/report_2.html", {"visit": visit, "start_date": start_date, "finish_date": finish_date, "gruppa": gruppa, "selected_item_gruppa": selected_item_gruppa})        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Отчет 3
@login_required
@group_required("Managers")
def report_3(request):
    try:
        # Группы (для поиска)
        gruppa = Gruppa.objects.all().order_by('cipher')
        selected_item_gruppa = ""
        if 'searchBtn' in request.POST:
            start_date = request.POST.get("start_date")
            print(start_date)
            finish_date = request.POST.get("finish_date")
            finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
            print(finish_date)            
            # Успеваемость
            rating = Rating.objects.filter(dater__range=[start_date, finish_date]).order_by('dater')
            # Поиск по группе
            selected_item_gruppa = request.POST.get('item_gruppa')
            print(selected_item_gruppa)
            if selected_item_gruppa != '-----':
                gruppa_query = Gruppa.objects.filter(cipher = selected_item_gruppa).only('id').all()
                student_query = Student.objects.filter(gruppa_id__in = gruppa_query).only('id').all()
                rating = rating.filter(student_id__in = student_query).order_by('dater', 'student__full_name')
            else:
                rating = Rating.objects.filter(dater__range=[start_date, finish_date]).order_by('dater', 'student__full_name')
            finish_date = request.POST.get("finish_date")
        else:
            start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
            finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59).strftime('%Y-%m-%d') 
            # Оценки
            rating = Rating.objects.all().order_by('dater', 'student__full_name')
        return render(request, "report/report_3.html", {"rating": rating, "start_date": start_date, "finish_date": finish_date, "gruppa": gruppa, "selected_item_gruppa": selected_item_gruppa})        
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)


###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def faculty_index(request):
    try:
        faculty = Faculty.objects.all().order_by('title')
        return render(request, "faculty/index.html", {"faculty": faculty,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def faculty_create(request):
    try:
        if request.method == "POST":
            faculty = Faculty()
            faculty.title = request.POST.get("title")
            facultyform = FacultyForm(request.POST)
            if facultyform.is_valid():
                faculty.save()
                return HttpResponseRedirect(reverse('faculty_index'))
            else:
                return render(request, "faculty/create.html", {"form": facultyform})
        else:        
            facultyform = FacultyForm()
            return render(request, "faculty/create.html", {"form": facultyform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def faculty_edit(request, id):
    try:
        faculty = Faculty.objects.get(id=id)
        if request.method == "POST":
            faculty.title = request.POST.get("title")
            facultyform = FacultyForm(request.POST)
            if facultyform.is_valid():
                faculty.save()
                return HttpResponseRedirect(reverse('faculty_index'))
            else:
                return render(request, "faculty/edit.html", {"form": facultyform})
        else:
            # Загрузка начальных данных
            facultyform = FacultyForm(initial={'title': faculty.title, })
            return render(request, "faculty/edit.html", {"form": facultyform})
    except Faculty.DoesNotExist:
        return HttpResponseNotFound("<h2>Faculty not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def faculty_delete(request, id):
    try:
        faculty = Faculty.objects.get(id=id)
        faculty.delete()
        return HttpResponseRedirect(reverse('faculty_index'))
    except Faculty.DoesNotExist:
        return HttpResponseNotFound("<h2>Faculty not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def faculty_read(request, id):
    try:
        faculty = Faculty.objects.get(id=id) 
        return render(request, "faculty/read.html", {"faculty": faculty})
    except Faculty.DoesNotExist:
        return HttpResponseNotFound("<h2>Faculty not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def speciality_index(request):
    try:
        speciality = Speciality.objects.all().order_by('title')
        return render(request, "speciality/index.html", {"speciality": speciality,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def speciality_create(request):
    try:
        if request.method == "POST":
            speciality = Speciality()
            speciality.cipher = request.POST.get("cipher")
            speciality.title = request.POST.get("title")
            speciality.faculty = Faculty.objects.filter(id=request.POST.get("faculty")).first()
            specialityform = SpecialityForm(request.POST)
            if specialityform.is_valid():
                speciality.save()
                return HttpResponseRedirect(reverse('speciality_index'))
            else:
                return render(request, "speciality/create.html", {"form": specialityform})
        else:        
            specialityform = SpecialityForm()
            return render(request, "speciality/create.html", {"form": specialityform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def speciality_edit(request, id):
    try:
        speciality = Speciality.objects.get(id=id)
        if request.method == "POST":
            speciality.cipher = request.POST.get("cipher")
            speciality.title = request.POST.get("title")
            speciality.faculty = Faculty.objects.filter(id=request.POST.get("faculty")).first()
            specialityform = SpecialityForm(request.POST)
            if specialityform.is_valid():
                speciality.save()
                return HttpResponseRedirect(reverse('speciality_index'))
            else:
                return render(request, "speciality/edit.html", {"form": specialityform})
        else:
            # Загрузка начальных данных
            specialityform = SpecialityForm(initial={'cipher': speciality.cipher, 'title': speciality.title, 'faculty': speciality.faculty, })
            return render(request, "speciality/edit.html", {"form": specialityform})
    except Speciality.DoesNotExist:
        return HttpResponseNotFound("<h2>Speciality not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def speciality_delete(request, id):
    try:
        speciality = Speciality.objects.get(id=id)
        speciality.delete()
        return HttpResponseRedirect(reverse('speciality_index'))
    except Speciality.DoesNotExist:
        return HttpResponseNotFound("<h2>Speciality not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def speciality_read(request, id):
    try:
        speciality = Speciality.objects.get(id=id) 
        return render(request, "speciality/read.html", {"speciality": speciality})
    except Speciality.DoesNotExist:
        return HttpResponseNotFound("<h2>Speciality not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def gruppa_index(request):
    try:
        gruppa = Gruppa.objects.all().order_by('cipher')
        return render(request, "gruppa/index.html", {"gruppa": gruppa,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def gruppa_create(request):
    try:
        if request.method == "POST":
            gruppa = Gruppa()
            gruppa.cipher = request.POST.get("cipher")
            gruppa.speciality = Speciality.objects.filter(id=request.POST.get("speciality")).first()
            gruppa.language = request.POST.get("language")            
            gruppaform = GruppaForm(request.POST)
            if gruppaform.is_valid():
                gruppa.save()
                return HttpResponseRedirect(reverse('gruppa_index'))
            else:
                return render(request, "gruppa/create.html", {"form": gruppaform})
        else:        
            gruppaform = GruppaForm()
            return render(request, "gruppa/create.html", {"form": gruppaform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def gruppa_edit(request, id):
    try:
        gruppa = Gruppa.objects.get(id=id)
        if request.method == "POST":
            gruppa.cipher = request.POST.get("cipher")
            gruppa.speciality = Speciality.objects.filter(id=request.POST.get("speciality")).first()
            gruppa.language = request.POST.get("language") 
            gruppaform = GruppaForm(request.POST)
            if gruppaform.is_valid():
                gruppa.save()
                return HttpResponseRedirect(reverse('gruppa_index'))
            else:
                return render(request, "gruppa/edit.html", {"form": gruppaform})
        else:
            # Загрузка начальных данных
            gruppaform = GruppaForm(initial={'cipher': gruppa.cipher, 'speciality': gruppa.speciality, 'language': gruppa.language, })
            return render(request, "gruppa/edit.html", {"form": gruppaform})
    except Gruppa.DoesNotExist:
        return HttpResponseNotFound("<h2>Gruppa not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def gruppa_delete(request, id):
    try:
        gruppa = Gruppa.objects.get(id=id)
        gruppa.delete()
        return HttpResponseRedirect(reverse('gruppa_index'))
    except Gruppa.DoesNotExist:
        return HttpResponseNotFound("<h2>Gruppa not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def gruppa_read(request, id):
    try:
        gruppa = Gruppa.objects.get(id=id) 
        return render(request, "gruppa/read.html", {"gruppa": gruppa})
    except Gruppa.DoesNotExist:
        return HttpResponseNotFound("<h2>Gruppa not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)
    
###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def student_index(request):
    try:
        student = Student.objects.all().order_by('full_name')
        return render(request, "student/index.html", {"student": student,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def student_create(request):
    try:
        if request.method == "POST":
            student = Student()
            student.full_name = request.POST.get("full_name")
            student.sex = request.POST.get("sex")
            student.iin = request.POST.get("iin")
            student.birthday = request.POST.get("birthday")
            student.phone = request.POST.get("phone")
            student.address = request.POST.get("address")
            student.email = request.POST.get("email")
            student.gruppa = Gruppa.objects.filter(id=request.POST.get("gruppa")).first()
            studentform = StudentForm(request.POST)
            if studentform.is_valid():
                student.save()
                return HttpResponseRedirect(reverse('student_index'))
            else:
                return render(request, "student/create.html", {"form": studentform})
        else:        
            studentform = StudentForm(initial={ 'birthday': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "student/create.html", {"form": studentform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def student_edit(request, id):
    try:
        student = Student.objects.get(id=id)
        if request.method == "POST":
            student.full_name = request.POST.get("full_name")
            student.sex = request.POST.get("sex")
            student.iin = request.POST.get("iin")
            student.birthday = request.POST.get("birthday")
            student.phone = request.POST.get("phone")
            student.address = request.POST.get("address")
            student.email = request.POST.get("email")
            student.gruppa = Gruppa.objects.filter(id=request.POST.get("gruppa")).first()
            studentform = StudentForm(request.POST)
            if studentform.is_valid():
                student.save()
                return HttpResponseRedirect(reverse('student_index'))
            else:
                return render(request, "student/edit.html", {"form": studentform})
        else:
            # Загрузка начальных данных
            studentform = StudentForm(initial={'full_name': student.full_name, 'sex': student.sex, 'iin': student.iin, 'birthday': student.birthday.strftime('%Y-%m-%d'), 'phone': student.phone, 'address': student.address, 'email': student.email, 'gruppa': student.gruppa, })
            return render(request, "student/edit.html", {"form": studentform})
    except Student.DoesNotExist:
        return HttpResponseNotFound("<h2>Student not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def student_delete(request, id):
    try:
        student = Student.objects.get(id=id)
        student.delete()
        return HttpResponseRedirect(reverse('student_index'))
    except Student.DoesNotExist:
        return HttpResponseNotFound("<h2>Student not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def student_read(request, id):
    try:
        student = Student.objects.get(id=id) 
        return render(request, "student/read.html", {"student": student})
    except Student.DoesNotExist:
        return HttpResponseNotFound("<h2>Student not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def discipline_index(request):
    try:
        discipline = Discipline.objects.all().order_by('title')
        return render(request, "discipline/index.html", {"discipline": discipline,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def discipline_create(request):
    try:
        if request.method == "POST":
            discipline = Discipline()
            discipline.title = request.POST.get("title")
            disciplineform = DisciplineForm(request.POST)
            if disciplineform.is_valid():
                discipline.save()
                return HttpResponseRedirect(reverse('discipline_index'))
            else:
                return render(request, "discipline/create.html", {"form": disciplineform})
        else:        
            disciplineform = DisciplineForm()
            return render(request, "discipline/create.html", {"form": disciplineform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def discipline_edit(request, id):
    try:
        discipline = Discipline.objects.get(id=id)
        if request.method == "POST":
            discipline.title = request.POST.get("title")
            disciplineform = DisciplineForm(request.POST)
            if disciplineform.is_valid():
                discipline.save()
                return HttpResponseRedirect(reverse('discipline_index'))
            else:
                return render(request, "discipline/edit.html", {"form": disciplineform})
        else:
            # Загрузка начальных данных
            disciplineform = DisciplineForm(initial={'title': discipline.title, })
            return render(request, "discipline/edit.html", {"form": disciplineform})
    except Discipline.DoesNotExist:
        return HttpResponseNotFound("<h2>Discipline not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def discipline_delete(request, id):
    try:
        discipline = Discipline.objects.get(id=id)
        discipline.delete()
        return HttpResponseRedirect(reverse('discipline_index'))
    except Discipline.DoesNotExist:
        return HttpResponseNotFound("<h2>Discipline not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def discipline_read(request, id):
    try:
        discipline = Discipline.objects.get(id=id) 
        return render(request, "discipline/read.html", {"discipline": discipline})
    except Discipline.DoesNotExist:
        return HttpResponseNotFound("<h2>Discipline not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def schedule_index(request):
    try:
        schedule = Schedule.objects.all().order_by('-dates')
        return render(request, "schedule/index.html", {"schedule": schedule,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
#@login_required
#@group_required("Managers")
def schedule_list(request):
   try:
        # Группы (для поиска)
        gruppa = Gruppa.objects.all().order_by('cipher')
        selected_item_gruppa = '-----' 
        if 'searchBtn' in request.POST:
            start_date = request.POST.get("start_date")
            print(start_date)
            finish_date = request.POST.get("finish_date")
            finish_date = str(datetime.strptime(finish_date, "%Y-%m-%d") + timedelta(days=1))
            print(finish_date)
            # Расписание
            schedule = Schedule.objects.filter(dates__range=[start_date, finish_date]).order_by('dates')
            finish_date = request.POST.get("finish_date")
            # Поиск по группе
            selected_item_gruppa = request.POST.get('item_gruppa')
            print(selected_item_gruppa)
            if selected_item_gruppa != '-----':
                gruppa_query = Gruppa.objects.filter(cipher = selected_item_gruppa).only('id').all()
                schedule = schedule.filter(gruppa_id__in = gruppa_query).all()
        else:
            start_date = datetime(datetime.now().year, 1, 1, 0, 0).strftime('%Y-%m-%d') 
            finish_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 23, 59).strftime('%Y-%m-%d') 
            # Расписание
            schedule = Schedule.objects.all().order_by('dates')
        return render(request, "schedule/list.html", {"schedule": schedule, "start_date": start_date, "finish_date": finish_date, "gruppa": gruppa, "selected_item_gruppa": selected_item_gruppa})   
   except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def schedule_create(request):
    try:
        if request.method == "POST":
            schedule = Schedule()
            schedule.dates = request.POST.get("dates")
            schedule.discipline = Discipline.objects.filter(id=request.POST.get("discipline")).first()
            schedule.gruppa = Gruppa.objects.filter(id=request.POST.get("gruppa")).first()
            scheduleform = ScheduleForm(request.POST)
            if scheduleform.is_valid():
                schedule.save()
                return HttpResponseRedirect(reverse('schedule_index'))
            else:
                return render(request, "schedule/create.html", {"form": scheduleform})
        else:        
            scheduleform = ScheduleForm(initial={ 'dates': datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            return render(request, "schedule/create.html", {"form": scheduleform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def schedule_edit(request, id):
    try:
        schedule = Schedule.objects.get(id=id)
        if request.method == "POST":
            schedule.dates = request.POST.get("dates")
            schedule.discipline = Discipline.objects.filter(id=request.POST.get("discipline")).first()
            schedule.gruppa = Gruppa.objects.filter(id=request.POST.get("gruppa")).first()
            scheduleform = ScheduleForm(request.POST)
            if scheduleform.is_valid():
                schedule.save()
                return HttpResponseRedirect(reverse('schedule_index'))
            else:
                return render(request, "schedule/edit.html", {"form": scheduleform})
        else:
            # Загрузка начальных данных
            scheduleform = ScheduleForm(initial={'dates': schedule.dates.strftime('%Y-%m-%d %H:%M:%S'), 'discipline': schedule.discipline, 'gruppa': schedule.gruppa, })
            return render(request, "schedule/edit.html", {"form": scheduleform})
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("<h2>Schedule not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def schedule_delete(request, id):
    try:
        schedule = Schedule.objects.get(id=id)
        schedule.delete()
        return HttpResponseRedirect(reverse('schedule_index'))
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("<h2>Schedule not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def schedule_read(request, id):
    try:
        schedule = Schedule.objects.get(id=id) 
        return render(request, "schedule/read.html", {"schedule": schedule})
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("<h2>Schedule not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Посещение для этого расписания
@login_required
@group_required("Managers")
def schedule_visit(request, id):
    try:
        # Расписание
        #print(id)
        schedule = Schedule.objects.get(id=id) 
        # Группа
        #print(schedule.gruppa_id)
        gruppa = Gruppa.objects.get(id=schedule.gruppa_id)
        # Студенты данной группы
        #print(gruppa.id)
        student = Student.objects.filter(gruppa_id=gruppa.id).order_by('full_name')
        # Проверить есть ли для этого раписания записи в таблице посещений
        visit_count = Visit.objects.filter(schedule_id=schedule.id).count()
        print("visit_count ", visit_count)
        # Если посещения есть для этого рапсиания - переход на изменение страницы с посещениями
        if (visit_count!=0):    
            return HttpResponseRedirect(reverse('visit_index'))  
        # Иначе вводим посщения для этого занятия
        if request.method == "POST":
            # Считать со страницы значения checkbox
            dictionary_checkbox = {}
            for key, value in request.POST.items():
                if key != 'csrfmiddlewaretoken':
                    if key != 'save_btn':
                        if key != 'back_btn':
                            dictionary_checkbox.update({key:value})
                #print(f'Key: {key}')
                #print(f'Value: {value}')
            # Это отмеченные id из таблицы student
            for key in dictionary_checkbox:
                #print(key,dictionary_checkbox[key])
                print(key[4:])
            # Перебрать всех студентов и для отмеченных поставить True а не отмечнных False
            visit = Visit()
            for s in student:
                print(s.full_name)                 
                print(s.id)                 
                parameters = [id, s.id, dictionary_checkbox.get("cbox" + str(s.id), False)]
                insert_visit(parameters)
            return HttpResponseRedirect(reverse('schedule_index'))          
        else:        
            return render(request, "schedule/visit.html", {"schedule": schedule, "gruppa": gruppa, "student": student})
    except Schedule.DoesNotExist:
        return HttpResponseNotFound("<h2>Schedule not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Добавить Посещение 
def insert_visit(param):   
    visit = Visit()
    visit.schedule_id = param[0]   
    visit.student_id = param[1]  
    if param[2]==False: 
        visit.visited = False  
    else:
        visit.visited = True  
    print(str(visit))
    visit.save()
    return
###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def visit_index(request):
    try:
        visit = Visit.objects.all().order_by('schedule').order_by('-schedule__dates')
        return render(request, "visit/index.html", {"visit": visit,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
@login_required
def visit_list(request):
    try:
        student_query = Student.objects.filter(email = request.user.email).only('id').all()
        visit = Visit.objects.filter(student_id__in = student_query).all().order_by('-schedule__dates')
        #visit = Visit.objects.all().order_by('schedule')
        return render(request, "visit/list.html", {"visit": visit,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def visit_create(request):
    try:
        if request.method == "POST":
            visit = Visit()
            visit.schedule = Schedule.objects.filter(id=request.POST.get("schedule")).first()
            visit.student = Student.objects.filter(id=request.POST.get("student")).first()
            if (request.POST.get("visited") == 'on'):
                visit.visited = True
            else:
                visit.visited = False
            visitform = VisitForm(request.POST)
            if visitform.is_valid():
                visit.save()
                return HttpResponseRedirect(reverse('visit_index'))
            else:
                return render(request, "visit/create.html", {"form": visitform})
        else:        
            visitform = VisitForm()
            return render(request, "visit/create.html", {"form": visitform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def visit_edit(request, id):
    try:
        visit = Visit.objects.get(id=id)
        if request.method == "POST":
            visit.schedule = Schedule.objects.filter(id=request.POST.get("schedule")).first()
            visit.student = Student.objects.filter(id=request.POST.get("student")).first()
            if (request.POST.get("visited") == 'on'):
                visit.visited = True
            else:
                visit.visited = False
            visitform = VisitForm(request.POST)
            if visitform.is_valid():
                visit.save()
                return HttpResponseRedirect(reverse('visit_index'))
            else:
                return render(request, "visit/edit.html", {"form": visitform})
        else:
            # Загрузка начальных данных
            visitform = VisitForm(initial={'schedule': visit.schedule, 'student': visit.student, 'visited': visit.visited, })
            return render(request, "visit/edit.html", {"form": visitform})
    except Visit.DoesNotExist:
        return HttpResponseNotFound("<h2>Visit not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def visit_delete(request, id):
    try:
        visit = Visit.objects.get(id=id)
        visit.delete()
        return HttpResponseRedirect(reverse('visit_index'))
    except Visit.DoesNotExist:
        return HttpResponseNotFound("<h2>Visit not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def visit_read(request, id):
    try:
        visit = Visit.objects.get(id=id) 
        return render(request, "visit/read.html", {"visit": visit})
    except Visit.DoesNotExist:
        return HttpResponseNotFound("<h2>Visit not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def rating_index(request):
    try:
        rating = Rating.objects.all().order_by('dater')
        return render(request, "rating/index.html", {"rating": rating,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для изменения с кнопками создать, изменить, удалить
@login_required
def rating_list(request):
    try:
        student_query = Student.objects.filter(email = request.user.email).only('id').all()
        rating = Rating.objects.filter(student_id__in = student_query).all()
        #rating = Rating.objects.all().order_by('dater')
        return render(request, "rating/list.html", {"rating": rating,})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def rating_create(request):
    try:
        if request.method == "POST":
            rating = Rating()
            rating.dater = request.POST.get("dater")
            rating.course = request.POST.get("course")
            rating.semester = request.POST.get("semester")
            rating.discipline = Discipline.objects.filter(id=request.POST.get("discipline")).first()
            rating.student = Student.objects.filter(id=request.POST.get("student")).first()
            rating.value = request.POST.get("value")
            ratingform = RatingForm(request.POST)
            if ratingform.is_valid():
                rating.save()
                return HttpResponseRedirect(reverse('rating_index'))
            else:
                return render(request, "rating/create.html", {"form": ratingform})
        else:        
            ratingform = RatingForm(initial={ 'dater': datetime.now().strftime('%Y-%m-%d')})
            return render(request, "rating/create.html", {"form": ratingform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
@login_required
@group_required("Managers")
def rating_edit(request, id):
    try:
        rating = Rating.objects.get(id=id)
        if request.method == "POST":
            rating.dater = request.POST.get("dater")
            rating.course = request.POST.get("course")
            rating.semester = request.POST.get("semester")
            rating.discipline = Discipline.objects.filter(id=request.POST.get("discipline")).first()
            rating.student = Student.objects.filter(id=request.POST.get("student")).first()
            rating.value = request.POST.get("value")
            ratingform = RatingForm(request.POST)
            if ratingform.is_valid():
                rating.save()
                return HttpResponseRedirect(reverse('rating_index'))
            else:
                return render(request, "rating/edit.html", {"form": ratingform})
        else:
            # Загрузка начальных данных
            ratingform = RatingForm(initial={'dater': rating.dater.strftime('%Y-%m-%d'), 'course': rating.course, 'semester': rating.semester, 'discipline': rating.discipline, 'student': rating.student, 'value': rating.value, })
            return render(request, "rating/edit.html", {"form": ratingform})
    except Rating.DoesNotExist:
        return HttpResponseNotFound("<h2>Rating not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def rating_delete(request, id):
    try:
        rating = Rating.objects.get(id=id)
        rating.delete()
        return HttpResponseRedirect(reverse('rating_index'))
    except Rating.DoesNotExist:
        return HttpResponseNotFound("<h2>Rating not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
@login_required
@group_required("Managers")
def rating_read(request, id):
    try:
        rating = Rating.objects.get(id=id) 
        return render(request, "rating/read.html", {"rating": rating})
    except Rating.DoesNotExist:
        return HttpResponseNotFound("<h2>Rating not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Список для изменения с кнопками создать, изменить, удалить
@login_required
@group_required("Managers")
def news_index(request):
    try:
        news = News.objects.all().order_by('-daten')
        return render(request, "news/index.html", {"news": news})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Список для просмотра
def news_list(request):
    try:
        news = News.objects.all().order_by('-daten')
        if request.method == "POST":
            # Определить какая кнопка нажата
            if 'searchBtn' in request.POST:
                # Поиск по названию 
                news_search = request.POST.get("news_search")
                #print(news_search)                
                if news_search != '':
                    news = news.filter(Q(title__contains = news_search) | Q(details__contains = news_search)).all()                
                return render(request, "news/list.html", {"news": news, "news_search": news_search, })    
            else:          
                return render(request, "news/list.html", {"news": news})                 
        else:
            return render(request, "news/list.html", {"news": news}) 
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# В функции create() получаем данные из запроса типа POST, сохраняем данные с помощью метода save()
# и выполняем переадресацию на корень веб-сайта (то есть на функцию index).
@login_required
@group_required("Managers")
def news_create(request):
    try:
        if request.method == "POST":
            news = News()        
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if 'photo' in request.FILES:                
                news.photo = request.FILES['photo']   
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/create.html", {"form": newsform})
        else:        
            newsform = NewsForm(initial={'daten': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), })
            return render(request, "news/create.html", {"form": newsform})
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Функция edit выполняет редактирование объекта.
# Функция в качестве параметра принимает идентификатор объекта в базе данных.
@login_required
@group_required("Managers")
def news_edit(request, id):
    try:
        news = News.objects.get(id=id) 
        if request.method == "POST":
            news.daten = request.POST.get("daten")
            news.title = request.POST.get("title")
            news.details = request.POST.get("details")
            if "photo" in request.FILES:                
                news.photo = request.FILES["photo"]
            newsform = NewsForm(request.POST)
            if newsform.is_valid():
                news.save()
                return HttpResponseRedirect(reverse('news_index'))
            else:
                return render(request, "news/edit.html", {"form": newsform})
        else:
            # Загрузка начальных данных
            newsform = NewsForm(initial={'daten': news.daten.strftime('%Y-%m-%d %H:%M:%S'), 'title': news.title, 'details': news.details, 'photo': news.photo })
            return render(request, "news/edit.html", {"form": newsform})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Удаление данных из бд
# Функция delete аналогичным функции edit образом находит объет и выполняет его удаление.
@login_required
@group_required("Managers")
def news_delete(request, id):
    try:
        news = News.objects.get(id=id)
        news.delete()
        return HttpResponseRedirect(reverse('news_index'))
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

# Просмотр страницы read.html для просмотра объекта.
#@login_required
def news_read(request, id):
    try:
        news = News.objects.get(id=id) 
        return render(request, "news/read.html", {"news": news})
    except News.DoesNotExist:
        return HttpResponseNotFound("<h2>News not found</h2>")
    except Exception as exception:
        print(exception)
        return HttpResponse(exception)

###################################################################################################

# Регистрационная форма 
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
            #return render(request, 'registration/register_done.html', {'new_user': user})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# Изменение данных пользователя
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'registration/my_account.html'
    success_url = reverse_lazy('index')
    #success_url = reverse_lazy('my_account')
    def get_object(self):
        return self.request.user

# Выход
from django.contrib.auth import logout
def logoutUser(request):
    logout(request)
    return render(request, "index.html")

