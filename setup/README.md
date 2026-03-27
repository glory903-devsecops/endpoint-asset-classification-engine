# Setup Guide (Multi-Platform)

이 프로젝트는 엔드포인트 자산 분류 및 제로트러스트 거버넌스 엔진입니다. 
정상적인 실행과 개발을 위해 **Python 3.12**, **Git**, **GitHub CLI**가 필요합니다.

이미 환경이 구성된 사용자는 이 과정을 건너뛰고 바로 `pip install -r requirements.txt`를 실행하십시오.

## 자동 설치 스크립트

각 플랫폼별로 제공되는 스크립트를 사용하여 필요한 소프트웨어를 자동으로 설치할 수 있습니다.

### 1. Windows (Recommended)
PowerShell을 관리자 권한으로 실행한 후 다음 스크립트를 실행하십시오. (Winget이 필요합니다.)
```powershell
./install_windows.ps1
```

### 2. macOS
터미널을 열고 다음 스크립트를 실행하십시오. (Homebrew가 설치되어 있어야 합니다.)
```bash
chmod +x install_macos.sh
./install_macos.sh
```

### 3. Linux (Ubuntu/Debian/Fedora)
터미널을 열고 다음 스크립트를 실행하십시오.
```bash
chmod +x install_linux.sh
./install_linux.sh
```

## 설치 확인

설치 후 터미널을 다시 시작한 뒤 다음 명령어로 설치 여부를 확인하십시오.
- `python --version`
- `git --version`
- `gh --version`

완료된 후 프로젝트 루트 디렉토리에서 의존성을 설치하십시오:
```bash
pip install -r requirements.txt
```
