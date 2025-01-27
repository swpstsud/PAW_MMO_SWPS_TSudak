from django.urls import path
from . import views

urlpatterns = [
    path('postacie/', views.postacie_list, name='postacie_list'),
    path('postacie/<int:pk>/', views.postacie_detail),
    path('postacie/update/<int:pk>/', views.postacie_update),
    path('postacie/delete/<int:pk>/', views.postacie_delete),
    path('osoby/', views.osoba_list),
    path('osoby/<int:pk>/', views.osoba_details),
    path('osoby/search/<str:substring>/', views.osoba_search),
    path('stanowiska/', views.stanowisko_list),
    path('stanowiska/<int:pk>/', views.stanowisko_detail),
    path('welcome/', views.welcome_view),
    path('postacie_html/', views.postacie_list_html),
    path('persons_html/<int:id>/', views.postacie_detail_html),
    path('druzyny_html/', views.druzyna_list_html),
    path('druzyny/<int:id>/', views.druzyna_detail_html, name='druzyna_detail'),
    path('stanowisko/<int:pk>/members/', views.StanowiskoMemberView.as_view()),
    path('api/logout/', views.LogoutView.as_view(), name='api_logout'),
    path('druzyna/<int:pk>/', views.DruzynaDetail.as_view(), name='druzyna_detail'),
    path('register/', views.register_user, name='register_user'),
    path('test_base/', views.test_base),

]