# Product Requirement Document: Intelligent Asset Governance Engine

## 1. Overview
A security-first endpoint governance engine that automatically classifies files into Work, Personal, or Threat categories and enforces zero-trust isolation.

## 2. Target Audience
Security administrators and enterprise employees requiring automated data segregation on local endpoints.

## 3. Key Features
- **Intelligent Classification**: Weighted scoring based on file extensions, project markers (e.g., .git), and context-aware keywords.
- **Dynamic Signatures**: Decoupled signature provider capable of fetching updates from remote repositories.
- **Threat Isolation**: Automatic encryption and quarantine of identified malicious samples.
- **Interactive Dashboard**: Modern Vite+React dashboard using Tailwind CSS v4 for real-time monitoring and governance visualization.

## 4. Technical Stack
- **Backend**: Python 3.10+, Clean Architecture.
- **Frontend**: React 18, Vite, Tailwind CSS v4, Framer Motion, Lucide Icons.
- **Security**: Fernet Encryption (AES-128 in CBC mode), SHA-256 Hashing.

## 5. Success Metrics
- Classification accuracy > 95% on provided test data.
- Successful synchronization with remote GitHub repository.
