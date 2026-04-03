# OpenClaw Video Assistant

这是一个 `workspace 型` OpenClaw 视频助理包，不是普通的单 skill 包。

它的正确用法不是把整个目录复制到 `workspace/skills`，而是：

1. 保持整个目录原样存在
2. 新建一个 OpenClaw agent
3. 让这个 agent 的 `workspace` 直接指向当前目录

这样这个 agent 就会把下面这些文件一起当作工作区规则来使用：

- `AGENTS.md`
- `SOUL.md`
- `TOOLS.md`
- `skills/movo_video_generator/SKILL.md`

## 最简单的用法

### 1. 只创建一个本地 agent

在 PowerShell 里进入本目录后执行：

```powershell
.\install_video_agent.ps1
```

默认会创建：

- `agentId = video-agent`

并自动重启 OpenClaw gateway。

### 2. 创建 agent 并绑定到某个现有飞书机器人

```powershell
.\install_video_agent.ps1 -AccountId bot3
```

这会：

- 创建或更新 `video-agent`
- 把该 agent 的 `workspace` 指向当前目录
- 把飞书 `accountId=bot3` 绑定到 `video-agent`
- 重启 OpenClaw gateway

## 更灵活的 Python 方式

```powershell
python .\install_video_agent.py --agent-id video-agent --account-id bot3 --restart
```

可用参数：

- `--agent-id`
- `--account-id`
- `--config`
- `--restart`
- `--no-restart`

## 适合谁

适合：

- 想把这整个目录当成一个独立视频助理 workspace 来用
- 想给某个飞书机器人单独绑一个视频生成 agent

不适合：

- 直接把整个目录当普通 skill 安装到 `workspace/skills`

## 当前生效原理

安装器会自动修改当前 OpenClaw 生效配置：

- WSL2 配置文件：`/home/z852963/.openclaw/openclaw.json`

它会：

1. 在 `agents.list` 中新增或更新一个 agent
2. 把 `workspace` 指向当前目录
3. 如果你传了 `accountId`，就新增或更新对应 `bindings`
4. 重启 `openclaw-gateway.service`

## 推荐方式

从用户角度，最简单的方式就是：

```powershell
.\install_video_agent.ps1 -AccountId bot3
```

前提是：

- `bot3` 已经是 OpenClaw 当前配置里存在的飞书账号
- WSL2 里的 OpenClaw 正在作为正式运行环境
