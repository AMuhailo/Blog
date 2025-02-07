import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user , venv, actions = None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id = user.id, 
                                            venv = venv, 
                                            created__gte = last_minute)
    if actions:
        action_ct = ContentType.objects.get_for_model(actions)
        similar_actions = similar_actions.filter(action_ct = action_ct,
                                                 action_id = actions.id)
    if not similar_actions:
        action = Action(user = user, venv = venv, actions = actions)
        action.save()
        return True
    return False