<font color=#4db8ff>Link：</font>https://www.audiokinetic.com/zh/library/edge/?source=SDK&id=waapi_prepare.html

Code 推荐：https://www.audiokinetic.com/zh/library/edge/?source=SDK&id=waapi_gettingstarted.html



#### 一、环境

1,1 依赖库

安装依赖库，注意安装位置要与编译器使用python版本所在地，否则不识别

```python
# Windows
py -3 -m pip install waapi-client
 
# macOS, Linux
python3 -m pip install waapi-client
```

测试代码

```c++
#!/usr/bin/env python3
from waapi import WaapiClient, CannotConnectToWaapiException
from pprint import pprint

try:
# Connecting to Waapi using default URL
with WaapiClient() as client:
    # NOTE: client will automatically disconnect at the end of the scope

    # == Simple RPC without argument
    print("Getting Wwise instance information:")

    result = client.call("ak.wwise.core.getInfo")
    pprint(result)

    # == RPC with arguments
    print("Query the Default Work Unit information:")

    object_get_args = {
        "from": {
            "path": ["\\Actor-Mixer Hierarchy\\Default Work Unit"]
        },
        "options": {
            "return": ["id", "name", "type"]
        }
    }
    result = client.call("ak.wwise.core.object.get", object_get_args)
    pprint(result)
except CannotConnectToWaapiException:
print("Could not connect to Waapi: Is Wwise running and Wwise Authoring API enabled?")
```



#### 二、函数