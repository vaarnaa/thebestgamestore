from .models import User, Player, Developer
from django.shortcuts import redirect
from social_core.pipeline.partial import partial
from .views import get_user_type


def make_user_by_type(strategy, backend, response, user=None, *args, **kwargs):
    user_type = strategy.session_get('user_type', None)

    if user and user_type == 'player':
        user.is_player = True
        user.is_social = True
        user.save()
        player = Player.objects.filter(user=user)
        if not player:
            Player.objects.create(user=user)

    elif user and user_type == 'developer':
        user.is_developer = True
        user.is_social = True
        user.save()
        developer = Developer.objects.filter(user=user)
        if not developer:
            Developer.objects.create(user=user)

    # continue the pipeline
    return


# partial says "we may interrupt, but we will come back here again"
@partial
def collect_user_type(strategy, request, backend, details, user=None, is_new=False, *args, **kwargs):

    # session 'user_type' is set by the pipeline infrastructure
    # because it exists in FIELDS_STORED_IN_SESSION
    user_type = strategy.session_get('user_type', None)
    request.session['backend_name'] = backend.name

    # if user not created yet and user_type not determined redirect to usertype selection view
    if not user and user_type != 'player' and user_type != 'developer':
        # if we return something besides a dict or None, then that is
        # returned to the user -- in this case we will redirect to a
        # view that can be used to get a password
        #return redirect('/signup/select_user_type')
        return redirect(get_user_type)

    # if user created but not associated with type redirect to usertype selection view
    if user:
        if not (user.is_player or user.is_developer):
            return redirect(get_user_type)

    # continue the pipeline
    return
