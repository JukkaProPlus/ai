"""
斐波那契数列生成工具模块
"""

def fibonacci(n):
    """生成斐波那契数列的前n个数，返回由这些数字组成的字符串，数之间用逗号分隔."""
    sequence = []
    a, b = 0, 1
    while len(sequence) < n:
        sequence.append(b)
        a, b = b, a + b
    return ','.join(map(str, sequence))

from langchain.tools import StructuredTool

document_tool_fibonacci = StructuredTool.from_function(
    func=fibonacci,
    name='FibonacciSequence',
    description='生成斐波那契数列的前n个数，返回由这些数字组成的字符串，数之间用逗号分隔。输入是一个整数n。'
)