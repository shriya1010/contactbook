from django.conf.urls import url
from contact_details_app import views
from django.urls import path

urlpatterns = [
    path('', views.login),
    path('index',views.index,name="index"),
    path('signup',views.signup,name="signup"),
    
    path('login',views.signup2,name="signup2"),


    path('api/contacts_list', views.contacts,name="contact"),
    path('api/contacts/<int:pk>/', views.contact),
    path('home',views.home,name="home"),
    path('searchfilter',views.searchfilter,name="searchfilter"),
    path('addcontact',views.addcontact,name="addcontact"),
    path('add',views.add,name="add"),
    path('delete/<int:pk>',views.delete,name="delete"),
    path('update/<int:pk>',views.update,name="update"),
    path('update_contact/<int:pk>',views.update_contact,name="update_contact"),
    path('mail/<int:pk>', views.mail, name="mail"),
    path('send/<int:pk>', views.send, name="send")

]
 