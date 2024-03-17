from django.contrib import admin

from .models import Faculty, Speciality, Gruppa, Student, Discipline, Schedule, Visit, Rating, News

# Добавление модели на главную страницу интерфейса администратора
admin.site.register(Faculty)
admin.site.register(Speciality)
admin.site.register(Gruppa)
admin.site.register(Student)
admin.site.register(Discipline)
admin.site.register(Schedule)
admin.site.register(Visit)
admin.site.register(Rating)
admin.site.register(News)



