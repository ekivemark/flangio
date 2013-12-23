import urllib, time, urlparse, random, string, uuid, re
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.core.mail import send_mail, mail_admins
from localflavor.us.us_states import US_STATES
from django.utils.translation import ugettext_lazy as _
from localflavor.us.models import PhoneNumberField, USPostalCodeField
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin, UserManager)
from django.core.mail import send_mail
from django.core import validators
from django.utils import timezone



def genereate_vid():
    str(random.randint(100000000000000,999999999999999))


class flangioUserManager(BaseUserManager):
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = UserManager.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, **extra_fields)
 
        user.set_password(password)
        user.save(using=self._db)
        return user
 
    def create_superuser(self, username, email, password, **extra_fields):
        u = self.create_user(username, email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u    


#All allowed methods plus standard email method.
SOCIAL_CHOICES =( ('email','Email'),
                  ('twitter','Twitter'),
                  ('facebook','Facebook'),
                  ('google', 'Google'),
                  ('instagram','Instagram'),
                )
#You may only register with these
REGISTER_CHOICES =(  ('VERIFY-EMAIL','Verify Email'),
                     ('facebook','Facebook'),
                     ('twitter','Twitter'),
                  )


class flangioUser(AbstractBaseUser, PermissionsMixin):
 
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


 
 
 
    user_type   = models.CharField(max_length=10,
                                   choices=settings.USERTYPE_CHOICES,
                                   )
    vid                 = models.CharField(max_length=15, blank=True,
                           #default = genereate_vid
                           )
    anonymous_patient_id = models.CharField(max_length=36, blank=True,
                                verbose_name=u'Anonymous ID',
                                #default = genereate_vid,
                                )
    pin                    =  models.PositiveIntegerField(max_length=4,
                                                        verbose_name='PIN', blank=True,
                                                        default="1994"
                                                        )
    gender                 = models.CharField(max_length=40, blank=True,
                                              choices=settings.GENDER_CHOICES)
    #daily_request_max      = models.PositiveIntegerField(blank=True, default =1000, max_length=10)
    
    year_of_birth          = models.PositiveIntegerField(blank=True, default =0, max_length=4)
    height_inches          = models.PositiveIntegerField(blank=True, default =0, max_length=3)
    weight_lbs             = models.PositiveIntegerField(blank=True, default =0, max_length=4)
    state                  = models.CharField(blank=True, max_length=2,
                                        choices=US_STATES,)
    city                   = models.CharField(max_length=256, blank=True, default="")
    postal_code            = models.CharField(blank=True, default="", max_length=10)
    mobile_phone_number         = PhoneNumberField(max_length=15, blank=True, default="")
    fax_number                  = PhoneNumberField(max_length=15, blank=True, default="")
    organization                = models.CharField(max_length=100, blank=True, default="")
    npi                         = models.CharField(max_length=20, blank=True,
                                    verbose_name="National Provider Identifier (NPI)")
    
    
    
    photo_image             = models.ImageField(blank = True, null=False, default='',
                                    max_length=255L, upload_to="avatars",
                                    verbose_name= "Profile Photo")
    
    last_soc_login_avatar_url =  models.URLField(blank = True, max_length=200, default="", null=True)

    last_login_via          = models.CharField(max_length=10, choices=SOCIAL_CHOICES,
                                               default="email")
    email_verified          = models.BooleanField(default=False)

    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects  = UserManager()



    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        pass
        
    def __unicode__(self):
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True



# This is merely an example USerProfile.
# More than liekly you'll want to create your own in your app.
# If you are not using flangio for data collection (i.e. you are merely importing
# then you might not need to use a UserProfile at all. )


#class UserProfile(models.Model):
#    user        = models.ForeignKey(User, unique=True, related_name="BuiltInflangioUserProfile")
#    user_type   = models.CharField(max_length=10,
#                                           choices=USERTYPE_CHOICES,
#                                           default="patient")
#    vid = models.CharField(max_length=15, unique=True, blank=True,
#                           default = genereate_vid)
#    anonymous_patient_id = models.CharField(max_length=36,       
#                                  unique=True,
#                                  verbose_name=u'Anonymous Patient ID',
#                                  default = genereate_vid,blank=True,)
#    pin                         =  models.PositiveIntegerField(max_length=4, verbose_name='PIN', blank=True,)
#    gender                      = models.CharField(max_length=40, choices=gender_choices)
#    year_of_birth               = models.IntegerField(blank=True, default="", max_length=4)
#    height_inches               = models.IntegerField(blank=True, default="", max_length=3)
#    weight_lbs                  = models.IntegerField(blank=True, default="", max_length=4)
#    state                       = models.CharField(blank=True, max_length=2,
#                                        choices=US_STATES,)
#    city                        = models.CharField(max_length=256)
#    postal_code                 = models.CharField(blank=True, default="", max_length=10)
#    mobile_phone_number         = PhoneNumberField(max_length=15, blank=True, default="")
#    fax_number                  = PhoneNumberField(max_length=15, blank=True, default="")
#    organization                = models.CharField(max_length=100, blank=True, default="")
#    
#
#
#
#
#
#
#    def __unicode__(self):
#        return '%s %s (%s)' % (self.user.first_name,
#                          self.user.last_name,
#                          self.vid)
#    
#    def save(self, **kwargs):    
#        randcode=random.randint(1000,9999)
#        if not self.pin:
#            self.pin=randcode
#        
#        if not self.anonymous_patient_id:
#            self.anonymous_patient_id=str(uuid.uuid4())
#            
#            
#        if not self.vid:
#            self.vid = str(random.randint(100000000000000,
#                                          999999999999999))
#        
#        super(UserProfile, self).save(**kwargs)
#    
        



class Permission(models.Model):
    user  = models.ForeignKey(flangioUser)
    permission_name = models.CharField(max_length=50,
                choices=settings.PERMISSION_CHOICES)

    def __unicode__(self):
        return '%s has the %s permission.' % (self.user.email, self.permission_name)

    class Meta:
        unique_together = (("user", "permission_name"),)


        


