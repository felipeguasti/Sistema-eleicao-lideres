@echo off

echo Instalando as dependencias para Eleicoes...
echo Baixando o instalador do Python...
curl -k https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe --output C:\python-install\python-installer.exe --create-dirs
echo Preparando para instalar o Python...
echo Instalando o Python...
start /wait C:\python-install\python-installer.exe /quiet PrependPath=1 Include_test=0
echo Python instalado.
echo Versao do Python
python --version
echo Fazendo o download do get-pip.py...
curl -k https://bootstrap.pypa.io/get-pip.py --output C:\pip-install\pip-installer.exe --create-dirs
echo Instalando o PIP...
python C:\pip-install\pip-installer.exe 
echo Instalando tkinter
pip install tk
echo Instalando pillow
pip install Pillow
echo Instalando kivy
pip install kivy
echo Instalando datetime
pip install datetime
echo Instalando reportlab
pip install reportlab
echo Checando por outras dependencias


echo Cheque se todas os requisitos foram instalados com sucesso.
pause
echo Limpando os arquivos temporários do PIP...
del get-pip.py
echo Limpando arquivos temporarios do python...
del python-installer.exe
echo Aguardando o fechamento deste prompt
timeout /t 5
exit
