
from django.urls import path
from . import views

app_name = 'book'

urlpatterns = [
   path('<int:book_id>/', views.bookDetail, name='detail'),
   path('',views.openMap, name='map'),
]