import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrt_web.settings')
django.setup()

from django.contrib.auth.models import User
from web.models import (
    SiteSettings, Candidate, ProgramCategory, ProgramPoint,
    Event, Supporter, PhotoAlbum, Photo, VideoLink
)

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mameraditrutnov.cz', 'admin123')
    print("Superuser 'admin' created (password: admin123)")

# Site Settings
SiteSettings.objects.filter(pk=1).delete()
settings, _ = SiteSettings.objects.get_or_create(pk=1, defaults={
    "site_name": "Máme rádi Trutnov",
    "tagline": "A co vy?",
    "about_text": "Základem tohoto projektu byla snaha skupiny lidí kolem bývalého starosty a stávajícího zastupitele Ivana Adamce vyjádřit náklonnost městu, v němž žijeme.\n\nTaké pod vedením současného starosty Michala Rosy zůstává cílem využít při správě věcí veřejných nabyté zkušenosti, odpovědnost a konkrétní, splnitelné vize k rozvoji Trutnova v sebevědomé evropské město se všemi službami a vybaveností, jež ke spokojenému životu jeho obyvatelé potřebují.\n\nSlovní spojení Máme rádi Trutnov se stalo jednoduchým mottem Občanské demokratické strany a svůj význam neztratilo dodnes.\n\nChceme pokračovat v práci, která se daří a využít i dlouhodobě prověřenou spolupráci mezi ODS a stranami KDU-ČSL a TOP 09 v Trutnově.\n\nJsme připraveni i nadále rozvíjet Trutnov v město, kde se dobře žije, kam se budou rádi vracet naše děti po studiích.",
    "contact_email": "baratomasovapr@gmail.com",
    "contact_phone": "",
    "facebook_url": "https://www.facebook.com/MameRadiTrutnov/",
    "instagram_url": "https://www.instagram.com/mameraditrutnov/",
    "footer_text": "© 2026 Máme rádi Trutnov",
    "meta_description": "Máme rádi Trutnov – Kandidátka do komunálních voleb 2026. Společně pro lepší Trutnov.",
})
print("Site settings created")

# Candidates
Candidate.objects.all().delete()

rosa_bio = (
    "Když jsem v prosinci 2021 ukončil činnost svého architektonického ateliéru a stal se starostou Trutnova, "
    "mnozí lidé to nechápali. Dodnes se mě někteří ptají, zda mi to stálo za to. Odpovídám bez váhání. "
    "Nikdy jsem neuměl stát stranou a jen přihlížet. Vždy jsem měl potřebu zapojit se, hledat řešení a nést za ně "
    "odpovědnost. O to více si vážím příležitosti podílet se na rozvoji svého rodného města.\n\n"
    "V komunálních volbách v roce 2022 jsem Vás požádal o důvěru. Slíbil jsem odpovědnou správu města, péči o jeho "
    "majetek, promyšlený rozvoj a otevřenou komunikaci. Čtyři roky jsme se snažili tento závazek naplňovat.\n\n"
    "Nebyla to jednoduchá doba. Přesto jsme společně dokončili dvě významné investice – kino Vesmír a nové křídlo "
    "domova pro seniory. Zahájili jsme projekty, které zlepší život v jednotlivých městských částech, významně jsme "
    "investovali do mateřských a základních škol a využili příležitosti, které nabízely dotační programy. Současně "
    "jsme připravili řadu dalších projektů, které budou Trutnov posouvat vpřed i v následujících letech.\n\n"
    "Jsem přesvědčen, že Trutnov je dnes silnější, sebevědomější a lépe připravený na budoucnost.\n\n"
    "Kandidátku do nadcházejících komunálních voleb Máme rádi Trutnov jsem sestavil s maximální péčí. Vedle "
    "kandidátů Občanské demokratické strany na ní najdete také nezávislé osobnosti a zástupce TOP 09 a KDU-ČSL. "
    "Jsou to lidé pracovití, zkušení a připravení převzít odpovědnost za budoucnost našeho města.\n\n"
    "Společně chceme navázat na to, co se podařilo, a pokračovat v rozvoji města, které máme rádi."
)

