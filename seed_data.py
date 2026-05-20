import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrt_web.settings')
django.setup()

from django.contrib.auth.models import User
from web.models import (
    SiteSettings, Candidate, ProgramCategory, ProgramPoint,
    Event, Supporter
)

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mameraditrutnov.cz', 'admin123')
    print("Superuser 'admin' created (password: admin123)")

# Site Settings
settings, _ = SiteSettings.objects.get_or_create(pk=1, defaults={
    "site_name": "Máme rádi Trutnov",
    "tagline": "A co vy?",
    "about_text": "Základem projektu byla snaha skupiny lidí kolem bývalého starosty a stávajícího zastupitele Ivana Adamce vyjádřit náklonnost městu, v němž žijeme.\n\nSlovní spojení Máme rádi Trutnov se stalo jednoduchým mottem Občanské demokratické strany a svůj význam neztratilo dodnes.\n\nCílem zůstává využít při správě věcí veřejných nabyté zkušenosti, odpovědnost a konkrétní, splnitelné vize k rozvoji Trutnova v sebevědomé evropské město se všemi službami a vybaveností, jež ke spokojenému životu jeho obyvatelé potřebují.\n\nJsme připraveni i nadále měnit Trutnov v město, kde se dobře žije, kam se budou rádi vracet naše děti po studiích.",
    "contact_email": "barboratomasova@seznam.cz",
    "contact_phone": "775 887 616",
    "facebook_url": "https://www.facebook.com/MameRadiTrutnov/",
    "footer_text": "© 2026 Máme rádi Trutnov",
    "meta_description": "Máme rádi Trutnov – Kandidátka do komunálních voleb 2026. Společně pro lepší Trutnov.",
})
print("Site settings created")

# Candidates
Candidate.objects.all().delete()
candidates_data = [
    {"order": 1, "title_prefix": "Ing. arch.", "first_name": "Michal", "last_name": "Rosa", "party": "ODS", "is_leader": True},
    {"order": 2, "title_prefix": "Mgr.", "first_name": "Pavel", "last_name": "Káňa", "party": "ODS"},
    {"order": 3, "title_prefix": "PhDr.", "first_name": "Jana", "last_name": "Křemenská", "party": "nezávislá"},
    {"order": 4, "first_name": "Radek", "last_name": "Horák", "party": "nezávislý"},
    {"order": 5, "title_prefix": "Bc.", "first_name": "Filip", "last_name": "Bělík", "party": "TOP 09"},
    {"order": 6, "title_prefix": "Bc.", "first_name": "Sabina", "last_name": "Tláskalová", "party": "ODS"},
    {"order": 7, "first_name": "Miroslav", "last_name": "Krčmář", "party": "ODS"},
    {"order": 8, "first_name": "Juraj", "last_name": "Sucháň", "party": "ODS"},
    {"order": 9, "title_prefix": "Mgr.", "first_name": "Ivan", "last_name": "Adamec", "party": "ODS"},
    {"order": 10, "title_prefix": "Ing.", "first_name": "Vladislav", "last_name": "Sauer", "party": "nezávislý"},
    {"order": 11, "title_prefix": "Bc.", "first_name": "Kristýna", "last_name": "Retková", "party": "KDU-ČSL"},
    {"order": 12, "first_name": "Lukáš", "last_name": "Vydra", "party": "ODS"},
    {"order": 13, "title_prefix": "MUDr.", "first_name": "Jiří", "last_name": "David", "party": "ODS"},
    {"order": 14, "title_prefix": "Mgr.", "first_name": "Libor", "last_name": "Kasík", "party": "ODS"},
    {"order": 15, "title_prefix": "MUDr.", "first_name": "Silvie", "last_name": "Šidáková", "party": "TOP 09"},
    {"order": 16, "title_prefix": "Mgr.", "first_name": "Václav", "last_name": "Fišer", "party": "ODS"},
    {"order": 17, "title_prefix": "MUDr.", "first_name": "Jakub", "last_name": "Vomáčka", "party": "nezávislý"},
    {"order": 18, "title_prefix": "Mgr.", "first_name": "Gabriela", "last_name": "Grundová", "party": "nezávislá"},
    {"order": 19, "title_prefix": "Mgr.", "first_name": "Petr", "last_name": "Gaisler", "party": "ODS"},
    {"order": 20, "first_name": "Jaroslav", "last_name": "Bureš", "party": "ODS"},
    {"order": 21, "first_name": "Libor", "last_name": "Šrol", "party": "nezávislý"},
    {"order": 22, "first_name": "Lukáš", "last_name": "Vysoudil", "party": "ODS"},
    {"order": 23, "first_name": "Lucie", "last_name": "Špetlová", "party": "nezávislá"},
    {"order": 24, "first_name": "Josef", "last_name": "Fujera", "party": "ODS"},
    {"order": 25, "title_prefix": "Mgr.", "first_name": "Hana", "last_name": "Nýdrlová", "party": "ODS"},
    {"order": 26, "first_name": "Jan", "last_name": "Joudal", "party": "TOP 09"},
    {"order": 27, "title_prefix": "Mgr.", "first_name": "Simona", "last_name": "Vomáčková", "party": "ODS"},
    {"order": 28, "title_prefix": "JUDr.", "first_name": "Lukáš", "last_name": "Haase", "party": "ODS"},
    {"order": 29, "first_name": "Zuzana", "last_name": "Trösterová", "party": "ODS"},
    {"order": 30, "first_name": "Pavel", "last_name": "Škop", "party": "ODS"},
    {"order": 31, "first_name": "Tomáš", "last_name": "Krčmář", "party": "ODS"},
    {"order": 32, "first_name": "Prokop", "last_name": "Bartoň", "party": "KDU-ČSL"},
    {"order": 33, "first_name": "Petr", "last_name": "Syrovátka", "party": "TOP 09"},
]

