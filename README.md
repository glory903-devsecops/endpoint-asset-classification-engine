# Endpoint Asset Classification and Zero-Trust Governance Engine

이 프로젝트는 엔드포인트 자산(업무용/개인용)을 식별 및 분류하고, 취약점 샘플을 격리하는 제로트러스트 보안 엔진입니다. 
v2.5 리팩토링을 통해 **지능형 스코어링 분류**와 **Tailwind CSS v4 기반 익스클루시브 대시보드**가 추가되었습니다.

## 핵심 기능

-   **지능형 자산 분류 (Intelligent Classification)**: 확장자, 프로젝트 마커(.git 등), 가중치 기반 키워드 분석을 통한 정밀 분류.
-   **동적 시그니처 배포**: 로컬 및 원격 저장소에서 최신 분류 규칙을 가져오는 `SignatureProvider` 구조.
-   **위협 샘플 격리 (Isolation)**: 보안 경고가 감지된 파일을 안전하게 격리하고 Fernet(AES-128)으로 암호화.
-   **프리미엄 웹 대시보드**: **Tailwind CSS v4**와 React로 구축된 현대적인 실시간 거버넌스 모니터링 툴.

## 🚀 빠른 시작 (Quick Start)

터미널에서 아래 명령어를 입력하여 **환경 구성, 자산 스캔, 대시보드 실행**을 한 번에 완료할 수 있습니다.

1.  **프로젝트 폴더로 이동**:
    ```bash
    cd endpoint-asset-classification-engine
    ```
2.  **통합 시작 도구 실행**:
    ```bash
    python dev.py all
    ```

> [!TIP]
> `dev.py all` 명령어를 실행하면 약 1~2분 내에 모든 설정이 완료되고, **내장 웹 대시보드 서버가 가동되며 브라우저 창이 자동으로 열립니다.**

## 디렉토리 구조

-   `domain/`: 비즈니스 규칙 및 인터페이스 (추상화 레이어)
-   `use_cases/`: 애플리케이션 로직 (스코어링 기반 분류)
-   `adapters/`: 인프라 세부 구현 (원격 시그니처, 파일 시스템, 암호화)
-   `dashboard/`: **Tailwind CSS v4** 기반 프리미엄 대시보드 (React)
-   `docs/`: 제품 요구사항 정의서(PRD) 및 QA 결과 보고서
-   `dev.py`: 프로젝트 통합 관리 및 자동 시작 도구

## 라이선스

이 프로젝트는 자가 거버넌스 및 시큐어 코딩 실습 목적의 참조용 소프트웨어입니다.
