# Utility class that helps maintain metadata about the chat
class ChatUtil:

    def __init__(self):
        self.users_online = set()

        # Styles for each user role
        self.owner_style = "width: 100%;color:blue;text-align: right"
        self.guest_style = "width: 100%;color:#3b3b3b;text-align: left"

    # Called when a user joins the chat, adds email to set
    def user_join(self, email):
        self.users_online.add(email)
    
    # Called when a user leaves the chat, removes email from set
    def user_leave(self, email):
        self.users_online.remove(email)