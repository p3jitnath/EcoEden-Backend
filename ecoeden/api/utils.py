from django.conf import settings

def update_score(new_vote, old_vote, obj):    
    
    if new_vote == 0 : 
            if old_vote < 0: obj.downvotes -= 1
            elif old_vote > 0: obj.upvotes -= 1
    elif new_vote > 0 : 
        if old_vote < 0:
            obj.downvotes -= 1
            obj.upvotes += 1
        elif old_vote == 0: obj.upvotes += 1
    elif new_vote < 0 : 
        if old_vote > 0:
            obj.upvotes -= 1
            obj.downvotes += 1
        elif old_vote == 0: obj.downvotes += 1
    
    return obj

def update_user_score(user, **kwargs):
    if 'collect' in kwargs and kwargs["collect"]:
        user.collections += 1
        user.score += settings.SCORE_COLLECT
    elif 'post' in kwargs and kwargs['post']:
        user.posts += 1
        user.score += settings.SCORE_POST
    elif 'verify' in kwargs and kwargs['verify']:
        user.verifications += 1
        user.score += settings.SCORE_VERIFY
    return user

def update_trash_collection_object(obj):
    difference = obj.upvotes - obj.downvotes
    if (difference > settings.THRESHOLD):
        user = update_user_score(obj.collector, collect=True)
        user.save()
        obj.visible = False
        obj.photo.visible = False
    elif obj.downvotes > settings.THRESHOLD:
        obj.visible = False
    return obj