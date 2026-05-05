import os
from django.contrib.auth import get_user_model

User = get_user_model()
    # You can change these details
username = 'admin'
email = 'clementcrownrise@gmail.com'
password = 'YourSecurePassword123'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superuser {username} created.")
else:
    print(f"Superuser {username} already exists.")