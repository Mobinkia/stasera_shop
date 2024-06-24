from django.urls import path
from . import views
urlpatterns = [
    path('', views.store,name='store'),
    path('cart/', views.cart,name='cart'),
    path('checkout/', views.checkout,name='checkout'),
    path('login/', views.login_page,name='login'),
    path('signup/', views.signup,name='signup'),
    path('logout/', views.logout_page,name='logout'),
    path('update_item/', views.updateItem,name='update_item'),
    path('history/', views.history,name='history'),
    path('profile/', views.profile,name='profile'),
    path('products/', views.products,name='products'),
    path('panel/', views.panel,name='panel'),
    
]
