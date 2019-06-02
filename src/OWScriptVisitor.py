# Generated from OWScript.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .OWScriptParser import OWScriptParser
else:
    from OWScriptParser import OWScriptParser

# This class defines a complete generic visitor for a parse tree produced by OWScriptParser.

class OWScriptVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by OWScriptParser#script.
    def visitScript(self, ctx:OWScriptParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#stmt.
    def visitStmt(self, ctx:OWScriptParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#funcdef.
    def visitFuncdef(self, ctx:OWScriptParser.FuncdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#funcbody.
    def visitFuncbody(self, ctx:OWScriptParser.FuncbodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#ruleset.
    def visitRuleset(self, ctx:OWScriptParser.RulesetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#ruledef.
    def visitRuledef(self, ctx:OWScriptParser.RuledefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#rulename.
    def visitRulename(self, ctx:OWScriptParser.RulenameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#RulebodyBlock.
    def visitRulebodyBlock(self, ctx:OWScriptParser.RulebodyBlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#RCall.
    def visitRCall(self, ctx:OWScriptParser.RCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#ruleblock.
    def visitRuleblock(self, ctx:OWScriptParser.RuleblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#block.
    def visitBlock(self, ctx:OWScriptParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#line.
    def visitLine(self, ctx:OWScriptParser.LineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#assign.
    def visitAssign(self, ctx:OWScriptParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#if_stmt.
    def visitIf_stmt(self, ctx:OWScriptParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#expr.
    def visitExpr(self, ctx:OWScriptParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#logic_or.
    def visitLogic_or(self, ctx:OWScriptParser.Logic_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#logic_and.
    def visitLogic_and(self, ctx:OWScriptParser.Logic_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#logic_not.
    def visitLogic_not(self, ctx:OWScriptParser.Logic_notContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#compare.
    def visitCompare(self, ctx:OWScriptParser.CompareContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#Pow.
    def visitPow(self, ctx:OWScriptParser.PowContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#Mul.
    def visitMul(self, ctx:OWScriptParser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#Div.
    def visitDiv(self, ctx:OWScriptParser.DivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#Add.
    def visitAdd(self, ctx:OWScriptParser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#Sub.
    def visitSub(self, ctx:OWScriptParser.SubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#Mod.
    def visitMod(self, ctx:OWScriptParser.ModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#ArithPrimary.
    def visitArithPrimary(self, ctx:OWScriptParser.ArithPrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#PItem.
    def visitPItem(self, ctx:OWScriptParser.PItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#PCall.
    def visitPCall(self, ctx:OWScriptParser.PCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#PrimaryNone.
    def visitPrimaryNone(self, ctx:OWScriptParser.PrimaryNoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#primary.
    def visitPrimary(self, ctx:OWScriptParser.PrimaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#action.
    def visitAction(self, ctx:OWScriptParser.ActionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#value.
    def visitValue(self, ctx:OWScriptParser.ValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#const.
    def visitConst(self, ctx:OWScriptParser.ConstContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#after_line.
    def visitAfter_line(self, ctx:OWScriptParser.After_lineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#param_list.
    def visitParam_list(self, ctx:OWScriptParser.Param_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#arg_list.
    def visitArg_list(self, ctx:OWScriptParser.Arg_listContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#item.
    def visitItem(self, ctx:OWScriptParser.ItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#call.
    def visitCall(self, ctx:OWScriptParser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#name.
    def visitName(self, ctx:OWScriptParser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#time.
    def visitTime(self, ctx:OWScriptParser.TimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#numeral.
    def visitNumeral(self, ctx:OWScriptParser.NumeralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#variable.
    def visitVariable(self, ctx:OWScriptParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#global_var.
    def visitGlobal_var(self, ctx:OWScriptParser.Global_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#player_var.
    def visitPlayer_var(self, ctx:OWScriptParser.Player_varContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#vector.
    def visitVector(self, ctx:OWScriptParser.VectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by OWScriptParser#array.
    def visitArray(self, ctx:OWScriptParser.ArrayContext):
        return self.visitChildren(ctx)



del OWScriptParser