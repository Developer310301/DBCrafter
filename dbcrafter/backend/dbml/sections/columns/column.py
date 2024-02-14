from dbcrafter.backend.dbml.sections.columns.column_settings import ColumnSettings

class Columns:
    
    def __init__(self) -> None:
        self.columns = []
    
    def __str__(self) -> str:
        return str.format("{0}", '\n\t'.join([str(column) for column in self.columns]))
    
    def add_column(self, column: 'Column') -> None:
        if column not in self.columns:
            self.columns.append(column)
        else:
            raise Exception(f"Column {column.name} already exists")
    
    # could get a setting by name like a dictionary ColumnSettings["setting_name"]
    def __getitem__(self, name: str) -> 'Column':
        for c in self.columns:
            if c.name == name:
                return c
        return None

    # could delete a setting by name like a dictionary del ColumnSettings["setting_name"]
    def __delitem__(self, name: str) -> None:
        for i, c in enumerate(self.columns):
            if c.name == name:
                del self.columns[i]
                return
            
    # could get the length of the settings like a list len(ColumnSettings)
    def __len__(self) -> int:
        return len(self.columns)
    
    # could iterate over the settings like a list for setting in ColumnSettings
    def __iter__(self) -> 'Column':
        return iter(self.columns)
    
    # could check if a setting is in the settings like a list setting in ColumnSettings
    def __contains__(self, name: str) -> bool:
        return name in [c.name for c in self.columns]

class Column:
    
    def __init__(self, name: str, data_type: str) -> None:
        self.name = name
        self.data_type = data_type
        self.settings = ColumnSettings()
        
    @staticmethod
    def allowed_data_types() -> list[str]:
        return ["int", "varchar", "text", "timestamp", "boolean", "json", "jsonb", "uuid", "byte", "short", "long", "float", "double", "decimal", "date", "time", "datetime", "binary", "blob", "clob", "array", "enum", "set", "geometry", "point", "linestring", "polygon", "multipoint", "multilinestring", "multipolygon", "geometrycollection"]
        
    # is a string in the format {name} {data_type} {settings}
    def __str__(self) -> str:
        return f"{self.name} {self.data_type} {self.settings}"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Column):
            return self.name == __value.name and self.schema == __value.schema
        return False