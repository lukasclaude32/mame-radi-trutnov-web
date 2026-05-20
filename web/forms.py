from django import forms
from web.models import (
    ContactMessage, Candidate, Event, Post, SiteSettings,
    ProgramCategory, ProgramPoint, Supporter, PhotoAlbum, Photo, VideoLink
)


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input", "placeholder": "Vaše jméno"}),
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "Váš e-mail"}),
            "subject": forms.TextInput(attrs={"class": "form-input", "placeholder": "Předmět"}),
            "message": forms.Textarea(attrs={"class": "form-input", "placeholder": "Vaše zpráva...", "rows": 5}),
        }


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = "__all__"
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
            "priorities": forms.Textarea(attrs={"rows": 4}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date", "time_from", "time_to", "location", "image", "is_published"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "time_from": forms.TimeInput(attrs={"type": "time"}),
            "time_to": forms.TimeInput(attrs={"type": "time"}),
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content", "excerpt", "image", "is_published"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 10}),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
        }


class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = "__all__"
        widgets = {
            "about_text": forms.Textarea(attrs={"rows": 6}),
        }


class ProgramCategoryForm(forms.ModelForm):
    class Meta:
        model = ProgramCategory
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class ProgramPointForm(forms.ModelForm):
    class Meta:
        model = ProgramPoint
        fields = "__all__"
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class SupporterForm(forms.ModelForm):
    class Meta:
        model = Supporter
        fields = "__all__"
        widgets = {
            "quote": forms.Textarea(attrs={"rows": 3}),
        }


class PhotoAlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ["title", "description", "cover_image", "date", "is_published"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "caption", "order"]


class VideoLinkForm(forms.ModelForm):
    class Meta:
        model = VideoLink
        fields = ["title", "url", "thumbnail", "description", "order", "is_published"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
