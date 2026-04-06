# ============================================
# PowerShell Enterprise Rolling Logging Module
# ============================================

# Target log directory: ../logs/powershell/
$LogFolder = Join-Path (Join-Path $PSScriptRoot "..") "logs/powershell"
if (!(Test-Path $LogFolder)) { New-Item -ItemType Directory -Path $LogFolder | Out-Null }

# Log file names
$LogFile = Join-Path $LogFolder "ps.log"
$MaxLogFiles = 5    # keep ps.log.1 ... ps.log.5

# --------- Rolling log implementation ---------
function Rotate-Logs {

    # Remove oldest
    $oldest = "$LogFile.$MaxLogFiles"
    if (Test-Path $oldest) { Remove-Item $oldest -Force }

    # Move automation.log.(n-1) → automation.log.n
    for ($i = $MaxLogFiles - 1; $i -ge 1; $i--) {
        $src = "$LogFile.$i"
        $dst = "$LogFile." + ($i + 1)
        if (Test-Path $src) { Rename-Item $src $dst }
    }

    # Move ps.log.(n-1) → ps.log.n
    if (Test-Path $LogFile) {
        Rename-Item $LogFile "$LogFile.1"
    }
}

# Create log if size too large (> 5MB)
$MaxSizeMB = 2
if (Test-Path $LogFile) {
    $sizeMB = [math]::Round((Get-Item $LogFile).Length / 1MB, 2)
    if ($sizeMB -ge $MaxSizeMB) {
        Rotate-Logs
    }
}

# ---------- Public log function ----------
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )

    $time = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$time] [$Level] $Message"
    Add-Content -Path $LogFile -Value $line
    Write-Output $line
}

# ---------- Auto-run when module loads ----------
Write-Log "=== Script started ==="
$ErrorActionPreference = "Stop"

# Auto error logging
trap {
    Write-Log "ERROR: $($_.Exception.Message)" "ERROR"
    Write-Log "StackTrace:`n$($_.Exception.StackTrace)" "ERROR"
    Write-Log "=== Script ended with ERROR ==="
    exit 1
}

Export-ModuleMember -Function Write-Log