from users.models import UserProfile


def color_user(request):
    profile = UserProfile.objects.filter(user_id=request.user.id).prefetch_related("rank").first()
    return {"profile_header": profile}
