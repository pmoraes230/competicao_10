from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("home/", views.home, name="home"),
    path("list_user/", views.list_user, name="list_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/<int:id_user>/", views.update_user, name="update_user"),
    path("delete_user/<int:id_user>/", views.delete_user, name="delete_user"),
    
    # evento
    path("deteils_event/<int:id_event>/", views.deteils_event, name="deteils_event"),
    path("delete_event/<int:id_event>/", views.delete_event, name="delete_event"),
    path("register_event/", views.register_event, name="register_event"),
    path("update_event/<int:id_event>/", views.update_event, name="update_event"),
    path("register_client/<int:id_event>/", views.register_client, name="register_client"),
    path("buy_ticket/<int:id_event>/", views.buy_ticket, name="buy_ticket"),
    path("ticket_generate/<int:id_event>/", views.ticket_generate, name="ticket_generate"),
    path("ticket_export/<str:id_ticket>/", views.export_ticket, name="export_ticket"),
    
    # setores
    path("list_setores/<int:id_event>/", views.list_setores, name="lista_setores"),
    path("delete_setor/<int:id_setor>/", views.delete_setor, name="delete_setor"),
    path("register_setor/<int:id_event>/", views.register_setor, name="register_setor"),
    path("update_setor/<int:id_setor>/", views.update_setor, name="update_setor")
]
