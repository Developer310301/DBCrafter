from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

from dbcrafter.backend.gui.widget.menubar.menu_bar import MenuBar

class DBMLCrafterGUI(QMainWindow):
    
    def __init__(self):
        super(DBMLCrafterGUI, self).__init__(None)
        self.setWindowTitle("DBML Crafter")
        self.setGeometry(100, 100, 800, 600)
        
        self.setMenuBar(MenuBar())
        
        self.show()

    def open_file(self):
        file_name = QFileDialog.getOpenFileName(self, "Open File")
        print(file_name)