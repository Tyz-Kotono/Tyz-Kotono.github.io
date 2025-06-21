导入

![image-20250412162940873](./assets/image-20250412162940873.png)

![image-20250412162755039](./assets/image-20250412162755039.png)

![image-20250412162811413](./assets/image-20250412162811413.png)

![0a8f211498b87c7c8c24a30044738680](./assets/0a8f211498b87c7c8c24a30044738680.png)

![image-20250412163200444](./assets/image-20250412163200444.png)







![image-20250412162547412](./assets/image-20250412162547412.png)

![image-20250412163040380](./assets/image-20250412163040380.png)





其中Source Engine 
![image-20250412180419130](./assets/image-20250412180419130.png)

Source View 2

![image-20250412180324486](./assets/image-20250412180324486.png)









![image-20250412195323057](./assets/image-20250412195323057.png)



#### Crowbar

![image-20250412202306274](./assets/image-20250412202306274.png)

##### Blender

input vmdl_C

![image-20250412213025183](./assets/image-20250412213025183.png)









#### Source 2 View

![image-20250412211857896](./assets/image-20250412211857896.png)

![image-20250412211735941](./assets/image-20250412211735941.png)



#### 导出

![image-20250412235940446](./assets/image-20250412235940446.png)



##### Blender 官方模型

![image-20250413000427784](./assets/image-20250413000427784.png)

##### 撬锁解包![image-20250413003216556](./assets/image-20250413003216556.png)

##### VRF反编译动作

![image-20250413003330258](./assets/image-20250413003330258.png)

##### 导出动作![image-20250413003350545](./assets/image-20250413003350545.png)

##### 四元素

![image-20250413000318911](./assets/image-20250413000318911.png)

动作脚本写入NLA

```c++
import bpy

# 获取当前选中的骨骼对象（需提前在3D视图中选中骨骼）
armature = bpy.context.active_object

# 检查是否为骨骼
if not armature or armature.type != 'ARMATURE':
    raise Exception("未选中骨骼对象！请在3D视图中选择骨骼后运行脚本")

# 获取文件中所有动作
all_actions = bpy.data.actions

# 过滤系统默认动作（可选）
valid_actions = [act for act in all_actions if not act.name.startswith('_')]

# 检查是否有可用动作
if not valid_actions:
    raise Exception("未找到有效动作！请确保已导入或创建动作")

# 初始化动画数据
if not armature.animation_data:
    armature.animation_data_create()

# 清空现有NLA轨道（可选，按需取消注释）
# armature.animation_data.nla_tracks.clear()

# 批量添加动作到NLA轨道
for action in valid_actions:
    # 创建新轨道（以动作命名）
    track = armature.animation_data.nla_tracks.new()
    track.name = f"{action.name}"
    
    # 添加动作片段到轨道起始位置
    strip = track.strips.new(action.name, 0, action)
    
    # 可选：自动设置片段长度为动作时长
    strip.frame_end = strip.frame_start + action.frame_range[1] - 1

# 操作完成提示
print(f"成功添加 {len(valid_actions)} 个动作到NLA轨道：")
for action in valid_actions:
    print(f" - {action.name}")
    
```

##### 轴向

![image-20250413000955812](./assets/image-20250413000955812.png)

##### 导出Glft

![image-20250413000652262](./assets/image-20250413000652262.png)