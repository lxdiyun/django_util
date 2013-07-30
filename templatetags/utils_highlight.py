from haystack.templatetags.highlight import HighlightNode
from utils.highlighting import SummaryHighlighter
from django import template


class SummaryHighlightNode(HighlightNode):
    def render(self, context):
        text_block = self.text_block.resolve(context)
        query = self.query.resolve(context)
        kwargs = {}

        if self.html_tag is not None:
            kwargs['html_tag'] = self.html_tag.resolve(context)

        if self.css_class is not None:
            kwargs['css_class'] = self.css_class.resolve(context)

        if self.max_length is not None:
            kwargs['max_length'] = self.max_length.resolve(context)

        highlighter = SummaryHighlighter(query, **kwargs)
        highlighted_text = highlighter.highlight(text_block)

        return highlighted_text


register = template.Library()


@register.tag
def summary_highlight(parser, token):
    """
    Takes a block of text and highlights words from a provided query within
    that block of text. Optionally accepts arguments to provide the HTML tag
    to wrap highlighted word in, a CSS class to use with the tag and a maximum
    length of the blurb in characters.

    Syntax::

        {% summary_highlight <text_block> with <query> [css_class "class_name"] [html_tag "span"] [max_length 200] %}

    Example::

        # Highlight summary with default behavior.
        {% summary_highlight result.summary with request.query %}

        # Highlight summary but wrap highlighted words with a div and the
        # following CSS class.
        {% summary_highlight result.summary with request.query html_tag "div" css_class "highlight_me_please" %}

        # Highlight summary but only show 40 characters.
        {% summary_highlight result.summary with request.query max_length 40 %}
    """
    bits = token.split_contents()
    tag_name = bits[0]

    if not len(bits) % 2 == 0:
        raise template.TemplateSyntaxError(
            u"'%s' tag requires valid pairings arguments." % tag_name)

    text_block = bits[1]

    if len(bits) < 4:
        raise template.TemplateSyntaxError(
            u"'%s' tag requires an object and a query provided by 'with'."
            % tag_name)

    if bits[2] != 'with':
        raise template.TemplateSyntaxError(
            u"'%s' tag's second argument should be 'with'." % tag_name)

    query = bits[3]

    arg_bits = iter(bits[4:])
    kwargs = {}

    for bit in arg_bits:
        if bit == 'css_class':
            kwargs['css_class'] = arg_bits.next()
        
        if bit == 'html_tag':
            kwargs['html_tag'] = arg_bits.next()
        
        if bit == 'max_length':
            kwargs['max_length'] = arg_bits.next()
    
    return SummaryHighlightNode(text_block, query, **kwargs)
