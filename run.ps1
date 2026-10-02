# Ir a la raíz del proyecto (ajusta la ruta si es necesario)
cd $PSScriptRoot

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Mostrar ubicación actual para confirmar
Write-Host "Raiz del proyecto: $(Get-Location)" -ForegroundColor Cyan

# Ejecutar el sistema
python manager.py