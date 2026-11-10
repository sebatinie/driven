from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from userportal.accounts.models import User, Profile, Settings


def get_user_data(request, user_id):
    try:
        # Fetch user
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": f"User with id {user_id} not found"},
                status=404
            )

        # Fetch profile
        try:
            profile = Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": f"Profile for user {user_id} not found"},
                status=404
            )

        # Fetch settings
        try:
            settings = Settings.objects.get(user=user)
        except ObjectDoesNotExist:
            return JsonResponse(
                {"error": f"Settings for user {user_id} not found"},
                status=404
            )

        return JsonResponse({
            "status": "success",
            "user": {
                "id": user.id,
                "username": user.username
            },
            "profile": {
                "bio": profile.bio
            },
            "settings": {
                "theme": settings.theme
            }
        }, status=200)

    except ObjectDoesNotExist as e:
        return JsonResponse(
            {"error": str(e)},
            status=404
        )