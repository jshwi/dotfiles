function Get-Pip {
    $positional = $args[0]
    if ($positional -eq "install") {
        $pkg = $args[1]
        C:\Users\swhitlock\scoop\apps\python\3.8.5\Scripts\pip3.8.exe install --trusted-host pypi.org --trusted-host files.pythonhosted.org @args
    }
    elseif ($args) {
        pip @args
    }
    else {
        pip --help
    }
}
function Get-Hidden {
    ATTRIB +H /s /d "C:\Users\swhitlock\.*"
}
