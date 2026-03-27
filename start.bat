@echo off
setlocal
echo ==========================================
echo   Endpoint Asset Governance Engine v2.5
echo           Quick Start Script
echo ==========================================
echo.

:: 1. Backend 가상환경 및 라이브러리 설치
echo [1/3] Backend 가상환경 및 Python 패키지 설치 중...
python setup\bootstrap.py

:: 2. 대시보드 라이브러리 설치 (PowerShell 권한 이슈 우회)
echo.
echo [2/3] Dashboard (Tailwind CSS v4) 라이브러리 설치 중...
if exist "dashboard" (
    pushd dashboard
    call npm.cmd install
    popd
) else (
    echo [경고] dashboard 폴더를 찾을 수 없습니다.
)

:: 3. 서비스 실행 옵션
echo.
echo [3/3] 모든 설정이 완료되었습니다!
echo.
echo ------------------------------------------
echo  [실행 옵션 선택]
echo  1. 지능형 분류 엔진 실행 (main.py)
echo  2. 프리미엄 대시보드 서버 실행 (Vite/React)
echo  3. 종료
echo ------------------------------------------
echo.

set /p choice="원하시는 작업 번호를 입력하세요 (1-3): "

if "%choice%"=="1" (
    echo.
    echo [정보] 분류 엔진을 실행합니다...
    if exist "venv\Scripts\python.exe" (
        .\venv\Scripts\python.exe main.py
    ) else (
        python main.py
    )
)

if "%choice%"=="2" (
    echo.
    echo [정보] 대시보드 서버를 시작합니다... (접속: http://localhost:5173)
    pushd dashboard
    call npm.cmd run dev
    popd
)

if "%choice%"=="3" (
    exit /b
)

echo.
echo 작업을 완료했습니다.
pause
