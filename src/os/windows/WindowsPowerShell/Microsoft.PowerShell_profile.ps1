Import-Module "${HOME}\.posh-git\src\posh-git.psd1"
# $GitPromptSettings.DefaultPromptPrefix.Text = '$(Get-Date -f "MM-dd HH:mm:ss") '
$GitPromptSettings.DefaultPromptPrefix.ForegroundColor = [ConsoleColor]::Magenta
$GitPromptSettings.DefaultPromptPath.ForegroundColor = 'orange'
$GitPromptSettings.DefaultPromptBeforeSuffix.Text = '`n'
. "${HOME}\.dotfiles\src\os\windows\WindowsPowerShell\functions.ps1"
