from dbcrafter.backend.dbml.dbml import DBMLCrafter, DatabaseType
from dbcrafter.backend.dbml.sections.table import Table
from dbcrafter.backend.dbml.sections.columns.column import *

if __name__ == "__main__":
    dbml = DBMLCrafter()
    dbml.project.name = "TestDB"
    dbml.project.database_type = DatabaseType.POSTGRES
    dbml.project.description = "This is a test database"
    dbml.tables.add_table(Table("test_table"))
    dbml.tables["test_table"].columns.add_column(Column("id", "int"))
    dbml.tables["test_table"].columns.add_column(Column("name", "varchar"))
    dbml.tables["test_table"].columns["id"].settings.add_setting("pk")
    dbml.tables["test_table"].columns["id"].settings.add_setting("not null")
    dbml.tables.add_table(Table("test_table", "test_schema"))
    dbml.tables["test_table", "test_schema"].columns.add_column(Column("id", "int"))
    dbml.tables["test_table", "test_schema"].note = "This is a test table"
    print(dbml)