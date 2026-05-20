from django.contrib import admin
from web.models import (
    SiteSettings, Candidate, ProgramCategory, ProgramPoint,
    Event, Post, Supporter, PhotoAlbum, Photo, VideoLink, ContactMessage
)

admin.site.site_header = "Máme rádi Trutnov - Administrace"

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ["site_name", "contact_email"]

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ["order", "__str__", "occupation", "party", "is_leader", "is_visible"]
    list_display_links = ["__str__"]
    list_editable = ["order", "is_visible", "is_leader"]
    list_filter = ["party", "is_visible"]

@admin.register(ProgramCategory)
class ProgramCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "order"]
    list_editable = ["order"]

@admin.register(ProgramPoint)
class ProgramPointAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "order"]
    list_editable = ["order"]
    list_filter = ["category"]

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "location", "is_published"]
    list_filter = ["is_published", "date"]

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published"]

@admin.register(Supporter)
class SupporterAdmin(admin.ModelAdmin):
    list_display = ["name", "title", "order", "is_visible"]
    list_editable = ["order", "is_visible"]

@admin.register(PhotoAlbum)
class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "is_published"]

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3

@admin.register(VideoLink)
class VideoLinkAdmin(admin.ModelAdmin):
    list_display = ["title", "url", "is_published"]

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "subject", "is_read", "created_at"]
    list_filter = ["is_read"]
