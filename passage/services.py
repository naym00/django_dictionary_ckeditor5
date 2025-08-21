from word.serializers.GET import serializer as SR_WORD
from help.common.generic import ghelp

class PassageService:
    def get_user_passage_words(self, request, user_passage):
        filter_dict = ghelp.prepare_word_filter_dict(
            request.user,
            {'attribute': 'level', 'value': request.GET.get('complexity', '0')},
            new={'attribute': 'created_at__gte', 'value': request.GET.get('keyword')},
            search={'attribute': 'word__text__icontains', 'value': request.GET.get('search')},
            extra={'word__word_passages__passage_id': user_passage.passage.id}
        )
        return request.user.user_words.filter(**filter_dict).distinct().order_by('-id')
    
    def serialized_user_passage_words(self, words):
        return SR_WORD.UserWordSerializer(words, many=True).data

passage_service = PassageService()