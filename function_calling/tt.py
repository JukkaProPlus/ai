# from langchain_experimental.utilities import PythonREPL
# def add(a,b):
#     return a + b
# code = """
# sum = add(3, 4)
# print(sum)
# """
# ans = PythonREPL().run(code)
# print(ans)

# from langchain_experimental.utilities import PythonREPL

# # 定义本地函数
# def add(a, b):
#     return a + b

# # 将本地函数添加到环境中
# environment = {
#     'add': add
# }

# # 由大模型生成的代码
# code = """
# sum = add(3, 4)
# print(sum)
# """

# # 创建PythonREPL实例并设置环境
# repl = PythonREPL()
# repl.set_globals(environment)

# # 运行代码
# ans = repl.run(code)
# print(ans)


from langchain_experimental.utilities import PythonREPL

# 定义本地函数
def add(a, b):
    return a + b

# 由大模型生成的代码
model_generated_code = """
sum = add(3, 4)
print(sum)
"""

# 将本地函数的定义添加到生成的代码中
combined_code = f"""
def add(a, b):
    return a + b

{model_generated_code}
"""

# 运行代码
repl = PythonREPL()
ans = repl.run(combined_code)
print(ans)
