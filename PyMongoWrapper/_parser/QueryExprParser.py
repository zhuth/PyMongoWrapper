# Generated from D:\PyMongoWrapper\QueryExpr.g by ANTLR 4.11.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,47,236,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        1,0,4,0,56,8,0,11,0,12,0,57,1,0,1,0,1,0,3,0,63,8,0,1,1,1,1,1,1,5,
        1,68,8,1,10,1,12,1,71,9,1,1,1,3,1,74,8,1,1,2,1,2,1,2,1,2,1,2,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,3,2,95,8,2,1,
        3,1,3,1,3,1,3,3,3,101,8,3,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,
        6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,1,10,1,10,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,137,8,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,5,11,163,
        8,11,10,11,12,11,166,9,11,1,12,1,12,1,12,1,12,1,12,1,12,3,12,174,
        8,12,1,13,1,13,3,13,178,8,13,1,13,1,13,1,14,1,14,1,14,3,14,185,8,
        14,1,14,1,14,1,15,1,15,1,15,5,15,192,8,15,10,15,12,15,195,9,15,1,
        16,1,16,1,16,1,16,3,16,201,8,16,1,16,1,16,1,16,5,16,206,8,16,10,
        16,12,16,209,9,16,1,17,1,17,1,18,1,18,1,19,1,19,1,20,1,20,1,21,1,
        21,1,22,1,22,1,23,1,23,1,24,1,24,1,25,1,25,1,25,3,25,230,8,25,1,
        26,1,26,3,26,234,8,26,1,26,0,2,22,32,27,0,2,4,6,8,10,12,14,16,18,
        20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,0,5,2,0,8,13,
        15,16,1,0,30,33,2,0,27,27,29,29,1,0,36,41,3,0,27,27,29,29,42,43,
        244,0,62,1,0,0,0,2,73,1,0,0,0,4,94,1,0,0,0,6,96,1,0,0,0,8,102,1,
        0,0,0,10,105,1,0,0,0,12,109,1,0,0,0,14,113,1,0,0,0,16,115,1,0,0,
        0,18,117,1,0,0,0,20,119,1,0,0,0,22,136,1,0,0,0,24,173,1,0,0,0,26,
        175,1,0,0,0,28,181,1,0,0,0,30,188,1,0,0,0,32,200,1,0,0,0,34,210,
        1,0,0,0,36,212,1,0,0,0,38,214,1,0,0,0,40,216,1,0,0,0,42,218,1,0,
        0,0,44,220,1,0,0,0,46,222,1,0,0,0,48,224,1,0,0,0,50,229,1,0,0,0,
        52,233,1,0,0,0,54,56,3,4,2,0,55,54,1,0,0,0,56,57,1,0,0,0,57,55,1,
        0,0,0,57,58,1,0,0,0,58,63,1,0,0,0,59,63,3,2,1,0,60,63,3,22,11,0,
        61,63,3,30,15,0,62,55,1,0,0,0,62,59,1,0,0,0,62,60,1,0,0,0,62,61,
        1,0,0,0,63,1,1,0,0,0,64,74,3,4,2,0,65,69,5,20,0,0,66,68,3,4,2,0,
        67,66,1,0,0,0,68,71,1,0,0,0,69,67,1,0,0,0,69,70,1,0,0,0,70,72,1,
        0,0,0,71,69,1,0,0,0,72,74,5,21,0,0,73,64,1,0,0,0,73,65,1,0,0,0,74,
        3,1,0,0,0,75,76,3,22,11,0,76,77,5,19,0,0,77,95,1,0,0,0,78,79,3,20,
        10,0,79,80,5,19,0,0,80,95,1,0,0,0,81,95,3,6,3,0,82,95,3,10,5,0,83,
        95,3,12,6,0,84,85,3,14,7,0,85,86,5,19,0,0,86,95,1,0,0,0,87,88,3,
        16,8,0,88,89,5,19,0,0,89,95,1,0,0,0,90,91,3,18,9,0,91,92,5,19,0,
        0,92,95,1,0,0,0,93,95,5,19,0,0,94,75,1,0,0,0,94,78,1,0,0,0,94,81,
        1,0,0,0,94,82,1,0,0,0,94,83,1,0,0,0,94,84,1,0,0,0,94,87,1,0,0,0,
        94,90,1,0,0,0,94,93,1,0,0,0,95,5,1,0,0,0,96,97,5,1,0,0,97,98,3,22,
        11,0,98,100,3,2,1,0,99,101,3,8,4,0,100,99,1,0,0,0,100,101,1,0,0,
        0,101,7,1,0,0,0,102,103,5,2,0,0,103,104,3,2,1,0,104,9,1,0,0,0,105,
        106,5,3,0,0,106,107,3,22,11,0,107,108,3,2,1,0,108,11,1,0,0,0,109,
        110,5,4,0,0,110,111,3,20,10,0,111,112,3,2,1,0,112,13,1,0,0,0,113,
        114,5,5,0,0,114,15,1,0,0,0,115,116,5,6,0,0,116,17,1,0,0,0,117,118,
        5,7,0,0,118,19,1,0,0,0,119,120,5,17,0,0,120,121,5,18,0,0,121,122,
        3,22,11,0,122,21,1,0,0,0,123,124,6,11,-1,0,124,125,5,22,0,0,125,
        126,3,22,11,0,126,127,5,23,0,0,127,137,1,0,0,0,128,137,3,26,13,0,
        129,137,3,24,12,0,130,137,3,28,14,0,131,132,3,52,26,0,132,133,3,
        22,11,9,133,137,1,0,0,0,134,137,3,34,17,0,135,137,3,32,16,0,136,
        123,1,0,0,0,136,128,1,0,0,0,136,129,1,0,0,0,136,130,1,0,0,0,136,
        131,1,0,0,0,136,134,1,0,0,0,136,135,1,0,0,0,137,164,1,0,0,0,138,
        139,10,8,0,0,139,140,3,42,21,0,140,141,3,22,11,9,141,163,1,0,0,0,
        142,143,10,7,0,0,143,144,3,44,22,0,144,145,3,22,11,8,145,163,1,0,
        0,0,146,147,10,6,0,0,147,148,3,46,23,0,148,149,3,22,11,7,149,163,
        1,0,0,0,150,151,10,5,0,0,151,152,3,38,19,0,152,153,3,22,11,6,153,
        163,1,0,0,0,154,155,10,4,0,0,155,156,3,40,20,0,156,157,3,22,11,5,
        157,163,1,0,0,0,158,159,10,3,0,0,159,160,3,36,18,0,160,161,3,22,
        11,4,161,163,1,0,0,0,162,138,1,0,0,0,162,142,1,0,0,0,162,146,1,0,
        0,0,162,150,1,0,0,0,162,154,1,0,0,0,162,158,1,0,0,0,163,166,1,0,
        0,0,164,162,1,0,0,0,164,165,1,0,0,0,165,23,1,0,0,0,166,164,1,0,0,
        0,167,168,5,24,0,0,168,169,3,30,15,0,169,170,5,25,0,0,170,174,1,
        0,0,0,171,172,5,24,0,0,172,174,5,25,0,0,173,167,1,0,0,0,173,171,
        1,0,0,0,174,25,1,0,0,0,175,177,5,22,0,0,176,178,3,30,15,0,177,176,
        1,0,0,0,177,178,1,0,0,0,178,179,1,0,0,0,179,180,5,23,0,0,180,27,
        1,0,0,0,181,182,5,17,0,0,182,184,5,22,0,0,183,185,3,30,15,0,184,
        183,1,0,0,0,184,185,1,0,0,0,185,186,1,0,0,0,186,187,5,23,0,0,187,
        29,1,0,0,0,188,193,3,22,11,0,189,190,5,26,0,0,190,192,3,22,11,0,
        191,189,1,0,0,0,192,195,1,0,0,0,193,191,1,0,0,0,193,194,1,0,0,0,
        194,31,1,0,0,0,195,193,1,0,0,0,196,197,6,16,-1,0,197,201,5,17,0,
        0,198,199,5,44,0,0,199,201,3,32,16,2,200,196,1,0,0,0,200,198,1,0,
        0,0,201,207,1,0,0,0,202,203,10,1,0,0,203,204,5,33,0,0,204,206,5,
        17,0,0,205,202,1,0,0,0,206,209,1,0,0,0,207,205,1,0,0,0,207,208,1,
        0,0,0,208,33,1,0,0,0,209,207,1,0,0,0,210,211,7,0,0,0,211,35,1,0,
        0,0,212,213,5,28,0,0,213,37,1,0,0,0,214,215,5,34,0,0,215,39,1,0,
        0,0,216,217,5,35,0,0,217,41,1,0,0,0,218,219,7,1,0,0,219,43,1,0,0,
        0,220,221,7,2,0,0,221,45,1,0,0,0,222,223,7,3,0,0,223,47,1,0,0,0,
        224,225,7,4,0,0,225,49,1,0,0,0,226,230,3,42,21,0,227,230,3,44,22,
        0,228,230,3,46,23,0,229,226,1,0,0,0,229,227,1,0,0,0,229,228,1,0,
        0,0,230,51,1,0,0,0,231,234,3,48,24,0,232,234,3,50,25,0,233,231,1,
        0,0,0,233,232,1,0,0,0,234,53,1,0,0,0,17,57,62,69,73,94,100,136,162,
        164,173,177,184,193,200,207,229,233
    ]

