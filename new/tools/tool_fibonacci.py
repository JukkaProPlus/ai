"""
쳲������������ɹ���ģ��
"""

def fibonacci(n):
    """����쳲��������е�ǰn��������������Щ������ɵ��ַ�������֮���ö��ŷָ�."""
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
    description='����쳲��������е�ǰn��������������Щ������ɵ��ַ�������֮���ö��ŷָ���������һ������n��'
)