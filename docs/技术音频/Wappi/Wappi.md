

```c++
现在使用中文回答
现在我要利用Waapi给Wwise写工具所以我使用
python3.13和QT6编写UI

首先我有两个类QTWindow.py继承于QT的窗口他的子类都可以拖拽放置窗口位置并且垂直和水平都可以

另一个类继承QTWindowBase.py他继承于继承QTWindowBase.py
他内部允许放置所有的QTWindow.py窗口，但是禁止放置自己的子类以及QTWindow.py不允许QTEditorWindow.py的子类的窗口
随后根据图片生成这几个Python文件

所有通过 QTWindowBase 继承的窗口都可以：

放在顶部或底部区域（支持多个并列或堆叠）；

自由拖拽、浮动、小窗化；

文件路径录

Main.py
Source
     ModuleCore.py					被Main执行调用 
     WindowModule
    	QTWindowModule.py 			负责绘制窗口被ModuleCore调用他的Draw函数
	    QTWindowModuleCollection.py
        base
    	    QTEditorWindowBase.py	可能继承于QSplitter 
            QTWindowBase.py		    可能继承于DockWidget 
        Window
            QTDebug.py		继承QTWindowBase
            QTContent.py	继承QTWindowBase


```







```c++
    Main.py
    Source
         ModuleCore.py					被Main执行调用 
         WindowModule
            QTWindowModule.py 			负责绘制窗口被ModuleCore调用他的Draw函数
            QTWindowModuleCollection.py
        base
            QTEditorWindowBase.py	可能继承于QSplitter 
            QTWindowBase.py		    可能继承于DockWidget 
        Window
                QTDebug.py		继承QTWindowBase
                QTContent.py	继承QTWindowBase
```



```c++
Main.py
Config
	config.ini 					保存所有Ini的路径方便读取以及一些设置
    Layout/DefaultLayout.ini 	保存默认的Layout分布
		   Layout.ini        	Custom定义的Layout
	WindowMoudel.ini			保存所有的Window类型
    Moudel.ini
Source
   	 ModuleCore.py					被CollectionCore执行调用 判断获得的所有module是否开启module，随后写入Moudel.ini
     CollectionCore.py				调用ModuleCollectionBase.py的子类开启收集
     Base
     	ModuleBase.py				被module子类继承
     	ModuleCollectionBase.py		收集所有的 ModuleBase.py子类，保存在字典里，所有遍历判断是否开启module
	 WindowModule
		QTWindowModule.py		    被ModuleBase.Build.py收集，随后调用 ModuleCore.py，执行一些逻辑这里先Print String
    	QTWindowModuleCollection.py  继承于ModuleCollectionBase.py 收集所有继承于QTWindowBase的子类这里不查找QTEditorWindow.py的子类，类如QTDebug.py、Dertails等QT窗口,随后查找和QTEditorWindow.py的子类，保存在两个字典中，并且有功能写入随后写入WindowMoudel.ini
		base
			QTEditorWindowBase.py	可能继承于QSplitter 
			QTWindowBase.py			可能继承于DockWidget 
		Window
    		QTDebug.py		继承QTWindowBase
			QTContent.py	继承QTWindowBase
```









```c++
Main.py
Config
	config.ini 				保存所有Ini的路径方便读取以及一些设置
    Layout/DefaultLayout.ini 保存默认的Layout分布
		   Layout.ini        Custom定义的Layout
    Module.ini		 		收集所有的Module
Source
    collector.py			 被Main调用，负责开启Build收集数据，管理数据，写入Ini的管理
    Build
    	Bulid.py			 收集所有的继承Bulid.base.py写入Module.ini，同时写入或者创建对应的ini文件
		Bulid.base.py		
    Module
		Module.Build.py		收集所有的Module写入 Module.ini	
    	Module.py			被Main调用随后调用所有的Module如WindowModule
    WindowModule
            QTWindow.Build.py  收集所有继承于QTWindowBase的子类，如Setting、Dertails等QT窗口
            QTWindowBase.py
            QTWindow.py			被MenusMoudle调用针对收集的Menu进行QTWindow
			//下列部分仅绘制一个简单UI即可
            Settings
                Setting.py		负责设置，继承于QTWindow.py		
            Details
                Details.py		负责展示Details，wwise文件细节，继承于QTWindow.py		
            Debug	
                Debug.py		负责搜集Debug并且显示，继承于QTWindow.py		
            Content
                Content.py	    负责显示收集到的所有Wwise对象，继承于QTWindow.py	
  
```





一、菜单栏

```c++
利用Menu.ini 抓取所有的Window，Window窗口通过Menu.ini可以打开所有的窗口类型
```









```c++

```

