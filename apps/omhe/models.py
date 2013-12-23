from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from utils import  (update_filename, create_mongo_transaction,
                    prepare_idTransaction_dict, get_since_id)
import json
import uuid
TRANSACTION_CHOICES=tuple(zip(settings.ALLOWABLE_TRANSACTION_TYPES,
                              settings.ALLOWABLE_TRANSACTION_TYPES
                        ))

SECURITY_CHOICES = (('0','Undefined'),('1','Private'),('2','Anonymous Sharing'),
    ('3','Public'))

MIME_CHOICES = (('txt/plain','txt/plain'),
                ('application/xml','application/xml'),
                ('txt/html','txt/html'))





class Transaction(models.Model):
    
    #The Required Fields -------------------------------------------------------
    transaction_id    = models.CharField(max_length=100, default=uuid.uuid4,
                                verbose_name="Transaction ID")

    transaction_reference   = models.CharField(max_length=100, blank=True,
                                        default="",
                                        verbose_name="Transaction Reference")

    sender    = models.CharField(max_length=100, verbose_name="Sender")
    
    receiver  = models.CharField(max_length=100, verbose_name="Receiver")
    
    subject     = models.CharField(max_length=100, verbose_name="Subject")
    
    transaction_datetime = models.CharField(
                        verbose_name = "Transaction Datetime (YYYY-MM-DD HH:MM:SS)",
                        max_length = 20, )

    transaction_timezone    = models.CharField(verbose_name="Transaction Timezone Offset (e.g. -5 for D.C./NYC )",
                                   max_length=3, default="0") 
    sinceid                 = models.CharField(max_length=12, editable=False, default="",
                               verbose_name="A server-generated auto incremented ID.")

    transaction_type   =  models.CharField(max_length=30, choices=TRANSACTION_CHOICES,
                                verbose_name="Transaction Type")

    
    event_datetime    = models.CharField(verbose_name="Event Datetime (YYYY-MM-DD HH:MM:SS)",
                                    max_length=20, default="",)

    event_date        = models.CharField(verbose_name="Event Date (YYYY-MM-DD)",
                                    max_length=20, default="")
    
    event_timezone    = models.CharField(verbose_name="Event Timezone Offset (e.g. -5 for D.C./NYC )",
                                max_length=3, default="0")
    
    security_level     = models.CharField(max_length=1, choices=SECURITY_CHOICES,
                               verbose_name="Security Level", default='2')
    
    #The payload items --------------------------------------------------------
    text = models.CharField(max_length=140,default="",)
    
    file = models.FileField(upload_to=update_filename,
                                null=True,
                                blank=True)
    
    url = models.CharField(max_length=1024,default="",)
    
    # Other defined fields. ----------------------------------------------------
    
    name        =  models.TextField(max_length=200, verbose_name="Name",
                                    default="",)    
    
    tags        =  models.CharField(max_length=1000,
                        verbose_name="A JSON list of tags.",
                        default="",)
        
    note        =  models.TextField(max_length=2048, default="", blank=True,
                        verbose_name="Note")
    
    mime        = models.CharField(max_length=50, default="txt/plain",
                                         choices=MIME_CHOICES,
                        verbose_name="MIME Type")
    
    geopoint    =  models.TextField(max_length=2048, default="",
                        verbose_name="Geometric feature point (GeoJSON Encoded)")
    
    icd9        =  models.TextField(max_length=2048,default="",
                        verbose_name= "A JSON list of ICD9 codes.")
    
    icd10       =  models.TextField(max_length=2048,default="",
                        verbose_name="A JSON list of ICD10 codes")

    cpt         =  models.TextField(max_length=2048, default="",
                        verbose_name= "A JSON list of CPT procedure codes.")
    
    cpt_mods    =  models.CharField(max_length=2048, default="",
                        verbose_name= "A JSON list of CPT modifiers.")
    
    fee_usd     =  models.CharField(max_length=20, default="",
                        verbose_name= "Fee (in US dollars)")
    
    hid         = models.CharField(max_length=50, default="",
                        verbose_name="Hardware or Device ID")

    crt         = models.CharField(max_length=50, default="",
                        verbose_name="A Security Certificate")

    points      = models.CharField(max_length=10, default="",
                        verbose_name="Points")
    
    # Where you user defined fields go as a JSON dict.
    
    # Example: {"q1_q":"How are you feeling?", "q1_a":"Good"}.
    extra_fields = models.TextField(max_length=20480,
                           null=True,
                           blank=True,
                           verbose_name="Extra Fields (as a JSON Dict)")

    
    creation_dt = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        get_latest_by = "creation_dt"
        ordering = ('-creation_dt',)
    
    def save(self, **kwargs):
        
        if not self.event_date:
            self.event_date=self.event_datetime.date()
        
        
        if not self.sinceid:
            self.sinceid = get_since_id()
            
            
        args = prepare_idTransaction_dict(self)
        result = create_mongo_transaction(args)
        super(Transaction, self).save(**kwargs)
        return result

    def __unicode__(self):
        return "SinceID:%s,  Subject:%s,  Created:%s" % (self.sinceid,
                                                        self.subject,
                                                        self.creation_dt)

