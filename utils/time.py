# IMPORTS

# Builtins
import time as _time
import datetime as _datetime


# FUNCTIONS

# Sleep
def sleep(duration: float) -> None:
    _time.sleep(duration)


# Benchmark time
def bench_time() -> float:
    return _time.perf_counter()


# Benchmark time in nanoseconds
def bench_time_ns() -> int:
    return _time.perf_counter_ns()


# Run time
def run_time() -> float:
    return _time.process_time()


# Run time in nanoseconds
def run_time_ns() -> int:
    return _time.process_time_ns()


# Absolute time since epoch
def abs_time() -> float:
    return _time.time()


# Absolute time since epoch in nanoseconds
def abs_time_ns() -> int:
    return _time.time_ns()


# Datetime format 1
def datetime_f1() -> str:
    return _datetime.datetime.now().strftime("%d/%b/%y %H:%M:%S")


# Datetime format 2
def datetime_f2() -> str:
    return _datetime.datetime.now().strftime("%Yy-%mm-%dd_%Hh-%Mm-%Ss")
