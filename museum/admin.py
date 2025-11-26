from django.contrib import admin
from .models import Car, Arena, GameUpdate, Achievement, Tournament, VisitorComment, Highlight

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'rarity', 'hitbox', 'release_date']
    list_filter = ['rarity', 'manufacturer', 'hitbox']
    search_fields = ['name', 'manufacturer']

@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ['name', 'arena_type', 'environment', 'capacity']
    list_filter = ['arena_type', 'environment']
    search_fields = ['name', 'environment']

@admin.register(GameUpdate)
class GameUpdateAdmin(admin.ModelAdmin):
    list_display = ['version', 'title', 'release_date']
    list_filter = ['release_date']
    search_fields = ['version', 'title']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'reward']
    list_filter = ['difficulty']
    search_fields = ['title', 'description']

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'season', 'date', 'winner', 'prize_pool']
    list_filter = ['season', 'date']
    search_fields = ['name', 'winner', 'mvp']

@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ['title', 'player', 'tournament', 'moment_type', 'duration', 'views', 'is_featured', 'created_at']
    list_filter = ['moment_type', 'tournament', 'is_featured', 'created_at']
    search_fields = ['title', 'player', 'description']
    list_editable = ['is_featured']
    readonly_fields = ['views', 'created_at']

@admin.register(VisitorComment)
class VisitorCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'comment']