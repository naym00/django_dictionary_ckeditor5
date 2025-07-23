from django.core.mail import EmailMessage
from datetime import datetime, date, timedelta
from django.db.models import Q
from help.common.o import O
import pytz

class N(O):
    def get_timezone(self, zone='utc'):
        time_zone = None
        if zone == 'utc': time_zone = pytz.UTC
        else:
            try: time_zone = pytz.timezone(zone)
            except: pass
        return time_zone
    
    def list_to_tuple(self, demo_list):
        return tuple(map(lambda a: (a, a), demo_list))
    
    def get_unique_code(self):
      return f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"[:18]
  
    def get_settings(self, Settings):
        settings = Settings.objects.all()
        if settings.exists(): return settings.first()
        else: return None
    
    def send_mail_including_attatchment(self, subject, message, recipient_list, attachments=[], email_from = None):
        flag = False
        try:
            email = EmailMessage(subject, message, email_from, recipient_list)
            for attachment in attachments:
                email.attach_file(attachment)
            flag = bool(email.send())
        except: flag = False
        return flag
    
    def nav_links(self, key='home', user=None):
        links = {
            'home': {'level': 'Home' if user == None else user.short_name if user.is_authenticated else 'Home', 'link': '/'},
            'login': {'level': 'Login', 'link': '/auth/login'},
            'register': {'level': 'Register', 'link': '/auth/register'},
            'logout': {'level': 'Logout', 'link': '/auth/logout'},
            'forgot_password': {'level': 'Forgot Password', 'link': '/auth/forgot-password'},
            'words': {'level': 'Word-Meaning', 'link': '/word/words'},
            'word_details': {'level': 'Word-Meaning-Example', 'link': '/word/word-details'},
            'easy_words': {'level': 'Easy', 'link': '/word/easy-words'},
            'medium_words': {'level': 'Medium', 'link': '/word/medium-words'},
            'hard_words': {'level': 'Hard', 'link': '/word/hard-words'},
            'new_words': {'level': 'New Words', 'link': '/word/new-words'},
            'view_passage': {'level': 'View Passage', 'link': '/passage/get-passages'},
            'add_passage': {'level': 'Add Passage', 'link': '/passage/add-passage'},
        }
        return links[key] if key in links else '#'
    
    def get_friends(self, Userfriend, loggedin_user, id=True):
        if id: return [user_id for pair in Userfriend.objects.filter(Q(user=loggedin_user) | Q(friend=loggedin_user)).values('user', 'friend') for user_id in pair.values() if user_id != loggedin_user.id]
        else:
            friends = []
            for user_friend in Userfriend.objects.filter(Q(user=loggedin_user) | Q(friend=loggedin_user)):
                if user_friend.user.id == loggedin_user.id: friends.append(user_friend.friend)
                else: friends.append(user_friend.user)
            return friends
    
    def get_fields_name(self, model):
        return [field.name for field in model._meta.get_fields()]