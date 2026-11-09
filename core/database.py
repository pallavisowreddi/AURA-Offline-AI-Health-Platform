# -*- coding: utf-8 -*-
"""
AURA Offline AI Health Platform - Local SQLite Database Engine
100% Offline, zero external network dependency.
Supports conversations, disease knowledge, MedQuAD RAG indexing,
biometric telemetry measurements, monitoring sessions, disease predictions, and BLE devices.
"""
import os
import json
import sqlite3
import uuid
import shutil
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGINAL_DB_PATH = os.path.join(BASE_DIR, "data", "aura_health.db")

# On Vercel / Serverless AWS Lambda, filesystem is read-only except /tmp
if os.environ.get("VERCEL"):
    TMP_DATA_DIR = os.path.join("/tmp", "data")
    os.makedirs(TMP_DATA_DIR, exist_ok=True)
    DB_PATH = os.path.join(TMP_DATA_DIR, "aura_health.db")
    if os.path.exists(ORIGINAL_DB_PATH) and not os.path.exists(DB_PATH):
        try:
            shutil.copy2(ORIGINAL_DB_PATH, DB_PATH)
        except Exception as e:
            print(f"[DB Warning] Could not copy DB to /tmp: {e}")
else:
    DB_PATH = ORIGINAL_DB_PATH

def get_db_connection():
    """Returns a SQLite connection with dict-like row factory."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    """Initializes schema and seeds local knowledge base tables."""
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

    # 8. Biometric Telemetry Measurements table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS measurements (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        device_id TEXT,
        metric_type TEXT NOT NULL,
        value REAL NOT NULL,
        secondary_value REAL,
        unit TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        source_type TEXT NOT NULL,
        signal_quality TEXT DEFAULT 'Good',
        notes TEXT
    )
    """)

    # 9. Monitoring Sessions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monitoring_sessions (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        start_time TEXT NOT NULL,
        end_time TEXT,
        session_type TEXT DEFAULT 'live_biometrics',
        avg_hr REAL,
        avg_spo2 REAL,
        readings_count INTEGER DEFAULT 0,
        status TEXT DEFAULT 'active',
        notes TEXT
    )
    """)

    # 10. Disease Predictions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_predictions (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        symptoms TEXT NOT NULL,
        predicted_condition TEXT NOT NULL,
        confidence REAL NOT NULL,
        top_conditions_json TEXT NOT NULL,
        model_version TEXT DEFAULT '1.0',
        timestamp TEXT NOT NULL,
        disclaimer_acknowledged INTEGER DEFAULT 1
    )
    """)

    # 11. Devices table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id TEXT PRIMARY KEY,
        device_name TEXT NOT NULL,
        device_type TEXT NOT NULL,
        mac_or_uuid TEXT NOT NULL,
        last_connected TEXT NOT NULL,
        is_active INTEGER DEFAULT 1
    )
    """)

    # 12. Emergency Events table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergency_events (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        trigger_type TEXT NOT NULL,
        description TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        resolved INTEGER DEFAULT 0
    )
    """)

    # 13. Medical Reports table (Persistent report library)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS medical_reports (
        id TEXT PRIMARY KEY,
        user_id TEXT DEFAULT 'local_user',
        filename TEXT NOT NULL,
        file_type TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        file_path TEXT NOT NULL,
        upload_date TEXT NOT NULL,
        processing_status TEXT NOT NULL,
        document_type TEXT DEFAULT 'lab_report',
        summary TEXT,
        extracted_biomarkers_json TEXT,
        extraction_warnings_json TEXT,
        analysis_json TEXT
    )
    """)

    conn.commit()

    # Seed data if tables are empty
    seed_knowledge_base(conn)
    conn.close()

def seed_knowledge_base(conn):
    """Seeds diseases, symptoms, health tips, emergency guidelines, and MedQuAD into knowledge documents."""
    cursor = conn.cursor()

    # Seed Diseases
    cursor.execute("SELECT COUNT(*) FROM diseases")
    diseases_file = os.path.join(BASE_DIR, "data", "diseases.json")
    if cursor.fetchone()[0] == 0 and os.path.exists(diseases_file):
        with open(diseases_file, "r", encoding="utf-8") as f:
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
    symptoms_file = os.path.join(BASE_DIR, "data", "symptoms.json")
    if cursor.fetchone()[0] == 0 and os.path.exists(symptoms_file):
        with open(symptoms_file, "r", encoding="utf-8") as f:
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

    # Seed Health Tips
    health_tips_file = os.path.join(BASE_DIR, "data", "health_tips.json")
    if os.path.exists(health_tips_file):
        with open(health_tips_file, "r", encoding="utf-8") as f:
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

    # Seed Emergency Guidelines
    emer_file = os.path.join(BASE_DIR, "data", "emergency_guidelines.json")
    if os.path.exists(emer_file):
        with open(emer_file, "r", encoding="utf-8") as f:
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
    faq_file = os.path.join(BASE_DIR, "data", "faq.json")
    if os.path.exists(faq_file):
        with open(faq_file, "r", encoding="utf-8") as f:
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

    # Seed MedQuAD
    medquad_path = os.path.join(BASE_DIR, "data", "medquad", "medquad_rag_knowledge.json")
    if os.path.exists(medquad_path):
        with open(medquad_path, "r", encoding="utf-8") as f:
            mq_data = json.load(f)
        for entry in mq_data:
            content = f"Medical Topic: {entry.get('topic')}\nClinical Question: {entry.get('question')}\nVerified Medical Guidance: {entry.get('answer')}\nFocus: {entry.get('focus')}"
            cursor.execute("""
            INSERT OR REPLACE INTO knowledge_documents (id, title, category, doc_type, content, source)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                f"doc_mq_{entry.get('id')}",
                entry.get("topic"),
                entry.get("category", "Clinical RAG"),
                "medquad_qa",
                content,
                f"Local Health Knowledge Base → MedQuAD Knowledge Repository → {entry.get('source')}"
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
    """Returns all symptoms for Disease Prediction selection."""
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


