from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

router = DefaultRouter()
router.register(r'users', api_views.UserViewSet)
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'products', api_views.ProductViewSet)
router.register(r'transactions', api_views.TransactionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('categories/', views.categories, name='categories'),
    path('edit_product/<int:pid>/', views.edit_product, name='edit_product'),
    
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
]
