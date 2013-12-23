

# This is a promiscuous example.  This is suitable setting for research in a
# controlled environment or in a situation where you want all users to have
# read/write access to each others transactions.


# When creating transactions, the server will not require the transaction
# datetime to match "now".
ENFORCE_TIME_SANITY=False

# The server will allow any user to create/view any transaction, so long
# as the users subject, sender, receiver exist.
RESPECT_SOCIAL_GRAPH=False

# Allow old transactions to be updated.  The old transaction will be pushed onto
# the historical collection.
ALLOW_UPDATE_TX = True

