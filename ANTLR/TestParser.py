# Generated from Test.g4 by ANTLR 4.7.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
from typing.io import TextIO
import sys

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\17")
        buf.write("Q\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\4\7\t\7\4\b")
        buf.write("\t\b\4\t\t\t\4\n\t\n\4\13\t\13\4\f\t\f\3\2\3\2\7\2\33")
        buf.write("\n\2\f\2\16\2\36\13\2\3\2\3\2\3\3\3\3\5\3$\n\3\3\4\3\4")
        buf.write("\3\4\3\5\6\5*\n\5\r\5\16\5+\3\6\3\6\3\6\7\6\61\n\6\f\6")
        buf.write("\16\6\64\13\6\3\7\3\7\3\b\3\b\3\b\3\b\5\b<\n\b\3\b\3\b")
        buf.write("\3\t\3\t\3\t\6\tC\n\t\r\t\16\tD\3\t\3\t\3\n\3\n\5\nK\n")
        buf.write("\n\3\13\3\13\3\f\3\f\3\f\2\2\r\2\4\6\b\n\f\16\20\22\24")
        buf.write("\26\2\3\3\2\5\7\2M\2\34\3\2\2\2\4#\3\2\2\2\6%\3\2\2\2")
        buf.write("\b)\3\2\2\2\n-\3\2\2\2\f\65\3\2\2\2\16\67\3\2\2\2\20?")
        buf.write("\3\2\2\2\22J\3\2\2\2\24L\3\2\2\2\26N\3\2\2\2\30\33\7\13")
        buf.write("\2\2\31\33\5\4\3\2\32\30\3\2\2\2\32\31\3\2\2\2\33\36\3")
        buf.write("\2\2\2\34\32\3\2\2\2\34\35\3\2\2\2\35\37\3\2\2\2\36\34")
        buf.write("\3\2\2\2\37 \7\2\2\3 \3\3\2\2\2!$\5\6\4\2\"$\5\b\5\2#")
        buf.write("!\3\2\2\2#\"\3\2\2\2$\5\3\2\2\2%&\7\3\2\2&\'\7\n\2\2\'")
        buf.write("\7\3\2\2\2(*\5\n\6\2)(\3\2\2\2*+\3\2\2\2+)\3\2\2\2+,\3")
        buf.write("\2\2\2,\t\3\2\2\2-.\7\4\2\2.\62\5\f\7\2/\61\5\16\b\2\60")
        buf.write("/\3\2\2\2\61\64\3\2\2\2\62\60\3\2\2\2\62\63\3\2\2\2\63")
        buf.write("\13\3\2\2\2\64\62\3\2\2\2\65\66\7\b\2\2\66\r\3\2\2\2\67")
        buf.write("8\7\13\2\289\7\16\2\29;\t\2\2\2:<\5\20\t\2;:\3\2\2\2;")
        buf.write("<\3\2\2\2<=\3\2\2\2=>\7\17\2\2>\17\3\2\2\2?@\7\13\2\2")
        buf.write("@B\7\16\2\2AC\5\22\n\2BA\3\2\2\2CD\3\2\2\2DB\3\2\2\2D")
        buf.write("E\3\2\2\2EF\3\2\2\2FG\7\17\2\2G\21\3\2\2\2HK\5\26\f\2")
        buf.write("IK\7\13\2\2JH\3\2\2\2JI\3\2\2\2K\23\3\2\2\2LM\7\n\2\2")
        buf.write("M\25\3\2\2\2NO\7\t\2\2O\27\3\2\2\2\n\32\34#+\62;DJ")
        return buf.getvalue()


