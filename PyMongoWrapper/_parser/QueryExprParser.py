# Generated from QueryExpr.g by ANTLR 4.11.1
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
        4,1,48,259,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,1,0,4,0,58,8,0,11,0,12,0,59,1,0,1,0,1,0,3,0,65,8,0,1,1,
        1,1,1,1,5,1,70,8,1,10,1,12,1,73,9,1,1,1,3,1,76,8,1,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,3,2,100,8,2,1,3,1,3,1,3,1,3,3,3,106,8,3,1,4,1,4,1,4,1,
        5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,10,1,10,
        1,10,3,10,128,8,10,1,10,1,10,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,3,11,148,8,11,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,5,11,174,8,11,
        10,11,12,11,177,9,11,1,12,1,12,1,12,1,12,1,12,1,12,3,12,185,8,12,
        1,13,1,13,3,13,189,8,13,1,13,1,13,1,14,1,14,1,14,3,14,196,8,14,1,
        14,1,14,1,14,1,14,3,14,202,8,14,3,14,204,8,14,1,15,1,15,1,15,5,15,
        209,8,15,10,15,12,15,212,9,15,1,16,1,16,1,16,1,16,3,16,218,8,16,
        1,16,1,16,1,16,5,16,223,8,16,10,16,12,16,226,9,16,1,17,1,17,1,18,
        1,18,1,19,1,19,1,20,1,20,1,21,1,21,1,22,1,22,1,23,1,23,1,24,1,24,
        1,24,1,24,3,24,246,8,24,1,25,1,25,1,25,3,25,251,8,25,1,26,1,26,1,
        27,1,27,3,27,257,8,27,1,27,0,2,22,32,28,0,2,4,6,8,10,12,14,16,18,
        20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,0,4,2,0,8,
        13,15,17,1,0,31,34,2,0,28,28,30,30,1,0,37,42,274,0,64,1,0,0,0,2,
        75,1,0,0,0,4,99,1,0,0,0,6,101,1,0,0,0,8,107,1,0,0,0,10,110,1,0,0,
        0,12,114,1,0,0,0,14,118,1,0,0,0,16,120,1,0,0,0,18,122,1,0,0,0,20,
        124,1,0,0,0,22,147,1,0,0,0,24,184,1,0,0,0,26,186,1,0,0,0,28,203,
        1,0,0,0,30,205,1,0,0,0,32,217,1,0,0,0,34,227,1,0,0,0,36,229,1,0,
        0,0,38,231,1,0,0,0,40,233,1,0,0,0,42,235,1,0,0,0,44,237,1,0,0,0,
        46,239,1,0,0,0,48,245,1,0,0,0,50,250,1,0,0,0,52,252,1,0,0,0,54,256,
        1,0,0,0,56,58,3,4,2,0,57,56,1,0,0,0,58,59,1,0,0,0,59,57,1,0,0,0,
        59,60,1,0,0,0,60,65,1,0,0,0,61,65,3,2,1,0,62,65,3,22,11,0,63,65,
        3,30,15,0,64,57,1,0,0,0,64,61,1,0,0,0,64,62,1,0,0,0,64,63,1,0,0,
        0,65,1,1,0,0,0,66,76,3,4,2,0,67,71,5,21,0,0,68,70,3,4,2,0,69,68,
        1,0,0,0,70,73,1,0,0,0,71,69,1,0,0,0,71,72,1,0,0,0,72,74,1,0,0,0,
        73,71,1,0,0,0,74,76,5,22,0,0,75,66,1,0,0,0,75,67,1,0,0,0,76,3,1,
        0,0,0,77,78,3,22,11,0,78,79,5,20,0,0,79,100,1,0,0,0,80,81,3,30,15,
        0,81,82,5,20,0,0,82,100,1,0,0,0,83,84,3,20,10,0,84,85,5,20,0,0,85,
        100,1,0,0,0,86,100,3,6,3,0,87,100,3,10,5,0,88,100,3,12,6,0,89,90,
        3,14,7,0,90,91,5,20,0,0,91,100,1,0,0,0,92,93,3,16,8,0,93,94,5,20,
        0,0,94,100,1,0,0,0,95,96,3,18,9,0,96,97,5,20,0,0,97,100,1,0,0,0,
        98,100,5,20,0,0,99,77,1,0,0,0,99,80,1,0,0,0,99,83,1,0,0,0,99,86,
        1,0,0,0,99,87,1,0,0,0,99,88,1,0,0,0,99,89,1,0,0,0,99,92,1,0,0,0,
        99,95,1,0,0,0,99,98,1,0,0,0,100,5,1,0,0,0,101,102,5,1,0,0,102,103,
        3,22,11,0,103,105,3,2,1,0,104,106,3,8,4,0,105,104,1,0,0,0,105,106,
        1,0,0,0,106,7,1,0,0,0,107,108,5,2,0,0,108,109,3,2,1,0,109,9,1,0,
        0,0,110,111,5,3,0,0,111,112,3,22,11,0,112,113,3,2,1,0,113,11,1,0,
        0,0,114,115,5,4,0,0,115,116,3,20,10,0,116,117,3,2,1,0,117,13,1,0,
        0,0,118,119,5,5,0,0,119,15,1,0,0,0,120,121,5,6,0,0,121,17,1,0,0,
        0,122,123,5,7,0,0,123,19,1,0,0,0,124,125,5,18,0,0,125,127,5,19,0,
        0,126,128,5,42,0,0,127,126,1,0,0,0,127,128,1,0,0,0,128,129,1,0,0,
        0,129,130,3,22,11,0,130,21,1,0,0,0,131,132,6,11,-1,0,132,133,5,23,
        0,0,133,134,3,22,11,0,134,135,5,24,0,0,135,148,1,0,0,0,136,148,3,
        26,13,0,137,148,3,24,12,0,138,148,3,28,14,0,139,140,3,54,27,0,140,
        141,3,22,11,10,141,148,1,0,0,0,142,143,3,52,26,0,143,144,3,22,11,
        6,144,148,1,0,0,0,145,148,3,34,17,0,146,148,3,32,16,0,147,131,1,
        0,0,0,147,136,1,0,0,0,147,137,1,0,0,0,147,138,1,0,0,0,147,139,1,
        0,0,0,147,142,1,0,0,0,147,145,1,0,0,0,147,146,1,0,0,0,148,175,1,
        0,0,0,149,150,10,9,0,0,150,151,3,42,21,0,151,152,3,22,11,10,152,
        174,1,0,0,0,153,154,10,8,0,0,154,155,3,44,22,0,155,156,3,22,11,9,
        156,174,1,0,0,0,157,158,10,7,0,0,158,159,3,46,23,0,159,160,3,22,
        11,8,160,174,1,0,0,0,161,162,10,5,0,0,162,163,3,38,19,0,163,164,
        3,22,11,6,164,174,1,0,0,0,165,166,10,4,0,0,166,167,3,40,20,0,167,
        168,3,22,11,5,168,174,1,0,0,0,169,170,10,3,0,0,170,171,3,36,18,0,
        171,172,3,22,11,4,172,174,1,0,0,0,173,149,1,0,0,0,173,153,1,0,0,
        0,173,157,1,0,0,0,173,161,1,0,0,0,173,165,1,0,0,0,173,169,1,0,0,
        0,174,177,1,0,0,0,175,173,1,0,0,0,175,176,1,0,0,0,176,23,1,0,0,0,
        177,175,1,0,0,0,178,179,5,25,0,0,179,180,3,30,15,0,180,181,5,26,
        0,0,181,185,1,0,0,0,182,183,5,25,0,0,183,185,5,26,0,0,184,178,1,
        0,0,0,184,182,1,0,0,0,185,25,1,0,0,0,186,188,5,23,0,0,187,189,3,
        30,15,0,188,187,1,0,0,0,188,189,1,0,0,0,189,190,1,0,0,0,190,191,
        5,24,0,0,191,27,1,0,0,0,192,193,5,18,0,0,193,195,5,23,0,0,194,196,
        3,30,15,0,195,194,1,0,0,0,195,196,1,0,0,0,196,197,1,0,0,0,197,204,
        5,24,0,0,198,201,5,11,0,0,199,202,3,34,17,0,200,202,3,32,16,0,201,
        199,1,0,0,0,201,200,1,0,0,0,202,204,1,0,0,0,203,192,1,0,0,0,203,
        198,1,0,0,0,204,29,1,0,0,0,205,210,3,22,11,0,206,207,5,27,0,0,207,
        209,3,22,11,0,208,206,1,0,0,0,209,212,1,0,0,0,210,208,1,0,0,0,210,
        211,1,0,0,0,211,31,1,0,0,0,212,210,1,0,0,0,213,214,6,16,-1,0,214,
        218,5,18,0,0,215,216,5,45,0,0,216,218,3,32,16,2,217,213,1,0,0,0,
        217,215,1,0,0,0,218,224,1,0,0,0,219,220,10,1,0,0,220,221,5,34,0,
        0,221,223,5,18,0,0,222,219,1,0,0,0,223,226,1,0,0,0,224,222,1,0,0,
        0,224,225,1,0,0,0,225,33,1,0,0,0,226,224,1,0,0,0,227,228,7,0,0,0,
        228,35,1,0,0,0,229,230,5,29,0,0,230,37,1,0,0,0,231,232,5,35,0,0,
        232,39,1,0,0,0,233,234,5,36,0,0,234,41,1,0,0,0,235,236,7,1,0,0,236,
        43,1,0,0,0,237,238,7,2,0,0,238,45,1,0,0,0,239,240,7,3,0,0,240,47,
        1,0,0,0,241,246,3,52,26,0,242,246,5,43,0,0,243,246,5,30,0,0,244,
        246,5,28,0,0,245,241,1,0,0,0,245,242,1,0,0,0,245,243,1,0,0,0,245,
        244,1,0,0,0,246,49,1,0,0,0,247,251,3,42,21,0,248,251,3,44,22,0,249,
        251,3,46,23,0,250,247,1,0,0,0,250,248,1,0,0,0,250,249,1,0,0,0,251,
        51,1,0,0,0,252,253,5,44,0,0,253,53,1,0,0,0,254,257,3,48,24,0,255,
        257,3,50,25,0,256,254,1,0,0,0,256,255,1,0,0,0,257,55,1,0,0,0,21,
        59,64,71,75,99,105,127,147,173,175,184,188,195,201,203,210,217,224,
        245,250,256
    ]

