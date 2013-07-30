# -*- coding: utf-8 -*-
from haystack.utils.highlighting import Highlighter
from re import search


class HighlighterBase(Highlighter):
    html_tag = "b"
    css_class = ""


class SummaryHighlighter(HighlighterBase):
    """ Highlighter with summary """

    def find_window(self, highlight_locations):
        best_start, best_end = super(SummaryHighlighter,
                                     self).find_window(highlight_locations)
        if 0 < best_start:
            sentence_separator = ur"[ ,.，。]"
            reg = r"(" + sentence_separator + r")(?!.*\1.*)"
            result = search(reg, self.text_block[:best_start])
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
