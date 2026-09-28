# -*- coding: utf-8 -*-
"""
AURA Offline AI Health Platform - Local SQLite Database Engine
100% Offline, zero external network dependency.
"""
import os
import json
import sqlite3
import uuid
from datetime import datetime

DB_PATH = os.path.join("data", "aura_health.db")

def get_db_connection():
    """Returns a SQLite connection with dict-like row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes schema and seeds local knowledge base tables."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Conversations table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 2. Messages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        metadata TEXT,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
    )
    """)

    # 3. Diseases table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diseases (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        overview TEXT NOT NULL,
        causes TEXT,
        transmission TEXT,
        prevention TEXT,
        warning_signs TEXT,
        raw_json TEXT NOT NULL
    )
    """)

    # 4. Symptoms table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS symptoms (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT NOT NULL,
        warning_level TEXT NOT NULL,
        raw_json TEXT NOT NULL
    )
    """)

    # 5. Disease-Symptoms junction table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_symptoms (
        disease_id TEXT NOT NULL,
        symptom_id TEXT NOT NULL,
        PRIMARY KEY (disease_id, symptom_id),
        FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE,
        FOREIGN KEY (symptom_id) REFERENCES symptoms(id) ON DELETE CASCADE
    )
    """)

    # 6. Knowledge Documents table (RAG indexing documents)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_documents (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        doc_type TEXT NOT NULL,
        content TEXT NOT NULL,
        source TEXT NOT NULL
    )
    """)

    # 7. Settings table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)

    conn.commit()

    # Seed data if tables are empty
    seed_knowledge_base(conn)
    conn.close()

