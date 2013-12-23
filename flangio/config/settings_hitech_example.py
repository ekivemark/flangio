# This is an example configuration for a HITECH compliant audit trail


# When creating transactions, the server will require the transaction's
# datetime to match "now".
ENFORCE_TIME_SANITY = True
MAX_TIME_SKEW_MIN = 5

# A social graph must exist between sender and subject, and sender and receiver
RESPECT_SOCIAL_GRAPH = True

# Do not allow upgates.  Each transaction must be new. 
ALLOW_UPDATE_TX = False