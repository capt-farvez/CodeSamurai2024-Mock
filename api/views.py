from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Book
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status

class GetUpdateBookById(APIView):
    def get(self, request, id):
        book = get_object_or_404(Book, id=id)
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'price': book.price
        }
        return JsonResponse(book_data, status=status.HTTP_200_OK)

    def put(self, request, id):
        book = get_object_or_404(Book, id=id)

        try:
            data = json.loads(request.body)
            book.title = data.get('title', book.title)
            book.author = data.get('author', book.author)
            book.genre = data.get('genre', book.genre)
            book.price = data.get('price', book.price)
            book.save()

            return JsonResponse({
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'price': book.price
            }, status=status.HTTP_200_OK)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    

class ListBooks(APIView):
    def get(self, request):
        # Get query parameters
        search_field = request.query_params.get('search_field')
        value = request.query_params.get('value')
        sort_field = request.query_params.get('sort', 'id')
        order = request.query_params.get('order', 'ASC')

        # Filter and sort books
        books = self.filter_books(search_field, value, sort_field, order)

        # Serialize and return the response
        book_list = self.serialize_books(books)
        return JsonResponse({'books': book_list})

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            try:
                data = json.loads(request.body)
                new_book = Book.objects.create(
                    title=data.get('title'),
                    author=data.get('author'),
                    genre=data.get('genre'),
                    price=data.get('price')
                )
                return JsonResponse({
                    'id': new_book.id,
                    'title': new_book.title,
                    'author': new_book.author,
                    'genre': new_book.genre,
                    'price': new_book.price
                }, status=201)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON format'}, status=400)
            except KeyError as e:
                return JsonResponse({'error': f'Missing required field: {str(e)}'}, status=400)

        return JsonResponse({'error': 'Invalid request method'}, status=405)

def filter_books(self, search_field, value, sort_field, order):
    # Mapping fields to the corresponding model fields
    field_mapping = {
        'title': 'title',
        'author': 'author',
        'genre': 'genre',
    }

    # Validate search field
    if search_field not in field_mapping:
        raise ValueError("Invalid search field")

    # Filter books based on search criteria
    filter_kwargs = {f'{field_mapping[search_field]}__exact': value} if search_field else {}
    books = Book.objects.filter(**filter_kwargs).order_by(sort_field, 'id' if sort_field else 'id')

    # Apply sorting order
    if order == 'DESC':
        books = books.reverse()

    return books

def serialize_books(self, books):
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'price': book.price,
        }
        book_list.append(book_data)
    return book_list
