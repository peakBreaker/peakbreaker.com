---
categories: Golang
description: Introducing the Golang programming language and its features!
layout: post
featured_image: covers/paalsgo.png
author: Anders
tags: ['go', 'software', 'web']
finished: false
date: "2018-09-07"
title: "Golang with the P\xE5lgang"
---

*Just a short intro to the basics of golang with Pål*

# This is Pål

![paal](/assets/img/blog/paalsgo/paal.jpg)

*(He is the normal looking one by the window)*

Pål is the superhero developer keeping the Sensario backend operational.

I have worked Pål on his right hand side since mid 2017 and have enjoyed every
second of it.  We have been getting coffee together nearly every day, spoken
and learned about software engineering together and discovered the magic of Vim
and Chad memes together.

![chad linux](/assets/img/blog/paalsgo/chad_linux.png)

*From alg0001 on [reddit](https://www.reddit.com/r/virginvschad/comments/7rkm5n/the_virgin_windows_peasant_vs_the_chad_gnulinux/)*

Pål joined the Sensario company mid 2017 with the goal of building the backend of
the company so it could handle and process the incoming traffic from both our
IoT sensor nodes with LTE (which I am programming), users and he has provided
development services for the the engineering team. To do this, he has shown great 
mastery of Golang.

So join us in discovering this great programming language!

## Main characteristics of Golang

- General purpose programming language
- Compiled languate w/ great compile time and performance
- Static types
- Strings, chars, pointers, mutant for loops
- Implicit interfaces, structs, maps, slices and arrays
- Made with concurrency in mind; Goroutines and channels
- Nice utilities: Defer, multiple returns

## Whats in $GOPATH?

Golang has an environment variable which determines the workspace of your go
project. Coming from a C and Python background, this system took a bit getting
used to for me, and the Golang package system is something that stopped me from
getting too much into it in the start. Anyway, in the GOPATH you create the
following folders:

* src: source => This is where we keep our projects
* pkg: Object files => We dont usually touch this, its for the go toolchain
* bin: Binary files => We dont usually touch this, its for the go toolchain

This creates a $GOPATH workflow:

* With golang we import from $GOPATH/src/...
* Normal structure is this:
`$GOPATH/src/myProj/vendor/package`
* protip: Use godep instead of `$ go get` to maintain better structure.  I wont get to much into the use of this in this post
* Note: Go 1.11 introduces experimental support for projects outside $GOPATH.
  Havent looked too closely on this yet, but theres a [wiki entry](https://github.com/golang/go/wiki/Modules)

## Golang Syntax

A few of my main takeaways/heads up from the basics of golang syntax

- When returning multiple values, either give all returns a declaration in function prototype, or none (just datatypes).  Declaring return variables in function prototype will return them implicitly.

```
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}
```

The above function will return x and y implicitly because they are declared as returns in the function prototype. Sweet!

- go fmt is the standard for golang formatting/convention: `$ go fmt myfile.go`
- Golang scope rules are very simple, everything between {} is a scope
- In switch case statements, break is implicit/default and to ignore a break one 
  writes the `fallthrough` keyword

```
v := 42
switch v {
case 100:
	fmt.Println(100)
	fallthrough
case 42:
	fmt.Println(42)
	fallthrough
case 1:
	fmt.Println(1)
	fallthrough
default:
	fmt.Println("default")
}
// Output:
// 42
// 1
// default
```

*In C, for example, this is switched. By default the switch statement in C will
fallthrough, and one writes `break` to break the switch statement.  In Golang,
the break is implicit. Since one most often want to break the switch statment,
the golang syntax is pretty great!*

- Exported variables, constants and functions from packages must start with a capital letter

```
import (
	"fmt"
	"math"
)

func main() {
	fmt.Println(math.pi)
    // doesn't work
	fmt.Println(math.Pi)
    // works
}
```

A great tut on this in [A Tour of Go](https://tour.golang.org/basics/3)

## Golang datatypes

- Basics
  * uints/ints
  * floats
  * string: always utf-8
  * char: called rune, utf-8 => int32 under the hood

### Arrays
* Arrays are lists of values

```
// var myArray [<optional len>]<datatype>{<optional initializer>}
// myArray :=  [<optional len>]<datatype>{<optional initializer>}
myArray := [2]string{'hello', 'world'}
```

* Array utils: 

```
// Getting length in int
len(myArray)
// Looping over array
for idx, val := range myArray {...} 
```

### Slices
- Slices are parts of an underlying array

```
// array := [<len>]<datatype>{<optional initializer>}
// slice := array[<begin>:<end>]
```

And theyre very nice to work with.  Here are some slice utils:

```
len(slice)  // length of slice
cap(slice) // capacity of slice
append(<slice>, <value>[, <more values>]) // returns a new slice
```

Note on appending to slices: The new slice may point to the underlying array
only if appending to the slice didnt overflow the array.  Pål made a nice demo
on this:

```
s := make([]string, 1, 2)  // Length 1. Cap 2
s[0] = "start"             // Base slice
s1 := append(s, "slice 1") // Shared undelying array
s2 := append(s, "slice 2") // Shared undelying array
s3 := append(s, "slice 3",
    "needs more space!") // Exceedes cap. Allocates a new array

fmt.Printf("Before mutating:\ns:\t%v\ns1:\t%v\ns2:\t%v\ns3:\t%v\n", s, s1, s2, s3)
s[0] = "mutated"
fmt.Printf("After mutating:\ns:\t%v\ns1:\t%v\ns2:\t%v\ns3:\t%v\n", s, s1, s2, s3)
```

Outputs:

```
Before mutating:
s:	[start]
s1:	[start slice 2]
s2:	[start slice 2]
s3:	[start slice 3 needs more space!]
After mutating:
s:	[mutated]
s1:	[mutated slice 2]
s2:	[mutated slice 2]
s3:	[start slice 3 needs more space!]
```

hyyyyyiiiiiinteresting

### Maps
* Maps are like python dictionaries, but they are type sensitive
* Example usage:

```
// syntax
// myMap := map[<key type>]<val type>\
//          {<opt key>: <opt value>}
// Example map
myMap := map[string]float64{"Key": 33}
// Getting
myVar := myMap["myKey"]
// Setting
myMap["myKey"] = <myValue>
```

* Looping over maps:

```
for <key>, <value> := range myMap {...}
for <key> := range myMap {...}
```

## Working with datatypes

Here comes some of the nice golang features into play.  So far we've only
looked at the basic capabilities and mechanics of the language

### Custom types
* Custom types is like typedef in C
* Syntax: type <MyType> <ActualType>
* Example: type Hours int
* Custom types can be compared to same custom type or underlying type, but cannot be compared with different custom even if they share the same underlying type

### Methods

But Go isn't object oriented?
* Methods are implicit methods on types.  It is a function with a specific receiver argument, which tells which types implement the method
* func (t <MyType>) <MyMethod>(<MyArgs>) <MyReturn> {...}
* Now <MyType> vars will implement the <MyMethod> method
* In Go it is common to write methods that gracefully handle being called with nil receiver
* For example: 

```
func (v Vertex) Abs() float64 {...}
/* (using) --> */ vert.Abs()
```

### Structs

* In concept pretty much like structs in C -> structured data
* Convention to make all struct methods take either values or pointers as recv
* Declaring struct:

```
      type MyStruct struct {
         myArg string
     }
```

* Initializing struct:

```
      myStruct := MyStruct{MyArg: "Hello World!"}
      myStruct := MyStruct{"Hello World"} // Does the same, but need order of args
```

* Using struct:
  * Non cap members of struct are private
  * Accessing struct members are the same for pointers and value based structs
    (unlike c): `myStruct.MyArg`

### Interfaces

* The interface type is a set of method signatures
* Interfaces are implemented implicitly, if a datatype has the methods to satisfy the interface, it automatically implements the interface
* Syntax for declaring interface: 

`type <MyInterface> interface {/*methods*/}`

* Describing interfaces:

```
fmt.Printf("(%v, %T)\n", i, i) // i is an interface
```

This will show us that the interface is just a tuple of a value and datatype.
This is well illustrated in the [Tour of Go](https://tour.golang.org/methods/14) example.

```
Some interfaces:
(<nil>, <nil>)
(42, int)
(hello, string)
```

* a variable declared as an interface may be initialized with all types with the corresponding methods

## Golang concurrency

Golang is built with concurrency in mind, and thus has some cool features for
building stuff concurrently, namely Goroutines and channels

- Goroutines
  * A syntax for starting [goroutines](https://golang.org/ref/spec#Go_statements)
  * Syntax: go <expression>
  * Goroutines cant catch/handle returns, but can interact with channels (see
    below)
- Channels
  * Allows us to do IPC
  * Syntax:

```
// Making channel: 
channel := make(chan <type>)
// Reading from channel: 
<-chan
// Writing to channel: 
chan<- <value>
```

## Utilies worth mentioning

- `pprof` for analyzing load
- `reflect` for inspecting stuff
- `encoding` and `json` for serializing structured data
- Reader/Writer interfaces which are quite common

## Thanks for reading

This is all for now, later I may dive deeper into some of the parts of Golang!
