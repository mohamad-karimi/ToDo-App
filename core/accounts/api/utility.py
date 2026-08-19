import threading


class EmailThreading(threading.Thread):
    """
    Create a custom thread class to send emails in the background
    without blocking the main request.
    """

    def __init__(self, email):
        """
        Initialize the thread with the email message that should be sent.
        """
        super().__init__()
        self.email = email

    def run(self):
        """
        Send the email when the thread starts.
        """
        self.email.send()
