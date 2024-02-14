from pyparsing import *

identifier = Word(alphas + "_", alphanums + "_")
number = Word(nums)
spaced_identifier = Combine(ZeroOrMore(identifier + " "))
project_keyword = Suppress(CaselessKeyword("Project"))
name_keyword = Suppress(CaselessKeyword("name"))
note_keyword = Suppress(CaselessKeyword("Note"))
table_keyword = Suppress(CaselessKeyword("Table"))
reference_keyword = Suppress(CaselessKeyword("Ref"))
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
table = Group(table_keyword + Optional(identifier.setResultsName("schemaName")+dot_point) + identifier.setResultsName("tableName") + bracket + columns.setResultsName("columns") + Optional(note_keyword+double_point+string_literal.setResultsName("tableNote")) + bracket)
tables = ZeroOrMore(table)

#  reference
reference_type = Or([Literal("-"), Literal("<"), Literal(">"), Literal("<>")])
column_reference = Group(Or([identifier.setResultsName("schema") + dot_point + identifier.setResultsName("table_name") + dot_point + identifier.setResultsName("column_name"),identifier.setResultsName("table_name") + dot_point + identifier.setResultsName("column_name")]))
long_reference = Group(reference_keyword + identifier.setResultsName("name") + bracket + \
                    column_reference.setResultsName("first_column") + reference_type.setResultsName("relation_type") + column_reference.setResultsName("second_column") + bracket)

short_reference = Group(reference_keyword + identifier.setResultsName("name") + double_point + column_reference.setResultsName("first_column") + reference_type.setResultsName("relation_type") + column_reference.setResultsName("second_column"))

references =  ZeroOrMore(Or([long_reference, short_reference]))


# dbml file
dbml_file = project_definition.setResultsName("project") + tables.setResultsName("tables") + references.setResultsName("references")


def get_dbml_tokens(content_string: str):
    
    dbml_dict = {
        "project": {
            "projectName": "",
            "projectNameValue": "",
            "projectNoteValue": ""
        },
        "tables": [],
        "references": []
    }
    
    for tokens, _, _ in dbml_file.scanString(content_string):

        dbml_dict["project"]["projectName"] = tokens.project.projectName
        dbml_dict["project"]["projectNameValue"] = tokens.project.projectNameValue
        dbml_dict["project"]["projectNoteValue"] = tokens.project.projectNoteValue
        
        for table_tokens in tokens.tables:
            table = {
                "tableName": table_tokens.tableName,
                "schemaName": "public" if "schemaName" not in table_tokens else table_tokens.schemaName,
                "columns": [],
                "tableNote": "" if "tableNote" not in table_tokens else table_tokens.tableNote
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
        print(tokens.references)
        for reference_tokens in tokens.references:
            reference = {
                "name": reference_tokens.name,
                "first_column": {
                    "schema": "public" if "schema" not in reference_tokens.first_column else reference_tokens.first_column.schema,
                    "table_name": reference_tokens.first_column.table_name,
                    "column_name": reference_tokens.first_column.column_name
                },
                "second_column": {
                    "schema": "public" if "schema" not in reference_tokens.second_column else reference_tokens.second_column.schema,
                    "table_name": reference_tokens.second_column.table_name,
                    "column_name": reference_tokens.second_column.column_name
                },
                "relation_type": reference_tokens.relation_type
            }
            dbml_dict["references"].append(reference)
    
    return dbml_dict