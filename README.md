# 법령·행정규칙 트래킹 DB

(하단에 Mysql 설치방법 및 과정 있습니다.)

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
│  └─ seed_initial.sql
├─ scripts/
│  └─ load_full_text.py
├─ docs/
│  └─ DB_초기적재_정리본.xlsx
├─ .env.example
├─ .gitignore
├─ requirements.txt
└─ README.md
```

## DB 생성

MySQL Workbench에서 다음 순서로 실행합니다.

1. `database/schema.sql`
2. `database/seed_initial.sql`

확인:

```sql
USE law_tracking_db;

SELECT COUNT(*) AS law_count
FROM laws;

SELECT COUNT(*) AS administrative_rule_count
FROM administrative_rules;
```

정상 결과:

* 법령: 75건
* 행정규칙: 25건

## Python 패키지 설치

```bash
pip install -r requirements.txt
```

## 전문 JSON 입력 (현재는 미구현 상태로 필드만 존재 / 내용 추가 및 정정 필요)



해당 부분은 일단 임의로 만들어본 부분이고 테스트도 안해본 상태

```bash
python scripts/load_full_text.py
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



## MySQL 설치 및 실행 방법 (Windows)

본 프로젝트는 **MySQL Server 8.0**과 **MySQL Workbench**를 기준으로 작성되었습니다.

### 1. MySQL Installer 다운로드

1. 아래 MySQL 공식 다운로드 페이지에 접속합니다.

   [MySQL Installer for Windows](https://dev.mysql.com/downloads/installer/)

2. 설치 파일은 다음 중 하나를 선택합니다.

   * `mysql-installer-community-8.0.xx.msi`
     * 필요한 설치 파일이 포함된 전체 설치본
     * 인터넷 환경이 불안정한 경우 권장
   * `mysql-installer-web-community-8.0.xx.msi`
     * 설치 중 필요한 구성요소를 인터넷으로 내려받는 방식

3. Oracle 계정 로그인이 표시되면 `No thanks, just start my download`를 눌러도 됩니다.
4. 다운로드한 `.msi` 파일을 실행합니다.

> MySQL Installer에서 Server 다운로드 오류가 반복되면 Web Installer 대신 용량이 큰 전체 설치본을 사용합니다.

### 2. 설치 항목 선택

`Choosing a Setup Type` 화면에서 다음 중 하나를 선택합니다.

#### 간편 설치 (권장)

```text
Full
```

MySQL Server, MySQL Workbench, MySQL Shell 등 전체 구성요소를 설치합니다.

#### 필요한 항목만 설치 (선택)

```text
Custom
```

Custom을 선택한 경우 최소한 다음 두 항목을 추가합니다.

```text
MySQL Server 8.0
MySQL Workbench 8.0
```

본 프로젝트에는 MySQL Router, Samples and Examples, Documentation이 필수는 아닙니다.

### 3. MySQL Server 설정

#### Type and Networking

다음과 같이 설정합니다.

```text
Config Type: Development Computer
TCP/IP: 체크
Port: 3306
X Protocol Port: 33060
Named Pipe: 체크하지 않음
Shared Memory: 체크하지 않음
```

본인 PC에서만 사용할 경우 `Open Windows Firewall ports for network access`는 체크하지 않아도 됩니다.  
추후 외부 PC에서 접속해야 하는 경우 MySQL Installer의 `Reconfigure`에서 변경할 수 있습니다.

#### Authentication Method

다음 권장 옵션을 선택합니다.

```text
Use Strong Password Encryption for Authentication
```

#### Accounts and Roles

`root` 계정에서 사용할 비밀번호를 설정합니다.

```text
Username: root
Password: 설치 과정에서 직접 설정
```

해당 비밀번호는 MySQL Workbench 및 Python에서 DB에 접속할 때 사용하므로 별도로 보관합니다.  
비밀번호를 README나 GitHub 저장소에 입력하지 않습니다.

#### Windows Service

다음 기본 설정을 유지합니다.

```text
Configure MySQL Server as a Windows Service: 체크
Windows Service Name: MySQL80
Start the MySQL Server at System Startup: 체크
Standard System Account: 선택
```

#### Server File Permissions

첫 번째 옵션을 선택합니다.

```text
Yes, grant full access to the user running the Windows Service
and the administrators group only.
```

#### Apply Configuration

`Execute`를 누르고 모든 항목에 초록색 체크가 표시되는지 확인합니다.

MySQL Router 설정 화면이 나타나면 아래 항목은 체크하지 않고 종료합니다.

```text
Bootstrap MySQL Router for use with InnoDB Cluster
```

### 4. MySQL Workbench 실행 및 접속

설치 완료 후 MySQL Workbench를 실행합니다.

홈 화면에 `Local instance MySQL80`이 보이면 클릭한 뒤 설치 과정에서 설정한 `root` 비밀번호를 입력합니다.

연결 항목이 보이지 않으면 `MySQL Connections` 옆의 `+` 버튼을 누르고 다음과 같이 생성합니다. (우상단에 X로 팝업창 다지워보기)

```text
Connection Name: Local instance MySQL80
Hostname: 127.0.0.1
Port: 3306
Username: root
```

`Test Connection`을 눌러 연결이 성공하는지 확인한 뒤 저장합니다.

접속 후 새 SQL 탭에서 다음 쿼리를 실행하여 서버 상태를 확인합니다.

```sql
SELECT VERSION();
```

MySQL 버전이 출력되면 정상적으로 설치 및 실행된 상태입니다.

### 5. MySQL 서비스 실행 상태 확인

MySQL이 실행되지 않으면 Windows 검색에서 `서비스`를 실행한 뒤 다음 항목을 확인합니다.

```text
서비스 이름: MySQL80
상태: 실행 중
시작 유형: 자동
```

관리자 권한으로 명령 프롬프트를 실행한 경우 다음 명령으로 서비스를 시작하거나 중지할 수 있습니다.

```bat
net start MySQL80
net stop MySQL80
```

### 6. 설정 변경

포트, Windows 방화벽, 서비스 설정 등을 변경하려면 다음 순서로 진행합니다.

```text
MySQL Installer 실행
→ MySQL Server 선택
→ Reconfigure
```

설정 변경 후 `Apply Configuration`에서 다시 `Execute`를 눌러 적용합니다.




