---
title: "RenderDoc"
date: 2025-06-15T03:45:46+08:00
draft: false
categories:
- "逆向"
---





1. Editor->ProjectSetting->RenderDoc，勾选“Auto Attach on startup”
2. ![image-20241127013729389](./assets/image-20241127013729389.png)
3. 去项目的config目录下，打开DefaultEngine.ini输入以下

```c++
[/Script/Engine.RendererSettings]
r.Shaders.Optimize = 0
r.Shaders.Symbols=1
r.Shaders.SkipCompression=1
r.ShaderDevelopmentMode=1
```

