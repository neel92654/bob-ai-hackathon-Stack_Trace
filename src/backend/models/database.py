"""
Nexora — Database Connection & Query Utilities
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

import sqlite3
from src.backend.config.settings import DB_PATH

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    r = cur.fetchall()
    conn.close()
    if one:
        return dict(r[0]) if r else None
    return [dict(row) for row in r]

def execute_db(query, args=()):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    conn.close()
