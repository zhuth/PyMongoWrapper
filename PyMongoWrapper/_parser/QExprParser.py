# Generated from QExpr.g by ANTLR 4.13.0
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
        4,1,50,292,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,1,0,4,0,62,8,0,11,0,12,0,63,1,0,1,
        0,1,0,3,0,69,8,0,1,1,1,1,1,1,5,1,74,8,1,10,1,12,1,77,9,1,1,1,3,1,
        80,8,1,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,5,2,91,8,2,10,2,12,2,
        94,9,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,2,1,
        2,1,2,1,2,1,2,1,2,3,2,115,8,2,1,3,1,3,1,3,1,3,3,3,121,8,3,1,4,1,
        4,1,4,1,5,1,5,1,5,1,5,1,6,1,6,1,6,1,6,1,6,1,6,1,7,1,7,1,7,1,8,1,
        8,1,8,1,9,1,9,1,10,1,10,1,11,1,11,1,12,1,12,1,12,3,12,151,8,12,1,
        12,1,12,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,3,13,171,8,13,1,13,1,13,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,
        13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,13,1,
        13,1,13,1,13,5,13,207,8,13,10,13,12,13,210,9,13,1,14,1,14,1,14,1,
        14,1,14,1,14,3,14,218,8,14,1,15,1,15,3,15,222,8,15,1,15,1,15,1,16,
        1,16,1,16,3,16,229,8,16,1,16,1,16,1,16,1,16,3,16,235,8,16,3,16,237,
        8,16,1,17,1,17,1,17,5,17,242,8,17,10,17,12,17,245,9,17,1,18,1,18,
        1,18,1,18,3,18,251,8,18,1,18,1,18,1,18,5,18,256,8,18,10,18,12,18,
        259,9,18,1,19,1,19,1,20,1,20,1,21,1,21,1,22,1,22,1,23,1,23,1,24,
        1,24,1,25,1,25,1,26,1,26,1,26,1,26,3,26,279,8,26,1,27,1,27,1,27,
        3,27,284,8,27,1,28,1,28,1,29,1,29,3,29,290,8,29,1,29,0,2,26,36,30,
        0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,
        46,48,50,52,54,56,58,0,4,2,0,9,15,17,19,1,0,33,36,2,0,30,30,32,32,
        1,0,39,44,310,0,68,1,0,0,0,2,79,1,0,0,0,4,114,1,0,0,0,6,116,1,0,
        0,0,8,122,1,0,0,0,10,125,1,0,0,0,12,129,1,0,0,0,14,135,1,0,0,0,16,
        138,1,0,0,0,18,141,1,0,0,0,20,143,1,0,0,0,22,145,1,0,0,0,24,147,
        1,0,0,0,26,170,1,0,0,0,28,217,1,0,0,0,30,219,1,0,0,0,32,236,1,0,
        0,0,34,238,1,0,0,0,36,250,1,0,0,0,38,260,1,0,0,0,40,262,1,0,0,0,
        42,264,1,0,0,0,44,266,1,0,0,0,46,268,1,0,0,0,48,270,1,0,0,0,50,272,
        1,0,0,0,52,278,1,0,0,0,54,283,1,0,0,0,56,285,1,0,0,0,58,289,1,0,
        0,0,60,62,3,4,2,0,61,60,1,0,0,0,62,63,1,0,0,0,63,61,1,0,0,0,63,64,
        1,0,0,0,64,69,1,0,0,0,65,69,3,2,1,0,66,69,3,26,13,0,67,69,3,34,17,
        0,68,61,1,0,0,0,68,65,1,0,0,0,68,66,1,0,0,0,68,67,1,0,0,0,69,1,1,
        0,0,0,70,80,3,4,2,0,71,75,5,23,0,0,72,74,3,4,2,0,73,72,1,0,0,0,74,
        77,1,0,0,0,75,73,1,0,0,0,75,76,1,0,0,0,76,78,1,0,0,0,77,75,1,0,0,
        0,78,80,5,24,0,0,79,70,1,0,0,0,79,71,1,0,0,0,80,3,1,0,0,0,81,82,
        3,26,13,0,82,83,5,22,0,0,83,115,1,0,0,0,84,85,3,34,17,0,85,86,5,
        22,0,0,86,115,1,0,0,0,87,92,3,24,12,0,88,89,5,29,0,0,89,91,3,24,
        12,0,90,88,1,0,0,0,91,94,1,0,0,0,92,90,1,0,0,0,92,93,1,0,0,0,93,
        95,1,0,0,0,94,92,1,0,0,0,95,96,5,22,0,0,96,115,1,0,0,0,97,115,3,
        6,3,0,98,115,3,10,5,0,99,115,3,12,6,0,100,101,3,18,9,0,101,102,5,
        22,0,0,102,115,1,0,0,0,103,104,3,20,10,0,104,105,5,22,0,0,105,115,
        1,0,0,0,106,107,3,22,11,0,107,108,5,22,0,0,108,115,1,0,0,0,109,110,
        3,16,8,0,110,111,5,22,0,0,111,115,1,0,0,0,112,115,3,14,7,0,113,115,
        5,22,0,0,114,81,1,0,0,0,114,84,1,0,0,0,114,87,1,0,0,0,114,97,1,0,
        0,0,114,98,1,0,0,0,114,99,1,0,0,0,114,100,1,0,0,0,114,103,1,0,0,
        0,114,106,1,0,0,0,114,109,1,0,0,0,114,112,1,0,0,0,114,113,1,0,0,
        0,115,5,1,0,0,0,116,117,5,1,0,0,117,118,3,26,13,0,118,120,3,2,1,
        0,119,121,3,8,4,0,120,119,1,0,0,0,120,121,1,0,0,0,121,7,1,0,0,0,
        122,123,5,2,0,0,123,124,3,2,1,0,124,9,1,0,0,0,125,126,5,3,0,0,126,
        127,3,26,13,0,127,128,3,2,1,0,128,11,1,0,0,0,129,130,5,4,0,0,130,
        131,5,25,0,0,131,132,3,24,12,0,132,133,5,26,0,0,133,134,3,2,1,0,
        134,13,1,0,0,0,135,136,5,12,0,0,136,137,3,2,1,0,137,15,1,0,0,0,138,
        139,5,5,0,0,139,140,3,26,13,0,140,17,1,0,0,0,141,142,5,6,0,0,142,
        19,1,0,0,0,143,144,5,7,0,0,144,21,1,0,0,0,145,146,5,8,0,0,146,23,
        1,0,0,0,147,148,3,36,18,0,148,150,5,21,0,0,149,151,5,44,0,0,150,
        149,1,0,0,0,150,151,1,0,0,0,151,152,1,0,0,0,152,153,3,26,13,0,153,
        25,1,0,0,0,154,155,6,13,-1,0,155,156,5,25,0,0,156,157,3,26,13,0,
        157,158,5,26,0,0,158,171,1,0,0,0,159,171,3,30,15,0,160,171,3,28,
        14,0,161,171,3,32,16,0,162,171,3,38,19,0,163,164,3,58,29,0,164,165,
        3,26,13,11,165,171,1,0,0,0,166,167,3,56,28,0,167,168,3,26,13,7,168,
        171,1,0,0,0,169,171,3,36,18,0,170,154,1,0,0,0,170,159,1,0,0,0,170,
        160,1,0,0,0,170,161,1,0,0,0,170,162,1,0,0,0,170,163,1,0,0,0,170,
        166,1,0,0,0,170,169,1,0,0,0,171,208,1,0,0,0,172,173,10,10,0,0,173,
        174,3,46,23,0,174,175,3,26,13,11,175,207,1,0,0,0,176,177,10,9,0,
        0,177,178,3,48,24,0,178,179,3,26,13,10,179,207,1,0,0,0,180,181,10,
        8,0,0,181,182,3,50,25,0,182,183,3,26,13,9,183,207,1,0,0,0,184,185,
        10,6,0,0,185,186,3,42,21,0,186,187,3,26,13,7,187,207,1,0,0,0,188,
        189,10,5,0,0,189,190,3,44,22,0,190,191,3,26,13,6,191,207,1,0,0,0,
        192,193,10,4,0,0,193,194,3,40,20,0,194,195,3,26,13,5,195,207,1,0,
        0,0,196,197,10,3,0,0,197,198,5,27,0,0,198,199,3,26,13,0,199,200,
        5,28,0,0,200,207,1,0,0,0,201,202,10,2,0,0,202,203,5,27,0,0,203,204,
        3,24,12,0,204,205,5,28,0,0,205,207,1,0,0,0,206,172,1,0,0,0,206,176,
        1,0,0,0,206,180,1,0,0,0,206,184,1,0,0,0,206,188,1,0,0,0,206,192,
        1,0,0,0,206,196,1,0,0,0,206,201,1,0,0,0,207,210,1,0,0,0,208,206,
        1,0,0,0,208,209,1,0,0,0,209,27,1,0,0,0,210,208,1,0,0,0,211,212,5,
        27,0,0,212,213,3,34,17,0,213,214,5,28,0,0,214,218,1,0,0,0,215,216,
        5,27,0,0,216,218,5,28,0,0,217,211,1,0,0,0,217,215,1,0,0,0,218,29,
        1,0,0,0,219,221,5,25,0,0,220,222,3,34,17,0,221,220,1,0,0,0,221,222,
        1,0,0,0,222,223,1,0,0,0,223,224,5,26,0,0,224,31,1,0,0,0,225,226,
        5,20,0,0,226,228,5,25,0,0,227,229,3,34,17,0,228,227,1,0,0,0,228,
        229,1,0,0,0,229,230,1,0,0,0,230,237,5,26,0,0,231,234,5,12,0,0,232,
        235,3,38,19,0,233,235,3,36,18,0,234,232,1,0,0,0,234,233,1,0,0,0,
        235,237,1,0,0,0,236,225,1,0,0,0,236,231,1,0,0,0,237,33,1,0,0,0,238,
        243,3,26,13,0,239,240,5,29,0,0,240,242,3,26,13,0,241,239,1,0,0,0,
        242,245,1,0,0,0,243,241,1,0,0,0,243,244,1,0,0,0,244,35,1,0,0,0,245,
        243,1,0,0,0,246,247,6,18,-1,0,247,251,5,20,0,0,248,249,5,47,0,0,
        249,251,3,36,18,2,250,246,1,0,0,0,250,248,1,0,0,0,251,257,1,0,0,
        0,252,253,10,1,0,0,253,254,5,36,0,0,254,256,5,20,0,0,255,252,1,0,
        0,0,256,259,1,0,0,0,257,255,1,0,0,0,257,258,1,0,0,0,258,37,1,0,0,
        0,259,257,1,0,0,0,260,261,7,0,0,0,261,39,1,0,0,0,262,263,5,31,0,
        0,263,41,1,0,0,0,264,265,5,37,0,0,265,43,1,0,0,0,266,267,5,38,0,
        0,267,45,1,0,0,0,268,269,7,1,0,0,269,47,1,0,0,0,270,271,7,2,0,0,
        271,49,1,0,0,0,272,273,7,3,0,0,273,51,1,0,0,0,274,279,3,56,28,0,
        275,279,5,45,0,0,276,279,5,32,0,0,277,279,5,30,0,0,278,274,1,0,0,
        0,278,275,1,0,0,0,278,276,1,0,0,0,278,277,1,0,0,0,279,53,1,0,0,0,
        280,284,3,46,23,0,281,284,3,48,24,0,282,284,3,50,25,0,283,280,1,
        0,0,0,283,281,1,0,0,0,283,282,1,0,0,0,284,55,1,0,0,0,285,286,5,46,
        0,0,286,57,1,0,0,0,287,290,3,52,26,0,288,290,3,54,27,0,289,287,1,
        0,0,0,289,288,1,0,0,0,290,59,1,0,0,0,22,63,68,75,79,92,114,120,150,
        170,206,208,217,221,228,234,236,243,250,257,278,283,289
    ]