# ============================================================================
# BIOMETRICS & LIVE HEALTH CRUD
# ============================================================================

def save_measurement(metric_type, value, unit, secondary_value=None, source_type="MANUAL_ENTRY",
                     device_id=None, signal_quality="Good", notes="", user_id="local_user"):
    """
    Saves a biometric measurement into SQLite.
    source_type must be one of: 'REAL_DEVICE', 'SIMULATED', 'MANUAL_ENTRY', 'DATASET'
    """
    valid_sources = ["REAL_DEVICE", "SIMULATED", "MANUAL_ENTRY", "DATASET"]
    if source_type not in valid_sources:
        source_type = "MANUAL_ENTRY"

    conn = get_db_connection()
    meas_id = str(uuid.uuid4())
    now = datetime.now().isoformat()

    conn.execute("""
    INSERT INTO measurements (id, user_id, device_id, metric_type, value, secondary_value, unit, timestamp, source_type, signal_quality, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        meas_id,
        user_id,
        device_id,
        metric_type.lower(),
        float(value),
        float(secondary_value) if secondary_value is not None else None,
        unit,
        now,
        source_type,
        signal_quality,
        notes
    ))
    conn.commit()
    conn.close()
    return meas_id

def get_measurements(metric_type=None, limit=50, source_type=None):
    """Retrieves biometric measurements with optional filtering."""
    conn = get_db_connection()
    query = "SELECT * FROM measurements"
    params = []
    conds = []

    if metric_type and metric_type.lower() != "all":
        conds.append("metric_type = ?")
        params.append(metric_type.lower())

    if source_type:
        conds.append("source_type = ?")
        params.append(source_type)

    if conds:
        query += " WHERE " + " AND ".join(conds)

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(query, params).fetchall()
    results = [dict(r) for r in rows]
    conn.close()
    return results

def get_latest_vitals():
    """Returns the most recent reading for each of the 4 primary biometrics."""
    conn = get_db_connection()
    metrics = ["heart_rate", "spo2", "blood_pressure", "body_temperature"]
    latest = {}

    for m in metrics:
        row = conn.execute("""
        SELECT * FROM measurements WHERE metric_type = ? ORDER BY timestamp DESC LIMIT 1
        """, (m,)).fetchone()
        if row:
            latest[m] = dict(row)
        else:
            latest[m] = None

    conn.close()
    return latest

def get_vitals_trends(metric_type, days=7):
    """Returns timestamped series of measurements for trends graphing."""
    conn = get_db_connection()
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    rows = conn.execute("""
    SELECT timestamp, value, secondary_value, unit, source_type
    FROM measurements
    WHERE metric_type = ? AND timestamp >= ?
    ORDER BY timestamp ASC
    """, (metric_type.lower(), cutoff)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def save_monitoring_session(session_type="live_biometrics", user_id="local_user"):
    """Starts a monitoring session and returns its ID."""
    conn = get_db_connection()
    session_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    conn.execute("""
    INSERT INTO monitoring_sessions (id, user_id, start_time, session_type, status)
    VALUES (?, ?, ?, ?, 'active')
    """, (session_id, user_id, now, session_type))
    conn.commit()
    conn.close()
    return session_id

def stop_monitoring_session(session_id, avg_hr=None, avg_spo2=None, readings_count=0, notes=""):
    """Closes an active monitoring session with summary telemetry."""
    conn = get_db_connection()
    now = datetime.now().isoformat()
    conn.execute("""
    UPDATE monitoring_sessions
    SET end_time = ?, avg_hr = ?, avg_spo2 = ?, readings_count = ?, status = 'completed', notes = ?
    WHERE id = ?
    """, (now, avg_hr, avg_spo2, readings_count, notes, session_id))
    conn.commit()
    conn.close()
    return True


# ============================================================================
# DISEASE PREDICTIONS CRUD
# ============================================================================

def save_disease_prediction(symptoms, predicted_condition, confidence, top_conditions,
                            model_version="1.0", user_id="local_user"):
    """Stores a symptom prediction event with model version and top possibilities."""
    conn = get_db_connection()
    pred_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    conn.execute("""
    INSERT INTO disease_predictions (id, user_id, symptoms, predicted_condition, confidence, top_conditions_json, model_version, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pred_id,
        user_id,
        ", ".join(symptoms) if isinstance(symptoms, list) else str(symptoms),
        predicted_condition,
        float(confidence),
        json.dumps(top_conditions, ensure_ascii=False),
        model_version,
        now
    ))
    conn.commit()
    conn.close()
    return pred_id

