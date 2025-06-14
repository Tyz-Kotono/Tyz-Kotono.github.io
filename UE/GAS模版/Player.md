

#### 1、Player

```c++
class UAbilitySystemComponent;
class UInputAction;
class UInputMappingContext;
class UCameraComponent;
class USpringArmComponent;


UCLASS()
class DEVCAVE_API AGASTutorialBasicCharacter : public ACharacter,public IAbilitySystemInterface
{
	GENERATED_BODY()

	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
	TObjectPtr<USpringArmComponent> CameraBoom;
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Camera", meta = (AllowPrivateAccess = "true"))
	TObjectPtr<UCameraComponent> FollowCamera;

public:
	AGASTutorialBasicCharacter();

protected:
	
	UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "GAS", meta = (AllowPrivateAccess = "true"))
	TObjectPtr<UAbilitySystemComponent> AbilitySystemComponent;

	
	
	virtual void SetupPlayerInputComponent(class UInputComponent* PlayerInputComponent) override;
	virtual void BeginPlay() override;

public:	
	virtual void Tick(float DeltaTime) override;

	virtual UAbilitySystemComponent* GetAbilitySystemComponent() const override{return AbilitySystemComponent;}

	FORCEINLINE class USpringArmComponent* GetCameraBoom() const {return CameraBoom;}

	FORCEINLINE class UCameraComponent* GetCamera() const {return FollowCamera;}
};

```





```c++
// Fill out your copyright notice in the Description page of Project Settings.


#include "GASTutorialBasicCharacter.h"
#include "AbilitySystemComponent.h"
#include "Camera/CameraComponent.h"
#include "Components/CapsuleComponent.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/SpringArmComponent.h"

// Sets default values
AGASTutorialBasicCharacter::AGASTutorialBasicCharacter()
{
	PrimaryActorTick.bCanEverTick = true;
	GetCapsuleComponent()->InitCapsuleSize(42.f,96.f);

	bUseControllerRotationPitch = false;
	bUseControllerRotationYaw = false;
	bUseControllerRotationRoll = false;

	
	GetCharacterMovement()->bOrientRotationToMovement = true;	//角色移动方向为输入
	GetCharacterMovement()->RotationRate = FRotator(0.0,500.0f,0.0f);

	GetCharacterMovement()->JumpZVelocity = 700.0f;
	GetCharacterMovement()->AirControl = 0.35f;
	GetCharacterMovement()->MaxWalkSpeed = 500.0f;
	GetCharacterMovement()->MinAnalogWalkSpeed = 20.0f;
	GetCharacterMovement()->BrakingDecelerationWalking = 2000.0f;

	CameraBoom = CreateDefaultSubobject<USpringArmComponent>(TEXT("CameraBoom"));
	CameraBoom->SetupAttachment(RootComponent);
	CameraBoom->TargetArmLength = 400.0f;
	CameraBoom->bUsePawnControlRotation = true;

	FollowCamera = CreateDefaultSubobject<UCameraComponent>(TEXT("FollowCamera"));
	FollowCamera->SetupAttachment(CameraBoom,USpringArmComponent::SocketName);
	FollowCamera->bUsePawnControlRotation = false;

	AbilitySystemComponent = CreateDefaultSubobject<UAbilitySystemComponent>(TEXT("AbilitySystemComponent"));
}

// Called when the game starts or when spawned
void AGASTutorialBasicCharacter::BeginPlay()
{
	Super::BeginPlay();
	
}


// Called every frame
void AGASTutorialBasicCharacter::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);
}

// Called to bind functionality to input
void AGASTutorialBasicCharacter::SetupPlayerInputComponent(UInputComponent* PlayerInputComponent)
{
	Super::SetupPlayerInputComponent(PlayerInputComponent);
}


```



#### 2、Ability

