"""Database connection helpers for MySQL and MongoDB."""
import mysql.connector
from mysql.connector import pooling
from pymongo import MongoClient
from config import Config

_mysql_pool = None
_mongo_client = None
_mongo_db = None


def init_mysql():
    global _mysql_pool
    _mysql_pool = pooling.MySQLConnectionPool(
        pool_name="unifind_pool",
        pool_size=10,
        pool_reset_session=True,
        **Config.MYSQL,
    )
    print(f"[DB] MySQL pool initialised -> {Config.MYSQL['host']}:{Config.MYSQL['port']}/{Config.MYSQL['database']}")


def init_mongo():
    global _mongo_client, _mongo_db
    _mongo_client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=3000)
    _mongo_db = _mongo_client[Config.MONGO_DB]
    print(f"[DB] MongoDB connected -> {Config.MONGO_URI}{Config.MONGO_DB}")


def mysql_conn():
    if _mysql_pool is None:
        init_mysql()
    return _mysql_pool.get_connection()


def mongo():
    if _mongo_db is None:
        init_mongo()
    return _mongo_db


def query(sql, params=None, one=False):
    """Run a SELECT and return dict results."""
    conn = mysql_conn()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(sql, params or ())
        rows = cur.fetchall()
        return (rows[0] if rows else None) if one else rows
    finally:
        cur.close()
        conn.close()


def execute(sql, params=None, return_id=False):
    """Run an INSERT/UPDATE/DELETE."""
    conn = mysql_conn()
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        conn.commit()
        return cur.lastrowid if return_id else cur.rowcount
    finally:
        cur.close()
        conn.close()
