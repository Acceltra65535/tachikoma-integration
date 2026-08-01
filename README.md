# 🤖 Telegram OAuth Auth Bot

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

一个轻量、安全且易于集成的 **Telegram Bot 身份验证与 OAuth 登录系统**。支持通过 Telegram 进行无密码登录验证、用户授权请求以及第三方系统（如 Web / App）的身份对接。

---

## ✨ 核心特性

* 🔐 **安全校验**：基于 Telegram 官方标准校验机制（HMAC-SHA-256）防篡改。
* 🚀 **即插即用**：轻松集成到现有 Web / Mobile 项目作为第三方登录方式。
* 📲 **双向授权流程**：
  * **Web 登录 Widget**：通过 Telegram 官方 Login Widget 一键登录。
  * **Bot 智能交互**：支持通过 Bot 发送一次性登录验证指令（One-Time Login Request）。
* 🛡️ **JWT 支持**：验证成功后自动签发 JWT Token，方便前端进行状态持久化。
* 🌐 **多端适配**：支持 Webhook 或长轮询（Long Polling）模式。

---

## 🛠️ 技术栈

* **语言/框架**：[如：Node.js / Python FastAPI / Go]
* **Telegram SDK**：[如：Telegraf / python-telegram-bot / Telebot]
* **认证标准**：Telegram Login / OAuth 2.0 / JWT

---

## 🚀 快速开始

### 1. 前置准备

在启动项目之前，你需要先在 Telegram 中创建一个 Bot：

1. 打开 Telegram 并搜索 [@BotFather](https://t.me/BotFather)。
2. 发送 `/newbot` 指令，按照提示创建一个新的机器人，获取 **Bot Token**。
3. 如果需要使用 Telegram Web Login 功能，请向 BotFather 发送 `/setdomain` 并关联你的域名。

---

### 2. 本地安装

克隆仓库并安装依赖：

```bash
# 克隆项目
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

# 安装依赖 (以 Node.js 为例)
npm install
```

---

### 3. 环境配置

在项目根目录下创建 `.env` 文件，填充以下变量：

```env
# 服务端口
PORT=3000

# Telegram Bot 配置
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyZ
TELEGRAM_BOT_USERNAME=your_bot_username

# 安全配置
JWT_SECRET=your_super_secret_jwt_key
ALLOWED_ORIGINS=http://localhost:3000,[https://yourdomain.com](https://yourdomain.com)
```

---

### 4. 启动项目

```bash
# 开发模式
npm run dev

# 生产模式
npm start
```

---

## 🔄 认证流程

```
[ 用户 / 前端 ] --(1) 发起登录请求 --> [ 本服务 API / Bot ]
                                            |
[ 用户 ] <--(2) 在 Telegram 中确认授权 ------+
    |
    +--(3) 发送加密验证数据 --> [ 本服务 Backend ]
                                     |
                             (4) 校验数据合法性 (HMAC-SHA-256)
                                     |
[ 用户 ] <--(5) 返回 JWT / Session --+
```

1. **前端交互**：用户点击“使用 Telegram 登录”或向 Bot 发送登录请求。
2. **身份授权**：Telegram 弹出授权确认窗口或 Bot 向用户发送确认按钮。
3. **哈希签名校验**：后端接收 Telegram 返回的字段（`id`, `first_name`, `hash` 等），使用 `BOT_TOKEN` 计算 SHA-256 哈希值比对，确保数据未被伪造。
4. **颁发凭证**：校验通过后注册或登录用户，并向客户端返回 JWT。

---

## 📖 API 接口说明

### 1. Telegram 数据校验 & 登录
* **URL**: `/api/auth/telegram`
* **Method**: `POST`
* **请求体 (Body)**:
  ```json
  {
    "id": 123456789,
    "first_name": "John",
    "username": "john_doe",
    "auth_date": 1672531199,
    "hash": "c1f7a7..."
  }
  ```
* **响应示例**:
  ```json
  {
    "code": 200,
    "message": "Auth successful",
    "data": {
      "token": "eyJhbGciOiJIUzI1NiIsIn...",
      "user": {
        "telegramId": 123456789,
        "username": "john_doe"
      }
    }
  }
  ```

---

## 🛡️ 安全性说明

* **防重放攻击**：服务端会自动校验 `auth_date` 时间戳，超过设定时效（默认 86400 秒）的请求将被拦截。
* **密钥保护**：切勿将 `TELEGRAM_BOT_TOKEN` 和 `JWT_SECRET` 泄露提交到版本控制系统中。

---
