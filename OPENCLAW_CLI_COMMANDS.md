# OpenClaw CLI 命令与消息模板

## 1. 进入 workspace

```powershell
cd D:\codeX\openclaw-video-assistant
```

## 2. 启动 OpenClaw CLI

```powershell
openclaw agent
```

## 3. 在 OpenClaw CLI 里可直接发送的启动文字

```text
请把当前 workspace 作为一个视频助手 agent 来工作。

先读取并加载以下文件：
1. AGENTS.md
2. SOUL.md
3. TOOLS.md
4. skills/movo_video_generator/SKILL.md

从现在开始，所有生视频任务都按这些文件执行。
执行原则是：
- 先理解用户需求
- 在执行前先做一次简短确认
- 没有 X-Movo-API-Key 不发起请求
- 如果用户没有 X-Movo-API-Key，提醒其前往 www.movo.do 免费获取
- 不要硬编码任何真实密钥
- 模板视频与 veo3.1 系列使用各自正确的轮询地址
- 返回真实任务 ID、状态、视频链接或错误原因

请先告诉我你已经加载完成，并列出你当前可用的视频能力名称：
- 纯广告视频
- 广告故事类视频
- 操作口播视频
- 纯口播视频
- veo3.1-fast(文\图生视频)
- veo3.1-fast-fl(首帧\首尾帧生视频)
- veo3.1(文\图生视频)
- veo3.1-fl(首帧\首尾帧生视频)
```

## 4. 如果要直接开始任务，可发送这段

```text
我的 X-Movo-API-Key 是：<请填写你的 X-Movo-API-Key>

我现在要生成一个视频。
请你先理解我的需求并用一句话复述，然后告诉我你建议使用哪个能力或模型。
在我确认之前不要执行。
确认后再按 skill 文档发起请求，并每 60 秒轮询一次。
最后返回：
1. 使用的能力或模型
2. 提交返回的任务 ID
3. 最终状态
4. 视频链接或失败原因
```

## 5. 单图 9:16 视频模板

```text
我的 X-Movo-API-Key 是：<请填写你的 X-Movo-API-Key>

我刚上传了一张图片，请先理解我的需求并确认。
如果没有额外首帧要求，优先建议使用 veo3.1-fast(文\图生视频)，尺寸 720x1280。
如果你判断更适合首帧模式，请先说明原因并等我确认。
确认后再执行，并每 60 秒轮询一次。
最后返回 message_id、user_sequence_id、conversation_id、最终状态和视频链接。
```
