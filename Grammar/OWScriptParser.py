# Generated from OWScript.g4 by ANTLR 4.7.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\24")
        buf.write("j\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\4\r\t\r\4\16\t")
        buf.write("\16\4\17\t\17\4\20\t\20\3\2\3\2\7\2#\n\2\f\2\16\2&\13")
        buf.write("\2\3\2\3\2\3\3\3\3\5\3,\n\3\3\4\3\4\3\4\3\5\6\5\62\n\5")
        buf.write("\r\5\16\5\63\3\6\3\6\3\6\7\69\n\6\f\6\16\6<\13\6\3\7\3")
        buf.write("\7\3\b\3\b\3\b\3\b\5\bD\n\b\3\b\3\b\3\t\3\t\3\t\6\tK\n")
        buf.write("\t\r\t\16\tL\3\t\3\t\3\n\3\n\3\n\3\n\3\n\3\n\5\nW\n\n")
        buf.write("\3\13\3\13\3\f\3\f\3\f\3\r\3\r\3\r\3\16\3\16\3\16\3\17")
        buf.write("\3\17\3\17\3\17\3\20\3\20\3\20\2\2\21\2\4\6\b\n\f\16\20")
        buf.write("\22\24\26\30\32\34\36\2\3\3\2\5\7\2f\2$\3\2\2\2\4+\3\2")
        buf.write("\2\2\6-\3\2\2\2\b\61\3\2\2\2\n\65\3\2\2\2\f=\3\2\2\2\16")
        buf.write("?\3\2\2\2\20G\3\2\2\2\22V\3\2\2\2\24X\3\2\2\2\26Z\3\2")
        buf.write("\2\2\30]\3\2\2\2\32`\3\2\2\2\34c\3\2\2\2\36g\3\2\2\2 ")
        buf.write("#\7\f\2\2!#\5\4\3\2\" \3\2\2\2\"!\3\2\2\2#&\3\2\2\2$\"")
        buf.write("\3\2\2\2$%\3\2\2\2%\'\3\2\2\2&$\3\2\2\2\'(\7\2\2\3(\3")
        buf.write("\3\2\2\2),\5\6\4\2*,\5\b\5\2+)\3\2\2\2+*\3\2\2\2,\5\3")
        buf.write("\2\2\2-.\7\3\2\2./\7\13\2\2/\7\3\2\2\2\60\62\5\n\6\2\61")
        buf.write("\60\3\2\2\2\62\63\3\2\2\2\63\61\3\2\2\2\63\64\3\2\2\2")
        buf.write("\64\t\3\2\2\2\65\66\7\4\2\2\66:\5\f\7\2\679\5\16\b\28")
        buf.write("\67\3\2\2\29<\3\2\2\2:8\3\2\2\2:;\3\2\2\2;\13\3\2\2\2")
        buf.write("<:\3\2\2\2=>\7\b\2\2>\r\3\2\2\2?@\7\f\2\2@A\7\17\2\2A")
        buf.write("C\t\2\2\2BD\5\20\t\2CB\3\2\2\2CD\3\2\2\2DE\3\2\2\2EF\7")
        buf.write("\20\2\2F\17\3\2\2\2GH\7\f\2\2HJ\7\17\2\2IK\5\22\n\2JI")
        buf.write("\3\2\2\2KL\3\2\2\2LJ\3\2\2\2LM\3\2\2\2MN\3\2\2\2NO\7\20")
        buf.write("\2\2O\21\3\2\2\2PW\5\26\f\2QW\5\30\r\2RW\5\32\16\2SW\5")
        buf.write("\34\17\2TW\5\24\13\2UW\7\f\2\2VP\3\2\2\2VQ\3\2\2\2VR\3")
        buf.write("\2\2\2VS\3\2\2\2VT\3\2\2\2VU\3\2\2\2W\23\3\2\2\2XY\7\13")
        buf.write("\2\2Y\25\3\2\2\2Z[\7\21\2\2[\\\5\36\20\2\\\27\3\2\2\2")
        buf.write("]^\7\22\2\2^_\5\36\20\2_\31\3\2\2\2`a\7\23\2\2ab\5\36")
        buf.write("\20\2b\33\3\2\2\2cd\7\t\2\2de\7\24\2\2ef\7\t\2\2f\35\3")
        buf.write("\2\2\2gh\7\f\2\2h\37\3\2\2\2\n\"$+\63:CLV")
        return buf.getvalue()


