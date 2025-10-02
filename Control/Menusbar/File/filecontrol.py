class FileControl:
    def __init__(self, 
                 model, 
                 view):
        self.model = model
        self.view = view
        parent = self.view.menusbarlayout.parent
        self.view.menusbarlayout.exitlayout.trigger_exit.triggered.connect(parent.close)