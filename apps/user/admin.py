from django.contrib import admin
from django.utils.translation import ugettext as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import Usuario


@admin.register(Usuario)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    def groups_display(self, obj):
        return ', '.join([
            group.name for group in obj.groups.all()
        ])
    groups_display.short_description = 'Grupos'

    list_display = ('email', 'name', 'date_joined', 'is_superuser', 'is_active', )
    list_filter = ('email', 'name', 'date_joined', 'is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Informações pessoais'), {'fields': ('name', )}),
        (_('Permissões'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        (_('Datas importantes'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2')}
         ),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['last_login', 'date_joined', ]
        else:
            return ['last_login', 'date_joined', ]
