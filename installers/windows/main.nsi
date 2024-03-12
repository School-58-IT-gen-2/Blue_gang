Outfile "Chess_Installer.exe"
InstallDir "$PROGRAMFILES\chess"

Section "chess"
    SetOutPath $INSTDIR
    File /r "src/*"
    CreateShortcut "$SMPROGRAMS\Chess.lnk" "$INSTDIR\chess.exe"
SectionEnd