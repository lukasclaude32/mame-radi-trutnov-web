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
candidates_data = [
    {"order": 1, "title_prefix": "Ing. arch.", "first_name": "Michal", "last_name": "Rosa", "party": "ODS", "is_leader": True},
    {"order": 2, "title_prefix": "PhDr.", "first_name": "Jana", "last_name": "Křemenská", "age": 44, "party": "ODS",
     "occupation": "Vedoucí personálního oddělení, koučka osobního rozvoje",
     "bio": "Vede personální oddělení ve výrobní firmě a je koučkou osobního rozvoje. Do Trutnova se přistěhovala za manželem, žije zde přibližně 20 let.",
     "priorities": "Dostupná lékařská péče (zubaři, praktičtí lékaři)\nZvýhodněné vstupné pro obyvatele na kulturu a sport\nBezbariérovost města\nŘešení dopravní situace"},
    {"order": 3, "title_prefix": "Mgr.", "first_name": "Ivan", "last_name": "Adamec", "age": 62, "party": "ODS",
     "occupation": "Poslanec Parlamentu ČR, předseda Hospodářského výboru",
     "bio": "Člen Parlamentu ČR, předseda Hospodářského výboru, krajský a městský zastupitel. Bývalý starosta Trutnova po dobu více než 23 let. Absolvent Pedagogické fakulty Univerzity Karlovy, bývalý učitel a ředitel školy. Člen ODS od roku 1994. V Trutnově od roku 1987.",
     "priorities": "Rozvoj města a infrastruktury\nPodpora vzdělávání a kultury\nTransparentní správa města"},
    {"order": 4, "title_prefix": "Mgr.", "first_name": "Pavel", "last_name": "Káňa", "age": 48, "party": "ODS",
     "occupation": "Učitel matematiky a zeměpisu, Gymnázium Trutnov",
     "bio": "Učitel matematiky a zeměpisu na Gymnáziu Trutnov. Absolvent Univerzity Karlovy.",
     "priorities": "Udržitelný rozvoj města\nModerní vzdělávací technologie\nCyklostezky napojené na Labskou stezku\nNový krytý bazén\nKulturní nabídka\nKvalita vody v rekreačním areálu Dolce\nDálniční obchvat"},
    {"order": 5, "title_prefix": "Ing.", "first_name": "Vladislav", "last_name": "Sauer", "age": 60, "party": "ODS",
     "occupation": "Ředitel Střední průmyslové školy v Trutnově",
     "bio": "Ředitel Střední průmyslové školy v Trutnově, nezávislý zastupitel za ODS. Rodák z Trutnova.",
     "priorities": "Parkování a plynulost dopravy\nRozvoj autobusového nádraží\nBydlení pro mladé\nZlepšení prostředí města\nRekonstrukce chodníků a silnic"},
    {"order": 6, "title_prefix": "Mgr.", "first_name": "Václav", "last_name": "Fišer", "age": 52, "party": "ODS",
     "occupation": "Učitel informatiky a fyziky, ZŠ Komenského",
     "bio": "Učitel informatiky a fyziky na ZŠ Komenského, síťový administrátor a ICT koordinátor. Získal evropské ocenění eTwinning.",
     "priorities": "Vzdělávání a rozvoj technologií\nPodpora technických talentů\nDálniční napojení\nOdpadové hospodářství\nBydlení a udržitelnost\nRekonstrukce infrastruktury"},
    {"order": 7, "title_prefix": "MgA.", "first_name": "Libor", "last_name": "Kasík", "age": 51, "party": "ODS",
     "occupation": "Ředitel Společenského centra Uffo",
     "bio": "Ředitel Společenského centra Uffo (od 2009), městský zastupitel, předseda místní organizace ODS Trutnov, předseda kulturní komise, místopředseda výboru pro kulturu Královéhradeckého kraje.",
     "priorities": "Kultura\nDoprava\nEnergetika (solární panely, tepelná čerpadla)"},
    {"order": 8, "title_prefix": "Mgr.", "first_name": "Jiří", "last_name": "Paták", "age": 59, "party": "ODS",
     "occupation": "Ředitel ZŠ kpt. Jaroše",
     "bio": "Ředitel ZŠ kpt. Jaroše. Rodák z Trutnova. V městském zastupitelstvu od revoluce 1989, více než 30 let služby městu.",
     "priorities": "Projekt Junior-Senior Park na Kryblici\nCyklostezky a in-line stezky\nRozšíření komunikací v Horním Starém Městě\nParkování\nÚdržba infrastruktury"},
    {"order": 9, "first_name": "Lucie", "last_name": "Špetlová", "party": "ODS"},
    {"order": 10, "title_prefix": "Mgr.", "first_name": "Radek", "last_name": "Horák", "age": 46, "party": "ODS",
     "occupation": "Vedoucí sportovišť MEBYS",
     "bio": "Vedoucí sportovních zařízení MEBYS. Narozen v Trutnově. Aktivní sportovec s cca 20letou zkušeností v místním sportu. Nezávislý kandidát za ODS.",
     "priorities": "Modernizace sportovních zařízení\nParkování a bydlení\nDostupnost služeb\nPřitažení mladých lidí\nPozice Trutnova jako sportovně-kulturního centra v podhůří Krkonoš"},
    {"order": 11, "first_name": "Juraj", "last_name": "Sucháň", "age": 32, "party": "ODS",
     "occupation": "Obchodní ředitel Toyota, Autostyl",
     "bio": "Obchodní ředitel Toyota v Autostylu, městský zastupitel. Původem z Rudníku.",
     "priorities": "Urychlení stavby dálnice D11\nRozvoj sportu\nBezpečnost města\nSociální služby\nPodnikatelské prostředí a pracovní místa\nVzdělávání"},
    {"order": 12, "title_prefix": "MUDr.", "first_name": "Jiří", "last_name": "David", "age": 67, "party": "ODS",
     "occupation": "Lékař, provozuje chirurgickou praxi od 1993",
     "bio": "Lékař s chirurgickou praxí od roku 1993. V Trutnově 40 let. Městský zastupitel, působí od roku 1990.",
     "priorities": "Dopravní infrastruktura\nNemocnice a zdravotní služby\nRegenererace města\nTransparentnost radnice\nDigitalizace\nOdpovědnost občanů"},
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
