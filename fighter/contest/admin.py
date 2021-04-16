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
	Role,
	Game,
	ChatRoom,
	ChatFile,
	ChatMessage,
	Faq,
	Ticket,
)

from .forms import GameForm

# Register your models here.
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
	list_per_page = 20

	search_fields = ('id', )
	list_display = ('id', )

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_per_page = 20

	search_fields = ('username', 'displayname', 'email', )
	list_display = ('username', 'email', 'displayname', "date_joined", "coins", 'referred_by', 'id', )

	filter_horizontal = ("roles", )

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
	list_display = ('name', 'gender', 'image', 'id')

	class Meta:
		ordering = ("name", )

@admin.register(Bout)
class BoutAdmin(admin.ModelAdmin):
	list_per_page = 20
	search_fields = ('method', 'status', 'event__name', 'fighter1__name', 'fighter2__name')
	list_display = ('fighter1', 'fighter2', 'event', "method", "division", 'status', 'round', 'time', 'id')

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

class GameEventFilter(AutocompleteFilter):
    title = 'Event' # display title
    field_name = 'event' # name of the foreign key field

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_per_page = 20
	# form = GameForm
	list_filter = [GameEventFilter]

	search_fields = ('name', 'event__name', 'owner__username', 'type_of_registration', 'genre', 'entrants__username', 'summary', 'rules_set', )
	list_display = ('name', 'event', 'owner', 'custom_date', 'type_of_registration', 'multientry', 'info_entrants', 'summary', 'short_rules_set', 'entry_limit')

	filter_horizontal = ("joined_users", "entrants", "bouts")

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
