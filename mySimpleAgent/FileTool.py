import os
from FuncDict import func_dict
import chardet
def register_function(func_dict):  
    def decorator(func):  
        func_dict[func.__name__] = func  
        return func  
    return decorator  
@register_function(func_dict=func_dict)
def getWorkDir()->str:
    """
    获取当前工作目录。
    """
    return repr(os.getcwd())
@register_function(func_dict=func_dict)
def isFileExist(filePath)->bool:
    """
    检查文件是否存在。
    """
    return os.path.isfile(filePath)
@register_function(func_dict=func_dict)
def isDirExist(dirPath)->bool:
    """
    检查文件夹是否存在。
    """
    return os.path.isdir(dirPath)
@register_function(func_dict=func_dict)
def getAllFilePath(dirPath)->list:
    """
    获取文件夹下所有文件的路径。
    """
    return [os.path.join(dirPath, fileName) for fileName in os.listdir(dirPath)]

@register_function(func_dict=func_dict)
def getJamesResult(a,b):
    """
    计算两个数字的詹姆斯运算结果,詹姆斯运算是本地定义的一种计算,有其自己的特殊定义.
    """
    return (a+b) * (a-b)
@register_function(func_dict=func_dict)
def getFileContent(filePath)->str:
    """
    获取文件的内容。
    """
    with open(filePath, 'r') as file:
        return file.read()

def read_file_with_chardet(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
    with open(file_path, 'r', encoding=encoding) as f:
        return f.read()
