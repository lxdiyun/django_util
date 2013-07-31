# -*- coding: utf-8 -*-
from haystack.utils.highlighting import Highlighter
from re import search


class HighlighterBase(Highlighter):
    html_tag = "b"
    css_class = ""


class SummaryHighlighter(HighlighterBase):
    """ Highlighter with summary """

    min_length = 100
    max_length = 100

    def __init__(self, query, **kwargs):
        super(SummaryHighlighter, self).__init__(query, **kwargs)

        if 'min_length' in kwargs:
            self.min_length = int(kwargs['max_length'])

    def find_window(self, highlight_locations):
        best_start, best_end = super(SummaryHighlighter,
                                     self).find_window(highlight_locations)
        if 0 < best_start:
            min_end = min(len(self.text_block), best_end)
            min_start = min_end - self.min_length
            min_start = max(0, min_start)
            search_pos = min(min_start, best_start)
            sentence_separator = ur"[ ,.，。]"
            reg = r"(" + sentence_separator + r")(?!.*\1.*)"
            result = search(reg, self.text_block[:search_pos])
            if result:
                best_start = result.start() + 1
            else:
                best_start = 0

        return (best_start, best_end)


class CompleteHighlighter(HighlighterBase):
    """ Highlighter without omit """

    def highlight(self, text_block):
        block_len = len(text_block)
        if 0 < block_len:
            self.max_length = block_len
        else:
            self.max_length = 1
        return super(CompleteHighlighter, self).highlight(text_block)

    def find_window(self, highlight_locations):
        return (0, self.max_length)
