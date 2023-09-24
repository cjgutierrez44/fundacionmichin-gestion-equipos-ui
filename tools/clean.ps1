$tempFolder = [System.IO.Path]::GetTempPath()
Remove-Item "$tempFolder\*" -Force -Recurse
