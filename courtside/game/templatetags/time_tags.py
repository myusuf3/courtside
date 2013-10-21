from django import template

from delorean import parse

register = template.Library()

class VerbatimNode(template.Node):

    def __init__(self, text):
        self.text = text

    def render(self, context):
        return self.text

def localize_datetime(timezone, string):
    gametime = parse(string)
    gametime.shift(timezone)
    return gametime.datetime.strftime("%Y-%m-%d %I:%M %p")

@register.simple_tag(takes_context=True)
def localize_time(context, string):
    string = str(string)
    timezone = context['timezone']
    return localize_datetime(timezone, string)

@register.tag
def verbatim(parser, token):
    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{%')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append('}}')
        elif token.token_type == template.TOKEN_BLOCK:
            if not text[-1].startswith('='):
                text[-1:-1] = [' ']
            text.append(' %}')
    return VerbatimNode(''.join(text))