def ConvertDecimalToHex(decimal_str: str) -> str:
    """
    将10进制表示的数字字符串转换为16进制表示的数字的字符串。

    参数:
    decimal_str (str): 10进制表示的数字字符串。

    返回:
    str: 16进制表示的数字字符串。
    """
    decimal_number = int(decimal_str)
    hex_number = hex(decimal_number)[2:].upper()  # 转换为16进制并去掉前缀 '0x'
    return hex_number

from langchain.tools import StructuredTool

document_tool_ConvertDecimalToHex = StructuredTool.from_function(
    func=ConvertDecimalToHex,
    name='ConvertDecimalToHex',
    description='将10进制表示的数字字符串转换为16进制表示的数字的字符串'
)