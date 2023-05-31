# The QExpr Language

QExpr (abbreviated as QX) is a programming language designed for expressing queries and transformations on structured data. It provides a flexible and concise syntax for working with various data types, including objects, arrays, functions, and more. This README provides an overview of the QExpr programming language and its grammar as defined in the ANTLR file.
## Conventions

### IDs

In QExpr, all references to `id` will be interpreted as `_id`. For example, `group(id=$name)` means the same for `group(_id=$name)`, and `sort(image.id)` is the same with `sort(image._id)`.

### The Leading `$` Symbol

In the QExpr language, the `$` symbol is used as a prefix to indicate the value of a field or variable. Conversely, the field or variable name without the leading `$` is used for assigning a value to it. This convention is similar to the original query language of MongoDB. Here's an example to illustrate the usage:

```qexpr
age = 30;        // Assigning a value of 30 to the variable "age"

if ($age > 50) { // Accessing the value for comparison
    ...
}
```

In this example, the variable (or field) `age` is assigned without the `$` symbol. When referencing `age` for comparison, the `$` symbol is used to indicate that we want to access its value.

The usage of the `$` symbol in QExpr follows the convention of the MongoDB query language, where it is used to access field values in queries and updates. This convention helps differentiate between assigning values to fields/variables and referencing their values within the query context.

### The Ending `@` Symbol

There are two ways to use a shortcut or user-defined function in QExpr. One is to parse it as part of a query, and the other is to call it during runtime. For example:

```qexpr
:foo {
    match(age > 20);
}
```

The QExpr expression `foo()` will be parsed as a part of a MongoDB query:

```javascript
{
    $match: {
        age: {
            $gt: 20
        }
    }
}
```

However, if we need to call it at runtime, we should use `foo@()` instead. Since there is no `return` statement in `foo`, it won't provide any output.

## Grammar

The QExpr programming language follows the grammar defined in the `QueryExpr.g` ANTLR file. Here is a summary of the grammar rules:

### Statements

- `stmts`: Represents one or more statements. It can be a single `stmt` or a block of statements enclosed in braces `{}`.
- `stmt`: Represents different types of statements, including expressions, assignments, control flow statements, and more.

### Control Flow Statements

- `if`: Represents an if statement with a condition expression and optional blocks for the true branch (`if_true`) and the false branch (`if_false`).
- `else`: Represents the else branch of an if statement, consisting of a pipeline of statements.
- `repeat`: Represents a repeat statement with a condition expression and a pipeline of statements to repeat.
- `for`: Represents a for statement with an assignment expression, followed by a pipeline of statements to execute.
- `break`: Represents a break statement to exit a loop or switch statement.
- `continue`: Represents a continue statement to skip the current iteration of a loop.
- `halt`: Represents a halt statement to terminate the program.
- `return`: Represents a return statement with a mandatory return value expression. To return nothing, explicitly specify `return null;`.
- Assignment: Represents assigning a value to a variable or a field.
- Definition statement: Represents defining a name (shortcut) and a pipeline of statements associated with it.

### Example for `if`:

```qexpr
if ($score > 90) {
    comment := "Excellent!";
}
```

In this example, the `if` statement checks if the `$score` variable is greater than 90. If the condition is true, it executes the block of statements within the curly braces. Since there is no `else` block, no statements are executed if the condition is false.

Note: `()` in `if` is optional. In other words, you can write it

 as:

```qexpr
if $score > 90 {
    comment := "Excellent!";
}
```

### Example for `repeat` loop:

```qexpr
count = 10;
repeat ($count > 0) {
    print("Hello");
    count = $count - 1;
}
```

In this example, the `repeat` statement repeatedly executes the block of statements as long as the condition `$count > 0` is true. It prints "Hello" and updates the `count` variable in each iteration. Similarly, `()` in the `repeat` statement is optional.

### Example for `for` loop:

```qexpr
for (img := $images) {
    doSomething($img);
}
```

In this example, the `for` statement initializes the `img` variable to iterate through an array `$images`. It continues executing the block of statements to perform some action with `$img`. Notice that `()` is _not_ optional here.

You can use `break` and `continue` in `for` and `repeat` loops.

### Example for user function definition:

```qexpr
:shortcut {
    if ($arg > 10) return 10;
    if ($arg < 0) return 0;
    return $arg;
}
```

In this example, we define a user function called `shortcut` to limit the value between 0 and 10 inclusively. We can call it in the following manner:

```qexpr
shortcut(22); // returns 10
shortcut(-1); // returns 0
shortcut(2);  // returns 2
```

The variable `$arg` represents the argument value passed to the function. If the function is called with a list of parameters, like `foo(1, 2, 3, 4)`, you can access them using `$arg.0`, `$arg.1`, `$arg.2`, and `$arg.3`. If the function is called with key-value pairs, you can access them using `$arg.key`. Note that since there are no global variables, you can always use `$ctx` to store globally shared values. However, be aware that your access to `$ctx` is not thread-safe, which can be an issue when executing QExpr in parallel calls. Also, `return` is only used in function definitions.

