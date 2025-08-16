# Getting Started with C Language: Day 2 - The Program's Intelligent Decision System

Conditional statements are the core tools in the C language for implementing program logic decisions. They enable programs to make intelligent choices based on different conditions, much like traffic signals guide the direction of vehicles. Through these statements, programs can select the most appropriate execution path based on input data or runtime status, thereby achieving more complex and flexible functionality. This article systematically explains the branching control structures in C language, helping you master the program's "thinking" capability.

## `if` Statement: Basic Conditional Judgment

The `if` statement is the most fundamental conditional control structure in C, used to determine whether to execute specific code blocks based on the result of a conditional expression. In C language, **any non-zero value is considered "true," while zero is considered "false"**—this differs from boolean types in many modern languages.

### Syntax Structure

```c
if (conditional expression) {
    // Code executed when condition is true
}
```

- **Conditional expression**: Can be relational expressions (e.g., `x > 0`), logical expressions (e.g., `a && b`), or any expression that evaluates to an integer value
- **Code block**: A set of statements enclosed in curly braces `{}`, executed when the condition is true

### Example Analysis

```c
#include <stdio.h>

int main() {
    int score = 85;
    
    if (score >= 60) {
        printf("Congratulations! You have passed the exam.\n");
        printf("Score: %d points\n", score);
    }
    
    return 0;
}
```

In this example, `score >= 60` evaluates to 1 (true), so both `printf` statements execute. If `score` were changed to 55, the conditional expression would evaluate to 0 (false), and the entire code block would be skipped.

> **Key Tip**: C language lacks a native boolean type (prior to C99), with conditional judgments based on integer values. `true` and `false` are actually macro definitions (in `stdbool.h`), fundamentally representing integers 1 and 0.

## `if-else` Statement: Binary Decision Making

When choosing between two mutually exclusive scenarios, the `if-else` structure provides complete condition coverage, ensuring one path is always executed.

### Syntax Structure

```c
if (conditional expression) {
    // Code executed when condition is true
} else {
    // Code executed when condition is false
}
```

### Example Analysis

```c
#include <stdio.h>

int main() {
    int temperature = 28;
    
    if (temperature > 30) {
        printf("Weather is hot, recommended to stay indoors.\n");
    } else {
        printf("Weather is pleasant, suitable for outdoor activities.\n");
    }
    
    return 0;
}
```

In this example, since `temperature` is 28 (not greater than 30), the program executes the `else` branch. Note: The code blocks of `if` and `else` are mutually exclusive—only one will execute.

## `else if` Chain: Multi-level Conditional Judgment

When facing multiple mutually exclusive conditions, the `else if` chain provides a clear hierarchical judgment structure. The program **checks conditions from top to bottom**, executing the first matching branch and then exiting the entire structure.

### Syntax Structure

```c
if (condition1) {
    // Execute when condition1 is true
} else if (condition2) {
    // Execute when condition1 is false but condition2 is true
} else if (condition3) {
    // Execute when first two conditions are false but condition3 is true
} else {
    // Execute when all conditions are false
}
```

### Example Analysis

```c
#include <stdio.h>

int main() {
    int score = 75;
    
    if (score >= 90) {
        printf("Excellent (A)\n");
    } else if (score >= 80) {
        printf("Good (B)\n");
    } else if (score >= 70) {
        printf("Average (C)\n");
    } else if (score >= 60) {
        printf("Pass (D)\n");
    } else {
        printf("Fail (F)\n");
    }
    
    return 0;
}
```

The program checks score ranges sequentially. 75 satisfies `score >= 70` but not `score >= 80`, so it outputs "Average (C)". **Condition order is crucial**—placing `score >= 70` before `score >= 80` would cause logical errors.

## `switch` Statement: Multi-way Branch Selection

When branching based on **different values of a single expression**, the `switch` statement is clearer and more efficient than multiple `else if` statements. It's particularly suitable for handling discrete values (such as menu options, status codes, etc.).

### Syntax Structure

```c
switch (expression) {
    case constant1:
        // Execute when expression equals constant1
        break;
    case constant2:
        // Execute when expression equals constant2
        break;
    // More cases can be added
    default:
        // Execute when no case matches
}
```

- **Expression**: Must be of integer or character type (including enumerations)
- **Case labels**: Must be integer constant expressions (cannot be variables or ranges)
- **break statement**: Used to exit the `switch` structure, preventing "fall-through" behavior
- **default branch**: Recommended to always include for code robustness

### Example Analysis

```c
#include <stdio.h>

int main() {
    char grade = 'B';
    
    switch (grade) {
        case 'A':
            printf("90-100 points: Excellent\n");
            break;
        case 'B':
            printf("80-89 points: Good\n");
            break;
        case 'C':
            printf("70-79 points: Average\n");
            break;
        case 'D':
            printf("60-69 points: Pass\n");
            break;
        case 'F':
            printf("<60 points: Fail\n");
            break;
        default:
            printf("Invalid grade\n");
    }
    
    return 0;
}
```

