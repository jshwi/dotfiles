Import-Module 'C:\Users\swhitlock\.posh-git\src\posh-git.psd1'
# $GitPromptSettings.DefaultPromptPrefix.Text = '$(Get-Date -f "MM-dd HH:mm:ss") '
$GitPromptSettings.DefaultPromptPrefix.ForegroundColor = [ConsoleColor]::Magenta
$GitPromptSettings.DefaultPromptPath.ForegroundColor = 'orange'
$GitPromptSettings.DefaultPromptBeforeSuffix.Text = '`n'