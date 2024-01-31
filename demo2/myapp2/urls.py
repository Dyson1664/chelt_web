from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("day1/", views.day1, name="day1"),
    path("day2/", views.day2, name="day2"),
    path("day3/", views.day3, name="day3"),
    path("day4/", views.day4, name="day4"),
    path("top5/", views.top5, name="top5"),
    path("base/", views.base, name="base"),
    path("practice/", views.practice, name="practice"),
    path("races/", views.races, name="races"),
    path('results/', views.results, name='results'),
    path('test/', views.test, name='test'),
    path('test-cache/', views.test_cache, name='test_cache'),

]

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)