In this example, `grade` is 'B', so the program executes the corresponding `case 'B'` branch and outputs "80-89 points: Good". **Note**: The `break` after each `case` is crucial—omitting it causes the program to continue executing subsequent `case` code.

## Nested Branching: Handling Compound Conditions

In practical programming, multiple conditional judgments often need to be combined. C allows nesting other branching structures within conditional statements, but excessive nesting (typically more than 3 levels) should be avoided to maintain code readability.

### Example: Nested if Structure

```c
#include <stdio.h>

int main() {
    int age = 25;
    int hasLicense = 1;  // 1 means has driver's license
    
    if (age >= 18) {
        if (hasLicense) {
            printf("You are an adult with a license, legally allowed to drive.\n");
        } else {
            printf("You are an adult but without a license, cannot drive.\n");
        }
    } else {
        printf("You are underage, cannot apply for a license.\n");
    }
    
    return 0;
}
```

This example demonstrates first checking age, then making further judgments based on license status. **Key technique**: Use indentation to clearly show nesting levels, with each level indented by 4 spaces.

## Common Pitfalls and Best Practices

### 1. Scenarios Where Braces Are Mandatory

Even when a code block contains only one statement, **it's strongly recommended to always use braces**:

```c
// Error example: Missing braces causing logical error
if (x > 0)
    printf("x is positive\n");
    printf("This statement always executes!\n");  // Actually outside if block

// Correct implementation
if (x > 0) {
    printf("x is positive\n");
    printf("This statement executes only when x>0\n");
}
```

### 2. The "Fall-through" Phenomenon in switch

The `break` in `switch` is not optional—omitting it causes unexpected "fall-through" behavior:

```c
// Intentional fall-through example (must be clearly commented)
switch (month) {
    case 4: case 6: case 9: case 11:
        printf("This month has 30 days\n");
        break;
    case 2:
        printf("February usually has 28 days\n");
        // Intentionally omitting break to continue execution
    default:
        printf("This month has 31 days\n");
}
```

> **Best Practice**: Unless fall-through is explicitly needed, each `case` should end with `break`, with comments explaining the intentional fall-through.

## Advanced Techniques

### 1. Ternary Operator: Simplifying Simple Conditions

For simple binary choices, the ternary operator `?:` can make code more concise:

```c
#include <stdio.h>

int main() {
    int num = 10;
    // Traditional if-else
    if (num % 2 == 0) {
        printf("%d is even\n", num);
    } else {
        printf("%d is odd\n", num);
    }
    
    // Equivalent ternary operator implementation
    printf("%d is %s number\n", num, (num % 2 == 0) ? "even" : "odd");
    
    return 0;
}
```

> **Appropriate Use**: Only use when logic is very simple; avoid nested ternary operators that reduce readability.

### 2. Perfect Combination of Enumerations and switch

Using enumeration types with `switch` statements significantly improves code readability and maintainability:

```c
#include <stdio.h>

typedef enum { 
    MONDAY, TUESDAY, WEDNESDAY, 
    THURSDAY, FRIDAY, SATURDAY, SUNDAY 
} Weekday;

int main() {
    Weekday today = WEDNESDAY;
    
    switch (today) {
        case MONDAY:    printf("Monday: New week begins\n"); break;
        case TUESDAY:   printf("Tuesday: Getting into the groove\n"); break;
        case WEDNESDAY: printf("Wednesday: Halfway through work\n"); break;
        case THURSDAY:  printf("Thursday: Weekend approaching\n"); break;
        case FRIDAY:    printf("Friday: Preparing for the weekend\n"); break;
        case SATURDAY:  printf("Saturday: Enjoying leisure time\n"); break;
        case SUNDAY:    printf("Sunday: Adjusting for the new week\n"); break;
        default:        printf("Invalid day\n");
    }
    
    return 0;
}
```

## Summary and Reflection

Conditional statements are the cornerstone of intelligent decision-making in programs. Through this lesson, you should have mastered:

1. **Basic Structures**: Correct usage of `if`, `if-else`, `else if` chains, and `switch`
2. **Key Details**: Conditional judgments in C are based on integer values; `break` in `switch` is essential
3. **Best Practices**: Always use braces, organize condition order logically, avoid excessive nesting
4. **Advanced Techniques**: Appropriate use of ternary operators, combining enumerations with `switch`

> **Programming Wisdom**: Excellent conditional logic design should be as clear and unambiguous as traffic signs—each branch has explicit conditions with no ambiguity or missing paths. Remember, code readability is often more important than short-term writing speed.

**Practice Suggestion**: Try writing a program that outputs the number of days in a month based on user-input year and month (considering leap year rules). This will comprehensively apply your knowledge of branching control!
