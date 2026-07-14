CREATE DATABASE IF NOT EXISTS law_tracking_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE law_tracking_db;

CREATE TABLE IF NOT EXISTS laws (
    law_name VARCHAR(255) NOT NULL COMMENT '법령명',
    law_id VARCHAR(50) NOT NULL COMMENT '법령 ID',
    law_serial_no VARCHAR(50) NOT NULL COMMENT '법령 일련번호',
    law_full_text JSON NOT NULL COMMENT '법령 전문 JSON',
    db_timestamp TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
        COMMENT 'DB 추가 또는 수정 시각',
    PRIMARY KEY (law_id, law_serial_no)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS administrative_rules (
    administrative_rule_name VARCHAR(255) NOT NULL COMMENT '행정규칙명',
    administrative_rule_id VARCHAR(50) NOT NULL COMMENT '행정규칙 ID',
    administrative_rule_serial_no VARCHAR(50) NOT NULL COMMENT '행정규칙 일련번호',
    administrative_rule_full_text JSON NOT NULL COMMENT '행정규칙 전문 JSON',
    db_timestamp TIMESTAMP NOT NULL
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
        COMMENT 'DB 추가 또는 수정 시각',
    PRIMARY KEY (
        administrative_rule_id,
        administrative_rule_serial_no
    )
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8mb4
COLLATE=utf8mb4_unicode_ci;
