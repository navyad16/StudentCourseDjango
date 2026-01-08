from django.shortcuts import redirect
from .models import Student

def student_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        Student.objects.get_or_create(user=request.user)
        return view_func(request, *args, **kwargs)

    return wrapper