class QExprParser ( Parser ):

    grammarFileName = "QExpr.g"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'if'", "'else'", "'repeat'", "'for'", 
                     "'return'", "'break'", "'continue'", "'halt'", "'true'", 
                     "'false'", "'null'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "':'", "';'", "'{'", "'}'", 
                     "'('", "')'", "'['", "']'", "','", "'+'", "'=>'", "'-'", 
                     "'*'", "'/'", "'%'", "'.'", "'&'", "'|'", "'>'", "'<'", 
                     "'>='", "'<='", "'!='", "'='", "'%%'", "'~'", "'$'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "SHORTCUT", "STRING", "REGEX", "NUMBER", "TIME", "TIME_INTERVAL", 
                      "DATETIME", "OBJECT_ID", "ID", "Colon", "Semicolon", 
                      "LBrace", "RBrace", "LPar", "RPar", "LBrack", "RBrack", 
                      "Comma", "Plus", "Join", "Minus", "Star", "Div", "Mod", 
                      "Dot", "And", "Or", "Gt", "Lt", "Gte", "Lte", "Ne", 
                      "Eq", "Search", "Tilde", "Dollar", "WS", "COMMENT", 
                      "LINE_COMMENT" ]

    RULE_snippet = 0
    RULE_stmts = 1
    RULE_stmt = 2
    RULE_ifStmt = 3
    RULE_elseStmt = 4
    RULE_repeatStmt = 5
    RULE_forStmt = 6
    RULE_definitionStmt = 7
    RULE_returnStmt = 8
    RULE_breakLoop = 9
    RULE_continueLoop = 10
    RULE_halt = 11
    RULE_assignment = 12
    RULE_expr = 13
    RULE_arr = 14
    RULE_obj = 15
    RULE_func = 16
    RULE_sepExpr = 17
    RULE_idExpr = 18
    RULE_value = 19
    RULE_joinOp = 20
    RULE_andOp = 21
    RULE_orOp = 22
    RULE_multiplicativeOp = 23
    RULE_additiveOp = 24
    RULE_relationalOp = 25
    RULE_uniOp = 26
    RULE_binOp = 27
    RULE_notOp = 28
    RULE_asUniOp = 29

    ruleNames =  [ "snippet", "stmts", "stmt", "ifStmt", "elseStmt", "repeatStmt", 
                   "forStmt", "definitionStmt", "returnStmt", "breakLoop", 
                   "continueLoop", "halt", "assignment", "expr", "arr", 
                   "obj", "func", "sepExpr", "idExpr", "value", "joinOp", 
                   "andOp", "orOp", "multiplicativeOp", "additiveOp", "relationalOp", 
                   "uniOp", "binOp", "notOp", "asUniOp" ]

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
    T__10=11
    SHORTCUT=12
    STRING=13
    REGEX=14
    NUMBER=15
    TIME=16
    TIME_INTERVAL=17
    DATETIME=18
    OBJECT_ID=19
    ID=20
    Colon=21
    Semicolon=22
    LBrace=23
    RBrace=24
    LPar=25
    RPar=26
    LBrack=27
    RBrack=28
    Comma=29
    Plus=30
    Join=31
    Minus=32
    Star=33
    Div=34
    Mod=35
    Dot=36
    And=37
    Or=38
    Gt=39
    Lt=40
    Gte=41
    Lte=42
    Ne=43
    Eq=44
    Search=45
    Tilde=46
    Dollar=47
    WS=48
    COMMENT=49
    LINE_COMMENT=50

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class SnippetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QExprParser.StmtContext)
            else:
                return self.getTypedRuleContext(QExprParser.StmtContext,i)


        def stmts(self):
            return self.getTypedRuleContext(QExprParser.StmtsContext,0)


        def expr(self):
            return self.getTypedRuleContext(QExprParser.ExprContext,0)


        def sepExpr(self):
            return self.getTypedRuleContext(QExprParser.SepExprContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_snippet

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSnippet" ):
                listener.enterSnippet(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSnippet" ):
                listener.exitSnippet(self)




    def snippet(self):

        localctx = QExprParser.SnippetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_snippet)
        self._la = 0 # Token type
        try:
            self.state = 68
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 61 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 60
                    self.stmt()
                    self.state = 63 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 281059612622842) != 0)):
                        break

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 65
                self.stmts()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 66
                self.expr(0)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 67
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
                return self.getTypedRuleContexts(QExprParser.StmtContext)
            else:
                return self.getTypedRuleContext(QExprParser.StmtContext,i)


        def LBrace(self):
            return self.getToken(QExprParser.LBrace, 0)

        def RBrace(self):
            return self.getToken(QExprParser.RBrace, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_stmts

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmts" ):
                listener.enterStmts(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmts" ):
                listener.exitStmts(self)




    def stmts(self):

        localctx = QExprParser.StmtsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmts)
        self._la = 0 # Token type
        try:
            self.state = 79
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 22, 25, 27, 30, 32, 33, 34, 35, 36, 39, 40, 41, 42, 43, 44, 45, 46, 47]:
                self.enterOuterAlt(localctx, 1)
                self.state = 70
                self.stmt()
                pass
            elif token in [23]:
                self.enterOuterAlt(localctx, 2)
                self.state = 71
                self.match(QExprParser.LBrace)
                self.state = 75
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while (((_la) & ~0x3f) == 0 and ((1 << _la) & 281059612622842) != 0):
                    self.state = 72
                    self.stmt()
                    self.state = 77
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 78
                self.match(QExprParser.RBrace)
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
            return self.getTypedRuleContext(QExprParser.ExprContext,0)


        def Semicolon(self):
            return self.getToken(QExprParser.Semicolon, 0)

        def sepExpr(self):
            return self.getTypedRuleContext(QExprParser.SepExprContext,0)


        def assignment(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QExprParser.AssignmentContext)
            else:
                return self.getTypedRuleContext(QExprParser.AssignmentContext,i)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(QExprParser.Comma)
            else:
                return self.getToken(QExprParser.Comma, i)

        def ifStmt(self):
            return self.getTypedRuleContext(QExprParser.IfStmtContext,0)


        def repeatStmt(self):
            return self.getTypedRuleContext(QExprParser.RepeatStmtContext,0)


        def forStmt(self):
            return self.getTypedRuleContext(QExprParser.ForStmtContext,0)


        def breakLoop(self):
            return self.getTypedRuleContext(QExprParser.BreakLoopContext,0)


        def continueLoop(self):
            return self.getTypedRuleContext(QExprParser.ContinueLoopContext,0)


        def halt(self):
            return self.getTypedRuleContext(QExprParser.HaltContext,0)


        def returnStmt(self):
            return self.getTypedRuleContext(QExprParser.ReturnStmtContext,0)


        def definitionStmt(self):
            return self.getTypedRuleContext(QExprParser.DefinitionStmtContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)




    def stmt(self):

        localctx = QExprParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_stmt)
        self._la = 0 # Token type
        try:
            self.state = 114
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,5,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 81
                self.expr(0)
                self.state = 82
                self.match(QExprParser.Semicolon)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 84
                self.sepExpr()
                self.state = 85
                self.match(QExprParser.Semicolon)
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 87
                self.assignment()
                self.state = 92
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==29:
                    self.state = 88
                    self.match(QExprParser.Comma)
                    self.state = 89
                    self.assignment()
                    self.state = 94
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 95
                self.match(QExprParser.Semicolon)
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 97
                self.ifStmt()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 98
                self.repeatStmt()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 99
                self.forStmt()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 100
                self.breakLoop()
                self.state = 101
                self.match(QExprParser.Semicolon)
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 103
                self.continueLoop()
                self.state = 104
                self.match(QExprParser.Semicolon)
                pass

            elif la_ == 9:
                self.enterOuterAlt(localctx, 9)
                self.state = 106
                self.halt()
                self.state = 107
                self.match(QExprParser.Semicolon)
                pass

            elif la_ == 10:
                self.enterOuterAlt(localctx, 10)
                self.state = 109
                self.returnStmt()
                self.state = 110
                self.match(QExprParser.Semicolon)
                pass

            elif la_ == 11:
                self.enterOuterAlt(localctx, 11)
                self.state = 112
                self.definitionStmt()
                pass

            elif la_ == 12:
                self.enterOuterAlt(localctx, 12)
                self.state = 113
                self.match(QExprParser.Semicolon)
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
            self.if_false = None # ElseStmtContext

        def expr(self):
            return self.getTypedRuleContext(QExprParser.ExprContext,0)


        def stmts(self):
            return self.getTypedRuleContext(QExprParser.StmtsContext,0)


        def elseStmt(self):
            return self.getTypedRuleContext(QExprParser.ElseStmtContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_ifStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIfStmt" ):
                listener.enterIfStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIfStmt" ):
                listener.exitIfStmt(self)




    def ifStmt(self):

        localctx = QExprParser.IfStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_ifStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            self.match(QExprParser.T__0)
            self.state = 117
            localctx.cond = self.expr(0)
            self.state = 118
            localctx.if_true = self.stmts()
            self.state = 120
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
            if la_ == 1:
                self.state = 119
                localctx.if_false = self.elseStmt()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ElseStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.pipeline = None # StmtsContext

        def stmts(self):
            return self.getTypedRuleContext(QExprParser.StmtsContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_elseStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterElseStmt" ):
                listener.enterElseStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitElseStmt" ):
                listener.exitElseStmt(self)




    def elseStmt(self):

        localctx = QExprParser.ElseStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_elseStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 122
            self.match(QExprParser.T__1)
            self.state = 123
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
            return self.getTypedRuleContext(QExprParser.ExprContext,0)


        def stmts(self):
            return self.getTypedRuleContext(QExprParser.StmtsContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_repeatStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRepeatStmt" ):
                listener.enterRepeatStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRepeatStmt" ):
                listener.exitRepeatStmt(self)




    def repeatStmt(self):

        localctx = QExprParser.RepeatStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_repeatStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 125
            self.match(QExprParser.T__2)
            self.state = 126
            localctx.cond = self.expr(0)
            self.state = 127
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

        def LPar(self):
            return self.getToken(QExprParser.LPar, 0)

        def RPar(self):
            return self.getToken(QExprParser.RPar, 0)

        def assignment(self):
            return self.getTypedRuleContext(QExprParser.AssignmentContext,0)


        def stmts(self):
            return self.getTypedRuleContext(QExprParser.StmtsContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_forStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterForStmt" ):
                listener.enterForStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitForStmt" ):
                listener.exitForStmt(self)




    def forStmt(self):

        localctx = QExprParser.ForStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_forStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 129
            self.match(QExprParser.T__3)
            self.state = 130
            self.match(QExprParser.LPar)
            self.state = 131
            localctx.assign = self.assignment()
            self.state = 132
            self.match(QExprParser.RPar)
            self.state = 133
            localctx.pipeline = self.stmts()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DefinitionStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.name = None # Token

        def stmts(self):
            return self.getTypedRuleContext(QExprParser.StmtsContext,0)


        def SHORTCUT(self):
            return self.getToken(QExprParser.SHORTCUT, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_definitionStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDefinitionStmt" ):
                listener.enterDefinitionStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDefinitionStmt" ):
                listener.exitDefinitionStmt(self)




    def definitionStmt(self):

        localctx = QExprParser.DefinitionStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_definitionStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            localctx.name = self.match(QExprParser.SHORTCUT)
            self.state = 136
            self.stmts()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ReturnStmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.retval = None # ExprContext

        def expr(self):
            return self.getTypedRuleContext(QExprParser.ExprContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_returnStmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturnStmt" ):
                listener.enterReturnStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturnStmt" ):
                listener.exitReturnStmt(self)




    def returnStmt(self):

        localctx = QExprParser.ReturnStmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_returnStmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.match(QExprParser.T__4)
            self.state = 139
            localctx.retval = self.expr(0)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BreakLoopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QExprParser.RULE_breakLoop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBreakLoop" ):
                listener.enterBreakLoop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBreakLoop" ):
                listener.exitBreakLoop(self)




    def breakLoop(self):

        localctx = QExprParser.BreakLoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_breakLoop)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 141
            self.match(QExprParser.T__5)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ContinueLoopContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return QExprParser.RULE_continueLoop

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterContinueLoop" ):
                listener.enterContinueLoop(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitContinueLoop" ):
                listener.exitContinueLoop(self)




    def continueLoop(self):

        localctx = QExprParser.ContinueLoopContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_continueLoop)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            self.match(QExprParser.T__6)
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
            return QExprParser.RULE_halt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterHalt" ):
                listener.enterHalt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitHalt" ):
                listener.exitHalt(self)




    def halt(self):

        localctx = QExprParser.HaltContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_halt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 145
            self.match(QExprParser.T__7)
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
            self.target = None # IdExprContext
            self.val = None # ExprContext

        def Colon(self):
            return self.getToken(QExprParser.Colon, 0)

        def idExpr(self):
            return self.getTypedRuleContext(QExprParser.IdExprContext,0)


        def expr(self):
            return self.getTypedRuleContext(QExprParser.ExprContext,0)


        def Eq(self):
            return self.getToken(QExprParser.Eq, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)




    def assignment(self):

        localctx = QExprParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            localctx.target = self.idExpr(0)
            self.state = 148
            self.match(QExprParser.Colon)
            self.state = 150
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,7,self._ctx)
            if la_ == 1:
                self.state = 149
                self.match(QExprParser.Eq)


            self.state = 152
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
            self.indexer = None # ExprContext
            self.filter_ = None # AssignmentContext

        def LPar(self):
            return self.getToken(QExprParser.LPar, 0)

        def RPar(self):
            return self.getToken(QExprParser.RPar, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(QExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(QExprParser.ExprContext,i)


        def obj(self):
            return self.getTypedRuleContext(QExprParser.ObjContext,0)


        def arr(self):
            return self.getTypedRuleContext(QExprParser.ArrContext,0)


        def func(self):
            return self.getTypedRuleContext(QExprParser.FuncContext,0)


        def value(self):
            return self.getTypedRuleContext(QExprParser.ValueContext,0)


        def asUniOp(self):
            return self.getTypedRuleContext(QExprParser.AsUniOpContext,0)


        def notOp(self):
            return self.getTypedRuleContext(QExprParser.NotOpContext,0)


        def idExpr(self):
            return self.getTypedRuleContext(QExprParser.IdExprContext,0)


        def multiplicativeOp(self):
            return self.getTypedRuleContext(QExprParser.MultiplicativeOpContext,0)


        def additiveOp(self):
            return self.getTypedRuleContext(QExprParser.AdditiveOpContext,0)


        def relationalOp(self):
            return self.getTypedRuleContext(QExprParser.RelationalOpContext,0)


        def andOp(self):
            return self.getTypedRuleContext(QExprParser.AndOpContext,0)


        def orOp(self):
            return self.getTypedRuleContext(QExprParser.OrOpContext,0)


        def joinOp(self):
            return self.getTypedRuleContext(QExprParser.JoinOpContext,0)


        def LBrack(self):
            return self.getToken(QExprParser.LBrack, 0)

        def RBrack(self):
            return self.getToken(QExprParser.RBrack, 0)

        def assignment(self):
            return self.getTypedRuleContext(QExprParser.AssignmentContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = QExprParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 26
        self.enterRecursionRule(localctx, 26, self.RULE_expr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,8,self._ctx)
            if la_ == 1:
                self.state = 155
                self.match(QExprParser.LPar)
                self.state = 156
                localctx.parred = self.expr(0)
                self.state = 157
                self.match(QExprParser.RPar)
                pass

            elif la_ == 2:
                self.state = 159
                self.obj()
                pass

            elif la_ == 3:
                self.state = 160
                self.arr()
                pass

            elif la_ == 4:
                self.state = 161
                self.func()
                pass

            elif la_ == 5:
                self.state = 162
                self.value()
                pass

            elif la_ == 6:
                self.state = 163
                localctx.uniop = self.asUniOp()
                self.state = 164
                localctx.right = self.expr(11)
                pass

            elif la_ == 7:
                self.state = 166
                localctx.notop = self.notOp()
                self.state = 167
                localctx.right = self.expr(7)
                pass

            elif la_ == 8:
                self.state = 169
                self.idExpr(0)
                pass


            self._ctx.stop = self._input.LT(-1)
            self.state = 208
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,10,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 206
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,9,self._ctx)
                    if la_ == 1:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 172
                        if not self.precpred(self._ctx, 10):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 10)")
                        self.state = 173
                        localctx.op1 = self.multiplicativeOp()
                        self.state = 174
                        localctx.right = self.expr(11)
                        pass

                    elif la_ == 2:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 176
                        if not self.precpred(self._ctx, 9):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 9)")
                        self.state = 177
                        localctx.op2 = self.additiveOp()
                        self.state = 178
                        localctx.right = self.expr(10)
                        pass

                    elif la_ == 3:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 180
                        if not self.precpred(self._ctx, 8):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 8)")
                        self.state = 181
                        localctx.op3 = self.relationalOp()
                        self.state = 182
                        localctx.right = self.expr(9)
                        pass

                    elif la_ == 4:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 184
                        if not self.precpred(self._ctx, 6):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 6)")
                        self.state = 185
                        localctx.op4 = self.andOp()
                        self.state = 186
                        localctx.right = self.expr(7)
                        pass

                    elif la_ == 5:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 188
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 189
                        localctx.op5 = self.orOp()
                        self.state = 190
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 6:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 192
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 193
                        localctx.op6 = self.joinOp()
                        self.state = 194
                        localctx.right = self.expr(5)
                        pass

                    elif la_ == 7:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 196
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 197
                        self.match(QExprParser.LBrack)
                        self.state = 198
                        localctx.indexer = self.expr(0)
                        self.state = 199
                        self.match(QExprParser.RBrack)
                        pass

                    elif la_ == 8:
                        localctx = QExprParser.ExprContext(self, _parentctx, _parentState)
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 201
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 202
                        self.match(QExprParser.LBrack)
                        self.state = 203
                        localctx.filter_ = self.assignment()
                        self.state = 204
                        self.match(QExprParser.RBrack)
                        pass

             
                self.state = 210
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,10,self._ctx)

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
            return self.getToken(QExprParser.LBrack, 0)

        def sepExpr(self):
            return self.getTypedRuleContext(QExprParser.SepExprContext,0)


        def RBrack(self):
            return self.getToken(QExprParser.RBrack, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_arr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArr" ):
                listener.enterArr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArr" ):
                listener.exitArr(self)




    def arr(self):

        localctx = QExprParser.ArrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_arr)
        try:
            self.state = 217
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 211
                self.match(QExprParser.LBrack)
                self.state = 212
                self.sepExpr()
                self.state = 213
                self.match(QExprParser.RBrack)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 215
                self.match(QExprParser.LBrack)
                self.state = 216
                self.match(QExprParser.RBrack)
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
            return self.getToken(QExprParser.LPar, 0)

        def RPar(self):
            return self.getToken(QExprParser.RPar, 0)

        def sepExpr(self):
            return self.getTypedRuleContext(QExprParser.SepExprContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_obj

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObj" ):
                listener.enterObj(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObj" ):
                listener.exitObj(self)




    def obj(self):

        localctx = QExprParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
            self.match(QExprParser.LPar)
            self.state = 221
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 281059608428032) != 0):
                self.state = 220
                localctx.val = self.sepExpr()


            self.state = 223
            self.match(QExprParser.RPar)
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
            return self.getToken(QExprParser.LPar, 0)

        def RPar(self):
            return self.getToken(QExprParser.RPar, 0)

        def ID(self):
            return self.getToken(QExprParser.ID, 0)

        def sepExpr(self):
            return self.getTypedRuleContext(QExprParser.SepExprContext,0)


        def SHORTCUT(self):
            return self.getToken(QExprParser.SHORTCUT, 0)

        def value(self):
            return self.getTypedRuleContext(QExprParser.ValueContext,0)


        def idExpr(self):
            return self.getTypedRuleContext(QExprParser.IdExprContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_func

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFunc" ):
                listener.enterFunc(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFunc" ):
                listener.exitFunc(self)




    def func(self):

        localctx = QExprParser.FuncContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_func)
        self._la = 0 # Token type
        try:
            self.state = 236
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                self.enterOuterAlt(localctx, 1)
                self.state = 225
                localctx.func_name = self.match(QExprParser.ID)
                self.state = 226
                self.match(QExprParser.LPar)
                self.state = 228
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 281059608428032) != 0):
                    self.state = 227
                    self.sepExpr()


                self.state = 230
                self.match(QExprParser.RPar)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 231
                localctx.func_name = self.match(QExprParser.SHORTCUT)
                self.state = 234
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [9, 10, 11, 12, 13, 14, 15, 17, 18, 19]:
                    self.state = 232
                    self.value()
                    pass
                elif token in [20, 47]:
                    self.state = 233
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
                return self.getTypedRuleContexts(QExprParser.ExprContext)
            else:
                return self.getTypedRuleContext(QExprParser.ExprContext,i)


        def Comma(self, i:int=None):
            if i is None:
                return self.getTokens(QExprParser.Comma)
            else:
                return self.getToken(QExprParser.Comma, i)

        def getRuleIndex(self):
            return QExprParser.RULE_sepExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSepExpr" ):
                listener.enterSepExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSepExpr" ):
                listener.exitSepExpr(self)




    def sepExpr(self):

        localctx = QExprParser.SepExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_sepExpr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 238
            self.expr(0)
            self.state = 243
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==29:
                self.state = 239
                self.match(QExprParser.Comma)
                self.state = 240
                self.expr(0)
                self.state = 245
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
            return self.getToken(QExprParser.ID, 0)

        def Dollar(self):
            return self.getToken(QExprParser.Dollar, 0)

        def idExpr(self):
            return self.getTypedRuleContext(QExprParser.IdExprContext,0)


        def Dot(self):
            return self.getToken(QExprParser.Dot, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_idExpr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIdExpr" ):
                listener.enterIdExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIdExpr" ):
                listener.exitIdExpr(self)



    def idExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = QExprParser.IdExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 36
        self.enterRecursionRule(localctx, 36, self.RULE_idExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 250
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [20]:
                self.state = 247
                self.match(QExprParser.ID)
                pass
            elif token in [47]:
                self.state = 248
                self.match(QExprParser.Dollar)
                self.state = 249
                self.idExpr(2)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 257
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = QExprParser.IdExprContext(self, _parentctx, _parentState)
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_idExpr)
                    self.state = 252
                    if not self.precpred(self._ctx, 1):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                    self.state = 253
                    self.match(QExprParser.Dot)
                    self.state = 254
                    self.match(QExprParser.ID) 
                self.state = 259
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

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
            return self.getToken(QExprParser.STRING, 0)

        def REGEX(self):
            return self.getToken(QExprParser.REGEX, 0)

        def DATETIME(self):
            return self.getToken(QExprParser.DATETIME, 0)

        def TIME_INTERVAL(self):
            return self.getToken(QExprParser.TIME_INTERVAL, 0)

        def NUMBER(self):
            return self.getToken(QExprParser.NUMBER, 0)

        def SHORTCUT(self):
            return self.getToken(QExprParser.SHORTCUT, 0)

        def OBJECT_ID(self):
            return self.getToken(QExprParser.OBJECT_ID, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)




    def value(self):

        localctx = QExprParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_value)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 260
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 982528) != 0)):
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
            return self.getToken(QExprParser.Join, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_joinOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJoinOp" ):
                listener.enterJoinOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJoinOp" ):
                listener.exitJoinOp(self)




    def joinOp(self):

        localctx = QExprParser.JoinOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_joinOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 262
            self.match(QExprParser.Join)
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
            return self.getToken(QExprParser.And, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_andOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAndOp" ):
                listener.enterAndOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAndOp" ):
                listener.exitAndOp(self)




    def andOp(self):

        localctx = QExprParser.AndOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_andOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 264
            self.match(QExprParser.And)
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
            return self.getToken(QExprParser.Or, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_orOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOrOp" ):
                listener.enterOrOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOrOp" ):
                listener.exitOrOp(self)




    def orOp(self):

        localctx = QExprParser.OrOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_orOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 266
            self.match(QExprParser.Or)
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
            return self.getToken(QExprParser.Star, 0)

        def Div(self):
            return self.getToken(QExprParser.Div, 0)

        def Dot(self):
            return self.getToken(QExprParser.Dot, 0)

        def Mod(self):
            return self.getToken(QExprParser.Mod, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_multiplicativeOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterMultiplicativeOp" ):
                listener.enterMultiplicativeOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitMultiplicativeOp" ):
                listener.exitMultiplicativeOp(self)




    def multiplicativeOp(self):

        localctx = QExprParser.MultiplicativeOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_multiplicativeOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 268
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 128849018880) != 0)):
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
            return self.getToken(QExprParser.Plus, 0)

        def Minus(self):
            return self.getToken(QExprParser.Minus, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_additiveOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAdditiveOp" ):
                listener.enterAdditiveOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAdditiveOp" ):
                listener.exitAdditiveOp(self)




    def additiveOp(self):

        localctx = QExprParser.AdditiveOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_additiveOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 270
            _la = self._input.LA(1)
            if not(_la==30 or _la==32):
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
            return self.getToken(QExprParser.Gt, 0)

        def Lt(self):
            return self.getToken(QExprParser.Lt, 0)

        def Gte(self):
            return self.getToken(QExprParser.Gte, 0)

        def Lte(self):
            return self.getToken(QExprParser.Lte, 0)

        def Ne(self):
            return self.getToken(QExprParser.Ne, 0)

        def Eq(self):
            return self.getToken(QExprParser.Eq, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_relationalOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRelationalOp" ):
                listener.enterRelationalOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRelationalOp" ):
                listener.exitRelationalOp(self)




    def relationalOp(self):

        localctx = QExprParser.RelationalOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_relationalOp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 272
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 34634616274944) != 0)):
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
            return self.getTypedRuleContext(QExprParser.NotOpContext,0)


        def Search(self):
            return self.getToken(QExprParser.Search, 0)

        def Minus(self):
            return self.getToken(QExprParser.Minus, 0)

        def Plus(self):
            return self.getToken(QExprParser.Plus, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_uniOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterUniOp" ):
                listener.enterUniOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitUniOp" ):
                listener.exitUniOp(self)




    def uniOp(self):

        localctx = QExprParser.UniOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_uniOp)
        try:
            self.state = 278
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [46]:
                self.enterOuterAlt(localctx, 1)
                self.state = 274
                self.notOp()
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 2)
                self.state = 275
                self.match(QExprParser.Search)
                pass
            elif token in [32]:
                self.enterOuterAlt(localctx, 3)
                self.state = 276
                self.match(QExprParser.Minus)
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 4)
                self.state = 277
                self.match(QExprParser.Plus)
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
            return self.getTypedRuleContext(QExprParser.MultiplicativeOpContext,0)


        def additiveOp(self):
            return self.getTypedRuleContext(QExprParser.AdditiveOpContext,0)


        def relationalOp(self):
            return self.getTypedRuleContext(QExprParser.RelationalOpContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_binOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinOp" ):
                listener.enterBinOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinOp" ):
                listener.exitBinOp(self)




    def binOp(self):

        localctx = QExprParser.BinOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_binOp)
        try:
            self.state = 283
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [33, 34, 35, 36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 280
                self.multiplicativeOp()
                pass
            elif token in [30, 32]:
                self.enterOuterAlt(localctx, 2)
                self.state = 281
                self.additiveOp()
                pass
            elif token in [39, 40, 41, 42, 43, 44]:
                self.enterOuterAlt(localctx, 3)
                self.state = 282
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
            return self.getToken(QExprParser.Tilde, 0)

        def getRuleIndex(self):
            return QExprParser.RULE_notOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNotOp" ):
                listener.enterNotOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNotOp" ):
                listener.exitNotOp(self)




    def notOp(self):

        localctx = QExprParser.NotOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_notOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 285
            self.match(QExprParser.Tilde)
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
            return self.getTypedRuleContext(QExprParser.UniOpContext,0)


        def binOp(self):
            return self.getTypedRuleContext(QExprParser.BinOpContext,0)


        def getRuleIndex(self):
            return QExprParser.RULE_asUniOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAsUniOp" ):
                listener.enterAsUniOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAsUniOp" ):
                listener.exitAsUniOp(self)




    def asUniOp(self):

        localctx = QExprParser.AsUniOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_asUniOp)
        try:
            self.state = 289
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,21,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 287
                self.uniOp()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 288
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
        self._predicates[13] = self.expr_sempred
        self._predicates[18] = self.idExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 10)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 9)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 8)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 6)
         

            if predIndex == 4:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 5:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 6:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 7:
                return self.precpred(self._ctx, 2)
         

    def idExpr_sempred(self, localctx:IdExprContext, predIndex:int):
            if predIndex == 8:
                return self.precpred(self._ctx, 1)
         




