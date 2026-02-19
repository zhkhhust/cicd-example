# CICD Example

一个使用GitHub Actions做CICD的例子

视频地址： https://www.bilibili.com/video/BV1jNSEBiE6D

## Flask REST API 服务

本项目包含一个简单的 Flask REST API 服务，具有完整的 CRUD 操作和测试用例。

### 功能特性

- ✅ RESTful API 设计
- ✅ 完整的 CRUD 操作（创建、读取、更新、删除）
- ✅ 全面的单元测试（15个测试用例）
- ✅ GitHub Actions CI/CD 集成

### API 端点

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/` | 首页，显示API文档 |
| GET | `/items` | 获取所有项目 |
| POST | `/items` | 创建新项目（需要JSON: `{"name": "...", "description": "..."}`）|
| GET | `/items/<id>` | 根据ID获取项目 |
| PUT | `/items/<id>` | 更新项目（需要JSON: `{"name": "...", "description": "..."}`）|
| DELETE | `/items/<id>` | 删除项目 |

### 快速开始

#### 1. 安装依赖

```bash
uv sync
```

#### 2. 运行 Flask 服务器

```bash
uv run python main.py
```

服务器将在 `http://localhost:5000` 启动。

#### 3. 运行测试

```bash
uv run pytest tests/test_main.py -v
```

### 测试覆盖

项目包含 15 个全面的测试用例，覆盖以下场景：

- ✅ 首页端点测试
- ✅ 创建项目测试（成功、缺少字段、空请求体）
- ✅ 获取所有项目测试（空列表、有数据）
- ✅ 根据ID获取项目测试（成功、未找到）
- ✅ 更新项目测试（更新名称、描述、两者、未找到）
- ✅ 删除项目测试（成功、未找到）

### 使用示例

#### 创建项目

```bash
curl -X POST http://localhost:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "我的项目", "description": "这是一个测试项目"}'
```

#### 获取所有项目

```bash
curl http://localhost:5000/items
```

#### 更新项目

```bash
curl -X PUT http://localhost:5000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "更新后的名称"}'
```

#### 删除项目

```bash
curl -X DELETE http://localhost:5000/items/1
```

### CI/CD

项目使用 GitHub Actions 进行持续集成和测试。每次代码推送时，都会自动运行测试套件。

### 技术栈

- **Flask** - Python Web 框架
- **pytest** - 测试框架
- **uv** - Python 包管理器
