from django.urls import path
from web import views

urlpatterns = [
    # Frontend
    path("", views.home, name="home"),
    path("o-nas/", views.about, name="about"),
    path("kandidati/", views.candidates_list, name="candidates"),
    path("kandidati/<int:pk>/", views.candidate_detail, name="candidate_detail"),
    path("program/", views.program, name="program"),
    path("udalosti/", views.events_list, name="events"),
    path("aktuality/", views.posts_list, name="posts"),
    path("aktuality/<slug:slug>/", views.post_detail, name="post_detail"),
    path("podporovatele/", views.supporters, name="supporters"),
    path("galerie/", views.gallery, name="gallery"),
    path("galerie/<slug:slug>/", views.album_detail, name="album_detail"),
    path("kontakt/", views.contact, name="contact"),

    # Admin Panel
    path("admin-panel/login/", views.admin_login, name="admin_login"),
    path("admin-panel/logout/", views.admin_logout, name="admin_logout"),
    path("admin-panel/", views.admin_dashboard, name="admin_dashboard"),

    path("admin-panel/kandidati/", views.admin_candidates, name="admin_candidates"),
    path("admin-panel/kandidati/novy/", views.admin_candidate_create, name="admin_candidate_create"),
    path("admin-panel/kandidati/<int:pk>/", views.admin_candidate_edit, name="admin_candidate_edit"),
    path("admin-panel/kandidati/<int:pk>/smazat/", views.admin_candidate_delete, name="admin_candidate_delete"),

    path("admin-panel/udalosti/", views.admin_events, name="admin_events"),
    path("admin-panel/udalosti/nova/", views.admin_event_create, name="admin_event_create"),
    path("admin-panel/udalosti/<int:pk>/", views.admin_event_edit, name="admin_event_edit"),
    path("admin-panel/udalosti/<int:pk>/smazat/", views.admin_event_delete, name="admin_event_delete"),

    path("admin-panel/prispevky/", views.admin_posts, name="admin_posts"),
    path("admin-panel/prispevky/novy/", views.admin_post_create, name="admin_post_create"),
    path("admin-panel/prispevky/<int:pk>/", views.admin_post_edit, name="admin_post_edit"),
    path("admin-panel/prispevky/<int:pk>/smazat/", views.admin_post_delete, name="admin_post_delete"),

    path("admin-panel/program/", views.admin_program, name="admin_program"),
    path("admin-panel/program/kategorie/nova/", views.admin_program_category_create, name="admin_program_category_create"),
    path("admin-panel/program/kategorie/<int:pk>/", views.admin_program_category_edit, name="admin_program_category_edit"),
    path("admin-panel/program/kategorie/<int:pk>/smazat/", views.admin_program_category_delete, name="admin_program_category_delete"),
    path("admin-panel/program/bod/novy/", views.admin_program_point_create, name="admin_program_point_create"),
    path("admin-panel/program/bod/<int:pk>/", views.admin_program_point_edit, name="admin_program_point_edit"),
    path("admin-panel/program/bod/<int:pk>/smazat/", views.admin_program_point_delete, name="admin_program_point_delete"),

    path("admin-panel/podporovatele/", views.admin_supporters, name="admin_supporters"),
    path("admin-panel/podporovatele/novy/", views.admin_supporter_create, name="admin_supporter_create"),
    path("admin-panel/podporovatele/<int:pk>/", views.admin_supporter_edit, name="admin_supporter_edit"),
    path("admin-panel/podporovatele/<int:pk>/smazat/", views.admin_supporter_delete, name="admin_supporter_delete"),

    path("admin-panel/galerie/", views.admin_gallery, name="admin_gallery"),
    path("admin-panel/galerie/album/nove/", views.admin_album_create, name="admin_album_create"),
    path("admin-panel/galerie/album/<int:pk>/", views.admin_album_edit, name="admin_album_edit"),
    path("admin-panel/galerie/album/<int:pk>/smazat/", views.admin_album_delete, name="admin_album_delete"),
    path("admin-panel/galerie/album/<int:album_pk>/nahrat/", views.admin_photo_upload, name="admin_photo_upload"),
    path("admin-panel/galerie/foto/<int:pk>/smazat/", views.admin_photo_delete, name="admin_photo_delete"),
    path("admin-panel/galerie/video/nove/", views.admin_video_create, name="admin_video_create"),
    path("admin-panel/galerie/video/<int:pk>/", views.admin_video_edit, name="admin_video_edit"),
    path("admin-panel/galerie/video/<int:pk>/smazat/", views.admin_video_delete, name="admin_video_delete"),

    path("admin-panel/zpravy/", views.admin_messages_list, name="admin_messages"),
    path("admin-panel/zpravy/<int:pk>/", views.admin_message_detail, name="admin_message_detail"),
    path("admin-panel/zpravy/<int:pk>/smazat/", views.admin_message_delete, name="admin_message_delete"),

    path("admin-panel/nastaveni/", views.admin_settings, name="admin_settings"),
]
