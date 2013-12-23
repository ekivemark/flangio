from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ReadOnlyPasswordHashField
from models import Permission, flangioUser
from django.utils.translation import ugettext_lazy as _
from models import flangioUser
admin.site.register(Permission)



class flangioUserChangeForm(UserChangeForm):

    class Meta:
        
        model =  flangioUser

class flangioUserCreationForm(UserCreationForm):

    class Meta:
        model =  flangioUser

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

class flangioUserAdmin(UserAdmin):
    form = flangioUserChangeForm
    add_form = flangioUserCreationForm
    fieldsets = (
        (None, {'fields': [('username',  'password'),]}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',
                                         'user_type', 'vid','anonymous_patient_id',
                                         'pin','gender','year_of_birth',
                                         'height_inches', 'weight_lbs', 'state',
                                         'city', 'postal_code', 'mobile_phone_number',
                                         'fax_number', 'organization', 'npi',
                                         'photo_image','last_soc_login_avatar_url'
                                           )}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        )

admin.site.register(flangioUser, flangioUserAdmin)