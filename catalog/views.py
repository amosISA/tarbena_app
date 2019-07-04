from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()
    num_authors = Author.objects.count()
    list_genre = Genre.objects.all()
    num_genre = list_genre.count()
    libros_castillo = Book.objects.all().filter(title__icontains='castillo')
    return render(
        request,
        'index.html',
        context = {
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_available':num_instances_available,
            'num_authors':num_authors,
            'list_genre':list_genre,
            'num_genre': num_genre,
            'libros_castillo': libros_castillo,
                   }
    )

from django.views import generic

class BookListView(generic.ListView):
    model = Book