class TestParser ( Parser ):

    grammarFileName = "Test.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'%'", "'Rule'", "'Event'", "'Conditions'", 
                     "'Actions'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "STRING", "INTEGER", "NAME", 
                      "NEWLINE", "SKIP_", "UNKNOWN_CHAR", "INDENT", "DEDENT" ]

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
    RULE_number = 10

    ruleNames =  [ "script", "stmt", "funcdef", "ruleset", "ruledef", "rulename", 
                   "rulebody", "block", "line", "name", "number" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    STRING=6
    INTEGER=7
    NAME=8
    NEWLINE=9
    SKIP_=10
    UNKNOWN_CHAR=11
    INDENT=12
    DEDENT=13

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
            return self.getToken(TestParser.EOF, 0)

        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(TestParser.NEWLINE)
            else:
                return self.getToken(TestParser.NEWLINE, i)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TestParser.StmtContext)
            else:
                return self.getTypedRuleContext(TestParser.StmtContext,i)


        def getRuleIndex(self):
            return TestParser.RULE_script

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterScript" ):
                listener.enterScript(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitScript" ):
                listener.exitScript(self)




    def script(self):

        localctx = TestParser.ScriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_script)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 26
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << TestParser.T__0) | (1 << TestParser.T__1) | (1 << TestParser.NEWLINE))) != 0):
                self.state = 24
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [TestParser.NEWLINE]:
                    self.state = 22
                    self.match(TestParser.NEWLINE)
                    pass
                elif token in [TestParser.T__0, TestParser.T__1]:
                    self.state = 23
                    self.stmt()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 28
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 29
            self.match(TestParser.EOF)
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
            return self.getTypedRuleContext(TestParser.FuncdefContext,0)


        def ruleset(self):
            return self.getTypedRuleContext(TestParser.RulesetContext,0)


        def getRuleIndex(self):
            return TestParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)




    def stmt(self):

        localctx = TestParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 33
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [TestParser.T__0]:
                self.state = 31
                self.funcdef()
                pass
            elif token in [TestParser.T__1]:
                self.state = 32
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
            return self.getToken(TestParser.NAME, 0)

        def getRuleIndex(self):
            return TestParser.RULE_funcdef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncdef" ):
                listener.enterFuncdef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncdef" ):
                listener.exitFuncdef(self)




    def funcdef(self):

        localctx = TestParser.FuncdefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_funcdef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 35
            self.match(TestParser.T__0)
            self.state = 36
            self.match(TestParser.NAME)
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
                return self.getTypedRuleContexts(TestParser.RuledefContext)
            else:
                return self.getTypedRuleContext(TestParser.RuledefContext,i)


        def getRuleIndex(self):
            return TestParser.RULE_ruleset

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuleset" ):
                listener.enterRuleset(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuleset" ):
                listener.exitRuleset(self)




    def ruleset(self):

        localctx = TestParser.RulesetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_ruleset)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 39 
            self._errHandler.sync(self)
            _alt = 1
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt == 1:
                    self.state = 38
                    self.ruledef()

                else:
                    raise NoViableAltException(self)
                self.state = 41 
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
            return self.getTypedRuleContext(TestParser.RulenameContext,0)


        def rulebody(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TestParser.RulebodyContext)
            else:
                return self.getTypedRuleContext(TestParser.RulebodyContext,i)


        def getRuleIndex(self):
            return TestParser.RULE_ruledef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRuledef" ):
                listener.enterRuledef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRuledef" ):
                listener.exitRuledef(self)




    def ruledef(self):

        localctx = TestParser.RuledefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_ruledef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43
            self.match(TestParser.T__1)
            self.state = 44
            self.rulename()
            self.state = 48
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,4,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 45
                    self.rulebody() 
                self.state = 50
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
            return self.getToken(TestParser.STRING, 0)

        def getRuleIndex(self):
            return TestParser.RULE_rulename

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRulename" ):
                listener.enterRulename(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRulename" ):
                listener.exitRulename(self)




    def rulename(self):

        localctx = TestParser.RulenameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_rulename)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 51
            self.match(TestParser.STRING)
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
            return self.getToken(TestParser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(TestParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(TestParser.DEDENT, 0)

        def block(self):
            return self.getTypedRuleContext(TestParser.BlockContext,0)


        def getRuleIndex(self):
            return TestParser.RULE_rulebody

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRulebody" ):
                listener.enterRulebody(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRulebody" ):
                listener.exitRulebody(self)




    def rulebody(self):

        localctx = TestParser.RulebodyContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_rulebody)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(TestParser.NEWLINE)
            self.state = 54
            self.match(TestParser.INDENT)
            self.state = 55
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & ((1 << TestParser.T__2) | (1 << TestParser.T__3) | (1 << TestParser.T__4))) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 57
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==TestParser.NEWLINE:
                self.state = 56
                self.block()


            self.state = 59
            self.match(TestParser.DEDENT)
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
            return self.getToken(TestParser.NEWLINE, 0)

        def INDENT(self):
            return self.getToken(TestParser.INDENT, 0)

        def DEDENT(self):
            return self.getToken(TestParser.DEDENT, 0)

        def line(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TestParser.LineContext)
            else:
                return self.getTypedRuleContext(TestParser.LineContext,i)


        def getRuleIndex(self):
            return TestParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)




    def block(self):

        localctx = TestParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 61
            self.match(TestParser.NEWLINE)
            self.state = 62
            self.match(TestParser.INDENT)
            self.state = 64 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 63
                self.line()
                self.state = 66 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==TestParser.INTEGER or _la==TestParser.NEWLINE):
                    break

            self.state = 68
            self.match(TestParser.DEDENT)
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

        def number(self):
            return self.getTypedRuleContext(TestParser.NumberContext,0)


        def NEWLINE(self):
            return self.getToken(TestParser.NEWLINE, 0)

        def getRuleIndex(self):
            return TestParser.RULE_line

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterLine" ):
                listener.enterLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitLine" ):
                listener.exitLine(self)




    def line(self):

        localctx = TestParser.LineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_line)
        try:
            self.state = 72
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [TestParser.INTEGER]:
                self.enterOuterAlt(localctx, 1)
                self.state = 70
                self.number()
                pass
            elif token in [TestParser.NEWLINE]:
                self.enterOuterAlt(localctx, 2)
                self.state = 71
                self.match(TestParser.NEWLINE)
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
            return self.getToken(TestParser.NAME, 0)

        def getRuleIndex(self):
            return TestParser.RULE_name

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterName" ):
                listener.enterName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitName" ):
                listener.exitName(self)




    def name(self):

        localctx = TestParser.NameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_name)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 74
            self.match(TestParser.NAME)
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

        def INTEGER(self):
            return self.getToken(TestParser.INTEGER, 0)

        def getRuleIndex(self):
            return TestParser.RULE_number

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumber" ):
                listener.enterNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumber" ):
                listener.exitNumber(self)




    def number(self):

        localctx = TestParser.NumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_number)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 76
            self.match(TestParser.INTEGER)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





