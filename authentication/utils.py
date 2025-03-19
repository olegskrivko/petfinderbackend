import random
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model  # ✅ Get the correct user model
User = get_user_model()  # ✅ Use CustomUser instead of auth.User
# Adjectives & pet names for unique usernames
ADJECTIVES = ["Happy", "Clever", "Swift", "Brave", "Loyal", "Gentle", "Curious", "Playful", "Furry", "Energetic"]
PET_NAMES = ["Fox", "Puppy", "Kitten", "Otter", "Bunny", "Parrot", "Hound", "Whiskers", "Lion", "Dolphin"]

def generate_hex_username(max_attempts=10):
    """Generate a unique pet-themed username with a 6-digit hex code."""
    adjective = random.choice(ADJECTIVES)
    pet = random.choice(PET_NAMES)

    for _ in range(max_attempts):  # Try up to 10 times
        hex_code = f"{random.randint(0, 0xFFFFFF):06X}"  # Generate 6-digit hex (000000-FFFFFF)
        username = f"{adjective}{pet}_{hex_code}"  # Example: "HappyFox_A1B2C3"

        if not User.objects.filter(username=username).exists():
            return username  # ✅ Unique username found

    return f"User_{random.randint(100000, 999999)}"  # Fallback username

# For millions of users, expand hex from 6 to 8 digits (00000000 → FFFFFFFF)
# hex_code = f"{random.randint(0, 0xFFFFFFFF):08X}"  # Generates 8-character hex