def seed_knowledge_base(conn):
    """Seeds diseases, symptoms, health tips, and RAG knowledge documents from data/ JSON files."""
    cursor = conn.cursor()

    # Seed Diseases
    cursor.execute("SELECT COUNT(*) FROM diseases")
    if cursor.fetchone()[0] == 0 and os.path.exists("data/diseases.json"):
        with open("data/diseases.json", "r", encoding="utf-8") as f:
            diseases_data = json.load(f)
        for d in diseases_data:
            cursor.execute("""
            INSERT OR REPLACE INTO diseases (id, name, category, overview, causes, transmission, prevention, warning_signs, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                d.get("id"),
                d.get("name"),
                d.get("category", "General"),
                d.get("overview", ""),
                "\n".join(d.get("causes", [])),
                "\n".join(d.get("transmission", [])),
                "\n".join(d.get("prevention", [])),
                "\n".join(d.get("warning_signs", [])),
                json.dumps(d, ensure_ascii=False)
            ))
            
            # Also insert RAG document for this disease
            content = f"{d.get('name')} ({d.get('category')}): {d.get('overview')}\nSymptoms: {', '.join(d.get('common_symptoms', []))}\nCauses: {', '.join(d.get('causes', []))}\nTransmission: {', '.join(d.get('transmission', []))}\nPrevention: {', '.join(d.get('prevention', []))}\nGeneral Care: {', '.join(d.get('general_care_information', []))}\nWarning Signs: {', '.join(d.get('warning_signs', []))}\nWhen to Seek Help: {d.get('when_to_seek_medical_help', '')}"
            cursor.execute("""
            INSERT OR REPLACE INTO knowledge_documents (id, title, category, doc_type, content, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"doc_dis_{d.get('id')}",
                d.get("name"),
                d.get("category", "General"),
                "disease",
                content,
                f"Local Health Knowledge Base → Diseases → {d.get('name')}"
            ))

    # Seed Symptoms
    cursor.execute("SELECT COUNT(*) FROM symptoms")
    if cursor.fetchone()[0] == 0 and os.path.exists("data/symptoms.json"):
        with open("data/symptoms.json", "r", encoding="utf-8") as f:
            symptoms_data = json.load(f)
        for s in symptoms_data:
            cursor.execute("""
            INSERT OR REPLACE INTO symptoms (id, name, category, description, warning_level, raw_json)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                s.get("id"),
                s.get("name"),
                s.get("category", "General"),
                s.get("description", ""),
                s.get("warning_level", "low"),
                json.dumps(s, ensure_ascii=False)
            ))

            content = f"Symptom: {s.get('name')} [{s.get('category')}] (Warning Level: {s.get('warning_level')})\nDescription: {s.get('description')}"
            cursor.execute("""
            INSERT OR REPLACE INTO knowledge_documents (id, title, category, doc_type, content, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"doc_sym_{s.get('id')}",
                s.get("name"),
                s.get("category", "General"),
                "symptom",
                content,
                f"Local Health Knowledge Base → Symptoms → {s.get('name')}"
            ))

    # Seed Health Tips into Knowledge Documents
    if os.path.exists("data/health_tips.json"):
        with open("data/health_tips.json", "r", encoding="utf-8") as f:
            tips_data = json.load(f)
        for idx, tip in enumerate(tips_data):
            content = f"Health Prevention Topic: {tip.get('title')} ({tip.get('category')})\nKey Guidelines:\n" + "\n".join([f"- {t}" for t in tip.get("tips", [])])
            cursor.execute("""
            INSERT OR REPLACE INTO knowledge_documents (id, title, category, doc_type, content, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"doc_tip_{idx}",
                tip.get("title"),
                tip.get("category"),
                "prevention",
                content,
                f"Local Health Knowledge Base → Prevention → {tip.get('category')}"
            ))

    # Seed Emergency Guidelines into Knowledge Documents
    if os.path.exists("data/emergency_guidelines.json"):
        with open("data/emergency_guidelines.json", "r", encoding="utf-8") as f:
            emer_data = json.load(f)
        for idx, em in enumerate(emer_data):
            content = f"EMERGENCY DIRECTIVE: {em.get('condition')} [Severity: {em.get('severity')}]\nKeywords: {', '.join(em.get('keywords', []))}\nImmediate Action: {em.get('immediate_action')}\nContraindications:\n" + "\n".join([f"- {c}" for c in em.get("contraindications", [])])
            cursor.execute("""
            INSERT OR REPLACE INTO knowledge_documents (id, title, category, doc_type, content, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"doc_emer_{idx}",
                em.get("condition"),
                "Emergency",
                "emergency_protocol",
                content,
                f"Local Clinical Safety Protocol → Emergency Triage → {em.get('condition')}"
            ))

    # Seed FAQs
    if os.path.exists("data/faq.json"):
        with open("data/faq.json", "r", encoding="utf-8") as f:
            faq_data = json.load(f)
        for idx, faq in enumerate(faq_data):
            content = f"Question: {faq.get('q')}\nVerified Answer: {faq.get('a')}"
            cursor.execute("""
            INSERT OR REPLACE INTO knowledge_documents (id, title, category, doc_type, content, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"doc_faq_{idx}",
                faq.get("q"),
                faq.get("category", "General"),
                "faq",
                content,
                "Local Health Knowledge Base → Health FAQs"
            ))

    conn.commit()


# ============================================================================
# CONVERSATIONS & CHAT HISTORY CRUD
# ============================================================================

def create_conversation(title="New Health Consultation"):
    """Creates a new conversation record and returns its ID."""
    conn = get_db_connection()
    conv_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    conn.execute(
        "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
        (conv_id, title, now, now)
    )
    conn.commit()
    conn.close()
    return conv_id

def get_conversations():
    """Returns all conversations ordered by recent activity."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM conversations ORDER BY updated_at DESC").fetchall()
    convs = [dict(r) for r in rows]
    conn.close()
    return convs

