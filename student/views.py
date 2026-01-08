from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Order, Student
from core.decorators import student_required

@login_required
@student_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    enrolled = Order.objects.filter(student=student, paid=True)
    return render(request, 'student/dashboard.html', {'enrolled': enrolled})

