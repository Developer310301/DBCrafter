import sys
import argparse

from PyQt6.QtWidgets import QApplication
from dbcrafter.backend.gui.dbmlcrafter_gui import DBMLCrafterGUI

class DBMLLauncher:
    
    def __init__(self, *args, **kwargs):
        self.app = QApplication(*args, **kwargs)
        self.gui = DBMLCrafterGUI()
        self.parse_args()
        
    
    def run(self):
        self.gui.show()
        sys.exit(self.app.exec())
    
    def parse_args(self):
        parser = argparse.ArgumentParser(description="DBML Crafter")
        return parser.parse_args()
    
def main():
    launcher = DBMLLauncher([])
    launcher.run()