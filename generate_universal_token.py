from django.contrib.auth.models import User

# Create a universal API user if not exists
user, created = User.objects.get_or_create(username='universal_api_user')
if created:
    user.set_password('universal_password')
    user.save()
