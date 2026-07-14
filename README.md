# 법령·행정규칙 트래킹 DB



## 현재 구현 범위

* 법령 테이블

  * 법령명
  * 법령 ID
  * 법령 일련번호
  * 법령 전문 JSON
  * DB 추가·수정 타임스탬프
* 행정규칙 테이블

  * 행정규칙명
  * 행정규칙 ID
  * 행정규칙 일련번호
  * 행정규칙 전문 JSON
  * DB 추가·수정 타임스탬프
* 법령 75건, 행정규칙 25건 초기 데이터 적재
* 전문 JSON 자동 입력 스크립트

## 폴더 구조

```text
law-tracking-db/
├─ database/
│  ├─ schema.sql
│  └─ seed\\\_initial.sql
├─ scripts/
│  └─ load\\\_full\\\_text.py
├─ docs/
│  └─ DB\\\_초기적재\\\_정리본.xlsx
├─ .env.example
├─ .gitignore
├─ requirements.txt
└─ README.md
```

## DB 생성

MySQL Workbench에서 다음 순서로 실행합니다.

1. `database/schema.sql`
2. `database/seed\\\_initial.sql`

확인:

```sql
USE law\\\_tracking\\\_db;

SELECT COUNT(\\\*) AS law\\\_count
FROM laws;

SELECT COUNT(\\\*) AS administrative\\\_rule\\\_count
FROM administrative\\\_rules;
```

정상 결과:

* 법령: 75건
* 행정규칙: 25건

## Python 패키지 설치

```bash
pip install -r requirements.txt
```

## 전문 JSON 입력 (추가 및 정정 필요)



해당 부분은 일단 임의로 만들어본 부분이고 테스트도 안해본 상태

```bash
python scripts/load\\\_full\\\_text.py
```

실행 시 다음 정보를 입력합니다.

* 국가법령정보 API OC
* MySQL root 비밀번호



## 보안 주의사항

다음 정보는 저장소에 커밋하지 않습니다.

* 국가법령정보 API OC 값
* MySQL root 비밀번호
* `.env` 파일
* 실제 운영 서버 접속 정보

`.env.example`에는 형식만 작성되어 있습니다.

