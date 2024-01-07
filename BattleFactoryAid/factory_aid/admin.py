from django.contrib import admin
from .models import Pokemon, Teams

class TeamsAdmin(admin.ModelAdmin):
    list_display = ('id', 'composing_sets', 'tier')
    search_fields = ['composing_sets']

admin.site.register(Pokemon)
admin.site.register(Teams, TeamsAdmin)

# Register your models here.
