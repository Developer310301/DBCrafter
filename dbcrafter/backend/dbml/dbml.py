from dbcrafter.backend.dbml.sections.project import *
from dbcrafter.backend.dbml.sections.table import Tables, Table
from dbcrafter.backend.dbml.sections.columns.column import Column
from dbcrafter.backend.dbml.dbml_parser import get_dbml_tokens

class DBMLCrafter:
    
    def __init__(self) -> None:
        self.project = Project()
        self.project.name = "database_name"
        self.project.database_type = DatabaseType.MYSQL
        self.tables = Tables()
        self.references = []

    @staticmethod
    def from_file(file_path: str) -> 'DBMLCrafter':
        with open(file_path, "r") as file:
            content = file.read()
            return DBMLCrafter.from_string(content)
        
    @staticmethod
    def from_string(content: str) -> 'DBMLCrafter':
        dbml = DBMLCrafter()
        dbml_dict = get_dbml_tokens(content)
        dbml.project.name = dbml_dict["project"]["projectNameValue"]
        dbml.project.description = dbml_dict["project"]["projectNoteValue"]
        for table in dbml_dict["tables"]:
            t = Table(table["tableName"], table["schemaName"] if "schemaName" in table else "public")
            for column in table["columns"]:
                c = Column(column["columnName"], column["columnType"], int(column["dataLength"]) if "dataLength" in column else 0)
                for setting in column["columnSettings"]:
                    if ":" in setting:
                        setting_splitted = setting.split(":")
                        c.settings.add_setting(setting_splitted[0])
                        #remove leading and trailing whitespaces
                        c.settings[setting_splitted[0]].value = str(setting_splitted[1]).strip()
                        if "char" in c.data_type or "text" in c.data_type:
                            c.settings[setting_splitted[0]].type = str
                    else:
                        c.settings.add_setting(setting)
                t.columns.add_column(c)
            dbml.tables.add_table(t)
        return dbml
    
    def to_file(self, file_path: str) -> None:
        with open(file_path, "w") as file:
            file.write(str(self))
    
    def __str__(self) -> str:
        return f"""{self.project}\n{self.tables}"""
    
    