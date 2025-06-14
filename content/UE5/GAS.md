

### DevKaiUnreal

Link:https://www.youtube.com/@DevKaiUnreal

#### Set

这个是负责存数据的

```c++
class GAS_DEVKAIFAB_API UFabAttributeSet : public UGameplayAbilitySet
{
	GENERATED_BODY()
public:
	UFabAttributeSet();

	UPROPERTY()
	FGameplayAttributeData Health;
};

```

#### Attribute

```c++
void APlayerCharacter::InitAbilitySystemComponent()
{
	AFabPlayerState* FabPlayerState = GetPlayerState<AFabPlayerState>();

	check(FabPlayerState);

	// if(FabPlayerState != nullptr)
	// {
	// 	
	// }


	AbilitySystemComponent = CastChecked<UFabAbilitySystemComponent>(FabPlayerState->GetAbilitySystemComponent());

	AbilitySystemComponent->InitAbilityActorInfo(FabPlayerState, this);

	AttributeSet = FabPlayerState->GetAttributeSet();

	// Gameplay Effect 的网络同步策略，敌人效果不会复制给任何人
	// AbilitySystemComponent->SetReplicationMode(EGameplayEffectReplicationMode::Minimal);
}
```





![image-20240911233013854](./assets/image-20240911233013854.png)





![image-20240911232852463](./assets/image-20240911232852463.png)



![image-20240911233339203](./assets/image-20240911233339203.png)





#### Debug

![image-20240911232417550](./assets/image-20240911232417550.png)

//DefaultGame.ini

```c++
[/Script/GameplayAbilities.AbilitySystemGlobals]
bUseDebugTargetFromHub = true
```

```c++
ShowDebug AblitySystem
```

#### Tag

![image-20240912222610374](./assets/image-20240912222610374.png)

分别是这个GA的标签

正在播放GA时会添加的标签
	如果GA有这个标签则无法执行GA

这样可以避免GA多次播放



消耗的GE

![image-20240913002141057](./assets/image-20240913002141057.png)

应用GE

![image-20240913002202792](./assets/image-20240913002202792.png)

冷却



![image-20240913002411201](./assets/image-20240913002411201.png)

消耗以及冷却的GE

![image-20240913002437581](./assets/image-20240913002437581.png)

SetByCaller

![image-20240914014434776](./assets/image-20240914014434776.png)

使用引用GE，Tag取GE中的效果DataType

其中持续时间，应用给拥有者



![image-20240914014523462](./assets/image-20240914014523462.png)

#### Cue

配置GC

![image-20240914015026303](./assets/image-20240914015026303.png)

HUd

![image-20240914021843358](./assets/image-20240914021843358.png) 

抓取Widget的值

### [Dev Cave](https://www.youtube.com/@thegamedevcave)

<font color=#4db8ff>Link：</font>https://www.youtube.com/watch?v=yKLKunEZaj8&list=PLoReGgpfex3woa35rnoXRyF9N3_p7QVQ2&index=2

![image-20240918194318456](./assets/image-20240918194318456.png)

属性集赋值

针对那个类，即使用哪个类作为前缀

```c++
UBasicAttributeSet
```

命名为<font color=#4db8ff>BasicAttributeSet.</font> 加相应的类型

![image-20240918212857915](./assets/image-20240918212857915.png)

![image-20240918212908549](./assets/image-20240918212908549.png)

![image-20240918213229002](./assets/image-20240918213229002.png)

#### Damage

![image-20240919012137363](./assets/image-20240919012137363.png)

随后控制碰撞盒，在蒙太奇和AnimaBluePrint里面

![image-20240919013349376](./assets/image-20240919013349376.png)

![image-20240919013318149](./assets/image-20240919013318149.png)

人物发出信息
![image-20240919013604209](./assets/image-20240919013604209.png)

这时候会传递 到GA里面

![image-20240919013705767](./assets/image-20240919013705767.png)

https://www.youtube.com/watch?v=CoNjS_lMqJ0&list=PLoReGgpfex3woa35rnoXRyF9N3_p7QVQ2&index=6

#### SetByCall

首先是修改GE

![image-20240919141537082](./assets/image-20240919141537082.png)

蓝图中使用

![image-20240919142046825](./assets/image-20240919142046825.png)

#### Input

按键绑定对应的GA

![image-20240919144615975](./assets/image-20240919144615975.png)



修改为C++

![image-20240919154328353](./assets/image-20240919154328353.png)



