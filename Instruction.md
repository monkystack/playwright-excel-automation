Save path in Macro: Python → PS1 → VBA:

    Python: today_folder
        ↓
    PowerShell: -OutputFolder today_folder
        ↓
    PowerShell: $finalFile = today_folder + "pivot_table_103355.xlsx"
        ↓
    PowerShell: $excel.Run("Macro2", $finalFile)
        ↓
    VBA Macro2(outputPath As String)

    
    
    1. remember to install `psutil`
    2. store wms `username` and `password` in Windows Credentials
    3. import xml into Task Scheduler
