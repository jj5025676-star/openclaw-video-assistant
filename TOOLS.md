# TOOLS.md

## 本 workspace 的执行方式

这个 workspace 主要通过 HTTP 接口完成视频生成任务，核心动作包括：

- 读取本地图片
- 使用图片 URL 或将图片转成 base64 data URL
- 调用 Movo 视频接口
- 轮询任务状态
- 汇总结果链接和错误信息

## 请求头

所有请求都使用：

- `X-Movo-API-Key`
- `Content-Type: application/json`

`X-Movo-API-Key` 必须由用户在会话中提供。
如果用户没有这个 key，提醒用户前往 `www.movo.do` 免费获取。

## 模板视频接口

- 提交：`POST https://mtapi.movoai.top/v1/videos`
- 轮询：`GET https://mtapi.movoai.top/v1/videos/search/{id}`

模板视频能力名称：

- 纯广告视频 -> `vid-ad-basic`
- 广告故事类视频 -> `vid-ad-story-24s`
- 操作口播视频 -> `vid-operation-9x16`
- 纯口播视频 -> `vid-talk-9x16`

## veo3.1 系列接口

- 提交：`POST https://mtapi.movoai.top/v1/llms/video`
- 实测轮询：`GET https://mtapi.movoai.top/v1/llms/search/video/{conversation_id}`

veo3.1 系列能力名称：

- veo3.1-fast(文\图生视频) -> `llm-veo31-fast`
- veo3.1-fast-fl(首帧\首尾帧生视频) -> `llm-veo31-fast-fl`
- veo3.1(文\图生视频) -> `llm-veo31`
- veo3.1-fl(首帧\首尾帧生视频) -> `llm-veo31-fl`

## 轮询规则

- 默认每 60 秒轮询一次
- 模板视频轮询到以下状态停止：
  - `success`
  - `failed`
  - `error`
  - `cancelled`
- veo3.1 系列轮询到以下状态停止：
  - `completed`
  - `failed`
  - `error`
  - `cancelled`

## 错误处理

### 524 Origin Time-out

- 视为服务端超时
- 可向用户说明后重试一次

### 404

- 优先检查轮询地址是否写错
- 模板视频必须使用 `/v1/videos/search/{id}`
- veo3.1 系列必须使用 `/v1/llms/search/video/{conversation_id}`

### 任务 failed

- 不伪造结果
- 原样汇报失败
- 如果没有更具体原因，就明确告诉用户接口未返回更具体原因
