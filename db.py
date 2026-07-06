"""
Database Layer
---------------
Handles all persistent storage using SQLite (a single local file,
no server setup needed - perfect for a student project).

Tables:
- users            : login accounts (citizens + admins)
- saved_profiles   : profiles a logged-in citizen chose to save
- schemes          : the scheme knowledge base (editable via Admin Panel)
- search_logs      : one row per "Find My Schemes" click, used for analytics

On first run, schemes are imported once from data/schemes.json, and a
default admin account is created (username: admin, password: admin123 -
change this after your first login).
"""

import sqlite3
import json
import os
import hashlib
import secrets
from datetime import datetime
from collections import Counter
from dotenv import load_dotenv
load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), "scheme_app.db")
SEED_JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "schemes.json")

DEFAULT_ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def _get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ==================== INITIALIZATION ====================

def init_db():
    conn = _get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            created_at TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS saved_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            age INTEGER, gender TEXT, occupation TEXT, annual_income INTEGER,
            category TEXT, disability INTEGER, land_owner INTEGER,
            documents_owned TEXT,
            saved_at TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS schemes (
            id TEXT PRIMARY KEY,
            name TEXT, name_ta TEXT,
            sector TEXT, sector_ta TEXT,
            description TEXT, description_ta TEXT,
            eligibility TEXT,
            documents TEXT,
            how_to_apply TEXT,
            how_to_apply_ta TEXT,
            apply_link TEXT,
            office TEXT, office_ta TEXT,
            deadline TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            searched_at TEXT,
            age INTEGER, gender TEXT, occupation TEXT, annual_income INTEGER,
            category TEXT,
            matched_scheme_ids TEXT,
            matched_scheme_names TEXT,
            missing_documents TEXT
        )
    """)

    conn.commit()

    # One-time seed: import schemes.json into the schemes table if empty
    c.execute("SELECT COUNT(*) as cnt FROM schemes")
    if c.fetchone()["cnt"] == 0 and os.path.exists(SEED_JSON_PATH):
        with open(SEED_JSON_PATH, "r", encoding="utf-8") as f:
            seed_schemes = json.load(f)
        for s in seed_schemes:
            _insert_scheme_row(conn, s)
        conn.commit()

    # One-time seed: create a default admin account if no users exist yet
    c.execute("SELECT COUNT(*) as cnt FROM users")
    if c.fetchone()["cnt"] == 0:
        create_user(DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD, is_admin=True)

    conn.close()


# ==================== PASSWORD HELPERS ====================

def _hash_password(password, salt):
    return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()


# ==================== USERS ====================

def create_user(username, password, is_admin=False):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username = ?", (username,))
    if c.fetchone():
        conn.close()
        return False, "Username already exists."

    salt = secrets.token_hex(8)
    password_hash = _hash_password(password, salt)
    c.execute(
        "INSERT INTO users (username, password_hash, salt, is_admin, created_at) VALUES (?, ?, ?, ?, ?)",
        (username, password_hash, salt, int(is_admin), datetime.now().isoformat())
    )
    conn.commit()
    conn.close()
    return True, "Account created successfully."


def verify_user(username, password):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    if _hash_password(password, row["salt"]) != row["password_hash"]:
        return None
    return {"id": row["id"], "username": row["username"], "is_admin": bool(row["is_admin"])}


# ==================== SAVED PROFILES ====================

def save_profile(user_id, profile):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO saved_profiles
        (user_id, age, gender, occupation, annual_income, category, disability, land_owner, documents_owned, saved_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id, profile["age"], profile["gender"], profile["occupation"], profile["annual_income"],
        profile["category"], int(profile["disability"]), int(profile["land_owner"]),
        json.dumps(profile["documents_owned"]), datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()


def get_saved_profiles(user_id):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM saved_profiles WHERE user_id = ? ORDER BY saved_at DESC", (user_id,))
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({
            "id": row["id"],
            "age": row["age"], "gender": row["gender"], "occupation": row["occupation"],
            "annual_income": row["annual_income"], "category": row["category"],
            "disability": bool(row["disability"]), "land_owner": bool(row["land_owner"]),
            "documents_owned": json.loads(row["documents_owned"]),
            "saved_at": row["saved_at"],
        })
    return results


def delete_saved_profile(profile_id, user_id):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM saved_profiles WHERE id = ? AND user_id = ?", (profile_id, user_id))
    conn.commit()
    conn.close()


# ==================== SCHEMES (Admin Panel) ====================

def _insert_scheme_row(conn, s):
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO schemes
        (id, name, name_ta, sector, sector_ta, description, description_ta,
         eligibility, documents, how_to_apply, how_to_apply_ta, apply_link, office, office_ta, deadline)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        s["id"], s["name"], s.get("name_ta", s["name"]),
        s["sector"], s.get("sector_ta", s["sector"]),
        s["description"], s.get("description_ta", s["description"]),
        json.dumps(s["eligibility"]), json.dumps(s["documents"]),
        json.dumps(s["how_to_apply"]), json.dumps(s.get("how_to_apply_ta", s["how_to_apply"])),
        s["apply_link"], s["office"], s.get("office_ta", s["office"]), s["deadline"]
    ))


def _row_to_scheme(row):
    return {
        "id": row["id"], "name": row["name"], "name_ta": row["name_ta"],
        "sector": row["sector"], "sector_ta": row["sector_ta"],
        "description": row["description"], "description_ta": row["description_ta"],
        "eligibility": json.loads(row["eligibility"]),
        "documents": json.loads(row["documents"]),
        "how_to_apply": json.loads(row["how_to_apply"]),
        "how_to_apply_ta": json.loads(row["how_to_apply_ta"]),
        "apply_link": row["apply_link"],
        "office": row["office"], "office_ta": row["office_ta"],
        "deadline": row["deadline"],
    }


def get_all_schemes():
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM schemes")
    rows = c.fetchall()
    conn.close()
    return [_row_to_scheme(row) for row in rows]


def get_scheme(scheme_id):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM schemes WHERE id = ?", (scheme_id,))
    row = c.fetchone()
    conn.close()
    return _row_to_scheme(row) if row else None


def add_or_update_scheme(scheme_dict):
    conn = _get_conn()
    _insert_scheme_row(conn, scheme_dict)
    conn.commit()
    conn.close()


def delete_scheme(scheme_id):
    conn = _get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM schemes WHERE id = ?", (scheme_id,))
    conn.commit()
    conn.close()


# ==================== ANALYTICS ====================

def log_search(profile, results):
    """Records one 'Find My Schemes' event for the analytics dashboard."""
    matched_ids = [r["scheme"]["id"] for r in results]
    matched_names = [r["scheme"]["name"] for r in results]
    missing_docs = []
    for r in results:
        missing_docs.extend(r["documents"]["missing"])

    conn = _get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO search_logs
        (searched_at, age, gender, occupation, annual_income, category,
         matched_scheme_ids, matched_scheme_names, missing_documents)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(), profile["age"], profile["gender"], profile["occupation"],
        profile["annual_income"], profile["category"],
        json.dumps(matched_ids), json.dumps(matched_names), json.dumps(missing_docs)
    ))
    conn.commit()
    conn.close()


def get_analytics():
    conn = _get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM search_logs")
    rows = c.fetchall()
    conn.close()

    total_searches = len(rows)
    scheme_counter = Counter()
    missing_doc_counter = Counter()
    occupation_counter = Counter()
    ages = []

    for row in rows:
        for name in json.loads(row["matched_scheme_names"]):
            scheme_counter[name] += 1
        for doc in json.loads(row["missing_documents"]):
            missing_doc_counter[doc] += 1
        occupation_counter[row["occupation"]] += 1
        ages.append(row["age"])

    return {
        "total_searches": total_searches,
        "top_schemes": scheme_counter.most_common(10),
        "top_missing_docs": missing_doc_counter.most_common(10),
        "occupation_breakdown": occupation_counter.most_common(),
        "ages": ages,
    }
