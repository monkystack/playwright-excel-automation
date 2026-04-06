param(
    [string]$OutputFolder   # *must be put in the first line*. The folder passed in from Python for today's output
)

Import-Module "$PSScriptRoot\logs.psm1"

Write-Log "PowerShell script START"

# -----------------------------------------

try {
    # --- Generate file name ---
    $timestamp = Get-Date -Format "HHmmss"
    $finalFile = Join-Path $OutputFolder ("pivot_table_" + $timestamp + ".xlsx")
    Write-Log "Excel output path: $finalFile"

    # --- Open Excel ---
    $path = Join-Path $PSScriptRoot "..\excel_tool\AnalyseTool.xlsm"
    $resolved = Resolve-Path $path

    Write-Log "Opening Excel..."
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.Interactive = $false

    $wb = $excel.Workbooks.Open($resolved.Path)

    Write-Log "Running VBA Macro2..."
    $excel.Run("Macro2", $finalFile)
    Write-Log "Macro2 FINISHED (check vba/macro.log for details)"

    # Close
    $wb.Close($false)
    $excel.Quit()

    Write-Log "PowerShell completed successfully"
    exit 0     # <<< success：return 0
}
catch {
    Write-Log "Caught ERROR in PowerShell: $($_.Exception.Message)" "ERROR"
    # the trap block will write additional logs
    exit 1     # <<< failed：return 1
}


# --- 4. Quit Excel ---
$wb.Close($false)
$excel.Quit()
