<p align="center">
    <img alt="favicon" src="./static/images/favicon.svg"
        width="138" />
</p>

# PixelPuzzle-web

<p align="right">
    <b>English</b> | <a href="./README_zh.md">简体中文</a>
</p>

[![GitHub deployments](https://img.shields.io/github/deployments/ZhanZiyuan/PixelPuzzle-web/Production)](https://github.com/ZhanZiyuan/PixelPuzzle-web/blob/main/vercel.json)
[![GitHub last commit](https://img.shields.io/github/last-commit/ZhanZiyuan/PixelPuzzle-web)](https://github.com/ZhanZiyuan/PixelPuzzle-web/commits/main/)
[![GitHub License](https://img.shields.io/github/license/ZhanZiyuan/PixelPuzzle-web)](https://github.com/ZhanZiyuan/PixelPuzzle-web/blob/main/LICENSE)
[![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/ZhanZiyuan/PixelPuzzle-web/total)](https://github.com/ZhanZiyuan/PixelPuzzle-web/releases)
[![Vercel Deploy](https://deploy-badge.vercel.app/vercel/pixelpuzzle-web)](https://pixelpuzzle-web.vercel.app/)

Pixel Puzzle is a Flask-based web application designed for image manipulation.
It offers a user-friendly interface to encode images to Base64, decode Base64 text back to images, and securely shuffle or recover image pixels using a seed-based algorithm.

## Features

- **Encode**: Convert any image file into a Base64 encoded text file.
- **Decode**: Reconstruct images from Base64 encoded text files.
- **Shuffle**: Scramble the pixels of an image based on a user-provided numeric seed. This essentially "locks" the image visual content.
- **Recover**: Restore the original image from a shuffled version using the correct seed.

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, JavaScript, Tailwind CSS (CDN), Material Design Icons
- **Core Logic**: [PixelPuzzle](https://github.com/ZhanZiyuan/PixelPuzzle) Python library

## Getting Started

### Prerequisites

- Python>=3.10
- pip

### Installation

- Clone the repository:

   ```bash
   git clone https://github.com/ZhanZiyuan/PixelPuzzle-web.git
   cd PixelPuzzle-web
   ```

- Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

- Start the Flask application:

   ```bash
   python api/app.py
   ```

- Open your web browser and navigate to:

   ```bash
   http://127.0.0.1:5000
   ```

## License

Distributed under the GPLv3 License. See [LICENSE](./LICENSE) for more information.
