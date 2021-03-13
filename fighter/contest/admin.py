from django.contrib import admin
from admin_auto_filters.filters import AutocompleteFilter
from django.contrib.auth.models import Group
from .models import (
	Event,
	Fighter,
	Bout,
	Entry,
	Selection,
	CustomUser,
	Game,
	ChatRoom,
	ChatFile,
	ChatMessage,
	Faq,
	Ticket,
)

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_per_page = 20

	search_fields = ('username', 'displayname', 'email', )
	list_display = ('username', 'email', 'displayname', "date_joined", "coins", 'referred_by', 'id', )

	class Meta:
		ordering = ("email", 'date_joined', )

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_per_page = 20

	search_fields = ('name', 'date', 'location', )
	list_display = ('name', 'date', 'location', 'status', 'action', )

	class Meta:
		ordering = ("date", 'name', )

@admin.register(Fighter)
class FighterAdmin(admin.ModelAdmin):
	list_per_page = 20
	search_fields = ('name', 'title', )
	list_display = ('name', 'title', 'id')

	class Meta:
		ordering = ("name", )

@admin.register(Bout)
class BoutAdmin(admin.ModelAdmin):
	list_per_page = 20
	search_fields = ('weight_class', 'method', 'status', 'event__name', 'fighter1__name', 'fighter2__name')
	list_display = ('fighter1', 'fighter2', 'event', "method", "weight_class", 'status', 'round', 'time', 'id')

	class Meta:
		ordering = ('event', "fighter1", 'fighter2')

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
	list_per_page = 20
	readonly_fields = ('last_edited',)
	search_fields = ('event__name', 'user__email', 'user__displayname', 'ranking', )
	list_display = ('event', 'user', 'ranking', 'game')

	class Meta:
		ordering = ('ranking', "event", 'user')

@admin.register(Selection)
class SelectionAdmin(admin.ModelAdmin):
	list_per_page = 20

	search_fields = ('bout__fighter1__name', 'bout__fighter2__name', 'entry__event__name', 'entry__user__email',)
	list_display = ('entry', 'bout', 'survivor1', 'survivor2', )

	class Meta:
		ordering = ('entry', "bout", )

class GameFilter(AutocompleteFilter):
    title = 'Event' # display title
    field_name = 'event' # name of the foreign key field

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_per_page = 20
	list_filter = [GameFilter]

	search_fields = ('name', 'event__name', 'type_of_registration', 'genre', 'entrants__username', 'instructions', 'rules_set', )
	list_display = ('name', 'event', 'type_of_registration', 'genre', 'info_entrants', 'info_joined', 'short_instructions', 'short_rules_set', 'date',)

	filter_horizontal = ("joined_users", "entrants")

	class Meta:
		ordering = ('event', 'date', )

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

	search_fields = ('content', 'sender__email', )
	list_display = ('sender', 'content', 'timestamp', )

	class Meta:
		ordering = ('timestamp', "sender", )

# FAQ
@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
	list_per_page = 20

	search_fields = ('question', 'answer', )
	list_display = ('question', 'answer', )

	class Meta:
		ordering = ('question', )

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
	list_per_page = 20

	search_fields = ('title', 'message', 'status', 'answer', 'creator__username')
	list_display = ('title', 'message', 'status', 'answer', 'creator', 'delivered', 'resolved', )

	readonly_fields = ["title", "message", "delivered"]

	class Meta:
		ordering = ('delivered', 'title', )

# admin.site.unregister(Group)
