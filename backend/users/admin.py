from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from recipes.admin import Admin

from .models import Following, User


# регистрируем кастомную модель юзера и прописываем разрешения для stuff
class UsersAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'username')

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()
        if not is_superuser:
            disabled_fields |= {
                'is_stuff',
                'is_superuser',
                'user_permissions',
            }
        # Запретить пользователям, не являющимся суперпользователями,
        # редактировать свои собственные разрешения
        if (
            not is_superuser
            and obj is not None
            and obj == request.user
            or obj is not None
            and obj.is_superuser
        ):
            disabled_fields |= {
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form


admin.site.register(User, UsersAdmin)
admin.site.register(Following, Admin)
