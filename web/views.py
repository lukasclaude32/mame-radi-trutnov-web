from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count
from datetime import date

from web.models import (
    SiteSettings, Candidate, ProgramCategory, ProgramPoint,
    Event, Post, Supporter, PhotoAlbum, Photo, VideoLink, ContactMessage
)
from web.forms import (
    ContactForm, CandidateForm, EventForm, PostForm,
    SiteSettingsForm, ProgramCategoryForm, ProgramPointForm,
    SupporterForm, PhotoAlbumForm, PhotoForm, VideoLinkForm
)


def home(request):
    candidates = Candidate.objects.filter(is_visible=True)[:6]
    upcoming_events = Event.objects.filter(is_published=True, date__gte=date.today())[:3]
    posts = Post.objects.filter(is_published=True)[:3]
    program_categories = ProgramCategory.objects.prefetch_related("points")[:4]
    return render(request, "web/home.html", {
        "candidates": candidates,
        "upcoming_events": upcoming_events,
        "posts": posts,
        "program_categories": program_categories,
    })


def about(request):
    return render(request, "web/about.html")


def candidates_list(request):
    candidates = Candidate.objects.filter(is_visible=True)
    return render(request, "web/candidates.html", {"candidates": candidates})


def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk, is_visible=True)
    return render(request, "web/candidate_detail.html", {"candidate": candidate})


def program(request):
    categories = ProgramCategory.objects.prefetch_related("points")
    return render(request, "web/program.html", {"categories": categories})


def events_list(request):
    upcoming = Event.objects.filter(is_published=True, date__gte=date.today())
    past = Event.objects.filter(is_published=True, date__lt=date.today())
    return render(request, "web/events.html", {"upcoming": upcoming, "past": past})


def posts_list(request):
    posts = Post.objects.filter(is_published=True)
    return render(request, "web/posts.html", {"posts": posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, "web/post_detail.html", {"post": post})


def supporters(request):
    supporters = Supporter.objects.filter(is_visible=True)
    return render(request, "web/supporters.html", {"supporters": supporters})


def gallery(request):
    albums = PhotoAlbum.objects.filter(is_published=True).annotate(photo_count=Count("photos"))
    videos = VideoLink.objects.filter(is_published=True)
    return render(request, "web/gallery.html", {"albums": albums, "videos": videos})


def album_detail(request, slug):
    album = get_object_or_404(PhotoAlbum, slug=slug, is_published=True)
    return render(request, "web/album_detail.html", {"album": album})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Děkujeme za vaši zprávu! Brzy se vám ozveme.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "web/contact.html", {"form": form})


# ==================== ADMIN PANEL ====================

def admin_login(request):
    if request.user.is_authenticated:
        return redirect("admin_dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_dashboard")
        messages.error(request, "Neplatné přihlašovací údaje.")
    return render(request, "admin_panel/login.html")


def admin_logout(request):
    logout(request)
    return redirect("home")


@login_required
def admin_dashboard(request):
    stats = {
        "candidates": Candidate.objects.count(),
        "events": Event.objects.count(),
        "posts": Post.objects.count(),
        "messages": ContactMessage.objects.filter(is_read=False).count(),
        "supporters": Supporter.objects.count(),
        "albums": PhotoAlbum.objects.count(),
        "videos": VideoLink.objects.count(),
        "program_categories": ProgramCategory.objects.count(),
    }
    recent_messages = ContactMessage.objects.order_by("-created_at")[:5]
    return render(request, "admin_panel/dashboard.html", {
        "stats": stats,
        "recent_messages": recent_messages,
    })


# Generic CRUD helpers
def _admin_list(request, model, template, context_name):
    items = model.objects.all()
    return render(request, template, {context_name: items})


def _admin_create(request, form_class, template, redirect_name, title="Nový"):
    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspěšně vytvořeno.")
            return redirect(redirect_name)
    else:
        form = form_class()
    return render(request, template, {"form": form, "title": title})


def _admin_edit(request, model, pk, form_class, template, redirect_name, title="Upravit"):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Úspěšně uloženo.")
            return redirect(redirect_name)
    else:
        form = form_class(instance=obj)
    return render(request, template, {"form": form, "obj": obj, "title": title})


def _admin_delete(request, model, pk, redirect_name):
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Úspěšně smazáno.")
    return redirect(redirect_name)


# Candidates
@login_required
def admin_candidates(request):
    return _admin_list(request, Candidate, "admin_panel/candidates.html", "candidates")

@login_required
def admin_candidate_create(request):
    return _admin_create(request, CandidateForm, "admin_panel/form.html", "admin_candidates", "Nový kandidát")

@login_required
def admin_candidate_edit(request, pk):
    return _admin_edit(request, Candidate, pk, CandidateForm, "admin_panel/form.html", "admin_candidates", "Upravit kandidáta")

@login_required
def admin_candidate_delete(request, pk):
    return _admin_delete(request, Candidate, pk, "admin_candidates")


# Events
@login_required
def admin_events(request):
    return _admin_list(request, Event, "admin_panel/events.html", "events")

@login_required
def admin_event_create(request):
    return _admin_create(request, EventForm, "admin_panel/form.html", "admin_events", "Nová událost")

@login_required
def admin_event_edit(request, pk):
    return _admin_edit(request, Event, pk, EventForm, "admin_panel/form.html", "admin_events", "Upravit událost")

@login_required
def admin_event_delete(request, pk):
    return _admin_delete(request, Event, pk, "admin_events")