```c++
UPROPERTY(EditDefaultsOnly, Category = "GAS")
TArray<TSubclassOf<UGameplayAbility>> DefaultAbilities;

void GiveDefaultAbilities();
```



```c++
void AGASTutorialBasicCharacter::GiveDefaultAbilities()
{
	check(AbilitySystemComponent);
	if (!HasAuthority()) return;

	for (TSubclassOf<UGameplayAbility> AbilityClass : DefaultAbilities)
	{
		const FGameplayAbilitySpec AbilitySpec(AbilityClass, 1);
		AbilitySystemComponent->GiveAbility(AbilitySpec);
	}
}

```





#### 3、UAttributeSet

```c++
#define ATTRIBUTE_ACCESSORS(ClassName, PropertyName) \
GAMEPLAYATTRIBUTE_PROPERTY_GETTER(ClassName, PropertyName) \
GAMEPLAYATTRIBUTE_VALUE_GETTER(PropertyName) \
GAMEPLAYATTRIBUTE_VALUE_SETTER(PropertyName) \
GAMEPLAYATTRIBUTE_VALUE_INITTER(PropertyName)


// 用于设置网络复制的属性和条件。这个宏告诉 Unreal Engine 的网络系统，
// 哪些属性需要在网络上进行复制，并且在什么条件下进行复制
virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;
//在属性值改变之前被调用。这个函数接收两个参数：一个是将要改变的属性，另一个是新的属性值
virtual void PreAttributeChange(const FGameplayAttribute& Attribute, float& NewValue) override;

// 它在游戏效果（Gameplay Effect）执行之后被调用，这时候属性值已经实际改变了
virtual void PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data) override;

//ReplicatedUsing 通过网络更新时调用的回调函数
UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_Health, Category = "Ability | Gameplay Attribute")
FGameplayAttributeData Health;
ATTRIBUTE_ACCESSORS(UFabAttributeSet, Health);

UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_MaxHealth, Category = "Ability | Gameplay Attribute")
FGameplayAttributeData MaxHealth;
ATTRIBUTE_ACCESSORS(UFabAttributeSet, MaxHealth);

UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_Stamina, Category = "Ability | Gameplay Attribute")
FGameplayAttributeData Stamina;
ATTRIBUTE_ACCESSORS(UFabAttributeSet, Stamina);

UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_MaxStamina, Category = "Ability | Gameplay Attribute")
FGameplayAttributeData MaxStamina;
ATTRIBUTE_ACCESSORS(UFabAttributeSet, MaxStamina);

UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_Strength, Category = "Ability | Gameplay Attribute")
FGameplayAttributeData Strength;
ATTRIBUTE_ACCESSORS(UFabAttributeSet, Strength);

UPROPERTY(BlueprintReadOnly, ReplicatedUsing = OnRep_MaxStrength, Category = "Ability | Gameplay Attribute")
FGameplayAttributeData MaxStrength;
ATTRIBUTE_ACCESSORS(UFabAttributeSet, MaxStrength);


//ReplicatedUsing 通过网络更新时调用的回调函数
UFUNCTION()
void OnRep_Health(const FGameplayAttributeData& OldHealth) const;

UFUNCTION()
void OnRep_MaxHealth(const FGameplayAttributeData& OldMaxHealth) const;

UFUNCTION()
void OnRep_Stamina(const FGameplayAttributeData& OldStamina) const;

UFUNCTION()
void OnRep_MaxStamina(const FGameplayAttributeData& OldMaxStamina) const;

UFUNCTION()
void OnRep_Strength(const FGameplayAttributeData& OldStamina) const;

UFUNCTION()
void OnRep_MaxStrength(const FGameplayAttributeData& OldMaxStamina) const;
```

Cpp

