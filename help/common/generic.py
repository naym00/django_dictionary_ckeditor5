from help.common.h import H
from django.db.models import Q
class Generic(H):
    def users_to_send_friend_request(self, User, Userfriend, Friendrequest, loggedin_user):
        # Users who are already friends (either direction)
        friend_ids = Userfriend.objects.filter(
            Q(user=loggedin_user) | Q(friend=loggedin_user)
        ).values_list('user_id', 'friend_id')
        
        # Flatten the list of IDs and remove duplicates and the current user
        friend_ids = {id for pair in friend_ids for id in pair if id != loggedin_user.id}
        
        # Users with pending requests (either as sender or receiver)
        pending_ids = Friendrequest.objects.filter(
            Q(user=loggedin_user) | Q(requested_to=loggedin_user)
        ).values_list('user_id', 'requested_to_id')
        
        # Flatten the list of IDs and remove duplicates and the current user
        pending_ids = {id for pair in pending_ids for id in pair if id != loggedin_user.id}
        
        # Combine both sets of IDs to exclude
        excluded_ids = friend_ids.union(pending_ids)
        
        # Get all users except yourself and those in excluded_ids
        potential_friends = User.objects.exclude(
            Q(id=loggedin_user.id) | Q(id__in=excluded_ids) | Q(is_superuser=True)
        )
        return potential_friends

ghelp = Generic()