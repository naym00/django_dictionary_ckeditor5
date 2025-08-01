from help.common.k import K
class J(K):
    def prepare_word_filter_dict(self, Settings, complexity, keyword):
        filter_dict = {}
        # if complexity in ['-1', '0']:
        #     if complexity == '-1': self.update_new_word_filter_dict(Settings, filter_dict)
        # else: filter_dict.update({'level': complexity})
        # if complexity != '-1':
        #     if keyword == 'new': self.update_new_word_filter_dict(Settings, filter_dict)
        
        if complexity != '0': filter_dict.update({'level': complexity})
        if keyword == 'new': self.update_new_word_filter_dict(Settings, filter_dict)
        return filter_dict