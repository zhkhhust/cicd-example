# Flask 应用部署说明

## 部署方式

本部署使用 **GNU Screen** 会话来保持 Flask 服务持续运行，无需 sudo 权限。

## 工作原理

### 为什么使用 Screen？

- ✅ **无需 sudo 权限**：普通用户即可使用
- ✅ **进程持久化**：Screen 会话中的进程会持续运行，即使启动它的进程退出
- ✅ **易于管理**：可以随时重新连接查看日志或停止服务
- ✅ **标准工具**：Screen 是 Linux 标准工具，通常已预装

## 自动部署

部署通过 GitHub Actions 自动触发：

```bash
# 推送到 main 分支时自动部署
git push origin main

# 或手动触发
# 在 GitHub Actions 页面点击 "Run workflow"
```

## 手动管理服务

### 查看运行中的 Screen 会话

```bash
screen -list
```

输出示例：
```
There is a screen on:
    12345.flask-app   (Detached)
```

### 连接到 Flask 服务会话

```bash
screen -r flask-app
```

在会话中可以看到：
- Flask 服务器输出
- 访问日志
- 错误信息

### 断开 Screen 会话（不停止服务）

在会话中按 `Ctrl+A` 然后按 `D`

### 停止 Flask 服务

```bash
# 方法 1: 使用 screen 命令
screen -S flask-app -X quit

# 方法 2: 手动停止进程
kill $(cat server.pid)

# 方法 3: 停止占用 5000 端口的进程
lsof -ti:5000 | xargs kill -9
```

### 启动 Flask 服务（手动）

```bash
# 在 screen 会话中启动
screen -dmS flask-app bash -c "uv run python main.py > flask_server.log 2>&1"
```

## 日志文件

服务器日志保存在：
- `flask_server.log` - 标准输出日志
- `flask_server_error.log` - 错误日志（如果使用 systemd）

查看日志：
```bash
# 查看完整日志
cat flask_server.log

# 实时查看日志
tail -f flask_server.log

# 查看最近 100 行
tail -n 100 flask_server.log
```

## 服务信息

- **URL**: http://localhost:5000
- **主机**: 0.0.0.0（监听所有网络接口）
- **端口**: 5000

## API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | 首页，显示可用端点列表 |
| GET | `/items` | 获取所有项目 |
| POST | `/items` | 创建新项目（需要 JSON body: `{"name": "...", "description": "..."}`） |
| GET | `/items/<id>` | 根据 ID 获取项目 |
| PUT | `/items/<id>` | 更新项目（需要 JSON body） |
| DELETE | `/items/<id>` | 删除项目 |

## 测试 API

```bash
# 测试首页
curl http://localhost:5000/

# 创建项目
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "description": "Test item"}'

# 获取所有项目
curl http://localhost:5000/items

# 获取特定项目
curl http://localhost:5000/items/1

# 更新项目
curl -X PUT http://localhost:5000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated", "description": "Updated description"}'

# 删除项目
curl -X DELETE http://localhost:5000/items/1
```

## 故障排查

### 服务无法访问

1. 检查 screen 会话是否存在：
   ```bash
   screen -list | grep flask-app
   ```

2. 检查端口是否被占用：
   ```bash
   lsof -i :5000
   ```

3. 检查进程是否运行：
   ```bash
   ps aux | grep "python main.py"
   ```

4. 查看日志文件：
   ```bash
   cat flask_server.log
   ```

### 如果 screen 未安装

```bash
# Ubuntu/Debian
sudo apt-get install screen

# CentOS/RHEL
sudo yum install screen

# Fedora
sudo dnf install screen
```

## 开发环境

本地开发时直接运行：
```bash
uv run python main.py
```

服务会在前台运行，便于调试。