from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('author/<int:author_id>/', views.author, name='author'),
    path('books/', views.BooklistView.as_view(), name='books'),
    # pk - primary key
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book'),
    path('my_books/', views.UserBookListView.as_view(), name='user_books'),
    path('borrow_new_book/', views.UserBookInstanceCreateView.as_view(), name='user_bookinstance_create'),
]