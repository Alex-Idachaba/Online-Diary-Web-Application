from django.urls import path
from .views import(
    HomePageView, 
    AboutPageView, 
    entry_list,
    create_entry,
    entry_update,
    entry_delete,
    search,
    EntryDetailView,
)


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('about/', AboutPageView.as_view(), name='about'),
    path('entry-list/', entry_list, name='entry_list'),
    path('new/', create_entry, name='entry_new'),
    path('<uuid:pk>/edit/', entry_update, name='entry_edit'),
    path('<uuid:pk>/delete/>',entry_delete, name='entry_delete'),
    path('search/', search, name='search_results'),
    path('<uuid:pk>', EntryDetailView.as_view(), name='entry_detail'),
]
