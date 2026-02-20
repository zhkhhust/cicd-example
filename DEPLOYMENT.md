# Flask 应用部署说明

## 部署方式

本部署使用 **Docker 容器**来运行 Flask 服务，确保服务的持续运行和易于管理。

## 工作原理

### 为什么使用 Docker？

- ✅ **环境隔离**：容器化应用，避免环境冲突
- ✅ **进程持久化**：容器中的进程持续运行，即使启动它的进程退出
- ✅ **自动重启**：配置了 `--restart unless-stopped` 策略，容器崩溃或系统重启后自动恢复
- ✅ **易于管理**：使用标准 Docker 命令即可管理
- ✅ **可移植性**：同样的容器可以在任何支持 Docker 的环境中运行

## 自动部署

部署通过 GitHub Actions 自动触发：

```bash
# 推送到 main 分支时自动部署
git push origin main

# 或手动触发
# 在 GitHub Actions 页面点击 "Run workflow"
```

## 手动管理服务

### 查看运行中的容器

```bash
docker ps
```

输出示例：
```
CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS         PORTS                    NAMES
abc123         flask-app:latest  "uv run python main.py"  10 seconds ago  Up 9 seconds   0.0.0.0:5000->5000/tcp   flask-app
```

### 查看容器日志

```bash
# 查看所有日志
docker logs flask-app

# 实时查看日志
docker logs -f flask-app

# 查看最近 100 行日志
docker logs --tail 100 flask-app
```

### 停止 Flask 服务

```bash
# 停止容器
docker stop flask-app

# 停止并删除容器
docker stop flask-app && docker rm flask-app
```

### 启动 Flask 服务（手动）

```bash
# 使用已存在的镜像启动
docker run -d \
  --name flask-app \
  --restart unless-stopped \
  -p 5000:5000 \
  flask-app:latest

# 或重新构建并启动
docker build -t flask-app:latest .
docker run -d \
  --name flask-app \
  --restart unless-stopped \
  -p 5000:5000 \
  flask-app:latest
```

### 重启服务

```bash
docker restart flask-app
```

## 服务信息

- **容器名称**: flask-app
- **镜像名称**: flask-app:latest
- **URL**: http://localhost:5000
- **主机**: 0.0.0.0（监听所有网络接口）
- **端口**: 5000（宿主机）→ 5000（容器）

## Docker 容器配置

- **重启策略**: `unless-stopped` - 容器崩溃时自动重启，除非手动停止
- **端口映射**: `-p 5000:5000` - 将宿主机的 5000 端口映射到容器的 5000 端口
- **运行模式**: `-d` - 后台运行（detached mode）

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

1. 检查容器是否运行：
   ```bash
   docker ps | grep flask-app
   ```

2. 检查容器状态（包括停止的容器）：
   ```bash
   docker ps -a | grep flask-app
   ```

3. 查看容器日志：
   ```bash
   docker logs flask-app
   ```

4. 实时查看容器日志：
   ```bash
   docker logs -f flask-app
   ```

5. 检查端口是否被占用：
   ```bash
   lsof -i :5000
   # 或
   netstat -tlnp | grep 5000
   ```

6. 进入容器内部调试：
   ```bash
   docker exec -it flask-app bash
   ```

### 容器启动失败

1. 查看容器退出状态：
   ```bash
   docker inspect flask-app --format='{{.State.Status}}'
   ```

2. 查看完整日志：
   ```bash
   docker logs flask-app
   ```

3. 重新构建镜像：
   ```bash
   docker build -t flask-app:latest .
   ```

4. 手动运行容器进行调试：
   ```bash
   docker run -it --rm -p 5000:5000 flask-app:latest
   ```

### 如果 Docker 未安装

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io

# CentOS/RHEL
sudo yum install docker

# 启动 Docker 服务
sudo systemctl start docker
sudo systemctl enable docker

# 将当前用户添加到 docker 组（避免每次使用 sudo）
sudo usermod -aG docker $USER
# 需要重新登录才能生效
```

## 开发环境

本地开发时直接运行：
```bash
uv run python main.py
```

服务会在前台运行，便于调试。

## Docker 部署流程

部署工作流会自动执行以下步骤：

1. ✅ **停止旧容器**：停止并删除名为 `flask-app` 的旧容器
2. ✅ **删除旧镜像**：删除旧的 `flask-app:latest` 镜像
3. ✅ **构建新镜像**：使用 Dockerfile 构建新镜像
4. ✅ **启动新容器**：使用新镜像启动容器，配置自动重启
5. ✅ **等待启动**：等待 5 秒让服务完全启动
6. ✅ **验证服务**：检查容器状态和日志
7. ✅ **健康检查**：测试 API 端点是否可访问
8. ✅ **API 测试**：测试所有主要端点

部署完成后，容器会持续运行，即使 GitHub Actions workflow 完成。
