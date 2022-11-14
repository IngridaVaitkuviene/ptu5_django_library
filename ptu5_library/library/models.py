from django.db import models
import uuid
from django.utils.html import format_html
from django.urls import reverse

#id automatiskai susikuria, nereikia nurodyt
#models.Model tas pats, kas Base sqlalchemy
#models.CharField yra stringas, varchar'as
class Genre(models.Model):
    name = models.CharField('name', max_length=200, help_text="Enter the name of book genre")

    def __str__(self) -> str:
        return self.name

    def link_filtered_books(self):
        link = reverse('books')+'?genre_id='+str(self.id)
        return format_html('<a class="genre" href="{link}">{name}</a>', link=link, name=self.name)

class Author(models.Model):
    first_name = models.CharField('first name', max_length=50)
    last_name = models.CharField('last name', max_length=50)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def display_books(self) -> str:
        return ', '.join(book.title for book in self.books.all())
    # pakeitem stulpeliui pavadinima is display books i books
    display_books.short_description = 'books'

    def link(self) -> str:
        link = reverse('author', kwargs={'author_id': self.id})
        return format_html('<a href="{link}">{author}</a>', link=link, author=self.__str__())

    # klase kuri padeda aprasyti modelio klase, siuo atveju autoriui
    class Meta:
        ordering = ['last_name', 'first_name'] # rusiuoja pagal autoriaus pavarde
        verbose_name = "author"
        verbose_name_plural = "authors"

class Book(models.Model):
    title = models.CharField('title', max_length=255) #Charfield maximalus yra 255 ir privalomas max_length
    summary = models.TextField('summary') #Textfield neribojamas ilgis, tai max_length nereikia nurodyti
    isbn = models.CharField('ISBN', max_length=13, null=True, blank=True, 
        help_text='<a href="https://www.isbn-international.org/content/what-isbn" target="_blank">ISBN code</a> consisting of 13 symbols') #null=True duombazei, blank=True djangui,adminui
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='books', )
    # cascade - istrinant autoriu, istrins ir visas knygas(ziauriausias), 
    # protect-neleis istrinti autoriaus, jei jis tures knygu, 
    # set_null-autoriu padarys null ji istrynus, bet paliks knygas, 
    # do nothing (nerekomenduojamas) - ismes klaida, nes nieko nedaro
    genre = models.ManyToManyField(Genre, help_text='Choose genre(s) for this book', verbose_name='genre(s)') #verbose_name padaro kur reikia daugyskaita, vienaskaita, didziaja raide, mazaja
    cover = models.ImageField("cover", upload_to='covers', blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.author} - {self.title}"

    # cia class BookAdmin'ui
    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    # pakeitem stulpeliui pavadinima is display genre i genre(s)
    display_genre.short_description = 'genre(s)'

    # vietoj pvz <a href="{% url 'book' book.pk %}" pasidarom linka author_link
    def author_link(self) -> str:
        # reverse suformuoja adresa (link'a)
        link = reverse('author', kwargs={'author_id': self.author.id})
        return format_html('<a href="{link}">{author}</a>', link=link, author=self.author)

class BookInstance(models.Model):
    unique_id = models.UUIDField('unique ID', default=uuid.uuid4, editable=False) # uuid3 ir uuid5 reikia paduoti argumenta, uuid4 - random
    book = models.ForeignKey(Book, verbose_name='book', on_delete=models.CASCADE)
    due_back = models.DateField('due back', null=True, blank=True)

    LOAN_STATUS = (
        ('m', "managed"),
        ('t', "taken"),
        ('a', "available"),
        ('r', "reserved"),
    )
    
    status = models.CharField('status', max_length=1, choices=LOAN_STATUS, default='m')
    # price = models.DecimalField('price', max_digits=18, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.unique_id}: {self.book.title}"

    class Meta:
        ordering = ['due_back']