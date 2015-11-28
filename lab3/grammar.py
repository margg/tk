"""grammar"""

# """program : instruction_list"""

# """instruction_list : instruction_list instruction_item
#                         | """

"""instruction_item : declarations
                        | fundefs_opt
                        | instructions_opt"""

# """declarations : declarations declaration
#                     | """
#
# """declaration : TYPE inits ';'
#                    | error ';' """
#
# """inits : inits ',' init
#              | init """
#
# """init : ID '=' expression """

"""instructions_opt : instructions
                        | """

"""instructions : instructions instruction
                    | instruction """

"""instruction : print_instr
                   | labeled_instr
                   | assignment
                   | choice_instr
                   | while_instr
                   | repeat_instr
                   | return_instr
                   | break_instr
                   | continue_instr
                   | compound_instr
                   | expression ';' """

"""print_instr : PRINT expr_list ';'
                   | PRINT error ';' """

"""labeled_instr : ID ':' instruction """

"""assignment : ID '=' expression ';' """

"""choice_instr : IF '(' condition ')' instruction  %prec IFX
                    | IF '(' condition ')' instruction ELSE instruction
                    | IF '(' error ')' instruction  %prec IFX
                    | IF '(' error ')' instruction ELSE instruction """

"""while_instr : WHILE '(' condition ')' instruction
                   | WHILE '(' error ')' instruction """

"""repeat_instr : REPEAT instructions UNTIL condition ';' """

"""return_instr : RETURN expression ';' """

"""continue_instr : CONTINUE ';' """

"""break_instr : BREAK ';' """

"""compound_instr : '{' declarations instructions_opt '}' """

"""condition : expression"""

# """const : INTEGER
#              | FLOAT
#              | STRING"""

"""expression : const
                  | ID
                  | expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression '%' expression
                  | expression '|' expression
                  | expression '&' expression
                  | expression '^' expression
                  | expression AND expression
                  | expression OR expression
                  | expression SHL expression
                  | expression SHR expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression '>' expression
                  | expression '<' expression
                  | expression LE expression
                  | expression GE expression
                  | '(' expression ')'
                  | '(' error ')'
                  | ID '(' expr_list_or_empty ')'
                  | ID '(' error ')' """

"""expr_list_or_empty : expr_list
                          | """

"""expr_list : expr_list ',' expression
                 | expression """

"""fundefs_opt : fundefs
                   | """

"""fundefs : fundefs fundef
               | fundef """

"""fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """

"""args_list_or_empty : args_list
                          | """

"""args_list : args_list ',' arg
                 | arg """

"""arg : TYPE ID """