from django import template
from markdown import markdown
from markdownx.settings import MARKDOWNX_MARKDOWN_EXTENSIONS, MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS


register = template.Library()

@register.filter(name='markdownify')
def markdownify(content):
    return  markdown(
        text=content,
        extensions=MARKDOWNX_MARKDOWN_EXTENSIONS,
        extension_configs=MARKDOWNX_MARKDOWN_EXTENSION_CONFIGS
    )
