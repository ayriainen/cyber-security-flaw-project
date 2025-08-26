from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from src.pages.models import UserProfile, Note

class Command(BaseCommand):
    help = 'Set up demo data'

    def handle(self, *args, **options):
        self.stdout.write('Setup demo initiated\n')

        # test users
        users_data = [
            {'username': 'alice', 'email': 'alice@example.com', 'is_premium': False},
            {'username': 'bob', 'email': 'bob@example.com', 'is_premium': True},
            {'username': 'charlie', 'email': 'charlie@example.com', 'is_premium': False},
        ]

        for user_data in users_data:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='password123',
                    email=user_data['email'],
                    first_name=username.capitalize(),
                    last_name='Demo'
                )

                UserProfile.objects.create(
                    user=user,
                    is_premium=user_data['is_premium']
                )

                premium_status = "Premium" if user_data["is_premium"] else "Basic"
                self.stdout.write(f'Created user: {username} ({premium_status})')
            else:
                self.stdout.write(f'User {username} already exists')

        # test notes
        alice = User.objects.get(username='alice')
        bob = User.objects.get(username='bob')
        charlie = User.objects.get(username='charlie')

        sample_notes = [
            {
                'title': "headlock throws",
                'content': ("head-and-arm throw, the belly-to-side suplex"),
                'owner': alice
            },
            {
                'title': "work reminders", 
                'content': ("project deadline friday, team meeting at noon"),
                'owner': alice
            },
            {
                'title': "Doctor Appointment",
                'content': ("Dermatology appointment next Tuesday at 2 o'clock. "
                           "Need to discuss the recurring rash issue."),
                'owner': bob
            },
            {
                'title': "Quarterly Review",
                'content': ("Performance metrics looking good. Sales targets exceeded by 15%. "
                           "Need to prepare team expansion proposal for next quarter."),
                'owner': bob
            },
            {
                'title': "Elvish",
                'content': ("Quenya root *KALAR 'light' gives us Calacirya, Calaquendi. "
                        "Sindarin equivalent GAL- in Galadriel, Galion. "
                        "Tolkien's linguistic consistency is remarkable across the "
                        "legendarium."),
                'owner': charlie
            }
        ]

        for note_data in sample_notes:
            if not Note.objects.filter(title=note_data['title'], owner=note_data['owner']).exists():
                note = Note.objects.create(**note_data)
                note_title = note_data["title"]
                owner_name = note_data["owner"].username

        # test shared note
        if Note.objects.filter(title="Shared Project Ideas").exists():
            shared_note = Note.objects.get(title="Shared Project Ideas")
        else:
            shared_note = Note.objects.create(
                title="Team Project Planning",
                content=("<h3>Q4 Goals</h3><p> 1. Complete user authentication system<br>"
                        " 2. Implement sharing features<br>"
                        " 3. Security audit scheduled for December</p>"),
                owner=bob,
                is_shared=True
            )
            shared_note.shared_with.add(alice, charlie)

        self.stdout.write(self.style.SUCCESS('\nDemo setup complete'))
        self.stdout.write('\nTest Accounts (password: password123):')
        self.stdout.write('   • alice (Basic user)')
        self.stdout.write('   • bob (Premium user)')
        self.stdout.write('   • charlie (Basic user)')

        self.stdout.write('\nVulnerabilities to test:')
        self.stdout.write('   • A01: Try accessing /note/1/, /note/3/, etc. as different users')
        self.stdout.write("   • A03: Try creating a note with content "
                        "<script>fetch('/upgrade/', {method: 'POST'});</script>")
        self.stdout.write('   • A04: Try posting a whole Project Gutenberg book as a note')
        self.stdout.write('   • A05: Try A01 and then deleting that note of someone else')
        self.stdout.write('   • A07: Check browser cookies for predictable session IDs')

        self.stdout.write(f'\nStart the server: python3 manage.py runserver')
        self.stdout.write(f'   Visit: http://localhost:8000/')
        self.stdout.write('')
