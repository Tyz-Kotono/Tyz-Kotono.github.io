





```c++

Unhandled Exception: EXCEPTION_ACCESS_VIOLATION reading address 0x0000000000000008

UnrealEditor_SteamAudio!FSteamAudioReverbSubmixPlugin::LazyInit() [E:\UE\SteamAudioUE554\Plugins\SteamAudio\Source\SteamAudio\Private\SteamAudioReverb.cpp:535]
UnrealEditor_SteamAudio!FSteamAudioReverbSubmixPlugin::OnProcessAudio() [E:\UE\SteamAudioUE554\Plugins\SteamAudio\Source\SteamAudio\Private\SteamAudioReverb.cpp:750]
UnrealEditor_Engine!FSoundEffectSubmix::ProcessAudio() [D:\build\++UE5\Sync\Engine\Source\Runtime\Engine\Private\SoundEffectSubmix.cpp:23]
UnrealEditor_AudioMixer!Audio::FMixerSubmix::GenerateEffectChainAudio() [D:\build\++UE5\Sync\Engine\Source\Runtime\AudioMixer\Private\AudioMixerSubmix.cpp:1717]
UnrealEditor_AudioMixer!Audio::FMixerSubmix::ProcessAudio() [D:\build\++UE5\Sync\Engine\Source\Runtime\AudioMixer\Private\AudioMixerSubmix.cpp:1414]
UnrealEditor_AudioMixer!Audio::FMixerSubmix::ProcessAudio() [D:\build\++UE5\Sync\Engine\Source\Runtime\AudioMixer\Private\AudioMixerSubmix.cpp:1306]
UnrealEditor_AudioMixer!Audio::FMixerDevice::OnProcessAudioStream() [D:\build\++UE5\Sync\Engine\Source\Runtime\AudioMixer\Private\AudioMixerDevice.cpp:960]
UnrealEditor_AudioMixerCore!Audio::FOutputBuffer::MixNextBuffer() [D:\build\++UE5\Sync\Engine\Source\Runtime\AudioMixerCore\Private\AudioMixer.cpp:230]
UnrealEditor_AudioMixerCore!Audio::IAudioMixerPlatformInterface::RunInternal() [D:\build\++UE5\Sync\Engine\Source\Runtime\AudioMixerCore\Private\AudioMixer.cpp:730]
UnrealEditor_AudioMixerCore!Audio::IAudioMixerPlatformInterface::Run() [D:\build\++UE5\Sync\Engine\Source\Runtime\AudioMixerCore\Private\AudioMixer.cpp:778]
UnrealEditor_Core!FRunnableThreadWin::Run() [D:\build\++UE5\Sync\Engine\Source\Runtime\Core\Private\Windows\WindowsRunnableThread.cpp:159]
```

