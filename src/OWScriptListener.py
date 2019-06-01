# Generated from OWScript.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .OWScriptParser import OWScriptParser
else:
    from OWScriptParser import OWScriptParser

# This class defines a complete listener for a parse tree produced by OWScriptParser.
class OWScriptListener(ParseTreeListener):

    # Enter a parse tree produced by OWScriptParser#script.
    def enterScript(self, ctx:OWScriptParser.ScriptContext):
        pass

    # Exit a parse tree produced by OWScriptParser#script.
    def exitScript(self, ctx:OWScriptParser.ScriptContext):
        pass


    # Enter a parse tree produced by OWScriptParser#stmt.
    def enterStmt(self, ctx:OWScriptParser.StmtContext):
        pass

    # Exit a parse tree produced by OWScriptParser#stmt.
    def exitStmt(self, ctx:OWScriptParser.StmtContext):
        pass


    # Enter a parse tree produced by OWScriptParser#funcdef.
    def enterFuncdef(self, ctx:OWScriptParser.FuncdefContext):
        pass

    # Exit a parse tree produced by OWScriptParser#funcdef.
    def exitFuncdef(self, ctx:OWScriptParser.FuncdefContext):
        pass


    # Enter a parse tree produced by OWScriptParser#funcbody.
    def enterFuncbody(self, ctx:OWScriptParser.FuncbodyContext):
        pass

    # Exit a parse tree produced by OWScriptParser#funcbody.
    def exitFuncbody(self, ctx:OWScriptParser.FuncbodyContext):
        pass


    # Enter a parse tree produced by OWScriptParser#ruleset.
    def enterRuleset(self, ctx:OWScriptParser.RulesetContext):
        pass

    # Exit a parse tree produced by OWScriptParser#ruleset.
    def exitRuleset(self, ctx:OWScriptParser.RulesetContext):
        pass


    # Enter a parse tree produced by OWScriptParser#ruledef.
    def enterRuledef(self, ctx:OWScriptParser.RuledefContext):
        pass

    # Exit a parse tree produced by OWScriptParser#ruledef.
    def exitRuledef(self, ctx:OWScriptParser.RuledefContext):
        pass


    # Enter a parse tree produced by OWScriptParser#rulename.
    def enterRulename(self, ctx:OWScriptParser.RulenameContext):
        pass

    # Exit a parse tree produced by OWScriptParser#rulename.
    def exitRulename(self, ctx:OWScriptParser.RulenameContext):
        pass


    # Enter a parse tree produced by OWScriptParser#RulebodyBlock.
    def enterRulebodyBlock(self, ctx:OWScriptParser.RulebodyBlockContext):
        pass

    # Exit a parse tree produced by OWScriptParser#RulebodyBlock.
    def exitRulebodyBlock(self, ctx:OWScriptParser.RulebodyBlockContext):
        pass


    # Enter a parse tree produced by OWScriptParser#RCall.
    def enterRCall(self, ctx:OWScriptParser.RCallContext):
        pass

    # Exit a parse tree produced by OWScriptParser#RCall.
    def exitRCall(self, ctx:OWScriptParser.RCallContext):
        pass


    # Enter a parse tree produced by OWScriptParser#ruleblock.
    def enterRuleblock(self, ctx:OWScriptParser.RuleblockContext):
        pass

    # Exit a parse tree produced by OWScriptParser#ruleblock.
    def exitRuleblock(self, ctx:OWScriptParser.RuleblockContext):
        pass


    # Enter a parse tree produced by OWScriptParser#block.
    def enterBlock(self, ctx:OWScriptParser.BlockContext):
        pass

    # Exit a parse tree produced by OWScriptParser#block.
    def exitBlock(self, ctx:OWScriptParser.BlockContext):
        pass


    # Enter a parse tree produced by OWScriptParser#line.
    def enterLine(self, ctx:OWScriptParser.LineContext):
        pass

    # Exit a parse tree produced by OWScriptParser#line.
    def exitLine(self, ctx:OWScriptParser.LineContext):
        pass


    # Enter a parse tree produced by OWScriptParser#assign.
    def enterAssign(self, ctx:OWScriptParser.AssignContext):
        pass

    # Exit a parse tree produced by OWScriptParser#assign.
    def exitAssign(self, ctx:OWScriptParser.AssignContext):
        pass


    # Enter a parse tree produced by OWScriptParser#if_stmt.
    def enterIf_stmt(self, ctx:OWScriptParser.If_stmtContext):
        pass

    # Exit a parse tree produced by OWScriptParser#if_stmt.
    def exitIf_stmt(self, ctx:OWScriptParser.If_stmtContext):
        pass


    # Enter a parse tree produced by OWScriptParser#expr.
    def enterExpr(self, ctx:OWScriptParser.ExprContext):
        pass

    # Exit a parse tree produced by OWScriptParser#expr.
    def exitExpr(self, ctx:OWScriptParser.ExprContext):
        pass


    # Enter a parse tree produced by OWScriptParser#logic_or.
    def enterLogic_or(self, ctx:OWScriptParser.Logic_orContext):
        pass

    # Exit a parse tree produced by OWScriptParser#logic_or.
    def exitLogic_or(self, ctx:OWScriptParser.Logic_orContext):
        pass


    # Enter a parse tree produced by OWScriptParser#logic_and.
    def enterLogic_and(self, ctx:OWScriptParser.Logic_andContext):
        pass

    # Exit a parse tree produced by OWScriptParser#logic_and.
    def exitLogic_and(self, ctx:OWScriptParser.Logic_andContext):
        pass


    # Enter a parse tree produced by OWScriptParser#logic_not.
    def enterLogic_not(self, ctx:OWScriptParser.Logic_notContext):
        pass

    # Exit a parse tree produced by OWScriptParser#logic_not.
    def exitLogic_not(self, ctx:OWScriptParser.Logic_notContext):
        pass


    # Enter a parse tree produced by OWScriptParser#compare.
    def enterCompare(self, ctx:OWScriptParser.CompareContext):
        pass

    # Exit a parse tree produced by OWScriptParser#compare.
    def exitCompare(self, ctx:OWScriptParser.CompareContext):
        pass


    # Enter a parse tree produced by OWScriptParser#Pow.
    def enterPow(self, ctx:OWScriptParser.PowContext):
        pass

    # Exit a parse tree produced by OWScriptParser#Pow.
    def exitPow(self, ctx:OWScriptParser.PowContext):
        pass


    # Enter a parse tree produced by OWScriptParser#Mul.
    def enterMul(self, ctx:OWScriptParser.MulContext):
        pass

    # Exit a parse tree produced by OWScriptParser#Mul.
    def exitMul(self, ctx:OWScriptParser.MulContext):
        pass


    # Enter a parse tree produced by OWScriptParser#Div.
    def enterDiv(self, ctx:OWScriptParser.DivContext):
        pass

    # Exit a parse tree produced by OWScriptParser#Div.
    def exitDiv(self, ctx:OWScriptParser.DivContext):
        pass


    # Enter a parse tree produced by OWScriptParser#Add.
    def enterAdd(self, ctx:OWScriptParser.AddContext):
        pass

    # Exit a parse tree produced by OWScriptParser#Add.
    def exitAdd(self, ctx:OWScriptParser.AddContext):
        pass


    # Enter a parse tree produced by OWScriptParser#Sub.
    def enterSub(self, ctx:OWScriptParser.SubContext):
        pass

    # Exit a parse tree produced by OWScriptParser#Sub.
    def exitSub(self, ctx:OWScriptParser.SubContext):
        pass


    # Enter a parse tree produced by OWScriptParser#Mod.
    def enterMod(self, ctx:OWScriptParser.ModContext):
        pass

    # Exit a parse tree produced by OWScriptParser#Mod.
    def exitMod(self, ctx:OWScriptParser.ModContext):
        pass


    # Enter a parse tree produced by OWScriptParser#ArithPrimary.
    def enterArithPrimary(self, ctx:OWScriptParser.ArithPrimaryContext):
        pass

    # Exit a parse tree produced by OWScriptParser#ArithPrimary.
    def exitArithPrimary(self, ctx:OWScriptParser.ArithPrimaryContext):
        pass


    # Enter a parse tree produced by OWScriptParser#PItem.
    def enterPItem(self, ctx:OWScriptParser.PItemContext):
        pass

    # Exit a parse tree produced by OWScriptParser#PItem.
    def exitPItem(self, ctx:OWScriptParser.PItemContext):
        pass


    # Enter a parse tree produced by OWScriptParser#PCall.
    def enterPCall(self, ctx:OWScriptParser.PCallContext):
        pass

    # Exit a parse tree produced by OWScriptParser#PCall.
    def exitPCall(self, ctx:OWScriptParser.PCallContext):
        pass


    # Enter a parse tree produced by OWScriptParser#PrimaryNone.
    def enterPrimaryNone(self, ctx:OWScriptParser.PrimaryNoneContext):
        pass

    # Exit a parse tree produced by OWScriptParser#PrimaryNone.
    def exitPrimaryNone(self, ctx:OWScriptParser.PrimaryNoneContext):
        pass


    # Enter a parse tree produced by OWScriptParser#primary.
    def enterPrimary(self, ctx:OWScriptParser.PrimaryContext):
        pass

    # Exit a parse tree produced by OWScriptParser#primary.
    def exitPrimary(self, ctx:OWScriptParser.PrimaryContext):
        pass


    # Enter a parse tree produced by OWScriptParser#action.
    def enterAction(self, ctx:OWScriptParser.ActionContext):
        pass

    # Exit a parse tree produced by OWScriptParser#action.
    def exitAction(self, ctx:OWScriptParser.ActionContext):
        pass


    # Enter a parse tree produced by OWScriptParser#value.
    def enterValue(self, ctx:OWScriptParser.ValueContext):
        pass

    # Exit a parse tree produced by OWScriptParser#value.
    def exitValue(self, ctx:OWScriptParser.ValueContext):
        pass


    # Enter a parse tree produced by OWScriptParser#const.
    def enterConst(self, ctx:OWScriptParser.ConstContext):
        pass

    # Exit a parse tree produced by OWScriptParser#const.
    def exitConst(self, ctx:OWScriptParser.ConstContext):
        pass


    # Enter a parse tree produced by OWScriptParser#after_line.
    def enterAfter_line(self, ctx:OWScriptParser.After_lineContext):
        pass

    # Exit a parse tree produced by OWScriptParser#after_line.
    def exitAfter_line(self, ctx:OWScriptParser.After_lineContext):
        pass


    # Enter a parse tree produced by OWScriptParser#arg_list.
    def enterArg_list(self, ctx:OWScriptParser.Arg_listContext):
        pass

    # Exit a parse tree produced by OWScriptParser#arg_list.
    def exitArg_list(self, ctx:OWScriptParser.Arg_listContext):
        pass


    # Enter a parse tree produced by OWScriptParser#item.
    def enterItem(self, ctx:OWScriptParser.ItemContext):
        pass

    # Exit a parse tree produced by OWScriptParser#item.
    def exitItem(self, ctx:OWScriptParser.ItemContext):
        pass


    # Enter a parse tree produced by OWScriptParser#call.
    def enterCall(self, ctx:OWScriptParser.CallContext):
        pass

    # Exit a parse tree produced by OWScriptParser#call.
    def exitCall(self, ctx:OWScriptParser.CallContext):
        pass


    # Enter a parse tree produced by OWScriptParser#name.
    def enterName(self, ctx:OWScriptParser.NameContext):
        pass

    # Exit a parse tree produced by OWScriptParser#name.
    def exitName(self, ctx:OWScriptParser.NameContext):
        pass


    # Enter a parse tree produced by OWScriptParser#time.
    def enterTime(self, ctx:OWScriptParser.TimeContext):
        pass

    # Exit a parse tree produced by OWScriptParser#time.
    def exitTime(self, ctx:OWScriptParser.TimeContext):
        pass


    # Enter a parse tree produced by OWScriptParser#numeral.
    def enterNumeral(self, ctx:OWScriptParser.NumeralContext):
        pass

    # Exit a parse tree produced by OWScriptParser#numeral.
    def exitNumeral(self, ctx:OWScriptParser.NumeralContext):
        pass


    # Enter a parse tree produced by OWScriptParser#variable.
    def enterVariable(self, ctx:OWScriptParser.VariableContext):
        pass

    # Exit a parse tree produced by OWScriptParser#variable.
    def exitVariable(self, ctx:OWScriptParser.VariableContext):
        pass


    # Enter a parse tree produced by OWScriptParser#global_var.
    def enterGlobal_var(self, ctx:OWScriptParser.Global_varContext):
        pass

    # Exit a parse tree produced by OWScriptParser#global_var.
    def exitGlobal_var(self, ctx:OWScriptParser.Global_varContext):
        pass


    # Enter a parse tree produced by OWScriptParser#player_var.
    def enterPlayer_var(self, ctx:OWScriptParser.Player_varContext):
        pass

    # Exit a parse tree produced by OWScriptParser#player_var.
    def exitPlayer_var(self, ctx:OWScriptParser.Player_varContext):
        pass


    # Enter a parse tree produced by OWScriptParser#vector.
    def enterVector(self, ctx:OWScriptParser.VectorContext):
        pass

    # Exit a parse tree produced by OWScriptParser#vector.
    def exitVector(self, ctx:OWScriptParser.VectorContext):
        pass


    # Enter a parse tree produced by OWScriptParser#array.
    def enterArray(self, ctx:OWScriptParser.ArrayContext):
        pass

    # Exit a parse tree produced by OWScriptParser#array.
    def exitArray(self, ctx:OWScriptParser.ArrayContext):
        pass


