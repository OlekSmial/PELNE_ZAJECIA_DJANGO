
from django.urls import path, include
from . import views

urlpatterns = [
    path('persons/', views.person_list),
    path('persons/<int:pk>/', views.person_detail),
    path('persons/update/<int:pk>/', views.person_update),
    path('persons/delete/<int:pk>/', views.person_delete),
    path('welcome/', views.welcome_view),
    path('persons_html/', views.person_list_html),
    path('persons_html/<int:id>/', views.person_detail_html),
    path('osoby/', views.osoba_list),
    path('osoby/<int:pk>/', views.osoba_detail),
    path('osoby/search/<str:substring>/', views.osoba_search),
    path('team<int:pk>/', views.TeamDetail.as_view(),name = 'team_detail')
]