from django.db import models
from django.utils.text import slugify
import uuid


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=200, default="Máme rádi Trutnov")
    tagline = models.CharField(max_length=300, default="A co vy?")
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    hero_image = models.ImageField(upload_to="site/", blank=True, null=True)
    about_text = models.TextField(blank=True)
    contact_email = models.EmailField(default="barboratomasova@seznam.cz")
    contact_phone = models.CharField(max_length=30, default="775 887 616")
    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/MameRadiTrutnov/")
    instagram_url = models.URLField(blank=True)
    footer_text = models.CharField(max_length=300, default="© 2026 Máme rádi Trutnov")
    meta_description = models.CharField(max_length=300, blank=True)

    class Meta:
        verbose_name = "Nastavení webu"
        verbose_name_plural = "Nastavení webu"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            return SiteSettings.objects.first()
        return super().save(*args, **kwargs)


class Candidate(models.Model):
    order = models.PositiveIntegerField(default=0)
    title_prefix = models.CharField(max_length=50, blank=True, verbose_name="Titul před jménem")
    first_name = models.CharField(max_length=100, verbose_name="Jméno")
    last_name = models.CharField(max_length=100, verbose_name="Příjmení")
    title_suffix = models.CharField(max_length=50, blank=True, verbose_name="Titul za jménem")
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Věk")
    occupation = models.CharField(max_length=200, blank=True, verbose_name="Povolání")
    party = models.CharField(max_length=100, blank=True, default="ODS", verbose_name="Strana")
    bio = models.TextField(blank=True, verbose_name="Medailonek")
    priorities = models.TextField(blank=True, verbose_name="Priority")
    photo = models.ImageField(upload_to="candidates/", blank=True, null=True, verbose_name="Fotografie")
    is_leader = models.BooleanField(default=False, verbose_name="Lídr kandidátky")
    is_visible = models.BooleanField(default=True, verbose_name="Zobrazit na webu")

    class Meta:
        ordering = ["order"]
        verbose_name = "Kandidát"
        verbose_name_plural = "Kandidáti"

    def __str__(self):
        parts = [self.title_prefix, self.first_name, self.last_name, self.title_suffix]
        return " ".join(p for p in parts if p)

    @property
    def full_name(self):
        return str(self)

    @property
    def priorities_list(self):
        if self.priorities:
            return [p.strip() for p in self.priorities.split("\n") if p.strip()]
        return []


class ProgramCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name="Název kategorie")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Ikona (emoji)")
    order = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, verbose_name="Popis")

    class Meta:
        ordering = ["order"]
        verbose_name = "Kategorie programu"
        verbose_name_plural = "Kategorie programu"

    def __str__(self):
        return self.name


class ProgramPoint(models.Model):
    category = models.ForeignKey(ProgramCategory, on_delete=models.CASCADE, related_name="points", verbose_name="Kategorie")
    title = models.CharField(max_length=300, verbose_name="Název bodu")
    description = models.TextField(blank=True, verbose_name="Popis")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["category__order", "order"]
        verbose_name = "Bod programu"
        verbose_name_plural = "Body programu"

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=300, verbose_name="Název události")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Popis")
    date = models.DateField(verbose_name="Datum")
    time_from = models.TimeField(blank=True, null=True, verbose_name="Čas od")
    time_to = models.TimeField(blank=True, null=True, verbose_name="Čas do")
    location = models.CharField(max_length=300, blank=True, verbose_name="Místo")
    image = models.ImageField(upload_to="events/", blank=True, null=True, verbose_name="Obrázek")
    is_published = models.BooleanField(default=True, verbose_name="Publikováno")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]
        verbose_name = "Událost"
        verbose_name_plural = "Události"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if Event.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=300, verbose_name="Nadpis")
    slug = models.SlugField(max_length=300, unique=True, blank=True)
    content = models.TextField(verbose_name="Obsah")
    excerpt = models.TextField(blank=True, verbose_name="Krátký popis")
    image = models.ImageField(upload_to="posts/", blank=True, null=True, verbose_name="Hlavní obrázek")
    is_published = models.BooleanField(default=True, verbose_name="Publikováno")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Příspěvek"
        verbose_name_plural = "Příspěvky"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if Post.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)


class Supporter(models.Model):
    name = models.CharField(max_length=200, verbose_name="Jméno")
    title = models.CharField(max_length=200, blank=True, verbose_name="Funkce/titul")
    quote = models.TextField(blank=True, verbose_name="Citát")
    photo = models.ImageField(upload_to="supporters/", blank=True, null=True, verbose_name="Fotografie")
    order = models.PositiveIntegerField(default=0)
    is_visible = models.BooleanField(default=True, verbose_name="Zobrazit")

    class Meta:
        ordering = ["order"]
        verbose_name = "Podporovatel"
        verbose_name_plural = "Podporovatelé"

    def __str__(self):
        return self.name


class PhotoAlbum(models.Model):
    title = models.CharField(max_length=200, verbose_name="Název alba")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name="Popis")
    cover_image = models.ImageField(upload_to="albums/", blank=True, null=True, verbose_name="Obálka")
    date = models.DateField(blank=True, null=True, verbose_name="Datum")
    is_published = models.BooleanField(default=True, verbose_name="Publikováno")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        verbose_name = "Fotoalbum"
        verbose_name_plural = "Fotoalba"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            if PhotoAlbum.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{uuid.uuid4().hex[:6]}"
        super().save(*args, **kwargs)


class Photo(models.Model):
    album = models.ForeignKey(PhotoAlbum, on_delete=models.CASCADE, related_name="photos", verbose_name="Album")
    image = models.ImageField(upload_to="photos/", verbose_name="Fotografie")
    caption = models.CharField(max_length=300, blank=True, verbose_name="Popisek")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Fotografie"
        verbose_name_plural = "Fotografie"

    def __str__(self):
        return self.caption or f"Foto #{self.pk}"


class VideoLink(models.Model):
    title = models.CharField(max_length=300, verbose_name="Název")
    url = models.URLField(verbose_name="URL videa (YouTube, apod.)")
    thumbnail = models.ImageField(upload_to="videos/", blank=True, null=True, verbose_name="Náhled")
    description = models.TextField(blank=True, verbose_name="Popis")
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True, verbose_name="Publikováno")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Video"
        verbose_name_plural = "Videa"

    def __str__(self):
        return self.title

    @property
    def embed_url(self):
        url = self.url
        if "youtube.com/watch?v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        if "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url


class ContactMessage(models.Model):
    name = models.CharField(max_length=200, verbose_name="Jméno")
    email = models.EmailField(verbose_name="E-mail")
    subject = models.CharField(max_length=300, blank=True, verbose_name="Předmět")
    message = models.TextField(verbose_name="Zpráva")
    is_read = models.BooleanField(default=False, verbose_name="Přečteno")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Zpráva"
        verbose_name_plural = "Zprávy"

    def __str__(self):
        return f"{self.name}: {self.subject or 'Bez předmětu'}"
