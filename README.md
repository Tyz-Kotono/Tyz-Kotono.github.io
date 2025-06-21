[![avatar](https://github.com/Tyz-Kotono.png?size=100)](https://github.com/Tyz-Kotono)

**GitHub昵称**：Tyz-Kotono  
**个人主页**：[https://tyz-kotono.github.io](https://tyz-kotono.github.io)

---

# Tyz-Kotono.github.io

[访问我的博客主页](https://tyz-kotono.github.io/)

![GitHub 头像](https://github.com/Tyz-Kotono.png)

GitHub ID: Tyz-Kotono

# Blog 分类管理工具

一个基于PySide6的文档分类管理工具，支持Sphinx文档生成和GitHub Pages部署。

## 功能特性

- 📁 文档分类管理
- 📝 Markdown文件解析和Typora大纲生成
- 🎨 UE风格的文档界面
- 📚 Sphinx文档自动生成
- 🌐 GitHub Pages自动部署
- 🔧 本地预览和测试

## GitHub Pages 配置

### 1. 仓库设置

1. 进入你的GitHub仓库设置页面
2. 找到 "Pages" 选项
3. 在 "Source" 部分选择 "GitHub Actions"

### 2. 分支保护

确保 `main` 分支受到保护，只有通过Pull Request才能合并代码。

### 3. 自动部署

当你推送代码到 `main` 分支时，GitHub Actions会自动：
1. 安装Python依赖
2. 生成Sphinx文档
3. 构建HTML静态站点
4. 部署到GitHub Pages

### 4. 访问地址

部署完成后，你的文档将在以下地址可用：
`https://[你的用户名].github.io/[仓库名]/`

## 本地开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行工具

```bash
# 使用批处理文件
.\run_main.bat

# 或直接运行
cd Python
python main.py
```

### 本地预览

1. 点击"生成Sphinx文档"
2. 点击"构建Sphinx静态站点"
3. 点击"本地预览Sphinx网页"

## 项目结构

```
├── Python/                 # Python源代码
│   ├── main.py            # 主程序
│   ├── DataJsonManager.py # 数据管理
│   ├── TreePanel.py       # 分类树面板
│   ├── FunctionPanel.py   # 功能面板
│   ├── PreviewPanel.py    # 预览面板
│   ├── SphinxTools.py     # Sphinx工具
│   └── GitTools.py        # Git工具
├── Document/              # 文档目录
├── jsonFile/              # JSON配置文件
├── sphinx_site/           # Sphinx站点
├── .github/workflows/     # GitHub Actions
└── requirements.txt       # Python依赖
```

## 作者

- GitHub: [Tyz-Kotono](https://github.com/Tyz-Kotono)
- 个人网页: [Tyz-Kotono.github.io](https://Tyz-Kotono.github.io)