from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Админ-класс для кастомной модели пользователя User.

    Attributes
    ----------
    list_display : tuple
        Поля, отображаемые в списке пользователей.
    list_filter : tuple
        Поля для фильтрации списка пользователей.
    search_fields : tuple
        Поля, по которым выполняется поиск.
    ordering : tuple
        Поля для сортировки пользователей в списке.
    fieldsets : tuple
        Группы полей для отображения в карточке пользователя.
    add_fieldsets : tuple
        Группы полей при создании нового пользователя через админку.
    """
    list_display = ('email', 'full_name','is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name', 'middle_name')
    ordering = ('last_name',)

    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'middle_name')}),
        ('Разрешения', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'middle_name', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )

    readonly_fields = ('created_at', 'updated_at', 'last_login')