### Expressions

- `expr`: Represents various types of expressions, including literals, object and array literals, function calls, unary and binary operations, and more.
- `arr`: Represents an array literal enclosed in square brackets `[]`.
- `obj`: Represents an object literal enclosed in parentheses `()`.
- `func`: Represents a function call expression, either by name or using a defined name (shortcut).
- `sepExpr`: Represents a sequence of expressions separated by commas.

### Identifiers and Values

- `idExpr`: Represents an identifier, which can be a simple name or a sequence of identifiers separated by dots.
- `value`: Represents different types of literal values, including boolean values, strings, regular expressions, numbers, shortcuts, object IDs, and more.

### Operators

QExpr supports various operators for different operations:

- Join: `=>` (concatenating arrays)
- Logical: `&` (and `,` in contexts other than function calls), `|`
- Arithmetic: `*`, `/`, `.`, `+`, `-`
- Strings: `%` (matching regular expression)
- Relational: `>`, `<`, `>=`, `<=`, `!=`, `=`
- Unary: `!`, `%%`, `-`, `+`

## Lexicon

QueryExpr defines a set of lexical rules for parsing the source code:

- Strings: Double-quoted, single-quoted, and backtick-quoted strings.
- Regular Expressions: Enclosed in forward slashes with optional flags.
- Numbers: Integer and floating-point numbers, including exponential notation.
- Time and Date: Time, time intervals, and date literals.
- Object ID: A unique identifier for objects.
- Identifiers: Names used to represent variables, functions, and shortcuts.
- Punctuation: Various punctuation marks used for syntax, such as colons, semicolons, braces, parentheses, brackets, commas, and more.


### Literals

In QExpr, there are several types of literals that you can use. Here is an introduction to the different types of literals available:

1. Boolean Literals: The boolean literals in QExpr are `true` and `false`. They represent the logical values of true and false, respectively.

2. String Literals: QExpr supports string literals, which are sequences of characters enclosed in double quotes (`"`) or single quotes (`'`). For example: `"Hello, World!"`, `'QExpr'`.

3. Regular Expression Literals: Regular expression literals in QExpr are represented between forward slashes (`/`). They allow you to define patterns for pattern matching and manipulation. For example: `/[A-Za-z]+/` matches one or more alphabetic characters.

4. Number Literals: QExpr supports numeric literals, including integer and floating-point numbers. For example: `42`, `3.14`, `1e-5`.

5. Shortcut Literals: Shortcuts are identifiers that can be defined and associated with a block of statements. You can refer to a shortcut using its name. For example: `myShortcut`, `someName`.

6. Object ID Literals: Object ID literals start with the letter 'o' followed by a 24-bytes hexadecimal literal. They represent unique identifiers for objects. For example: `o"647712410062448e086da729"`.

7. Date and Time Literals: QExpr provides literals for representing date and time values. Examples include:
   - Date literal: `d"2022-01-01"` represents a specific date.
   - Time literal: `12:34:56` represents a specific time.
   - Time interval literal: `3d` represents a time interval of 3 days.

8. Null Literal: The null literal in QExpr is `null`. It represents the absence of a value or a null reference.

These literals allow you to work with different types of values in QExpr programs. You can use them in expressions, assignments, function calls, and more, depending on the context and requirements of your program.


### Undetermined Strings

In QExpr, strings can be unquoted, given that:

- They do not conflict with keywords, such as `for`, `continue`, etc.
- They are not in the form of any other literals, like numbers. For instance, `100` should not be confused with `"100"`.
- They do not contain punctuations (with the only exceptions of `#`, `_`, and `@`) or spaces.


## Buit-in Functions

The built-in functions can be regarded as macros in C/C++. The will be expanded into native MongoDB functions.

1. `empty(param='')`: Checks if the given parameter is empty. It returns `True` if the parameter is an empty string (`''`), an empty binary (`Binary(b'')`), or `None`, and `False` otherwise.

2. `json(x)`: Converts the given value `x` into a JSON object. It uses the `json.loads()` function to parse the string representation of `x` into a JSON object.

3. `objectId(x)`: Converts the given value `x` into a MongoDB ObjectId. If `x` is a numeric value (int or float), it treats it as a Unix timestamp and converts it to a `datetime.datetime` object. If `x` is already a `datetime.datetime` object, it converts it to an ObjectId. Otherwise, it assumes `x` is a string representation of an ObjectId and converts it to an ObjectId.

4. `binData(x)`: Converts the given value `x` into a MongoDB Binary object. If `x` is a string, it decodes it from base64 to binary before creating the Binary object.

