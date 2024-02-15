from PyQt6.QtWidgets import QMenuBar

"""

File
|- New
|- Open
|- Save
|- Save As
|- Close
|- Exit

"""

class MenuBar(QMenuBar):
    
    def __init__(self):
        super(MenuBar, self).__init__()
        self.file_menu=self.addMenu("File")
        self.file_menu.addAction("New")
        self.file_menu.addAction("Open")
        self.save_menu=self.file_menu.addMenu("Save")
        self.save_menu.addAction("Save")
        self.save_menu.addAction("Save As")
        self.file_menu.addAction("Close")
        self.file_menu.addAction("Exit")
        
    def add_menu(self, menu_name: str):
        self.addMenu(menu_name)