import importlib
import tools
while True:
    input()
    importlib.reload(tools)
    print(len(tools.tool_list))