for data in candidates_data:
    Candidate.objects.get_or_create(
        first_name=data["first_name"],
        last_name=data["last_name"],
        defaults=data
    )
print(f"Created {len(candidates_data)} candidates")

# Program categories and points
program_data = [
    {"name": "Doprava", "icon": "🚗", "order": 1, "description": "Řešení dopravní situace a infrastruktury", "points": [
        "Urychlení stavby dálnice D11",
        "Řešení parkování v centru města",
        "Rekonstrukce chodníků a silnic",
        "Rozvoj cyklostezek a napojení na Labskou stezku",
        "Modernizace autobusového nádraží",
    ]},
    {"name": "Vzdělávání a kultura", "icon": "🎓", "order": 2, "description": "Investice do budoucnosti našich dětí a kulturního života", "points": [
        "Moderní vzdělávací technologie ve školách",
        "Podpora kulturních akcí a institucí",
        "Rozvoj Společenského centra Uffo",
        "Podpora sportovních a volnočasových aktivit pro mládež",
    ]},
    {"name": "Zdravotnictví a sociální služby", "icon": "🏥", "order": 3, "description": "Dostupná péče pro všechny obyvatele", "points": [
        "Zajištění dostupné lékařské péče (zubaři, praktičtí lékaři)",
        "Podpora nemocnice a zdravotních služeb",
        "Zvýhodněné vstupné pro obyvatele na kulturu a sport",
        "Bezbariérovost města a přístupnost služeb",
        "Rozvoj sociálních služeb pro seniory",
    ]},
    {"name": "Rozvoj města", "icon": "🏗️", "order": 4, "description": "Moderní a udržitelný rozvoj Trutnova", "points": [
        "Bydlení pro mladé rodiny",
        "Energetická udržitelnost (solární panely, tepelná čerpadla)",
        "Regenerace městských částí",
        "Transparentní správa města a digitalizace",
        "Zlepšení kvality vody v rekreačním areálu Dolce",
        "Nový krytý bazén",
    ]},
]

for cat_data in program_data:
    points = cat_data.pop("points")
    cat, _ = ProgramCategory.objects.get_or_create(name=cat_data["name"], defaults=cat_data)
    for i, point_title in enumerate(points):
        ProgramPoint.objects.get_or_create(category=cat, title=point_title, defaults={"order": i})
print(f"Created {len(program_data)} program categories with points")

# Sample events
from datetime import date, time
events_data = [
    {"title": "Setkání s kandidáty na Krakonošově náměstí", "date": date(2026, 8, 15), "time_from": time(14, 0), "time_to": time(17, 0), "location": "Krakonošovo náměstí, Trutnov", "description": "Přijďte se seznámit s našimi kandidáty a probrat, co Trutnov potřebuje."},
    {"title": "Se starostou na pivo", "date": date(2026, 8, 25), "time_from": time(18, 0), "time_to": time(20, 0), "location": "Restaurace Na Hřišti", "description": "Neformální setkání u piva. Přijďte si popovídat o tom, jak vidíte budoucnost Trutnova."},
    {"title": "Veřejná debata o dopravě", "date": date(2026, 9, 5), "time_from": time(17, 0), "time_to": time(19, 0), "location": "Společenské centrum Uffo", "description": "Diskuze o dopravní situaci ve městě, parkování a dálnici D11."},
]

for event_data in events_data:
    Event.objects.get_or_create(title=event_data["title"], defaults=event_data)
print(f"Created {len(events_data)} events")

print("\nDone! You can now run: python manage.py runserver")
print("Admin: http://localhost:8000/admin-panel/")
print("Login: admin / admin123")
