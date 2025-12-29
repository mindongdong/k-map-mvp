#!/usr/bin/env python3
"""
단일세포 데이터 복원 스크립트
optimization_v2에서 덤프한 데이터를 k-map-mvp PostgreSQL에 복원

사용법:
    python restore_sc_data.py [--target-host HOST] [--target-port PORT]

환경변수:
    TARGET_DB_PASSWORD: 타겟 DB 비밀번호 (필수)
"""

import os
import re
import sys
import argparse
from pathlib import Path

# 테이블 매핑 (optimization_v2 -> k-map-mvp)
TABLE_MAPPING = {
    "public.datasets": "public.sc_datasets",
    "public.cells": "public.cells",
    "public.genes": "public.genes",
    "public.marker_genes": "public.marker_genes",
    "public.gene_expression": "public.gene_expression",
    "public.cluster_stats": "public.cluster_stats",
}


def convert_dump_file(input_path: Path, output_path: Path) -> None:
    """덤프 파일의 테이블명을 변환"""
    print(f"Converting {input_path} -> {output_path}")

    with open(input_path, 'r', encoding='utf-8') as infile:
        content = infile.read()

    # 테이블명 변환
    for old_table, new_table in TABLE_MAPPING.items():
        content = content.replace(old_table, new_table)

    # \restrict 라인 제거 (보안 관련)
    content = re.sub(r'^\\restrict.*$', '', content, flags=re.MULTILINE)

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

    print(f"Conversion complete: {output_path}")


def restore_to_postgres(sql_path: Path, host: str, port: int,
                        dbname: str, user: str, password: str) -> bool:
    """PostgreSQL에 데이터 복원"""
    import subprocess

    env = os.environ.copy()
    env['PGPASSWORD'] = password

    cmd = [
        'psql',
        '-h', host,
        '-p', str(port),
        '-U', user,
        '-d', dbname,
        '-f', str(sql_path)
    ]

    print(f"Restoring data to {host}:{port}/{dbname}...")

    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True,
            timeout=600  # 10분 타임아웃
        )

        if result.returncode == 0:
            print("Restore completed successfully!")
            return True
        else:
            print(f"Restore failed: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("Restore timed out after 10 minutes")
        return False
    except FileNotFoundError:
        print("psql command not found. Please ensure PostgreSQL client is installed.")
        return False


def main():
    parser = argparse.ArgumentParser(description='Restore single-cell data to k-map-mvp')
    parser.add_argument('--input', type=str, default='sc_data_dump.sql',
                        help='Input dump file (default: sc_data_dump.sql)')
    parser.add_argument('--convert-only', action='store_true',
                        help='Only convert the dump file, do not restore')
    parser.add_argument('--target-host', type=str, default='localhost',
                        help='Target PostgreSQL host (default: localhost)')
    parser.add_argument('--target-port', type=int, default=5432,
                        help='Target PostgreSQL port (default: 5432)')
    parser.add_argument('--target-db', type=str, default='kmap',
                        help='Target database name (default: kmap)')
    parser.add_argument('--target-user', type=str, default='kmap',
                        help='Target database user (default: kmap)')

    args = parser.parse_args()

    script_dir = Path(__file__).parent
    input_path = script_dir / args.input
    output_path = script_dir / 'sc_data_converted.sql'

    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)

    # 변환 실행
    convert_dump_file(input_path, output_path)

    if args.convert_only:
        print(f"Converted file saved to: {output_path}")
        return

    # 복원 실행
    password = os.environ.get('TARGET_DB_PASSWORD')
    if not password:
        print("Error: TARGET_DB_PASSWORD environment variable is required")
        sys.exit(1)

    success = restore_to_postgres(
        output_path,
        args.target_host,
        args.target_port,
        args.target_db,
        args.target_user,
        password
    )

    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
