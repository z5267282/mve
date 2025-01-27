"Note that this Powershell command might be needed"
"Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass"

if (Test-Path -Path .venv) {
    Remove-Item -Recurse .venv
}

python3.12.exe -m venv .venv
. .venv/Scripts/activate
pip3 install -r requirements.txt
deactivate

Write-Output "successfully installed .venv"
