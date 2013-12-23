from django.contrib.auth.models import User
from models import SocialGraph

def social_graph_validator(sndr, rcvr, subj):
    ##print """Validate a social graph exists where the
    #subject is %s and the receiver is %s""" % (sndr, rcvr)
    try:
        sender=User.objects.get(username=sndr)
        receiver=User.objects.get(username=rcvr)
        s=SocialGraph.objects.filter(grantor=sender, grantee=receiver)
                
    except(SocialGraph.DoesNotExist):
        error_string = "Sender %s has not granted access to receiver %s at security level %s." % (sender.grantor, receiver.grantee, security_level)
        return error_string
    except Exception, exc:
        ##print exc
        pass
    try:
        sender=User.objects.get(username=sndr)
        subject=User.objects.get(username=subj)
        s=SocialGraph.objects.filter(grantor=sender, grantee=subject, security_level__lte=security_level)
    except(SocialGraph.DoesNotExist):
        error_string = "Sender %s has not granted access to subject %s at security level %s." % (sender.grantor, subject.grantee, security_level)
        return error_string
    except Exception, exc:
        pass
    

def get_valid_social_graph(grntr, grnte):
    ##print "Get a social graph where %s grants rights to %s" % (grntr, grnte)
    try:

        grantor=User.objects.get(username=grntr)
        grantee=User.objects.get(username=grnte)
        sg=SocialGraph.objects.get(grantor=grantor, grantee=grantee)
        return sg
    
    except(SocialGraph.DoesNotExist):
        return None
    
def get_valid_social_graph_by_email(grntr, grnte):
    ##print "Get a social graph where %s grants rights to %s" % (grntr, grnte)
    try:

        grantor=User.objects.get(email=grntr)
        grantee=User.objects.get(email=grnte)
        sg=SocialGraph.objects.get(grantor=grantor, grantee=grantee)
        return sg
    
    except(SocialGraph.DoesNotExist):
        return None

def get_all_valid_socialgraphs_for_requester(username):
    ##print "Get a social graph where %s grants rights to %s" % (grntr, grnte)
    try:
        l=[]
        grantee=User.objects.filter(username=username)
        sg=SocialGraph.objects.filter(grantee=grantee)
        
        for s in sg:
           l.append(str(s.grantor.email)) 
        return l
    
    except(SocialGraph.DoesNotExist):
        return None


