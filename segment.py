from mmseg import seg_txt
from django.utils.encoding import smart_str, smart_unicode


def mmseg_segment(string):
    output = ""

    for term in seg_txt(smart_str(string)):
        output += term.strip() + " "

    return smart_unicode(output.strip())


def segment(string):
    return mmseg_segment(string)