candidates_data = [
    {"order": 1, "photo": "candidates/01-michal-rosa.jpg", "title_prefix": "Ing. arch.", "first_name": "Michal", "last_name": "Rosa", "occupation": "starosta Trutnova", "party": "ODS", "is_leader": True, "bio": rosa_bio},
    {"order": 2, "photo": "candidates/02-pavel-kana.jpg", "title_prefix": "Mgr.", "first_name": "Pavel", "last_name": "Káňa", "occupation": "učitel matematiky na gymnáziu", "party": "ODS"},
    {"order": 3, "photo": "candidates/03-jana-kremenska.jpg", "title_prefix": "PhDr.", "first_name": "Jana", "last_name": "Křemenská", "occupation": "HR manažerka", "party": "bez politické příslušnosti"},
    {"order": 4, "photo": "candidates/04-radek-horak.jpg", "title_prefix": "Mgr.", "first_name": "Radek", "last_name": "Horák", "occupation": "vedoucí sportovišť Trutnov", "party": "bez politické příslušnosti"},
    {"order": 5, "photo": "candidates/05-filip-belik.jpg", "title_prefix": "Bc.", "first_name": "Filip", "last_name": "Bělík", "occupation": "vedoucí sociální pracovník", "party": "TOP 09"},
    {"order": 6, "photo": "candidates/06-sabina-tlaskalova.jpg", "title_prefix": "Bc.", "first_name": "Sabina", "last_name": "Tláskalová", "occupation": "učitelka základní školy", "party": "ODS"},
    {"order": 7, "photo": "candidates/07-miroslav-krcmar.jpg", "first_name": "Miroslav", "last_name": "Krčmář", "occupation": "podnikatel", "party": "ODS"},
    {"order": 8, "photo": "candidates/08-juraj-suchan.jpg", "first_name": "Juraj", "last_name": "Sucháň", "occupation": "vedoucí prodeje nových vozů", "party": "ODS"},
    {"order": 9, "photo": "candidates/09-ivan-adamec.jpg", "title_prefix": "Mgr.", "first_name": "Ivan", "last_name": "Adamec", "occupation": "poslanec Parlamentu ČR", "party": "ODS"},
    {"order": 10, "photo": "candidates/10-vladislav-sauer.jpg", "title_prefix": "Ing.", "first_name": "Vladislav", "last_name": "Sauer", "occupation": "ředitel střední průmyslové školy", "party": "bez politické příslušnosti"},
    {"order": 11, "photo": "candidates/11-kristina-retkova.jpg", "title_prefix": "Bc.", "first_name": "Kristina", "last_name": "Retková", "occupation": "fyzioterapeutka", "party": "KDU-ČSL"},
    {"order": 12, "photo": "candidates/12-lukas-vydra.jpg", "first_name": "Lukáš", "last_name": "Vydra", "occupation": "podnikatel", "party": "ODS"},
    {"order": 13, "photo": "candidates/13-jiri-david.jpg", "title_prefix": "MUDr.", "first_name": "Jiří", "last_name": "David", "occupation": "lékař", "party": "ODS"},
    {"order": 14, "photo": "candidates/14-libor-kasik.jpg", "title_prefix": "MgA.", "first_name": "Libor", "last_name": "Kasík", "occupation": "ředitel spol. centra UFFO", "party": "ODS"},
    {"order": 15, "photo": "candidates/15-silvie-sidakova.jpg", "title_prefix": "MUDr.", "first_name": "Silvie", "last_name": "Šidáková", "occupation": "lékařka", "party": "TOP 09"},
    {"order": 16, "photo": "candidates/16-vaclav-fiser.jpg", "title_prefix": "Mgr.", "first_name": "Václav", "last_name": "Fišer", "occupation": "učitel základní školy", "party": "ODS"},
    {"order": 17, "photo": "candidates/17-jakub-vomacka.jpg", "title_prefix": "MUDr.", "first_name": "Jakub", "last_name": "Vomáčka", "occupation": "lékař", "party": "bez politické příslušnosti"},
    {"order": 18, "photo": "candidates/18-gabriela-grundova.jpg", "title_prefix": "Mgr.", "first_name": "Gabriela", "last_name": "Grundová", "occupation": "ředitelka ZŠ, koučka", "party": "bez politické příslušnosti"},
    {"order": 19, "photo": "candidates/19-petr-gaisler.jpg", "title_prefix": "Ing.", "first_name": "Petr", "last_name": "Gaisler", "occupation": "jednatel společnosti", "party": "ODS"},
    {"order": 20, "photo": "candidates/20-jaroslav-bures.jpg", "first_name": "Jaroslav", "last_name": "Bureš", "occupation": "podnikatel", "party": "ODS"},
    {"order": 21, "photo": "candidates/21-libor-srol.jpg", "first_name": "Libor", "last_name": "Šrol", "occupation": "podnikatel", "party": "bez politické příslušnosti"},
    {"order": 22, "photo": "candidates/22-lukas-vysoudil.jpg", "first_name": "Lukáš", "last_name": "Vysoudil", "occupation": "jednatel", "party": "ODS"},
    {"order": 23, "first_name": "Lucie", "last_name": "Špetlová", "occupation": "podnikatelka", "party": "bez politické příslušnosti"},
    {"order": 24, "photo": "candidates/24-josef-fujera.jpg", "first_name": "Josef", "last_name": "Fujera", "occupation": "důchodce", "party": "ODS"},
    {"order": 25, "photo": "candidates/25-hana-nydrlova.jpg", "title_prefix": "Ing.", "first_name": "Hana", "last_name": "Nýdrlová", "occupation": "důchodkyně", "party": "ODS"},
    {"order": 26, "title_prefix": "Ing.", "first_name": "Karel", "last_name": "Kostka", "occupation": "projektový manažer", "party": "TOP 09"},
    {"order": 27, "photo": "candidates/27-simona-vomackova.jpg", "title_prefix": "Mgr.", "first_name": "Simona", "last_name": "Vomáčková", "occupation": "podnikatelka", "party": "ODS"},
    {"order": 28, "photo": "candidates/28-lukas-haase.jpg", "title_prefix": "JUDr.", "first_name": "Lukáš", "last_name": "Haase", "occupation": "podnikatel", "party": "ODS"},
    {"order": 29, "first_name": "Zuzana", "last_name": "Trösterová", "occupation": "důchodkyně", "party": "ODS"},
    {"order": 30, "photo": "candidates/30-pavel-skop.jpg", "first_name": "Pavel", "last_name": "Škop", "occupation": "OSVČ", "party": "ODS"},
    {"order": 31, "photo": "candidates/31-tomas-krcmar.jpg", "first_name": "Tomáš", "last_name": "Krčmář", "occupation": "podnikatel", "party": "ODS"},
    {"order": 32, "photo": "candidates/32-prokop-barton.jpg", "first_name": "Prokop", "last_name": "Bartoň", "occupation": "student", "party": "KDU-ČSL"},
    {"order": 33, "photo": "candidates/33-petr-syrovatka.jpg", "first_name": "Petr", "last_name": "Syrovátka", "occupation": "projektant dopravních staveb", "party": "TOP 09"},
]

