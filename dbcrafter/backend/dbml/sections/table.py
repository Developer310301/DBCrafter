from dbcrafter.backend.dbml.sections.columns.column import Columns
    

class Table:
    
    @property
    def complete_name(self) -> str:
        return f"{self.schema+'.' if self.schema != 'public' else ''}{self.name}"
    
    def __init__(self, name:str, schema: str = "public") -> None:
        self.name = name
        self.schema = schema
        self.columns = Columns()
        self.indexes = []
        self.note = ""
    
    def __str__(self) -> str:
        string = f"Table {self.complete_name} {{\n"
        string += f"\t{self.columns}\n"
        string += f"\tNote: '{self.note}'\n" if self.note != "" else ""
        
        return string + "}"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Table):
            return self.name == __value.name and self.schema == __value.schema
        return False
    
class Tables:
    
    def __init__(self) -> None:
        self.tables = []
        
    def __str__(self) -> str:
        string = ""
        for table in self.tables:
            string += f"{table}\n"
        return string
    
    def add_table(self, table: Table) -> None:
        if table not in self.tables:
            self.tables.append(table)
        else:
            raise Exception(f"Table {table.name} already exists")
    
    def __getitem__(self, table) -> Table | list | None:
        if isinstance(table, tuple):
            name, schema = table
        else:
            name = table
            schema = "public"
        
        if isinstance(name, slice):
            return [t for t in self.tables if t.schema == schema]
        
        if isinstance(schema, slice):
            return [t for t in self.tables if t.name == name]
        
        for t in self.tables:
            if t.name == name and t.schema == schema:
                return t
        return None
        
    def __delitem__(self, table) -> None:
        
        if isinstance(table, tuple):
            name, schema = table
        else:
            name = table
            schema = "public"
        if isinstance(name, slice):
            for i, t in enumerate(self.tables):
                if t.schema == schema:
                    del self.tables[i]
            return
        if isinstance(schema, slice):
            for i, t in enumerate(self.tables):
                if t.name == name:
                    del self.tables[i]
            return
        
        for i, t in enumerate(self.tables):
            if t.name == name and t.schema == schema:
                del self.tables[i]
                return

    def __len__(self) -> int:
        return len(self.tables)
    
    def __iter__(self) -> Table:
        return iter(self.tables)
    
    def __contains__(self,table) -> bool:
        if isinstance(table, tuple):
            name, schema = table
        else:
            name = table
            schema = "public"
            
        if isinstance(name, slice):
            return len([t for t in self.tables if t.schema == schema]) > 0
        if isinstance(schema, slice):
            return len([t for t in self.tables if t.name == name]) > 0
            
        return name in [t.name for t in self.tables if t.schema == schema and t.name == name]