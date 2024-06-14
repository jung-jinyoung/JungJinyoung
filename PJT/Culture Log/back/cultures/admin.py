from django.contrib import admin
from .models import ChoicedBook, ChoicedMovie, Review
# Register your models here.
admin.site.register(ChoicedBook)
admin.site.register(ChoicedMovie)
admin.site.register(Review)