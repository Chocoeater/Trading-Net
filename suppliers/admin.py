from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from suppliers.models import Node, Product

admin.site.register(Product)

class ProductInline(admin.TabularInline):
    """
    Встроенный админ-класс для отображения продуктов в карточке узла сети.

    Parameters
    ----------
    model : Model
        Модель, которая будет отображаться inline (Product).
    extra : int
        Количество пустых форм для добавления новых записей (0 = нет).
    """
    model = Product
    extra = 0

@admin.action(description='Очистить задолженность перед поставщиком')
def clear_debt(modeladmin, request, queryset):
    """
    Админ-действие для обнуления задолженности у выбранных узлов.

    Parameters
    ----------
    modeladmin : ModelAdmin
        Текущий класс ModelAdmin.
    request : HttpRequest
        Объект запроса.
    queryset : QuerySet
        Выбранные объекты Node.

    Notes
    -----
    Выводит сообщение пользователю о количестве обновлённых объектов.
    """
    updated = queryset.update(debt=0)
    modeladmin.message_user(request, f"Обнулено задолженности у {updated} объектов.")

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    """
    Админ-класс для модели Node.

    Attributes
    ----------
    list_display : tuple
        Поля, отображаемые в списке объектов.
    list_filter : tuple
        Поля для фильтрации.
    search_fields : tuple
        Поля для поиска.
    actions : list
        Список действий для выбранных объектов.
    inlines : list
        Встроенные модели (ProductInline).
    """
    list_display =  ('name', 'city', 'country', 'debt', 'level_display', 'supplier_link')
    list_filter = ('city', 'country')
    search_fields = ('name', 'city', 'country')
    actions = [clear_debt]
    inlines = [ProductInline]

    def supplier_link(self, obj):
        """
        Отображает ссылку на поставщика узла в админке.

        Parameters
        ----------
        obj : Node
            Узел, для которого строится ссылка.

        Returns
        -------
        str
            HTML-ссылка на карточку поставщика или '-' если поставщика нет.
        """
        if obj.supplier:
            url = reverse(
                f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change',
                args=[obj.supplier.pk]
            )
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '-'

    supplier_link.short_description = 'Поставщик'

    def level_display(self, obj):
        """
        Отображает уровень узла в списке объектов админки.

        Parameters
        ----------
        obj : Node
            Узел, для которого выводится уровень.

        Returns
        -------
        int
            Уровень узла.
        """
        return obj.level

    level_display.short_description = 'Уровень'

