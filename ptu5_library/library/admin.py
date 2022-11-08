from django.contrib import admin
from . import models

class BookInstanceInline(admin.TabularInline):
    model = models.BookInstance
    extra = 0
    readonly_fields = ('unique_id', )
    can_delete = False

# pasipildem admino aplinkoj ties Books skilpim stulpeliais title, author 
# stulpeliu pavadinimai turi sutapti su modelio pavadinimais
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = (BookInstanceInline, )

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'book', 'status', 'due_back')
    list_filter = ('status', 'due_back')
    # grazina id rodyma, bet neduoda redaguoti
    readonly_fields = ('unique_id', )

# tuples tuplese. Atskyrem i general: knygos id ir pati knyga, ir availability: knygos statusa ir kalendoriu
# dvi juostas padarem ir pasitvarkem eiliskuma lauku, pasigrupavom
    fieldsets = (
        ('General', {'fields': ('unique_id', 'book')}),
        ('Availability', {'fields': (('status', 'due_back'),)})
    )

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')
    list_display_links = ('last_name', )

# Register your models here.
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Genre)
admin.site.register(models.Book, BookAdmin)
admin.site.register(models.BookInstance, BookInstanceAdmin)