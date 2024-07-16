import os
def getWorkDir()->str:
    """
    获取当前工作目录。
    """
    return os.getcwd()
def isFileExist(filePath)->bool:
    """
    检查文件是否存在。
    """
    return os.path.isfile(filePath)
def isDirExist(dirPath)->bool:
    """
    检查文件夹是否存在。
    """
    return os.path.isdir(dirPath)
def getAllFilePath(dirPath)->list:
    """
    获取文件夹下所有文件的路径。
    """
    return [os.path.join(dirPath, fileName) for fileName in os.listdir(dirPath)]
