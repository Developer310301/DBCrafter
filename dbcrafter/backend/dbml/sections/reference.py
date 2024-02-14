from enum import Enum

from dbcrafter.backend.dbml.sections.table import Table
from dbcrafter.backend.dbml.sections.columns.column import Column

class ReferenceType(int, Enum):
    ONE_TO_ONE = 1
    ONE_TO_MANY = 2
    MANY_TO_ONE = 3
    MANY_TO_MANY = 4
    
    @staticmethod
    def from_string(value: str) -> 'ReferenceType':
        if value.lower() == "-":
            return ReferenceType.ONE_TO_ONE
        if value.lower() == "<":
            return ReferenceType.ONE_TO_MANY
        if value.lower() == ">":
            return ReferenceType.MANY_TO_ONE
        if value.lower() == "<>":
            return ReferenceType.MANY_TO_MANY
        raise Exception(f"ReferenceType {value} not found")
    
    def __str__(self) -> str:
        if self == ReferenceType.ONE_TO_ONE:
            return "-"
        if self == ReferenceType.ONE_TO_MANY:
            return "<"
        if self == ReferenceType.MANY_TO_ONE:
            return ">"
        if self == ReferenceType.MANY_TO_MANY:
            return "<>"
        raise Exception(f"ReferenceType {self} not found")

class Reference:
    def __init__(self, name: str, first_table: Table, first_column: str, second_table: Table, second_column: str, relation_type: ReferenceType):
        self.name = name
        self.first_table = first_table
        self.first_column = first_column
        self.second_table = second_table
        self.second_column = second_column
        self.relation_type = relation_type
        
        if self.first_table is None or self.first_column not in self.first_table.columns:
            raise Exception(f"Column {self.first_column} not found in table {self.first_table}")
        if second_table is None or self.second_column not in self.second_table.columns:
            raise Exception(f"Column {self.second_column} not found in table {self.second_table}")

    def __str__(self):
        return f"""Ref {self.name} {{
    {self.first_table.complete_name}.{self.first_column} {str(self.relation_type)} {self.second_table.complete_name}.{self.second_column}
}}
"""

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name and self.first_table == other.first_table and self.first_column == other.first_column and self.second_table == other.second_table and self.second_column == other.second_column and self.relation_type == other.relation_type
    
    
class References:
    
    def __init__(self) -> None:
        self.references = []
        
    def __str__(self) -> str:
        string = ""
        for reference in self.references:
            string += f"{reference}\n"
        return string
    
    def add_reference(self, reference: Reference) -> None:
        if reference not in self.references:
            self.references.append(reference)
        else:
            raise Exception(f"Reference {reference.name} already exists")
        
    def __getitem__(self, reference) -> Reference | list | None:
        if isinstance(reference, str):
            return [r for r in self.references if r.name == reference]
        return None
    
    def __delitem__(self, reference) -> None:
        if isinstance(reference, str):
            for i, r in enumerate(self.references):
                if r.name == reference:
                    del self.references[i]
                    return
        else:
            for i, r in enumerate(self.references):
                if r == reference:
                    del self.references[i]
                    return
                
    def __len__(self) -> int:
        return len(self.references)
    
    def __iter__(self) -> Reference:
        return iter(self.references)
    
    def __contains__(self, reference) -> bool:
        if isinstance(reference, str):
            return reference in [r.name for r in self.references]
        return reference in self.references
    
    def __eq__(self, other):
        return self.references == other.references