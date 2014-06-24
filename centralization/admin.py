from django.contrib import admin
from .models import UserKeys, Server, UserData


class UserKeysAdmin(admin.ModelAdmin):
    fields = ['key_file', ]
    list_display = ['user','key_file', 'server_access','system_user_access', 'ssh_on_server','win_scp']

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

    def server_access(self, item):
        user_id = item.user.id
        user_data_obj = UserData.objects.filter(key_user=user_id).values_list('server__server_ipaddress', flat=True)
        if user_data_obj:
            return user_data_obj
        else:
            return None

    def system_user_access(self,item):
        user_id = item.user.id
        system_users = UserData.objects.filter(key_user=user_id).values_list('system_user__username', flat=True)
        return system_users

    def win_scp(self,item):
        return "To be Implemented"


    def ssh_on_server(self, item):
        servers = self.server_access(item)
        if servers:
            server_ip = servers[0]
            return '<a href="http://%s:6080/vnc_auto.html">OPEN SERVER</a>' %(server_ip)
        return None
        # return '<a href="%s">%s</a>' % (obj.firm_url, obj.firm_url)

    ssh_on_server.allow_tags = True


class UserDataAdmin(admin.ModelAdmin):
    list_display = ['key_user', 'system_user', 'server']

    class Meta:
        model = UserData


admin.site.register(UserKeys, UserKeysAdmin)
admin.site.register(Server)
admin.site.register(UserData, UserDataAdmin)