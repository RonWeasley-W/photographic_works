from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """将字符串按分隔符拆分"""
    return value.split(delimiter)

@register.filter
def float(value):
    """将字符串转换为浮点数"""
    return float(value)


