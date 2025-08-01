from django.db.models import Q
from help.common.l import L
from itertools import chain
import math

class K(L):
    def get_passages_to_display(self, Userfriend, Userpassage, loggedin_user):
        friend_ids = self.get_friends(Userfriend, loggedin_user)
        
        friend_passages = Userpassage.objects.filter(
            Q(user__in=friend_ids) & (
                Q(audience__in=['Public', 'Friend']) |
                Q(audience='Custom', audience_user_passages__user=loggedin_user)
            )
        ).order_by('?').exclude(
            passage__in=loggedin_user.user_passages.all().values_list('passage', flat=True)
        ).select_related('passage', 'user').distinct()
        
        non_friend_passages = Userpassage.objects.filter(
            Q(audience='Public') & ~Q(user__in=friend_ids)
        ).order_by('?').exclude(
            passage__in=loggedin_user.user_passages.all().values_list('passage', flat=True)
        ).select_related('passage', 'user').distinct()[:math.ceil((friend_passages.count()*30)/70)]
        
        return list(chain(friend_passages, non_friend_passages))
    
    def update_new_word_filter_dict(self, loggedin_user, filter_dict):
        user_settings = self.get_user_settings(loggedin_user)
        if user_settings:
            filter_dict.update(
                {
                    'created_at__gte': self.n_days_back_datetime(
                        n_days=user_settings.new_word_day_duration,
                        zone=self.dhaka_timezone
                    )
                }
            )