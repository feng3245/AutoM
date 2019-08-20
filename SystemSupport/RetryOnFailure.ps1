if ((Get-ScheduledTask | Where TaskName -eq AutoMentorWeekly ).State -eq "Ready" -AND -NOT ((Get-ScheduledTaskInfo AutoMentorWeekly).LastTaskResult -eq 0))
{
    $Items = @('Cache\*')
    $Folder = "$($env:LOCALAPPDATA)\Google\Chrome\User Data\Default"
    $Items | % { 
        if (Test-Path "$Folder\$_") 
        {
            Remove-Item "$Folder\$_" -Force
        }
    }
    Start-ScheduledTask -TaskName "AutoMentorWeekly"
}