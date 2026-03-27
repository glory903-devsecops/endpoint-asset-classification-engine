import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """
    명령어를 실행하며, 윈도우 환경에서의 쉘 실행 및 인코딩 이슈를 처리합니다.
    """
    try:
        # 윈도우에서는 shell=True가 필요할 수 있으며, npm.cmd 등을 직접 호출합니다.
        shell = os.name == 'nt'
        subprocess.check_call(command, cwd=cwd, shell=shell)
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

def main():
    root = Path(__file__).parent.absolute()
    
    while True:
        print("\n" + "="*45)
        print("   Endpoint Asset Governance Engine v2.5")
        print("           Developer Control Tool")
        print("="*45)
        print(" 1. 전체 초기화 (Backend + Dashboard Setup)")
        print(" 2. 분류 엔진 실행 (python main.py)")
        print(" 3. 대시보드 서버 실행 (Vite/React)")
        print(" 4. 종료")
        print("-" * 45)
        
        try:
            choice = input("\n작업 선택 (1-4): ").strip()
        except EOFError:
            break

        if choice == '1':
            setup()
        elif choice == '2':
            print("\n[정보] 분류 엔진을 가동합니다...")
            # 가상환경의 파이썬을 우선적으로 사용 시도
            venv_python = root / "venv" / ("Scripts" if os.name == "nt" else "bin") / ("python.exe" if os.name == "nt" else "python")
            python_exe = str(venv_python) if venv_python.exists() else sys.executable
            run_command([python_exe, "main.py"])
        elif choice == '3':
            print("\n[정보] 대시보드 서버를 시작합니다 (http://localhost:5173)...")
            dashboard_path = root / "dashboard"
            npm_cmd = "npm.cmd" if os.name == "nt" else "npm"
            run_command([npm_cmd, "run", "dev"], cwd=str(dashboard_path))
        elif choice == '4':
            print("\n도구를 종료합니다.")
            break
        else:
            print("\n[알림] 잘못된 선택입니다. 1에서 4 사이의 숫자를 입력해주세요.")

if __name__ == "__main__":
    main()
