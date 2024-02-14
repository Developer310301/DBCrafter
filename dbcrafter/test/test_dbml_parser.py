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
    Table users {
        id int [pk, increment, not null, unique, note: 'aas dfasdfasdfsdf']
        name varchar(100)
        email varchar
        created_at timestamp
        updated_at timestamp
        note: 'This is a sample table'
    }
    
    Table posts {
        id int [pk, increment, not null, unique]
        user_id int [not null]
        title varchar(100)
        content text
        created_at timestamp
        updated_at timestamp
    }
    
    Table test.comments {
        id int [pk, increment, not null, unique]
        post_id int [not null]
        user_id int [not null]
        content text
        created_at timestamp
        updated_at timestamp
    }
    
    Ref user_posts {
        users.id < posts.user_id
    }
    
    Ref post_comments: test.comments.post_id > posts.id
    
    """
    
    dbml_crafter = DBMLCrafter.from_string(dbml)
    print(dbml_crafter)