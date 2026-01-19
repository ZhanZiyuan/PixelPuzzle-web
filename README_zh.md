<p align="center">
    <img alt="favicon" src="./static/images/favicon.svg"
        width="138" />
</p>

# PixelPuzzle-web

<p align="right">
    <a href="./README.md">English</a> | <b>简体中文</b>
</p>

[![GitHub deployments](https://img.shields.io/github/deployments/ZhanZiyuan/PixelPuzzle-web/Production)](https://github.com/ZhanZiyuan/PixelPuzzle-web/blob/main/vercel.json)
[![GitHub last commit](https://img.shields.io/github/last-commit/ZhanZiyuan/PixelPuzzle-web)](https://github.com/ZhanZiyuan/PixelPuzzle-web/commits/main/)
[![GitHub License](https://img.shields.io/github/license/ZhanZiyuan/PixelPuzzle-web)](https://github.com/ZhanZiyuan/PixelPuzzle-web/blob/main/LICENSE)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/ZhanZiyuan/PixelPuzzle-web/total)](https://github.com/ZhanZiyuan/PixelPuzzle-web/releases)
[![Vercel Deploy](https://deploy-badge.vercel.app/vercel/pixelpuzzle-web)](https://pixelpuzzle-web.vercel.app/)

PixelPuzzle-web是一个基于Flask的Web应用程序，专注于图像处理。
它提供了一个简洁的用户界面，用于将图像编码为Base64、将Base64文本解码回图像，以及使用基于种子的算法对图像像素进行安全混淆或还原。

## 功能特性

- **编码 (Encode)**：将任何图像文件转换为Base64编码的文本文件。
- **解码 (Decode)**：从Base64编码的文本文件重建图像。
- **混淆 (Shuffle)**：根据用户提供的数字种子打乱图像的像素。这实际上在视觉上“锁定”了图像内容。
- **还原 (Recover)**：使用正确的种子将混淆后的图像还原为原始图像。

## 技术栈

- **后端**：Python, Flask
- **前端**：HTML5, JavaScript, Tailwind CSS (CDN), Material Design Icons
- **核心逻辑**：[PixelPuzzle](https://github.com/ZhanZiyuan/PixelPuzzle) Python库

## 快速开始

### 前置要求

- Python>=3.10
- pip

### 安装步骤

- 克隆仓库：

   ```bash
   git clone https://github.com/ZhanZiyuan/PixelPuzzle-web.git
   cd PixelPuzzle-web
   ```

- 安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

### 本地运行

- 启动Flask应用：

   ```bash
   python api/app.py
   ```

- 在浏览器中打开：

   ```bash
   http://127.0.0.1:5000
   ```

## 许可证

本项目基于 GPLv3 许可证分发。更多信息请查看 [LICENSE](./LICENSE) 文件。
