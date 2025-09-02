from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.custom_login, name='custom_login'),
    path('register/', views.custom_register, name='custom_register'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/sales/', views.sales_management, name='sales_management'),
    path('dashboard/sales/revenue/', views.add_revenue, name='add_revenue'),
    path('dashboard/sales/expense/', views.add_expense, name='add_expense'),
    path('dashboard/sales/sale/<int:sale_id>/delete/', views.delete_sale, name='delete_sale'),
    path('dashboard/sales/sale/<int:sale_id>/edit/', views.edit_sale, name='edit_sale'),
    path('dashboard/sales/expense/<int:expense_id>/delete/', views.delete_expense, name='delete_expense'),
    path('dashboard/sales/expense/<int:expense_id>/edit/', views.edit_expense, name='edit_expense'),
    path('dashboard/costs/', views.cost_management, name='cost_management'),
    path('dashboard/costs/add/', views.add_cost, name='add_cost'),
    path('dashboard/costs/<int:cost_id>/delete/', views.delete_cost, name='delete_cost'),
    path('dashboard/profit/', views.profit_analysis, name='profit_analysis'),
    path('dashboard/users/', views.user_management, name='user_management'),
    path('dashboard/users/<int:user_id>/', views.user_detail, name='user_detail'),
    path('dashboard/users/<int:user_id>/edit/', views.user_edit, name='user_edit'),
    path('dashboard/users/<int:user_id>/delete/', views.user_delete, name='user_delete'),
    path('admin/', admin.site.urls),  # 保留 Django Admin 作為備用
]

# 靜態檔案和媒體檔案 URL
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
