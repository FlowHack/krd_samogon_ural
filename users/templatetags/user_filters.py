from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    css = css.split('&')
    if len(css) == 2:
        return field.as_widget(attrs={'class': css[0], 'style': css[1]})

    return field.as_widget(attrs={'class': css[0]})
