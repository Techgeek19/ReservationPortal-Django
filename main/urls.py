from django.urls import path
from django.urls import include
from . import views
from .views import TableListView, BookingListView, TableDetailView, CancelBookingView, update_view
from django.contrib.auth.decorators import login_required

app_name = "main"

urlpatterns = [
    # path('main/', login_required(views.home), name='main'),       # for adding a new book
    # path('main/search/', views.search_note, name='search_note'),
    # path('main/<slug:slug>/', login_required(views.get_note_details), name='note_detail'),
    # path('main/<int:pk>/delete/', login_required(views.delete_note), name='delete_single_note'),
    # path('main/<int:pk>/delete/confirm/', login_required(views.confirm_delete_note), name='confirm_delete_note'),
    # path('main/<int:pk>/edit/', login_required(views.edit_note_details), name='note_details_edit'),
    # path('main/<slug:slug>/pdf/', login_required(views.generate_pdf), name='note_as_pdf'),
    # path('main/share/<str:signed_pk>/', views.get_shareable_link, name='share_main'),
    # path('tags/<slug:slug>/', views.get_all_main_tags, name='get_all_main_tags'),
    path('table_list/', TableListView, name='TableListView'),
    path('booking_list/', login_required(BookingListView.as_view()), name='BookingListView'),
    path('table/<category>', login_required(TableDetailView.as_view()), name='TableDetailView'),
    path('booking/edit/<id>', update_view,
         name='EditBookingView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(),
         name='CancelBookingView'),         
    path('', views.home, name='home')
]