class OWScriptParser ( Parser ):

    grammarFileName = "OWScript.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'%'", "'Rule'", "'Event'", "'Conditions'", 
                     "'Actions'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "STRING", "INTEGER", "FLOAT", 
                      "NAME", "NEWLINE", "SKIP_", "UNKNOWN_CHAR", "INDENT", 
                      "DEDENT", "ACTION", "VALUE", "NUMBER", "ASSIGN" ]

    RULE_script = 0
    RULE_stmt = 1
    RULE_funcdef = 2
    RULE_ruleset = 3
    RULE_ruledef = 4
    RULE_rulename = 5
    RULE_rulebody = 6
    RULE_block = 7
    RULE_line = 8
    RULE_name = 9
    RULE_action = 10
    RULE_value = 11
    RULE_number = 12
    RULE_assign = 13
    RULE_after_line = 14

    ruleNames =  [ "script", "stmt", "funcdef", "ruleset", "ruledef", "rulename", 
                   "rulebody", "block", "line", "name", "action", "value", 
                   "number", "assign", "after_line" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    STRING=6
    INTEGER=7
    FLOAT=8
    NAME=9
    NEWLINE=10
    SKIP_=11
    UNKNOWN_CHAR=12
    INDENT=13
    DEDENT=14
    ACTION=15
    VALUE=16
    NUMBER=17
    ASSIGN=18

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.7.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None



    class ScriptContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(OWScriptParser.EOF, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(OWScriptParser.NEWLINE)
            else:
                return self.getToken(OWScriptParser.NEWLINE, i)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OWScriptParser.StmtContext)
            else:
                return self.getTypedRuleContext(OWScriptParser.StmtContext,i)


        def getRuleIndex(self):
            return OWScriptParser.RULE_script

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterScript" ):
                listener.enterScript(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitScript" ):
                listener.exitScript(self)




    def script(self):

        localctx = OWScriptParser.ScriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_script)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 34
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OWScriptParser.T__0) | (1 << OWScriptParser.T__1) | (1 << OWScriptParser.NEWLINE))) != 0):
                self.state = 32
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [OWScriptParser.NEWLINE]:
                    self.state = 30
                    self.match(OWScriptParser.NEWLINE)
                    pass
                elif token in [OWScriptParser.T__0, OWScriptParser.T__1]:
                    self.state = 31
                    self.stmt()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 36
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 37
            self.match(OWScriptParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class StmtContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def funcdef(self):
            return self.getTypedRuleContext(OWScriptParser.FuncdefContext,0)


        def ruleset(self):
            return self.getTypedRuleContext(OWScriptParser.RulesetContext,0)


        def getRuleIndex(self):
            return OWScriptParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)




    def stmt(self):

        localctx = OWScriptParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 41
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OWScriptParser.T__0]:
                self.state = 39
                self.funcdef()
                pass
            elif token in [OWScriptParser.T__1]:
                self.state = 40
                self.ruleset()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class FuncdefContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(OWScriptParser.NAME, 0)

        def getRuleIndex(self):
            return OWScriptParser.RULE_funcdef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncdef" ):
                listener.enterFuncdef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncdef" ):
                listener.exitFuncdef(self)




    def funcdef(self):

        localctx = OWScriptParser.FuncdefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_funcdef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.match(OWScriptParser.T__0)
            self.state = 44
            self.match(OWScriptParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RulesetContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ruledef(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OWScriptParser.RuledefContext)
            else:
                return self.getTypedRuleContext(OWScriptParser.RuledefContext,i)


        def getRuleIndex(self):
            return OWScriptParser.RULE_ruleset

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleset" ):
                listener.enterRuleset(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleset" ):
                listener.exitRuleset(self)




    def ruleset(self):

        localctx = OWScriptParser.RulesetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_ruleset)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 47 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 46
                    self.ruledef()

                else:
                    raise NoViableAltException(self)
                self.state = 49 
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RuledefContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def rulename(self):
            return self.getTypedRuleContext(OWScriptParser.RulenameContext,0)


        def rulebody(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OWScriptParser.RulebodyContext)
            else:
                return self.getTypedRuleContext(OWScriptParser.RulebodyContext,i)


        def getRuleIndex(self):
            return OWScriptParser.RULE_ruledef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuledef" ):
                listener.enterRuledef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuledef" ):
                listener.exitRuledef(self)




    def ruledef(self):

        localctx = OWScriptParser.RuledefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_ruledef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(OWScriptParser.T__1)
            self.state = 52
            self.rulename()
            self.state = 56
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 53
                    self.rulebody() 
                self.state = 58
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,4,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RulenameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(OWScriptParser.STRING, 0)

        def getRuleIndex(self):
            return OWScriptParser.RULE_rulename

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRulename" ):
                listener.enterRulename(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRulename" ):
                listener.exitRulename(self)




    def rulename(self):

        localctx = OWScriptParser.RulenameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_rulename)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 59
            self.match(OWScriptParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class RulebodyContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEWLINE(self):
            return self.getToken(OWScriptParser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(OWScriptParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(OWScriptParser.DEDENT, 0)

        def block(self):
            return self.getTypedRuleContext(OWScriptParser.BlockContext,0)


        def getRuleIndex(self):
            return OWScriptParser.RULE_rulebody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRulebody" ):
                listener.enterRulebody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRulebody" ):
                listener.exitRulebody(self)




    def rulebody(self):

        localctx = OWScriptParser.RulebodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_rulebody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(OWScriptParser.NEWLINE)
            self.state = 62
            self.match(OWScriptParser.INDENT)
            self.state = 63
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OWScriptParser.T__2) | (1 << OWScriptParser.T__3) | (1 << OWScriptParser.T__4))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 65
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==OWScriptParser.NEWLINE:
                self.state = 64
                self.block()


            self.state = 67
            self.match(OWScriptParser.DEDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class BlockContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEWLINE(self):
            return self.getToken(OWScriptParser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(OWScriptParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(OWScriptParser.DEDENT, 0)

        def line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(OWScriptParser.LineContext)
            else:
                return self.getTypedRuleContext(OWScriptParser.LineContext,i)


        def getRuleIndex(self):
            return OWScriptParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)




    def block(self):

        localctx = OWScriptParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 69
            self.match(OWScriptParser.NEWLINE)
            self.state = 70
            self.match(OWScriptParser.INDENT)
            self.state = 72 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 71
                self.line()
                self.state = 74 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << OWScriptParser.INTEGER) | (1 << OWScriptParser.NAME) | (1 << OWScriptParser.NEWLINE) | (1 << OWScriptParser.ACTION) | (1 << OWScriptParser.VALUE) | (1 << OWScriptParser.NUMBER))) != 0)):
                    break

            self.state = 76
            self.match(OWScriptParser.DEDENT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class LineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def action(self):
            return self.getTypedRuleContext(OWScriptParser.ActionContext,0)


        def value(self):
            return self.getTypedRuleContext(OWScriptParser.ValueContext,0)


        def number(self):
            return self.getTypedRuleContext(OWScriptParser.NumberContext,0)


        def assign(self):
            return self.getTypedRuleContext(OWScriptParser.AssignContext,0)


        def name(self):
            return self.getTypedRuleContext(OWScriptParser.NameContext,0)


        def NEWLINE(self):
            return self.getToken(OWScriptParser.NEWLINE, 0)

        def getRuleIndex(self):
            return OWScriptParser.RULE_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLine" ):
                listener.enterLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLine" ):
                listener.exitLine(self)




    def line(self):

        localctx = OWScriptParser.LineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_line)
        try:
            self.state = 84
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [OWScriptParser.ACTION]:
                self.enterOuterAlt(localctx, 1)
                self.state = 78
                self.action()
                pass
            elif token in [OWScriptParser.VALUE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 79
                self.value()
                pass
            elif token in [OWScriptParser.NUMBER]:
                self.enterOuterAlt(localctx, 3)
                self.state = 80
                self.number()
                pass
            elif token in [OWScriptParser.INTEGER]:
                self.enterOuterAlt(localctx, 4)
                self.state = 81
                self.assign()
                pass
            elif token in [OWScriptParser.NAME]:
                self.enterOuterAlt(localctx, 5)
                self.state = 82
                self.name()
                pass
            elif token in [OWScriptParser.NEWLINE]:
                self.enterOuterAlt(localctx, 6)
                self.state = 83
                self.match(OWScriptParser.NEWLINE)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NameContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NAME(self):
            return self.getToken(OWScriptParser.NAME, 0)

        def getRuleIndex(self):
            return OWScriptParser.RULE_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName" ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName" ):
                listener.exitName(self)




    def name(self):

        localctx = OWScriptParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 86
            self.match(OWScriptParser.NAME)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ActionContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ACTION(self):
            return self.getToken(OWScriptParser.ACTION, 0)

        def after_line(self):
            return self.getTypedRuleContext(OWScriptParser.After_lineContext,0)


        def getRuleIndex(self):
            return OWScriptParser.RULE_action

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAction" ):
                listener.enterAction(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAction" ):
                listener.exitAction(self)




    def action(self):

        localctx = OWScriptParser.ActionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_action)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 88
            self.match(OWScriptParser.ACTION)
            self.state = 89
            self.after_line()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ValueContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VALUE(self):
            return self.getToken(OWScriptParser.VALUE, 0)

        def after_line(self):
            return self.getTypedRuleContext(OWScriptParser.After_lineContext,0)


        def getRuleIndex(self):
            return OWScriptParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)




    def value(self):

        localctx = OWScriptParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_value)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 91
            self.match(OWScriptParser.VALUE)
            self.state = 92
            self.after_line()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class NumberContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NUMBER(self):
            return self.getToken(OWScriptParser.NUMBER, 0)

        def after_line(self):
            return self.getTypedRuleContext(OWScriptParser.After_lineContext,0)


        def getRuleIndex(self):
            return OWScriptParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = OWScriptParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(OWScriptParser.NUMBER)
            self.state = 95
            self.after_line()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class AssignContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INTEGER(self, i:int=None):
            if i is None:
                return self.getTokens(OWScriptParser.INTEGER)
            else:
                return self.getToken(OWScriptParser.INTEGER, i)

        def ASSIGN(self):
            return self.getToken(OWScriptParser.ASSIGN, 0)

        def getRuleIndex(self):
            return OWScriptParser.RULE_assign

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssign" ):
                listener.enterAssign(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssign" ):
                listener.exitAssign(self)




    def assign(self):

        localctx = OWScriptParser.AssignContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_assign)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 97
            self.match(OWScriptParser.INTEGER)
            self.state = 98
            self.match(OWScriptParser.ASSIGN)
            self.state = 99
            self.match(OWScriptParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class After_lineContext(ParserRuleContext):

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NEWLINE(self):
            return self.getToken(OWScriptParser.NEWLINE, 0)

        def getRuleIndex(self):
            return OWScriptParser.RULE_after_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAfter_line" ):
                listener.enterAfter_line(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAfter_line" ):
                listener.exitAfter_line(self)




    def after_line(self):

        localctx = OWScriptParser.After_lineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_after_line)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 101
            self.match(OWScriptParser.NEWLINE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