```c++
for (int index = 0; index < DefaultAbilities.Num(); index++)
{
    TSubclassOf<UGameplayAbility> AbilityClass = DefaultAbilities[index];
    const FGameplayAbilitySpec AbilitySpec(AbilityClass, 1, index);
    AbilitySystemComponent->GiveAbility(AbilitySpec);
}
```





创建一个枚举去存储对应的GA

![image-20240919144924770](./assets/image-20240919144924770.png)

![image-20240919150234539](./assets/image-20240919150234539.png)

![image-20240919154847347](./assets/image-20240919154847347.png)



随后改用枚举调用

![image-20240919150216517](./assets/image-20240919150216517.png)

#### Press Time

![image-20240919151804421](./assets/image-20240919151804421.png)

#### GC

同时也给GC一个Tag

![image-20240919172022407](./assets/image-20240919172022407.png)

在GE中使用GC

![image-20240919171231041](./assets/image-20240919171231041.png)





![image-20240919171544602](./assets/image-20240919171544602.png)



#### GCA

添加 OnActive、OnRemove，在里面激活（active）和不激活（deactive）特效

![image-20240919205543275](./assets/image-20240919205543275.png)



给目标一个状态标签

![image-20240919221352223](./assets/image-20240919221352223.png)



#### Magnitude Modifier Calculations

![image-20240920005726349](./assets/image-20240920005726349.png)

```c++
class DEVCAVE_API UCal_RegenClass : public UGameplayModMagnitudeCalculation
{
	GENERATED_BODY()

	UCal_RegenClass();
	virtual float CalculateBaseMagnitude_Implementation(const FGameplayEffectSpec& Spec) const override;
	
	FGameplayEffectAttributeCaptureDefinition HealthDef;
	FGameplayEffectAttributeCaptureDefinition MaxHealthDef;
};

```



```c++
// Fill out your copyright notice in the Description page of Project Settings.


#include "Cal_RegenClass.h"

#include "DevCave/AblitySystem/BasicAttributeSet.h"

UCal_RegenClass::UCal_RegenClass()
{
	//HealthDef 将捕获和跟踪 "Health" 属性的值。
	HealthDef.AttributeToCapture = UBasicAttributeSet::GetHealthAttribute();
	HealthDef.AttributeSource = EGameplayEffectAttributeCaptureSource::Target;
	//属性值是实时获取的
	HealthDef.bSnapshot = false;

	MaxHealthDef.AttributeToCapture = UBasicAttributeSet::GetMaxHealthAttribute();
	MaxHealthDef.AttributeSource = EGameplayEffectAttributeCaptureSource::Target;
	MaxHealthDef.bSnapshot = false;

	//这意味着当 GameplayEffect 触发时，它将会关注这两个属性。
	RelevantAttributesToCapture.Add(HealthDef);
	RelevantAttributesToCapture.Add(MaxHealthDef);
}

//用于计算一个 GameplayEffect 的基础强度
float UCal_RegenClass::CalculateBaseMagnitude_Implementation(const FGameplayEffectSpec& Spec) const
{
	
	const FGameplayTagContainer* SourceTags = Spec.CapturedSourceTags.GetAggregatedTags();
	const FGameplayTagContainer* TargetTags = Spec.CapturedTargetTags.GetAggregatedTags();

	FAggregatorEvaluateParameters EvaluateParameters;

	EvaluateParameters.SourceTags = SourceTags;
	EvaluateParameters.TargetTags = TargetTags;

	float Health = 0.0f;
	GetCapturedAttributeMagnitude(HealthDef,Spec,EvaluateParameters,Health);
	float MaxHealth = 0.0f;
	GetCapturedAttributeMagnitude(MaxHealthDef,Spec,EvaluateParameters,MaxHealth);

	// if (Health + 1.0f < MaxHealth)
	// {
	// 	return MaxHealth - Health;
	// }
	// return 1.0f;
	
	//返回 * 
	return FMath::Clamp(MaxHealth - Health,0.0f,1.0f);
}

```



随后对应的计算GE，如回复

![image-20240920012359606](./assets/image-20240920012359606.png)

#### Execution Calculation

<font color=#4db8ff>Link：</font>https://www.youtube.com/watch?v=i3n4gwEBWJQ&list=PLoReGgpfex3woa35rnoXRyF9N3_p7QVQ2&index=10

基于其他变量的计算



