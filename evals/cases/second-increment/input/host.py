class Plugin:
    def __init__(self, connection):
        self.connection = connection

    def stop(self):
        self.connection.close()
