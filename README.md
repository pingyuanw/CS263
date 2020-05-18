#### Week 4

- learn about the architecture of PyPy

1. What is Pypy
    - A set of tools for implementing interpreters for interpreted languages
    - An implementation of Python using this toolchain

        PyPy is a Python interpreter written in Python(to be accurate: RPython), and is faster than CPython.

        * pro: shorter and simpler

        * con: slow, as the interpreter is running on top of CPython. So PyPy will do a whole program analysis of PyPy interpreter and create a C source again, which is called translation(rpython translation chain). As translation process is very time-consuming(>30min), PyPy is using test-driven development to avoid full translation.
2. Why do we need PyPy
  
    * better understanding how interpreter works

    * JIT included

    * develop VM

3. What do we need to know in PyPy?

    * RPython & translation toolchain

- about GIL in CPython
  
  global lock among all threads to prevent concurrent reference counting

    * pro: avoid locks, better performance for single thread

    * con: no parallism

    * workaround: 
        * multi-processing
        * Gilectomy: hard to preserve single thread performance.

- Build PyPy
    1. install hg
    2. get source code
        `hg clone http://foss.heptapod.net/pypy/pypy pypy`
    3. install pypy
        - brew install pypy: for python2
        - brew install pypy3: for python3
    4. run untranslated version:
        `PYTHONPATH=../pypy python entry.py xx.py`
    5. translation
        `cd goal`
        `pypy ../../rpython/bin/rpython --opt=jit entry.py`

#### Week 5

- About RPython
    1. What is RPython?
        Named Restricted Python, it's a subset of Python. The restrictions:
        - dynamic features like class modification could only be used in an initial phase, which is used to construct the final RPython program.
        - the final RPython program must be well-typed.
        - only single inheritance
        * RPython: 
            - a language for writing VMs
            - a strict subset of Python
            - compiled from live python objects, no parser. (Python is a meta programming language for RPython)
            - translated to C to run
            - selling point to use Rpython to write VMs: *JIT compiler for free*
                automatically layer alongside a second representation of the interpreter(tracing interpreter)
    2. Why do we need RPython?
        more expressive than C# and Java.

- JIT in PyPy
    - trace the interpreter(can be applied to all other interpreters)
        - tracer
        - optimizer
        - backend: turn to machine code
- GC: inserted during translation

- Concurrency/Parallism, 3 models:
    - threading
    - coroutine
    - multi-processing

- Python's async model(asyncio)
    - generator: synchronous, asynchronous
        - iterator:
            * iterable: can be used in an iteration. support __iter__
            * iterator: yield successive items. support __next__
            * iterator protocol: Objects that support the __iter__ and __next__ dunder methods automatically work with for-in loops.
                * __iter__: get the iterator object
                * __next__: get the next item from the iterator object
                * __iter__ returns any object with a __next__ method on it.
        - yield:
            1. When yield, the program suspends and returns the yielded value. 
            2. the state of that function is saved.
            3. when call next, it will pick up right after yield
        - pro of generator: no memory penalty    
    - coroutine: a function that can suspend its execution before reaching return

#### Week 6
- PyPy Interpreter
    - translated version: run goal/pypy-c
    - untranlated version, using cpython: run bin/pyinteractive.py
- how PyPy implements coroutine
    - Generator
        - stack frame?
            read PyPy source code
    - event loop:
    - future:

- how to implement concurrency features:
    - coroutine, by generator, or library such as libcoro
    - event loop, by library such as asyncio/curio

#### Week 7
- read asyncio source code
    - how to use custom event loop and custom policy
    - workflow to schedule and run tasks
        - core function: Task.__step
- coroutine deadlocks
    - try to detect deaklocks at runtime, but failed to produce deadlocks without using asyncio


*To do*
- produce deadlock
- implement a simple framework with event loop
    - schedule tasks
    - timer
    - I/O
    - race condition
- how libcoro works


*Things might be interesting*

- what is python code object
- write an interpreter for a new language using PyPy
- how TCP concurrency works
- how translation toolchain works?
- why is mercurial's branch model fits pypy better than git?
- implementation of for loops in different languages
- different implementation of GIL in PyPy
- greenlet in PyPy
- stackless