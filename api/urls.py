from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import GetUpdateBookById, ListBooks

urlpatterns = [
    path('books/<int:id>', GetUpdateBookById.as_view(), name='get_book_by_id'),
    path('books', ListBooks.as_view(), name='list_books'),
]

urlpatterns = format_suffix_patterns(urlpatterns)