for data in candidates_data:
    Candidate.objects.get_or_create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        defaults=data
    )
print(f"Created {len(candidates_data)} candidates")

# Program: full program will be published in the coming weeks; the page shows a
# static intro text (templates/web/program.html) until categories are added.
ProgramCategory.objects.all().delete()
print("Program categories cleared")

# Events: sample events removed; real dates (K VĚCI meetups) will be added
# once provided from the campaign's Facebook.
Event.objects.all().delete()
print("Events cleared")

# Gallery: team photo album + intro video (files committed in media/)
PhotoAlbum.objects.all().delete()
album = PhotoAlbum.objects.create(
    title="Společné focení kandidátky",
    description="Tým Máme rádi Trutnov pro komunální volby 2026.",
    cover_image="photos/tym-namesti.jpg",
    is_published=True,
)
Photo.objects.create(album=album, image="photos/tym-namesti.jpg", caption="Tým Máme rádi Trutnov na Krakonošově náměstí", order=0)
Photo.objects.create(album=album, image="photos/tym-podloubi.jpg", caption="Tým Máme rádi Trutnov", order=1)
print("Photo album created")

VideoLink.objects.all().delete()
VideoLink.objects.create(
    title="Máme rádi Trutnov",
    description="Podívejte se, kdo jsme a proč do komunálních voleb 2026 jdeme společně – ODS s podporou KDU-ČSL a TOP 09.",
    url="/media/videos/uvodni-video.mp4",
    thumbnail="videos/uvodni-video-poster.jpg",
    order=0,
    is_published=True,
)
print("Intro video created")

print("\nDone! You can now run: python manage.py runserver")
print("Admin: http://localhost:8000/admin-panel/")
print("Login: admin / admin123")
