

在 Unity 的 GraphView 中，如果你想要重写 **Edge** 效果，通常建议重写或扩展 `Edge` 类，而不是 `Control` 类。这取决于你具体想修改的内容是视觉效果还是交互逻辑。

1. **自定义 Edge 的渲染**：如果你的目标是改变边的视觉外观，例如添加效果、调整颜色或修改曲线的表现，那么扩展或重写 `Edge` 类是最佳选择。你可以重写 `DrawEdge` 方法，在这里可以控制节点之间连接的视觉表现。
2. **自定义输入或行为更改**：如果你想控制边缘与鼠标的交互，例如拖拽连接节点的行为，可能需要进一步研究 `Control` 类或 `GraphView` 类，以处理自定义的 UI 逻辑。

总结：**如果是视觉效果上的修改，建议扩展 `Edge` 类**，并重写相应方法以实现自定义效果。如果是涉及到交互逻辑的更深层次控制，则可能还需要研究 `GraphElement` 或 `Control`。





```c++
using UnityEditor.Experimental.GraphView;
using UnityEngine;
using UnityEngine.UIElements;

namespace Kotono.Code.Editor
{
    public class ColoredEdge : Edge
    {
        private Label label; // 中间的文字标签

        public ColoredEdge()
        {
            // 初始化时检查并创建标签
            CheckAndCreateLabel();
            // 注册几何形状变化事件，相当于 Unity 的 OnEnable
            RegisterCallback<GeometryChangedEvent>(OnGeometryChanged);
        }

        // 检查并创建 Label
        private void CheckAndCreateLabel()
        {
            if (label == null)
            {
                label = new Label("连接");
                label.style.position = Position.Absolute;
                Add(label); // 将标签添加到 Edge 中
            }
        }

        // 当几何形状变化时触发，类似 OnEnable
        private void OnGeometryChanged(GeometryChangedEvent evt)
        {
            // 检查并创建 Label
            CheckAndCreateLabel();
            UpdateLabelPosition();
        }
        
        // 重写 UpdateEdgeControl 方法，确保标签放在中间
        public override bool UpdateEdgeControl()
        {
            Debug.Log("测试");
            if (!base.UpdateEdgeControl())
            {
                return false;
            }

            // 每次更新时检查并重新创建 Label
            CheckAndCreateLabel();

            UpdateLabelPosition(); // 更新标签的位置
            return true;
        }

        // 计算并更新标签的位置（放在 Edge 中间）
        private void UpdateLabelPosition()
        {
            // 确保 controlPoints 存在，并且至少有两个点
            if (edgeControl.controlPoints.Length >= 2)
            {
                Vector2 startPoint = edgeControl.controlPoints[0];
                Vector2 endPoint = edgeControl.controlPoints[edgeControl.controlPoints.Length - 1];

                // 计算中点
                Vector2 middlePoint = (startPoint + endPoint) / 2;

                // 更新 Label 位置，使其位于中点
                label.style.left = middlePoint.x - label.resolvedStyle.width / 2;
                label.style.top = middlePoint.y - label.resolvedStyle.height / 2;

                // 确保 Label 显示在前面
                label.BringToFront();
            }
        }
    }
}
```

BaseNodeView 已包含 onPortConnected/onPortDisconnected 的事件
