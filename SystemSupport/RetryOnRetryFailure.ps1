if ((Get-ScheduledTask | Where TaskName -eq AutoMentorRetry ).State -eq "Ready" -AND (Get-ScheduledTask | Where TaskName -eq AutoMentorWeekly ).State -eq "Ready" -AND ((Get-ScheduledTaskInfo AutoMentorWeekly).LastTaskResult -eq 0) -AND (Get-Content -Path C:\AutoM\badlinks).Length -gt 0)
{
    $Items = @('Cache\*')
    $Folder = "$($env:LOCALAPPDATA)\Google\Chrome\User Data\Default"
    $Items | % { 
        if (Test-Path "$Folder\$_") 
        {
            Remove-Item "$Folder\$_" -Force
        }
    }
    Start-ScheduledTask -TaskName "AutoMentorRetry"
}