import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def run_command(command, cwd=None, wait=True):
    """
    명령어를 실행하며, 윈도우 환경에서의 쉘 실행 및 인코딩 이슈를 처리합니다.
    wait=False일 경우 백그라운드에서 실행하며 Popen 객체를 반환합니다.
    """
    try:
        shell = os.name == 'nt'
        if wait:
            subprocess.check_call(command, cwd=cwd, shell=shell)
        else:
            # 백그라운드 실행 시 stdout/stderr가 부모 터미널에 섞이지 않도록 처리 가능하지만
            # 개발 편의를 위해 일단 그대로 출력되게 둡니다.
            return subprocess.Popen(command, cwd=cwd, shell=shell)
    except subprocess.CalledProcessError as e:
        print(f"\n[오류] 명령어 실행 중 문제가 발생했습니다: {e}")
    except Exception as e:
        print(f"\n[오류] 예상치 못한 문제가 발생했습니다: {e}")

def setup():
    """가상환경 및 대시보드 라이브러리를 설치합니다."""
    root = Path(__file__).parent.absolute()
    
    print("\n[1/2] 백엔드 환경 구성 중 (setup/bootstrap.py)...")
    run_command([sys.executable, str(root / "setup" / "bootstrap.py")])
    
    print("\n[2/2] 대시보드 라이브러리 설치 중 (npm install)...")
    dashboard_path = root / "dashboard"
    if dashboard_path.exists():
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
        run_command([npm_cmd, "install"], cwd=str(dashboard_path))
    else:
        print("[경고] dashboard 폴더를 찾을 수 없습니다.")

def start_services():
    """API 서버와 대시보드 프론트엔드를 동시에 가동합니다."""
    root = Path(__file__).parent.absolute()
    venv_python = root / "venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
    python_exe = str(venv_python) if venv_python.exists() else sys.executable
    
    processes = []
    try:
        # 1. FastAPI 백엔드 시작 (포트 8000)
        print("\n[진행] FastAPI 백엔드 API 서버를 시작합니다 (Port: 8000)...")
        api_proc = run_command([python_exe, "infrastructure/api_server.py"], wait=False)
        processes.append(api_proc)
        
        # API 서버가 뜰 때까지 잠시 대기
        time.sleep(2)
        
        # 2. Vite 프론트엔드 시작 (포트 5173)
        print("[진행] Vite 프론트엔드 대시보드를 시작합니다 (Port: 5173)...")
        dashboard_path = root / "dashboard"
        npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
        ui_proc = run_command([npm_cmd, "run", "dev"], cwd=str(dashboard_path), wait=False)
        processes.append(ui_proc)
        
        # 3. 브라우저 자동 오픈
        time.sleep(2)
        print("\n>> 접속 주소: http://localhost:5173")
        webbrowser.open("http://localhost:5173")
        
        print("\n[알림] 모든 서비스가 실행 중입니다. (종료하시려면 Ctrl+C를 누르세요)")
        
        # 프로세스 유지
        for p in processes:
            if p: p.wait()
            
    except KeyboardInterrupt:
        print("\n\n[알림] 사용자에 의해 서비스가 종료됩니다.")
        for p in processes:
            if p: p.terminate()
            
def main():
    root = Path(__file__).parent.absolute()
    
    # 아규먼트 체크 (예: python dev.py all)
    is_auto = len(sys.argv) > 1 and sys.argv[1] == 'all'
    
    if is_auto:
        print("\n" + "="*45)
        print("   [Auto Mode] 순차 실행 프로세스 시작")
        print("="*45)
        setup()
        start_services()
        return

    while True:
        print("\n" + "="*45)
        print("   Endpoint Asset Governance Engine v2.5")
        print("           Developer Control Tool")
        print("="*45)
        print(" 1. 전체 순차 실행 (Setup -> Start All Services)")
        print(" 2. 개별 초기화 (Backend + Dashboard Setup)")
        print(" 3. 통합 서비스 시작 (API Backend + React Frontend)")
        print(" 4. 분류 엔진 단독 실행 (CLI Mode)")
        print(" 5. 종료")
        print("-" * 45)
        
        try:
            choice = input("\n작업 선택 (1-5): ").strip()
        except EOFError:
            break

        if choice == '1':
            setup()
            start_services()
        elif choice == '2':
            setup()
        elif choice == '3':
            start_services()
        elif choice == '4':
            print("\n[정보] 분류 엔진을 단독 가동합니다 (CLI 모드)...")
            venv_python = root / "venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
            python_exe = str(venv_python) if venv_python.exists() else sys.executable
            run_command([python_exe, "main.py"])
        elif choice == '5':
            print("\n도구를 종료합니다.")
            break
        else:
            print("\n[알림] 잘못된 선택입니다.")

if __name__ == "__main__":
    main()
