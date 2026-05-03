# 对话触发

`trigger_chat` 是一个 AstrBot 群聊触发插件，用于在群聊中通过关键词或单独 @ 机器人触发 AstrBot 默认 LLM 对话流程。

插件本身不直接回复消息，而是把符合条件的群聊消息转换成 AstrBot 默认聊天请求，由 AstrBot 的 LLM 和回复流程继续处理。

## 功能

- 支持群聊关键词触发默认 LLM 对话。
- 支持群聊单独 @ 机器人使用配置项 `at_prompt` 作为提示词触发默认 LLM 对话。
- 仅在群聊消息中生效。

## 项目结构

```text
.
├── main.py                 # 插件入口，负责串联触发判断和 LLM prompt 设置
├── _conf_schema.json       # 插件配置 schema
├── metadata.yaml           # AstrBot 插件元信息
├── services/
│   ├── __init__.py         # 内部服务模块声明
│   ├── config.py           # 配置读取工具
│   └── triggers.py         # 触发条件判断工具
├── README.md
└── LICENSE
```

## 配置

配置项说明：

| 配置项 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `keywords` | `list` | 无 | 群聊触发关键词列表。消息包含任意关键词即可触发。 |
| `at_prompt` | `string` | `请根据上下文自然回复一下` | 单独 @ 机器人时发送给 LLM 的提示词。 |

## 使用方法

1. 下载插件或者手动将插件放入 AstrBot 插件目录。
2. 关闭 AstrBot 配置 `唤醒词` 和 `只 @ 机器人是否触发等待`。
3. 在 AstrBot 插件管理中启用 `trigger_chat`。
4. 在插件配置中填写 `keywords` 和 `at_prompt`。
5. 确保 AstrBot 的 LLM provider 已启用，否则插件只能触发流程，无法获得 AI 回复。
6. 在群聊中发送包含关键词的消息，或单独 @ 机器人触发对话。

## 触发规则

### 1. 单独 @ 机器人

如果消息只 @ 机器人，且除 @ 之外没有其他非空文本，会触发 LLM 对话，并使用 `at_prompt` 作为提示词。

### 2. 关键词触发

如果关键词是“帮我看看”，并且消息包含关键词，会触发 LLM 对话，例如：

```text
这个接口一直 500，帮我看看可能是什么问题
```

## 使用示例

假设配置如下：

```json
{
  "keywords": ["帮我看看", "机器人"],
  "at_prompt": "请根据上下文自然回复一下"
}
```

### 示例 1：单独 @，使用 at_prompt

群聊中用户发送：

```text
用户A：@机器人
```

实际发送给 LLM 的提示词：

```text
请根据上下文自然回复一下
```

群聊中的效果类似：

```text
用户A：@机器人
机器人：可以先从超时链路、上游依赖和异常日志采集三个方向排查。建议先给超时请求加 request id，串起完整调用链。
```

### 示例 2：关键词触发，保留原始消息

群聊中用户发送：

```text
用户A：这个接口一直 500，帮我看看可能是什么问题
```

实际发送给 LLM 的提示词：

```text
这个接口一直 500，帮我看看可能是什么问题
```

## 实际发送机制

```text
群聊消息
  ↓
插件判断触发条件
  ↓
构造 LLM prompt
  ↓
AstrBot 默认 LLM 流程
  ↓
AstrBot RespondStage 发送回复
```

## 注意事项

- 单独 @ 会改写为 `at_prompt`，用于避免纯 @ 空消息被 AstrBot 跳过。
- 如果 AstrBot 的 LLM provider 未启用或当前会话禁用了 AI 能力，插件不会产生 AI 回复。

## 支持平台

```yaml
support_platforms:
  - aiocqhttp
```

## 相关链接

- [AstrBot](https://github.com/AstrBotDevs/AstrBot)
- [AstrBot 插件开发文档](https://docs.astrbot.app/dev/star/plugin-new.html)
