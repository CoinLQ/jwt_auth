# coding: utf-8
import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group, _user_get_all_permissions, _user_has_perm, _user_has_module_perms
from django.contrib.auth.models import Permission as DjangoPermission
from django.contrib.postgres.fields import JSONField
from functools import reduce
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

class StaffManager(BaseUserManager):

    def create_staff(self,username, email, password):
        if not email:
            raise ValueError('邮箱地址不能为空')
        if not password:
            raise ValueError('密码不合法.')

        staff = self.model(email=self.normalize_email(email), last_login=timezone.now())
        staff.set_password(password)
        staff.save(using=self._db)
        return staff


    def create_superuser(self, *args, **kwargs):
        staff = self.create_staff(*args, **kwargs)
        staff.is_admin = True
        staff.is_superuser = True
        staff.save(using=self._db)
        return staff


class Role(models.Model):
    name = models.CharField(u"名称", max_length=16, default="")

    def __str__(self):
        return self.name

    @property
    def menus(self):
        menus = self.permission_set.select_related('menu').only('menu').values_list('menu__menu_paths', flat=True)
        return reduce(lambda x, y: x + y, menus)

    # TODO: API有待详细设计
    def resources(self):
        pass

    class Meta:
        verbose_name_plural = verbose_name = u'角色'

class Menu(models.Model):
    name = models.CharField(u"名称", max_length=16, default="")
    menu_paths = JSONField(u'访问路径', default=list, help_text=u'选填', blank=False)
    is_active = models.BooleanField("是否激活", default=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u'菜单'


class Resource(models.Model):
    name = models.CharField(u"名称", max_length=16, default="")
    api_path = models.CharField(u'API路径', max_length=200, help_text=u'选填', default='')
    is_active = models.BooleanField("是否激活", default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = verbose_name = u'资源'

class MyPermissionsMixin(models.Model):
    """
    Add the fields and methods necessary to support the Group and Permission
    models using the ModelBackend.
    """
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        DjangoPermission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use simlar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

class Staff(AbstractBaseUser, MyPermissionsMixin):
    username = models.CharField(u"用户名", max_length=24, unique=True, db_index=True, default="")
    email = models.EmailField(u"邮件", max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField("是否激活", default=False)
    is_superuser = models.BooleanField("是否是超级用户", default=False)
    is_admin = models.BooleanField("是否管理员", default=False)
    introduce_by = models.CharField(u"推荐由", max_length=64, default="", blank=True)
    date_joined = models.DateTimeField(u'创建时间', auto_now=True)
    roles = models.ManyToManyField(Role, verbose_name=u'角色', blank=True)
    objects = StaffManager()

    USERNAME_FIELD = 'email'
    # USERNAME_FIELD = 'username'
    @property
    def is_staff(self):
        return self.is_superuser

    def __str__(self):
        return self.email

    @property
    def menus(self):
        roles = self.roles.prefetch_related('permission_set')
        menus = [m.menus for m in roles]
        if not menus:
            return []
        return list(set(reduce(lambda x, y: x + y, menus)))

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_short_name(self):
        # The user is identified by their email address
        return self.email


    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def fake_username(self):
        # return self.email.split('@')[0]
        return self.username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    class Meta:
        verbose_name_plural = verbose_name = u'活动用户'

class UserManagement(Staff):
    class Meta:
        proxy = True
        verbose_name = '用户管理'
        verbose_name_plural = '用户管理'

class UserAuthentication(Staff):
    class Meta:
        proxy = True
        verbose_name = '用户授权'
        verbose_name_plural = '用户授权'

@receiver(post_save, sender=Staff)
def assign_default_jiaodui_role(sender, instance, **kwargs):
    if not instance.username:
        instance.username = instance.email.split('@')[0] 
        instance.save(update_fields=['username'])

class Permission(models.Model):
    name = models.CharField(u"名称", max_length=24, default="")
    menu = models.OneToOneField(Menu, verbose_name=u'菜单组', 
                related_name='permissions', on_delete=models.SET_NULL, null=True)
    resources = models.ManyToManyField(Resource, verbose_name=u'资源',
        blank=True)
    roles = models.ManyToManyField(Role, verbose_name=u'角色',
        blank=True)
    is_active = models.BooleanField("是否激活", default=True)

    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = verbose_name = u'权限'

