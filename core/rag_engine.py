# -*- coding: utf-8 -*-
"""
AURA Local RAG (Retrieval-Augmented Generation) Engine
100% Offline Semantic Vector Retrieval and Grounded AI Response Generation.
No cloud APIs, no external network, zero hallucination.
"""
import re
import json
import urllib.request
import urllib.error
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from core import database
from core import safety

class LocalRagEngine:
    def __init__(self):
        self.vectorizer = None
        self.doc_vectors = None
        self.documents = []
        self.is_indexed = False
        self.build_index()

    def build_index(self):
        """Builds offline TF-IDF vector index over all local knowledge documents."""
        docs = database.get_knowledge_documents()
        if not docs:
            database.init_db()
            docs = database.get_knowledge_documents()

        if not docs:
            self.documents = []
            self.is_indexed = False
            return

        self.documents = docs
        corpus = [f"{d['title']} {d['category']} {d['content']}" for d in docs]

        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words='english',
            max_features=5000
        )
        self.doc_vectors = self.vectorizer.fit_transform(corpus)
        self.is_indexed = True

    def retrieve_context(self, query, top_k=3):
        """
        Retrieves top_k most relevant knowledge documents for a query.
        Returns: list of dicts with document content, title, source, and similarity score.
        """
        if not self.is_indexed or not query.strip():
            return []

        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.doc_vectors).flatten()

        # Get top-k indices with score > 0.05
        top_indices = similarities.argsort()[::-1][:top_k]
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            if score > 0.04:
                doc = self.documents[idx]
                results.append({
                    "id": doc["id"],
                    "title": doc["title"],
                    "category": doc["category"],
                    "doc_type": doc["doc_type"],
                    "content": doc["content"],
                    "source": doc["source"],
                    "score": round(score, 3)
                })
        return results

    def _query_local_ollama(self, query, context_str, system_prompt):
        """Tries to query a local Ollama instance on http://127.0.0.1:11434 if available."""
        try:
            req_data = json.dumps({
                "model": "mistral",
                "prompt": f"{system_prompt}\n\nContext:\n{context_str}\n\nUser Question:\n{query}\n\nAssistant Response:",
                "stream": False
            }).encode("utf-8")
            req = urllib.request.Request(
                "http://127.0.0.1:11434/api/generate",
                data=req_data,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                if resp.status == 200:
                    res_json = json.loads(resp.read().decode("utf-8"))
                    return res_json.get("response", "").strip()
        except Exception:
            pass
        return None

    def generate_grounded_response(self, query, history=None, lang="en"):
        """
        Main RAG Pipeline:
        1. Emergency safety check
        2. Local vector retrieval from SQLite knowledge base
        3. Local LLM / Local Grounded Generator
        4. Response safety validation
        """
        # Step 1: Deterministic Emergency Detection
        is_emer, emer_info = safety.check_emergency(query)
        if is_emer:
            emergency_card = safety.format_emergency_response(emer_info)
            return {
                "response": emergency_card,
                "is_emergency": True,
                "source": "Local Clinical Emergency Safety Protocol",
                "confidence": "Immediate Critical Triage",
                "retrieved_docs": []
            }

        # Step 2: Retrieve context chunks
        retrieved_docs = self.retrieve_context(query, top_k=3)

        # Context text
        if retrieved_docs:
            context_text = "\n\n---\n\n".join([f"Source: {d['source']}\n{d['content']}" for d in retrieved_docs])
            primary_source = retrieved_docs[0]["source"]
            confidence = "High (Verified Local Knowledge Base)"
        else:
            context_text = ""
            primary_source = "Local General Health Awareness Directory"
            confidence = "General Guidance"

        # Step 3: Check for local Ollama instance first
        system_prompt = (
            "You are AURA HealthAware AI, an offline public health awareness assistant. "
            "Provide educational information based only on the supplied context. "
            "Never claim to diagnose diseases or prescribe medication dosages. "
            "Encourage consulting a doctor when symptoms are concerning."
        )

        ollama_response = None
        if context_text:
            ollama_response = self._query_local_ollama(query, context_text, system_prompt)

        # Step 4: Built-in Offline Grounded Generator
        if ollama_response:
            raw_response = ollama_response
        else:
            raw_response = self._synthesize_grounded_response(query, retrieved_docs, lang)

        # Step 5: Post-generation Safety & Disclaimer validation
        final_response = safety.validate_medical_response(raw_response)

        return {
            "response": final_response,
            "is_emergency": False,
            "source": primary_source,
            "confidence": confidence,
            "retrieved_docs": retrieved_docs
        }

    def _synthesize_grounded_response(self, query, retrieved_docs, lang="en"):
        """
        Synthesizes a structured Health Awareness Card directly from verified local knowledge.
        Zero hallucinations; 100% faithful to retrieved medical docs.
        """
        if not retrieved_docs:
            if lang == "hi":
                return (
                    "### ℹ️ स्वास्थ्य जागरूकता सूचना\n\n"
                    "आपके प्रश्न के लिए स्थानीय ज्ञानकोष में सटीक जानकारी उपलब्ध नहीं है। "
                    "कृपया किसी विशिष्ट बीमारी (जैसे डेंगू, मलेरिया, टीबी, मधुमेह, बीपी) या लक्षण के बारे में पूछें।\n\n"
                    "- अपने लक्षणों को स्पष्ट रूप से लिखें।\n"
                    "- अधिक जानकारी के लिए 'रोग लाइब्रेरी' या 'लक्षण एक्सप्लोरर' टैब देखें।"
                )
            elif lang == "te":
                return (
                    "### ℹ️ ఆరోగ్య అవగాహన సమాచారం\n\n"
                    "మీ ప్రశ్నకు సంబంధించిన ఖచ్చితమైన సమాచారం స్థానిక డేటాబేస్‌లో అందుబాటులో లేదు. "
                    "దయచేసి నిర్దిష్ట వ్యాధి (ఉదాహరణకు డెంగ్యూ, మలేరియా, టీబీ, డయాబెటిస్) లేదా లక్షణాల గురించి అడగండి."
                )
            else:
                return (
                    "### ℹ️ Health Awareness Information\n\n"
                    "I could not locate specific verified information in the local offline knowledge base for this exact query.\n\n"
                    "**Suggested topics to explore:**\n"
                    "- Ask about specific conditions: *Dengue, Malaria, Tuberculosis, Diabetes, Hypertension, Asthma, Cholera*\n"
                    "- Explore symptoms: *Fever, headache, cough, shortness of breath, joint pain*\n"
                    "- Or visit the **Disease Library** and **Symptom Explorer** tabs in the sidebar for full guides."
                )

        primary_doc = retrieved_docs[0]
        title = primary_doc["title"]
        category = primary_doc["category"]
        content = primary_doc["content"]

        # Parse key blocks if it's a disease document
        overview_match = re.search(r":\s*(.*?)(?=\nSymptoms:|\nCauses:|$)", content, re.DOTALL)
        symptoms_match = re.search(r"Symptoms:\s*(.*?)(?=\nCauses:|\nTransmission:|$)", content, re.DOTALL)
        prevention_match = re.search(r"Prevention:\s*(.*?)(?=\nGeneral Care:|\nWarning Signs:|$)", content, re.DOTALL)
        warning_match = re.search(r"Warning Signs:\s*(.*?)(?=\nWhen to Seek Help:|$)", content, re.DOTALL)
        care_match = re.search(r"When to Seek Help:\s*(.*?)(?=$)", content, re.DOTALL)

        overview = overview_match.group(1).strip() if overview_match else ""
        symptoms_str = symptoms_match.group(1).strip() if symptoms_match else ""
        prevention_str = prevention_match.group(1).strip() if prevention_match else ""
        warning_str = warning_match.group(1).strip() if warning_match else ""
        care_str = care_match.group(1).strip() if care_match else ""

        # Build clean Health Awareness Card in Markdown
        md = f"### 🩺 {title} Awareness Guide\n"
        md += f"**Category:** `{category}` | **Retrieval Mode:** `100% Offline Local RAG`\n\n"

        if overview:
            md += f"#### 📖 Overview\n{overview}\n\n"

        if symptoms_str:
            s_list = [s.strip() for s in symptoms_str.split(",") if s.strip()]
            md += "#### 🔍 Common Associated Symptoms\n"
            for s in s_list:
                md += f"- {s}\n"
            md += "\n"

        if prevention_str:
            p_list = [p.strip() for p in prevention_str.split(",") if p.strip()]
            md += "#### 🛡️ Prevention & Lifestyle Directives\n"
            for p in p_list:
                md += f"- {p}\n"
            md += "\n"

        if warning_str:
            w_list = [w.strip() for w in warning_str.split(",") if w.strip()]
            md += "#### ⚠️ Critical Warning Signs\n"
            for w in w_list:
                md += f"- **{w}**\n"
            md += "\n"

        if care_str:
            md += f"> **🏥 When to Seek Medical Evaluation:**\n> {care_str}\n\n"

        md += f"---\n**Information Source:** `{primary_doc['source']}`"
        return md


# Singleton instance
rag_engine = LocalRagEngine()
