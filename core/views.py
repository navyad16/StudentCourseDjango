from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Student, Course, Order, Category
from .decorators import student_required
from django.contrib import messages


# ================= HOME =================
def home(request):
    # 🔍 SEARCH
    query = request.GET.get('q', '')

    # 🎯 CATEGORY FILTER
    selected_category = request.GET.get('category', 'all')

    courses = Course.objects.all()
    categories = Category.objects.all()

    # ✅ SEARCH BY TITLE
    if query:
        courses = courses.filter(title__icontains=query)

    # ✅ FILTER BY CATEGORY
    if selected_category != 'all':
        courses = courses.filter(category_id=selected_category)

    enrolled_ids = []
    cart_ids = []

    # ✅ AUTHENTICATED USER LOGIC
    if request.user.is_authenticated:
        student, _ = Student.objects.get_or_create(user=request.user)

        enrolled_ids = Order.objects.filter(
            student=student,
            paid=True
        ).values_list('course_id', flat=True)

        cart_ids = Order.objects.filter(
            student=student,
            paid=False
        ).values_list('course_id', flat=True)

    return render(request, 'core/home.html', {
        'courses': courses,
        'categories': categories,
        'query': query,                     # 🔥 UPDATED
        'selected_category': selected_category,
        'enrolled_course_ids': enrolled_ids,
        'cart_course_ids': cart_ids
    })



# ================= AUTH =================
def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        phone = request.POST.get('phone')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        Student.objects.create(user=user, phone=phone)

        messages.success(request, "Registration successful")
        return redirect('login')

    return render(request, 'core/register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_staff:
                return redirect('orders')          # ✅ ADMIN
            else:
                return redirect('student_dashboard')  # ✅ STUDENT

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')



# ================= COURSES =================
def course_list(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    courses = Course.objects.all()
    categories = Category.objects.all()

    if query:
        courses = courses.filter(title__icontains=query)

    if selected_category:
        courses = courses.filter(category_id=selected_category)

    return render(request, 'core/course_list.html', {
        'courses': courses,
        'categories': categories,
        'query': query,
        'selected_category': selected_category
    })



# ================= CART =================
@login_required
def add_to_cart(request, id):
    course = get_object_or_404(Course, id=id)
    student, _ = Student.objects.get_or_create(user=request.user)

    # 🚫 Already purchased
    if Order.objects.filter(
        student=student,
        course=course,
        paid=True
    ).exists():
        messages.warning(request, "You already purchased this course.")
        return redirect('home')

    # ✅ Add to cart OR get existing one
    order, created = Order.objects.get_or_create(
        student=student,
        course=course,
        paid=False,
        defaults={
            'amount': course.price   # ✅ REQUIRED FIELD
        }
    )

    if not created:
        messages.info(request, "Course already in your cart.")
    else:
        messages.success(request, "Course added to cart.")

    return redirect('cart')


@login_required
def cart(request):
    student, _ = Student.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(
        student=student,
        paid=False
    ).select_related('course')

    total = sum(order.course.price for order in orders)

    return render(request, 'core/cart.html', {
        'orders': orders,
        'total': total
    })

@login_required
def pay_now(request):
    student, _ = Student.objects.get_or_create(user=request.user)

    Order.objects.filter(
        student=student,
        paid=False
    ).update(paid=True)

    return redirect('my_courses')



@login_required
@student_required
def my_orders(request):
    student = Student.objects.get(user=request.user)
    orders = Order.objects.filter(student=student, paid=True)
    return render(request, 'core/my_orders.html', {'orders': orders})


# ================= ADMIN =================
@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'core/adminpanel/orders.html', {'orders': orders})


@staff_member_required
def update_order(request, id):
    order = get_object_or_404(Order, id=id)
    if request.method == "POST":
        order.paid = 'paid' in request.POST
        order.save()
    return redirect('admin_orders')


@login_required
def student_dashboard(request):
    student, _ = Student.objects.get_or_create(user=request.user)

    enrolled_courses = Order.objects.filter(
        student=student,
        paid=True
    ).select_related('course')

    return render(request, 'core/student_dashboard.html', {
        'enrolled_courses': enrolled_courses
    })



@login_required
def my_courses(request):
    student, _ = Student.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(
        student=student,
        paid=True
    ).select_related('course')

    return render(request, 'core/my_courses.html', {
        'orders': orders
    })


@login_required
def order_history(request):
    student, _ = Student.objects.get_or_create(user=request.user)

    orders = Order.objects.filter(
        student=student,
        paid=True
    ).select_related('course').order_by('-id')

    return render(request, 'core/order_history.html', {
        'orders': orders
    })
