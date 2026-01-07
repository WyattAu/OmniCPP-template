# scripts/detect_msvc_version.ps1
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"
$vsInstallation = & $vswhere -latest -products * -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath

if ($vsInstallation) {
    $vcvarsPath = Join-Path $vsInstallation "VC\Auxiliary\Build\vcvarsall.bat"
    if (Test-Path $vcvarsPath) {
        # Extract version from cl.exe
        $clPath = Join-Path $vsInstallation "VC\Tools\MSVC\*\bin\Hostx64\x64\cl.exe" | Get-ChildItem | Select-Object -First 1
        if ($clPath) {
            $version = & $clPath 2>&1 | Select-String "Version (\d+)\.(\d+)" | ForEach-Object { $_.Matches.Groups[1].Value + $_.Matches.Groups[2].Value }
            if ($version) {
                Write-Output $version
            } else {
                Write-Error "Failed to extract version from cl.exe"
                exit 1
            }
        } else {
            Write-Error "cl.exe not found in expected location"
            exit 1
        }
    } else {
        Write-Error "vcvarsall.bat not found, Visual Studio installation may be corrupted"
        exit 1
    }
} else {
    Write-Error "No Visual Studio installation found with VC++ tools"
    exit 1
}