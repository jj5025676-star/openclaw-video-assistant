#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_WSL_DISTRO = "Ubuntu"
DEFAULT_AGENT_ID = "video-agent"
DEFAULT_CONFIG_WIN = Path(r"\\wsl.localhost\Ubuntu\home\z852963\.openclaw\openclaw.json")
DEFAULT_CONFIG_WSL = Path("/home/z852963/.openclaw/openclaw.json")


def is_windows() -> bool:
    return os.name == "nt"


def to_wsl_path(path: Path) -> str:
    text = str(path)
    prefix = "\\\\wsl.localhost\\Ubuntu\\"
    if text.startswith(prefix):
        rest = text[len(prefix):].replace("\\", "/")
        return "/" + rest
    if len(text) >= 2 and text[1] == ":":
        drive = text[0].lower()
        rest = text[2:].replace("\\", "/")
        return f"/mnt/{drive}{rest}"
    return text.replace("\\", "/")


def detect_default_config() -> Path:
    if is_windows() and DEFAULT_CONFIG_WIN.exists():
        return DEFAULT_CONFIG_WIN
    if DEFAULT_CONFIG_WSL.exists():
        return DEFAULT_CONFIG_WSL
    raise FileNotFoundError("找不到 OpenClaw 生效配置文件 openclaw.json")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    path.write_text(text, encoding="utf-8")


def restart_gateway() -> None:
    if is_windows():
        cmd = ["wsl", "-d", DEFAULT_WSL_DISTRO, "--", "systemctl", "--user", "restart", "openclaw-gateway.service"]
    else:
        cmd = ["systemctl", "--user", "restart", "openclaw-gateway.service"]
    subprocess.run(cmd, check=True)


def ensure_agent(config: dict, agent_id: str, workspace_wsl: str, agent_dir_wsl: str) -> str:
    agents = config.setdefault("agents", {})
    agent_list = agents.setdefault("list", [])
    for agent in agent_list:
        if agent.get("id") == agent_id:
            agent["workspace"] = workspace_wsl
            agent["agentDir"] = agent_dir_wsl
            return "updated"
    agent_list.append(
        {
            "id": agent_id,
            "workspace": workspace_wsl,
            "agentDir": agent_dir_wsl,
        }
    )
    return "created"


def ensure_binding(config: dict, agent_id: str, account_id: str) -> str:
    feishu = config.get("channels", {}).get("feishu", {})
    accounts = feishu.get("accounts", {})
    if account_id not in accounts:
        raise ValueError(f"当前配置里不存在飞书 accountId={account_id}")

    if config.get("session", {}).get("dmScope") in (None, ""):
        config.setdefault("session", {})["dmScope"] = "per-account-channel-peer"

    bindings = config.setdefault("bindings", [])
    for binding in bindings:
        match = binding.get("match", {})
        if match.get("channel") == "feishu" and match.get("accountId") == account_id:
            binding["agentId"] = agent_id
            return "updated"

    bindings.append(
        {
            "agentId": agent_id,
            "match": {
                "channel": "feishu",
                "accountId": account_id,
            },
        }
    )
    return "created"


def main() -> int:
    parser = argparse.ArgumentParser(description="把当前目录注册成 OpenClaw 的一个新视频 agent 工作区")
    parser.add_argument("--agent-id", default=DEFAULT_AGENT_ID, help="要创建的 agentId，默认 video-agent")
    parser.add_argument("--account-id", help="可选：把某个现有飞书 accountId 绑定到该 agent")
    parser.add_argument("--config", help="可选：手动指定 openclaw.json 路径")
    parser.add_argument("--restart", dest="restart", action="store_true", help="写入后自动重启 gateway")
    parser.add_argument("--no-restart", dest="restart", action="store_false", help="写入后不自动重启 gateway")
    parser.set_defaults(restart=True)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    workspace_local = script_dir
    workspace_wsl = to_wsl_path(workspace_local)

    config_path = Path(args.config) if args.config else detect_default_config()
    config = load_json(config_path)

    config_dir_local = config_path.parent
    config_dir_wsl = to_wsl_path(config_dir_local)
    agent_dir_wsl = f"{config_dir_wsl}/agents/{args.agent_id}/agent"
    agent_dir_local = config_dir_local / "agents" / args.agent_id / "agent"
    agent_dir_local.mkdir(parents=True, exist_ok=True)

    backup_path = config_path.with_name(
        f"{config_path.stem}.before-video-agent-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}{config_path.suffix}"
    )
    shutil.copy2(config_path, backup_path)

    agent_status = ensure_agent(config, args.agent_id, workspace_wsl, agent_dir_wsl)
    binding_status = None
    if args.account_id:
        binding_status = ensure_binding(config, args.agent_id, args.account_id)

    meta = config.setdefault("meta", {})
    meta["lastTouchedAt"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    write_json(config_path, config)

    if args.restart:
        restart_gateway()

    print("安装完成")
    print(f"agent: {args.agent_id} ({agent_status})")
    print(f"workspace: {workspace_wsl}")
    print(f"agentDir: {agent_dir_wsl}")
    print(f"config: {config_path}")
    print(f"backup: {backup_path}")
    if args.account_id:
        print(f"binding: feishu/{args.account_id} -> {args.agent_id} ({binding_status})")
    print(f"gateway restarted: {'yes' if args.restart else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
