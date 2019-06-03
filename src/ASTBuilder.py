from string import capwords
from AST import *
from OWScriptVisitor import OWScriptVisitor
class ASTBuilder(OWScriptVisitor):
    """Builds an AST from a parse tree generated by ANTLR."""
    def visitScript(self, ctx):
        script = Script()
        for stmt in ctx.stmt():
            script.statements.append(self.visit(stmt))
        return script

    def visitStmt(self, ctx):
        if len(ctx.children) == 2:
            return Call(func=ctx.NAME().getText(), args=self.visit(ctx.call()))
        return self.visitChildren(ctx)

    def visitRuleset(self, ctx):
        ruleset = Ruleset()
        for rule in ctx.ruledef():
            ruleset.rules.append(self.visit(rule))
        return ruleset

    def visitRuledef(self, ctx):
        rule = Rule()
        rule.rulename = self.visit(ctx.rulename())
        for rulebody in ctx.rulebody():
            rule.rulebody.append(self.visit(rulebody))
        return rule

    def visitRulename(self, ctx):
        return ctx.STRING()

    def visitRulebodyBlock(self, ctx):
        if ctx.RULEBLOCK():
            ruleblock = Ruleblock(type_=ctx.RULEBLOCK().getText())
            ruleblock.block = self.visit(ctx.ruleblock())
            return ruleblock
        return self.visit(ctx.RCall())

    def visitBlock(self, ctx):
        block = Block()
        for line in ctx.line():
            x = self.visit(line)
            if x:
                block.lines.append(x)
        return block

    def visitAdd(self, ctx):
        if len(ctx.children) > 1:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return BinaryOp(left=left, op='+', right=right)
        return self.visitChildren(ctx)

    def visitSub(self, ctx):
        if len(ctx.children) > 1:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return BinaryOp(left=left, op='-', right=right)
        return self.visitChildren(ctx)

    def visitMul(self, ctx):
        if len(ctx.children) > 1:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return BinaryOp(left=left, op='*', right=right)
        return self.visitChildren(ctx)

    def visitDiv(self, ctx):
        if len(ctx.children) > 1:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return BinaryOp(left=left, op='/', right=right)
        return self.visitChildren(ctx)

    def visitPow(self, ctx):
        if len(ctx.children) > 1:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return BinaryOp(left=left, op='^', right=right)
        return self.visitChildren(ctx)

    def visitMod(self, ctx):
        if len(ctx.children) > 1:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return BinaryOp(left=left, op='%', right=right)
        return self.visitChildren(ctx)


    def visitPrimary(self, ctx):
        primary = self.visit(ctx.children[0])
        if ctx.expr():
            primary = self.visit(ctx.expr())
        if ctx.trailer():
            for trailer in ctx.trailer():
                t = self.visit(trailer)
                if type(t) == Item:
                    primary = ArrayItem(array=primary, item=t)
                elif type(t) == Call:
                    print('oof a call')
        return primary

    def visitLogic_or(self, ctx):
        if len(ctx.children) == 3:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return Or(left=left, op='or', right=right)
        return self.visitChildren(ctx)

    def visitLogic_and(self, ctx):
        if len(ctx.children) == 3:
            left = self.visit(ctx.children[0])
            right = self.visit(ctx.children[2])
            return And(left=left, op='and', right=right)
        return self.visitChildren(ctx)

    def visitLogic_not(self, ctx):
        if len(ctx.children) == 2:
            return Not(op='not', right=self.visit(ctx.children[1]))
        return self.visit(ctx.compare())

    def visitFuncdef(self, ctx):
        funcname = ctx.NAME().getText()
        funcparams = self.visit(ctx.param_list())
        funcbody = self.visit(ctx.funcbody())
        return Function(name=funcname, params=funcparams, body=funcbody)

    def visitFuncbody(self, ctx):
        return self.visit(ctx.ruleset() or ctx.ruledef() or ctx.rulebody() or ctx.block())

    def visitAssign(self, ctx):
        assign = Assign()
        expr = ctx.expr()
        assign.left = self.visit(expr[0])
        assign.op = ctx.ASSIGN().getText()
        assign.right = self.visit(expr[1])
        return assign

    def visitCompare(self, ctx):
        if len(ctx.children) >= 3:
            compare = Compare()
            compare.left = self.visit(ctx.children[0])
            compare.op = ' '.join(x.getText() for x in ctx.children[1:-1])
            compare.right = self.visit(ctx.children[-1])
            return compare
        return self.visit(ctx.arith()[0])

    def visitIf_stmt(self, ctx):
        expr = ctx.expr()
        block = ctx.block()
        if_cond = self.visit(expr[0])
        if_block = Ruleblock(block=self.visit(block[0]))
        elif_conds = []
        elif_blocks = []
        else_block = None
        if len(expr) > 1:
            elif_conds = [self.visit(x) for x in expr[1:]]
            if len(block) > len(expr):
                elif_blocks = [Ruleblock(block=self.visit(x)) for x in block[1:-1]]
                else_block = Ruleblock(block=self.visit(block[-1]))
            else:
                elif_blocks = [Ruleblock(block=self.visit(x)) for x in block[1:]]
        elif len(block) > len(expr):
            else_block = Ruleblock(block=self.visit(block[-1]))
        return If(cond=if_cond, block=if_block, elif_conds=elif_conds, elif_blocks=elif_blocks, else_block=else_block)

    def visitWhile_stmt(self, ctx):
        cond = self.visit(ctx.expr())
        block = Ruleblock(block=self.visit(ctx.block()))
        return While(cond=cond, block=block)

    def visitLine(self, ctx):
        if len(ctx.children) == 2:
            return self.visit(ctx.children[-1])
        if len(ctx.children) > 2:
            return Compare(left=self.visit(ctx.children[0]), op=ctx.comp_op.text, right=self.visit(ctx.children[-1]))
        return self.visit(ctx.children[0])

    def visitValue(self, ctx):
        value = Value(value=capwords(ctx.VALUE().getText()))
        for child in ctx.children:
            x = self.visit(child)
            if x:
                if type(x) == Block and not x.lines:
                    continue
                elif type(x) == Attr:
                    value = Attribute(value=x.name.value.upper(), arg=value)
                    continue
                value.args.append(x)
        return value

    def visitAction(self, ctx):
        action = Action(value=capwords(ctx.ACTION().getText()))
        for child in ctx.children:
            x = self.visit(child)
            if x:
                if type(x) == Block and not x.lines:
                    continue
                action.args.append(x)
        return action

    def visitAfter_line(self, ctx):
        if ctx.arg_list():
            return Block(lines=self.visit(ctx.arg_list()))
        if ctx.primary():
            block = Block()
            for primary in ctx.primary():
                x = self.visit(primary)
                if x:
                    block.lines.append(x)
            return block
        else:
            print('nop')

    def visitArg_list(self, ctx):
        arg_list = []
        for child in ctx.children:
            x = self.visit(child)
            if x:
                arg_list.append(x)
        return arg_list

    def visitParam_list(self, ctx):
        return [x.getText() for x in ctx.NAME()]

    def visitArray(self, ctx):
        array = Array()
        if len(ctx.children) == 3:
            array.elements = self.visit(ctx.children[1])
        return array

    def visitName(self, ctx):
        text = ctx.NAME().getText()
        if text.startswith('Wait'):
            action = Action(value='Wait')
            action.args.append(Time(value=text.lstrip('Wait ')))
            return action
        return Name(value=ctx.NAME().getText())

    def visitConst(self, ctx):
        if ctx.attribute():
            print('attr!')
        return Name(value=ctx.CONST().getText())

    def visitNumeral(self, ctx):
        return Numeral(value=ctx.num_const.text)

    def visitTime(self, ctx):
        return Time(value=ctx.getText())

    def visitVector(self, ctx):
        vector = Value(value='Vector')
        for child in ctx.children:
            x = self.visit(child)
            if x:
                if type(x) == Block and not x.lines:
                    continue
                vector.args.append(x)
        return vector

    def visitGlobal_var(self, ctx):
        gvar = GlobalVar(name=ctx.varname.text)
        return gvar

    def visitPlayer_var(self, ctx):
        pvar = PlayerVar(name=ctx.varname.text)
        if len(ctx.children) == 3:
            pvar.player = self.visit(ctx.children[-1])
        return pvar

    def visitRCall(self, ctx):
        func = self.visit(ctx.children[0])
        args = self.visit(ctx.children[1])
        return Call(func=func.name, args=args)

    def visitCall(self, ctx):
        if ctx.arg_list():
            return self.visit(ctx.arg_list())
        return None

    def visitItem(self, ctx):
        return Item(index=Numeral(value=ctx.INTEGER().getText()))

    def visitAttribute(self, ctx):
        return Attr(name=self.visit(ctx.name()))

    def run(self, parse_tree):
        return self.visit(parse_tree)