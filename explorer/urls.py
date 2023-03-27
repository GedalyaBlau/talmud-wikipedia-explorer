from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.user_logout, name='logout'),
    path('favorite/<int:talmud_text_id>/', views.add_favorite, name='add_talmud_favorite'),
    path('favorite/wiki/<int:wikipedia_article_id>/', views.add_favorite, name='add_wikipedia_favorite'),
    path('highlight/<int:talmud_text_id>/', views.add_highlight, name='add_talmud_highlight'),
    path('highlight/wiki/<int:wikipedia_article_id>/', views.add_highlight, name='add_wikipedia_highlight'),
    path('comment/talmud/<int:talmud_text_id>/', views.add_comment, name='add_talmud_comment'),
    path('comment/wiki/<int:wikipedia_article_id>/', views.add_comment, name='add_wikipedia_comment'),
    path('search/<str:talmudic_text_ref>/<str:wikipedia_article_title>/', views.home, name='search'),
]
