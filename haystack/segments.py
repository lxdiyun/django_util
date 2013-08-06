from django.utils.encoding import smart_str, smart_unicode
try:
    from django.utils import importlib
except ImportError:
    from haystack.utils import importlib


def mmseg_segment(string):
    mmseg_module = importlib.import_module("mmseg")
    output = " ".join(mmseg_module.seg_txt(smart_str(string)))

    return smart_unicode(output)


def jieba_segment(string):
    jieba_module = importlib.import_module("jieba")
    output = " ".join(jieba_module.cut_for_search(string))

    return output


def segment(string):
    return mmseg_segment(string)
