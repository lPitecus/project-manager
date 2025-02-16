import datetime

from users.models import Profile


def user_gender_greeting(request):
    """
    Adds a 'greeting' based on user gender to the context for templates.
    """
    if request.user.is_authenticated:
        try:
            # Access the user's profile and its gender field
            profile = request.user.profile  # Assumes a related name of "profile"
            if profile.gender == "M":  # Masculine
                greeting = "Bem Vindo"
            elif profile.gender == "F":  # Feminine
                greeting = "Bem Vinda"
            else:
                greeting = "Bem Vinde"  # Neutral or "Outro"
        except Profile.DoesNotExist:
            # If no profile exists (failsafe), add a default behavior
            greeting = "Bem Vindo/a"
    else:
        greeting = ""  # Not logged in or anonymous user

    return {"greeting": greeting}


def get_current_datetime(request):
    return {"current_datetime": datetime.datetime.now()}
