<font color=#4db8ff>Link：</font>https://www.youtube.com/watch?v=gNmPmWR2vV4





```c++
using UnityEngine;

namespace Octrees
{
    public class Octree
    {
        public GameObject root;
        private Bounds bounds;

        public Octree(GameObject[] worldObjects, float minNodeSize)
        {
            CalculateBounds(worldObjects);
        }

        void CalculateBounds(GameObject[] worldObjects)
        {
            foreach (var obj in worldObjects)
            {
                //强制包裹
                bounds.Encapsulate(obj.GetComponent<Collider>().bounds);
            }
        }
    }

    public class Octreenode
    {
        
    }

    public class OctreeObject
    {
        
    }
}
```

