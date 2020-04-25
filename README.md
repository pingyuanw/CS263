#### Week 4

- learn about the architecture of PyPy

1. What is Pypy
  
    PyPy is a Python interpreter written in Python(to be accurate: RPython), and is faster than CPython.

    * pro: shorter and simpler

    * con: slow, as the interpreter is running on top of CPython. So PyPy will do a whole program analysis of PyPy interpreter and create a C source again, which is called translation(rpython translation chain). As translation process is very time-consuming(>30min), PyPy is using test-driven development to avoid full translation.
2. Why do we need PyPy
  
    * better understanding how interpreter works

    * ?

3. What do we need to know in PyPy?

    * RPython: 
        - a language for writing VMs
        - a strict subset of Python
        - translated to C to run

    * translation toolchain

- about GIL in CPython
  
  global lock among all threads to prevent concurrent reference counting

    * pro: avoid locks, better performance for single thread

    * con: no parallism

    * workaround: 
        * multi-processing
        * Gilectomy: hard to preserve single thread performance.

- other topic intersted

    * how translation toolchain works?
    * why is mercurial's branch model fits pypy better than git?

- Build PyPy
    1. install hg
    2. get source code
        `hg clone http://foss.heptapod.net/pypy/pypy pypy`
    3. install pypy
    4. translation
        `pypy ../../rpython/bin/rpython --opt=jit`


#### Week 5
*Plan*
- analysis on different implementation of GIL in PyPy
- learn about asyncio of PyPy