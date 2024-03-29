from django.urls import path, include
from . import  views

urlpatterns = [
    path('<int:pk>/', views.BookStoreDetail.as_view()),
    path('', views.BookStoreList.as_view(), name='bookstore_list'),
    path('register/', views.BookForm_Form.as_view(), name='bookstore_register_form'),
    path('get_book_info/<int:kwd>/', views.get_book_info, name="get_book_info"),
    # path('connecting_camera/', views.camera_reading(), name='connecting_camera'),
    path('bookstore/category/<str:slug>', views.category_page),
    path('send_bookstore_message/<int:pk>/', views.send_bookstore_message, name='send_bookstore_message'),
    path('bookstore_sold/<int:pk>', views.bookstore_sold, name='bookstore_sold')
]

