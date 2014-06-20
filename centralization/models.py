import os
import subprocess
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


def key_file_path(instance, filename):
    return '/'.join(['media', 'key_file', instance.user.username, filename])


class UserKeys(models.Model):
    user = models.ForeignKey(User)
    key_file = models.FileField(upload_to=key_file_path)

    def __unicode__(self):
        return self.user.username


class Server(models.Model):
    name = models.CharField(max_length=100)
    server_ipaddress = models.IPAddressField()

    def __unicode__(self):
        return self.name


class UserData(models.Model):
    key_user = models.ForeignKey(User, related_name='key_user')
    system_user = models.ForeignKey(User, related_name='system_user')
    server = models.ForeignKey(Server)

    def __unicode__(self):
        return str(self.id)


def my_handler(sender, **kwargs):
    instance = kwargs['instance']
    key_user =  instance.key_user
    key_instance = UserKeys.objects.get(user=key_user)
    file_obj = key_instance.key_file.file
    file_text = file_obj.read()
    keys = subprocess.check_output(["ssh", "root@192.168.1.8", "cat", "/home/umesh/.ssh/authorized_keys"])
    if file_text not in keys:
        system_user = instance.system_user.username
        server = instance.server.server_ipaddress
        command = "cat %s | ssh root@%s 'cat >> /home/%s/.ssh/authorized_keys'" % (file_obj, server, system_user)
        os.system(command)


post_save.connect(my_handler, sender=UserData)
