from django.db import models
import datetime
from django.conf import settings

class SocialGraph(models.Model):
    
    grantor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="grantor")
    grantee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="grantee")
    created_on  =  models.DateField(default=datetime.date.today)
   
    def __unicode__(self):
        return "%s shares with %s since %s" % (self.grantor.username,
                                                self.grantee.username,
                                                self.created_on)
   
    class Meta:
        unique_together = (("grantor", "grantee"),)
        ordering = ('-created_on',)
        get_latest_by = "created_on"


