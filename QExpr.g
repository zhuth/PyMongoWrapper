grammar QExpr;

snippet: stmt+ | stmts | expr | sepExpr;

stmts: stmt | LBrace stmt* RBrace;

stmt:
	expr Semicolon
	| sepExpr Semicolon
	| assignment (Comma assignment)* Semicolon
	| ifStmt
	| repeatStmt
	| forStmt
	| breakLoop Semicolon
	| continueLoop Semicolon
	| halt Semicolon
	| returnStmt Semicolon
	| definitionStmt
	| Semicolon;

ifStmt: 'if' cond = expr if_true = stmts if_false = elseStmt?;

elseStmt: 'else' pipeline = stmts;

repeatStmt: 'repeat' cond = expr pipeline = stmts;

forStmt: 'for' LPar assign = assignment RPar pipeline = stmts;

definitionStmt: name = SHORTCUT stmts;

returnStmt: 'return' retval = expr;

breakLoop: 'break';

continueLoop: 'continue';

halt: 'halt';

assignment: target = idExpr Colon Eq? val = expr;

SHORTCUT: Colon ID;

expr:
	LPar parred = expr RPar
	| obj
	| arr
	| func
	| value
	| uniop = asUniOp right = expr
	| left = expr op1 = multiplicativeOp right = expr
	| left = expr op2 = additiveOp right = expr
	| left = expr op3 = relationalOp right = expr
	| notop = notOp right = expr
	| left = expr op4 = andOp right = expr
	| left = expr op5 = orOp right = expr
	| left = expr op6 = joinOp right = expr
	| left = expr LBrack Plus arrayIndexer = expr RBrack
	| left = expr LBrack indexer = expr RBrack
	| left = expr LBrack filter = assignment RBrack
	| field = idExpr Eq stmts
	| idExpr;
	
arr: LBrack sepExpr RBrack | LBrack RBrack;

obj: LPar val = sepExpr? RPar;

func: func_name = ID LPar sepExpr? RPar | func_name = SHORTCUT (value|idExpr);

sepExpr: expr (Comma expr)*;

idExpr:
	ID
	| Dollar idExpr
	| idExpr Dot ID;

value:
	'true'
	| 'false'
	| 'null'
	| STRING
	| REGEX
	| DATETIME
	| TIME_INTERVAL
	| NUMBER
	| SHORTCUT
	| OBJECT_ID;

// operators
joinOp: Join;
andOp: And;
orOp: Or;
multiplicativeOp: Star | Div | Dot | Mod;
additiveOp: Plus | Minus;
relationalOp: Gt | Lt | Gte | Lte | Ne | Eq;
uniOp: notOp | Search | Minus | Plus;
binOp: multiplicativeOp | additiveOp | relationalOp;
notOp: Tilde;
asUniOp: uniOp | binOp;

// LEXICON

STRING:
	'"' (ESC | SAFECODEPOINT)*? '"'
	| '\'' (ESC | SAFECODEPOINT)*? '\''
	| '`' .*? '`';

REGEX:
	STRING [imsxc]*;

fragment ESC: '\\' (["'\\/bfnrt] | UNICODE | HEXCODE);
fragment UNICODE: 'u' HEX HEX HEX HEX;
fragment HEXCODE: 'x' HEX HEX;
fragment HEX: [0-9a-fA-F];
fragment SAFECODEPOINT: ~ ["\\\u0000-\u001F];

NUMBER: INT ('.' INT)? EXP?;

fragment INT: [0-9]+;

fragment EXP: [Ee] [+\-]? INT;

fragment HOUR: [01]? [0-9] | '2' [0-3];

fragment MS60: [0-5][0-9];

TIME: HOUR ':' MS60 (':' MS60)?;

TIME_INTERVAL: NUMBER [dmywhis];

DATETIME: 'd' STRING;

OBJECT_ID: 'o' STRING;

ID: ALPHABETICS ([0-9] | ALPHABETICS)*;

fragment ALPHABETICS: [#@a-zA-Z_\u0080-\uFFFF];

Colon: ':';

Semicolon: ';';

LBrace: '{';

RBrace: '}';

LPar: '(';

RPar: ')';

LBrack: '[';

RBrack: ']';

Comma: ',';

Plus: '+';
Join: '=>';
Minus: '-';
Star: '*';
Div: '/';
Mod: '%';
Dot: '.';
And: '&';
Or: '|';

Gt: '>';
Lt: '<';
Gte: '>=';
Lte: '<=';
Ne: '!=';
Eq: '=';

Search: '%%';
Tilde: '~';

Dollar: '$';

WS: [ \t\n\r]+ -> skip;

COMMENT: '/*' .*? '*/' -> skip;

LINE_COMMENT: '//' ~[\r\n]* -> skip;