from django.urls import path
from .views import (
    dashboardView, noteView, createNoteView, notesListView, 
    shareNoteView, deleteNoteView, upgradeView
)

urlpatterns = [
    path('', dashboardView, name='dashboard'),
    path('note/<int:note_id>/', noteView, name='note_detail'),
    path('create-note/', createNoteView, name='create_note'),
    path('notes/', notesListView, name='notes_list'),
    path('note/<int:note_id>/share/', shareNoteView, name='share_note'),
    path('note/<int:note_id>/delete/', deleteNoteView, name='delete_note'),
    path('upgrade/', upgradeView, name='upgrade'),
]
