from django.contrib import admin
from .models import UserKeys, Server, UserData


class UserKeysAdmin(admin.ModelAdmin):
    fields = ['key_file', ]
    list_display = ['user','key_file']

    class Meta:
        model = UserKeys

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

    def queryset(self, request):
        if request.user.is_superuser:
            return UserKeys.objects.all()
        return UserKeys.objects.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        has_class_permission = super(UserKeysAdmin, self).has_change_permission(request, obj)
        if not has_class_permission:
            return False
        if obj is not None and not request.user.is_superuser and request.user.id != obj.user.id:
            return False
        return True


class UserDataAdmin(admin.ModelAdmin):
    list_display = ['key_user', 'system_user', 'server']

    class Meta:
        model = UserData


admin.site.register(UserKeys, UserKeysAdmin)
admin.site.register(Server)
admin.site.register(UserData, UserDataAdmin)