class QueryExprParser ( Parser ):

    grammarFileName = "QueryExpr.g"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'else'", "'repeat'", "'for'", 
                     "'break'", "'continue'", "'halt'", "'true'", "'false'", 
                     "'null'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "':'", "';'", 
                     "'{'", "'}'", "'('", "')'", "'['", "']'", "','", "'+'", 
                     "'=>'", "'-'", "'*'", "'/'", "'%'", "'.'", "'&'", "'|'", 
                     "'>'", "'<'", "'>='", "'<='", "'!='", "'='", "'%%'", 
                     "'~'", "'$'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "SHORTCUT", 
                      "STRING", "NUMBER", "TIME", "TIME_INTERVAL", "DATETIME", 
                      "ID", "Colon", "Semicolon", "LBrace", "RBrace", "LPar", 
                      "RPar", "LBrack", "RBrack", "Comma", "Plus", "Join", 
                      "Minus", "Star", "Div", "Mod", "Dot", "And", "Or", 
                      "Gt", "Lt", "Gte", "Lte", "Ne", "Eq", "Search", "Tilde", 
                      "Dollar", "WS", "COMMENT", "LINE_COMMENT" ]

    RULE_snippet = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_ifStmt = 3
    RULE_else = 4
    RULE_repeatStmt = 5
    RULE_forStmt = 6
    RULE_break = 7
    RULE_continue = 8
    RULE_halt = 9
    RULE_assignment = 10
    RULE_expr = 11
    RULE_arr = 12
    RULE_obj = 13
    RULE_func = 14
    RULE_sepExpr = 15
    RULE_idExpr = 16
    RULE_value = 17
    RULE_joinOp = 18
    RULE_andOp = 19
    RULE_orOp = 20
    RULE_multiplicativeOp = 21
    RULE_additiveOp = 22
    RULE_relationalOp = 23
    RULE_uniOp = 24
    RULE_binOp = 25
    RULE_asUniOp = 26

    ruleNames =  [ "snippet", "stmts", "stmt", "ifStmt", "else", "repeatStmt", 
                   "forStmt", "break", "continue", "halt", "assignment", 
                   "expr", "arr", "obj", "func", "sepExpr", "idExpr", "value", 
                   "joinOp", "andOp", "orOp", "multiplicativeOp", "additiveOp", 
                   "relationalOp", "uniOp", "binOp", "asUniOp" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    T__6=7
    T__7=8
    T__8=9
    T__9=10
    SHORTCUT=11
    STRING=12
    NUMBER=13
    TIME=14
    TIME_INTERVAL=15
    DATETIME=16
    ID=17
    Colon=18
    Semicolon=19
    LBrace=20
    RBrace=21
    LPar=22
    RPar=23
    LBrack=24
    RBrack=25
    Comma=26
    Plus=27
    Join=28
    Minus=29
    Star=30
    Div=31
    Mod=32
    Dot=33
    And=34
    Or=35
    Gt=36
    Lt=37
    Gte=38
    Lte=39
    Ne=40
    Eq=41
    Search=42
    Tilde=43
    Dollar=44
    WS=45
    COMMENT=46
    LINE_COMMENT=47

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.11.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SnippetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QueryExprParser.StmtContext)
            else:
                return self.getTypedRuleContext(QueryExprParser.StmtContext,i)


        def stmts(self):
            return self.getTypedRuleContext(QueryExprParser.StmtsContext,0)


        def expr(self):
            return self.getTypedRuleContext(QueryExprParser.ExprContext,0)


        def sepExpr(self):
            return self.getTypedRuleContext(QueryExprParser.SepExprContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_snippet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSnippet" ):
                listener.enterSnippet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSnippet" ):
                listener.exitSnippet(self)




    def snippet(self):

        localctx = QueryExprParser.SnippetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_snippet)
        self._la = 0 # Token type
        try:
            self.state = 62
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 55 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 54
                    self.stmt()
                    self.state = 57 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (((_la) & ~0x3f) == 0 and ((1 << _la) & 35132451569658) != 0):
                        break

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.stmts()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 60
                self.expr(0)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 61
                self.sepExpr()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QueryExprParser.StmtContext)
            else:
                return self.getTypedRuleContext(QueryExprParser.StmtContext,i)


        def LBrace(self):
            return self.getToken(QueryExprParser.LBrace, 0)

        def RBrace(self):
            return self.getToken(QueryExprParser.RBrace, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_stmts

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmts" ):
                listener.enterStmts(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmts" ):
                listener.exitStmts(self)




    def stmts(self):

        localctx = QueryExprParser.StmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmts)
        self._la = 0 # Token type
        try:
            self.state = 73
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 19, 22, 24, 27, 29, 30, 31, 32, 33, 36, 37, 38, 39, 40, 41, 42, 43, 44]:
                self.enterOuterAlt(localctx, 1)
                self.state = 64
                self.stmt()
                pass
            elif token in [20]:
                self.enterOuterAlt(localctx, 2)
                self.state = 65
                self.match(QueryExprParser.LBrace)
                self.state = 69
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while ((_la) & ~0x3f) == 0 and ((1 << _la) & 35132451569658) != 0:
                    self.state = 66
                    self.stmt()
                    self.state = 71
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 72
                self.match(QueryExprParser.RBrace)
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


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self):
            return self.getTypedRuleContext(QueryExprParser.ExprContext,0)


        def Semicolon(self):
            return self.getToken(QueryExprParser.Semicolon, 0)

        def assignment(self):
            return self.getTypedRuleContext(QueryExprParser.AssignmentContext,0)


        def ifStmt(self):
            return self.getTypedRuleContext(QueryExprParser.IfStmtContext,0)


        def repeatStmt(self):
            return self.getTypedRuleContext(QueryExprParser.RepeatStmtContext,0)


        def forStmt(self):
            return self.getTypedRuleContext(QueryExprParser.ForStmtContext,0)


        def break_(self):
            return self.getTypedRuleContext(QueryExprParser.BreakContext,0)


        def continue_(self):
            return self.getTypedRuleContext(QueryExprParser.ContinueContext,0)


        def halt(self):
            return self.getTypedRuleContext(QueryExprParser.HaltContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)




    def stmt(self):

        localctx = QueryExprParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        try:
            self.state = 94
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 75
                self.expr(0)
                self.state = 76
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 78
                self.assignment()
                self.state = 79
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 81
                self.ifStmt()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 82
                self.repeatStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 83
                self.forStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 84
                self.break_()
                self.state = 85
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 87
                self.continue_()
                self.state = 88
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 90
                self.halt()
                self.state = 91
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 93
                self.match(QueryExprParser.Semicolon)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IfStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.cond = None # ExprContext
            self.if_true = None # StmtsContext
            self.if_false = None # ElseContext

        def expr(self):
            return self.getTypedRuleContext(QueryExprParser.ExprContext,0)


        def stmts(self):
            return self.getTypedRuleContext(QueryExprParser.StmtsContext,0)


        def else_(self):
            return self.getTypedRuleContext(QueryExprParser.ElseContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)




    def ifStmt(self):

        localctx = QueryExprParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_ifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 96
            self.match(QueryExprParser.T__0)
            self.state = 97
            localctx.cond = self.expr(0)
            self.state = 98
            localctx.if_true = self.stmts()
            self.state = 100
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 99
                localctx.if_false = self.else_()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.pipeline = None # StmtsContext

        def stmts(self):
            return self.getTypedRuleContext(QueryExprParser.StmtsContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_else

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElse" ):
                listener.enterElse(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElse" ):
                listener.exitElse(self)




    def else_(self):

        localctx = QueryExprParser.ElseContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_else)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.match(QueryExprParser.T__1)
            self.state = 103
            localctx.pipeline = self.stmts()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RepeatStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.cond = None # ExprContext
            self.pipeline = None # StmtsContext

        def expr(self):
            return self.getTypedRuleContext(QueryExprParser.ExprContext,0)


        def stmts(self):
            return self.getTypedRuleContext(QueryExprParser.StmtsContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_repeatStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRepeatStmt" ):
                listener.enterRepeatStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRepeatStmt" ):
                listener.exitRepeatStmt(self)




    def repeatStmt(self):

        localctx = QueryExprParser.RepeatStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_repeatStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 105
            self.match(QueryExprParser.T__2)
            self.state = 106
            localctx.cond = self.expr(0)
            self.state = 107
            localctx.pipeline = self.stmts()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ForStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.assign = None # AssignmentContext
            self.pipeline = None # StmtsContext

        def assignment(self):
            return self.getTypedRuleContext(QueryExprParser.AssignmentContext,0)


        def stmts(self):
            return self.getTypedRuleContext(QueryExprParser.StmtsContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_forStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStmt" ):
                listener.enterForStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStmt" ):
                listener.exitForStmt(self)




    def forStmt(self):

        localctx = QueryExprParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_forStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 109
            self.match(QueryExprParser.T__3)
            self.state = 110
            localctx.assign = self.assignment()
            self.state = 111
            localctx.pipeline = self.stmts()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QueryExprParser.RULE_break

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreak" ):
                listener.enterBreak(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreak" ):
                listener.exitBreak(self)




    def break_(self):

        localctx = QueryExprParser.BreakContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_break)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 113
            self.match(QueryExprParser.T__4)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QueryExprParser.RULE_continue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinue" ):
                listener.enterContinue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinue" ):
                listener.exitContinue(self)




    def continue_(self):

        localctx = QueryExprParser.ContinueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_continue)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 115
            self.match(QueryExprParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class HaltContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QueryExprParser.RULE_halt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHalt" ):
                listener.enterHalt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHalt" ):
                listener.exitHalt(self)




    def halt(self):

        localctx = QueryExprParser.HaltContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_halt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 117
            self.match(QueryExprParser.T__6)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.target = None # Token
            self.val = None # ExprContext

        def Colon(self):
            return self.getToken(QueryExprParser.Colon, 0)

        def ID(self):
            return self.getToken(QueryExprParser.ID, 0)

        def expr(self):
            return self.getTypedRuleContext(QueryExprParser.ExprContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)




    def assignment(self):

        localctx = QueryExprParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 119
            localctx.target = self.match(QueryExprParser.ID)
            self.state = 120
            self.match(QueryExprParser.Colon)
            self.state = 121
            localctx.val = self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.left = None # ExprContext
            self.parred = None # ExprContext
            self.uniop = None # AsUniOpContext
            self.right = None # ExprContext
            self.op1 = None # MultiplicativeOpContext
            self.op2 = None # AdditiveOpContext
            self.op3 = None # RelationalOpContext
            self.op4 = None # AndOpContext
            self.op5 = None # OrOpContext
            self.op6 = None # JoinOpContext

        def LPar(self):
            return self.getToken(QueryExprParser.LPar, 0)

        def RPar(self):
            return self.getToken(QueryExprParser.RPar, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QueryExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(QueryExprParser.ExprContext,i)


        def obj(self):
            return self.getTypedRuleContext(QueryExprParser.ObjContext,0)


        def arr(self):
            return self.getTypedRuleContext(QueryExprParser.ArrContext,0)


        def func(self):
            return self.getTypedRuleContext(QueryExprParser.FuncContext,0)


        def asUniOp(self):
            return self.getTypedRuleContext(QueryExprParser.AsUniOpContext,0)


        def value(self):
            return self.getTypedRuleContext(QueryExprParser.ValueContext,0)


        def idExpr(self):
            return self.getTypedRuleContext(QueryExprParser.IdExprContext,0)


        def multiplicativeOp(self):
            return self.getTypedRuleContext(QueryExprParser.MultiplicativeOpContext,0)


        def additiveOp(self):
            return self.getTypedRuleContext(QueryExprParser.AdditiveOpContext,0)


        def relationalOp(self):
            return self.getTypedRuleContext(QueryExprParser.RelationalOpContext,0)


        def andOp(self):
            return self.getTypedRuleContext(QueryExprParser.AndOpContext,0)


        def orOp(self):
            return self.getTypedRuleContext(QueryExprParser.OrOpContext,0)


        def joinOp(self):
            return self.getTypedRuleContext(QueryExprParser.JoinOpContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = QueryExprParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 22
        self.enterRecursionRule(localctx, 22, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 124
                self.match(QueryExprParser.LPar)
                self.state = 125
                localctx.parred = self.expr(0)
                self.state = 126
                self.match(QueryExprParser.RPar)
                pass

            elif la_ == 2:
                self.state = 128
                self.obj()
                pass

            elif la_ == 3:
                self.state = 129
                self.arr()
                pass

            elif la_ == 4:
                self.state = 130
                self.func()
                pass

            elif la_ == 5:
                self.state = 131
                localctx.uniop = self.asUniOp()
                self.state = 132
                localctx.right = self.expr(9)
                pass

            elif la_ == 6:
                self.state = 134
                self.value()
                pass

            elif la_ == 7:
                self.state = 135
                self.idExpr(0)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 164
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,8,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 162
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
                    if la_ == 1:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 138
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 139
                        localctx.op1 = self.multiplicativeOp()
                        self.state = 140
                        localctx.right = self.expr(9)
                        pass

                    elif la_ == 2:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 142
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 143
                        localctx.op2 = self.additiveOp()
                        self.state = 144
                        localctx.right = self.expr(8)
                        pass

                    elif la_ == 3:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 146
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 147
                        localctx.op3 = self.relationalOp()
                        self.state = 148
                        localctx.right = self.expr(7)
                        pass

                    elif la_ == 4:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 150
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 151
                        localctx.op4 = self.andOp()
                        self.state = 152
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 5:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 154
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 155
                        localctx.op5 = self.orOp()
                        self.state = 156
                        localctx.right = self.expr(5)
                        pass

                    elif la_ == 6:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 158
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 159
                        localctx.op6 = self.joinOp()
                        self.state = 160
                        localctx.right = self.expr(4)
                        pass

             
                self.state = 166
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,8,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ArrContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBrack(self):
            return self.getToken(QueryExprParser.LBrack, 0)

        def sepExpr(self):
            return self.getTypedRuleContext(QueryExprParser.SepExprContext,0)


        def RBrack(self):
            return self.getToken(QueryExprParser.RBrack, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_arr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArr" ):
                listener.enterArr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArr" ):
                listener.exitArr(self)




    def arr(self):

        localctx = QueryExprParser.ArrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_arr)
        try:
            self.state = 173
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 167
                self.match(QueryExprParser.LBrack)
                self.state = 168
                self.sepExpr()
                self.state = 169
                self.match(QueryExprParser.RBrack)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 171
                self.match(QueryExprParser.LBrack)
                self.state = 172
                self.match(QueryExprParser.RBrack)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.val = None # SepExprContext

        def LPar(self):
            return self.getToken(QueryExprParser.LPar, 0)

        def RPar(self):
            return self.getToken(QueryExprParser.RPar, 0)

        def sepExpr(self):
            return self.getTypedRuleContext(QueryExprParser.SepExprContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_obj

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObj" ):
                listener.enterObj(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObj" ):
                listener.exitObj(self)




    def obj(self):

        localctx = QueryExprParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 175
            self.match(QueryExprParser.LPar)
            self.state = 177
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 35132451045120) != 0:
                self.state = 176
                localctx.val = self.sepExpr()


            self.state = 179
            self.match(QueryExprParser.RPar)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.func_name = None # Token

        def LPar(self):
            return self.getToken(QueryExprParser.LPar, 0)

        def RPar(self):
            return self.getToken(QueryExprParser.RPar, 0)

        def ID(self):
            return self.getToken(QueryExprParser.ID, 0)

        def sepExpr(self):
            return self.getTypedRuleContext(QueryExprParser.SepExprContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_func

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunc" ):
                listener.enterFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunc" ):
                listener.exitFunc(self)




    def func(self):

        localctx = QueryExprParser.FuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_func)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 181
            localctx.func_name = self.match(QueryExprParser.ID)
            self.state = 182
            self.match(QueryExprParser.LPar)
            self.state = 184
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 35132451045120) != 0:
                self.state = 183
                self.sepExpr()


            self.state = 186
            self.match(QueryExprParser.RPar)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SepExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QueryExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(QueryExprParser.ExprContext,i)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(QueryExprParser.Comma)
            else:
                return self.getToken(QueryExprParser.Comma, i)

        def getRuleIndex(self):
            return QueryExprParser.RULE_sepExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSepExpr" ):
                listener.enterSepExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSepExpr" ):
                listener.exitSepExpr(self)




    def sepExpr(self):

        localctx = QueryExprParser.SepExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_sepExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.expr(0)
            self.state = 193
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==26:
                self.state = 189
                self.match(QueryExprParser.Comma)
                self.state = 190
                self.expr(0)
                self.state = 195
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class IdExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(QueryExprParser.ID, 0)

        def Dollar(self):
            return self.getToken(QueryExprParser.Dollar, 0)

        def idExpr(self):
            return self.getTypedRuleContext(QueryExprParser.IdExprContext,0)


        def Dot(self):
            return self.getToken(QueryExprParser.Dot, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_idExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdExpr" ):
                listener.enterIdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdExpr" ):
                listener.exitIdExpr(self)



    def idExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = QueryExprParser.IdExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 32
        self.enterRecursionRule(localctx, 32, self.RULE_idExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 200
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [17]:
                self.state = 197
                self.match(QueryExprParser.ID)
                pass
            elif token in [44]:
                self.state = 198
                self.match(QueryExprParser.Dollar)
                self.state = 199
                self.idExpr(2)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 207
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,14,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = QueryExprParser.IdExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_idExpr)
                    self.state = 202
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 203
                    self.match(QueryExprParser.Dot)
                    self.state = 204
                    self.match(QueryExprParser.ID) 
                self.state = 209
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,14,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(QueryExprParser.STRING, 0)

        def DATETIME(self):
            return self.getToken(QueryExprParser.DATETIME, 0)

        def TIME_INTERVAL(self):
            return self.getToken(QueryExprParser.TIME_INTERVAL, 0)

        def NUMBER(self):
            return self.getToken(QueryExprParser.NUMBER, 0)

        def SHORTCUT(self):
            return self.getToken(QueryExprParser.SHORTCUT, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)




    def value(self):

        localctx = QueryExprParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 210
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 114432) != 0):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JoinOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Join(self):
            return self.getToken(QueryExprParser.Join, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_joinOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJoinOp" ):
                listener.enterJoinOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJoinOp" ):
                listener.exitJoinOp(self)




    def joinOp(self):

        localctx = QueryExprParser.JoinOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_joinOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 212
            self.match(QueryExprParser.Join)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AndOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def And(self):
            return self.getToken(QueryExprParser.And, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_andOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndOp" ):
                listener.enterAndOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndOp" ):
                listener.exitAndOp(self)




    def andOp(self):

        localctx = QueryExprParser.AndOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_andOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 214
            self.match(QueryExprParser.And)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Or(self):
            return self.getToken(QueryExprParser.Or, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_orOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrOp" ):
                listener.enterOrOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrOp" ):
                listener.exitOrOp(self)




    def orOp(self):

        localctx = QueryExprParser.OrOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_orOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 216
            self.match(QueryExprParser.Or)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class MultiplicativeOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Star(self):
            return self.getToken(QueryExprParser.Star, 0)

        def Div(self):
            return self.getToken(QueryExprParser.Div, 0)

        def Dot(self):
            return self.getToken(QueryExprParser.Dot, 0)

        def Mod(self):
            return self.getToken(QueryExprParser.Mod, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_multiplicativeOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeOp" ):
                listener.enterMultiplicativeOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeOp" ):
                listener.exitMultiplicativeOp(self)




    def multiplicativeOp(self):

        localctx = QueryExprParser.MultiplicativeOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_multiplicativeOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 218
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 16106127360) != 0):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AdditiveOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Plus(self):
            return self.getToken(QueryExprParser.Plus, 0)

        def Minus(self):
            return self.getToken(QueryExprParser.Minus, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_additiveOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveOp" ):
                listener.enterAdditiveOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveOp" ):
                listener.exitAdditiveOp(self)




    def additiveOp(self):

        localctx = QueryExprParser.AdditiveOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_additiveOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 220
            _la = self._input.LA(1)
            if not(_la==27 or _la==29):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RelationalOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Gt(self):
            return self.getToken(QueryExprParser.Gt, 0)

        def Lt(self):
            return self.getToken(QueryExprParser.Lt, 0)

        def Gte(self):
            return self.getToken(QueryExprParser.Gte, 0)

        def Lte(self):
            return self.getToken(QueryExprParser.Lte, 0)

        def Ne(self):
            return self.getToken(QueryExprParser.Ne, 0)

        def Eq(self):
            return self.getToken(QueryExprParser.Eq, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_relationalOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalOp" ):
                listener.enterRelationalOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalOp" ):
                listener.exitRelationalOp(self)




    def relationalOp(self):

        localctx = QueryExprParser.RelationalOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_relationalOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 222
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 4329327034368) != 0):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UniOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Tilde(self):
            return self.getToken(QueryExprParser.Tilde, 0)

        def Search(self):
            return self.getToken(QueryExprParser.Search, 0)

        def Minus(self):
            return self.getToken(QueryExprParser.Minus, 0)

        def Plus(self):
            return self.getToken(QueryExprParser.Plus, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_uniOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUniOp" ):
                listener.enterUniOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUniOp" ):
                listener.exitUniOp(self)




    def uniOp(self):

        localctx = QueryExprParser.UniOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_uniOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 224
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 13194810621952) != 0):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BinOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def multiplicativeOp(self):
            return self.getTypedRuleContext(QueryExprParser.MultiplicativeOpContext,0)


        def additiveOp(self):
            return self.getTypedRuleContext(QueryExprParser.AdditiveOpContext,0)


        def relationalOp(self):
            return self.getTypedRuleContext(QueryExprParser.RelationalOpContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_binOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinOp" ):
                listener.enterBinOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinOp" ):
                listener.exitBinOp(self)




    def binOp(self):

        localctx = QueryExprParser.BinOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_binOp)
        try:
            self.state = 229
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [30, 31, 32, 33]:
                self.enterOuterAlt(localctx, 1)
                self.state = 226
                self.multiplicativeOp()
                pass
            elif token in [27, 29]:
                self.enterOuterAlt(localctx, 2)
                self.state = 227
                self.additiveOp()
                pass
            elif token in [36, 37, 38, 39, 40, 41]:
                self.enterOuterAlt(localctx, 3)
                self.state = 228
                self.relationalOp()
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


    class AsUniOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def uniOp(self):
            return self.getTypedRuleContext(QueryExprParser.UniOpContext,0)


        def binOp(self):
            return self.getTypedRuleContext(QueryExprParser.BinOpContext,0)


        def getRuleIndex(self):
            return QueryExprParser.RULE_asUniOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAsUniOp" ):
                listener.enterAsUniOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAsUniOp" ):
                listener.exitAsUniOp(self)




    def asUniOp(self):

        localctx = QueryExprParser.AsUniOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_asUniOp)
        try:
            self.state = 233
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,16,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 231
                self.uniOp()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 232
                self.binOp()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[11] = self.expr_sempred
        self._predicates[16] = self.idExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 3)
         

    def idExpr_sempred(self, localctx:IdExprContext, predIndex:int):
            if predIndex == 6:
                return self.precpred(self._ctx, 1)
         




