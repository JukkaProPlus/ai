from datetime import datetime


def convert_timestamp_to_string(timestamp: int) -> str:
    """
    将时间戳转换为格式化的时间字符串。

    参数:
    timestamp (int): 时间戳。

    返回:
    str: 格式化的时间字符串，格式为'2021年1月1日19点33分27秒'。
    """
    # 转换时间戳为datetime对象
    dt_object = datetime.fromtimestamp(timestamp)
    
    # 格式化时间字符串
    formatted_time = dt_object.strftime('%Y年%m月%d日%H点%M分%S秒')
    
    return formatted_time

from langchain.tools import StructuredTool

document_tool_convert_timestamp = StructuredTool.from_function(
    func=convert_timestamp_to_string,
    name="ConvertTimestampToString",
    description="将时间戳转换为格式化的时间字符串，格式为'2021年1月1日19点33分27秒'。"
)