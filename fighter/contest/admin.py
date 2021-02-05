from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
	Event,
	Fighter,
	Bout,
	Entry,
	Selection,
	CustomUser,
	ChatRoom,
	ChatFile,
	ChatMessage
)

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_per_page = 20

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_per_page = 20

@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
	list_per_page = 20

@admin.register(Bout)
class BoutAdmin(admin.ModelAdmin):
	list_per_page = 20

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
	list_per_page = 20
	readonly_fields = ('last_edited',)

@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
	list_per_page = 20

# Chat

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
	list_per_page = 20

@admin.register(ChatFile)
class ChatFileAdmin(admin.ModelAdmin):
	list_per_page = 20

@admin.register(ChatMessage)
class ChatMessgaeAdmin(admin.ModelAdmin):
	list_per_page = 20

# admin.site.unregister(Group)
