from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance
from django.views.generic import ListView, DetailView


# Create your views here.

def index(request):
    # return HttpResponse("Sveiki atvykę!")
    book_count = Book.objects.count()
    book_instance_count = BookInstance.objects.count()
    book_instance_available_count = BookInstance.objects.filter(status='a').count()
    author_count = Author.objects.count()

    context = {
        'book_count': book_count,
        'book_instance_count': book_instance_count,
        'book_instance_available_count': book_instance_available_count,
        'author_count': author_count,
        'genre_count':Genre.objects.count()
    }

    return render(request, 'library/index.html', context)

def authors(request):
    return render(request, 'library/authors.html', {'authors': Author.objects.all()})

def author(request, author_id):
    return render(request, 'library/author.html', {'author': get_object_or_404(Author, id=author_id)})

class BooklistView(ListView):
    model = Book
    template_name = 'library/book_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['books_count'] = Book.objects.count()
        context['books_count'] = self.get_queryset().count()
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            context['genre'] = get_object_or_404(Genre, id=genre_id)
        return context


class BookDetailView(DetailView):
    model = Book
    template_name = 'library/book_detail.html'