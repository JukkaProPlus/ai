def calculate_gcd(a: int, b: int) -> str:
    """
    计算两个数的最大公约数。

    参数:
    a (int): 第一个整数。
    b (int): 第二个整数。

    返回:
    str: 描述两个数最大公约数的字符串。
    """
    while b:
        a, b = b, a % b
    return f'两个数的最大公约数是{a}'

from langchain.tools import StructuredTool

document_tool_calculate_gcd = StructuredTool.from_function(
    func=calculate_gcd,
    name='CalculateGCD',
    description='计算两个数的最大公约数'
)