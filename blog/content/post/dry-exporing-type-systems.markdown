---
categories: software
description: Exploring some software fundamentals
featured_image: covers/python-1.png
author: Anders
title: "DRY Series: Exploring Dynamic and Static type systems"
date: "2019-12-22"
layout: post
series: ["DRY Series"]
tags: ['basics', 'software', 'concept', 'python']
---

![Type systems header](/images/anim/typesystems_header.gif)

Type systems are inherent to every programming language, and determines a large part of the nature of how to use the programming language.  It is an important part of the programming language to understand, and full mastery brings many advantages for experienced programmers. The type system is often a double edged sword, and is a big reason for why there exists so many programming languages.

### Dynamic Python

Python is a programming language which is great for data processing. Its also great for a lot of other purposes, like scripting and web development. When working in enterprises and large codebases, it can be useful to create central repositories for code, which can be shared to other applications and adhere to the DRY principle.  Due to python dynamic nature, we can get added benefits when working with these libraries.

When it is said that python is a fun and silly language, or toy language, or something like that - it is often referred to the way python handles types. Everything in python can be treated as an object, and since it is duck typed, we can do some things which are quirky, but lets us avoid a lot of boilerplate or save a lot of time on occasions by abusing types in python

#### Lets look at a few examples

A basic example is that we can patch in things in libraries:

```python
>>> import datetime
>>> datetime.addnums = lambda x,y: x + y
>>> datetime.addnums(2,5)
7
```

Need to run some code before and after a function? Closure

```python
>>> def myfunc():
...     print('I am the original function')
...
>>> def wrapfunc(func):
...     def inner_func(*args, **kw):
...             print('wrapping func')
...             func(*args, **kw)
...             print('successfully wrapped func')
...     return inner_func
...
>>> myfunc()
I am the original function
>>> myfunc = wrapfunc(myfunc)
>>> myfunc()
wrapping func
I am the original function
successfully wrapped func
```

This ^ kind of thing is actually so common and used in python that it has its own language feature called "decorators" (and you should use functools, not just my simple example above. Remember to DuckDuckGo it before coding)

```python
>>> @wrapfunc
... def myfunc2()
...     print("Hello, I am original func!")
>>> myfunc2()
wrapping func
Hello, I am original func!
successfully wrapped func
```

We can monkeypatch in needed functionality before running it into the central library.  This is actually a "fork" for some code I used to solve a problem of concatenating objects earlier.

```python
from mycustom_package import ObjectStorage

# This is the method we want to patch into the class
# TODO: Add to library once we're done
def concat_chunks(self, bucket, chunk_folder, dest_filename):
   # Allright, lets combine all the files
   print('Proceeding to stitch chunks')
   chunks = [b.name for b in self.list_blobs(bucket, prefix=chunk_folder)]
   self.concat_blobs(bucket_name=bucket,
                     blob_out_name=dest_filename,
                     blob_names=chunks)


# Patch in the method if its not in the class
if not 'concat_chunks' in dir(ObjectStorage):
    ObjectStorage.concat_chunks = concat_chunks

# Running the program ..
storage = ObjectStorage(project=PROJECT_ID)
storage.concat_chunks(data['bucket'], chunk_folder, orig_filename)
```

All the above examples are things which cant, or is difficult to do in static languages such as C, Java, C#, etc.

### Understanding type systems

The above are some cool examples of how we may use the dynamic type system of python to do some advantageous things for our programs. Type systems, however, go beyond the static / dynamic axes. Going into every quirk of type systems, such as ducktyping/weak/strong/static/type safety/etc, would be well beyond this post - so I rather want to give an overview of where this falls into the ecosystem.

#### Type systems in Software Development

Using wikipedia, we can read that type systems are attributes of programming languages.  Programming languages are specifications for instructions to give some output, and are implemented by compilers or interpreters.  Programming languages are used when doing the process of computer programming to get a computer to perform computing tasks, to reach some desirable output specified by us humans. The act of programming further utilizes various practices such as software engineering to improve the output of the process of programming.

If we map it out, we get something like this:
```markdown
 <Process>Programming <- (Utilizes) <Methods>Software Engineering
         V (Produces)
 <Product>Programs/Instructions
         V (Interpreted by)
         V
 <Executable>Compiler or Interpreter <- (Implements)<Set>Instructions <- **(Has)<Attribute>Type systems**
         V (Produces)
 <<Executable>Machine code>Executable         OR <<Executable>Bytecode>Executable
         V (Runs on)                          OR        V (Runs on)
 <Hardware>Computer <- (Uses) Instruction set || <Executable>Virtual machine 
         V (Computes)                            V
 <Information>Desired Output                    < (Computes)
```

