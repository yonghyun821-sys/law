"""
국가법령정보 API에서 전문 JSON을 가져와 MySQL JSON 컬럼에 저장합니다.

설치:
    pip install requests mysql-connector-python

실행:
    python 전문_JSON_자동입력.py

처리 방식:
- 법령: target=law, MST=법령일련번호
- 행정규칙: target=admrul, ID=행정규칙일련번호
- 전문이 빈 JSON({})인 행만 처리
"""

import getpass
import json
import time
from pathlib import Path

import mysql.connector
import requests


API_URL = "https://www.law.go.kr/DRF/lawService.do"
ERROR_CSV = Path("전문_JSON_수집오류.csv")


def get_json(session: requests.Session, params: dict) -> dict:
    response = session.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    text = response.text.strip()

    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"JSON 응답이 아닙니다. Content-Type={content_type}, "
            f"응답 앞부분={text[:200]}"
        ) from exc

    if not isinstance(data, dict):
        raise RuntimeError("API 응답이 JSON 객체 형식이 아닙니다.")

    return data


def update_laws(cursor, connection, session, oc: str) -> tuple[int, list]:
    cursor.execute("""
        SELECT law_name, law_id, law_serial_no
        FROM laws
        WHERE JSON_LENGTH(law_full_text) = 0
        ORDER BY law_name
    """)
    rows = cursor.fetchall()

    success = 0
    errors = []

    for law_name, law_id, serial_no in rows:
        try:
            data = get_json(session, {
                "OC": oc,
                "target": "law",
                "type": "JSON",
                # 버전별 전문을 저장하기 위해 ID보다 MST(일련번호)를 사용
                "MST": serial_no,
            })

            cursor.execute("""
                UPDATE laws
                SET law_full_text = %s
                WHERE law_id = %s AND law_serial_no = %s
            """, (
                json.dumps(data, ensure_ascii=False),
                law_id,
                serial_no,
            ))
            connection.commit()
            success += 1
            print(f"[법령 성공] {law_name} ({law_id}/{serial_no})")

        except Exception as exc:
            connection.rollback()
            errors.append([
                "법령", law_name, law_id, serial_no, str(exc)
            ])
            print(f"[법령 실패] {law_name}: {exc}")

        time.sleep(0.2)

    return success, errors


def update_administrative_rules(
    cursor, connection, session, oc: str
) -> tuple[int, list]:
    cursor.execute("""
        SELECT
            administrative_rule_name,
            administrative_rule_id,
            administrative_rule_serial_no
        FROM administrative_rules
        WHERE JSON_LENGTH(administrative_rule_full_text) = 0
        ORDER BY administrative_rule_name
    """)
    rows = cursor.fetchall()

    success = 0
    errors = []

    for rule_name, rule_id, serial_no in rows:
        try:
            data = get_json(session, {
                "OC": oc,
                "target": "admrul",
                "type": "JSON",
                # 행정규칙 본문 API의 ID는 행정규칙 일련번호
                "ID": serial_no,
            })

            cursor.execute("""
                UPDATE administrative_rules
                SET administrative_rule_full_text = %s
                WHERE administrative_rule_id = %s
                  AND administrative_rule_serial_no = %s
            """, (
                json.dumps(data, ensure_ascii=False),
                rule_id,
                serial_no,
            ))
            connection.commit()
            success += 1
            print(f"[행정규칙 성공] {rule_name} ({rule_id}/{serial_no})")

        except Exception as exc:
            connection.rollback()
            errors.append([
                "행정규칙", rule_name, rule_id, serial_no, str(exc)
            ])
            print(f"[행정규칙 실패] {rule_name}: {exc}")

        time.sleep(0.2)

    return success, errors


def save_errors(errors: list[list[str]]) -> None:
    if not errors:
        return

    import csv

    with ERROR_CSV.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["구분", "이름", "ID", "일련번호", "오류"])
        writer.writerows(errors)


def main() -> None:
    print("API 인증값과 MySQL 정보를 입력하세요.")
    oc = getpass.getpass("국가법령정보 API OC: ").strip()
    mysql_password = getpass.getpass("MySQL root 비밀번호: ")

    connection = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password=mysql_password,
        database="law_tracking_db",
        charset="utf8mb4",
    )
    cursor = connection.cursor()

    session = requests.Session()
    session.headers.update({
        "User-Agent": "law-tracking-db-loader/1.0"
    })

    try:
        law_success, law_errors = update_laws(
            cursor, connection, session, oc
        )
        rule_success, rule_errors = update_administrative_rules(
            cursor, connection, session, oc
        )

        errors = law_errors + rule_errors
        save_errors(errors)

        print()
        print("=== 처리 결과 ===")
        print(f"법령 전문 저장 성공: {law_success}건")
        print(f"행정규칙 전문 저장 성공: {rule_success}건")
        print(f"오류: {len(errors)}건")

        if errors:
            print(f"오류 목록: {ERROR_CSV.resolve()}")

    finally:
        cursor.close()
        connection.close()
        session.close()


if __name__ == "__main__":
    main()
