from dbcrafter.backend.dbml.sections.project import *
from dbcrafter.backend.dbml.sections.table import Tables

class DBMLCrafter:
    
    def __init__(self) -> None:
        self.project = Project()
        self.project.name = "database_name"
        self.project.database_type = DatabaseType.MYSQL
        self.tables = Tables()
        self.references = []

    @staticmethod
    def from_file(file_path: str) -> 'DBMLCrafter':
        pass
    
    def to_file(self, file_path: str) -> None:
        pass
    
    def __str__(self) -> str:
        return f"""{self.project}\n{self.tables}"""
    
    