**The important part here** is that a _programming language is a specification_ and part of the specification is the _type system_ used by the language.  The compiler or interpreter implements the instruction set specified to create something executable by the computer to do something useful to us.

The type system attribute of the programming language specification determines limitations of the language, and further determines many of the use cases of the programming language (in theory you can write everything in brainfuck, but im writing in practical terms). Thus programming languages which are great of enormous codebases where safety and reliability is important may be very different from a language which is great for scripts which needs to be done very quickly.

#### Compared to a static typed language?

So when we say dynamic datatypes, it basically means that we dont have to specify the datatype of our variables when we are programming. We get the above benefits outlined in the examples, but it isn't without drawbacks. With a static typed language, we define the datatypes of variables and parameters etc, thus the program fails at compiletime if we pass variables to functions which do not support the datatype - which is great! Catching bugs on compiletime is much better than having something fail during runtime. Lets take this C program snippet as an example:

```c
#include <stdio.h>
#include <string.h>
#define MAXLEN 10

long char_as_long(char* arg) {
    size_t len  = strnlen(arg, MAXLEN); // get length of the char array
    long charval = 0; // The variable we add to

    // loop over the char array and add the values
    for (int i = 0; i < len; i++) {
        charval += (long) arg[i]; 
    }
    // return the added values
    return charval; 
}

int main() {
   // printf() displays the string inside quotation
   char my_msg[] = "Hello, World!";
   printf("the message '%s' has a total value of %i ", my_msg, char_as_long(my_msg));
   return 0;
}
```

Now what we're doing here is a bit unintuitive if youre not used to low level programming, but hold on. Every char is like a string in python of one character, if we make a list of chars, we have a string! We can extract the value of the memory address of the characters to a `long`, and the goal here is to add all the character values of the "Hello, World!" string and print it out!

aaaand lets run it:

```
/tmp/tmp.8epEIaLXcW
▶ gcc hello.c -o hello.bin

/tmp/tmp.8epEIaLXcW
▶ ./hello.bin
the message 'Hello, World!' has a total value of 888%
```

Good ol' C! Now lets change something. Say the prototype of the `char_as_long` takes a char value instead of a pointer to a char, with the same implementation as before.

```C
long char_as_long(char arg) { ... }
```

aaaand lets compile it!

```
/tmp/tmp.8epEIaLXcW
▶ gcc hello.c -o hello.bin

hello.c: In function ‘char_as_long’:
hello.c:6:27: warning: passing argument 1 of ‘strnlen’ makes pointer from integer without a cast [-Wint-conversion]
    6 |     size_t len  = strnlen(arg, MAXLEN); // get length of argument
      |                           ^~~
      |                           |
      |                           char
In file included from hello.c:2:
/usr/include/string.h:390:36: note: expected ‘const char *’ but argument is of type ‘char’
  390 | extern size_t strnlen (const char *__string, size_t __maxlen)
      |                        ~~~~~~~~~~~~^~~~~~~~
hello.c:9:30: error: subscripted value is neither array nor pointer nor vector
    9 |         charval += (long) arg[i];
      |                              ^
hello.c: In function ‘main’:
hello.c:17:76: warning: passing argument 1 of ‘char_as_long’ makes integer from pointer without a cast [-Wint-conversion]
   17 |    printf("the message '%s' has a total value of %i", my_msg, char_as_long(my_msg));
      |                                                                            ^~~~~~
      |                                                                            |
      |                                                                            char *
hello.c:5:25: note: expected ‘char’ but argument is of type ‘char *’
    5 | float char_as_long(char arg) {
      |                    ~~~~~^~~
```

oh no!

As you can see we get a full report of the failure before we even run the program, i.e. when we compile the program. The GCC compiler can see that we're passing the wrong arguments to the function, and the parameter is being used in the `strnlen` function which takes a char pointer - not a char. Awesome!

So whats the big deal?  Well if we're making something more complicated than this - say for example, an operating system - its naturally way better for the program to fail when we compile it rather than when it is in the hands of the user!

This type safety is lost in python, and we have to resort to doing asserts and tests instead to increase reliability of the program.

![c versus python](/images/anim/cvspython.gif)

(haha, I tried doing a simple 2d animation)

<hr>

### Subscribe for more!

So I hope you enjoyed this blogpost! If so, feel free to leave a comment below
or [sign up to my newsletter](https://sub.peakbreaker.com/subscribe)

