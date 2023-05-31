# Generated from QExpr.g by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .QExprParser import QExprParser
else:
    from QExprParser import QExprParser

# This class defines a complete listener for a parse tree produced by QExprParser.
class QExprListener(ParseTreeListener):

    # Enter a parse tree produced by QExprParser#snippet.
    def enterSnippet(self, ctx:QExprParser.SnippetContext):
        pass

    # Exit a parse tree produced by QExprParser#snippet.
    def exitSnippet(self, ctx:QExprParser.SnippetContext):
        pass


    # Enter a parse tree produced by QExprParser#stmts.
    def enterStmts(self, ctx:QExprParser.StmtsContext):
        pass

    # Exit a parse tree produced by QExprParser#stmts.
    def exitStmts(self, ctx:QExprParser.StmtsContext):
        pass


    # Enter a parse tree produced by QExprParser#stmt.
    def enterStmt(self, ctx:QExprParser.StmtContext):
        pass

    # Exit a parse tree produced by QExprParser#stmt.
    def exitStmt(self, ctx:QExprParser.StmtContext):
        pass


    # Enter a parse tree produced by QExprParser#ifStmt.
    def enterIfStmt(self, ctx:QExprParser.IfStmtContext):
        pass

    # Exit a parse tree produced by QExprParser#ifStmt.
    def exitIfStmt(self, ctx:QExprParser.IfStmtContext):
        pass


    # Enter a parse tree produced by QExprParser#elseStmt.
    def enterElseStmt(self, ctx:QExprParser.ElseStmtContext):
        pass

    # Exit a parse tree produced by QExprParser#elseStmt.
    def exitElseStmt(self, ctx:QExprParser.ElseStmtContext):
        pass


    # Enter a parse tree produced by QExprParser#repeatStmt.
    def enterRepeatStmt(self, ctx:QExprParser.RepeatStmtContext):
        pass

    # Exit a parse tree produced by QExprParser#repeatStmt.
    def exitRepeatStmt(self, ctx:QExprParser.RepeatStmtContext):
        pass


    # Enter a parse tree produced by QExprParser#forStmt.
    def enterForStmt(self, ctx:QExprParser.ForStmtContext):
        pass

    # Exit a parse tree produced by QExprParser#forStmt.
    def exitForStmt(self, ctx:QExprParser.ForStmtContext):
        pass


    # Enter a parse tree produced by QExprParser#definitionStmt.
    def enterDefinitionStmt(self, ctx:QExprParser.DefinitionStmtContext):
        pass

    # Exit a parse tree produced by QExprParser#definitionStmt.
    def exitDefinitionStmt(self, ctx:QExprParser.DefinitionStmtContext):
        pass


    # Enter a parse tree produced by QExprParser#returnStmt.
    def enterReturnStmt(self, ctx:QExprParser.ReturnStmtContext):
        pass

    # Exit a parse tree produced by QExprParser#returnStmt.
    def exitReturnStmt(self, ctx:QExprParser.ReturnStmtContext):
        pass


    # Enter a parse tree produced by QExprParser#breakLoop.
    def enterBreakLoop(self, ctx:QExprParser.BreakLoopContext):
        pass

    # Exit a parse tree produced by QExprParser#breakLoop.
    def exitBreakLoop(self, ctx:QExprParser.BreakLoopContext):
        pass


    # Enter a parse tree produced by QExprParser#continueLoop.
    def enterContinueLoop(self, ctx:QExprParser.ContinueLoopContext):
        pass

    # Exit a parse tree produced by QExprParser#continueLoop.
    def exitContinueLoop(self, ctx:QExprParser.ContinueLoopContext):
        pass


    # Enter a parse tree produced by QExprParser#halt.
    def enterHalt(self, ctx:QExprParser.HaltContext):
        pass

    # Exit a parse tree produced by QExprParser#halt.
    def exitHalt(self, ctx:QExprParser.HaltContext):
        pass


    # Enter a parse tree produced by QExprParser#assignment.
    def enterAssignment(self, ctx:QExprParser.AssignmentContext):
        pass

    # Exit a parse tree produced by QExprParser#assignment.
    def exitAssignment(self, ctx:QExprParser.AssignmentContext):
        pass


    # Enter a parse tree produced by QExprParser#expr.
    def enterExpr(self, ctx:QExprParser.ExprContext):
        pass

    # Exit a parse tree produced by QExprParser#expr.
    def exitExpr(self, ctx:QExprParser.ExprContext):
        pass


    # Enter a parse tree produced by QExprParser#arr.
    def enterArr(self, ctx:QExprParser.ArrContext):
        pass

    # Exit a parse tree produced by QExprParser#arr.
    def exitArr(self, ctx:QExprParser.ArrContext):
        pass


    # Enter a parse tree produced by QExprParser#obj.
    def enterObj(self, ctx:QExprParser.ObjContext):
        pass

    # Exit a parse tree produced by QExprParser#obj.
    def exitObj(self, ctx:QExprParser.ObjContext):
        pass


    # Enter a parse tree produced by QExprParser#func.
    def enterFunc(self, ctx:QExprParser.FuncContext):
        pass

    # Exit a parse tree produced by QExprParser#func.
    def exitFunc(self, ctx:QExprParser.FuncContext):
        pass


    # Enter a parse tree produced by QExprParser#sepExpr.
    def enterSepExpr(self, ctx:QExprParser.SepExprContext):
        pass

    # Exit a parse tree produced by QExprParser#sepExpr.
    def exitSepExpr(self, ctx:QExprParser.SepExprContext):
        pass


    # Enter a parse tree produced by QExprParser#idExpr.
    def enterIdExpr(self, ctx:QExprParser.IdExprContext):
        pass

    # Exit a parse tree produced by QExprParser#idExpr.
    def exitIdExpr(self, ctx:QExprParser.IdExprContext):
        pass


    # Enter a parse tree produced by QExprParser#value.
    def enterValue(self, ctx:QExprParser.ValueContext):
        pass

    # Exit a parse tree produced by QExprParser#value.
    def exitValue(self, ctx:QExprParser.ValueContext):
        pass


    # Enter a parse tree produced by QExprParser#joinOp.
    def enterJoinOp(self, ctx:QExprParser.JoinOpContext):
        pass

    # Exit a parse tree produced by QExprParser#joinOp.
    def exitJoinOp(self, ctx:QExprParser.JoinOpContext):
        pass


    # Enter a parse tree produced by QExprParser#andOp.
    def enterAndOp(self, ctx:QExprParser.AndOpContext):
        pass

    # Exit a parse tree produced by QExprParser#andOp.
    def exitAndOp(self, ctx:QExprParser.AndOpContext):
        pass


    # Enter a parse tree produced by QExprParser#orOp.
    def enterOrOp(self, ctx:QExprParser.OrOpContext):
        pass

    # Exit a parse tree produced by QExprParser#orOp.
    def exitOrOp(self, ctx:QExprParser.OrOpContext):
        pass


    # Enter a parse tree produced by QExprParser#multiplicativeOp.
    def enterMultiplicativeOp(self, ctx:QExprParser.MultiplicativeOpContext):
        pass

    # Exit a parse tree produced by QExprParser#multiplicativeOp.
    def exitMultiplicativeOp(self, ctx:QExprParser.MultiplicativeOpContext):
        pass


    # Enter a parse tree produced by QExprParser#additiveOp.
    def enterAdditiveOp(self, ctx:QExprParser.AdditiveOpContext):
        pass

    # Exit a parse tree produced by QExprParser#additiveOp.
    def exitAdditiveOp(self, ctx:QExprParser.AdditiveOpContext):
        pass


    # Enter a parse tree produced by QExprParser#relationalOp.
    def enterRelationalOp(self, ctx:QExprParser.RelationalOpContext):
        pass

    # Exit a parse tree produced by QExprParser#relationalOp.
    def exitRelationalOp(self, ctx:QExprParser.RelationalOpContext):
        pass


    # Enter a parse tree produced by QExprParser#uniOp.
    def enterUniOp(self, ctx:QExprParser.UniOpContext):
        pass

    # Exit a parse tree produced by QExprParser#uniOp.
    def exitUniOp(self, ctx:QExprParser.UniOpContext):
        pass


    # Enter a parse tree produced by QExprParser#binOp.
    def enterBinOp(self, ctx:QExprParser.BinOpContext):
        pass

    # Exit a parse tree produced by QExprParser#binOp.
    def exitBinOp(self, ctx:QExprParser.BinOpContext):
        pass


    # Enter a parse tree produced by QExprParser#notOp.
    def enterNotOp(self, ctx:QExprParser.NotOpContext):
        pass

    # Exit a parse tree produced by QExprParser#notOp.
    def exitNotOp(self, ctx:QExprParser.NotOpContext):
        pass


    # Enter a parse tree produced by QExprParser#asUniOp.
    def enterAsUniOp(self, ctx:QExprParser.AsUniOpContext):
        pass

    # Exit a parse tree produced by QExprParser#asUniOp.
    def exitAsUniOp(self, ctx:QExprParser.AsUniOpContext):
        pass



del QExprParser