# setup.ps1

Write-Output "Creating virtual environment 'venv'..."
python -m venv venv

Write-Output "Activating virtual environment..."
# Dot-source the activation script to apply it to the current session
. .\venv\Scripts\Activate.ps1

Write-Output "Upgrading pip to the latest version..."
python -m pip install --upgrade pip

Write-Output "Installing required packages..."
pip install discord.py aiohttp python-dotenv

Write-Output "Generating requirements.txt..."
pip freeze | Out-File -Encoding utf8 requirements.txt

Write-Output "`nSetup complete!"
Write-Output "------------------------------------------------"
Write-Output "To run your bot now, type: python main.py"
Write-Output "To activate this environment later, run: . .\venv\Scripts\Activate.ps1"