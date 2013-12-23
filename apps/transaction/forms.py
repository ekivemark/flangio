from django import forms
from django.conf import settings
from ..accounts.models import flangioUser as User
from models import *
import json, uuid
from omhe.core.parseomhe import parseomhe
from datetime import datetime, timedelta, date
import json
from utils import  get_labels_tuple, build_non_observational_key
from models import DataLabelMeta





class DataDictionaryForm(forms.Form):
    
    outputformat = forms.TypedChoiceField(initial="xls", label="Output Format",
                                  choices = (('xls','Excel'),
                                             ('json','JSON'),))
    
    def save(self):

        data={
            'outputformat': self.cleaned_data.get('outputformat', ""),
            'labels': get_labels_tuple()
        }
        return data


class KeysForm(forms.Form):
    
    outputformat = forms.TypedChoiceField(initial="xls", label="Output Format",
                                  choices = (('xls','Excel'),
                                             ('json','JSON'),
                                             ('csv','CSV'),
                                             ('xml','XML'),))
    query    = forms.CharField(widget=forms.Textarea(),
                                 max_length=25000,
                                 initial="{}",
                                 label="Query (JSON dictionary)")
    
    def __init__(self, key_list, label_dict, *args,**kwargs):
        """Override the form's init to set the tag choices dropdown"""
        super(KeysForm,self).__init__(*args,**kwargs)
        
       #print "label_dict keys", label_dict.values()
        
        if not settings.OTHER_LABELS:
            for k in key_list:
                #print k
                if label_dict.has_key(str(k)):    
                    self.fields[k] = forms.BooleanField(required = False,
                                                        help_text = label_dict[k],)

                else:
                    #print "nokey"
                    self.fields[k] = forms.BooleanField(required=False,)
        else:
             for k in key_list:
                #print k
                if label_dict.has_key(str(k)):    
                    #print k, label_dict
                    
                    try:
                        l = DataLabelMeta.objects.get(variable_name=build_non_observational_key(k))
                        
                        self.fields[k] = forms.BooleanField(required = False,
                                                    label = l.label,)
                    except(DataLabelMeta.DoesNotExist):
                        self.fields[k] = forms.BooleanField(required = False,
                                                        label = label_dict[k],)
                        

                else:
                    #print "nokey"
                    self.fields[k] = forms.BooleanField(required=False,)
            

    def clean_query(self):
        """Make sure the query is JSON"""
        query = self.cleaned_data.get("query", "")
        
        if query:
            try:
                jsquery = json.loads(query)
                if type(jsquery) != type({}):
                    raise forms.ValidationError("The query you passed was not a JSON dict.")
            except:
                raise forms.ValidationError("The query you passed was not a JSON dict.")
                
            #for k,v in jsquery.items():
                #print k,v
                
        return query

class DeleteTransactionForm(forms.Form):
    transaction_id    = forms.CharField( max_length=50, label="Transaction ID")


class MeowSQLForm(forms.Form):
    meowsql    = forms.CharField(widget=forms.Textarea(), max_length=25000,
                                 label="Enter MeowSQL here.")

