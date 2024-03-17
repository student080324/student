from django import forms
from django.forms import ModelForm, TextInput, Textarea, DateInput, NumberInput, DateTimeInput, CheckboxInput
from .models import Faculty, Speciality, Gruppa, Student, Discipline, Schedule, Visit, Rating, News
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
import pytz

# При разработке приложения, использующего базу данных, чаще всего необходимо работать с формами, которые аналогичны моделям.
# В этом случае явное определение полей формы будет дублировать код, так как все поля уже описаны в модели.
# По этой причине Django предоставляет вспомогательный класс, который позволит вам создать класс Form по имеющейся модели
# атрибут fields - указание списка используемых полей, при fields = '__all__' - все поля
# атрибут widgets для указания собственный виджет для поля. Его значением должен быть словарь, ключами которого являются имена полей, а значениями — классы или экземпляры виджетов.

# Категория товара
class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('faculty_title'),            
        }
    # Метод-валидатор для поля title
    #def clean_title(self):
    #    data = self.cleaned_data['title']
    #    # Ошибка если начинается не с большой буквы
    #    if data.istitle() == False:
    #        raise forms.ValidationError(_('Value must start with a capital letter'))
    #    # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
    #    return data

# Специальности
class SpecialityForm(forms.ModelForm):
    class Meta:
        model = Speciality
        fields = ('cipher', 'title', 'faculty')
        widgets = {
            'cipher': TextInput(attrs={"size":"50"}),
            'title': TextInput(attrs={"size":"100"}),
            'faculty': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'faculty': _('faculty_title'),            
        }

# Специальности
class GruppaForm(forms.ModelForm):
    class Meta:
        model = Gruppa
        fields = ('cipher', 'speciality', 'language')
        widgets = {
            'cipher': TextInput(attrs={"size":"50"}),
            'speciality': forms.Select(attrs={'class': 'chosen'}),
            'language': TextInput(attrs={"size":"50"}),
        }
        labels = {
            'speciality': _('speciality_title'),            
        }

# Студенты
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('full_name', 'sex', 'iin', 'birthday', 'phone', 'address', 'gruppa')
        widgets = {
            'full_name': TextInput(attrs={"size":"100"}),
            'iin': TextInput(attrs={"size":"50"}),
            'birthday': DateInput(attrs={"type":"date"}),
            'phone': TextInput(attrs={"size":"40", "type":"tel", "pattern": "+7-[0-9]{3}-[0-9]{3}-[0-9]{4}"}),
            'address': TextInput(attrs={"size":"100"}),
            'gruppa': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'gruppa': _('gruppa_cipher'),            
        }
    # Метод-валидатор для поля birthday
    def clean_birthday(self):        
        if isinstance(self.cleaned_data['birthday'], datetime.date) == True:
            data = self.cleaned_data['birthday']
            # Проверка даты рождения не моложе 16 лет
            if data > timezone.now() - relativedelta(years=16):
                raise forms.ValidationError(_('Minimum age 16 years old'))
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Категория товара
class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = ['title',]
        widgets = {
            'title': TextInput(attrs={"size":"100"}),            
        }
        labels = {
            'title': _('discipline_title'),            
        }

# Расписание
class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('dates', 'discipline', 'gruppa')
        widgets = {
            'dates': DateInput(format='%d/%m/%Y %H:%M:%S'),
            'discipline': forms.Select(attrs={'class': 'chosen'}),
            'gruppa': forms.Select(attrs={'class': 'chosen'}),
        }
        labels = {
            'discipline': _('discipline_title'),            
            'gruppa': _('gruppa_cipher'),            
        }
    # Метод-валидатор для поля dates
    def clean_dates(self):        
        if isinstance(self.cleaned_data['dates'], datetime.date) == True:
            data = self.cleaned_data['dates']
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Посещение
class VisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ('schedule', 'student', 'visited')
        widgets = {
            'schedule': forms.Select(attrs={'class': 'chosen'}),
            'student': forms.Select(attrs={'class': 'chosen'}),
            'visited' : CheckboxInput(),
        }
        labels = {
            'schedule': _('schedule'),            
            'student': _('student'),            
        }

# Посещение
class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('dater', 'course', 'semester', 'discipline', 'student', 'value')
        widgets = {
            'dater': DateInput(attrs={"type":"date"}),
            'course': NumberInput(attrs={"size":"10", "min": "1", "max": "6", "step": "1"}),
            'semester': NumberInput(attrs={"size":"10", "min": "1", "max": "2", "step": "1"}),
            'discipline': forms.Select(attrs={'class': 'chosen'}),
            'student': forms.Select(attrs={'class': 'chosen'}),
            'value': NumberInput(attrs={"size":"10", "min": "1", "max": "5", "step": "1"}),
        }
        labels = {
            'discipline': _('discipline'),            
            'student': _('student'),            
        }
    # Метод-валидатор для поля dater
    def clean_dater(self):        
        if isinstance(self.cleaned_data['dater'], datetime.date) == True:
            data = self.cleaned_data['dater']
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data    

# Новости
class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('daten', 'title', 'details', 'photo')
        widgets = {
            'daten': DateTimeInput(format='%d/%m/%Y %H:%M:%S'),
            'title': TextInput(attrs={"size":"100"}),
            'details': Textarea(attrs={'cols': 100, 'rows': 10}),                        
        }
    # Метод-валидатор для поля daten
    def clean_daten(self):        
        if isinstance(self.cleaned_data['daten'], datetime.date) == True:
            data = self.cleaned_data['daten']
            #print(data)        
        else:
            raise forms.ValidationError(_('Wrong date and time format'))
        # Метод-валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
        return data   

# Форма регистрации
class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