def get_disease_predictions(limit=20):
    """Retrieves previous prediction records."""
    conn = get_db_connection()
    rows = conn.execute("""
    SELECT * FROM disease_predictions ORDER BY timestamp DESC LIMIT ?
    """, (limit,)).fetchall()
    results = []
    for r in rows:
        d = dict(r)
        d["top_conditions"] = json.loads(d["top_conditions_json"])
        results.append(d)
    conn.close()
    return results


# ============================================================================
# DEVICES & EMERGENCY LOGS
# ============================================================================

def register_or_update_device(device_name, device_type, mac_or_uuid):
    """Registers or updates a discovered BLE device."""
    conn = get_db_connection()
    row = conn.execute("SELECT id FROM devices WHERE mac_or_uuid = ?", (mac_or_uuid,)).fetchone()
    now = datetime.now().isoformat()
    if row:
        dev_id = row[0]
        conn.execute("""
        UPDATE devices SET device_name = ?, device_type = ?, last_connected = ?, is_active = 1 WHERE id = ?
        """, (device_name, device_type, now, dev_id))
    else:
        dev_id = str(uuid.uuid4())
        conn.execute("""
        INSERT INTO devices (id, device_name, device_type, mac_or_uuid, last_connected, is_active)
        VALUES (?, ?, ?, ?, ?, 1)
        """, (dev_id, device_name, device_type, mac_or_uuid, now))
    conn.commit()
    conn.close()
    return dev_id

def get_devices():
    """Lists registered devices."""
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM devices ORDER BY last_connected DESC").fetchall()
    devices = [dict(r) for r in rows]
    conn.close()
    return devices

def log_emergency_event(trigger_type, description, user_id="local_user"):
    """Logs a triggered emergency event in the audit trail."""
    conn = get_db_connection()
    event_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    conn.execute("""
    INSERT INTO emergency_events (id, user_id, trigger_type, description, timestamp, resolved)
    VALUES (?, ?, ?, ?, ?, 0)
    """, (event_id, user_id, trigger_type, description, now))
    conn.commit()
    conn.close()
    return event_id

