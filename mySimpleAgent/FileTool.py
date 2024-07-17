import os
from FuncDict import func_dict
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
    return os.getcwd()
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
def getJamesSum(a,b):
    """
    计算两个数字的詹姆斯和
    """
    return (a+b) * (a-b)

