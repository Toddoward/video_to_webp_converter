# 🎬 MP4 to WebP Converter

[![English](https://img.shields.io/badge/lang-English-blue)](README.md)
[![Korean](https://img.shields.io/badge/lang-한국어-red)](README.ko.md)

고성능 MP4 비디오를 WebP 애니메이션으로 변환하는 웹 기반 도구입니다.

## ✨ 주요 기능

- 🎥 **MP4 → WebP 변환**: 고품질 애니메이션 WebP 생성
- 🎨 **다크/라이트 테마**: 시스템 설정 자동 감지 및 수동 전환
- 🌐 **다국어 지원**: 한국어/영어 자동 감지 및 전환
- 📐 **크기 조절**: 너비/높이 기준 리사이징
- 🎚️ **품질 설정**: 무손실/손실 압축 옵션
- 📁 **폴더 관리**: 웹 기반 출력 폴더 선택
- 🔌 **원클릭 종료**: GUI에서 서버 안전 종료

## 🚀 빠른 시작

### 자동 설치 및 실행 (권장)

1. **모든 파일을 한 폴더에 다운로드**
2. **`start.bat` 더블클릭**
3. **자동으로 설치 및 실행됩니다!**

### 수동 설치

```bash
# 1. Python 3.8+ 설치 확인
python --version

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 서버 실행
python app.py

# 4. 브라우저에서 접속
# http://localhost:5000
```

## 📁 프로젝트 구조

```
MP4-to-WebP-Converter/
├── start.bat              # 자동 설치 및 실행 스크립트
├── app.py                 # Flask 백엔드 서버
├── requirements.txt       # Python 패키지 목록
├── templates/
│   └── index.html        # 웹 프론트엔드
├── uploads/              # 업로드된 MP4 파일 (자동 생성)
├── outputs/              # 변환된 WebP 파일 (자동 생성)
└── venv/                 # 가상환경 (자동 생성)
```

## 🔧 시스템 요구사항

- **Python 3.8+**
- **Windows 10/11** (다른 OS에서도 동작하지만 배치파일은 Windows 전용)
- **최소 4GB RAM** (권장: 8GB+)
- **OpenCV 호환 시스템**

## 📋 의존성 패키지

- `Flask` - 웹 서버 프레임워크
- `opencv-python` - 비디오 처리
- `Pillow` - 이미지 처리 및 WebP 생성
- `psutil` - 시스템 리소스 모니터링
- `Werkzeug` - Flask 유틸리티
- `numpy` - 수치 연산

## 🎯 사용법

1. **파일 업로드**: MP4 파일을 드래그 앤 드롭 또는 버튼으로 선택
2. **설정 조정**: 품질, 압축률, FPS, 크기 등 조정
3. **출력 폴더**: 원하는 저장 위치 선택
4. **변환 시작**: "변환 시작" 버튼 클릭
5. **결과 다운로드**: 변환 완료 후 파일 다운로드

## 🌟 고급 기능

### 테마 전환
- 🌙/☀️ 버튼으로 다크/라이트 모드 전환
- 시스템 설정 자동 감지

### 언어 전환
- 🌐 버튼으로 한국어/영어 전환
- 브라우저 언어 자동 감지

### 서버 종료
- 🔌 버튼으로 안전한 서버 종료
- 웹페이지와 서버 모두 종료

## 🛠️ 문제 해결

### Python이 설치되지 않은 경우
- [Python 공식 사이트](https://www.python.org/downloads/)에서 다운로드
- 설치 시 "Add Python to PATH" 체크 필수

### 패키지 설치 실패
```bash
# pip 업그레이드
python -m pip install --upgrade pip

# 관리자 권한으로 실행
# 또는 가상환경 사용
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 포트 충돌
```python
# app.py 마지막 줄 수정
app.run(debug=True, host='0.0.0.0', port=5001)  # 포트 변경
```

## 📜 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

## 📞 지원

문제가 발생하면 이슈를 등록하거나 문의해주세요.

---

💡 **팁**: `start.bat` 파일을 바탕화면에 바로가기로 만들어두면 더욱 편리합니다!