def save_medical_report(filename, file_type, file_size, file_path,
                        processing_status="complete", document_type="lab_report",
                        summary="", extracted_biomarkers=None, extraction_warnings=None,
                        analysis=None, user_id="local_user", report_id=None):
    """Stores a user-specific medical report into SQLite."""
    conn = get_db_connection()
    if not report_id:
        report_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    conn.execute("""
    INSERT OR REPLACE INTO medical_reports (
        id, user_id, filename, file_type, file_size, file_path, upload_date,
        processing_status, document_type, summary, extracted_biomarkers_json,
        extraction_warnings_json, analysis_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        report_id,
        user_id,
        filename,
        file_type,
        int(file_size),
        file_path,
        now,
        processing_status,
        document_type,
        summary,
        json.dumps(extracted_biomarkers or [], ensure_ascii=False),
        json.dumps(extraction_warnings or [], ensure_ascii=False),
        json.dumps(analysis or {}, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()
    return report_id

def get_medical_reports(user_id="local_user", limit=50):
    """Retrieves user-specific medical reports."""
    conn = get_db_connection()
    rows = conn.execute("""
    SELECT * FROM medical_reports WHERE user_id = ? ORDER BY upload_date DESC LIMIT ?
    """, (user_id, limit)).fetchall()
    results = []
    for r in rows:
        item = dict(r)
        item["extracted_biomarkers"] = json.loads(item["extracted_biomarkers_json"] or "[]")
        item["extraction_warnings"] = json.loads(item["extraction_warnings_json"] or "[]")
        item["analysis"] = json.loads(item["analysis_json"] or "{}")
        results.append(item)
    conn.close()
    return results

def get_medical_report_by_id(report_id, user_id="local_user"):
    """Retrieves a single medical report with user isolation check."""
    conn = get_db_connection()
    row = conn.execute("""
    SELECT * FROM medical_reports WHERE id = ? AND user_id = ?
    """, (report_id, user_id)).fetchone()
    conn.close()
    if not row:
        return None
    item = dict(row)
    item["extracted_biomarkers"] = json.loads(item["extracted_biomarkers_json"] or "[]")
    item["extraction_warnings"] = json.loads(item["extraction_warnings_json"] or "[]")
    item["analysis"] = json.loads(item["analysis_json"] or "{}")
    return item

def delete_medical_report(report_id, user_id="local_user"):
    """Deletes a medical report and removes file from disk if present."""
    conn = get_db_connection()
    row = conn.execute("SELECT file_path FROM medical_reports WHERE id = ? AND user_id = ?", (report_id, user_id)).fetchone()
    if not row:
        conn.close()
        return False
    
    file_path = row[0]
    conn.execute("DELETE FROM medical_reports WHERE id = ? AND user_id = ?", (report_id, user_id))
    conn.commit()
    conn.close()

    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception:
            pass
    return True

def get_database_stats():
    """Returns statistics for dashboard (diseases, symptoms, knowledge docs, measurements, predictions)."""
    conn = get_db_connection()
    diseases_count = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
    symptoms_count = conn.execute("SELECT COUNT(*) FROM symptoms").fetchone()[0]
    docs_count = conn.execute("SELECT COUNT(*) FROM knowledge_documents").fetchone()[0]
    convs_count = conn.execute("SELECT COUNT(*) FROM conversations").fetchone()[0]
    meas_count = conn.execute("SELECT COUNT(*) FROM measurements").fetchone()[0]
    preds_count = conn.execute("SELECT COUNT(*) FROM disease_predictions").fetchone()[0]
    devices_count = conn.execute("SELECT COUNT(*) FROM devices").fetchone()[0]
    reports_count = conn.execute("SELECT COUNT(*) FROM medical_reports").fetchone()[0]
    conn.close()
    return {
        "diseases_count": diseases_count,
        "symptoms_count": symptoms_count,
        "knowledge_docs_count": docs_count,
        "conversations_count": convs_count,
        "measurements_count": meas_count,
        "predictions_count": preds_count,
        "devices_count": devices_count,
        "reports_count": reports_count,
        "mode": "offline",
        "database": "sqlite_local"
    }

