from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from ..accounts.models import UserProfile
from ..utils import write_mongo
import json, uuid
from omhe.core.parseomhe import parseomhe
from datetime import datetime, timedelta, date
import json
from utils import get_user_profile_info, get_since_id
import time
from bson.objectid import ObjectId





class DeleteTransactionForm(forms.Form):
    transaction_id    = forms.CharField( max_length=50, label="Transaction ID")


ALLOWABLE_TRANSACTION_CHOICES = (('lymphoma-observation','lymphoma-observation'),)

class LymphomaTransactionForm(forms.Form):
    
  
   #The required Fields -------------------------------------------------------
    transaction_type   =  forms.TypedChoiceField(
                            choices=ALLOWABLE_TRANSACTION_CHOICES,
                            label="Transaction Type", initial="lymphoma-observation")
    
    
    transaction_id    = forms.CharField(max_length=50, initial=uuid.uuid4,
                                label="Transaction ID")
    
    #who is sending this data (likely a web or mobile app)
    sender          = forms.CharField(max_length=200, label="Sender")
    
    #the provider
    receiver        = forms.CharField(max_length=200, label="Receiver")
    
    #the patient
    subject         = forms.CharField(max_length=200, label="Subject")
    
    event_datetime    = forms.DateTimeField(label="Event Datetime (Local)",
                                        initial=datetime.now())
    
    event_timezone    = forms.CharField(label="Event Timezone Offset",
                                        required=False,
                                        max_length=3, initial="0")

    event_date      = forms.DateField(label="Event Date", required=False,
                                    initial=date.today)

    transaction_datetime   = forms.DateTimeField(label="Transaction Datetime UTC",
                                                  initial=datetime.utcnow)    
    
    


    #The lymphoma payload items ------------------------------------------------

    
    #rating 1 to 10 where 10 is the worst/max.
    lymphoma_pain                   = forms.IntegerField(required=False)
    lymphoma_fatigue                = forms.IntegerField(required=False)
    lymphoma_depression             = forms.IntegerField(required=False)

    lymphoma_restricted_movement    = forms.IntegerField(required=False)
    lymphoma_weakness               = forms.IntegerField(required=False)
    lymphoma_swelling               = forms.IntegerField(required=False)
    lymphoma_heaviness              = forms.IntegerField(required=False)
    lymphoma_neuropathy_of_arm_hand = forms.IntegerField(required=False)
    lymphoma_neuropathy_of_leg_foot = forms.IntegerField(required=False)
    lymphoma_adapting               = forms.IntegerField(required=False)
    lymphoma_anxiety                = forms.IntegerField(required=False)
     
    #binary values where 1=true and 0=false.
     
    adhere_to_medications           = forms.IntegerField(required=False)
    exercised_today                 = forms.IntegerField(required=False)
    slepted_well                    = forms.IntegerField(required=False)
    drank_water                     = forms.IntegerField(required=False)


    # Other defined fields ----------------------------------------------------
        
    note        =  forms.CharField(max_length=2048, required=False,
                        label="Note")
    
    hid         = forms.CharField(max_length=50, required=False, initial="",
                        label="Hardware or Device ID")

    # Where you user defined fields go as a JSON dict.
    # Example: {"q1_q":"How are you feeling?", "q1_a":"Good"}.
    extra_fields = forms.CharField(max_length=204800,
                           required=False,
                           label="Extra Fields (as a JSON Dict)")


    def clean_sender(self):
    
        sender = self.cleaned_data.get('sender')
        if settings.USERS_MUST_EXIST:
            if User.objects.filter(username=sender).count()==0 and \
                User.objects.filter(email=sender).count()==0 and \
                UserProfile.objects.filter(vid = sender).count()==0 and \
                UserProfile.objects.filter(anonymous_patient_id = sender).count()==0:    
                msg="The sender %s does not exist." % (sender)
                raise forms.ValidationError(msg)
        return sender
    
    def clean_receiver(self):
    
        receiver = self.cleaned_data.get('receiver')
        if settings.USERS_MUST_EXIST:
            if User.objects.filter(username=receiver).count()==0 and \
                User.objects.filter(email=receiver).count()==0 and \
                UserProfile.objects.filter(vid = receiver).count()==0 and \
                UserProfile.objects.filter(anonymous_patient_id = receiver).count()==0: 
                msg="The receiver %s does not exist." % (receiver)
                raise forms.ValidationError(msg)
        return receiver
    
    def clean_subject(self):
    
        subject = self.cleaned_data.get('subject')
        if settings.USERS_MUST_EXIST:
            if User.objects.filter(username=subject).count()==0 and \
                User.objects.filter(email=subject).count()==0 and \
                UserProfile.objects.filter(vid = subject).count()==0 and \
                UserProfile.objects.filter(anonymous_patient_id = subject).count()==0: 
                msg="The subject %s does not exist." % (subject)
                raise forms.ValidationError(msg)
        return subject
       
    
    def clean_transaction_datetime(self):
        transaction_datetime = self.cleaned_data.get('transaction_datetime')
        if settings.ENFORCE_TIME_SANITY:
            utcnow = datetime.utcnow()
            lower_bound = utcnow - timedelta(minutes = settings.MAX_TIME_SKEW_MIN)
            upper_bound = utcnow + timedelta(minutes = settings.MAX_TIME_SKEW_MIN)
            
            if not (lower_bound < transaction_datetime < upper_bound):
                msg='Datetime skew Error. ENFORCE_TIME_SANITY is on and Datetime %s is off more than MAX_TIME_SKEW_MIN %s minutes.' % \
                            (transaction_datetime, settings.MAX_TIME_SKEW_MIN)
    
                raise forms.ValidationError(msg) 
        return transaction_datetime
    
    def save(self, update):
        """Custom save for saving to MongoDB"""
        print "save", update
        mongodb_id = ObjectId()
        transaction_id =  self.cleaned_data.get('transaction_id', "")
        if not transaction_id:
            transaction_id = uuid.uuid4()
        
        
        #get the utc timestamp and turn it into an epoch
        timestamp = datetime.utcnow()
        timestamp = "%d" % time.mktime(timestamp.timetuple())
        
        event_datetime = self.cleaned_data.get('event_datetime')
        event_datetime = "%d" % time.mktime(event_datetime.timetuple())
        
        transaction_datetime = self.cleaned_data.get('transaction_datetime')
        transaction_datetime = "%d" % time.mktime(transaction_datetime.timetuple())
        
        up = get_user_profile_info(self.cleaned_data.get('subject'))

        
        temp_kwargs={'_id'                       : mongodb_id,
                'transaction_id'                 : self.cleaned_data.get('transaction_id', ""),
                'since_id'                       : get_since_id(),
                'sender'                         : self.cleaned_data.get('sender'),
                'receiver'                       : self.cleaned_data.get('receiver'),
                'subject'                        : self.cleaned_data.get('subject'),
                'event_datetime'                 : int(event_datetime),
                'event_timezone'                 : self.cleaned_data.get('event_timezone', ""),
                'event_date'                     : str(self.cleaned_data.get('event_date')),
                'transaction_datetime'           : int(transaction_datetime),    
                'note'                           : self.cleaned_data.get('note', ""),
                'lymphoma_pain'                  : self.cleaned_data.get('lymphoma_pain', ""),            
                'lymphoma_fatigue'               : self.cleaned_data.get('lymphoma_fatigue', ""),           
                'lymphoma_depression'            : self.cleaned_data.get('lymphoma_depression', ""),        
                'lymphoma_restricted_movement'   : self.cleaned_data.get('ymphoma_restricted_movement', ""),
                'lymphoma_weakness'              : self.cleaned_data.get('lymphoma_weakness', ""),   
                'lymphoma_swelling'              : self.cleaned_data.get('lymphoma_swelling', ""), 
                'lymphoma_heaviness'             : self.cleaned_data.get('lymphoma_heaviness', ""),
                'lymphoma_neuropathy_of_arm_hand': self.cleaned_data.get('lymphoma_neuropathy_of_arm_hand', ""),
                'lymphoma_neuropathy_of_leg_foot': self.cleaned_data.get('lymphoma_neuropathy_of_leg_foot', ""),
                'lymphoma_adapting':             self.cleaned_data.get('lymphoma_adapting', ""), 
                'lymphoma_anxiety':              self.cleaned_data.get('lymphoma_anxiety', ""),  
                'adhere_to_medications':         self.cleaned_data.get('adhere_to_medications', ""),  
                'exercised_today':               self.cleaned_data.get('exercised_today', ""),     
                'slepted_well':                  self.cleaned_data.get('slepted_well', ""),
                'drank_water':                   self.cleaned_data.get('drank_water', ""),
                'postal_code':                   up.postal_code,
                'year_of_birth':                 up.year_of_birth,
                'weight_lbs':                    up.weight_lbs,
                'height_inches':                 up.height_inches,
                #'npi':                           up.npi,
                
                }
        
        
        kwargs ={}
        
        #Only populate fields that are not blank.
        for k,v in temp_kwargs.items():
            if v:
                kwargs[k]=v
        
        #write to mongoDB
        result = write_mongo(kwargs, settings.MONGO_MASTER_COLLECTION, update)        
        return result
