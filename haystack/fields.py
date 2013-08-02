from haystack.fields import CharField
from jieba import cut_for_search


class ZhCharField(CharField):

    def __init__(self, **kwargs):
        super(ZhCharField, self).__init__(**kwargs)

        self.is_multivalued = True

    def convert(self, value):
        convered_value = super(ZhCharField, self).convert(value)

        return list(cut_for_search(convered_value))
