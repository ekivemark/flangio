# This is an example configuration for a patient adherence tracking server.
# This is the common setting for most insurance companies, HMOs or ACOs.



# To enable self tracking set to True.  A self-graph is created when the user is created.

# To only users to enter data about other users, set this to Dalse and do not create a
# self social graph for the subject. You may also prevent subject transaction
# create/read by simply creating the subjects' users but not providing the
# subjects with their password credcentials.


AUTO_SELF_FOLLOW=True

# When creating transactions, the server will require the transaction's
# datetime to match "now".
ENFORCE_TIME_SANITY = True
MAX_TIME_SKEW_MIN = 5

# A social graph must exist between sender and subject, and sender and receiver
RESPECT_SOCIAL_GRAPH = True

# Do not allow upgates.  Each transaction must be new. 
ALLOW_UPDATE_TX = False