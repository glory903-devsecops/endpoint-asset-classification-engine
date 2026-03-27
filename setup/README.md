# 🛠️ 초보자를 위한 셋업 가이드 (Multi-Platform)

이 엔진을 실행하기 위해 필요한 파이썬 환경을 구성하는 방법입니다. 모든 과정은 **터미널(Terminal)** 또는 **PowerShell**에서 진행됩니다.

---

## 🚀 가장 추천하는 방법: 자동 설치 (Python 필수)
파이썬이 설치되어 있다면, 아래 명령 한 줄로 가상 환경(`venv`) 생성과 라이브러리 설치를 한 번에 끝낼 수 있습니다.

```bash
# 프로젝트 폴더 내에서 실행
python setup/bootstrap.py
```

---

## 📋 수동 설치 가이드 (단계별 복사-붙여넣기)

자동 설치가 원활하지 않을 경우, 아래 OS별 명령어를 순서대로 복사하여 실행하세요.

### 1️⃣ Windows (PowerShell)
가장 보편적인 윈도우 환경에서의 셋업입니다.

1.  **파이썬 경로 확인** (경로를 모를 때):
    ```powershell
    where.exe python
    ```
2.  **가상 환경 생성**:
    ```powershell
    # 만약 'python' 명령어가 안 먹힌다면 위에서 확인한 전체 경로를 쓰세요.
    python -m venv venv
    ```
3.  **보안 정책 일시 허용 및 활성화** (매우 중요!):
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
    .\venv\Scripts\activate
    ```
4.  **라이브러리 설치**:
    ```powershell
    pip install -r requirements.txt
    ```

### 2️⃣ macOS / Linux (Terminal)
맥북이나 리눅스 사용자를 위한 가이드입니다.

1.  **가상 환경 생성**:
    ```bash
    python3 -m venv venv
    ```
2.  **활성화**:
    ```bash
    source venv/bin/activate
    ```
3.  **라이브러리 설치**:
    ```bash
    pip install -r requirements.txt
    ```

---

## ❓ 트러블슈팅 (Q&A)

**Q: `python` 명령어를 입력해도 아무 반응이 없거나 스토어로 연결돼요.**
A: 파이썬이 설치되지 않았거나 환경 변수에 등록되지 않은 경우입니다. `where.exe python`으로 경로를 찾은 뒤, `& "전체경로" -m venv venv` 식으로 전체 경로를 따옴표와 함께 사용하세요.

**Q: `UnauthorizedAccess` 보안 오류가 떠서 가상 환경 활성화가 안 돼요.**
A: 윈도우 PowerShell의 보안 정책 때문입니다. `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` 명령어를 입력하면 현재 터미널 창에서만 실행이 허용됩니다.

---

## ✅ 설치 확인 및 도구 실행
모든 설치가 끝났다면 아래 명령어로 엔진과 대시보드를 차례로 실행해 보세요.

1.  **분류 엔진 실행**: `python main.py`
2.  **웹 대시보드 실행**: `python infrastructure/web_dashboard.py` (접속: http://localhost:8080)