5. `now(param='')`: Returns the current UTC datetime. If a parameter is provided and it is a `datetime.timedelta` object, it adds the timedelta to the current datetime before returning it.

6. `sort(*sortstrs, **params)`: Constructs a MongoDB sort parameter based on the provided sort strings (`sortstrs`) and additional keyword arguments (`params`). The sort strings represent the sorting order for different fields. If a sort string starts with a minus sign (`-`), it represents descending order. The function returns a MongoDB sort parameter that can be used in a query.

7. `sorted(input, by=1)`: Sorts the input array (`input`) based on the specified sorting criteria (`by`). The sorting criteria can be provided as a string or a dictionary. If `by` is a string, it is parsed into a dictionary representing the sorting order. The function returns the sorted array.

8. `join(field)`: Concatenates the values of the specified field across documents in the collection. The field name is provided as an argument (`field`). The function adds a field to each document that contains the concatenated values and returns the modified documents.

9. `strJoin(input, delimiter=' ')`: Joins the values in the input array (`input`) into a string using the specified delimiter (`delimiter`). The function returns the resulting string.

10. `sample(size)`: Returns a random sample of documents from the collection. The number of documents in the sample is determined by the `size` parameter.

11. `replaceRoot(newroot='', **obj)`: Replaces the root document with a new root document or an object. If a new root document is specified (`newroot`), it replaces the root document with it. Otherwise, if an object is specified as keyword arguments (`obj`), it replaces the root document with the object.

12. `group(id, **params)`: Groups the documents based on the specified grouping criteria (`id`) and additional aggregation parameters (`params`). The `id` parameter represents the grouping key(s) and can be a string or a dictionary. The function returns the grouped documents.

13. `filter(input, cond, as='this')`: Filters the input array (`input`) based on the provided condition (`cond`). The condition is specified as an expression, and the filtered array is assigned to the specified variable (`as`, defaulting to `'this'`). The function returns the filtered array.

14. `match(*ands, **params)`: Constructs a MongoDB `$match` stage based on the provided conditions (`ands`) and additional parameters (`params`). The conditions can be combined using logical operators like `$and`, `$or`, and `$text`. The function returns the `$match` stage.

15. `replaceOne(input, find, replacement)`: Replaces the first occurrence of the specified string (`find`) in the input string (`input`) with the replacement string (`replacement`). The function returns the modified string.

16. `replaceAll(input, find, replacement)`: Replaces all occurrences of the specified string (`find`) in the input string (`input`) with the replacement string (`replacement`). The function returns the modified string.

17. `bytes`: A reference to the `bytes.fromhex` function, which converts a hexadecimal string to a `bytes` object.

18. `let`: An alias to `addFields`/`set`/assignment.

19. `F(string)`: Constructs a `MongoField` object based on the specified string. The `MongoField` object represents a field in a MongoDB query.

## Usage

The interpreter (parser) is defined in class `QExprInterpreter`. Here are some examples for how to use it.

```python
# Create an instance of QExprInterpreter
interpreter = QExprInterpreter()

# Example 1: Tokenize an expression
expression = 'age > 30'
tokens = interpreter.tokenize(expression)
print(tokens)
# Output: [Token(age, 'age'), Token(>, '>'), Token(30, '30')]

# Example 2: Get a string representation of tokens
expression = 'age > 30'
tokens = interpreter.tokenize(expression)
tokens_string = interpreter.get_tokens_string(tokens)
print(tokens_string)
# Output: 'age/VARIABLE >/> 30/NUMBER'


# Example 3: Parse an expression
expression = 'age > 30'
result = interpreter.parse(expression)
print(result)
# Output: {'$gt': [{'$var': 'age'}, 30]}

# Example 4: Parse a literal value
expression = '40'
result = interpreter.parse_literal(expression)
print(result)
# Output: 40

# Create an instance of QExprInterpreter with default field and operator
interpreter2 = QExprInterpreter('content', '%')
result = interpreter2.parse('hello')
print(result)
# Output: {'content': {'$regex': 'hello'}}
```

The evaluator is defined in class `QExprEvaluator`. Here are some examples for how to use it.

```python
# Create an instance of QExprEvaluator
evaluator = QExprEvaluator()

# Example 1: Register a python function
@evaluator.function(mapping={'a': 'param1', 'b': 'param2'})
def add_div_2(a, b):
    return (a + b) / 2

# Example 2: Execute statements
statements = interpreter.parse('addDiv2($param1, $param2);') # Function name is automatically converted into camelCase. Also, notice the ending comma `;`.
result = evaluator.execute(statements, {'param1': 2, 'param2': 3})
print(result)
# Output: None

# Example 3: Evaluate an expression
statements = interpreter.parse('addDiv2($param1, $param2)') # No ending comma
result = evaluator.evaluate(statements, {'param1': 2, 'param2': 3})
print(result)
# Output: 2.5
```
