;-------------------------------------------
; General Information
;-------------------------------------------
OutFile "@@INSTALLER_NAME@@.exe"
RequestExecutionLevel admin

!include "MUI2.nsh"
!include "nsDialogs.nsh"
!include "winmessages.nsh"
!include "logiclib.nsh"

;-------------------------------------------
; Custom Dialog & Variable
;-------------------------------------------
Var Dialog
Var Label
Var Username_TxtBox
Var Username
Var Password
Var hwnd
Var Password_TxtBox
Var STR_HAYSTACK
Var STR_NEEDLE
Var STR_CONTAINS_VAR_1
Var STR_CONTAINS_VAR_2
Var STR_CONTAINS_VAR_3
Var STR_CONTAINS_VAR_4
Var STR_RETURN_VAR
Var Creds

;-------------------------------------------
; Modern UI Appearance
;-------------------------------------------
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\orange-install.ico"
!define MUI_UNICON "${NSISDIR}\Contrib\Graphics\Icons\orange-install.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"
!define MUI_WELCOMEPAGE_TITLE  "JENKINS AUTOMATION DEMO INSTALLATION"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "${NSISDIR}\Contrib\Graphics\Wizard\orange.bmp"

;-------------------------------------------
; Installer Pages
;-------------------------------------------
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "${NSISDIR}\Docs\Modern UI\License.txt"
Page custom Login Login_leave
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

;-------------------------------------------
; Language
;-------------------------------------------
!insertmacro MUI_LANGUAGE "English"


;-------------------------------------------
; StrContain Function
;-------------------------------------------
Function StrContains
  Exch $STR_NEEDLE
  Exch 1
  Exch $STR_HAYSTACK
  ; Uncomment to debug
  ; MessageBox MB_OK 'STR_NEEDLE = $STR_NEEDLE STR_HAYSTACK = $STR_HAYSTACK '
    StrCpy $STR_RETURN_VAR ""
    StrCpy $STR_CONTAINS_VAR_1 -1
    StrLen $STR_CONTAINS_VAR_2 $STR_NEEDLE
    StrLen $STR_CONTAINS_VAR_4 $STR_HAYSTACK
    loop:
      IntOp $STR_CONTAINS_VAR_1 $STR_CONTAINS_VAR_1 + 1
      StrCpy $STR_CONTAINS_VAR_3 $STR_HAYSTACK $STR_CONTAINS_VAR_2 $STR_CONTAINS_VAR_1
      StrCmp $STR_CONTAINS_VAR_3 $STR_NEEDLE found
      StrCmp $STR_CONTAINS_VAR_1 $STR_CONTAINS_VAR_4 done
      Goto loop
    found:
      StrCpy $STR_RETURN_VAR $STR_NEEDLE
      Goto done
    done:
   Pop $STR_NEEDLE ;Prevent "invalid opcode" errors and keep the
   Exch $STR_RETURN_VAR  
FunctionEnd
 
!macro _StrContainsConstructor OUT NEEDLE HAYSTACK
  Push `${HAYSTACK}`
  Push `${NEEDLE}`
  Call StrContains
  Pop `${OUT}`
!macroend
 
!define StrContains '!insertmacro "_StrContainsConstructor"'


;-------------------------------------------
; Custom Authentication Page
;-------------------------------------------
Function Login
  SetOutPath $INSTDIR
  File "@@FILE_PATH@@"
  nsDialogs::Create 1018
  Pop $Dialog

   ${If} $Dialog == error
        Abort
    ${EndIf}

     # Username Dialog Control
    ${NSD_CreateLabel} 0 0 100% 9u "&Username:"
    Pop $Label
    ${NSD_CreateText} 0 10% 100% 12u ""
    Pop $Username_TxtBox
    # Password Dialog Control
    ${NSD_CreateLabel} 0 20% 100% 9u "&Password:"
    Pop $Label
	${NSD_CreatePassword} 0 30% 100% 12u ""
	Pop $Password_TxtBox
    ${NSD_CreateCheckbox} 0 40% 25% 8% "Show password"
	Pop $hwnd
	${NSD_OnClick} $hwnd ShowPassword
	nsDialogs::Show
FunctionEnd


Function ShowPassword
	Pop $hwnd
    ; Retrieve state(check/uncheck) of checkbox
	${NSD_GetState} $hwnd $0
    ; Hide password input field
	ShowWindow $Password_TxtBox ${SW_HIDE}
	${If} $0 == 1
		SendMessage $Password_TxtBox ${EM_SETPASSWORDCHAR} 0 0
	${Else}
		SendMessage $Password_TxtBox ${EM_SETPASSWORDCHAR} 42 0
	${EndIf}
	ShowWindow $Password_TxtBox ${SW_SHOW}

FunctionEnd

Function Login_leave

    ${NSD_GetText} $Username_TxtBox $Username
    ${NSD_GetText} $Password_TxtBox $Password
    StrCpy $Creds "$Username $Password"

    # Pass the username and password values to cmd
    nsExec::ExecToStack 'cmd.exe /C "echo $Creds| "$INSTDIR\Bryan.exe" $Username $Password"'
    Pop $0
    Pop $1

    # Uncomment to debug
    ; MessageBox MB_OK "0 = $0"
    ; MessageBox MB_OK "1 = $1"  

    ${StrContains} $0 "SUCCESS" $1
    StrCmp $0 "" notfound1
        MessageBox MB_OK 'Authentication successful.'
        nsExec::ExecToStack 'cmd.exe /C ""$INSTDIR\Bryan.exe" start"'

    notfound1:
    ${StrContains} $0 "FAILURE" $1
    StrCmp $0 "" notfound2
        MessageBox MB_OK 'Wrong credentials. Please try again.'
        nsExec::ExecToStack 'cmd.exe /C ""$INSTDIR\Bryan.exe" remove"'
        Abort
    
    notfound2:
    ${StrContains} $0 "EMPTY" $1
    StrCmp $0 "" notfound3
        MessageBox MB_OK 'Username and password field cannot be empty.'
        nsExec::ExecToStack 'cmd.exe /C ""$INSTDIR\Bryan.exe" remove"'
        Abort

     notfound3:
     Return
FunctionEnd


;-------------------------------------------
; Installer Components
;-------------------------------------------
Section "Install" 
    SectionIn RO

    nsExec::ExecToStack 'cmd.exe /C "echo $Creds| "$INSTDIR\Bryan.exe" $Username $Password"'
    Pop $0
    Pop $1
    Pop $2
    ; MessageBox MB_OK "0=$0, 1=$1, 2=$2" 

    ${StrContains} $0 "Finish" $1
    StrCmp $0 "" notDone
        MessageBox MB_OK 'Installation complete. Click OK to proceed.'
        Return
    
    notDone:
SectionEnd