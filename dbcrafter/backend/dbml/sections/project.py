from enum import Enum

class DatabaseType(str, Enum):
    MYSQL = "mysql"
    POSTGRES = "PostgreSQL"
    

class Project:
    def __init__(self) -> None:
        self.name = ""
        self.database_type = DatabaseType.MYSQL
        self.description = ""
    
    def __str__(self) -> str:
            return f"""Project {self.name}{{
    database_type: '{self.database_type.value}'
    Note: '{self.description}'
}}"""