# Posts
@login_required
def admin_posts(request):
    return _admin_list(request, Post, "admin_panel/posts.html", "posts")

@login_required
def admin_post_create(request):
    return _admin_create(request, PostForm, "admin_panel/form.html", "admin_posts", "Nový příspěvek")

@login_required
def admin_post_edit(request, pk):
    return _admin_edit(request, Post, pk, PostForm, "admin_panel/form.html", "admin_posts", "Upravit příspěvek")

@login_required
def admin_post_delete(request, pk):
    return _admin_delete(request, Post, pk, "admin_posts")


# Program
@login_required
def admin_program(request):
    categories = ProgramCategory.objects.prefetch_related("points")
    return render(request, "admin_panel/program.html", {"categories": categories})

@login_required
def admin_program_category_create(request):
    return _admin_create(request, ProgramCategoryForm, "admin_panel/form.html", "admin_program", "Nová kategorie programu")

@login_required
def admin_program_category_edit(request, pk):
    return _admin_edit(request, ProgramCategory, pk, ProgramCategoryForm, "admin_panel/form.html", "admin_program", "Upravit kategorii")

@login_required
def admin_program_category_delete(request, pk):
    return _admin_delete(request, ProgramCategory, pk, "admin_program")

@login_required
def admin_program_point_create(request):
    return _admin_create(request, ProgramPointForm, "admin_panel/form.html", "admin_program", "Nový bod programu")

@login_required
def admin_program_point_edit(request, pk):
    return _admin_edit(request, ProgramPoint, pk, ProgramPointForm, "admin_panel/form.html", "admin_program", "Upravit bod programu")

@login_required
def admin_program_point_delete(request, pk):
    return _admin_delete(request, ProgramPoint, pk, "admin_program")


# Supporters
@login_required
def admin_supporters(request):
    return _admin_list(request, Supporter, "admin_panel/supporters.html", "supporters")

@login_required
def admin_supporter_create(request):
    return _admin_create(request, SupporterForm, "admin_panel/form.html", "admin_supporters", "Nový podporovatel")

@login_required
def admin_supporter_edit(request, pk):
    return _admin_edit(request, Supporter, pk, SupporterForm, "admin_panel/form.html", "admin_supporters", "Upravit podporovatele")

@login_required
def admin_supporter_delete(request, pk):
    return _admin_delete(request, Supporter, pk, "admin_supporters")


# Gallery
@login_required
def admin_gallery(request):
    albums = PhotoAlbum.objects.annotate(photo_count=Count("photos"))
    videos = VideoLink.objects.all()
    return render(request, "admin_panel/gallery.html", {"albums": albums, "videos": videos})

@login_required
def admin_album_create(request):
    return _admin_create(request, PhotoAlbumForm, "admin_panel/form.html", "admin_gallery", "Nové album")

@login_required
def admin_album_edit(request, pk):
    album = get_object_or_404(PhotoAlbum, pk=pk)
    if request.method == "POST":
        form = PhotoAlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            # Handle multiple photo uploads
            for f in request.FILES.getlist("photos"):
                Photo.objects.create(album=album, image=f)
            messages.success(request, "Album uloženo.")
            return redirect("admin_gallery")
    else:
        form = PhotoAlbumForm(instance=album)
    photos = album.photos.all()
    return render(request, "admin_panel/album_edit.html", {"form": form, "album": album, "photos": photos})

@login_required
def admin_album_delete(request, pk):
    return _admin_delete(request, PhotoAlbum, pk, "admin_gallery")

@login_required
def admin_photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    album_pk = photo.album.pk
    if request.method == "POST":
        photo.delete()
        messages.success(request, "Fotografie smazána.")
    return redirect("admin_album_edit", pk=album_pk)

@login_required
def admin_photo_upload(request, album_pk):
    album = get_object_or_404(PhotoAlbum, pk=album_pk)
    if request.method == "POST":
        for f in request.FILES.getlist("photos"):
            Photo.objects.create(album=album, image=f)
        messages.success(request, "Fotografie nahrány.")
    return redirect("admin_album_edit", pk=album_pk)


# Videos
@login_required
def admin_video_create(request):
    return _admin_create(request, VideoLinkForm, "admin_panel/form.html", "admin_gallery", "Nové video")

@login_required
def admin_video_edit(request, pk):
    return _admin_edit(request, VideoLink, pk, VideoLinkForm, "admin_panel/form.html", "admin_gallery", "Upravit video")

@login_required
def admin_video_delete(request, pk):
    return _admin_delete(request, VideoLink, pk, "admin_gallery")


# Messages
@login_required
def admin_messages_list(request):
    msgs = ContactMessage.objects.all()
    return render(request, "admin_panel/messages.html", {"contact_messages": msgs})

@login_required
def admin_message_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if not msg.is_read:
        msg.is_read = True
        msg.save()
    return render(request, "admin_panel/message_detail.html", {"msg": msg})

@login_required
def admin_message_delete(request, pk):
    return _admin_delete(request, ContactMessage, pk, "admin_messages")


# Site Settings
@login_required
def admin_settings(request):
    settings_obj = SiteSettings.objects.first()
    if not settings_obj:
        settings_obj = SiteSettings.objects.create()
    if request.method == "POST":
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Nastavení uloženo.")
            return redirect("admin_settings")
    else:
        form = SiteSettingsForm(instance=settings_obj)
    return render(request, "admin_panel/settings.html", {"form": form})
