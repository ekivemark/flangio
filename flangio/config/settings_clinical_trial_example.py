# This is an example configuration for managing a clinical trail.


# Do not allow the subject to create/read.
AUTO_SELF_FOLLOW=False

# When creating transactions, the server will require the transaction's
# datetime to match "now".
ENFORCE_TIME_SANITY = True
MAX_TIME_SKEW_MIN = 5

# A social graph must exist between sender and subject, and sender and receiver
RESPECT_SOCIAL_GRAPH = False

# Do not allow upgates.  Each transaction must be new. 
ALLOW_UPDATE_TX = False