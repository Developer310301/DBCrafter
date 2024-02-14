from dbcrafter.backend.dbml.dbml import DBMLCrafter, DatabaseType
from dbcrafter.backend.dbml.sections.table import Table
from dbcrafter.backend.dbml.sections.columns.column import *
from dbcrafter.backend.dbml.dbml_parser import get_dbml_tokens

if __name__ == "__main__":

    dbml = """
    Project MyProject {
        name: 'MySampleDB'
        Note: 'This is my sample DBML project'
    }
    Table db.users {
        id int [pk, increment, not null, unique, note: 'aas dfasdfasdfsdf']
        name varchar(100)
        email varchar
        created_at timestamp
        updated_at timestamp
    }
    """
    
    dbml_crafter = DBMLCrafter.from_string(dbml)
    print(dbml_crafter)