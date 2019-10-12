Import-Module 'C:\Users\swhitlock\.posh-git\src\posh-git.psd1'
#$GitPromptSettings.DefaultPromptPrefix.Text = '$(Get-Date -f "MM-dd HH:mm:ss") '
$GitPromptSettings.DefaultPromptPrefix.ForegroundColor = [ConsoleColor]::Magenta
$GitPromptSettings.DefaultPromptPath.ForegroundColor = 'orange'
$GitPromptSettings.DefaultPromptBeforeSuffix.Text = '`n'

# Run this as a Computer Startup script to allow installing fonts from C:\InstallFont\
# Based on http://www.edugeek.net/forums/windows-7/123187-installation-fonts-without-admin-rights-2.html
# Run this as a Computer Startup Script in Group Policy

# Full details on my website - https://mediarealm.com.au/articles/windows-font-install-no-password-powershell/

# $SourceDir   = "C:\Users\swhitlock\.opt\cascadia-code"
# $Source      = "C:\Users\swhitlock\.opt\cascadia-code\*"
# $Destination = (New-Object -ComObject Shell.Application).Namespace(0x14)
# $TempFolder  = "C:\Users\swhitlock\AppData\Local\Temp\Fonts"

# # Create the source directory if it doesn't already exist
# New-Item -ItemType Directory -Force -Path $SourceDir

# New-Item $TempFolder -Type Directory -Force | Out-Null

# Get-ChildItem -Path $Source -Include '*.ttf','*.ttc','*.otf' -Recurse | ForEach {
#     If (-not(Test-Path "C:\Users\swhit\AppData\Fonts\$($_.Name)")) {

#         $Font = "$TempFolder\$($_.Name)"

#         # Copy font to local temporary folder
#         Copy-Item $($_.FullName) -Destination $TempFolder

#         # Install font
#         $Destination.CopyHere($Font,0x10)

#         # Delete temporary copy of font
#         Remove-Item $Font -Force
#     }
# }
