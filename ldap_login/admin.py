from django.contrib import admin
from ldap_login.models import group,user

#ref: https://docs.djangoproject.com/en/1.2/ref/contrib/admin/#working-with-many-to-many-models
class membershipInline(admin.TabularInline):
    model = user.groups.through; #a reference to the intermediary modeli
    extra = 1
#    fk_name = 'user'

class userAdmin(admin.ModelAdmin):
    search_fields = ['username'];
    list_filter=['groups']
    #because model will automatically ensure that ManytoManyKeisDisplayed

class groupAdmin(admin.ModelAdmin):
    inlines = [
        membershipInline,
        ]

#class UsersInline(admin.TabularInline):
#    model = user;
#    extra = 1;

#class groupAdmin(admin.ModelAdmin):
#	inlines = [UsersInline];

admin.site.register(group,groupAdmin);
admin.site.register(user,userAdmin);


