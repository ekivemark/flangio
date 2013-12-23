from urllib import urlopen
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from social_auth.backends.google import GoogleBackend, GoogleOAuth2Backend
from social_auth.backends.contrib.instagram import InstagramBackend
from models import flangioUser as User
import sys

def get_extra_user_data(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    #print "Backend=", backend.__class__

    
      
    if backend.__class__ == FacebookBackend:
        user.last_soc_login_avatar_url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        user.last_login_via = "facebook"
    
    elif backend.__class__ == TwitterBackend:
        user.last_soc_login_avatar_url = response.get('profile_image_url', '').replace('_normal', '')
        user.last_login_via = "twitter"
    elif backend.__class__ == GoogleOAuth2Backend:
        if "picture" in response:
            user.last_soc_login_avatar_url = response["picture"]
            user.last_login_via = "google"

    elif backend.__class__ == InstagramBackend:
        #print type(response_instagram), response_instagram
        
        if "profile_picture" in response['data']:
            user.last_soc_login_avatar_url = response['data']["profile_picture"]
        user.last_login_via = "instagram"

    #Save the User
    user.save()
        

     
def create_user_profile_with_facebook(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    
    if backend.__class__ == FacebookBackend:
        print user
        
        try:
            #This FB user already has a profile.
            profile = UserProfile.objects.get(user=user)
            profile.facebook_response_data = str(response)
            profile.save()
            
        except UserProfile.DoesNotExist:
            # this is new so create a new user profile and update user.
            #Update the user
            user.first_name = response['first_name']
            user.last_name = response['last_name']
            if response.has_key('email'):
                user.email = response['email']
            
            user.save()
            #create a new user profile.
            facebook_avatar_url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
            
            
            try:
                UserProfile.objects.create(user=user,
                    facebook_avatar_url = facebook_avatar_url,
                    facebook_response_data = str(response),
                    last_login_via = "facebook",)
            
                #profile created
            except:
                #This should never happen so long as fields line up in create.
                print "Error", sys.exc_info()
                

def create_user_profile_with_twitter(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    
    if backend.__class__ == TwitterBackend:
        try:
            #This Twitter user already has a profile.
            profile = UserProfile.objects.get(user=user)
            
        except UserProfile.DoesNotExist:
            # this is new so create a new user profile and update user.
            #Update the user

            
            #get the name from twitter
            name = response.get('name', '')
            
            #split it up into two parts
            names = name.split(" ", 1)
            last_name = ""
            if len(names) == 2:
                last_name = names[1]
            
            #Set the user first and last name.
            user.first_name = names[0]
            user.last_name = last_name
            user.save()
            
            twitter_avatar_url = response.get('profile_image_url', '').replace('_normal', '')
            
            #create a new user profile.          
            try:
                UserProfile.objects.create(user=user,
                    twitter_avatar_url = twitter_avatar_url,
                    twitter_response_data = str(response),
                    last_login_via = "twitter",)
                #profile created
            except:
                #This should never happen so long as fields line up in create.
                print "Error", sys.exc_info()
                            