class QueryExprParser ( Parser ):

    grammarFileName = "QueryExpr.g"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'else'", "'repeat'", "'for'", 
                     "'break'", "'continue'", "'halt'", "'true'", "'false'", 
                     "'null'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "':'", "';'", "'{'", "'}'", "'('", "')'", "'['", "']'", 
                     "','", "'+'", "'=>'", "'-'", "'*'", "'/'", "'%'", "'.'", 
                     "'&'", "'|'", "'>'", "'<'", "'>='", "'<='", "'!='", 
                     "'='", "'%%'", "'~'", "'$'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "SHORTCUT", 
                      "STRING", "NUMBER", "TIME", "TIME_INTERVAL", "DATETIME", 
                      "OBJECT_ID", "ID", "Colon", "Semicolon", "LBrace", 
                      "RBrace", "LPar", "RPar", "LBrack", "RBrack", "Comma", 
                      "Plus", "Join", "Minus", "Star", "Div", "Mod", "Dot", 
                      "And", "Or", "Gt", "Lt", "Gte", "Lte", "Ne", "Eq", 
                      "Search", "Tilde", "Dollar", "WS", "COMMENT", "LINE_COMMENT" ]

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
    RULE_notOp = 26
    RULE_asUniOp = 27

    ruleNames =  [ "snippet", "stmts", "stmt", "ifStmt", "else", "repeatStmt", 
                   "forStmt", "break", "continue", "halt", "assignment", 
                   "expr", "arr", "obj", "func", "sepExpr", "idExpr", "value", 
                   "joinOp", "andOp", "orOp", "multiplicativeOp", "additiveOp", 
                   "relationalOp", "uniOp", "binOp", "notOp", "asUniOp" ]

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
    OBJECT_ID=17
    ID=18
    Colon=19
    Semicolon=20
    LBrace=21
    RBrace=22
    LPar=23
    RPar=24
    LBrack=25
    RBrack=26
    Comma=27
    Plus=28
    Join=29
    Minus=30
    Star=31
    Div=32
    Mod=33
    Dot=34
    And=35
    Or=36
    Gt=37
    Lt=38
    Gte=39
    Lte=40
    Ne=41
    Eq=42
    Search=43
    Tilde=44
    Dollar=45
    WS=46
    COMMENT=47
    LINE_COMMENT=48

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
            self.state = 64
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 57 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 56
                    self.stmt()
                    self.state = 59 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (((_la) & ~0x3f) == 0 and ((1 << _la) & 70264903155706) != 0):
                        break

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 61
                self.stmts()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 62
                self.expr(0)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 63
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
            self.state = 75
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 20, 23, 25, 28, 30, 31, 32, 33, 34, 37, 38, 39, 40, 41, 42, 43, 44, 45]:
                self.enterOuterAlt(localctx, 1)
                self.state = 66
                self.stmt()
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 2)
                self.state = 67
                self.match(QueryExprParser.LBrace)
                self.state = 71
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while ((_la) & ~0x3f) == 0 and ((1 << _la) & 70264903155706) != 0:
                    self.state = 68
                    self.stmt()
                    self.state = 73
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 74
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

        def sepExpr(self):
            return self.getTypedRuleContext(QueryExprParser.SepExprContext,0)


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
            self.state = 99
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,4,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 77
                self.expr(0)
                self.state = 78
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 80
                self.sepExpr()
                self.state = 81
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 83
                self.assignment()
                self.state = 84
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 86
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 87
                self.repeatStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 88
                self.forStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 89
                self.break_()
                self.state = 90
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 92
                self.continue_()
                self.state = 93
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 95
                self.halt()
                self.state = 96
                self.match(QueryExprParser.Semicolon)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 98
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
            self.state = 101
            self.match(QueryExprParser.T__0)
            self.state = 102
            localctx.cond = self.expr(0)
            self.state = 103
            localctx.if_true = self.stmts()
            self.state = 105
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.state = 104
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
            self.state = 107
            self.match(QueryExprParser.T__1)
            self.state = 108
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
            self.state = 110
            self.match(QueryExprParser.T__2)
            self.state = 111
            localctx.cond = self.expr(0)
            self.state = 112
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
            self.state = 114
            self.match(QueryExprParser.T__3)
            self.state = 115
            localctx.assign = self.assignment()
            self.state = 116
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
            self.state = 118
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
            self.state = 120
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
            self.state = 122
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


        def Eq(self):
            return self.getToken(QueryExprParser.Eq, 0)

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
            self.state = 124
            localctx.target = self.match(QueryExprParser.ID)
            self.state = 125
            self.match(QueryExprParser.Colon)
            self.state = 127
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 126
                self.match(QueryExprParser.Eq)


            self.state = 129
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
            self.notop = None # NotOpContext
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


        def notOp(self):
            return self.getTypedRuleContext(QueryExprParser.NotOpContext,0)


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
            self.state = 147
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.state = 132
                self.match(QueryExprParser.LPar)
                self.state = 133
                localctx.parred = self.expr(0)
                self.state = 134
                self.match(QueryExprParser.RPar)
                pass

            elif la_ == 2:
                self.state = 136
                self.obj()
                pass

            elif la_ == 3:
                self.state = 137
                self.arr()
                pass

            elif la_ == 4:
                self.state = 138
                self.func()
                pass

            elif la_ == 5:
                self.state = 139
                localctx.uniop = self.asUniOp()
                self.state = 140
                localctx.right = self.expr(10)
                pass

            elif la_ == 6:
                self.state = 142
                localctx.notop = self.notOp()
                self.state = 143
                localctx.right = self.expr(6)
                pass

            elif la_ == 7:
                self.state = 145
                self.value()
                pass

            elif la_ == 8:
                self.state = 146
                self.idExpr(0)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 175
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,9,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 173
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
                    if la_ == 1:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 149
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 150
                        localctx.op1 = self.multiplicativeOp()
                        self.state = 151
                        localctx.right = self.expr(10)
                        pass

                    elif la_ == 2:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 153
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 154
                        localctx.op2 = self.additiveOp()
                        self.state = 155
                        localctx.right = self.expr(9)
                        pass

                    elif la_ == 3:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 157
                        if not self.precpred(self._ctx, 7):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 7)")
                        self.state = 158
                        localctx.op3 = self.relationalOp()
                        self.state = 159
                        localctx.right = self.expr(8)
                        pass

                    elif la_ == 4:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 161
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 162
                        localctx.op4 = self.andOp()
                        self.state = 163
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 5:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 165
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 166
                        localctx.op5 = self.orOp()
                        self.state = 167
                        localctx.right = self.expr(5)
                        pass

                    elif la_ == 6:
                        localctx = QueryExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 169
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 170
                        localctx.op6 = self.joinOp()
                        self.state = 171
                        localctx.right = self.expr(4)
                        pass

             
                self.state = 177
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,9,self._ctx)

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
            self.state = 184
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 178
                self.match(QueryExprParser.LBrack)
                self.state = 179
                self.sepExpr()
                self.state = 180
                self.match(QueryExprParser.RBrack)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 182
                self.match(QueryExprParser.LBrack)
                self.state = 183
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
            self.state = 186
            self.match(QueryExprParser.LPar)
            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if ((_la) & ~0x3f) == 0 and ((1 << _la) & 70264902106880) != 0:
                self.state = 187
                localctx.val = self.sepExpr()


            self.state = 190
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


        def SHORTCUT(self):
            return self.getToken(QueryExprParser.SHORTCUT, 0)

        def value(self):
            return self.getTypedRuleContext(QueryExprParser.ValueContext,0)


        def idExpr(self):
            return self.getTypedRuleContext(QueryExprParser.IdExprContext,0)


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
            self.state = 203
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.enterOuterAlt(localctx, 1)
                self.state = 192
                localctx.func_name = self.match(QueryExprParser.ID)
                self.state = 193
                self.match(QueryExprParser.LPar)
                self.state = 195
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if ((_la) & ~0x3f) == 0 and ((1 << _la) & 70264902106880) != 0:
                    self.state = 194
                    self.sepExpr()


                self.state = 197
                self.match(QueryExprParser.RPar)
                pass
            elif token in [11]:
                self.enterOuterAlt(localctx, 2)
                self.state = 198
                localctx.func_name = self.match(QueryExprParser.SHORTCUT)
                self.state = 201
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [8, 9, 10, 11, 12, 13, 15, 16, 17]:
                    self.state = 199
                    self.value()
                    pass
                elif token in [18, 45]:
                    self.state = 200
                    self.idExpr(0)
                    pass
                else:
                    raise NoViableAltException(self)

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
            self.state = 205
            self.expr(0)
            self.state = 210
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==27:
                self.state = 206
                self.match(QueryExprParser.Comma)
                self.state = 207
                self.expr(0)
                self.state = 212
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
            self.state = 217
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18]:
                self.state = 214
                self.match(QueryExprParser.ID)
                pass
            elif token in [45]:
                self.state = 215
                self.match(QueryExprParser.Dollar)
                self.state = 216
                self.idExpr(2)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 224
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,17,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = QueryExprParser.IdExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_idExpr)
                    self.state = 219
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 220
                    self.match(QueryExprParser.Dot)
                    self.state = 221
                    self.match(QueryExprParser.ID) 
                self.state = 226
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,17,self._ctx)

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

        def OBJECT_ID(self):
            return self.getToken(QueryExprParser.OBJECT_ID, 0)

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
            self.state = 227
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 245504) != 0):
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
            self.state = 229
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
            self.state = 231
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
            self.state = 233
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
            self.state = 235
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 32212254720) != 0):
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
            self.state = 237
            _la = self._input.LA(1)
            if not(_la==28 or _la==30):
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
            self.state = 239
            _la = self._input.LA(1)
            if not(((_la) & ~0x3f) == 0 and ((1 << _la) & 8658654068736) != 0):
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

        def notOp(self):
            return self.getTypedRuleContext(QueryExprParser.NotOpContext,0)


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
        try:
            self.state = 245
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [44]:
                self.enterOuterAlt(localctx, 1)
                self.state = 241
                self.notOp()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 242
                self.match(QueryExprParser.Search)
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 3)
                self.state = 243
                self.match(QueryExprParser.Minus)
                pass
            elif token in [28]:
                self.enterOuterAlt(localctx, 4)
                self.state = 244
                self.match(QueryExprParser.Plus)
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
            self.state = 250
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [31, 32, 33, 34]:
                self.enterOuterAlt(localctx, 1)
                self.state = 247
                self.multiplicativeOp()
                pass
            elif token in [28, 30]:
                self.enterOuterAlt(localctx, 2)
                self.state = 248
                self.additiveOp()
                pass
            elif token in [37, 38, 39, 40, 41, 42]:
                self.enterOuterAlt(localctx, 3)
                self.state = 249
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


    class NotOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def Tilde(self):
            return self.getToken(QueryExprParser.Tilde, 0)

        def getRuleIndex(self):
            return QueryExprParser.RULE_notOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotOp" ):
                listener.enterNotOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotOp" ):
                listener.exitNotOp(self)




    def notOp(self):

        localctx = QueryExprParser.NotOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_notOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 252
            self.match(QueryExprParser.Tilde)
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
        self.enterRule(localctx, 54, self.RULE_asUniOp)
        try:
            self.state = 256
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,20,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 254
                self.uniOp()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 255
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
                return self.precpred(self._ctx, 9)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 7)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 3)
         

    def idExpr_sempred(self, localctx:IdExprContext, predIndex:int):
            if predIndex == 6:
                return self.precpred(self._ctx, 1)
         




