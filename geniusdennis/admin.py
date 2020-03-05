from django.contrib import admin

# Register your models here.
from .models import Spanish, English

class EnglishInline(admin.TabularInline):
    model = English
    extra = 3
class SpanishAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,               {'fields': ['word_esp']}),
		('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
	]
	inlines = [EnglishInline]
	list_display = ('word_esp', 'pub_date','freshvocab')
	list_filter = ['pub_date']
	search_fields = ['word_esp']

admin.site.register(Spanish, SpanishAdmin)
