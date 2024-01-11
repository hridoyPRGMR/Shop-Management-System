from django.urls import path
from .views import home, profile,product,RegisterView,additem,delete_item,edit_item,update_item,sellitem,delete_sell,help,brand,vendor,order

urlpatterns = [
    path('', home, name='users-home'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('product/',product,name='product'),
    path('additem/',additem,name='users-additem'),
    path('delete_item/<int:myid>',delete_item,name='delete_item'),
    path('edit_item/<int:myid>',edit_item,name='edit_item'),
    path('update_item/<int:myid>',update_item,name='update_item'),
    path('sellitem/',sellitem,name='users-sellitem'),
    path('delete_sell/<int:myid>',delete_sell,name='delete_sell'),
    path('help/',help,name='help'),
    path('brand/',brand,name='brand'),
    path('vendor/',vendor,name='vendor'),
    path('order/',order,name='order'),
]
