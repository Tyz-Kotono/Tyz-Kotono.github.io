https://www.youtube.com/watch?v=nKpM98I7PeM

#### 1、Node

状态，核心为 Runing则执行Update

```c++
public enum State {
    Running,
    Failure,
    Success
}
```



基础Node

```c++
 public abstract class Node : ScriptableObject
 {
[HideInInspector] public State state = State.Running;
[HideInInspector] public bool started = false;
[HideInInspector] public string guid;
[HideInInspector] public Vector2 position;
[HideInInspector] public Context context;

public virtual void OnDrawGizmos() { }

protected abstract void OnStart();
protected abstract void OnStop();
protected abstract State OnUpdate();
}
```

编写一个顺序函数

```c++
public State Update() {

    //Start 没有执行就执行
    if (!started) {
        OnStart();
        started = true;
    }

    state = OnUpdate();

    if (state != State.Running) {
        OnStop();
        started = false;
    }

    return state;
}
```

#### 2、Tree

跟节点，状态

```c++
    public class BehaviourTree : ScriptableObject {
        
        public Node rootNode;
        public Node.State treeState = Node.State.Running;
        public List<Node> nodes = new List<Node>();
        public Blackboard blackboard = new Blackboard();

        //如果不是执行就停止
        public Node.State Update() {
            if (rootNode.state == Node.State.Running) {
                treeState = rootNode.Update();
            }
            return treeState;
        }
    }
```

#### 3、Node

#####  3.1、ActionNode

```c++
  public abstract class ActionNode : Node {

    }
```

##### 3.2、Log

随后扩展

```c++
  public class Log : ActionNode
    {
        public string message;
        protected override void OnStart() {}
        protected override void OnStop() }
        protected override State OnUpdate() {
            Debug.Log($"{message}");
            //停止继续Run
            return State.Success;
        }
    }
```

##### 3.3、CompositeNode

```c++
public abstract class CompositeNode : Node {
    [HideInInspector] public List<Node> children = new List<Node>();
}
```

##### 3.4、DecoratorNode

```c++
public abstract class DecoratorNode : Node {
    [HideInInspector] public Node child;
}
```

##### 3.4、Runtree

BehaviourTreeRunner

```c++
public class BehaviourTreeRun : MonoBehaviour
{
    public BehaviourTree tree;

    void Start() {
        tree = ScriptableObject.CreateInstance<BehaviourTree>();
        var log = ScriptableObject.CreateInstance<DebugNode>();
        log.message = "xxxx";
        tree.rootNode = log;
    }

    void Update()
    {
        if (tree) 
        {
            tree.Update();
        }
    }
}
```

##### 3.5、Repeat

重复

```c++
public class Repeat :DecoratorNode 
{
    protected override void OnStart() {}

    protected override void OnStop() {}

    protected override State OnUpdate() 
    {
        child.OnUpdate();
        return State.Running;
    }
}
```

修改BehaviourTreeRun

```c++
void Start() {
    tree = ScriptableObject.CreateInstance<BehaviourTree>();

    var log = ScriptableObject.CreateInstance<DebugNode>();
    log.message = "xxxx";

    var Loop = ScriptableObject.CreateInstance<Repeat>();
    Loop.child = log;
    tree.rootNode = Loop;
}
```

![image-20240921185447678](./assets/image-20240921185447678.png)

##### 3.6、Sequencer

顺序执行，如果成功则执行

```c++
public class Sequencer : CompositeNode 
{
    protected int current;

    protected override void OnStart() {
        current = 0;
    }

    protected override void OnStop() {}

    protected override State OnUpdate()
    {
        var child = children[current];

        switch (child.Update()) {
            case State.Running:
                return State.Running;
            case State.Failure:
                return State.Failure;
            case State.Success:
                current++;
                break;
        }
        Debug.Log("  " + current);
        return current == children.Count ? State.Success : State.Running;
    }
}
```

修改BehaviourTreeRun

```c++
void Start() 
{
    tree = ScriptableObject.CreateInstance<BehaviourTree>();

    var log = ScriptableObject.CreateInstance<DebugNode>();
    log.message = "xxxx";

    var log2 = ScriptableObject.CreateInstance<DebugNode>();
    log2.message = "xxxxYYYYYYYY";
    var log3= ScriptableObject.CreateInstance<DebugNode>();
    log3.message = "xxxxZZZZZZZZZZZZZZ";

    var Sequencer = ScriptableObject.CreateInstance<Sequencer>();
    Sequencer.children.Add(log);
    Sequencer.children.Add(log2);
    Sequencer.children.Add(log3);
    var Loop = ScriptableObject.CreateInstance<Repeat>();
    Loop.child = Sequencer;
    tree.rootNode = Loop;
}
```

![image-20240921191008214](./assets/image-20240921191008214.png)

##### 3.7、WaitNode



```c++
public class WaitNode : ActionNode
{
    public float duration = 1;
    float startTime;

    protected override void OnStart() {
        startTime = Time.time;
    }

    protected override void OnStop() {
    }

    protected override State OnUpdate() {
        if (Time.time - startTime > duration) {
            return State.Success;
        }
        return State.Running;
    }
}
```



```c++
void Start() {
    tree = ScriptableObject.CreateInstance<BehaviourTree>();

    var log = ScriptableObject.CreateInstance<DebugNode>();
    log.message = "xxxx";

    var Wait = ScriptableObject.CreateInstance<WaitNode>();
    var log2 = ScriptableObject.CreateInstance<DebugNode>();
    log2.message = "xxxxYYYYYYYY";
    var log3= ScriptableObject.CreateInstance<DebugNode>();
    log3.message = "xxxxZZZZZZZZZZZZZZ";

    var Sequencer = ScriptableObject.CreateInstance<Sequencer>();
    Sequencer.children.Add(log);
    Sequencer.children.Add(Wait);
    Sequencer.children.Add(log2);
    Sequencer.children.Add(Wait);
    Sequencer.children.Add(log3);
    Sequencer.children.Add(Wait);
    var Loop = ScriptableObject.CreateInstance<Repeat>();
    Loop.child = Sequencer;
    tree.rootNode = Loop;
}
```

![image-20240921193040057](./assets/image-20240921193040057.png)

#### 4、Tree Graph

https://www.youtube.com/watch?v=nKpM98I7PeM
