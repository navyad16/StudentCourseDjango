from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.course_list,name='home'),
    
    path('login/', views.login_view, name='login'),       
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('pay-now/', views.pay_now, name='pay_now'),

    path('my-orders/', views.my_orders,name='my_orders'),
    path('orders/', views.order_history, name='order_history'),

    # ADMIN
    path('staff/orders/', views.admin_orders, name='orders'),
    path('admin/update-order/<int:id>/', views.update_order),

    path('student/', include('core.student_urls')),  # ⭐ THIS IS STEP 4

    
]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
