from haystack.fields import CharField
from segment import jieba_segment


class ZhCharField(CharField):

    def convert(self, value):
        convered_value = super(ZhCharField, self).convert(value)

        return jieba_segment(convered_value)
