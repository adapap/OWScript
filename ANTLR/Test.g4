//grammar OWScript;
parser grammar Test;
tokens { INDENT, DEDENT }
options { tokenVocab = TestLexer; }

script : (NEWLINE | stmt)* EOF;
stmt : (funcdef | ruleset);

funcdef : '%' NAME;// funcbody?;
//funcbody : '1';

ruleset : ruledef+;
ruledef : 'Rule' rulename rulebody*;
rulename : STRING;
rulebody : NEWLINE INDENT ('Event' | 'Conditions' | 'Actions') block? DEDENT;

block : NEWLINE INDENT line+ DEDENT;
line : number
     | NEWLINE;

name : NAME;
number : INTEGER;