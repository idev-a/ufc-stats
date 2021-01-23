from django.contrib import admin
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
    pass

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass

@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
    pass

@admin.register(Bout)
class BoutAdmin(admin.ModelAdmin):
    pass

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    pass

@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
    pass

# Chat

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass

@admin.register(ChatFile)
class ChatFileAdmin(admin.ModelAdmin):
    pass

@admin.register(ChatMessage)
class ChatMessgaeAdmin(admin.ModelAdmin):
    pass