```c++
UBasicAttributeSet::UBasicAttributeSet()
{
	InitHealth(80.f);
}

// 用于设置网络复制的属性和条件。这个宏告诉 Unreal Engine 的网络系统，
// 哪些属性需要在网络上进行复制，并且在什么条件下进行复制
void UBasicAttributeSet::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
	Super::GetLifetimeReplicatedProps(OutLifetimeProps);
	
	DOREPLIFETIME_CONDITION_NOTIFY(UBasicAttributeSet, Health, COND_None, REPNOTIFY_Always);
	DOREPLIFETIME_CONDITION_NOTIFY(UBasicAttributeSet, MaxHealth, COND_None, REPNOTIFY_Always);
	DOREPLIFETIME_CONDITION_NOTIFY(UBasicAttributeSet, Stamina, COND_None, REPNOTIFY_Always);
	DOREPLIFETIME_CONDITION_NOTIFY(UBasicAttributeSet, MaxStamina, COND_None, REPNOTIFY_Always);
	DOREPLIFETIME_CONDITION_NOTIFY(UBasicAttributeSet, Strength, COND_None, REPNOTIFY_Always);
	DOREPLIFETIME_CONDITION_NOTIFY(UBasicAttributeSet, MaxStrength, COND_None, REPNOTIFY_Always);
}

//在属性值改变之前被调用。这个函数接收两个参数：一个是将要改变的属性，另一个是新的属性值
void UBasicAttributeSet::PreAttributeChange(const FGameplayAttribute& Attribute, float& NewValue)
{
	Super::PreAttributeChange(Attribute, NewValue);

	if(Attribute == GetHealthAttribute())
	{
		NewValue = FMath::Clamp(NewValue, 0.f, GetMaxHealth());
	}
}

//// 它在游戏效果（Gameplay Effect）执行之后被调用，这时候属性值已经实际改变了
void UBasicAttributeSet::PostGameplayEffectExecute(const FGameplayEffectModCallbackData& Data)
{
	Super::PostGameplayEffectExecute(Data);
	//用来获取游戏效果修改的相关信息的情况
	if(Data.EvaluatedData.Attribute == GetHealthAttribute())
	{
		SetHealth(FMath::Clamp(GetHealth(), 0.f, GetMaxHealth()));
	}

	//发起
	// UAbilitySystemComponent* ASC = Data.EffectSpec.GetContext().GetInstigatorAbilitySystemComponent();
	// AActor* ASCOwner = ASC->AbilityActorInfo->OwnerActor.Get();
	// ASCOwner->GetActorLocation();
}

void UBasicAttributeSet::OnRep_Health(const FGameplayAttributeData& OldHealth) const
{
		//用于生成网络属性复制的通知函数
	GAMEPLAYATTRIBUTE_REPNOTIFY(UBasicAttributeSet, Health, OldHealth);
}

void UBasicAttributeSet::OnRep_MaxHealth(const FGameplayAttributeData& OldMaxHealth) const
{
	GAMEPLAYATTRIBUTE_REPNOTIFY(UBasicAttributeSet, MaxHealth, OldMaxHealth);
}

void UBasicAttributeSet::OnRep_Stamina(const FGameplayAttributeData& OldStamina) const
{
	GAMEPLAYATTRIBUTE_REPNOTIFY(UBasicAttributeSet, Stamina, OldStamina);
}

void UBasicAttributeSet::OnRep_MaxStamina(const FGameplayAttributeData& OldMaxStamina) const
{
	GAMEPLAYATTRIBUTE_REPNOTIFY(UBasicAttributeSet, MaxStamina, OldMaxStamina);
}

void UBasicAttributeSet::OnRep_Strength(const FGameplayAttributeData& OldStrength) const
{
	GAMEPLAYATTRIBUTE_REPNOTIFY(UBasicAttributeSet, Strength, OldStrength);
}

void UBasicAttributeSet::OnRep_MaxStrength(const FGameplayAttributeData& OldMaxStrength) const
{
	GAMEPLAYATTRIBUTE_REPNOTIFY(UBasicAttributeSet, MaxStrength, OldMaxStrength);
}

```