def get_conversation(conv_id):
    """Returns conversation details along with all messages."""
    conn = get_db_connection()
    conv = conn.execute("SELECT * FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not conv:
        conn.close()
        return None
    conv_dict = dict(conv)
    rows = conn.execute("SELECT * FROM messages WHERE conversation_id = ? ORDER BY timestamp ASC", (conv_id,)).fetchall()
    conv_dict["messages"] = [dict(r) for r in rows]
    conn.close()
    return conv_dict

def delete_conversation(conv_id):
    """Deletes a conversation and its messages."""
    conn = get_db_connection()
    conn.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
    conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    conn.close()
    return True

def rename_conversation(conv_id, new_title):
    """Renames an existing conversation."""
    conn = get_db_connection()
    now = datetime.now().isoformat()
    conn.execute("UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?", (new_title, now, conv_id))
    conn.commit()
    conn.close()
    return True

def add_message(conv_id, role, content, metadata=None):
    """Adds a message to a conversation and updates the conversation timestamp."""
    conn = get_db_connection()
    msg_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    meta_str = json.dumps(metadata) if metadata else None
    
    # Check if conversation exists; if not, create it
    c = conn.execute("SELECT id FROM conversations WHERE id = ?", (conv_id,)).fetchone()
    if not c:
        auto_title = content[:30] + ("..." if len(content) > 30 else "")
        conn.execute("INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                     (conv_id, auto_title, now, now))
    else:
        conn.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conv_id))

    conn.execute(
        "INSERT INTO messages (id, conversation_id, role, content, timestamp, metadata) VALUES (?, ?, ?, ?, ?, ?)",
        (msg_id, conv_id, role, content, now, meta_str)
    )
    conn.commit()
    conn.close()
    return msg_id


# ============================================================================
# DISEASE & SYMPTOM QUERIES
# ============================================================================

def get_all_diseases(category=None, search_query=None):
    """Returns diseases with optional category filtering and search query."""
    conn = get_db_connection()
    query = "SELECT * FROM diseases"
    params = []
    conditions = []

    if category and category.lower() != "all":
        conditions.append("LOWER(category) = ?")
        params.append(category.lower())

    if search_query:
        conditions.append("(LOWER(name) LIKE ? OR LOWER(overview) LIKE ? OR LOWER(causes) LIKE ?)")
        sq = f"%{search_query.lower()}%"
        params.extend([sq, sq, sq])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY name ASC"
    rows = conn.execute(query, params).fetchall()
    results = []
    for r in rows:
        d = dict(r)
        d["raw"] = json.loads(d["raw_json"])
        results.append(d)
    conn.close()
    return results

def get_disease_by_id(disease_id):
    """Returns complete disease record by ID."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM diseases WHERE id = ?", (disease_id,)).fetchone()
    conn.close()
    if not row:
        return None
    res = dict(row)
    res["raw"] = json.loads(res["raw_json"])
    return res

def get_all_symptoms(category=None):
    """Returns all symptoms for Symptom Explorer."""
    conn = get_db_connection()
    if category and category.lower() != "all":
        rows = conn.execute("SELECT * FROM symptoms WHERE LOWER(category) = ? ORDER BY name ASC", (category.lower(),)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM symptoms ORDER BY name ASC").fetchall()
    results = []
    for r in rows:
        s = dict(r)
        s["raw"] = json.loads(s["raw_json"])
        results.append(s)
    conn.close()
    return results

def get_knowledge_documents():
    """Returns all knowledge documents for RAG indexing."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM knowledge_documents").fetchall()
    docs = [dict(r) for r in rows]
    conn.close()
    return docs

def get_database_stats():
    """Returns statistics for dashboard (total diseases, symptoms, knowledge docs, conversations)."""
    conn = get_db_connection()
    diseases_count = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
    symptoms_count = conn.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0]
    docs_count = conn.execute("SELECT COUNT(*) FROM knowledge_documents").fetchone()[0]
    convs_count = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    conn.close()
    return {
        "diseases_count": diseases_count,
        "symptoms_count": symptoms_count,
        "knowledge_docs_count": docs_count,
        "conversations_count": convs_count,
        "mode": "offline",
        "database": "sqlite_local"
    }
