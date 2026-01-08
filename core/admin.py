from django.contrib import admin
from .models import Course, Category, Order, Student


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'category')
    search_fields = ('title',)
    list_filter = ('category',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'amount', 'paid', 'created_at')
    list_filter = ('paid',)
    search_fields = ('student__user__username', 'course__title')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user',)
