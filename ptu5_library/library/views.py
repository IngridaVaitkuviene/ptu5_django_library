from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Genre, Author, Book, BookInstance
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from .forms import BookReviewForm
from django.urls import reverse, reverse_lazy
from django.contrib import messages


def index(request):
    # return HttpResponse("Sveiki atvykę!")
    book_count = Book.objects.count()
    book_instance_count = BookInstance.objects.count()
    book_instance_available_count = BookInstance.objects.filter(status='a').count()
    author_count = Author.objects.count()
    # kiek kartu sesijoje apsilankeme
    visits_count = request.session.get('visits_count', 1)
    request.session['visits_count'] = visits_count + 1

    context = {
        'book_count': book_count,
        'book_instance_count': book_instance_count,
        'book_instance_available_count': book_instance_available_count,
        'author_count': author_count,
        'genre_count':Genre.objects.count(),
        'visits_count': visits_count,
    }

    return render(request, 'library/index.html', context)

def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    return render(request, 'library/authors.html', {'authors': paged_authors})

def author(request, author_id):
    return render(request, 'library/author.html', {'author': get_object_or_404(Author, id=author_id)})

class BooklistView(ListView):
    model = Book
    # tiek rodo lape knygu Books sarase
    paginate_by = 4
    template_name = 'library/book_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            # Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės didžiosios/mažosios
            queryset = queryset.filter(Q(title__icontains=search)| Q(summary__icontains=search))
        genre_id = self.request.GET.get('genre_id')
        if genre_id:
            queryset = queryset.filter(genre__id=genre_id)
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['books_count'] = Book.objects.count()
        context['books_count'] = self.get_queryset().count()
        genre_id = self.request.GET.get('genre_id')
        context['genres'] = Genre.objects.all
        if genre_id:
            context['genre'] = get_object_or_404(Genre, id=genre_id)
        return context


class BookDetailView(FormMixin, DetailView):
    model = Book
    template_name = 'library/book_detail.html'
    form_class = BookReviewForm

    def get_success_url(self):
        return reverse('book', kwargs={'pk': self.get_object().id})

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            messages.error(self.request, 'Youre posting too much!')
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.book = self.get_object()
        form.instance.reader = self.request.user
        form.save()
        messages.success(self.request, 'Your review has been posted')
        return super().form_valid(form)

    def get_initial(self):
        return {
            'book': self.get_object(),
            'reader': self.request.user,
        }


class UserBookListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'library/user_book_list.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(reader=self.request.user).order_by('due_back')
        return queryset

# klasese turim naudoti ne reverse, o reverse_lazy
class UserBookInstanceCreateView(LoginRequiredMixin, CreateView):
    model = BookInstance
    fields = ('book', 'due_back', )
    template_name = 'library/user_bookinstance_create.html'
    success_url = reverse_lazy('user_books')

    def form_valid(self, form):
        form.instance.reader = self.request.user
        form.instance.status = 'r'
        return super().form_valid(form)