$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
python -m pip install -r requirements-dev.txt
if ($LASTEXITCODE -ne 0) { throw 'Falha ao instalar o empacotador.' }
python testes.py
if ($LASTEXITCODE -ne 0) { throw 'Os testes falharam. Executável não gerado.' }
python -m PyInstaller --noconfirm --clean --onefile --windowed --name ControleDeNotas main.py
if ($LASTEXITCODE -ne 0) { throw 'Falha ao gerar o executável.' }
Write-Host 'Pronto: dist\ControleDeNotas.exe'
