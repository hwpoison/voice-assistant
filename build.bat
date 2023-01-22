@echo off
echo Building to exe
pyinstaller gui.pyw --hidden-import autoit --hidden-import vosk --name voiceAssistant --icon icon.ico
echo Finished.
pause