```c++
class DEVCAVE_API UCalc_exec_Regen : public UGameplayEffectExecutionCalculation
{
	GENERATED_BODY()
	UCalc_exec_Regen();
	virtual void Execute_Implementation(const FGameplayEffectCustomExecutionParameters& ExecutionParams, FGameplayEffectCustomExecutionOutput& OutExecutionOutput) const override;
	
};
```





```c++
// Fill out your copyright notice in the Description page of Project Settings.


#include "Calc_exec_Regen.h"

#include "DevCave/AblitySystem/BasicAttributeSet.h"

struct DamageCapture
{
	//捕获
	DECLARE_ATTRIBUTE_CAPTUREDEF(Health);
	DECLARE_ATTRIBUTE_CAPTUREDEF(MaxHealth);

	DECLARE_ATTRIBUTE_CAPTUREDEF(Mana)

	//定义
	DamageCapture()
	{
		DEFINE_ATTRIBUTE_CAPTUREDEF(UBasicAttributeSet, Health, Target, false);
		DEFINE_ATTRIBUTE_CAPTUREDEF(UBasicAttributeSet, MaxHealth, Target, false);
		DEFINE_ATTRIBUTE_CAPTUREDEF(UBasicAttributeSet, Mana, Source, false);
	}
};

static DamageCapture& GetDamageCapture()
{
	static DamageCapture DamageCapture;
	return DamageCapture;
}

UCalc_exec_Regen::UCalc_exec_Regen()
{
	//添加捕获
	RelevantAttributesToCapture.Add(GetDamageCapture().HealthDef);
	RelevantAttributesToCapture.Add(GetDamageCapture().MaxHealthDef);
	RelevantAttributesToCapture.Add(GetDamageCapture().ManaDef);
}

void UCalc_exec_Regen::Execute_Implementation(const FGameplayEffectCustomExecutionParameters& ExecutionParams,
                                              FGameplayEffectCustomExecutionOutput& OutExecutionOutput) const
{
	Super::Execute_Implementation(ExecutionParams, OutExecutionOutput);


	UAbilitySystemComponent* TargetABSC = ExecutionParams.GetTargetAbilitySystemComponent();
	AActor* TargetActor = TargetABSC ? TargetABSC->GetAvatarActor() : nullptr;


	UAbilitySystemComponent* SourceABSC = ExecutionParams.GetSourceAbilitySystemComponent();
	AActor* SourceActor = SourceABSC ? SourceABSC->GetAvatarActor() : nullptr;

	const FGameplayEffectSpec& Spec = ExecutionParams.GetOwningSpec();
	const FGameplayTagContainer* SourceTags = Spec.CapturedSourceTags.GetAggregatedTags();
	const FGameplayTagContainer* TargetTags = Spec.CapturedTargetTags.GetAggregatedTags();

	FAggregatorEvaluateParameters EvaluateParameters;
	EvaluateParameters.SourceTags = SourceTags;
	EvaluateParameters.TargetTags = TargetTags;


	float Health = 0.0f;
	ExecutionParams.
		AttemptCalculateCapturedAttributeMagnitude(GetDamageCapture().HealthDef, EvaluateParameters, Health);
	float MaxHealth = 0.0f;
	ExecutionParams.AttemptCalculateCapturedAttributeMagnitude(GetDamageCapture().MaxHealthDef, EvaluateParameters,
	                                                           MaxHealth);

	float Mana = 0.0f;
	ExecutionParams.AttemptCalculateCapturedAttributeMagnitude(GetDamageCapture().ManaDef, EvaluateParameters, Mana);

	float HealthToAdd = FMath::Clamp(MaxHealth - Health, 0.0f, 1.0f);


	TargetABSC->ApplyModToAttributeUnsafe(UBasicAttributeSet::GetHealthAttribute(), EGameplayModOp::Additive,
	                                      HealthToAdd);

	// OutExecutionOutput.AddOutputModifier
	// (
	// 	FGameplayModifierEvaluatedData(GetDamageCapture().HealthProperty, EGameplayModOp::Additive, HealthToAdd)
	// );
	OutExecutionOutput.AddOutputModifier
	(
		FGameplayModifierEvaluatedData(GetDamageCapture().ManaProperty, EGameplayModOp::Additive, -HealthToAdd)
	);
}
```

选择对应的计算类

![image-20240920221115765](./assets/image-20240920221115765.png)

可以看到捕获的定义

![image-20240920221133324](./assets/image-20240920221133324.png)
