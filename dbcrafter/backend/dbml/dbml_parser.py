from pyparsing import *

identifier = Word(alphas + "_", alphanums + "_")
number = Word(nums)
spaced_identifier = Combine(ZeroOrMore(identifier + " "))
project_keyword = Suppress(CaselessKeyword("Project"))
name_keyword = Suppress(CaselessKeyword("name"))
note_keyword = Suppress(CaselessKeyword("Note"))
table_keyword = Suppress(CaselessKeyword("Table"))
string_literal = QuotedString("'")
bracket = Suppress(Literal("{") | Literal("}"))
square_bracket = Suppress(Literal("[") | Literal("]"))
round_bracket = Suppress(Literal("(") | Literal(")"))
double_point = Suppress(Literal(":"))
dot_point = Suppress(Literal("."))

# project
project_definition = Group(project_keyword + identifier.setResultsName("projectName") + bracket + \
                    name_keyword + double_point + string_literal.setResultsName("projectNameValue") + \
                    note_keyword + double_point + string_literal.setResultsName("projectNoteValue") + bracket)

#table
column_setting = Combine(identifier + Optional(Or([Literal(" ") + identifier, Literal(":") + Optional(ZeroOrMore(Literal(" "))) + Or([identifier, string_literal])])))
column_settings = Group(Optional(square_bracket+ZeroOrMore(delimitedList(OneOrMore(column_setting), delim=","))+square_bracket))
column = Group(identifier.setResultsName("columnName") + identifier.setResultsName("columnType") + Optional(round_bracket + number.setResultsName("dataLength") + round_bracket) + column_settings.setResultsName("columnSettings"))
columns = ZeroOrMore(column)
table = Group(table_keyword + Optional(identifier.setResultsName("schemaName")+dot_point) + identifier.setResultsName("tableName") + bracket + columns.setResultsName("columns") + bracket)
tables = ZeroOrMore(table)

# dbml file
dbml_file = project_definition.setResultsName("project") + tables.setResultsName("tables")


def get_dbml_tokens(content_string: str):
    
    dbml_dict = {
        "project": {
            "projectName": "",
            "projectNameValue": "",
            "projectNoteValue": ""
        },
        "tables": []
    }
    
    for tokens, _, _ in dbml_file.scanString(content_string):
        
        #print(tokens)

        dbml_dict["project"]["projectName"] = tokens.project.projectName
        dbml_dict["project"]["projectNameValue"] = tokens.project.projectNameValue
        dbml_dict["project"]["projectNoteValue"] = tokens.project.projectNoteValue
        
        for table_tokens in tokens.tables:
            table = {
                "tableName": table_tokens.tableName,
                "schemaName": "public" if "schemaName" not in table_tokens else table_tokens.schemaName,
                "columns": []
            }
            for column_tokens in table_tokens.columns:
                column = {
                    "columnName": column_tokens.columnName,
                    "dataLength": column_tokens.dataLength if "dataLength" in column_tokens else 0,
                    "columnType": column_tokens.columnType,
                    "columnSettings": []
                }
                for setting in column_tokens.columnSettings:
                    column["columnSettings"].append(setting)
                table["columns"].append(column)
            dbml_dict["tables"].append(table)
    
    return dbml_dict