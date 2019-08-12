if ((Get-ScheduledTask | Where TaskName -eq AutoMentorWeekly ).State -eq "Ready" -AND -NOT ((Get-ScheduledTaskInfo AutoMentorWeekly).LastTaskResult -eq 0))
{
    Start-ScheduledTask -TaskName "AutoMentorWeekly"
}