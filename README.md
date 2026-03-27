# Endpoint Asset Classification and Zero-Trust Governance Engine

이 프로젝트는 엔드포인트 자산(업무용/개인용)을 식별 및 분류하고, 취약점 샘플을 격리하는 제로트러스트 보안 엔진입니다. 
SOLID 원칙과 Clean Architecture를 준수하며, AI 기반 거버넌스를 위한 MCP(Model Context Protocol) 호환 로그 기능을 포함합니다.

## 핵심 기능

-   **업무/개인 전용 자산 분류**: 파일 키워드 및 메타데이터 기반 자동 이동 및 분류.
-   **위협 샘플 격리 (Isolation)**: 보안 경고가 감지된 파일을 안전하게 격리하고 Fernet(SES)으로 암호화.
-   **MCP 호환 로깅**: AI 모델이 자산 상태를 즉시 파악할 수 있는 정형화된 JSON 파일 로그 출력.
-   **멀티 플랫폼 지원**: Windows, macOS, Linux 환경 지원 및 자동 설치 스크립트 제공.

## 🚀 빠른 시작 (Quick Start)

가장 빠르게 환경을 구성하고 엔진을 실행하는 방법입니다.

1.  **환경 구성 (가상환경 및 라이브러리 설치)**:
    ```bash
    python setup/bootstrap.py
    ```
2.  **자산 분류 엔진 실행**:
    ```bash
    python main.py
    ```
3.  **웹 대시보드 모니터링**:
    ```bash
    python infrastructure/web_dashboard.py
    # 접속: http://localhost:8080
    ```

환경 구성(Python 설치, 경로 찾기, 권한 설정 등)에 대한 자세한 안내는 `setup/` 디렉토리를 확인하십시오.
-   **[초보자를 위한 초정밀 설치 가이드 바로가기](./setup/README.md)**

## 디렉토리 구조

-   `domain/`: 비즈니스 규칙 및 인터페이스 (추상화 레이어)
-   `use_cases/`: 애플리케이션 로직 (분류 및 격리 프로세스)
-   `adapters/`: 인프라 세부 구현 (파일 시스템, 해시, 암호화)
-   `setup/`: 멀티 플랫폼 환경 구성 스크립트
-   `.github/workflows/`: CI (GitHub Actions) 워크플로우

## 라이선스

이 프로젝트는 자가 거버넌스 및 시큐어 코딩 실습 목적의 참조용 소프트웨어입니다.
