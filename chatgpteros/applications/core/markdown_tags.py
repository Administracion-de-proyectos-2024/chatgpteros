from django import template
import markdown

register = template.Library()

@register.filter(name='render_markdown')
def render_markdown(value):
    return markdown.markdown(value)