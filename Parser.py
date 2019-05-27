from AST import *
from ply import yacc
from Lexer import tokens

def p_ruleset(p):
    """ruleset : rule
               | rule ruleset"""
    p[0] = Ruleset(rules=[p[1]])
    if len(p) == 3:
        p[0].rules += p[2].rules

def p_rule(p):
    """rule : RULE 
            | RULE NEWLINE INDENT ruleblock DEDENT"""
    p[0] = Rule(rulename=p[1])
    if len(p) == 6:
        for block in p[4]:
            if block.__class__ == Event:
                p[0].event = block
            elif block.__class__ == Conditions:
                p[0].conditions = block
            elif block.__class__ == Actions:
                p[0].actions = block

def p_ruleblock(p):
    """ruleblock : event ruleblock
                 | conditions ruleblock
                 | actions ruleblock
                 | NEWLINE ruleblock
                 | empty"""
    p[0] = [p[1]]
    if len(p) == 3:
        p[0] += p[2]

def p_event(p):
    """event : EVENT block"""
    p[0] = Event(block=p[2])

def p_conditions(p):
    """conditions : CONDITIONS block"""
    p[0] = Conditions(block=p[2])

def p_actions(p):
    """actions : ACTIONS block"""
    p[0] = Actions(block=p[2])

def p_statements(p):
    """statements : statements statement
                  | statement"""
    p[0] = p[1]
    if len(p) == 3:
        p[0] += p[2]

def p_statement(p):
    """statement : simple_stmt"""
    p[0] = [p[1]]

def p_simple_stmt(p):
    """simple_stmt : expr NEWLINE
                   | expr"""
    p[0] = p[1]

def p_compound_stmt(p):
    """compound_stmt : number_expr
                     | value_expr
                     | action_expr"""
    p[0] = p[1]

def p_block(p):
    """block : NEWLINE INDENT statements DEDENT
             | simple_stmt"""
    p[0] = Block()
    if len(p) == 2:
        p[0].statements = [p[1]]
    elif len(p) == 5:
        p[0].statements = p[3]

def p_expr(p):
    """expr : compare
            | assign
            | ANNOTATION expr"""
    p[0] = p[1]
    if len(p) == 3:
        p[0] = p[2]

def p_arith_expr(p):
    """arith_expr : term
                  | arith_expr '+' arith_expr
                  | arith_expr '-' arith_expr"""
    p[0] = p[1]
    if len(p) == 4:
        p[0] = BinaryOp(left=p[1], op=p[2], right=p[3])

def p_term(p):
    """term : value
            | term '*' term
            | term '/' term"""
    p[0] = p[1]
    if len(p) == 4:
        p[0] = BinaryOp(left=p[1], op=p[2], right=p[3])

def p_value(p):
    """value : variable
             | compound_stmt
             | number_const
             | vector
             | unary
             | array
             | time
             | '(' compare ')'
             | empty"""
    p[0] = p[1]
    if len(p) == 4:
        p[0] = p[2]

def p_after_expr(p):
    """after_expr : '(' value_list ')'
                  | block
                  | NEWLINE"""
    p[0] = p[1]
    if p[0] == '\n':
        p[0] = None
    if len(p) == 4:
        p[0] = p[2]
    if type(p[0]) == Block:
        p[0] = p[0].statements
        if p[0][0].__class__ == Empty:
            p[0] = None

def p_value_list(p):
    """value_list : value
                  | value ',' value_list
    """
    p[0] = [p[1]]
    if len(p) == 4:
        p[0] += p[3]

def p_unary(p):
    """unary : '-' value"""
    p[0] = Negate(op=p[1], right=p[2])

def p_compare(p):
    """compare : arith_expr
               | compare COMPARE arith_expr"""
    p[0] = p[1]
    if len(p) == 4:
        p[0] = Compare(left=p[1], op=p[2], right=p[3])

def p_assign(p):
    """assign : value ASSIGN compare"""
    p[0] = Assign(left=p[1], op=p[2], right=p[3])

def p_number_expr(p):
    """number_expr : NUMBER after_expr"""
    p[0] = Number(value=p[1], args=p[2])

def p_value_expr(p):
    """value_expr : VALUE after_expr"""
    p[0] = Value(name=p[1], args=p[2])

def p_action_expr(p):
    """action_expr : ACTION after_expr"""
    p[0] = p[1]
    if len(p) == 3:
        p[0] = Action(name=p[1], args=p[2])

def p_time_expr(p):
    """time : TIME"""
    p[0] = Time(value=p[1])

def p_number_const(p):
    """number_const : INTEGER
                    | FLOAT"""
    p[0] = NumberConst(value=p[1])

def p_variable(p):
    """variable : name
                | global_var
                | player_var"""
    p[0] = p[1]

def p_name(p):
    """name : NAME"""
    p[0] = Name(value=p[1])

def p_global_var(p):
    """global_var : GLOBAL_VAR"""
    p[0] = GlobalVar(name=p[1])

def p_player_var(p):
    """player_var : PLAYER_VAR"""
    p[0] = PlayerVar(name=p[1])

def p_vector(p):
    """vector : COMPARE value ',' value ',' value COMPARE"""
    p[0] = Value(name='Vector', args=[p[2], p[4], p[6]])

def p_array(p):
    """array : '[' value_list ']'"""
    if p[2][0].__class__ == Empty:
        p[2] = None
    p[0] = Array(values=p[2])

def p_empty(p):
    """empty : COMMENT
             |"""
    p[0] = Empty()

def p_error(p):
    print('Error in parsing token', p)

Parser = yacc.yacc()