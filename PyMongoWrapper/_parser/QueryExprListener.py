# Generated from QueryExpr.g by ANTLR 4.11.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .QueryExprParser import QueryExprParser
else:
    from QueryExprParser import QueryExprParser

# This class defines a complete listener for a parse tree produced by QueryExprParser.
class QueryExprListener(ParseTreeListener):

    # Enter a parse tree produced by QueryExprParser#snippet.
    def enterSnippet(self, ctx:QueryExprParser.SnippetContext):
        pass

    # Exit a parse tree produced by QueryExprParser#snippet.
    def exitSnippet(self, ctx:QueryExprParser.SnippetContext):
        pass


    # Enter a parse tree produced by QueryExprParser#stmts.
    def enterStmts(self, ctx:QueryExprParser.StmtsContext):
        pass

    # Exit a parse tree produced by QueryExprParser#stmts.
    def exitStmts(self, ctx:QueryExprParser.StmtsContext):
        pass


    # Enter a parse tree produced by QueryExprParser#stmt.
    def enterStmt(self, ctx:QueryExprParser.StmtContext):
        pass

    # Exit a parse tree produced by QueryExprParser#stmt.
    def exitStmt(self, ctx:QueryExprParser.StmtContext):
        pass


    # Enter a parse tree produced by QueryExprParser#ifStmt.
    def enterIfStmt(self, ctx:QueryExprParser.IfStmtContext):
        pass

    # Exit a parse tree produced by QueryExprParser#ifStmt.
    def exitIfStmt(self, ctx:QueryExprParser.IfStmtContext):
        pass


    # Enter a parse tree produced by QueryExprParser#else.
    def enterElse(self, ctx:QueryExprParser.ElseContext):
        pass

    # Exit a parse tree produced by QueryExprParser#else.
    def exitElse(self, ctx:QueryExprParser.ElseContext):
        pass


    # Enter a parse tree produced by QueryExprParser#repeatStmt.
    def enterRepeatStmt(self, ctx:QueryExprParser.RepeatStmtContext):
        pass

    # Exit a parse tree produced by QueryExprParser#repeatStmt.
    def exitRepeatStmt(self, ctx:QueryExprParser.RepeatStmtContext):
        pass


    # Enter a parse tree produced by QueryExprParser#forStmt.
    def enterForStmt(self, ctx:QueryExprParser.ForStmtContext):
        pass

    # Exit a parse tree produced by QueryExprParser#forStmt.
    def exitForStmt(self, ctx:QueryExprParser.ForStmtContext):
        pass


    # Enter a parse tree produced by QueryExprParser#break.
    def enterBreak(self, ctx:QueryExprParser.BreakContext):
        pass

    # Exit a parse tree produced by QueryExprParser#break.
    def exitBreak(self, ctx:QueryExprParser.BreakContext):
        pass


    # Enter a parse tree produced by QueryExprParser#continue.
    def enterContinue(self, ctx:QueryExprParser.ContinueContext):
        pass

    # Exit a parse tree produced by QueryExprParser#continue.
    def exitContinue(self, ctx:QueryExprParser.ContinueContext):
        pass


    # Enter a parse tree produced by QueryExprParser#halt.
    def enterHalt(self, ctx:QueryExprParser.HaltContext):
        pass

    # Exit a parse tree produced by QueryExprParser#halt.
    def exitHalt(self, ctx:QueryExprParser.HaltContext):
        pass


    # Enter a parse tree produced by QueryExprParser#assignment.
    def enterAssignment(self, ctx:QueryExprParser.AssignmentContext):
        pass

    # Exit a parse tree produced by QueryExprParser#assignment.
    def exitAssignment(self, ctx:QueryExprParser.AssignmentContext):
        pass


    # Enter a parse tree produced by QueryExprParser#expr.
    def enterExpr(self, ctx:QueryExprParser.ExprContext):
        pass

    # Exit a parse tree produced by QueryExprParser#expr.
    def exitExpr(self, ctx:QueryExprParser.ExprContext):
        pass


    # Enter a parse tree produced by QueryExprParser#arr.
    def enterArr(self, ctx:QueryExprParser.ArrContext):
        pass

    # Exit a parse tree produced by QueryExprParser#arr.
    def exitArr(self, ctx:QueryExprParser.ArrContext):
        pass


    # Enter a parse tree produced by QueryExprParser#obj.
    def enterObj(self, ctx:QueryExprParser.ObjContext):
        pass

    # Exit a parse tree produced by QueryExprParser#obj.
    def exitObj(self, ctx:QueryExprParser.ObjContext):
        pass


    # Enter a parse tree produced by QueryExprParser#func.
    def enterFunc(self, ctx:QueryExprParser.FuncContext):
        pass

    # Exit a parse tree produced by QueryExprParser#func.
    def exitFunc(self, ctx:QueryExprParser.FuncContext):
        pass


    # Enter a parse tree produced by QueryExprParser#sepExpr.
    def enterSepExpr(self, ctx:QueryExprParser.SepExprContext):
        pass

    # Exit a parse tree produced by QueryExprParser#sepExpr.
    def exitSepExpr(self, ctx:QueryExprParser.SepExprContext):
        pass


    # Enter a parse tree produced by QueryExprParser#idExpr.
    def enterIdExpr(self, ctx:QueryExprParser.IdExprContext):
        pass

    # Exit a parse tree produced by QueryExprParser#idExpr.
    def exitIdExpr(self, ctx:QueryExprParser.IdExprContext):
        pass


    # Enter a parse tree produced by QueryExprParser#value.
    def enterValue(self, ctx:QueryExprParser.ValueContext):
        pass

    # Exit a parse tree produced by QueryExprParser#value.
    def exitValue(self, ctx:QueryExprParser.ValueContext):
        pass


    # Enter a parse tree produced by QueryExprParser#joinOp.
    def enterJoinOp(self, ctx:QueryExprParser.JoinOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#joinOp.
    def exitJoinOp(self, ctx:QueryExprParser.JoinOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#andOp.
    def enterAndOp(self, ctx:QueryExprParser.AndOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#andOp.
    def exitAndOp(self, ctx:QueryExprParser.AndOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#orOp.
    def enterOrOp(self, ctx:QueryExprParser.OrOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#orOp.
    def exitOrOp(self, ctx:QueryExprParser.OrOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#multiplicativeOp.
    def enterMultiplicativeOp(self, ctx:QueryExprParser.MultiplicativeOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#multiplicativeOp.
    def exitMultiplicativeOp(self, ctx:QueryExprParser.MultiplicativeOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#additiveOp.
    def enterAdditiveOp(self, ctx:QueryExprParser.AdditiveOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#additiveOp.
    def exitAdditiveOp(self, ctx:QueryExprParser.AdditiveOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#relationalOp.
    def enterRelationalOp(self, ctx:QueryExprParser.RelationalOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#relationalOp.
    def exitRelationalOp(self, ctx:QueryExprParser.RelationalOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#uniOp.
    def enterUniOp(self, ctx:QueryExprParser.UniOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#uniOp.
    def exitUniOp(self, ctx:QueryExprParser.UniOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#binOp.
    def enterBinOp(self, ctx:QueryExprParser.BinOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#binOp.
    def exitBinOp(self, ctx:QueryExprParser.BinOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#notOp.
    def enterNotOp(self, ctx:QueryExprParser.NotOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#notOp.
    def exitNotOp(self, ctx:QueryExprParser.NotOpContext):
        pass


    # Enter a parse tree produced by QueryExprParser#asUniOp.
    def enterAsUniOp(self, ctx:QueryExprParser.AsUniOpContext):
        pass

    # Exit a parse tree produced by QueryExprParser#asUniOp.
    def exitAsUniOp(self, ctx:QueryExprParser.AsUniOpContext):
        pass



del QueryExprParser