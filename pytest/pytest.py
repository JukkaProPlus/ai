
def printAll(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

def getSum(a, b):
    return a + b

ff = {"a": 1, "b": 2}
print(getSum(**ff))