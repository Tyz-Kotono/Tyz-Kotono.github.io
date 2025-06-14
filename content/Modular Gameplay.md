Link：https://www.youtube.com/watch?v=sSoGEO1tnEI



依赖于Game Features和 Modular GamePlay

![image-20240918022202726](./assets/image-20240918022202726.png)

![image-20240918022832006](./assets/image-20240918022832006.png)



![image-20240918022822976](./assets/image-20240918022822976.png)



![image-20240918023110005](./assets/image-20240918023110005.png)



#### GameFeatureAction

![image-20240918023049102](./assets/image-20240918023049102.png)

#### Lyar

![image-20240918032323910](./assets/image-20240918032323910.png)

做了与蓝图相同的事情

![image-20240918033017091](./assets/image-20240918033017091.png)

删除蓝图之后，依然有效

![image-20240918033042403](./assets/image-20240918033042403.png)





![image-20240918033151864](./assets/image-20240918033151864.png)



![image-20240918033343164](./assets/image-20240918033343164.png)

```c++
void AModularCharacter::PreInitializeComponents()
{
	Super::PreInitializeComponents();

	UGameFrameworkComponentManager::AddGameFrameworkComponentReceiver(this);
}

void AModularCharacter::BeginPlay()
{
	UGameFrameworkComponentManager::SendGameFrameworkComponentExtensionEvent(this, UGameFrameworkComponentManager::NAME_GameActorReady);

	Super::BeginPlay();
}

void AModularCharacter::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
	UGameFrameworkComponentManager::RemoveGameFrameworkComponentReceiver(this);

	Super::EndPlay(EndPlayReason);
}


```

