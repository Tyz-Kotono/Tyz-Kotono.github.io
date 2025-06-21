<font color=#4db8ff>LinK：</font>https://www.youtube.com/watch?v=OMDfr1dzBco&list=PLF3U0rzFKlTGzz-AUFacf9_OKiW_hGYIR&index=2

#### 显示错误

每次创建完Node和Port 需要调用更新

```c++
nodeCache.RefreshExpandedState();
nodeCache.RefreshPorts();
```

#### Port链接

```c++
public override List<Port> GetCompatiblePorts(Port startAnchor, NodeAdapter nodeAdapter)
{
    var compatiblePorts = new List<Port>();
    foreach (var port in ports.ToList())
    {
        if (startAnchor.node == port.node ||
            startAnchor.direction == port.direction ||
            startAnchor.portType != port.portType)
        {
            continue;
        }

        compatiblePorts.Add(port);
    }
    return compatiblePorts;
}
```



#### Save

<font color=#4db8ff>Link：</font>https://www.youtube.com/watch?v=OMDfr1dzBco&list=PLF3U0rzFKlTGzz-AUFacf9_OKiW_hGYIR&index=2

