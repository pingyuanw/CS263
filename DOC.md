#### 1. Setup
python version: 2 and 3

- clone the repo to local: `git clone https://github.com/pingyuanw/CS263.git`

- go to repo folder: `cd CS263`

- clone the pypy repo to current folder: `hg clone http://foss.heptapod.net/pypy/pypy pypy`

#### 2. Run test
First go the language folder: `cd language_x`

- Run Python test
    `python3 test.py`
- Run X test
    `PYTHONPATH=../pypy python2 targetx.py example.x`
