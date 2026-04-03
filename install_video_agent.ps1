param(
  [string]$AgentId = "video-agent",
  [string]$AccountId = "",
  [switch]$NoRestart
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$py = Join-Path $scriptDir "install_video_agent.py"

$args = @($py, "--agent-id", $AgentId)

if ($AccountId -ne "") {
  $args += @("--account-id", $AccountId)
}

if ($NoRestart) {
  $args += "--no-restart"
} else {
  $args += "--restart"
}

python @args
