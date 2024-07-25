def ConvertDecimalToOctal(decimal_str: str) -> str:
    """
    将10进制表示的数字字符串转换为8进制表示的数字的字符串。

    参数:
    decimal_str (str): 10进制表示的数字字符串。

    返回:
    str: 8进制表示的数字字符串。
    """
    decimal_number = int(decimal_str)
    octal_number = oct(decimal_number)[2:]  # 转换为8进制并去掉前缀 '0o'
    return octal_number

from langchain.tools import StructuredTool

document_tool_ConvertDecimalToOctal = StructuredTool.from_function(
    func=ConvertDecimalToOctal,
    name='ConvertDecimalToOctal',
    description='将10进制表示的数字字符串转换为8进制表示的数字的字符串'
)