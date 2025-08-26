from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Note, UserProfile

@login_required
def dashboardView(request):
    # notes and tasks
    user_notes = Note.objects.filter(owner=request.user)[:5]
    shared_notes = Note.objects.filter(shared_with=request.user)[:5]

    # get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    # check if user can create more than 5 notes
    can_create_notes = True
    if not profile.is_premium:
        user_note_count = user_notes.count()
        can_create_notes = user_note_count < 5

    context = {
        'notes': user_notes,
        'shared_notes': shared_notes,
        'profile': profile,
        'note_count': user_notes.count(),
        'can_create_notes': can_create_notes,
    }
    return render(request, 'pages/dashboard.html', context)

# OWASP A01: Broken Access Control
# no ownership validation, anyone can access any note by ID
@login_required
def noteView(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    # SECURE VERSION: checking if request.user == note.owner (commented out):
    # if note.owner != request.user and not note.is_public:
    #     return redirect('dashboard')

    return render(request, 'pages/note_detail.html', {'note': note})

# OWASP A04: Insecure Design
# no content size validation
# someone can essentially store gigabytes of data in the notes
@login_required
def createNoteView(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        # SECURE VERSION: limit note content size (commented out):
        # if len(content) > 10000:
        #     return render(request, 'pages/create_note.html', {
        #         'error': 'Note content too large. Maximum 10KB allowed.'
        #     })

        note = Note.objects.create(
            title=title,
            content=content,
            owner=request.user
        )

        return redirect('note_detail', note_id=note.id)

    return render(request, 'pages/create_note.html')

@login_required
def notesListView(request):
    notes = Note.objects.filter(owner=request.user)
    return render(request, 'pages/notes_list.html', {'notes': notes})

@login_required
def shareNoteView(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)

    if request.method == 'POST':
        username = request.POST.get('share_with')
        try:
            user_to_share = User.objects.get(username=username)
            if user_to_share != request.user:
                note.shared_with.add(user_to_share)
                note.is_shared = True
                note.save()
                return redirect('note_detail', note_id=note.id)
        except User.DoesNotExist:
            return render(request, 'pages/share_note.html', {
                'note': note, 'error': 'User not found'
            })

    users = User.objects.exclude(id=request.user.id)
    return render(request, 'pages/share_note.html', {'note': note, 'users': users})

@login_required
def deleteNoteView(request, note_id):
    note = get_object_or_404(Note, id=note_id, owner=request.user)

    if request.method == 'POST':
        note.delete()
        return redirect('dashboard')

    return render(request, 'pages/confirm_delete.html', {'note': note})

# OWASP A05: Security Misconfiguration
# @csrf_exempt allows easy bypass of CSRF security
# based on Securing Software exercise 20 Bad configuration
# SECURE VERSION: remove @csrf_exempt
# we could also apply csrf_protect but Django applies it automatically
@login_required
@csrf_exempt
def upgradeView(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    note_count = Note.objects.filter(owner=request.user).count()

    if request.method == 'POST':
        # technically OWASP A04 as there is no payment validation
        # but it would require actually creating payment validation for this project
        profile.is_premium = True
        profile.save()
        return redirect('dashboard')

    return render(request, 'pages/upgrade.html', {
        'profile': profile,
        'note_count': note_count
    })
