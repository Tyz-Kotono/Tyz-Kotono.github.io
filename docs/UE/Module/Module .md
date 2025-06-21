<font color=#4db8ff>Link：</font>https://www.youtube.com/watch?v=-r4OmyrFC30

前向定义不会Include ，而是让他关注这个类，因为他是一个指针，他包含一个运行时的内存地址，可以获得更快的编译时间。他没有向我们提供任何实际信息





```c++
class FShadeupExamplePluginModule : public IModuleInterface
{
public:

	/** IModuleInterface implementation */
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;
};

```





```c++
#include "ShadeupExamplePlugin.h"

#define LOCTEXT_NAMESPACE "FShadeupExamplePluginModule"

void FShadeupExamplePluginModule::StartupModule()
{
	// This code will execute after your module is loaded into memory; the exact timing is specified in the .uplugin file per-module
}

void FShadeupExamplePluginModule::ShutdownModule()
{
	// This function may be called during shutdown to clean up your module.  For modules that support dynamic reloading,
	// we call this function before unloading the module.
}

#undef LOCTEXT_NAMESPACE
	
IMPLEMENT_MODULE(FShadeupExamplePluginModule, ShadeupExamplePlugin)
```