class TransactionForm(forms.Form):

   #The required Fields -------------------------------------------------------
    transaction_type   =  forms.TypedChoiceField(choices=TRANSACTION_CHOICES,
                                label="Transaction Type")
    
    transaction_id    = forms.CharField(max_length=50, initial=uuid.uuid4,
                                label="Transaction ID")
    
    sender          = forms.CharField(max_length=200, label="Sender")
    receiver        = forms.CharField(max_length=200, label="Receiver")
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
    
    security_level     = forms.TypedChoiceField(choices=SECURITY_CHOICES,
                               label="Security Level",
                               initial='2')
    
    #The payload items --------------------------------------------------------
    text = forms.CharField(max_length=140, required=False)
    
    file = forms.FileField(required=False)
    
    url = forms.CharField(max_length=512, required=False)
    
    # Other defined fields ----------------------------------------------------
    
    name        =  forms.CharField(max_length=200, label="Name", required=False)
      
    tags        =  forms.CharField(max_length=1000,
                        label="A JSON list of tags.",
                        required=False)
        
    note        =  forms.CharField(max_length=2048, required=False,
                        label="Note")
    
    mime        = forms.TypedChoiceField( required=False,
                                         choices=MIME_CHOICES,
                                        label="MIME Type")
    
    geopoint    =  forms.CharField(max_length=2048, required=False,
                        label='Geometric feature point [Lat, Lon]')
    
    icd9        =  forms.CharField(max_length=2048, required=False,
                        label= "A JSON list of  ICD9 codes.")
    
    icd10       =  forms.CharField(max_length=2048, required=False,
                        label="A JSON list of ICD10 codes")

    cpt         =  forms.CharField(max_length=2048, required=False,
                        label= "A JSON list of CPT procedure codes.")
    
    cpt_mods    =  forms.CharField(max_length=2048, required=False,
                        label= "A JSON list of CPT modifiers.")
    
    fee_usd     =  forms.CharField(max_length=20, required=False,
                        label= "Fee (in USD)")
    
    hid         = forms.CharField(max_length=50, required=False,
                        label="Hardware or Device ID")

    crt         = forms.CharField(max_length=50, required=False,
                        label="A Security Certificate")

    points      = forms.CharField(max_length=50, required=False, label="Points")
    
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
    
    def clean_text(self):
        #If OMHE, then validate OMHE.
        text = self.cleaned_data.get('text')
        transaction_type = self.cleaned_data.get('transaction_type')
        if transaction_type=="omhe":
            p = parseomhe()
            r=p.parse(text)
            if r.has_key('error'):
                msg="OMHE Parse Error: %s" % (r['error'])
                raise forms.ValidationError(msg)
        return text

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            try:
                t =json.loads(tags)
                l=[]
                if type(l) != type(t):
                    msg='Tags parse error. JSON was not a list. Should be in the form: ["fee","foo", "bar"]'
                    raise forms.ValidationError(msg)  
            except(ValueError):
                msg='Tags parse error. Invalid JSON. Should be in the form: ["fee","foo", "bar"]'
                raise forms.ValidationError(msg) 
            return tags
        return ""
    
    def clean_icd9(self):
        icd9 = self.cleaned_data.get('icd9')
        if icd9:
            try:
                t =json.loads(icd9)
                l=[]
                if type(l) != type(t):
                    msg='icd9 parse error. JSON was not a list. Should be in the form: ["fee","foo", "bar"]'
                    raise forms.ValidationError(msg)  
            except(ValueError):
                msg='icd9 parse error. Invalid JSON. Should be in the form: ["fee","foo", "bar"]'
                raise forms.ValidationError(msg) 
            return icd9
        return ""

    def clean_icd10(self):
        icd10 = self.cleaned_data.get('icd10')
        if icd10:
            try:
                t =json.loads(icd10)
                l=[]
                if type(l) != type(t):
                    msg='icd10 parse error. JSON was not a list. Should be in the form: ["fee","foo", "bar"]'
                    raise forms.ValidationError(msg)  
            except(ValueError):
                msg='icd10 parse error. Invalid JSON. Should be in the form: ["fee","foo", "bar"]'
                raise forms.ValidationError(msg) 
            return icd10
        return ""

    def clean_cpt(self):
        
        cpt = self.cleaned_data.get('cpt')
        if cpt:
            try:
                t =json.loads(cpt)
                l=[]
                if type(l) != type(t):
                    msg='CPT parse error. JSON was not a list. Should be in the form: ["fee","foo", "bar"]'
                    raise forms.ValidationError(msg)  
            except(ValueError):
                msg='CPT parse error. Invalid JSON. Should be in the form: ["fee","foo", "bar"]'
                raise forms.ValidationError(msg) 
            return cpt
        return ""
         
    def clean_cpt_mods(self):
        cpt_mods = self.cleaned_data.get('cpt_mods')
        if cpt_mods:
            try:
                t =json.loads(cpt_mods)
                l=[]
                if type(l) != type(t):
                    msg='CPT modifications (mods) parse error. JSON was not a list. Should be in the form: ["fee","foo", "bar"]'
                    raise forms.ValidationError(msg)  
            except(ValueError):
                msg='CPT modifications (mods) parse error. Invalid JSON. Should be in the form: ["fee","foo", "bar"]'
                raise forms.ValidationError(msg) 
            return cpt_mods
        return ""
    
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
