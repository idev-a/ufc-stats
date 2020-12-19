from django.contrib import admin
from .models import Event, Fighter, Bout

# Register your models here.

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    pass

@admin.register(Bout)
class BoutAdmin(admin.ModelAdmin):
    pass