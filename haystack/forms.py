from haystack.forms import ModelSearchForm
from haystack.inputs import AutoQuery
from haystack.query import SQ
from segment import jieba_segment


class MultiSearchForm(ModelSearchForm):
    def clean(self):
        cleaned_data = super(MultiSearchForm, self).clean()
        q = cleaned_data.get('q')
        q = jieba_segment(q)
#        cleaned_data['q'] = q

        return cleaned_data

#    def search(self):
#        if not self.is_valid():
#            return self.no_query_found()
#
#        if not self.cleaned_data.get('q'):
#            return self.no_query_found()
#
#        terms = self.cleaned_data['q'].split(" ")
#        sq = SQ()
#
#        for term in terms:
#            sq.add(SQ(content=AutoQuery(term)), SQ.AND)
#
#        sqs = self.searchqueryset.filter(sq)
#
#        if self.load_all:
#            sqs = sqs.load_all()
#
#        return sqs
