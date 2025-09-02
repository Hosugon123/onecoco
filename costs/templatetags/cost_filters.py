from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """分割字符串並返回列表"""
    if not value:
        return []
    return value.split(delimiter)

@register.filter
def get_name(value):
    """從描述中提取名稱（第一個部分）"""
    if not value:
        return ""
    if " - " in value:
        return value.split(" - ")[0]
    return value

@register.filter
def get_unit(value):
    """從描述中提取單位（最後一個部分）"""
    if not value:
        return "-"
    if " - " in value:
        parts = value.split(" - ")
        if len(parts) > 1:
            return parts[-1]
    return "-"