def add(a: int, b:int) -> int:
    return a+b
def subtract(a: int, b:int) -> int:
    return a-b
def multiply(a: int, b:int) -> int:
    return a*b
def divide(a: int, b:int) -> int:
    return a/b

# test
def test_add() -> None:
    assert add(1,1)==2
    assert add(1,3)==4
def test_subtract() -> None:
    assert subtract(1,2)==-1
def test_multiply() -> None:
    assert multiply(10,10)==100
def test_divide() -> None:
    assert divide(100,25)==4