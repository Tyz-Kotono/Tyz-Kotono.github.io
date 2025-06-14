@echo off
SET "PYTHON_EXECUTABLE=python"

REM 检查Python是否在PATH中，如果不在，尝试常见路径
where /q %PYTHON_EXECUTABLE%
if %errorlevel% neq 0 (
    SET "PYTHON_EXECUTABLE=C:\Python\Python3x\python.exe" REM 替换为你的Python实际安装路径，例如 C:\Python39\python.exe
    where /q %PYTHON_EXECUTABLE%
    if %errorlevel% neq 0 (
        echo 错误：未找到Python解释器。请确保Python已安装并添加到PATH，或修改run_sync.bat中的PYTHON_EXECUTABLE路径。
        pause
        exit /b 1
    )
)

REM 切换到脚本所在目录（如果当前目录不是项目根目录）
pushd "%~dp0"

REM 切换到项目根目录（如果脚本不在项目根目录）
cd ..

REM 运行Python同步脚本
%PYTHON_EXECUTABLE% Script\sync_hugo_content.py

REM 返回原始目录
popd

pause 