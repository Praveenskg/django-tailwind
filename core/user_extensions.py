from django.contrib.auth import get_user_model


def get_avatar_url(self):
    profile = getattr(self, "profile", None)
    if profile is None:
        return None
    if not profile.avatar:
        return None
    return profile.avatar.url


def patch_user_model():
    User = get_user_model()
    if not hasattr(User, "avatar_url"):
        User.add_to_class("avatar_url", property(get_avatar_url))
