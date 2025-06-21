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

## 🚀 GitHub Pages 配置（重要！）

### 第一步：手动启用GitHub Pages

**这是必须的步骤，GitHub Actions无法自动启用Pages！**

1. **打开仓库设置页面**：
   ```
   https://github.com/Tyz-Kotono/Tyz-Kotono.github.io/settings/pages
   ```

2. **配置Pages Source**：
   - 在"Source"部分选择 **"GitHub Actions"**
   - **不要**选择"Deploy from a branch"
   - 点击"Save"按钮

3. **验证配置**：
   - 配置完成后，你应该看到"Your site is being built"的消息
   - 等待几分钟让配置生效

### 第二步：推送代码触发部署

配置完成后，当你推送代码到main分支时，GitHub Actions会自动：
1. 安装Python依赖
2. 生成Sphinx文档
3. 构建HTML静态站点
4. 部署到GitHub Pages

### 第三步：访问网站

部署完成后，你的文档将在以下地址可用：
```
https://Tyz-Kotono.github.io/Tyz-Kotono.github.io/
```

## 本地开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行工具

```bash
# 使用批处理文件
.\\run_main.bat

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
│   ├── TreePanel.py       # 左侧树形面板
│   ├── FunctionPanel.py   # 中间功能面板
│   ├── PreviewPanel.py    # 右侧预览面板
│   ├── SphinxTools.py     # Sphinx工具
│   └── GitTools.py        # Git工具
├── Document/              # 文档源文件
│   └── 文档/              # 文档分类
├── jsonFile/              # JSON配置文件
├── sphinx_site/           # Sphinx项目
├── .github/workflows/     # GitHub Actions
└── requirements.txt       # Python依赖
```

## 故障排除

### GitHub Pages 404错误
- 确保已手动启用GitHub Pages
- 检查Actions是否成功运行
- 等待5-10分钟让部署生效

### Actions失败
- 检查Python依赖是否正确安装
- 确保Sphinx配置正确
- 查看Actions日志获取详细错误信息

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 作者

- GitHub: [Tyz-Kotono](https://github.com/Tyz-Kotono)
- 个人网页: [Tyz-Kotono.github.io](https://Tyz-Kotono.github.io)