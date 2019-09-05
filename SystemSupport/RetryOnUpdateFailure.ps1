if ((Get-ScheduledTask | Where TaskName -eq AutoStudentStatusUpdateRetry ).State -eq "Ready" -AND -NOT ((Get-ScheduledTaskInfo AutoStudentStatusUpdateRetry).LastTaskResult -eq 0))
{
    $Items = @('Cache\*')
    $Folder = "$($env:LOCALAPPDATA)\Google\Chrome\User Data\Default"
    $Items | % { 
        if (Test-Path "$Folder\$_") 
        {
            Remove-Item "$Folder\$_" -Force
        }
    }
    Start-ScheduledTask -TaskName "AutoStudentStatusUpdateRetry"
}