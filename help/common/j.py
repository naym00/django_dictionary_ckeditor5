from help.common.k import K
class J(K):
    def prepare_word_filter_dict(self, loggedin_user, complexity, new=None, search=None, meaning_search=None, extra={}):
        filter_dict = {}
        if complexity['value'] != '0': filter_dict.update({complexity['attribute']: complexity['value']})
        if new:
            if new['value'] == 'new': self.update_new_word_filter_dict(new['attribute'], loggedin_user, filter_dict)
        if search:
            if search['value']: filter_dict.update({search['attribute']: search['value'].strip()})
        if meaning_search:
            if meaning_search['value']: filter_dict.update({meaning_search['attribute']: meaning_search['value'].strip()})
        filter_dict.update(extra)
        return filter_dict