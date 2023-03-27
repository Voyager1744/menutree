from django import template
from django.urls import reverse

from menu.models import Menu, MenuItem

register = template.Library()


@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    # Получаем текущий путь URL из контекста
    current_path = context['request'].path

    # Получаем меню из БД по названию
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return ''

    # Получаем корневые элементы меню
    root_items = MenuItem.objects.filter(menu=menu, parent=None)

    # Рекурсивно обходим элементы меню и строим дерево
    def build_tree(menu_items, is_active_parent=False):
        result = ''
        for item in menu_items:
            is_active = current_path.startswith(item.url)
            children = MenuItem.objects.filter(menu=menu, parent=item)
            has_children = children.exists()
            item_url = reverse(item.url) if not item.url.startswith(
                '/') else item.url
            item_html = f'<a href="{item_url}" class="{"active" if is_active else ""}">{item.name}</a>'
            if has_children:
                item_html += build_tree(children, is_active)
            result += f'<li class="{ "active" if is_active or is_active_parent else ""}">{item_html}</li>'
        return f'<ul>{result}</ul>'

    # Строим дерево
    menu_html = build_tree(root_items)

    return menu_html
