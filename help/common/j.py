from help.common.k import K
class J(K):
    def prepare_word_filter_dict(self, loggedin_user, complexity, keyword, search):
        filter_dict = {}
        if complexity != '0': filter_dict.update({'level': complexity})
        if keyword == 'new': self.update_new_word_filter_dict(loggedin_user, filter_dict)
        if search: filter_dict.update({'word__text__icontains': search})
        return filter_dict