import os
import datetime
import pickle
import re
import warnings
import numpy as np
import cv2
from PIL import Image
import sklearn
import sklearn.ensemble
try:
    from rapidocr_onnxruntime import RapidOCR
    _ocr_engine = RapidOCR()
except Exception as e:
    _ocr_engine = None

import io

# Suppress feature names user warnings when passing numpy array to model
warnings.filterwarnings("ignore", category=UserWarning)

# Paths to models
SYMPTOM_MODEL_PATH = "models/symptom_model.pkl"
SYMPTOMS_LIST_PATH = "models/symptoms_list.pkl"
IMAGE_MODEL_PATH = "models/image_model.pkl"

# Initialize caches
_symptom_model = None
_symptoms_list = None
_image_model = None

# Multilingual Symptom Vocabularies (English, Hindi, Telugu)
SYMPTOM_VOCAB = {
    "en": {
        "fever": ["fever", "high temp", "temperature", "feverish", "hot body"],
        "high_fever": ["high fever", "burning fever", "very hot body", "severe fever"],
        "fatigue": ["fatigue", "tired", "exhausted", "weakness", "lethargy", "sleepy", "tiredness"],
        "headache": ["headache", "head pain", "pain in head", "head ache"],
        "throbbing_headache": ["throbbing headache", "migraine headache", "pulsing headache", "one side headache"],
        "sore_throat": ["sore throat", "throat pain", "throat irritation", "swallowing pain"],
        "body_ache": ["body ache", "body pain", "muscle pain", "body aches", "muscle ache", "generalized pain"],
        "runny_nose": ["runny nose", "congested", "congestion", "blocked nose", "nasal blockage", "sneezing nose"],
        "shortness_of_breath": ["shortness of breath", "breathless", "difficulty breathing", "breathing issue", "gasping"],
        "wheezing": ["wheezing", "whistling breath", "chest whistling", "wheeze"],
        "chest_tightness": ["chest tightness", "tight chest", "heavy chest", "chest pressure"],
        "chest_pain": ["chest pain", "pain in chest", "heart pain", "angina pain"],
        "neck_radiating_pain": ["neck pain", "radiating pain to arm", "jaw pain", "left arm pain", "shoulder radiating pain"],
        "palpitations": ["palpitations", "fluttering heart", "heart racing", "skipping beats"],
        "rapid_heartbeat": ["rapid heartbeat", "fast pulse", "tachycardia", "pounding heart"],
        "swollen_legs_ankles": ["swollen legs", "swollen ankles", "edema", "puffy feet", "water retention legs"],
        "cold_hands_feet": ["cold hands", "cold feet", "chilly extremities", "pale extremities"],
        "loss_of_taste_smell": ["loss of taste", "loss of smell", "cannot taste", "cannot smell", "taste loss"],
        "nausea": ["nausea", "nauseous", "feeling sick", "vomit sensation", "queasy"],
        "vomiting": ["vomiting", "vomit", "throw up", "vomited", "throwing up"],
        "diarrhea": ["diarrhea", "loose motion", "watery stool", "motions", "frequent stools"],
        "watery_diarrhea": ["watery diarrhea", "rice water stool", "severe loose motions", "liquid stools"],
        "stomach_pain": ["stomach pain", "stomach ache", "tummy ache", "abdominal pain", "belly pain"],
        "burning_stomach_pain": ["burning stomach pain", "burning belly", "stomach burning", "epigastric burn"],
        "heartburn": ["heartburn", "acid reflux", "chest burn after eating", "sour burp", "acidity"],
        "acid_regurgitation": ["acid regurgitation", "sour taste in mouth", "food coming back up", "acid burps"],
        "loss_of_appetite": ["loss of appetite", "no hunger", "not feeling like eating", "reduced appetite"],
        "increased_thirst": ["excessive thirst", "increased thirst", "always thirsty", "dry mouth thirst", "polydipsia", "drinking lots of water"],
        "increased_hunger": ["increased hunger", "always hungry", "excessive hunger", "polyphagia"],
        "frequent_urination": ["frequent urination", "peeing a lot", "urinating often", "waking up to pee", "polyuria"],
        "burning_urination": ["burning urination", "pain when peeing", "dysuria", "stinging urine", "urine burn"],
        "dark_urine": ["dark urine", "brown urine", "tea colored urine", "yellow dark urine"],
        "pale_stools": ["pale stools", "clay colored stool", "white stool"],
        "rash": ["rash", "skin rash", "spots", "red spots", "eruption"],
        "itching": ["itching", "itch", "itchy", "scratching", "pruritus"],
        "dry_skin": ["dry skin", "flaky skin", "skin dryness", "rough skin"],
        "skin_redness": ["redness", "red skin", "inflammation", "skin red", "erythema"],
        "blisters": ["blisters", "blister", "fluid-filled bumps", "bubbles on skin"],
        "silvery_scales": ["silvery scales", "flaking skin plaques", "scaly skin patches", "psoriasis plaques"],
        "acne_pimples": ["pimples", "acne", "whiteheads", "blackheads", "zits", "breakouts"],
        "slow_healing_sores": ["slow healing sores", "wounds not healing", "cuts not closing", "foot ulcers"],
        "yellow_skin_eyes": ["yellow eyes", "yellow skin", "jaundice eyes", "yellowish sclera"],
        "joint_pain": ["joint pain", "joint ache", "pain in joints", "knee pain", "elbow pain", "finger joint pain"],
        "joint_swelling": ["joint swelling", "swollen joints", "puffy knees", "swollen fingers"],
        "joint_stiffness": ["joint stiffness", "stiff joints in morning", "hard to move joints"],
        "muscle_weakness": ["muscle weakness", "weak muscles", "limb weakness", "loss of muscle strength"],
        "muscle_cramps": ["muscle cramps", "cramping", "spasms", "leg cramps"],
        "chills": ["chills", "cold shivers", "shivering", "feeling cold"],
        "sweating": ["sweating", "profuse sweat", "excessive sweat", "sweat"],
        "night_sweats": ["night sweats", "sweating at night", "waking up drenched in sweat"],
        "sneezing": ["sneezing", "sneeze", "sneezed", "continuous sneezing"],
        "itchy_eyes": ["itchy eyes", "watery eyes", "red eyes", "eye irritation"],
        "unexplained_weight_loss": ["weight loss", "losing weight without trying", "drastic weight loss", "unintentional weight loss"],
        "unexplained_weight_gain": ["weight gain", "gaining weight rapidly", "unexplained weight gain"],
        "weakness": ["weakness", "feeling weak", "lack of energy", "physical exhaustion"],
        "dizziness": ["dizziness", "dizzy", "lightheaded", "feeling faint", "spinning head"],
        "blurred_vision": ["blurred vision", "blurry eyes", "fuzzy vision", "cannot see clearly"],
        "numbness_one_side": ["numbness on one side", "facial droop", "arm numbness", "weakness on one side", "hemiplegia"],
        "slurred_speech": ["slurred speech", "difficulty speaking", "garbled words", "cannot talk properly"],
        "confusion": ["confusion", "disoriented", "memory haze", "mental confusion"],
        "excessive_body_fat": ["excessive body fat", "obesity", "belly fat accumulation", "high BMI"],
        "cold_sensitivity": ["cold sensitivity", "cannot tolerate cold", "feeling cold always"],
        "heat_sensitivity": ["heat sensitivity", "cannot tolerate heat", "feeling hot always"],
        "tremors": ["tremors", "shaky hands", "hand trembling", "shivering hands"]
    },
    "hi": {
        "fever": ["बुखार", "ज्वर", "bukhar", "tapman"],
        "high_fever": ["तेज बुखार", "तीव्र बुखार", "tej bukhar"],
        "fatigue": ["थकान", "कमजोरी", "thakan", "kamzori"],
        "headache": ["सिरदर्द", "सर दर्द", "sir dard"],
        "throbbing_headache": ["आधासीसी", "माइग्रेन दर्द", "तेज सिरदर्द"],
        "sore_throat": ["गले में खराश", "गले में दर्द", "gale me dard"],
        "body_ache": ["बदन दर्द", "शरीर में दर्द", "badan dard"],
        "runny_nose": ["बहती नाक", "नाक बहना", "naak behna"],
        "shortness_of_breath": ["सांस लेने में कठिनाई", "सांस फूलना", "saans phoolna"],
        "wheezing": ["सांस में सीटी की आवाज", "घरघराहट"],
        "chest_tightness": ["छाती में जकड़न", "सीने में दबाव"],
        "chest_pain": ["सीने में दर्द", "छाती में दर्द", "seene me dard"],
        "neck_radiating_pain": ["गर्दन और हाथ में दर्द", "बाएं हाथ में दर्द"],
        "palpitations": ["दिल की धड़कन तेज होना", "घबराहट"],
        "swollen_legs_ankles": ["पैरों में सूजन", "टखनों में सूजन"],
        "loss_of_taste_smell": ["स्वाद या गंध न आना", "स्वाद चला जाना"],
        "nausea": ["जी मिचलाना", "उल्टी जैसा लगना", "ji michlana"],
        "vomiting": ["उल्टी", "उल्टियां", "ulti"],
        "diarrhea": ["दस्त", "पतले दस्त", "dast"],
        "watery_diarrhea": ["पानी जैसा दस्त", "हैजा दस्त"],
        "stomach_pain": ["पेट दर्द", "पेट में दर्द", "pet dard"],
        "burning_stomach_pain": ["पेट में जलन", "pet me jalan"],
        "heartburn": ["सीने में जलन", "खट्टी डकारें", "एसिडिटी"],
        "increased_thirst": ["अधिक प्यास लगना", "बार-बार प्यास"],
        "frequent_urination": ["बार-बार पेशाब आना", "पेशाब की अधिकता"],
        "burning_urination": ["पेशाब में जलन", "पेशाब करते समय दर्द"],
        "dark_urine": ["पीला या गहरा पेशाब"],
        "rash": ["चकत्ते", "लाल चकत्ते", "rash"],
        "itching": ["खुजली", "khujli"],
        "dry_skin": ["रूखी त्वचा", "सूखी त्वचा"],
        "skin_redness": ["त्वचा का लाल होना"],
        "blisters": ["छाले", "फफोले", "पानी वाले दाने"],
        "silvery_scales": ["सफेद पपड़ी", "चांदी जैसी पपड़ी"],
        "acne_pimples": ["मुंहासे", "पिंपल्स", "कील"],
        "yellow_skin_eyes": ["पीलिया", "आंखों का पीलापन", "पीली त्वचा"],
        "joint_pain": ["जोड़ों का दर्द", "घुटनों का दर्द", "jodon me dard"],
        "joint_swelling": ["जोड़ों में सूजन"],
        "joint_stiffness": ["जोड़ों की अकड़न"],
        "chills": ["ठंड लगना", "कंपकंपी"],
        "sweating": ["पसीना आना", "अधिक पसीना"],
        "night_sweats": ["रात में पसीना आना"],
        "sneezing": ["छींकें", "छींक आना"],
        "itchy_eyes": ["आंखों में खुजली"],
        "unexplained_weight_loss": ["वजन कम होना", "अचानक वजन घटना"],
        "unexplained_weight_gain": ["वजन बढ़ना", "मोटापा बढ़ना"],
        "weakness": ["कमजोरी", "अशक्तता"],
        "dizziness": ["चक्कर आना", "चक्कर"],
        "blurred_vision": ["धुंधला दिखना", "आंखों में धुंधलापन"],
        "numbness_one_side": ["एक तरफ सुन्न होना", "लकवा जैसा लगना"],
        "slurred_speech": ["बोली में लड़खड़ाहट", "बोलने में दिक्कत"]
    },
    "te": {
        "fever": ["జ్వరం", "వేడి ఒళ్ళు", "jwaram"],
        "high_fever": ["తీవ్రమైన జ్వరం", "ఎక్కువ జ్వరం"],
        "fatigue": ["అలసట", "నీరసం", "alasata", "neerasam"],
        "headache": ["తలనొప్పి", "తలపోటు", "talanopik"],
        "throbbing_headache": ["పార్శ్వపు తలనొప్పి", "మైగ్రేన్ నొప్పి"],
        "sore_throat": ["గొంతు నొప్పి", "గొంతు మంట", "gonthu noppi"],
        "body_ache": ["ఒళ్ళు నొప్పులు", "కండరాల నొప్పులు", "ollu noppulu"],
        "runny_nose": ["ముక్కు కారడం", "ముక్కు దిబ్బడ", "mukku karadam"],
        "shortness_of_breath": ["శ్వాస ఆడకపోవడం", "ఆయాసం", "aayasam"],
        "wheezing": ["శ్వాసలో పిల్లికూతలు", "ఈల వేసినట్లు శబ్దం"],
        "chest_tightness": ["ఛాతీలో పట్టేసినట్లు ఉండటం"],
        "chest_pain": ["ఛాతీ నొప్పి", "గుండె నొప్పి", "chathi noppi"],
        "neck_radiating_pain": ["మెడ మరియు ఎడమ చేతికి నొప్పి పాకడం"],
        "palpitations": ["గుండె దడ", "గుండె వేగంగా కొట్టుకోవడం"],
        "swollen_legs_ankles": ["కాళ్ల వాపు", "పాదాల వాపు"],
        "loss_of_taste_smell": ["రుచి మరియు వాసన తెలియకపోవడం"],
        "nausea": ["వికారం", "వాంతి వచ్చేలా ఉండటం", "vikaaram"],
        "vomiting": ["వాంతులు", "vaanthulu"],
        "diarrhea": ["విరేచనాలు", "నీళ్ల విరేచనాలు", "virechanalu"],
        "watery_diarrhea": ["బియ్యపు కడుగు నీళ్ల వంటి విరేచనాలు"],
        "stomach_pain": ["కడుపు నొప్పి", "kadupu noppi"],
        "burning_stomach_pain": ["కడుపులో మంట", "ఆసిడిటీ"],
        "heartburn": ["ఛాతీలో మంట", "పుల్లటి తేన్పులు"],
        "increased_thirst": ["ఎక్కువ దాహం", "అధిక దాహం"],
        "frequent_urination": ["తరచుగా మూత్రవిసర్జన", "రాత్రిపూట మూత్రం"],
        "burning_urination": ["మూత్రంలో మంట", "మూత్ర విసర్జన నొప్పి"],
        "dark_urine": ["ముదురు పసుపు మూత్రం"],
        "rash": ["దద్దుర్లు", "ఎర్రటి మచ్చలు", "daddurlu"],
        "itching": ["దురద", "గజ్జి", "durada"],
        "dry_skin": ["పొడి చర్మం"],
        "skin_redness": ["చర్మం ఎర్రబడటం"],
        "blisters": ["బొబ్బలు", "నీటి గుల్లలు"],
        "silvery_scales": ["వెండి రంగు పొలుసులు"],
        "acne_pimples": ["మొటిమలు", "pimples"],
        "yellow_skin_eyes": ["కామెర్లు", "కళ్లు పసుపు రంగులోకి మారడం", "jaundice"],
        "joint_pain": ["కీళ్ల నొప్పులు", "మోకాళ్ల నొప్పులు", "keella noppulu"],
        "joint_swelling": ["కీళ్ల వాపు"],
        "joint_stiffness": ["కీళ్లు బిగుసుకుపోవడం"],
        "chills": ["చలి జ్వరం", "వణుకు"],
        "sweating": ["చెమటలు పట్టడం"],
        "night_sweats": ["రాత్రిపూట చెమటలు"],
        "sneezing": ["తుమ్ములు", "tummulu"],
        "itchy_eyes": ["కళ్లలో దురద", "నీరు కారడం"],
        "unexplained_weight_loss": ["బరువు తగ్గడం", "అకస్మాత్తుగా బరువు తగ్గడం"],
        "unexplained_weight_gain": ["విపరీతంగా బరువు పెరగడం"],
        "weakness": ["బలహీనత", "నీరసం"],
        "dizziness": ["తల తిరగడం", "కళ్లు తిరగడం"],
        "blurred_vision": ["మసక బారిన చూపు"],
        "numbness_one_side": ["శరీరం ఒక వైపు తిమ్మిరి", "పక్షవాతం లక్షణాలు"],
        "slurred_speech": ["మాట ముద్దబడటం", "స్పష్టంగా మాట్లాడలేకపోవడం"]
    }
}

# 34 Disease Symptoms Profiles
disease_symptoms = {
    "Diabetes": ["increased_thirst", "frequent_urination", "unexplained_weight_loss", "fatigue", "blurred_vision", "slow_healing_sores", "increased_hunger"],
    "Hypertension": ["headache", "dizziness", "shortness_of_breath", "palpitations", "blurred_vision", "chest_pain"],
    "Asthma": ["shortness_of_breath", "wheezing", "chest_tightness", "cough", "fatigue"],
    "Arthritis": ["joint_pain", "joint_stiffness", "joint_swelling", "muscle_weakness"],
    "Cancer (Early Warning)": ["unexplained_weight_loss", "fatigue", "weakness", "loss_of_appetite", "night_sweats"],
    "Obesity": ["excessive_body_fat", "shortness_of_breath", "fatigue", "joint_pain", "sweating"],
    "Dengue Fever": ["high_fever", "fever", "headache", "joint_pain", "rash", "nausea", "fatigue", "body_ache"],
    "Malaria": ["fever", "high_fever", "chills", "sweating", "headache", "nausea", "body_ache"],
    "Typhoid Fever": ["high_fever", "fever", "stomach_pain", "headache", "weakness", "diarrhea", "loss_of_appetite"],
    "Tuberculosis": ["cough_with_blood", "cough", "night_sweats", "unexplained_weight_loss", "chest_pain", "fever", "fatigue"],
    "Pneumonia": ["cough_with_phlegm", "high_fever", "chills", "shortness_of_breath", "chest_pain", "fatigue"],
    "COVID-19": ["fever", "cough", "fatigue", "shortness_of_breath", "loss_of_taste_smell", "sore_throat", "body_ache"],
    "Influenza": ["high_fever", "fever", "body_ache", "chills", "headache", "fatigue", "cough", "sore_throat"],
    "Common Cold": ["runny_nose", "sneezing", "sore_throat", "cough", "fatigue"],
    "Chickenpox": ["blisters", "rash", "itching", "fever", "fatigue", "loss_of_appetite"],
    "Gastroenteritis": ["watery_diarrhea", "diarrhea", "vomiting", "nausea", "stomach_pain", "fatigue"],
    "Cholera": ["watery_diarrhea", "vomiting", "muscle_cramps", "increased_thirst", "weakness"],
    "Hepatitis": ["yellow_skin_eyes", "dark_urine", "pale_stools", "fatigue", "nausea", "stomach_pain"],
    "Jaundice": ["yellow_skin_eyes", "dark_urine", "itching", "fatigue", "loss_of_appetite"],
    "Coronary Artery Disease": ["chest_pain", "neck_radiating_pain", "shortness_of_breath", "palpitations", "cold_hands_feet"],
    "Stroke (TIA Warning)": ["numbness_one_side", "slurred_speech", "confusion", "dizziness", "throbbing_headache"],
    "Chronic Kidney Disease": ["swollen_legs_ankles", "frequent_urination", "fatigue", "dark_urine", "shortness_of_breath"],
    "Anemia": ["fatigue", "weakness", "cold_hands_feet", "dizziness", "shortness_of_breath"],
    "Hypothyroidism": ["unexplained_weight_gain", "fatigue", "cold_sensitivity", "dry_skin", "muscle_weakness"],
    "Hyperthyroidism": ["unexplained_weight_loss", "rapid_heartbeat", "palpitations", "heat_sensitivity", "tremors"],
    "Migraine": ["throbbing_headache", "headache", "nausea", "blurred_vision", "vomiting"],
    "GERD (Acid Reflux)": ["heartburn", "acid_regurgitation", "burning_stomach_pain", "chest_pain"],
    "Peptic Ulcer": ["burning_stomach_pain", "stomach_pain", "heartburn", "nausea", "loss_of_appetite"],
    "Urinary Tract Infection": ["burning_urination", "frequent_urination", "stomach_pain", "dark_urine"],
    "Allergic Rhinitis": ["sneezing", "runny_nose", "itchy_eyes", "itching", "sore_throat"],
    "Food Allergy": ["itching", "rash", "stomach_pain", "vomiting", "shortness_of_breath"],
    "Eczema": ["itching", "dry_skin", "skin_redness", "rash"],
    "Psoriasis": ["silvery_scales", "skin_redness", "dry_skin", "itching", "joint_pain"],
    "Acne Vulgaris": ["acne_pimples", "skin_redness", "dry_skin"]
}

# Symptom Specificity Weights
SYMPTOM_WEIGHTS = {
    "fever": 1.0, "high_fever": 2.2, "fatigue": 0.8, "chills": 2.2, "sweating": 2.0, "night_sweats": 3.5,
    "unexplained_weight_loss": 3.2, "unexplained_weight_gain": 3.0, "weakness": 0.9, "dizziness": 1.5,
    "headache": 1.0, "throbbing_headache": 3.2, "sore_throat": 1.2, "runny_nose": 1.4, "sneezing": 1.5,
    "loss_of_taste_smell": 3.8, "itchy_eyes": 2.2, "blurred_vision": 2.5, "numbness_one_side": 4.5,
    "slurred_speech": 4.5, "confusion": 3.0, "cough": 1.2, "cough_with_phlegm": 2.8, "cough_with_blood": 4.5,
    "shortness_of_breath": 3.2, "wheezing": 3.8, "chest_tightness": 3.0, "chest_pain": 3.8, "neck_radiating_pain": 4.5,
    "palpitations": 2.5, "rapid_heartbeat": 2.5, "swollen_legs_ankles": 3.5, "cold_hands_feet": 2.0,
    "nausea": 1.2, "vomiting": 2.0, "diarrhea": 2.4, "watery_diarrhea": 3.8, "stomach_pain": 1.8,
    "burning_stomach_pain": 3.0, "heartburn": 3.2, "acid_regurgitation": 3.5, "loss_of_appetite": 1.6,
    "increased_thirst": 3.5, "increased_hunger": 2.5, "frequent_urination": 2.8, "burning_urination": 3.8,
    "dark_urine": 3.2, "pale_stools": 3.8, "body_ache": 1.3, "joint_pain": 2.4, "joint_swelling": 3.5,
    "joint_stiffness": 3.2, "muscle_weakness": 2.0, "muscle_cramps": 2.4, "rash": 2.5, "itching": 2.0,
    "dry_skin": 2.0, "skin_redness": 2.0, "blisters": 3.5, "silvery_scales": 4.0, "acne_pimples": 3.8,
    "slow_healing_sores": 3.5, "yellow_skin_eyes": 4.5, "excessive_body_fat": 3.0, "cold_sensitivity": 3.0,
    "heat_sensitivity": 3.0, "tremors": 3.2
}

# Defining Hallmark Signatures for Differential Accuracy
DISEASE_SIGNATURE = {
    "Diabetes": {"increased_thirst", "frequent_urination", "slow_healing_sores"},
    "Hypertension": {"headache", "dizziness", "palpitations"},
    "Asthma": {"wheezing", "chest_tightness", "shortness_of_breath"},
    "Arthritis": {"joint_pain", "joint_stiffness", "joint_swelling"},
    "Cancer (Early Warning)": {"unexplained_weight_loss", "night_sweats", "fatigue"},
    "Obesity": {"excessive_body_fat"},
    "Dengue Fever": {"high_fever", "rash", "joint_pain"},
    "Malaria": {"chills", "sweating", "fever"},
    "Typhoid Fever": {"high_fever", "stomach_pain", "weakness"},
    "Tuberculosis": {"cough_with_blood", "night_sweats", "unexplained_weight_loss"},
    "Pneumonia": {"cough_with_phlegm", "high_fever", "chest_pain"},
    "COVID-19": {"loss_of_taste_smell", "shortness_of_breath", "cough"},
    "Influenza": {"high_fever", "body_ache", "chills"},
    "Common Cold": {"runny_nose", "sneezing", "sore_throat"},
    "Chickenpox": {"blisters", "rash", "itching"},
    "Gastroenteritis": {"watery_diarrhea", "vomiting", "stomach_pain"},
    "Cholera": {"watery_diarrhea", "muscle_cramps"},
    "Hepatitis": {"yellow_skin_eyes", "dark_urine", "pale_stools"},
    "Jaundice": {"yellow_skin_eyes", "dark_urine"},
    "Coronary Artery Disease": {"chest_pain", "neck_radiating_pain", "palpitations"},
    "Stroke (TIA Warning)": {"numbness_one_side", "slurred_speech"},
    "Chronic Kidney Disease": {"swollen_legs_ankles", "frequent_urination"},
    "Anemia": {"fatigue", "weakness", "cold_hands_feet"},
    "Hypothyroidism": {"unexplained_weight_gain", "cold_sensitivity"},
    "Hyperthyroidism": {"unexplained_weight_loss", "rapid_heartbeat", "tremors"},
    "Migraine": {"throbbing_headache", "nausea", "blurred_vision"},
    "GERD (Acid Reflux)": {"heartburn", "acid_regurgitation"},
    "Peptic Ulcer": {"burning_stomach_pain", "stomach_pain"},
    "Urinary Tract Infection": {"burning_urination", "frequent_urination"},
    "Allergic Rhinitis": {"sneezing", "runny_nose", "itchy_eyes"},
    "Food Allergy": {"itching", "rash", "vomiting"},
    "Eczema": {"dry_skin", "skin_redness", "itching"},
    "Psoriasis": {"silvery_scales", "skin_redness"},
    "Acne Vulgaris": {"acne_pimples"}
}

GENERIC_SYMPTOMS = {"fever", "fatigue", "headache", "body_ache", "nausea", "weakness"}

# Critical Red-Flag Clinical Rules
RED_FLAG_RULES = [
    ({"chest_pain", "neck_radiating_pain"}, "🚨 CRITICAL: Radiating chest/neck/arm pain detected — potential Acute Myocardial Infarction (Heart Attack). Seek emergency medical care immediately!"),
    ({"numbness_one_side", "slurred_speech"}, "🚨 CRITICAL: Unilateral facial/arm numbness and slurred speech detected — potential Stroke (F.A.S.T Protocol). Call emergency ambulance immediately!"),
    ({"cough_with_blood"}, "⚠️ HIGH ALERT: Hemoptysis (coughing blood) detected — indicative of active Tuberculosis or severe pulmonary condition. Immediate clinical screening required."),
    ({"watery_diarrhea", "muscle_cramps"}, "⚠️ HIGH ALERT: Profuse watery diarrhea with muscle cramps — potential Cholera or severe dehydration crisis. Begin immediate oral rehydration salts (ORS) and seek IV therapy."),
    ({"shortness_of_breath", "wheezing", "chest_tightness"}, "⚠️ HIGH ALERT: Severe acute respiratory distress / asthma attack. Use prescribed bronchodilator inhaler immediately; seek emergency room if unresponsive."),
    ({"rash", "high_fever", "joint_pain"}, "⚠️ URGENT: Classic Dengue triad detected. Avoid aspirin/ibuprofen (risk of hemorrhage) and get immediate platelet count testing."),
    ({"increased_thirst", "frequent_urination", "confusion"}, "⚠️ URGENT: Symptoms consistent with Diabetic Ketoacidosis (DKA) or hyperosmolar hyperglycemic state. Immediate medical attention needed.")
]

FOLLOW_UP_BY_SYMPTOM = {
    "fever": ["Do you also experience chills and shivering?", "Is there an associated skin rash or joint ache?", "Any cough, breathing trouble, or chest pain?"],
    "chest_pain": ["Does the pain radiate to your left arm, neck, or jaw?", "Do you feel short of breath or cold sweats?", "Does the pain worsen with exertion?"],
    "cough": ["Is the cough dry, producing phlegm, or coughing up blood?", "How long have you had this cough (more than 2 weeks)?", "Do you also experience night sweats or weight loss?"],
    "headache": ["Is the pain throbbing and on one side of the head?", "Are your speech, vision, or facial muscles affected?", "Do you feel nauseous or sensitive to light?"],
    "stomach_pain": ["Is it a burning pain between meals relieved by food?", "Do you experience acid regurgitation or heartburn?", "Is there accompanied watery diarrhea or vomiting?"],
    "joint_pain": ["Are your joints visibly swollen, warm, or stiff in the morning?", "Are multiple joints affected symmetrically?", "Do you have any skin rash or silvery scales?"]
}

INSUFFICIENT_SYMPTOM_LABELS = {
    "en": "General Febrile / Symptom Screening (Needs More Information)",
    "hi": "सामान्य लक्षण जांच (अधिक जानकारी आवश्यक)",
    "te": "ప్రాథమిక లక్షణాల పరిశీలన (మరింత సమాచారం అవసరం)"
}

IMAGE_INFO = {
    "Healthy Skin": {
        "description": "The skin demonstrates normal epidermal architecture, uniform pigmentation, and absence of inflammatory lesions, erythema, or scaling.",
        "advice": "Maintain standard daily hygiene, apply sun protection (SPF 30+), and drink plenty of water to support skin barrier integrity.",
        "urgency": "Low"
    },
    "Skin Rash": {
        "description": "Mild to moderate inflammatory erythema detected. Could arise from contact dermatitis, viral exanthema, or localized allergic response.",
        "advice": "1. Avoid scratching or scrubbing the affected skin.\n2. Apply cool compresses or calamine lotion to reduce inflammation.\n3. Wash with mild soap and consult a dermatologist if lesions spread.",
        "urgency": "Medium"
    },
    "Acne": {
        "description": "Pilosebaceous follicular inflammation visible with papules, comedones, and localized erythema (Acne Vulgaris).",
        "advice": "1. Cleanse twice daily using a gentle non-comedogenic foaming cleanser.\n2. Use topical salicylic acid or benzoyl peroxide treatments.\n3. Avoid popping pimples to prevent hyperpigmentation and scarring.",
        "urgency": "Low"
    },
    "Eczema": {
        "description": "Dry, scaly, and erythematous dermatitic patches visible, characteristic of Atopic Dermatitis or xerotic eczema.",
        "advice": "1. Apply thick ceramide-based moisturizers immediately after bathing.\n2. Avoid harsh fragrances, synthetic detergents, or wool fabrics.\n3. Inquire with a physician regarding low-potency topical corticosteroids for flare-ups.",
        "urgency": "Medium"
    }
}

# ==========================================
# Comprehensive 34-Disease Medical Knowledge Base
# ==========================================
DISEASE_INFO = {
    # 1. User Kaggle Notebook Diseases
    "Diabetes": {
        "en": {
            "prediction": "Diabetes Mellitus (Type 2 / Metabolic)",
            "description": "A chronic metabolic disease characterized by elevated blood glucose levels due to insulin deficiency or insulin resistance. If unmanaged, it can damage blood vessels, kidneys, and eyes.",
            "advice": "1. Schedule fasting blood glucose (FBS) and HbA1c testing immediately.\n2. Reduce refined sugars, white rice, and processed carbohydrates; eat high-fiber meals.\n3. Engage in at least 30 minutes of moderate cardiovascular exercise daily.\n4. Inspect feet daily for cuts or sores to prevent diabetic ulcers.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "मधुमेह / डायबिटीज (Diabetes Mellitus)",
            "description": "एक पुरानी चयापचय (मेटाबॉलिक) बीमारी जिसमें इंसुलिन की कमी या प्रतिरोध के कारण रक्त शर्करा (ब्लड शुगर) बढ़ जाती है। इसका समय पर इलाज न होने से किडनी, आंखों और दिल पर असर पड़ सकता है।",
            "advice": "1. तुरंत खाली पेट ब्लड शुगर (FBS) और HbA1c टेस्ट करवाएं।\n2. मीठा, सफेद चावल और तली-भुनी चीजों से परहेज करें; फाइबर युक्त आहार लें।\n3. रोजाना कम से कम 30 मिनट टहलें या व्यायाम करें।\n4. पैरों की नियमित जांच करें ताकि घाव होने से बचा जा सके।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "మధుమేహం / డయాబెటిస్ (Diabetes Mellitus)",
            "description": "రక్తంలో చక్కెర స్థాయిలు పెరిగే దీర్ఘకాలిక వ్యాధి. ఇన్సులిన్ లోపం లేదా అసమర్థత వల్ల వస్తుంది. నియంత్రించకపోతే కిడ్నీలు, కంటి చూపు మరియు గుండెపై ప్రభావం చూపుతుంది.",
            "advice": "1. వెంటనే ఖాళీ కడుపుతో షుగర్ టెస్ట్ (FBS) మరియు HbA1c పరీక్ష చేయించుకోండి.\n2. తీపి పదార్థాలు, తెల్ల అన్నం తగ్గించి పీచు పదార్థాలు (ఫైబర్) ఎక్కువగా తీసుకోండి.\n3. రోజూ కనీసం 30 నిమిషాలు వ్యాయామం లేదా వాకింగ్ చేయండి.\n4. పాదాలపై పుండ్లు రాకుండా జాగ్రత్త వహించండి.",
            "urgency": "Medium"
        }
    },
    "Hypertension": {
        "en": {
            "prediction": "Hypertension (High Blood Pressure)",
            "description": "A silent cardiovascular disorder where the long-term force of blood against artery walls is elevated (>=140/90 mmHg), increasing risks of heart attacks, stroke, and kidney failure.",
            "advice": "1. Measure blood pressure twice daily and maintain a log.\n2. Limit dietary sodium intake to under 2,000 mg (less than 1 teaspoon of salt per day).\n3. Practice daily relaxation techniques (deep breathing) to manage emotional stress.\n4. Take prescribed antihypertensives consistently without abrupt stopping.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "उच्च रक्तचाप / हाइपरटेंशन (Hypertension)",
            "description": "एक गंभीर स्थिति जिसमें धमनियों में रक्त का दबाव लगातार अधिक (140/90 से ऊपर) रहता है। इसे 'साइलेंट किलर' भी कहा जाता है क्योंकि यह बिना बड़े लक्षणों के दिल और दिमाग को नुकसान पहुंचाता है।",
            "advice": "1. रोजाना अपना बीपी चेक करें और रिकॉर्ड रखें।\n2. भोजन में नमक की मात्रा कम करें (दिन में 1 चम्मच से कम)।\n3. तनाव कम करने के लिए ध्यान और प्राणायाम करें।\n4. डॉक्टर द्वारा दी गई बीपी की दवाएं नियमित समय पर लें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "అధిక రక్తపోటు / హైపర్‌టెన్షన్ (High Blood Pressure)",
            "description": "రక్తనాళాలలో రక్తపోటు ఉండవలసిన స్థాయి (140/90) కంటే నిరంతరం ఎక్కువగా ఉండే పరిస్థితి. ఇది గుండెపోటు, పక్షవాతం మరియు మూత్రపిండాల వ్యాధులకు ప్రధాన కారణం.",
            "advice": "1. క్రమం తప్పకుండా బీపీని చెక్ చేసుకుని డైరీలో నమోదు చేయండి.\n2. ఆహారంలో ఉప్పును బాగా తగ్గించండి (రోజుకు ఒక చెంచా కంటే తక్కువ).\n3. ఒత్తిడిని తగ్గించుకోవడానికి ప్రాణాయామం లేదా ధ్యానం చేయండి.\n4. వైద్యులు సూచించిన బీపీ మందులను సమయానికి వాడండి.",
            "urgency": "Medium"
        }
    },
    "Asthma": {
        "en": {
            "prediction": "Bronchial Asthma (Chronic Airway Inflammation)",
            "description": "A chronic inflammatory disorder of the airways causing reversible airflow obstruction, bronchospasms, wheezing, breathlessness, and nocturnal coughing.",
            "advice": "1. Keep a prescribed quick-relief rescue inhaler (e.g., Salbutamol) accessible at all times.\n2. Avoid common triggers: cigarette smoke, dust mites, cold drafts, animal dander, and strong perfumes.\n3. Monitor peak expiratory flow rate (PEFR) during weather transitions.\n4. Seek immediate emergency care if breathing trouble does not improve within 10 minutes of inhaler use.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "दमा / अस्थमा (Bronchial Asthma)",
            "description": "श्वसन तंत्र की पुरानी बीमारी जिसमें वायुमार्ग में सूजन और संकुचन हो जाता है, जिससे सांस लेने में कठिनाई, सीटी जैसी आवाज (घरघराहट) और सीने में जकड़न होती है।",
            "advice": "1. अपना इन्हेलर (Inhaler) हमेशा अपने पास रखें।\n2. धूल, धुएं, परागकण और ठंडी हवा से खुद को बचाएं।\n3. रात में सोते समय सिर को थोड़ा ऊंचा रखें।\n4. यदि इन्हेलर लेने के बाद भी सांस लेने में आराम न मिले तो तुरंत अस्पताल जाएं।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "ఆస్తమా / ఉబ్బసం (Bronchial Asthma)",
            "description": "శ్వాసనాళాల వాపు వల్ల వచ్చే దీర్ఘకాలిక సమస్య. దీనివల్ల శ్వాస తీసుకోవడం కష్టమవుతుంది, పిల్లికూతలు (wheezing), దగ్గు మరియు ఛాతీలో పట్టేసినట్లు ఉంటుంది.",
            "advice": "1. మీ ఇన్హేలర్ (Inhaler) ను ఎల్లప్పుడూ అందుబాటులో ఉంచుకోండి.\n2. దుమ్ము, ధూళి, చల్లని గాలి మరియు పొగకు దూరంగా ఉండండి.\n3. గోరువెచ్చని నీటిని తాగడం మరియు ఆవిరి పట్టడం ద్వారా ఉపశమనం పొందవచ్చు.\n4. శ్వాస తీసుకోవడం బాగా కష్టమైతే వెంటనే అత్యవసర చికిత్స తీసుకోండి.",
            "urgency": "Medium"
        }
    },
    "Arthritis": {
        "en": {
            "prediction": "Arthritis (Osteoarthritis / Rheumatoid)",
            "description": "Inflammation of one or more joints causing chronic pain, early morning joint stiffness, swelling, and reduced range of physical motion.",
            "advice": "1. Perform gentle, low-impact joint movements (water aerobics, cycling, light walking).\n2. Apply warm compress to alleviate morning stiffness; use cold ice packs for acute swelling.\n3. Maintain a healthy body weight to reduce mechanical stress on knees and hips.\n4. Consult a rheumatologist for anti-inflammatory or disease-modifying therapies.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "गठिया / आर्थराइटिस (Arthritis)",
            "description": "जोड़ों में सूजन और दर्द की बीमारी, जिसमें जोड़ों में अकड़न, चलने-फिरने में तकलीफ और सूजन आ जाती है। यह ऑस्टियोआर्थराइटिस या रूमेटाइड हो सकता है।",
            "advice": "1. सुबह जोड़ों की अकड़न पर गर्म पानी की सिकाई करें; सूजन पर बर्फ लगाएं।\n2. हल्का व्यायाम जैसे तैराकी या आसान योग करें, जोड़ों पर भारी वजन न डालें।\n3. वजन नियंत्रित रखें ताकि घुटनों पर दबाव कम पड़े।\n4. डॉक्टर की सलाह से कैल्शियम, विटामिन डी और सूजन रोधी दवाएं लें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "కీళ్లవాతం / ఆర్థరైటిస్ (Arthritis)",
            "description": "కీళ్లలో వాపు, తీవ్రమైన నొప్పి మరియు కీళ్లు బిగుసుకుపోవడానికి కారణమయ్యే సమస్య. ముఖ్యంగా ఉదయం లేవగానే కీళ్లు కదలడం కష్టమవుతుంది.",
            "advice": "1. కీళ్ల నొప్పిపై వేడి కాపడం లేదా వాపు ఉన్నప్పుడు ఐస్ ప్యాక్ వాడండి.\n2. కీళ్లపై ఎక్కువ భారం పడకుండా తేలికపాటి నడక మరియు వ్యాయామాలు చేయండి.\n3. మోకాళ్లపై ఒత్తిడి తగ్గించడానికి బరువును నియంత్రణలో ఉంచుకోండి.\n4. వైద్యుల సూచనతో కాల్షియం మరియు విటమిన్ డి తీసుకోండి.",
            "urgency": "Medium"
        }
    },
    "Cancer (Early Warning)": {
        "en": {
            "prediction": "Potential Oncological Warning Signs (Clinical Evaluation Needed)",
            "description": "Cluster of constitutional symptoms including unexplained rapid weight loss (>10% body mass), persistent night sweats, chronic exhaustion, and non-healing lesions.",
            "advice": "1. Schedule a comprehensive diagnostic clinical workup (Complete Blood Count, imaging scans, and targeted biopsy).\n2. Do not ignore persistent symptoms lasting more than 3 consecutive weeks.\n3. Consult an oncologist or internal medicine specialist for definitive histology.\n4. Maintain nutrient-dense protein intake to prevent cachexia.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "कैंसर चेतावनी संकेत (Oncological Warning Signs)",
            "description": "बिना कारण तेजी से वजन घटना, रात में पसीना आना, लगातार कमजोरी और लंबे समय से न भरने वाले घाव जैसी स्थितियां गंभीर जांच की मांग करती हैं।",
            "advice": "1. बिना देरी किए विशेषज्ञ डॉक्टर से संपूर्ण शारीरिक जांच और बायोप्सी करवाएं।\n2. यदि लक्षण 3 सप्ताह से अधिक बने रहें तो उन्हें नजरअंदाज न करें।\n3. पौष्टिक और प्रोटीन युक्त भोजन लें ताकि शरीर की ताकत बनी रहे।",
            "urgency": "High"
        },
        "te": {
            "prediction": "క్యాన్సర్ హెచ్చరిక లక్షణాలు (Oncological Warning Signs)",
            "description": "కారణం లేకుండా వేగంగా బరువు తగ్గడం, రాత్రిపూట చెమటలు, తీవ్రమైన నీరసం మరియు మానని పుండ్లు క్యాన్సర్ ముందస్తు హెచ్చరికలు కావచ్చు.",
            "advice": "1. వెంటనే నిపుణులైన వైద్యులను సంప్రదించి రక్త పరీక్షలు మరియు స్కాన్లు చేయించుకోండి.\n2. 3 వారాలకు పైగా లక్షణాలు కొనసాగితే ఏమాత్రం నిర్లక్ష్యం చేయవద్దు.\n3. శరీరానికి శక్తినిచ్చే బలవర్ధకమైన ఆహారం తీసుకోండి.",
            "urgency": "High"
        }
    },
    "Obesity": {
        "en": {
            "prediction": "Clinical Obesity (High Metabolic Risk)",
            "description": "Excess accumulation of adipose body tissue (BMI >= 30), substantially elevating lifetime risk for diabetes, sleep apnea, hypertension, and degenerative joint disease.",
            "advice": "1. Work with a registered clinical dietitian for a calorie-deficit, whole-foods nutrition plan.\n2. Target 150–300 minutes of moderate aerobic activity weekly.\n3. Screen for secondary metabolic markers (fasting lipids, thyroid profile, insulin resistance).\n4. Ensure 7–8 hours of restorative sleep to regulate hunger hormones (leptin and ghrelin).",
            "urgency": "Low"
        },
        "hi": {
            "prediction": "मोटापा / ओबेसिटी (Clinical Obesity)",
            "description": "शरीर में अत्यधिक चर्बी का जमाव (बीएमआई 30 से ऊपर)। यह स्थिति हृदय रोग, मधुमेह, फैटी लिवर और जोड़ों के दर्द का खतरा कई गुना बढ़ा देती है।",
            "advice": "1. जंक फूड, कोल्ड ड्रिंक्स और चीनी का सेवन पूरी तरह बंद करें।\n2. सप्ताह में कम से कम 150 मिनट तेज टहलें या कार्डियो व्यायाम करें।\n3. थायराइड और लिपिड प्रोफाइल की जांच करवाएं।\n4. समय पर भोजन करें और रात को 7-8 घंटे की पूरी नींद लें।",
            "urgency": "Low"
        },
        "te": {
            "prediction": "స్థూలకాయం / ఊబకాయం (Clinical Obesity)",
            "description": "శరీరంలో కొవ్వు అధికంగా పేరుకుపోవడం (BMI 30 కన్నా ఎక్కువ). దీనివల్ల మధుమేహం, గుండె జబ్బులు, కీళ్ల నొప్పులు మరియు శ్వాస సమస్యలు వచ్చే ప్రమాదం ఉంది.",
            "advice": "1. నూనె పదార్థాలు, తీపి మరియు ప్రాసెస్ చేసిన ఆహారాలను పూర్తిగా తగ్గించండి.\n2. వారానికి కనీసం 150 నిమిషాలు వేగంగా నడవండి లేదా వ్యాయామం చేయండి.\n3. రక్తంలో కొలెస్ట్రాల్ మరియు థైరాయిడ్ పరీక్షలు చేయించుకోండి.\n4. తగినంత నిద్ర మరియు సమయానికి ఆహారం తీసుకోవడం అలవాటు చేసుకోండి.",
            "urgency": "Low"
        }
    },

    # 2. Infectious & Tropical Epidemics
    "Dengue Fever": {
        "en": {
            "prediction": "Dengue Fever (Arboviral Infection)",
            "description": "A mosquito-borne viral illness caused by Dengue virus transmitted by Aedes mosquitoes, presenting with sudden high fever, retro-orbital eye pain, severe arthralgia, and petechial rash.",
            "advice": "1. CRITICAL: Avoid Aspirin, Ibuprofen, and NSAIDs as they increase hemorrhagic bleeding risk. Use only Paracetamol for fever.\n2. Drink 3–4 liters of fluids daily (ORS, tender coconut water, fruit juice) to maintain hydration.\n3. Monitor platelet count daily; watch for warning signs: gum bleeding, persistent abdominal pain, or black stools.\n4. Rest completely under mosquito nets to prevent vector transmission.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "डेंगू बुखार (Dengue Fever)",
            "description": "एडीज मच्छर के काटने से फैलने वाला वायरल संक्रमण। इसमें अचानक तेज बुखार, आंखों के पीछे दर्द, जोड़ों और मांसपेशियों में गंभीर दर्द और शरीर पर लाल चकत्ते होते हैं।",
            "advice": "1. अत्यधिक महत्वपूर्ण: एस्पिरिन या आईबुप्रोफेन जैसी दवाएं बिल्कुल न लें क्योंकि इनसे ब्लीडिंग का खतरा होता है। केवल पैरासिटामोल लें।\n2. ओआरएस, नारियल पानी और तरल पदार्थ प्रचुर मात्रा में पिएं।\n3. प्लेटलेट काउंट की रोजाना जांच कराएं।\n4. मसूड़ों से खून आना या पेट में तेज दर्द होने पर तुरंत अस्पताल जाएं।",
            "urgency": "High"
        },
        "te": {
            "prediction": "డెంగ్యూ జ్వరం (Dengue Fever)",
            "description": "ఎడిస్ దోమ ద్వారా వ్యాపించే వైరల్ వ్యాధి. ఆకస్మిక తీవ్ర జ్వరం, కళ్ల వెనుక నొప్పి, తీవ్ర కీళ్ల నొప్పులు మరియు చర్మంపై దద్దుర్లు రావడం దీని ప్రధాన లక్షణాలు.",
            "advice": "1. అత్యంత ముఖ్యం: ఆస్పిరిన్, ఐబుప్రోఫెన్ మందులు వాడవద్దు, ఇవి రక్తస్రావానికి దారితీస్తాయి. కేవలం పారాసిటమాల్ మాత్రమే వాడండి.\n2. డీహైడ్రేషన్ రాకుండా కొబ్బరి నీళ్లు, ఓఆర్ఎస్, పండ్ల రసాలు ఎక్కువగా తాగండి.\n3. రోజూ రక్తంలో ప్లేట్‌లెట్స్ సంఖ్యను పరీక్షించండి.\n4. రక్తస్రావం లేదా తీవ్ర కడుపు నొప్పి ఉంటే వెంటనే ఆసుపత్రిలో చేరండి.",
            "urgency": "High"
        }
    },
    "Malaria": {
        "en": {
            "prediction": "Malaria (Plasmodium Infection)",
            "description": "A life-threatening protozoan infection transmitted through Anopheles mosquito bites, marked by paroxysms of shaking chills, spiking fever, and profuse drenching sweats.",
            "advice": "1. Get a peripheral blood smear or Rapid Diagnostic Test (RDT) immediately.\n2. Complete a full course of prescribed antimalarial medication (such as Artemisinin-based therapy).\n3. Stay well hydrated with electrolytes to counteract fluid loss from severe sweating.\n4. Sleep under insecticide-treated bed nets and clear stagnant puddles.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "मलेरिया (Malaria Parasite Infection)",
            "description": "मादा एनोफिलीज मच्छर के काटने से होने वाला परजीवी संक्रमण। इसमें कंपकंपी के साथ तेज बुखार आता है और फिर पसीना आकर बुखार उतरता है।",
            "advice": "1. तुरंत मलेरिया ब्लड टेस्ट (RDT या स्लाइड टेस्ट) करवाएं।\n2. डॉक्टर द्वारा दी गई एंटीमलेरियल दवाओं का पूरा कोर्स बिना छोड़े पूरा करें।\n3. पसीने से पानी की कमी न हो, इसके लिए पर्याप्त पानी और ओआरएस पिएं।\n4. मच्छरदानी का प्रयोग करें और घर के आसपास रुका पानी साफ करें।",
            "urgency": "High"
        },
        "te": {
            "prediction": "మలేరియా (Malaria Parasitic Infection)",
            "description": "ఎనాఫిలిస్ దోమ కాటు వల్ల వ్యాపించే పరాన్నజీవి సంక్రమణ. తీవ్రమైన చలి, వణుకుతో కూడిన జ్వరం మరియు ఆ తర్వాత విపరీతంగా చెమటలు పట్టడం దీని లక్షణాలు.",
            "advice": "1. వెంటనే రక్త పరీక్ష (మలేరియా స్మియర్ లేదా RDT) చేయించుకోండి.\n2. వైద్యులు సూచించిన మలేరియా మందుల కోర్సును పూర్తిగా వాడండి.\n3. పండ్ల రసాలు మరియు ఓఆర్ఎస్ ద్రావణం తాగి శరీరంలో నీటి స్థాయిని కాపాడుకోండి.\n4. దోమతెరలు వాడండి, ఇంటి పరిసరాలలో నీరు నిల్వ ఉండకుండా చూడండి.",
            "urgency": "High"
        }
    },
    "Typhoid Fever": {
        "en": {
            "prediction": "Typhoid Fever (Enteric Salmonella)",
            "description": "A systemic bacterial infection caused by Salmonella typhi, spread through contaminated water and food. Features step-ladder progressive high fever, abdominal pain, and extreme malaise.",
            "advice": "1. Undergo Widal testing or Blood Culture to confirm bacterial diagnosis.\n2. Strictly finish the entire course of prescribed antibiotics.\n3. Consume only boiled water, freshly prepared home-cooked light foods (khichdi, broths).\n4. Avoid street foods, raw salads, and unpeeled fruits until complete recovery.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "टाइफाइड बुखार (Typhoid / Enteric Fever)",
            "description": "साल्मोनेला टाइफी बैक्टीरिया से दूषित पानी और भोजन के जरिए फैलने वाला गंभीर संक्रमण। इसमें लगातार तेज बुखार, पेट दर्द, सिरदर्द और अत्यधिक कमजोरी होती है।",
            "advice": "1. विडाल टेस्ट (Widal Test) या ब्लड कल्चर करवाएं।\n2. एंटीबायोटिक दवाओं का पूरा कोर्स डॉक्टर की सलाह से अनिवार्य रूप से पूरा करें।\n3. केवल उबला हुआ पानी और हल्का, ताजा बना खाना (जैसे खिचड़ी, दलिया) खाएं।\n4. बाहर का खुला खाना, सड़क किनारे के पेय और कटे फल बिल्कुल न खाएं।",
            "urgency": "High"
        },
        "te": {
            "prediction": "టైఫాయిడ్ జ్వరం (Typhoid / Enteric Fever)",
            "description": "కలుషితమైన ఆహారం మరియు నీటి ద్వారా వ్యాపించే బ్యాక్టీరియల్ సంక్రమణ. క్రమంగా పెరిగే తీవ్ర జ్వరం, కడుపు నొప్పి, తలనొప్పి మరియు విపరీతమైన నీరసం కలిగిస్తుంది.",
            "advice": "1. టైఫాయిడ్ నిర్ధారణ కొరకు విడాల్ (Widal) లేదా బ్లడ్ కల్చర్ పరీక్ష చేయించుకోండి.\n2. డాక్టర్ ఇచ్చిన యాంటీబయాటిక్స్ కోర్సును మధ్యలో ఆపకుండా పూర్తిగా వాడండి.\n3. కేవలం కాచి చల్లార్చిన నీటిని మరియు తేలికగా జీర్ణమయ్యే గంజి, కిచిడీ తినండి.\n4. వీధి తినుబండారాలు, నిల్వ ఉంచిన పదార్థాలు తినవద్దు.",
            "urgency": "High"
        }
    },
    "Tuberculosis": {
        "en": {
            "prediction": "Tuberculosis (Pulmonary TB)",
            "description": "A contagious mycobacterial infection primarily attacking the lungs. Hallmark symptoms include chronic cough lasting >2 weeks, hemoptysis (coughing blood), night sweats, and significant weight loss.",
            "advice": "1. Report immediately to a government DOTS clinic or pulmonologist for Sputum AFB testing and chest X-ray.\n2. Adhere strictly to the 6-month Directly Observed Therapy (DOTS) antibiotic regimen.\n3. Wear a well-fitted mask around family members to prevent aerosol transmission.\n4. Eat a high-calorie, protein-rich diet to rebuild pulmonary tissue.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "तपेदिक / टीबी (Pulmonary Tuberculosis)",
            "description": "माइकोबैक्टीरियम ट्यूबरकुलोसिस बैक्टीरिया से होने वाला संक्रामक फेफड़ों का रोग। 2 सप्ताह से अधिक खांसी, खांसी में खून, रात में पसीना और वजन घटना इसके मुख्य लक्षण हैं।",
            "advice": "1. तुरंत बलगम की जांच (Sputum Test) और छाती का एक्स-रे करवाएं।\n2. सरकार द्वारा दी जाने वाली डॉट्स (DOTS) दवाएं 6 महीने तक बिना नागा नियमित रूप से लें।\n3. खांसते समय मुंह पर रुमाल रखें और हवादार कमरे में रहें।\n4. पोषण के लिए दालें, अंडे और दूध का सेवन बढ़ाएं।",
            "urgency": "High"
        },
        "te": {
            "prediction": "క్షయ వ్యాధి / టి.బి (Tuberculosis - Pulmonary)",
            "description": "మైకోబ్యాక్టీరియం వల్ల ఊపిరితిత్తులకు సోకే అంటువ్యాధి. రెండు వారాలకు పైగా తగ్గని దగ్గు, దగ్గులో రక్తం పడటం, రాత్రిపూట చెమటలు మరియు విపరీతంగా బరువు తగ్గడం దీని సంకేతాలు.",
            "advice": "1. వెంటనే దగ్గరలోని ప్రభుత్వ డాట్స్ (DOTS) కేంద్రంలో కళ్లె పరీక్ష మరియు ఛాతీ ఎక్స్-రే చేయించుకోండి.\n2. వైద్యులు సూచించిన టి.బి మందులను 6 నెలల పాటు క్రమం తప్పకుండా వాడండి.\n3. ఇతరులకు సోకకుండా మాస్క్ ధరించండి మరియు గాలి వెలుతురు ఉన్న గదిలో ఉండండి.\n4. బలవర్ధకమైన పప్పుధాన్యాలు, పాలు మరియు గుడ్లు ఆహారంగా తీసుకోండి.",
            "urgency": "High"
        }
    },
    "Pneumonia": {
        "en": {
            "prediction": "Pneumonia (Acute Lower Respiratory Infection)",
            "description": "Inflammation and fluid consolidation of the lung alveoli caused by bacteria or viruses, leading to severe productive cough with purulent phlegm, high fever, chills, and sharp pleuritic chest pain.",
            "advice": "1. Get an urgent chest X-ray and pulse oximetry evaluation.\n2. Monitor oxygen levels (SpO2); if it drops below 94%, seek emergency hospital admission.\n3. Take prescribed antibiotics or antivirals exactly on schedule.\n4. Practice incentive spirometry and take deep breathing breaks.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "निमोनिया (Pneumonia Lung Infection)",
            "description": "फेफड़ों की वायु थैलियों (अल्वेओली) में मवाद या तरल भरने वाला गंभीर संक्रमण। इसमें बलगम वाली खांसी, तेज बुखार, कंपकंपी और सांस लेते समय छाती में तेज दर्द होता है।",
            "advice": "1. तुरंत छाती का एक्स-रे करवाएं और पल्स ऑक्सीमीटर से ऑक्सीजन मापें।\n2. यदि ऑक्सीजन 94% से नीचे जाए तो तुरंत अस्पताल में भर्ती हों।\n3. डॉक्टर द्वारा दी गई दवाएं समय पर लें और पूरा आराम करें।\n4. गर्म तरल पदार्थ पिएं और भाप लें।",
            "urgency": "High"
        },
        "te": {
            "prediction": "న్యుమోనియా (Pneumonia - Acute Lung Infection)",
            "description": "ఊపిరితిత్తులలో చీము లేదా ద్రవాలు చేరడం వల్ల వచ్చే తీవ్రమైన ఇన్ఫెక్షన్. తెమడతో కూడిన దగ్గు, తీవ్ర జ్వరం, చలి మరియు శ్వాస తీసుకునేటప్పుడు ఛాతీ నొప్పి కలిగిస్తుంది.",
            "advice": "1. వెంటనే ఛాతీ ఎక్స్-రే చేయించుకోండి మరియు పల్స్ ఆక్సిమీటర్ తో ఆక్సిజన్ స్థాయిలను పరిశీలించండి.\n2. ఆక్సిజన్ లెవెల్ 94% కంటే తగ్గితే వెంటనే ఆసుపత్రికి వెళ్లండి.\n3. వైద్యులు ఇచ్చిన యాంటీబయాటిక్స్ మందులను సమయానికి వాడండి.\n4. విశ్రాంతి తీసుకోండి మరియు వేడి నీటి ఆవిరి పట్టండి.",
            "urgency": "High"
        }
    },
    "COVID-19": {
        "en": {
            "prediction": "COVID-19 (SARS-CoV-2 Respiratory Infection)",
            "description": "An infectious coronavirus illness causing symptoms from mild upper airway congestion to pneumonia, characteristically involving fever, dry cough, anosmia (loss of smell), and dyspnea.",
            "advice": "1. Isolate in a well-ventilated room for at least 7 days.\n2. Monitor pulse oximeter readings every 4 hours (alert doctor if SpO2 < 94%).\n3. Maintain hydration, take Vitamin C and Zinc supplements as advised.\n4. Wear an N95 mask if interacting with caregivers.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "कोविड-19 (COVID-19 Corona Infection)",
            "description": "सार्स-सीओवी-2 वायरस से होने वाला संक्रामक रोग। बुखार, सूखी खांसी, अत्यधिक थकान, स्वाद और गंध का चले जाना और सांस लेने में तकलीफ इसके प्रमुख लक्षण हैं।",
            "advice": "1. कम से कम 7 दिनों के लिए खुद को हवादार कमरे में आइसोलेट करें।\n2. हर 4 घंटे में ऑक्सीमीटर से ऑक्सीजन (SpO2) जांचें।\n3. पर्याप्त पानी पिएं, पौष्टिक भोजन लें और डॉक्टर की सलाह अनुसार दवाएं लें।\n4. अन्य लोगों के संपर्क में आने पर N95 मास्क पहनें।",
            "urgency": "High"
        },
        "te": {
            "prediction": "కోవిడ్-19 (COVID-19 Corona Virus)",
            "description": "కరోనా వైరస్ వల్ల ఊపిరితిత్తులు మరియు శ్వాసకోశ వ్యవస్థకు సోకే అంటువ్యాధి. జ్వరం, పొడి దగ్గు, అలసట, రుచి వాసన కోల్పోవడం మరియు శ్వాసలో ఇబ్బంది కలిగిస్తుంది.",
            "advice": "1. కనీసం 7 రోజుల పాటు ప్రత్యేక గదిలో ఐసోలేషన్ లో ఉండండి.\n2. ప్రతి 4 గంటలకు ఆక్సిమీటర్ తో ఆక్సిజన్ లెవెల్స్ చూసుకోండి (94% కన్నా తగ్గితే జాగ్రత్త).\n3. వేడి నీరు, పౌష్టికాహారం తీసుకోండి మరియు వైద్యుల సలహా పాటించండి.\n4. ఇతరులతో మాట్లాడేటప్పుడు N95 మాస్క్ తప్పనిసరిగా ధరించండి.",
            "urgency": "High"
        }
    },
    "Influenza": {
        "en": {
            "prediction": "Influenza (Seasonal Flu Virus)",
            "description": "An acute respiratory viral infection causing rapid-onset high fever, generalized myalgia (severe body aches), shivering chills, headache, and persistent dry cough.",
            "advice": "1. Rest extensively in bed to permit cellular immune recovery.\n2. Drink warm liquids: herbal tea, lemon water, and clear soups.\n3. Take paracetamol for fever and body ache relief.\n4. Get an annual influenza vaccine to protect against mutating strains.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "इन्फ्लूएंजा / मौसमी फ्लू (Seasonal Flu)",
            "description": "इन्फ्लूएंजा वायरस से होने वाला श्वसन संक्रमण। इसमें अचानक तेज बुखार, गंभीर बदन दर्द, ठंड लगना, सिरदर्द और गले में खराश होती है।",
            "advice": "1. बिस्तर पर पूरा आराम करें और भारी काम से बचें।\n2. गर्म पानी, काढ़ा, सूप और हर्बल चाय पिएं।\n3. बदन दर्द और बुखार के लिए डॉक्टर की सलाह से पैरासिटामोल लें।\n4. हर साल फ्लू का टीका (Flu Vaccine) लगवाएं।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "ఇన్ఫ్లుయెంజా / ఫ్లూ జ్వరం (Influenza Flu)",
            "description": "వైరస్ వల్ల వేగంగా వ్యాపించే శ్వాసకోశ ఇన్ఫెక్షన్. తీవ్రమైన జ్వరం, ఒళ్ళు నొప్పులు, చలి, తలనొప్పి మరియు గొంతు నొప్పి దీని ముఖ్య లక్షణాలు.",
            "advice": "1. శరీరం కోలుకోవడానికి మంచి విశ్రాంతి అవసరం.\n2. గోరువెచ్చని నీరు, సూప్ మరియు పండ్ల రసాలు ఎక్కువగా తీసుకోండి.\n3. జ్వరం మరియు నొప్పుల ఉపశమనానికి పారాసిటమాల్ వాడండి.\n4. ఏటా ఫ్లూ వ్యాక్సిన్ తీసుకోవడం ద్వారా రక్షణ పొందవచ్చు.",
            "urgency": "Medium"
        }
    },
    "Common Cold": {
        "en": {
            "prediction": "Common Cold (Viral Nasopharyngitis)",
            "description": "A mild viral infection of the upper respiratory tract primarily caused by rhinoviruses, causing sneezing, nasal congestion, runny nose, and scratchy sore throat.",
            "advice": "1. Use saline nasal spray or steam inhalation to clear congested sinuses.\n2. Gargle with warm salt water three times daily for throat soothing.\n3. Stay comfortably hydrated and get sound nightly sleep.\n4. Antibiotics are completely ineffective against common cold viruses.",
            "urgency": "Low"
        },
        "hi": {
            "prediction": "सामान्य सर्दी-जुकाम (Common Cold)",
            "description": "राइनोवायरस के कारण ऊपरी श्वास नलिकाओं का हल्का वायरल संक्रमण। इसमें छींकें आना, नाक बहना, नाक बंद होना और गले में हल्की खराश होती है।",
            "advice": "1. बंद नाक खोलने के लिए गर्म पानी की भाप लें।\n2. गुनगुने नमक के पानी से दिन में 2-3 बार गरारे करें।\n3. अदरक वाली चाय, सूप और गर्म पानी पिएं।\n4. ध्यान रहे: जुकाम पर एंटीबायोटिक्स असर नहीं करतीं, केवल आराम करें।",
            "urgency": "Low"
        },
        "te": {
            "prediction": "సాధారణ జలుబు (Common Cold)",
            "description": "వైరస్ వల్ల ముక్కు మరియు గొంతుకు వచ్చే తేలికపాటి ఇన్ఫెక్షన్. తుమ్ములు, ముక్కు కారడం, గొంతు గరగర మరియు స్వల్ప తలనొప్పి ఉంటాయి.",
            "advice": "1. ముక్కు దిబ్బడ తగ్గడానికి వేడి నీటి ఆవిరి పట్టండి.\n2. గోరువెచ్చని ఉప్పు నీటితో రోజుకు మూడు సార్లు పుక్కిలించండి.\n3. అల్లం టీ, వేడి సూప్‌లు తాగి విశ్రాంతి తీసుకోండి.\n4. జలుబుకు యాంటీబయాటిక్స్ అవసరం లేదు, సహజంగానే తగ్గుతుంది.",
            "urgency": "Low"
        }
    },
    "Chickenpox": {
        "en": {
            "prediction": "Chickenpox (Varicella-Zoster Virus)",
            "description": "A highly contagious viral infection characterized by an intensely itchy vesicular rash presenting as fluid-filled blisters over red macules, accompanied by fever and malaise.",
            "advice": "1. Apply calamine lotion to blisters to soothe itching; DO NOT scratch (prevents secondary bacterial infection and scarring).\n2. Take cool or lukewarm oatmeal baths to calm skin irritation.\n3. Wear loose, smooth cotton clothing.\n4. Isolate at home until all blisters have fully crusted over.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "चेचक / छोटी माता (Chickenpox)",
            "description": "वेरिसेला-जोस्टर वायरस से फैलने वाला अत्यधिक संक्रामक रोग। इसमें तेज खुजली वाले पानी भरे दाने (फफोले), बुखार और भूख न लगना जैसे लक्षण होते हैं।",
            "advice": "1. दानों को बिल्कुल न खुजलाएं ताकि निशान न पड़ें; कैलामाइन लोशन लगाएं।\n2. ढीले और साफ सूती कपड़े पहनें।\n3. जब तक सारे फफोले सूखकर पपड़ी न बन जाएं, तब तक घर पर अलग रहें।\n4. नीम के पत्तों के उबले पानी से स्नान करें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "మశూచి / ఆటలమ్మ (Chickenpox)",
            "description": "వారిసెల్లా జోస్టర్ వైరస్ వల్ల వచ్చే అత్యంత వేగంగా వ్యాపించే చర్మ వ్యాధి. శరీరమంతా నీటి పొక్కులు (బొబ్బలు), దురద, జ్వరం మరియు నీరసం కలిగిస్తుంది.",
            "advice": "1. బొబ్బలను గోళ్లతో గిల్లవద్దు; దురద తగ్గడానికి కాలమైన్ లోషన్ రాయండి.\n2. వదులైన కాటన్ దుస్తులు మాత్రమే ధరించండి.\n3. పొక్కులన్నీ ఎండిపోయి రాలిపోయే వరకు ఇతరులకు దూరంగా ఉండండి.\n4. వేపాకు వేసి మరిగించిన చల్లని నీటితో స్నానం చేయడం మంచిది.",
            "urgency": "Medium"
        }
    },
    "Gastroenteritis": {
        "en": {
            "prediction": "Acute Gastroenteritis (Stomach Flu)",
            "description": "Inflammation of the stomach and intestinal mucosa caused by viral or bacterial pathogens, resulting in watery diarrhea, nausea, vomiting, and abdominal cramping.",
            "advice": "1. Sip Oral Rehydration Salts (ORS) solution continuously to replace lost fluid and electrolytes.\n2. Follow the BRAT diet (Bananas, Rice, Applesauce, Toast) once vomiting subsides.\n3. Avoid milk, dairy products, spicy foods, caffeine, and alcohol.\n4. Seek urgent IV fluids if unable to keep down liquids for >12 hours.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "गैस्ट्रोएंटेराइटिस / पेट का संक्रमण (Stomach Flu)",
            "description": "पेट और आंतों की परत में सूजन, जो दूषित भोजन या वायरस से होती है। इससे उल्टी, दस्त, पेट में मरोड़ और कमजोरी होती है।",
            "advice": "1. डिहाइड्रेशन से बचने के लिए ओआरएस (ORS) का घोल घूंट-घूंट करके लगातार पिएं।\n2. खिचड़ी, केला, छाछ और हल्का खाना ही लें।\n3. दूध, तली-भुनी चीजें, चाय और मिर्च-मसालों से पूरी तरह परहेज करें।\n4. यदि लगातार उल्टी हो रही हो तो डॉक्टर से ड्रिप लगवाएं।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "గ్యాస్ట్రోఎంటరైటిస్ / కడుపు ఇన్ఫెక్షన్ (Stomach Flu)",
            "description": "కలుషిత ఆహారం లేదా వైరస్ వల్ల జీర్ణవ్యవస్థలో వాపు రావడం. నీళ్ల విరేచనాలు, వాంతులు, కడుపులో తిప్పడం మరియు తీవ్ర కడుపు నొప్పి కలిగిస్తుంది.",
            "advice": "1. శరీరంలో నీటి శాతం తగ్గకుండా ఓఆర్ఎస్ (ORS) ద్రావణం తరచుగా తాగండి.\n2. వాంతులు తగ్గిన తర్వాత కిచిడీ, అరటిపండు, మజ్జిగ వంటివి మాత్రమే తినండి.\n3. పాలు, కారం మరియు వేపుడు పదార్థాలకు దూరంగా ఉండండి.\n4. 12 గంటల కంటే ఎక్కువ సమయం ఏమీ తాగలేకపోతే వెంటనే ఆసుపత్రికి వెళ్లండి.",
            "urgency": "Medium"
        }
    },
    "Cholera": {
        "en": {
            "prediction": "Cholera (Vibrio cholerae Secretory Diarrhea)",
            "description": "A severe, potentially fatal bacterial infection of the small intestine characterized by voluminous, painless watery 'rice-water' stools, leading to rapid catastrophic dehydration and shock.",
            "advice": "1. IMMEDIATE EMERGENCY: Administer massive oral rehydration salts (ORS) immediately and rush to a hospital for IV Ringer's Lactate.\n2. Do not wait for medical transport before starting oral fluid replacement.\n3. Antibiotics (such as Doxycycline or Azithromycin) shorten illness duration under medical prescription.\n4. Strictly disinfect drinking water through rolling boil or chlorine treatment.",
            "urgency": "Critical"
        },
        "hi": {
            "prediction": "हैजा / कॉलरा (Cholera Secretory Infection)",
            "description": "विब्रियो कॉलरी बैक्टीरिया से होने वाला घातक आंतों का संक्रमण। इसमें चावल के मांड जैसा सफेद पानी वाला दस्त और लगातार उल्टी होती है, जिससे कुछ ही घंटों में जानलेवा डिहाइड्रेशन हो सकता है।",
            "advice": "1. आपातकालीन स्थिति: तुरंत ओआरएस (ORS) का पानी पिलाना शुरू करें और बिना देरी किए नजदीकी अस्पताल ले जाएं।\n2. डॉक्टर से तुरंत नस द्वारा ड्रिप (IV Fluids) लगवाएं।\n3. पानी को अच्छी तरह उबालकर ही पिएं।",
            "urgency": "Critical"
        },
        "te": {
            "prediction": "కలరా / తీవ్ర విరేచనాలు (Cholera Severe Dehydration)",
            "description": "విబ్రియో కలరే బ్యాక్టీరియా వల్ల వచ్చే అత్యంత ప్రమాదకరమైన వ్యాధి. బియ్యపు కడుగు నీళ్ల వంటి విరేచనాలు మరియు తీవ్ర వాంతులు అవ్వడం వల్ల కొద్ది గంటల్లోనే తీవ్రమైన డీహైడ్రేషన్ మరియు ప్రాణాపాయం కలగవచ్చు.",
            "advice": "1. అత్యవసర పరిస్థితి: వెంటనే ఓఆర్ఎస్ ద్రావణం తాగిస్తూ ఆసుపత్రికి తరలించండి.\n2. వైద్యుల పర్యవేక్షణలో సెలైన్ (IV Fluids) ఎక్కించడం అత్యంత ముఖ్యం.\n3. తాగే నీటిని బాగా మరిగించి మాత్రమే వాడండి.",
            "urgency": "Critical"
        }
    },
    "Hepatitis": {
        "en": {
            "prediction": "Viral Hepatitis (Liver Inflammation - Hep A/B/C)",
            "description": "Inflammation of hepatic tissues caused by viral infection, presenting with jaundice (yellow sclera and skin), dark tea-colored urine, acholic pale stools, and right upper quadrant abdominal tenderness.",
            "advice": "1. Undergo Liver Function Tests (LFTs - Bilirubin, SGOT, SGPT) and viral serology.\n2. Strictly avoid all alcohol, hepatotoxic herbal compounds, and unnecessary medications.\n3. Consume easily digestible carbohydrates and maintain adequate caloric hydration.\n4. Screen household contacts and administer Hepatitis A and B immunizations.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "वायरल हेपेटाइटिस / यकृत शोथ (Viral Hepatitis)",
            "description": "लिवर में वायरस के कारण होने वाली गंभीर सूजन। इसमें त्वचा और आंखों का पीला पड़ना (पीलिया), गहरा पेशाब, हल्के रंग का मल और पेट के ऊपरी हिस्से में दर्द होता है।",
            "advice": "1. तुरंत लिवर फंक्शन टेस्ट (LFT) और वायरल हेपेटाइटिस टेस्ट करवाएं।\n2. शराब और भारी तले-भुने भोजन से पूरी तरह दूर रहें।\n3. गन्ने का रस, नारियल पानी और सुपाच्य कार्बोहाइड्रेट युक्त भोजन लें।\n4. घर के बाकी सदस्यों को हेपेटाइटिस का टीका लगवाएं।",
            "urgency": "High"
        },
        "te": {
            "prediction": "హెపటైటిస్ / కాలేయ వ్యాధి (Viral Hepatitis)",
            "description": "వైరస్ సంక్రమణ వల్ల కాలేయానికి సోకే తీవ్రమైన వాపు. కళ్లు మరియు చర్మం పసుపు రంగులోకి మారడం (కామెర్లు), ముదురు రంగు మూత్రం మరియు కడుపు కుడి వైపు నొప్పి ఉంటాయి.",
            "advice": "1. వెంటనే లివర్ ఫంక్షన్ టెస్ట్ (LFT) మరియు హెపటైటిస్ స్క్రీనింగ్ చేయించుకోండి.\n2. ఆల్కహాల్ మరియు నూనె పదార్థాలను పూర్తిగా మానెయ్యండి.\n3. చెరకు రసం, కొబ్బరి నీళ్లు మరియు తేలికపాటి ఆహారం తీసుకోండి.\n4. కుటుంబ సభ్యులకు హెపటైటిస్ టీకాలు వేయించండి.",
            "urgency": "High"
        }
    },
    "Jaundice": {
        "en": {
            "prediction": "Clinical Jaundice (Hyperbilirubinemia)",
            "description": "Yellowish pigmentation of the skin, mucous membranes, and conjunctival sclera caused by high levels of circulating bilirubin in blood, reflecting hepatic or biliary tract impairment.",
            "advice": "1. Order comprehensive liver profile and abdominal ultrasound to rule out gallstones or biliary obstruction.\n2. Rest adequately and avoid physical exhaustion.\n3. Maintain zero alcohol and low-fat nutrient intake.\n4. Promptly evaluate for underlying hemolytic, infectious, or obstructive causes.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "पीलिया / जॉन्डिस (Clinical Jaundice)",
            "description": "खून में बिलीरुबिन का स्तर बढ़ने से त्वचा और आंखों का सफेद भाग पीला पड़ जाता है। यह लिवर या पित्त की नली में खराबी का मुख्य संकेत है।",
            "advice": "1. लिवर की जांच (LFT) और पेट का अल्ट्रासाउंड करवाएं।\n2. तेल, घी, मसालेदार भोजन और शराब का सेवन बिल्कुल न करें।\n3. ग्लूकोज, नारियल पानी और ताजा फल खाएं।\n4. शारीरिक श्रम से बचें और भरपूर आराम करें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "కామెర్లు / జాండిస్ (Jaundice Hyperbilirubinemia)",
            "description": "రక్తంలో బిలిరుబిన్ స్థాయి పెరగడం వల్ల కళ్లు, చర్మం మరియు మూత్రం పసుపు రంగులోకి మారతాయి. ఇది కాలేయం లేదా పిత్తాశయ సమస్యలను సూచిస్తుంది.",
            "advice": "1. కాలేయ పరీక్షలు (LFT) మరియు అల్ట్రాసౌండ్ స్కాన్ చేయించుకోండి.\n2. నూనె, కొవ్వు పదార్థాలు మరియు మద్యం పూర్తిగా మానెయ్యండి.\n3. గ్లూకోజ్, కొబ్బరి నీరు మరియు పండ్లను ఆహారంగా తీసుకోండి.\n4. తగినంత విశ్రాంతి తీసుకోండి.",
            "urgency": "Medium"
        }
    },

    # 3. Cardiovascular, Neurological & Organ-Specific
    "Coronary Artery Disease": {
        "en": {
            "prediction": "Coronary Artery Disease / Angina Pectoris",
            "description": "Compromised myocardial blood supply due to atheromatous plaque accumulation in coronary arteries, presenting with substernal crushing chest pain, arm/jaw radiation, and dyspnea.",
            "advice": "1. EMERGENCY: If crushing central chest pain radiates to left arm or jaw with diaphoresis, call 108/emergency services immediately.\n2. Undergo 12-lead ECG, cardiac troponin blood tests, and 2D Echocardiography.\n3. Cease tobacco smoking immediately and transition to a heart-healthy Mediterranean diet.\n4. Strictly comply with prescribed statins, antiplatelets, and beta-blockers.",
            "urgency": "Critical"
        },
        "hi": {
            "prediction": "कोरोनरी आर्टरी रोग / हृदय रोग (Heart Disease / CAD)",
            "description": "हृदय की धमनियों में रुकावट के कारण खून का प्रवाह कम होना। इसमें सीने में भारीपन, दर्द का बाएं हाथ, गर्दन या जबड़े तक फैलना और पसीना आना शामिल है।",
            "advice": "1. आपातकालीन चेतावनी: यदि सीने में तेज दर्द बाएं हाथ या जबड़े तक फैले तो तुरंत एम्बुलेंस बुलाएं और इमरजेंसी में जाएं।\n2. ईसीजी (ECG) और ट्रोपोनिन टेस्ट करवाएं।\n3. धूम्रपान तुरंत छोड़ें और कम तेल-मसाले वाला आहार लें।\n4. हृदय रोग विशेषज्ञ की दवाएं नियमित रूप से लें।",
            "urgency": "Critical"
        },
        "te": {
            "prediction": "గుండె జబ్బు / కొరోనరీ ఆర్టరీ వ్యాధి (Heart Attack Risk / CAD)",
            "description": "గుండెకు రక్తాన్ని సరఫరా చేసే నాళాలలో కొవ్వు పేరుకుపోవడం వల్ల వచ్చే ప్రమాదకర పరిస్థితి. ఛాతీలో తీవ్ర నొప్పి, ఎడమ చేతికి నొప్పి పాకడం మరియు ఆయాసం కలిగిస్తుంది.",
            "advice": "1. అత్యవసర హెచ్చరిక: ఛాతీలో విపరీతమైన నొప్పి వచ్చి ఎడమ చేయి లేదా దవడకు పాకితే వెంటనే 108 లేదా ఆసుపత్రికి వెళ్లండి.\n2. ఈసీజీ (ECG) మరియు గుండె సంబంధిత పరీక్షలు చేయించుకోండి.\n3. ధూమపానం మానేయండి, తక్కువ నూనె ఉన్న ఆహారం తీసుకోండి.\n4. వైద్యులు ఇచ్చిన గుండె మందులను నిరంతరం వాడండి.",
            "urgency": "Critical"
        }
    },
    "Stroke (TIA Warning)": {
        "en": {
            "prediction": "Cerebrovascular Accident / Transient Ischemic Attack (Stroke)",
            "description": "Acute interruption of focal cerebral blood flow resulting in neurological deficits: unilateral facial drooping, arm weakness/numbness, and dysarthria (slurred speech).",
            "advice": "1. CRITICAL: Remember F.A.S.T: Face drooping, Arm weakness, Slurred speech, Time to call emergency services!\n2. Rush immediately to a stroke-ready hospital equipped with an acute CT scanner within the 4.5-hour thrombolytic window.\n3. Do not administer aspirin at home before non-contrast CT excludes intracranial hemorrhage.\n4. Keep the patient lying flat with airway clear.",
            "urgency": "Critical"
        },
        "hi": {
            "prediction": "ब्रेन स्ट्रोक / पक्षाघात चेतावनी (Stroke / Paralysis Warning)",
            "description": "दिमाग की नस में रुकावट या ब्लीडिंग के कारण दिमाग को खून न मिलना। चेहरे का एक तरफ झुकना, एक हाथ में कमजोरी/सुन्नपन और बोलने में लड़खड़ाहट इसके मुख्य लक्षण हैं।",
            "advice": "1. F.A.S.T याद रखें: Face (चेहरा टेढ़ा होना), Arm (हाथ न उठना), Speech (बोली लड़खड़ाना), Time (तुरंत अस्पताल भागें)!\n2. मरीज को 4.5 घंटे के भीतर सीटी स्कैन वाले बड़े अस्पताल पहुंचाएं ताकि लकवे से बचाया जा सके।\n3. घर पर कोई दवा या पानी न दें, सिर को सीधा रखें।",
            "urgency": "Critical"
        },
        "te": {
            "prediction": "పక్షవాతం / బ్రెయిన్ స్ట్రోక్ హెచ్చరిక (Brain Stroke Warning)",
            "description": "మెదడుకు రక్తప్రసరణ ఆగిపోవడం వల్ల వచ్చే అత్యవసర ప్రమాదం. ముఖం ఒకవైపు వంకరపోవడం, ఒక చేయి లేదా కాలు చచ్చుబడిపోవడం, మాట ముద్దబడటం దీని ముఖ్య లక్షణాలు.",
            "advice": "1. F.A.S.T గుర్తుంచుకోండి: ముఖం వంకరపోవడం, చేయి బలం తగ్గడం, మాట స్పష్టత లేకపోతే క్షణం ఆలస్యం చేయకుండా ఆసుపత్రికి తరలించండి!\n2. మొదటి 4.5 గంటల గోల్డెన్ అవర్ లో సీటీ స్కాన్ ఉన్న ఆసుపత్రికి చేర్చడం ప్రాణరక్షకం.\n3. రోగికి ఇంట్లో ఎలాంటి ఆహారం లేదా మందులు ఇవ్వవద్దు.",
            "urgency": "Critical"
        }
    },
    "Chronic Kidney Disease": {
        "en": {
            "prediction": "Chronic Kidney Disease (CKD / Renal Dysfunction)",
            "description": "Progressive, irreversible decline in renal filtration capacity, leading to fluid overload (edema of legs and ankles), electrolyte imbalances, and accumulation of nitrogenous waste.",
            "advice": "1. Order Serum Creatinine, Blood Urea Nitrogen (BUN), and Urine Albumin-to-Creatinine Ratio (uACR).\n2. Maintain strict control of blood pressure (<130/80 mmHg) and blood sugar.\n3. Limit dietary sodium, potassium, and phosphorus under nephrologist direction.\n4. Avoid nephrotoxic medications like over-the-counter NSAID painkillers.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "क्रोनिक किडनी रोग / गुर्दे की बीमारी (Chronic Kidney Disease)",
            "description": "किडनी की कार्यक्षमता में धीरे-धीरे कमी आना, जिससे शरीर में जहरीले अपशिष्ट और पानी जमा होने लगता है। पैरों और टखनों में सूजन, पेशाब में झाग और थकान इसके लक्षण हैं।",
            "advice": "1. सीरम क्रिएटिनिन (Creatinine) और यूरिन प्रोटीन टेस्ट करवाएं।\n2. ब्लड प्रेशर और ब्लड शुगर को सख्त नियंत्रण में रखें।\n3. दर्द निवारक दवाएं (NSAIDs) बिना डॉक्टर के बिल्कुल न खाएं।\n4. नमक और प्रोटीन का सेवन नेफ्रोलॉजिस्ट की सलाह अनुसार करें।",
            "urgency": "High"
        },
        "te": {
            "prediction": "దీర్ఘకాలిక మూత్రపిండాల వ్యాధి (Chronic Kidney Disease - CKD)",
            "description": "కిడ్నీల పనితీరు క్రమంగా క్షీణించే పరిస్థితి. దీనివల్ల శరీరంలో వ్యర్థాలు మరియు నీరు పేరుకుపోయి కాళ్ల వాపులు, అలసట మరియు మూత్రంలో మార్పులు వస్తాయి.",
            "advice": "1. సీరం క్రియాటినిన్ (Serum Creatinine) మరియు మూత్ర పరీక్షలు చేయించుకోండి.\n2. బీపీ మరియు షుగర్ లెవెల్స్ ను పూర్తిగా అదుపులో ఉంచుకోండి.\n3. పెయిన్ కిల్లర్ మందులను ఇష్టానుసారంగా వాడవద్దు, ఇవి కిడ్నీలను మరింత దెబ్బతీస్తాయి.\n4. ఉప్పు వాడకాన్ని బాగా తగ్గించండి.",
            "urgency": "High"
        }
    },
    "Anemia": {
        "en": {
            "prediction": "Iron-Deficiency Anemia / Nutritional Anemia",
            "description": "A deficiency in circulating red blood cells or hemoglobin, impairing cellular oxygen transport throughout peripheral tissues, causing extreme fatigue, pallor, and exertional dyspnea.",
            "advice": "1. Perform a Complete Blood Count (CBC) and Serum Ferritin profile.\n2. Consume iron-rich foods: spinach, beetroots, pomegranates, jaggery, and lentils.\n3. Pair iron-rich meals with Vitamin C (lemon juice, oranges) to enhance intestinal iron absorption.\n4. Take oral iron supplements as directed with clean water; avoid tea or coffee within 2 hours of intake.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "एनीमिया / खून की कमी (Iron Deficiency Anemia)",
            "description": "शरीर में हीमोग्लोबिन या लाल रक्त कोशिकाओं की कमी होना, जिससे अंगों तक पर्याप्त ऑक्सीजन नहीं पहुंच पाती। अत्यधिक कमजोरी, पीला चेहरा, चक्कर और हाथ-पैर ठंडे रहना इसके मुख्य लक्षण हैं।",
            "advice": "1. हीमोग्लोबिन (CBC) और फेरिटिन टेस्ट करवाएं।\n2. पालक, अनार, चुकंदर, गुड़ और खजूर का नियमित सेवन करें।\n3. आयरन सोखने के लिए नींबू पानी या संतरे का रस पिएं।\n4. डॉक्टर की सलाह से आयरन की गोलियां लें; दवा के साथ चाय/कॉफी न पिएं।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "రక్తహీనత / ఎనీమియా (Anemia - Low Hemoglobin)",
            "description": "రక్తంలో హిమోగ్లోబిన్ లేదా ఎర్ర రక్త కణాల లోపం. దీనివల్ల శరీర కణజాలాలకు ఆక్సిజన్ అందక తీవ్ర నీరసం, చర్మం పాలిపోవడం, తలతిరగడం మరియు ఆయాసం వస్తాయి.",
            "advice": "1. కంప్లీట్ బ్లడ్ పిక్చర్ (CBC) పరీక్ష చేయించుకుని హిమోగ్లోబిన్ శాతాన్ని తెలుసుకోండి.\n2. పాలకూర, దానిమ్మ, బీట్‌రూట్, బెల్లం మరియు ఖర్జూరం ఆహారంలో చేర్చుకోండి.\n3. ఐరన్ సరిగ్గా ఒంటపట్టడానికి నిమ్మరసం లేదా నారింజ రసం తీసుకోండి.\n4. వైద్యుల సలహాతో ఐరన్ మాత్రలు వాడండి.",
            "urgency": "Medium"
        }
    },
    "Hypothyroidism": {
        "en": {
            "prediction": "Hypothyroidism (Underactive Thyroid)",
            "description": "Insufficient secretion of thyroid hormones (T3/T4) by the thyroid gland, slowing systemic metabolic rate, leading to unexplained weight gain, chronic fatigue, cold intolerance, and dry skin.",
            "advice": "1. Get a comprehensive Thyroid Profile (TSH, Free T3, Free T4) drawn in early morning fasting state.\n2. Take prescribed Levothyroxine daily on an empty stomach with plain water 30–60 minutes before breakfast.\n3. Incorporate dietary iodine and selenium sources while avoiding raw goitrogenic vegetables (raw cabbage/kale in excess).\n4. Re-check TSH levels every 6–12 weeks until therapeutic stabilization.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "हाइपोथायरायडिज्म / थायराइड विकार (Hypothyroidism)",
            "description": "थायराइड ग्रंथि द्वारा पर्याप्त थायराइड हार्मोन न बना पाना। इससे शरीर की चयापचय दर धीमी हो जाती है, जिससे अचानक वजन बढ़ना, अत्यधिक थकान, ठंड लगना और रूखी त्वचा होती है।",
            "advice": "1. खाली पेट थायराइड प्रोफाइल (TSH, T3, T4) टेस्ट करवाएं।\n2. थायराइड की दवा (Levothyroxine) रोजाना सुबह खाली पेट एक गिलास पानी के साथ लें।\n3. दवा लेने के आधे घंटे बाद तक चाय या नाश्ता न करें।\n4. हर 2-3 महीने में TSH की जांच कराकर दवा की खुराक सही रखें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "హైపోథైరాయిడిజం / థైరాయిడ్ సమస్య (Hypothyroidism)",
            "description": "థైరాయిడ్ గ్రంథి తగినంత హార్మోన్లను విడుదల చేయకపోవడం. దీనివల్ల జీవక్రియ మందగించి కారణం లేకుండా బరువు పెరగడం, తీవ్ర అలసట, చలిని తట్టుకోలేకపోవడం మరియు చర్మం పొడిబారడం జరుగుతాయి.",
            "advice": "1. ఉదయం పరగడుపున థైరాయిడ్ ప్రొఫైల్ (TSH, T3, T4) పరీక్ష చేయించుకోండి.\n2. థైరాయిడ్ మాత్రలను ప్రతిరోజూ ఉదయం అల్పాహారానికి అరగంట ముందు ఖాళీ కడుపుతో వేసుకోండి.\n3. క్యాబేజీ, క్యాలీఫ్లవర్ వంటి వాటిని పచ్చిగా తినవద్దు.\n4. క్రమం తప్పకుండా TSH పరీక్ష చేయించి మందుల మోతాదును సరిచూసుకోండి.",
            "urgency": "Medium"
        }
    },
    "Hyperthyroidism": {
        "en": {
            "prediction": "Hyperthyroidism (Overactive Thyroid / Graves' Disease)",
            "description": "Excessive synthesis and secretion of thyroid hormones, accelerating systemic metabolism, presenting with unintended rapid weight loss, resting tachycardia, hand tremors, and heat intolerance.",
            "advice": "1. Schedule Free T3, Free T4, TSH, and thyroid antibody/ultrasound diagnostics.\n2. Consult an endocrinologist for antithyroid medications (e.g., Methimazole) or beta-blockers for palpitations.\n3. Increase healthy caloric density to counteract hypermetabolic muscle wasting.\n4. Avoid excessive dietary iodine and caffeine stimulants.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "हाइपरथायरायडिज्म (Hyperthyroidism - Overactive)",
            "description": "थायराइड ग्रंथि द्वारा जरूरत से ज्यादा हार्मोन का निर्माण होना। इससे चयापचय बहुत तेज हो जाता है, जिससे अचानक वजन घटना, दिल की धड़कन तेज होना, हाथों में कंपन और घबराहट होती है।",
            "advice": "1. थायराइड प्रोफाइल टेस्ट करवाएं और एंडोक्रिनोलॉजिस्ट से मिलें।\n2. दिल की धड़कन और घबराहट रोकने के लिए डॉक्टर की दवाएं लें।\n3. कैफीन, चाय और अधिक आयोडीन युक्त चीजों से बचें।\n4. पौष्टिक और संतुलित आहार लें ताकि वजन स्थिर रह सके।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "హైపర్‌థైరాయిడిజం (Hyperthyroidism - Overactive Thyroid)",
            "description": "థైరాయిడ్ గ్రంథి అధిక మోతాదులో హార్మోన్లను ఉత్పత్తి చేయడం. దీనివల్ల జీవక్రియ అతి వేగంగా జరిగి బరువు తగ్గడం, గుండె దడ, చేతులు వణకడం మరియు వేడిని తట్టుకోలేకపోవడం జరుగుతాయి.",
            "advice": "1. థైరాయిడ్ హార్మోన్ పరీక్షలు చేయించి నిపుణులైన వైద్యులను సంప్రదించండి.\n2. గుండె దడ నియంత్రణకు సూచించిన మందులు వాడండి.\n3. కాఫీ, టీ మరియు ఉత్ప్రేరకాలకు దూరంగా ఉండండి.\n4. బలవర్ధకమైన సమతుల్య ఆహారం తీసుకోండి.",
            "urgency": "Medium"
        }
    },
    "Migraine": {
        "en": {
            "prediction": "Migraine (Neurovascular Cephalea)",
            "description": "A primary neurological disorder causing recurrent episodes of moderate-to-severe unilateral throbbing headaches, frequently aggravated by physical activity and associated with photophobia and nausea.",
            "advice": "1. Rest in a dark, quiet room with an ice pack applied over the forehead or occiput.\n2. Identify and track personal triggers: irregular sleep, skipped meals, bright screens, aged cheeses, or stress.\n3. Stay consistently hydrated with cool water.\n4. Discuss triptans or preventive therapies with a neurologist if attacks occur >4 days monthly.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "माइग्रेन / आधासीसी (Migraine Headache)",
            "description": "सिर के एक हिस्से में होने वाला तेज धड़कता हुआ दर्द। इसके साथ जी मिचलाना, उल्टी आना और तेज रोशनी या आवाज से परेशानी होना बहुत आम है।",
            "advice": "1. अंधेरे और शांत कमरे में आराम करें; माथे पर ठंडे पानी की पट्टी या बर्फ लगाएं।\n2. नींद का समय निश्चित रखें और खाली पेट न रहें।\n3. मोबाइल और टीवी स्क्रीन से दूरी बनाएं।\n4. बार-बार माइग्रेन होने पर न्यूरोलॉजिस्ट से निवारक दवाएं लें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "మైగ్రేన్ / పార్శ్వపు తలనొప్పి (Migraine)",
            "description": "తల ఒక వైపు తీవ్రంగా పోటు వచ్చే నాడీ సంబంధిత సమస్య. వికారం, వాంతులు మరియు కాంతి లేదా శబ్దాలను భరించలేకపోవడం దీని లక్షణాలు.",
            "advice": "1. నిశ్శబ్దమైన, చీకటి గదిలో విశ్రాంతి తీసుకోండి; నుదుటిపై ఐస్ ప్యాక్ పెట్టండి.\n2. సమయానికి భోజనం చేయడం మరియు తగినంత నిద్రపోవడం ముఖ్యం.\n3. మొబైల్ స్క్రీన్లు మరియు తీవ్రమైన ఎండకు దూరంగా ఉండండి.\n4. నెలకు 3-4 సార్ల కంటే ఎక్కువ వస్తే వైద్యుడిని సంప్రదించండి.",
            "urgency": "Medium"
        }
    },
    "GERD (Acid Reflux)": {
        "en": {
            "prediction": "GERD / Acid Reflux (Gastroesophageal Reflux)",
            "description": "Retrograde flow of gastric acid past an incompetent lower esophageal sphincter into the esophagus, producing chronic retrosternal heartburn and acidic regurgitation.",
            "advice": "1. Elevate the head of your bed by 6 inches; avoid lying down for 3 hours following meals.\n2. Eliminate trigger foods: citrus fruits, tomatoes, caffeine, chocolates, fatty foods, and carbonated beverages.\n3. Eat smaller, more frequent meals rather than large heavy dinners.\n4. Consult a physician regarding short-term proton pump inhibitors (PPIs).",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "जीईआरडी / एसिड रिफ्लक्स (GERD - Acidity)",
            "description": "पेट के एसिड का वापस भोजन नली (ग्रासनली) में आना। इससे सीने में तेज जलन (हार्टबर्न), खट्टी डकारें और मुंह में खट्टा पानी आने की समस्या होती है।",
            "advice": "1. खाना खाने के तुरंत बाद न लेटें, कम से कम 2-3 घंटे बाद सोएं।\n2. ज्यादा मिर्च-मसाले, तली चीजें, चाय-कॉफी और खट्टे फल कम करें।\n3. एक बार में ज्यादा खाने के बजाय थोड़ा-थोड़ा करके खाएं।\n4. सोते समय सिरहाने को थोड़ा ऊंचा रखें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "ఆసిడ్ రిఫ్లక్స్ / గ్యాస్ట్రిక్ మంట (GERD - Acid Reflux)",
            "description": "కడుపులోని ఆమ్లం ఆహారనాళంలోకి తిరిగి రావడం వల్ల వచ్చే సమస్య. ఛాతీలో మంట (హార్ట్‌బర్న్), పుల్లటి తేన్పులు మరియు గొంతులో మంట కలిగిస్తుంది.",
            "advice": "1. భోజనం చేసిన వెంటనే పడుకోవద్దు, కనీసం 2-3 గంటల సమయం ఇవ్వండి.\n2. కారం, మసాలాలు, టీ, కాఫీ మరియు వేపుడు పదార్థాలు మానెయ్యండి.\n3. ఒకేసారి ఎక్కువగా తినకుండా కొద్దికొద్దిగా ఎక్కువ సార్లు తినండి.\n4. పడుకునేటప్పుడు తల వైపు భాగాన్ని కొద్దిగా ఎత్తుగా ఉంచండి.",
            "urgency": "Medium"
        }
    },
    "Peptic Ulcer": {
        "en": {
            "prediction": "Peptic Ulcer Disease (Gastric / Duodenal Ulcer)",
            "description": "Disruption and mucosal ulceration of the stomach or duodenum, predominantly driven by Helicobacter pylori infection or prolonged NSAID painkiller consumption, marked by burning epigastric pain.",
            "advice": "1. Undergo testing for H. pylori infection (Urea Breath Test or stool antigen test).\n2. Strictly avoid NSAID painkillers (ibuprofen, naproxen); use acetaminophen under medical guidance.\n3. Avoid smoking, alcohol, and heavily spiced culinary preparations.\n4. Seek immediate emergency evaluation if vomit contains blood or stools appear jet black.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "पेप्टिक अल्सर / पेट का छाला (Peptic Ulcer Disease)",
            "description": "पेट या छोटी आंत की अंदरूनी परत में घाव (अल्सर) बन जाना। भोजन के बीच या रात में पेट में तेज जलन और दर्द होना इसका मुख्य लक्षण है।",
            "advice": "1. एच. पाइलोरी (H. pylori) बैक्टीरिया की जांच करवाएं।\n2. दर्द निवारक गोलियां (NSAIDs) बिल्कुल न लें, ये अल्सर को गहरा करती हैं।\n3. शराब, सिगरेट और बहुत तीखे खाने से दूर रहें।\n4. यदि उल्टी में खून आए या काला मल आए तो तुरंत अस्पताल जाएं।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "కడుపులో పుండ్లు / పెప్టిక్ అల్సర్ (Peptic Ulcer Disease)",
            "description": "కడుపు లేదా ప్రేగుల లోపలి పొరలో పుండ్లు ఏర్పడటం. హెచ్. పైలోరి బ్యాక్టీరియా లేదా పెయిన్ కిల్లర్ మందుల వల్ల వస్తుంది. కడుపులో మంట మరియు నొప్పి దీని ప్రధాన లక్షణాలు.",
            "advice": "1. హెచ్. పైలోరి బ్యాక్టీరియా పరీక్ష చేయించుకోండి.\n2. పెయిన్ కిల్లర్ మందులను వాడటం వెంటనే ఆపండి.\n3. ధూమపానం, మద్యం మరియు అధిక మసాలాలకు దూరంగా ఉండండి.\n4. నల్లటి విరేచనాలు లేదా వాంతిలో రక్తం వస్తే వెంటనే అత్యవసర చికిత్స పొందండి.",
            "urgency": "Medium"
        }
    },
    "Urinary Tract Infection": {
        "en": {
            "prediction": "Urinary Tract Infection (Cystitis / UTI)",
            "description": "Bacterial colonization of the urinary bladder and urethra, causing dysuria (burning micturition), urinary urgency, pelvic cramping, and cloudy, malodorous urine.",
            "advice": "1. Drink 2.5–3 liters of water daily to flush bacteria from the urinary tract.\n2. Obtain a clean-catch midstream urine routine and culture test.\n3. Complete the prescribed short course of targeted antibiotics; do not discontinue prematurely.\n4. Avoid feminine hygiene sprays and hold urine for prolonged intervals.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "मूत्र मार्ग संक्रमण / यूटीआई (Urinary Tract Infection)",
            "description": "मूत्राशय या मूत्रमार्ग में बैक्टीरिया का संक्रमण। पेशाब करते समय तेज जलन, बार-बार पेशाब आने की इच्छा और पेट के निचले हिस्से में दर्द इसके मुख्य लक्षण हैं।",
            "advice": "1. दिन में 2.5 से 3 लीटर पानी पिएं ताकि बैक्टीरिया बाहर निकल सके।\n2. यूरिन रूटीन और कल्चर टेस्ट करवाएं।\n3. डॉक्टर द्वारा दी गई एंटीबायोटिक दवाओं का कोर्स पूरा करें।\n4. व्यक्तिगत स्वच्छता बनाए रखें और पेशाब को ज्यादा देर न रोकें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "మూత్రనాళ ఇన్ఫెక్షన్ / యుటిఐ (Urinary Tract Infection - UTI)",
            "description": "మూత్రాశయంలో బ్యాక్టీరియా చేరడం వల్ల వచ్చే సమస్య. మూత్ర విసర్జన సమయంలో తీవ్ర మంట, నొప్పి, తరచుగా మూత్రం రావడం దీని లక్షణాలు.",
            "advice": "1. బ్యాక్టీరియా బయటకు వెళ్లిపోవడానికి రోజుకు 3 లీటర్ల నీరు తాగండి.\n2. యూరిన్ రొటీన్ మరియు కల్చర్ పరీక్ష చేయించుకోండి.\n3. వైద్యులు రాసిన యాంటీబయాటిక్స్ కోర్సును క్రమంతప్పకుండా పూర్తి చేయండి.\n4. వ్యక్తిగత పరిశుభ్రత పాటించండి మరియు మూత్రాన్ని ఎక్కువసేపు ఆపుకోవద్దు.",
            "urgency": "Medium"
        }
    },

    # 4. Dermatological & Allergic
    "Allergic Rhinitis": {
        "en": {
            "prediction": "Allergic Rhinitis (Hay Fever / Inhalant Allergy)",
            "description": "IgE-mediated inflammatory hypersensitivity of the nasal mucosa triggered by airborne allergens (pollen, dust mites, molds, animal dander), causing paroxysmal sneezing and rhinorrhea.",
            "advice": "1. Use saline nasal irrigations to clear inhaled allergens.\n2. Keep windows closed during high pollen or windy dust conditions.\n3. Take second-generation non-sedating oral antihistamines (e.g., Cetirizine, Loratadine).\n4. Wash bed linens weekly in hot water (60°C) to eliminate dust mites.",
            "urgency": "Low"
        },
        "hi": {
            "prediction": "एलर्जिक राइनाइटिस / मौसमी एलर्जी (Allergic Rhinitis)",
            "description": "धूल, परागकण या जानवरों के बालों से होने वाली नाक की एलर्जी। लगातार छींकें आना, नाक बहना, आंखों में खुजली और पानी आना इसके मुख्य लक्षण हैं।",
            "advice": "1. धूल-मिट्टी और पराग से बचने के लिए बाहर जाते समय मास्क पहनें।\n2. नाक को साफ करने के लिए सलाइन नेजल स्प्रे का प्रयोग करें।\n3. डॉक्टर की सलाह से एंटीहिस्टामाइन दवाएं लें।\n4. चादरों और तकियों को नियमित गर्म पानी से धोएं।",
            "urgency": "Low"
        },
        "te": {
            "prediction": "ఎలర్జిక్ రైనైటిస్ / తుమ్ముల అలర్జీ (Allergic Rhinitis)",
            "description": "దుమ్ము, పుప్పొడి లేదా కాలుష్యం వల్ల ముక్కు లోపలి పొరలో వచ్చే ఎలర్జీ. ఆగకుండా తుమ్ములు రావడం, ముక్కు కారడం మరియు కళ్లలో దురద దీని లక్షణాలు.",
            "advice": "1. బయటకు వెళ్ళేటప్పుడు దుమ్ము తగలకుండా మాస్క్ ధరించండి.\n2. ముక్కు దిబ్బడ తగ్గడానికి సలైన్ స్ప్రే వాడండి.\n3. వైద్యుల సలహాతో యాంటీ-అలర్జీ మందులు తీసుకోండి.\n4. బెడ్ షీట్లను వేడి నీటితో శుభ్రం చేసుకోండి.",
            "urgency": "Low"
        }
    },
    "Food Allergy": {
        "en": {
            "prediction": "Food Allergy / Hypersensitivity Reaction",
            "description": "An immunological adverse reaction to specific dietary antigens (e.g., shellfish, peanuts, milk, eggs), causing localized cutaneous hives, oral pruritus, abdominal cramps, or anaphylaxis.",
            "advice": "1. Immediately identify and completely eliminate the offending allergen from your diet.\n2. Take prescribed oral antihistamines for localized urticaria and itching.\n3. CRITICAL: If throat tightness, tongue swelling, or wheezing develops, seek EMERGENCY medical care immediately for epinephrine injection.\n4. Carefully inspect pre-packaged food ingredient labels.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "फूड एलर्जी / खाद्य एलर्जी (Food Allergy)",
            "description": "किसी विशेष खाद्य पदार्थ (जैसे मूंगफली, दूध, अंडा, सीफूड) के प्रति शरीर की प्रतिरक्षा प्रणाली की तीव्र प्रतिक्रिया। त्वचा पर पित्ती (चकत्ते), उल्टी और पेट दर्द होता है।",
            "advice": "1. जिस भोजन से एलर्जी हुई है, उसका सेवन तुरंत बंद करें।\n2. खुजली और चकत्तों के लिए एंटीहिस्टामाइन दवा लें।\n3. आपातकालीन चेतावनी: यदि सांस लेने में दिक्कत या होंठ/जीभ में सूजन आए तो तुरंत अस्पताल जाएं।\n4. बाहर का खाना खरीदते समय सामग्री (Labels) ध्यान से पढ़ें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "ఆహార అలర్జీ (Food Allergy Reaction)",
            "description": "కొన్ని రకాల ఆహార పదార్థాలు (వేరుశనగలు, పాలు, గుడ్లు, చేపలు) పడకపోవడం వల్ల వచ్చే అలర్జీ. చర్మంపై దద్దుర్లు, దురద, వాంతులు మరియు కడుపు నొప్పి కలిగిస్తుంది.",
            "advice": "1. అలర్జీ కలిగించిన ఆహారాన్ని వెంటనే గుర్తించి తినడం ఆపేయండి.\n2. దురద తగ్గడానికి యాంటీహిస్టామైన్ మందులు వాడండి.\n3. అత్యవసర హెచ్చరిక: గొంతు వాపు లేదా శ్వాసలో ఇబ్బంది వస్తే వెంటనే ఎమర్జెన్సీ వార్డుకు వెళ్లండి.\n4. ప్యాక్ చేసిన ఆహార లేబుల్స్ జాగ్రత్తగా చదవండి.",
            "urgency": "Medium"
        }
    },
    "Eczema": {
        "en": {
            "prediction": "Eczema (Atopic Dermatitis)",
            "description": "A chronic pruritic inflammatory skin disorder impaired by cutaneous epidermal barrier defects, leading to dry, fissured, erythematous, and intensely itchy skin plaques.",
            "advice": "1. Apply liberal fragrance-free ceramide emollient within 3 minutes of bathing.\n2. Bathe with lukewarm water; avoid harsh antibacterial soaps and synthetic loofahs.\n3. Wear soft, breathable 100% cotton garments.\n4. Apply topical anti-inflammatory ointments as prescribed during flares.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "एक्जिमा / खाज (Eczema - Atopic Dermatitis)",
            "description": "त्वचा की पुरानी सूजन संबंधी बीमारी जिसमें त्वचा अत्यधिक रूखी, लाल, पपड़ीदार और तेज खुजली वाली हो जाती है। यह अक्सर कोहनी और घुटनों के पीछे होती है।",
            "advice": "1. नहाने के तुरंत बाद गाढ़ा मॉइस्चराइजर (जैसे सेरामाइड क्रीम) लगाएं।\n2. गुनगुने पानी से नहाएं और कठोर साबुन का प्रयोग न करें।\n3. केवल सूती और आरामदायक कपड़े पहनें।\n4. त्वचा को खुजलाने से बचें ताकि संक्रमण न फैले।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "ఎగ్జిమా / గజ్జి (Eczema - Skin Dermatitis)",
            "description": "చర్మం విపరీతంగా పొడిబారి, ఎర్రటి మచ్చలు మరియు తీవ్రమైన దురద కలిగించే చర్మ వ్యాధి. చర్మ రక్షణ పొర దెబ్బతినడం వల్ల ఇది వస్తుంది.",
            "advice": "1. స్నానం చేసిన వెంటనే తేమ పోకుండా మంచి మాయిశ్చరైజర్ రాయండి.\n2. వేడి నీటి స్నానాలు మరియు ఘాటైన సబ్బులకు దూరంగా ఉండండి.\n3. కాటన్ దుస్తులు మాత్రమే ధరించండి.\n4. చర్మాన్ని గోళ్లతో గిల్లవద్దు.",
            "urgency": "Medium"
        }
    },
    "Psoriasis": {
        "en": {
            "prediction": "Psoriasis (Plaque Psoriasis / Autoimmune)",
            "description": "An immune-mediated chronic dermatological disease marked by hyperproliferation of keratinocytes, resulting in well-demarcated erythematous plaques topped with coarse silvery-white scales.",
            "advice": "1. Apply topical keratolytics (Salicylic acid, coal tar) and Vitamin D analogs under dermatologist guidance.\n2. Maintain consistent daily skin barrier hydration with thick ointments.\n3. Get measured, brief natural sunlight exposure to downregulate epidermal overgrowth.\n4. Screen for concurrent joint inflammation (Psoriatic Arthritis).",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "सोरायसिस / चर्मरोग (Psoriasis Autoimmune)",
            "description": "त्वचा का ऑटोइम्यून रोग जिसमें त्वचा की कोशिकाएं बहुत तेजी से बनने लगती हैं। इससे त्वचा पर लाल चकत्ते और चांदी जैसी सफेद पपड़ी (Scales) जम जाती है।",
            "advice": "1. त्वचा रोग विशेषज्ञ (Dermatologist) की सलाह से मरहम और दवाएं लगाएं।\n2. त्वचा पर नारियल तेल या वैसलीन लगाकर हमेशा नमी बनाए रखें।\n3. सुबह की हल्की धूप लें, यह त्वचा के लिए लाभकारी होती है।\n4. तनाव कम करें, क्योंकि तनाव से सोरायसिस बढ़ जाता है।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "సోరియాసిస్ (Psoriasis Skin Disease)",
            "description": "చర్మ కణాలు వేగంగా వృద్ధి చెందడం వల్ల వచ్చే ఆటో ఇమ్యూన్ వ్యాధి. చర్మంపై ఎర్రటి మచ్చలు మరియు వెండి రంగు పొలుసులు ఏర్పడి తీవ్రమైన దురద, మంట కలిగిస్తాయి.",
            "advice": "1. చర్మవ్యాధి నిపుణులను సంప్రదించి సరైన లేపనాలు మరియు మందులు వాడండి.\n2. చర్మం పొడిబారకుండా కొబ్బరి నూనె లేదా మాయిశ్చరైజర్ రోజూ రాయండి.\n3. ఉదయం వేళ లేలేత ఎండలో కొద్దిసేపు ఉండటం మంచిది.\n4. ఒత్తిడిని తగ్గించుకోండి, ఇది వ్యాధి తీవ్రతను పెంచుతుంది.",
            "urgency": "Medium"
        }
    },
    "Acne Vulgaris": {
        "en": {
            "prediction": "Acne Vulgaris (Sebaceous Dermatosis)",
            "description": "Inflammatory condition of pilosebaceous units triggered by androgen-driven sebum hypersecretion, follicular hyperkeratinization, and Cutibacterium acnes colonization.",
            "advice": "1. Cleanse gently with a 2% salicylic acid or benzoyl peroxide cleanser twice daily.\n2. Use strictly oil-free, non-comedogenic sunscreens and moisturizers.\n3. Do not squeeze, pick, or pop acne lesions to avoid permanent dermal scarring.\n4. Inquire with a dermatologist about topical retinoids for long-term resolution.",
            "urgency": "Low"
        },
        "hi": {
            "prediction": "मुंहासे / कील-मुंहासे (Acne Vulgaris)",
            "description": "त्वचा की तैलीय ग्रंथियों में रुकावट और बैक्टीरिया के कारण चेहरे, गर्दन और पीठ पर पिंपल्स, ब्लैकहेड्स और व्हाइटहेड्स का निकलना।",
            "advice": "1. चेहरे को दिन में दो बार सेलिसिलिक एसिड वाले फेसवॉश से धोएं।\n2. पिंपल्स को कभी भी हाथ से न फोड़ें, इससे चेहरे पर गड्ढे और काले दाग पड़ जाते हैं।\n3. नॉन-कॉमेडोजेनिक (तेल रहित) सनस्क्रीन और क्रीम का उपयोग करें।\n4. अधिक पानी पिएं और तैलीय भोजन कम करें।",
            "urgency": "Low"
        },
        "te": {
            "prediction": "మొటిమలు / ఆక్నే (Acne Vulgaris)",
            "description": "చర్మ రంధ్రాలలో నూనె మరియు మృతకణాలు పేరుకుపోవడం వల్ల వచ్చే సాధారణ సమస్య. ముఖంపై పింపుల్స్, నల్లటి మరియు తెల్లటి మొటిమలు వస్తాయి.",
            "advice": "1. ముఖాన్ని రోజుకు రెండుసార్లు మంచి క్లెన్సర్‌తో శుభ్రం చేసుకోండి.\n2. మొటిమలను గోళ్లతో గిల్లవద్దు, దీనివల్ల మచ్చలు పడతాయి.\n3. ఆయిల్ ఫ్రీ (నూనె లేని) క్రీములు మాత్రమే వాడండి.\n4. తగినంత నీరు తాగండి మరియు జిడ్డు ఆహారాన్ని తగ్గించండి.",
            "urgency": "Low"
        }
    }
}


def load_models():
    """Load models from disk and cache in memory."""
    global _symptom_model, _symptoms_list, _image_model
    
    if _symptom_model is None or _symptoms_list is None:
        if os.path.exists(SYMPTOM_MODEL_PATH) and os.path.exists(SYMPTOMS_LIST_PATH):
            with open(SYMPTOM_MODEL_PATH, "rb") as f:
                _symptom_model = pickle.load(f)
            with open(SYMPTOMS_LIST_PATH, "rb") as f:
                _symptoms_list = pickle.load(f)
        else:
            print("Warning: Symptom models not found. Run train_models.py!")

    if _image_model is None:
        if os.path.exists(IMAGE_MODEL_PATH):
            with open(IMAGE_MODEL_PATH, "rb") as f:
                _image_model = pickle.load(f)
        else:
            print("Warning: Image model not found. Run train_models.py!")


def extract_symptoms_from_text(text, lang="en"):
    """Parse text query to extract symptom keywords supporting English, Hindi, Telugu."""
    text_lower = text.lower()
    matched = []
    
    vocab = SYMPTOM_VOCAB.get(lang, SYMPTOM_VOCAB["en"])
    for symptom_key, terms in vocab.items():
        for term in terms:
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, text_lower) or term in text_lower:
                matched.append(symptom_key)
                break
                
    if lang != "en":
        eng_vocab = SYMPTOM_VOCAB["en"]
        for symptom_key, terms in eng_vocab.items():
            if symptom_key in matched:
                continue
            for term in terms:
                pattern = r'\b' + re.escape(term) + r'\b'
                if re.search(pattern, text_lower) or term in text_lower:
                    matched.append(symptom_key)
                    break
                    
    return list(set(matched))


def _compute_rule_scores(symptom_keys):
    """Score each disease based on symptom overlap and hallmark signatures."""
    symptom_set = set(symptom_keys)
    scores = {}

    for disease, disease_syms in disease_symptoms.items():
        matched = symptom_set & set(disease_syms)
        if not matched:
            scores[disease] = 0.0
            continue

        signature = DISEASE_SIGNATURE.get(disease, set())
        if signature and not (symptom_set & signature):
            penalty = 0.10
        else:
            penalty = 1.0

        weighted_match = sum(SYMPTOM_WEIGHTS.get(s, 1.0) for s in matched)
        weighted_profile = sum(SYMPTOM_WEIGHTS.get(s, 1.0) for s in disease_syms)
        coverage = len(matched) / len(disease_syms)
        specificity = weighted_match / max(weighted_profile, 1.0)

        specific_count = len(matched - GENERIC_SYMPTOMS)
        specificity_bonus = 1.0 + (specific_count * 0.20)

        scores[disease] = (coverage * 0.35 + specificity * 0.65) * penalty * specificity_bonus

    return scores


def _normalize_scores(score_dict):
    """Convert raw scores to probability distribution."""
    total = sum(score_dict.values())
    if total <= 0:
        n = len(score_dict)
        return {k: 1.0 / n for k in score_dict}
    return {k: v / total for k, v in score_dict.items()}


def _blend_predictions(ml_probs, rule_probs, symptom_count):
    """Blend ML and clinical rule scores dynamically."""
    if symptom_count <= 1:
        ml_weight, rule_weight = 0.15, 0.85
    elif symptom_count == 2:
        ml_weight, rule_weight = 0.40, 0.60
    else:
        ml_weight, rule_weight = 0.60, 0.40

    all_diseases = set(ml_probs.keys()) | set(rule_probs.keys())
    blended = {}
    for disease in all_diseases:
        ml_val = ml_probs.get(disease, 0.0)
        rule_val = rule_probs.get(disease, 0.0)
        blended[disease] = ml_val * ml_weight + rule_val * rule_weight

    return _normalize_scores(blended)


def _get_follow_up_questions(symptom_keys, lang="en"):
    """Generate contextual follow-up questions."""
    questions = []
    seen = set()

    for sym in symptom_keys:
        for q in FOLLOW_UP_BY_SYMPTOM.get(sym, []):
            if q not in seen:
                questions.append(q)
                seen.add(q)

    if not questions and symptom_keys:
        questions = FOLLOW_UP_BY_SYMPTOM.get("fever", [])[:3]

    return questions[:4]


def _detect_red_flags(symptom_keys):
    """Detect critical emergency conditions."""
    symptom_set = set(symptom_keys)
    flags = []
    for required, message in RED_FLAG_RULES:
        if required.issubset(symptom_set):
            flags.append(message)
    return flags


def _determine_prediction_mode(symptom_keys, confidence, top_disease):
    """Determine confidence mode."""
    specific = set(symptom_keys) - GENERIC_SYMPTOMS

    if len(symptom_keys) == 0:
        return "none"
    if len(symptom_keys) == 1 and symptom_keys[0] in GENERIC_SYMPTOMS:
        return "insufficient"
    if len(specific) == 0 and len(symptom_keys) <= 2:
        return "differential"
    if confidence < 0.45:
        return "differential"
    return "confirmed"


CARE_LEVEL_TEXT = {
    "seek_emergency": {
        "en": "🚨 **Action:** Seek emergency medical care immediately.",
        "hi": "🚨 **कार्रवाई:** तुरंत आपातकालीन चिकित्सा सहायता लें।",
        "te": "🚨 **చర్య:** వెంటనే అత్యవసర వైద్య సహాయం పొందండి."
    },
    "see_doctor_soon": {
        "en": "🏥 **Action:** Consult a doctor within 24–48 hours if symptoms persist or worsen.",
        "hi": "🏥 **कार्रवाई:** यदि लक्षण बने रहें या बढ़ें, तो 24–48 घंटे में डॉक्टर से मिलें।",
        "te": "🏥 **చర్య:** లక్షణాలు కొనసాగితే 24–48 గంటలలో డాక్టరును సంప్రదించండి."
    },
    "monitor_and_report": {
        "en": "👁️ **Action:** Monitor at home, log vitals, and describe any additional symptoms for a clearer diagnosis.",
        "hi": "👁️ **कार्रवाई:** घर पर निगरानी करें, वाइटल्स लॉग करें, और अधिक लक्षण बताएं।",
        "te": "👁️ **చర్య:** ఇంట్లో పర్యవేక్షించండి, వైటల్స్ నమోదు చేయండి, మరిన్ని లక్షణాలు చెప్పండి."
    },
    "home_care_ok": {
        "en": "✅ **Action:** Home rest and hydration are appropriate; watch for worsening signs.",
        "hi": "✅ **कार्रवाई:** घर पर आराम और हाइड्रेशन पर्याप्त है; बिगड़ते लक्षणों पर ध्यान दें।",
        "te": "✅ **చర్య:** ఇంట్లో విశ్రాంతి, ద్రవాలు తీసుకోండి; మెరుగుపడకపోతే డాక్టరును సంప్రదించండి."
    }
}


def _get_care_level(urgency, red_flags, prediction_mode):
    if red_flags or urgency in ("Critical", "High"):
        return "seek_emergency"
    if urgency == "Medium" or prediction_mode == "differential":
        return "see_doctor_soon"
    if prediction_mode == "insufficient":
        return "monitor_and_report"
    return "home_care_ok"


def predict_disease(symptom_keys, lang="en"):
    """Predict disease using hybrid ML + clinical rule engine with calibrated confidence."""
    load_models()

    if _symptom_model is None or _symptoms_list is None:
        return {"error": "Symptom prediction model is not trained/loaded."}

    if not symptom_keys:
        return {
            "prediction": "No Symptoms Detected",
            "confidence": 0.0,
            "description": "Please describe your physical symptoms (e.g. fever, joint pain, cough) for analysis.",
            "advice": "",
            "urgency": "None",
            "probabilities": {},
            "prediction_mode": "none",
            "follow_up_questions": [],
            "red_flags": [],
            "care_level": "monitor_and_report"
        }

    # Intercept single fever
    if len(symptom_keys) == 1 and "fever" in symptom_keys:
        info = {
            "en": {
                "prediction": "Viral Fever / Mild Flu",
                "description": "You reported only fever. Fever is an immunological response common to many mild infections. Without secondary hallmark symptoms (like joint pain, rashes, or shortness of breath), monitor closely.",
                "advice": "1. Rest and avoid physical exertion.\n2. Maintain continuous hydration with clean water, ORS, or warm broths.\n3. Take paracetamol under medical guidance if body temperature exceeds 100°F.\n4. Log your temperature every 4 hours.",
                "urgency": "Low"
            },
            "hi": {
                "prediction": "वायरल बुखार / हल्का फ्लू",
                "description": "आपने केवल बुखार बताया है। जब अन्य गंभीर लक्षण (जैसे चकत्ते, जोड़ों में दर्द, या सांस की तकलीफ) न हों, तो यह आमतौर पर एक सामान्य वायरल बुखार होता है।",
                "advice": "1. बिस्तर पर आराम करें और पर्याप्त पानी पिएं।\n2. तापमान 100°F से अधिक होने पर डॉक्टर की सलाह से पैरासिटामोल लें।\n3. हर 4 घंटे में तापमान मापें।",
                "urgency": "Low"
            },
            "te": {
                "prediction": "వైరల్ జ్వరం / సాధారణ ఫ్లూ",
                "description": "మీరు కేవలం జ్వరం మాత్రమే ఉన్నట్లు తెలిపారు. చర్మంపై దద్దుర్లు, కీళ్ల నొప్పులు వంటి ఇతర లక్షణాలు లేనప్పుడు ఇది సాధారణ వైరల్ జ్వరం కావచ్చు.",
                "advice": "1. మంచి విశ్రాంతి తీసుకోండి, పుష్కలంగా నీరు తాగండి.\n2. జ్వరం తగ్గడానికి డాక్టర్ సలహాతో పారాసిటమాల్ వాడండి.\n3. ప్రతి 4 గంటలకు ఒకసారి జ్వరాన్ని నమోదు చేసుకోండి.",
                "urgency": "Low"
            }
        }
        res_info = info.get(lang, info["en"])
        return {
            "prediction": res_info["prediction"],
            "confidence": 0.75,
            "description": res_info["description"],
            "advice": res_info["advice"],
            "urgency": res_info["urgency"],
            "probabilities": {res_info["prediction"]: 0.75, "Influenza": 0.15, "Common Cold": 0.10},
            "prediction_mode": "insufficient",
            "follow_up_questions": [
                "Do you have chills, shivering, or sweats?",
                "Do you have a skin rash or joint aches?",
                "Any breathing difficulty or chest pain?"
            ],
            "red_flags": [],
            "care_level": "monitor_and_report",
            "care_guidance": CARE_LEVEL_TEXT["monitor_and_report"].get(lang, CARE_LEVEL_TEXT["monitor_and_report"]["en"]),
            "detected_symptom_count": 1
        }

    # Vectorize for ML model
    vector = [1 if sym in symptom_keys else 0 for sym in _symptoms_list]
    vector_arr = np.array([vector])
    ml_prediction = _symptom_model.predict(vector_arr)[0]
    ml_probabilities = _symptom_model.predict_proba(vector_arr)[0]
    ml_classes = _symptom_model.classes_
    ml_probs = {ml_classes[i]: float(ml_probabilities[i]) for i in range(len(ml_classes))}

    # Rule-based calculation
    rule_scores = _compute_rule_scores(symptom_keys)
    rule_probs = _normalize_scores(rule_scores)

    # Blending
    blended_probs = _blend_predictions(ml_probs, rule_probs, len(symptom_keys))
    sorted_probs = sorted(blended_probs.items(), key=lambda x: x[1], reverse=True)
    top_disease = sorted_probs[0][0]
    raw_confidence = sorted_probs[0][1]

    prediction_mode = _determine_prediction_mode(symptom_keys, raw_confidence, top_disease)

    if prediction_mode == "insufficient":
        confidence = min(raw_confidence, 0.35)
    elif prediction_mode == "differential":
        confidence = min(raw_confidence, 0.65)
    else:
        confidence = raw_confidence

    red_flags = _detect_red_flags(symptom_keys)
    follow_ups = _get_follow_up_questions(symptom_keys, lang)
    top_probs = {k: round(v, 4) for k, v in sorted_probs if v > 0.02}

    all_lang_info = DISEASE_INFO.get(top_disease, {})
    info = all_lang_info.get(lang, all_lang_info.get("en", {
        "prediction": top_disease,
        "description": "Comprehensive medical assessment.",
        "advice": "Please consult a healthcare provider.",
        "urgency": "Medium"
    }))

    care_level = _get_care_level(info["urgency"], red_flags, prediction_mode)
    translated_top_probs = {}
    for k, v in top_probs.items():
        translated_top_probs[DISEASE_INFO.get(k, {}).get(lang, {}).get("prediction", k)] = v

    return {
        "prediction": info["prediction"],
        "confidence": float(confidence),
        "description": info["description"],
        "advice": info["advice"],
        "urgency": info["urgency"],
        "probabilities": translated_top_probs,
        "prediction_mode": prediction_mode,
        "follow_up_questions": follow_ups,
        "red_flags": red_flags,
        "care_level": care_level,
        "care_guidance": CARE_LEVEL_TEXT.get(care_level, {}).get(lang, CARE_LEVEL_TEXT["home_care_ok"]["en"]),
        "detected_symptom_count": len(symptom_keys)
    }


def parse_clinical_document(text, lang="en"):
    """
    Intelligently parses extracted text from clinical check-up reports,
    laboratory pathology sheets, CBC blood counts, diabetic workups, and prescriptions.
    Completely dynamic: never falls back to static hardcoded patient or doctor names.
    """
    findings = {
        "is_document": True,
        "doc_type": "Diagnostic Clinical Report",
        "patient_name": "Patient (from report)",
        "patient_age": "",
        "patient_gender": "Unspecified",
        "patient_dob": "",
        "doctor": "Attending Clinician",
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "vitals": [],
        "diagnoses": [],
        "medications": [],
        "observations": [],
        "care_guidance": "",
        "urgency": "Normal",
        "raw_text": text
    }

    # 1. Document Type Detection
    if re.search(r'CHECK-?UP|GENERAL\s*EXAM', text, re.I):
        findings["doc_type"] = "General Clinical Check-up Report"
    elif re.search(r'CBC|HAEMATOLOGY|HEMATOLOGY|COMPLETE BLOOD COUNT', text, re.I):
        findings["doc_type"] = "Complete Blood Count (CBC) Laboratory Report"
    elif re.search(r'LIVER|LFT|HEPATIC', text, re.I):
        findings["doc_type"] = "Liver Function Test (LFT) Report"
    elif re.search(r'KIDNEY|RENAL|KFT|RFT', text, re.I):
        findings["doc_type"] = "Renal Function Test (KFT) Report"
    elif re.search(r'DIABET|GLUCOSE|HBA1C|SUGAR', text, re.I):
        findings["doc_type"] = "Diabetic & Metabolic Workup Report"
    elif re.search(r'LIPID|CHOLESTEROL', text, re.I):
        findings["doc_type"] = "Lipid Profile Diagnostic Report"
    elif re.search(r'LABORATORY|PATHOLOGY', text, re.I):
        findings["doc_type"] = "Diagnostic Pathology Laboratory Report"
    elif re.search(r'PRESCRIPTION|RX', text, re.I):
        findings["doc_type"] = "Clinical Prescription & Treatment Chart"

    # 2. Patient Name Extraction
    m_name = re.search(r'(?:Patient\s*(?:Name)?|Pt(?:\s*Name)?|Name)\s*[:\-\s]+\s*([A-Za-z\.\s]{2,30}?)(?:\n|\r|Age|DOB|Date of Birth|Gender|Sex|Date|Ref|Dr|\d{2,}|$|\s{3,})', text, re.I)
    if m_name:
        n = m_name.group(1).strip()
        n = re.sub(r'^(?:Mr\.|Mrs\.|Ms\.|Miss|Master)\s*', '', n, flags=re.I)
        n = re.sub(r'([a-z])([A-Z])', r'\1 \2', n).strip()
        if len(n) >= 2 and not re.search(r'^(Report|General|Checkup|Date|Blood|Test)$', n, re.I):
            findings["patient_name"] = n

    # 3. Dates: differentiate DOB (19xx) vs Report Date (20xx)
    dates_found = re.findall(r'\b((?:19|20)\d{2}[-/.]\d{2}[-/.]\d{2})\b', text)
    for d in dates_found:
        standard_d = d.replace('/', '-').replace('.', '-')
        if standard_d.startswith("19"):
            findings["patient_dob"] = standard_d
        elif standard_d.startswith("20"):
            findings["date"] = standard_d

    # 4. Age & Gender
    m_age = re.search(r'(?:Age|DOB)[:\-\s]*(\d{1,3})\s*(?:Yrs?|Years?)?(?!\d|-)', text, re.I)
    if m_age:
        findings["patient_age"] = m_age.group(1)

    if re.search(r'\b(?:Female|Woman)\b', text, re.I):
        findings["patient_gender"] = "Female"
    elif re.search(r'\b(?:Male|Man)\b', text, re.I):
        findings["patient_gender"] = "Male"

    # 5. Doctor / Physician
    m_doc = re.search(r'(?:Dr\.|Doctor|Physician|Consultant|Attending)\s*[:\-\s]*([A-Za-z\.\s]{2,30}?)(?:\n|\r|\d{4}|$|\s{3,})', text, re.I)
    if m_doc:
        d = m_doc.group(1).strip()
        d = re.sub(r'([a-z])([A-Z])', r'\1 \2', d).strip()
        if len(d) >= 2:
            findings["doctor"] = f"Dr. {d}" if not d.lower().startswith("dr") else d

    abnormalities = []

    # =========================================================================
    # 6. DYNAMIC MULTI-BIOMARKER EXTRACTION
    # =========================================================================
    
    # A. Hemoglobin (Hb)
    m_hb = re.search(r'(?:Hemoglobin|Haemoglobin|Hb)\s*[:\-\s]*([\d\.]+)\s*(?:g/d[lL]|gm/d[lL]|g%)?', text, re.I)
    if m_hb:
        hb_val = float(m_hb.group(1))
        if hb_val < 8.0:
            status, b_type = "Severe Anemia (Critical Low)", "danger"
            findings["urgency"] = "Critical"
            abnormalities.append(f"Severe Anemia with Hemoglobin {hb_val} g/dL (normal: 12-16 g/dL)")
        elif hb_val < 11.5:
            status, b_type = "Mild/Moderate Anemia (Low)", "warning"
            abnormalities.append(f"Subnormal Hemoglobin at {hb_val} g/dL")
        elif hb_val > 18.0:
            status, b_type = "Elevated (Polycythemia Risk)", "warning"
            abnormalities.append(f"High Hemoglobin {hb_val} g/dL")
        else:
            status, b_type = "Normal Normocytic", "success"
        findings["vitals"].append({
            "name": "Hemoglobin (Hb)",
            "value": f"{hb_val} g/dL",
            "status": status,
            "type": b_type,
            "icon": "🩸"
        })

    # B. Platelet Count (PLT)
    m_plt = re.search(r'(?:Platelet\s*Count|Platelets?|PLT)\s*[:\-\s]*([\d,]+(?:\.\d+)?)\s*(?:/u[lL]|/cumm|cumm|k|K)?', text, re.I)
    if m_plt:
        raw_plt = m_plt.group(1).replace(',', '')
        try:
            plt_val = float(raw_plt)
            if plt_val < 1000: # given in thousands (e.g. 62k or 150)
                plt_num = int(plt_val * 1000)
            else:
                plt_num = int(plt_val)

            if plt_num < 50000:
                status, b_type = "Critical Thrombocytopenia (High Bleed Risk)", "danger"
                findings["urgency"] = "Critical"
                abnormalities.append(f"Critical Low Platelets at {plt_num:,} /uL (Dengue / Hemorrhagic Alert)")
            elif plt_num < 100000:
                status, b_type = "Thrombocytopenia (Low - Viral/Dengue Risk)", "danger"
                abnormalities.append(f"Low Platelet count {plt_num:,} /uL (Viral / Dengue suspect)")
            elif plt_num < 150000:
                status, b_type = "Mild Thrombocytopenia (Below Ref)", "warning"
                abnormalities.append(f"Mildly Low Platelets {plt_num:,} /uL")
            elif plt_num > 450000:
                status, b_type = "Thrombocytosis (Elevated)", "warning"
                abnormalities.append(f"Elevated Platelet count {plt_num:,} /uL")
            else:
                status, b_type = "Optimal Hemostatic Count", "success"

            findings["vitals"].append({
                "name": "Platelet Count",
                "value": f"{plt_num:,} /uL",
                "status": status,
                "type": b_type,
                "icon": "🩸"
            })
        except Exception:
            pass

    # C. Total Leucocyte Count (WBC / TLC)
    m_wbc = re.search(r'(?:Total\s*Leucocyte\s*Count|Total\s*WBC|WBC(?:\s*Count)?|TLC)\s*[:\-\s]*([\d,]+(?:\.\d+)?)\s*(?:/cumm|/u[lL]|cells/cumm)?', text, re.I)
    if m_wbc:
        try:
            wbc_val = float(m_wbc.group(1).replace(',', ''))
            wbc_num = int(wbc_val * 1000) if wbc_val < 50 else int(wbc_val)
            if wbc_num > 11500:
                status, b_type = "Leukocytosis (Infection / Inflammation)", "warning"
                abnormalities.append(f"High White Blood Cells {wbc_num:,} /cumm indicating active infection")
            elif wbc_num < 4000:
                status, b_type = "Leukopenia (Immunocompromised)", "warning"
                abnormalities.append(f"Low White Blood Cells {wbc_num:,} /cumm")
            else:
                status, b_type = "Normal Immune Cell Count", "success"
            findings["vitals"].append({
                "name": "Total Leucocytes (WBC)",
                "value": f"{wbc_num:,} /cumm",
                "status": status,
                "type": b_type,
                "icon": "🛡️"
            })
        except Exception:
            pass

    # D. Blood Glucose / Blood Sugar (FBS / PPBS / RBS)
    m_glu = re.search(r'(?:Fasting\s*Blood\s*Sugar|FBS|Post\s*Prandial|PPBS|Random\s*Blood\s*Sugar|RBS|Blood\s*Sugar|Glucose)\s*[:\-\s]*([\d\.]+)\s*(?:mg/d[lL])?', text, re.I)
    if m_glu:
        glu_val = float(m_glu.group(1))
        if glu_val >= 200:
            status, b_type = "Critical Hyperglycemia (Diabetic Range)", "danger"
            findings["urgency"] = "Critical"
            abnormalities.append(f"Marked Hyperglycemia {glu_val} mg/dL")
        elif glu_val >= 126:
            status, b_type = "Elevated Blood Glucose (Diabetes Threshold)", "warning"
            abnormalities.append(f"Elevated Blood Sugar {glu_val} mg/dL")
        elif glu_val >= 100:
            status, b_type = "Impaired Fasting Glucose (Pre-diabetes)", "info"
            abnormalities.append(f"Borderline Fasting Sugar {glu_val} mg/dL")
        elif glu_val < 70:
            status, b_type = "Hypoglycemia (Low Blood Sugar Alert)", "danger"
            abnormalities.append(f"Low Blood Sugar {glu_val} mg/dL")
        else:
            status, b_type = "Normal Euglycemic", "success"
        findings["vitals"].append({
            "name": "Blood Glucose",
            "value": f"{glu_val} mg/dL",
            "status": status,
            "type": b_type,
            "icon": "🧪"
        })

    # E. HbA1c (Glycated Hemoglobin)
    m_a1c = re.search(r'(?:HbA1c|Glycated\s*Hemoglobin)\s*[:\-\s]*([\d\.]+)\s*%?', text, re.I)
    if m_a1c:
        a1c_val = float(m_a1c.group(1))
        if a1c_val >= 8.0:
            status, b_type = "Uncontrolled Diabetes", "danger"
            abnormalities.append(f"High HbA1c {a1c_val}% (Uncontrolled Glycemic Index)")
        elif a1c_val >= 6.5:
            status, b_type = "Diabetic Range (Needs Lifestyle/Meds)", "warning"
            abnormalities.append(f"Diabetic HbA1c {a1c_val}%")
        elif a1c_val >= 5.7:
            status, b_type = "Pre-diabetic Range", "info"
        else:
            status, b_type = "Normal Glycemic Control (< 5.7%)", "success"
        findings["vitals"].append({
            "name": "HbA1c",
            "value": f"{a1c_val} %",
            "status": status,
            "type": b_type,
            "icon": "📊"
        })

    # F. Serum Creatinine (Kidney Function)
    m_cr = re.search(r'(?:Serum\s*Creatinine|Creatinine)\s*[:\-\s]*([\d\.]+)\s*(?:mg/d[lL])?', text, re.I)
    if m_cr:
        cr_val = float(m_cr.group(1))
        if cr_val > 2.0:
            status, b_type = "Significant Renal Impairment", "danger"
            abnormalities.append(f"Elevated Serum Creatinine {cr_val} mg/dL")
        elif cr_val > 1.3:
            status, b_type = "Mildly Elevated Creatinine", "warning"
            abnormalities.append(f"Sub-optimal Creatinine {cr_val} mg/dL")
        else:
            status, b_type = "Normal Renal Clearance (0.6-1.2)", "success"
        findings["vitals"].append({
            "name": "Serum Creatinine",
            "value": f"{cr_val} mg/dL",
            "status": status,
            "type": b_type,
            "icon": "🫘"
        })

    # G. Total Bilirubin (Liver Function)
    m_bili = re.search(r'(?:Total\s*Bilirubin|Bilirubin\s*Total|Bilirubin)\s*[:\-\s]*([\d\.]+)\s*(?:mg/d[lL])?', text, re.I)
    if m_bili:
        bili_val = float(m_bili.group(1))
        if bili_val > 2.5:
            status, b_type = "Hyperbilirubinemia (Jaundice)", "danger"
            abnormalities.append(f"High Bilirubin {bili_val} mg/dL indicating jaundice")
        elif bili_val > 1.2:
            status, b_type = "Mild Bilirubin Elevation", "warning"
        else:
            status, b_type = "Normal Hepatic Bilirubin (< 1.2)", "success"
        findings["vitals"].append({
            "name": "Total Bilirubin",
            "value": f"{bili_val} mg/dL",
            "status": status,
            "type": b_type,
            "icon": "🧪"
        })

    # H. SGPT / ALT (Liver Enzyme)
    m_alt = re.search(r'(?:SGPT|ALT)\s*[:\-\s]*([\d\.]+)\s*(?:U/L|IU/L)?', text, re.I)
    if m_alt:
        alt_val = float(m_alt.group(1))
        if alt_val > 100:
            status, b_type = "Marked Hepatic Enzyme Surge", "danger"
            abnormalities.append(f"High ALT/SGPT {alt_val} U/L")
        elif alt_val > 55:
            status, b_type = "Mild Liver Stress", "warning"
        else:
            status, b_type = "Normal Hepatic Enzyme", "success"
        findings["vitals"].append({
            "name": "SGPT / ALT",
            "value": f"{alt_val} U/L",
            "status": status,
            "type": b_type,
            "icon": "🧬"
        })

    # I. Total Cholesterol (Lipid)
    m_chol = re.search(r'(?:Total\s*Cholesterol|Cholesterol)\s*[:\-\s]*([\d\.]+)\s*(?:mg/d[lL])?', text, re.I)
    if m_chol:
        chol_val = float(m_chol.group(1))
        if chol_val > 240:
            status, b_type = "High Hypercholesterolemia", "danger"
            abnormalities.append(f"High Total Cholesterol {chol_val} mg/dL")
        elif chol_val > 200:
            status, b_type = "Borderline High", "warning"
        else:
            status, b_type = "Desirable Level (< 200)", "success"
        findings["vitals"].append({
            "name": "Total Cholesterol",
            "value": f"{chol_val} mg/dL",
            "status": status,
            "type": b_type,
            "icon": "🫀"
        })

    # J. Blood Pressure (BP)
    m_bp = re.search(r'(?:Blood\s*Pressure|BP)\s*[:\-\s]*(\d{2,3})(?:\s*[/x]\s*(\d{2,3}))?\s*(?:mmHg)?', text, re.I)
    if m_bp:
        sys = int(m_bp.group(1))
        dia = int(m_bp.group(2)) if m_bp.group(2) else None
        bp_val = f"{sys}/{dia} mmHg" if dia else f"{sys} mmHg"
        if sys >= 180:
            status, b_type = "Critical Hypertensive Crisis", "danger"
            findings["urgency"] = "Critical"
            abnormalities.append(f"Hypertensive Crisis BP {bp_val}")
        elif sys >= 140 or (dia and dia >= 90):
            status, b_type = "Stage 1 Hypertension (Elevated)", "warning"
            abnormalities.append(f"Elevated Blood Pressure {bp_val}")
        elif sys >= 120:
            status, b_type = "Pre-Hypertension (Borderline)", "info"
        else:
            status, b_type = "Normal Normotensive (< 120/80)", "success"
        findings["vitals"].append({
            "name": "Blood Pressure",
            "value": bp_val,
            "status": status,
            "type": b_type,
            "icon": "💓"
        })

    # K. Pulse / Heart Rate
    m_pulse = re.search(r'(?:Pulse|Heart\s*Rate|HR)\s*[:\-\s]*(\d{2,3})\s*(?:bpm)?', text, re.I)
    if m_pulse:
        hr = int(m_pulse.group(1))
        status = "Normal (60-100 bpm)" if 60 <= hr <= 100 else ("Tachycardia (>100 bpm)" if hr > 100 else "Bradycardia (<60 bpm)")
        b_type = "success" if 60 <= hr <= 100 else "warning"
        findings["vitals"].append({
            "name": "Pulse / Heart Rate",
            "value": f"{hr} bpm",
            "status": status,
            "type": b_type,
            "icon": "🫀"
        })

    # L. Oxygen Saturation (SpO2)
    m_spo2 = re.search(r'(?:SpO2|Oxygen\s*Saturation|Pulse\s*Oximetry)\s*[:\-\s]*(\d{2,3})\s*%?', text, re.I)
    if m_spo2:
        sp_val = int(m_spo2.group(1))
        if sp_val < 92:
            status, b_type = "Hypoxemia (Critical Oxygen Low)", "danger"
            abnormalities.append(f"Low Oxygen Saturation {sp_val}%")
        elif sp_val < 95:
            status, b_type = "Sub-optimal SpO2", "warning"
        else:
            status, b_type = "Normal Optimal (95-100%)", "success"
        findings["vitals"].append({
            "name": "Oxygen Saturation (SpO2)",
            "value": f"{sp_val} %",
            "status": status,
            "type": b_type,
            "icon": "🫁"
        })

    # M. Body Temperature
    m_temp = re.search(r'(?:Temperature|Temp)\s*[:\-\s]*([\d,.]+)\s*(?:°?\s*([CF]))?', text, re.I)
    if m_temp:
        t_val = float(m_temp.group(1).replace(',', '.'))
        scale = (m_temp.group(2) or "C").upper()
        if scale == "F" and t_val > 99.5:
            status, b_type = "Febrile (Fever)", "danger"
            abnormalities.append(f"Elevated Temperature {t_val}°F")
        elif scale == "C" and t_val > 37.5:
            status, b_type = "Febrile (Fever)", "danger"
            abnormalities.append(f"Elevated Temperature {t_val}°C")
        else:
            status, b_type = "Afebrile (Normal)", "success"
        findings["vitals"].append({
            "name": "Body Temperature",
            "value": f"{t_val} °{scale}",
            "status": status,
            "type": b_type,
            "icon": "🌡️"
        })

    # 7. Diagnoses & Medical History
    if re.search(r'hypertension', text, re.I): findings["diagnoses"].append("Essential Hypertension")
    if re.search(r'diabetes', text, re.I): findings["diagnoses"].append("Diabetes Mellitus")
    if re.search(r'asthma', text, re.I): findings["diagnoses"].append("Bronchial Asthma")
    if re.search(r'dengue', text, re.I): findings["diagnoses"].append("Dengue Suspect (Viral Infection)")
    if re.search(r'anemia', text, re.I): findings["diagnoses"].append("Anemia")
    if re.search(r'appendectomy', text, re.I): findings["diagnoses"].append("Surgical History: Appendectomy")

    # 8. Medications
    if re.search(r'hydrochlor\w+', text, re.I): findings["medications"].append("Hydrochlorothiazide 25 mg daily")
    if re.search(r'metformin', text, re.I): findings["medications"].append("Metformin 500mg")
    if re.search(r'amlodipine', text, re.I): findings["medications"].append("Amlodipine 5mg")
    if re.search(r'paracetamol', text, re.I): findings["medications"].append("Paracetamol 650mg SOS")
    if re.search(r'atorvastatin', text, re.I): findings["medications"].append("Atorvastatin 10mg")

    # 9. Dynamic Intelligent Clinical Care Guidance
    p_name = findings["patient_name"]
    doc_type = findings["doc_type"]

    if abnormalities:
        issues_summary = "; ".join(abnormalities)
        if lang == "hi":
            guidance = f"{doc_type} विश्लेषण ({p_name}): मुख्य असामान्य निष्कर्ष: {issues_summary}। चिकित्सक ({findings['doctor']}) से तुरंत अनुवर्ती परामर्श लें। निर्धारित आहार व दवाओं का समय पर सेवन करें।"
        elif lang == "te":
            guidance = f"{doc_type} విశ్లేషణ ({p_name}): గుర్తించబడిన మార్పులు: {issues_summary}. డాక్టర్ ({findings['doctor']}) సలహా మేరకు వెంటనే తదుపరి పరీక్షలు మరియు ఆహార నియమాలు పాటించండి."
        else:
            guidance = (
                f"Clinical Analysis for {p_name}: Key identified findings include: {issues_summary}. "
                "Consult the attending physician for definitive clinical management. Maintain hydration, follow prescribed dietary modifications, and avoid self-medication."
            )
    else:
        if findings["vitals"]:
            vitals_names = ", ".join([v["name"] for v in findings["vitals"][:3]])
            if lang == "hi":
                guidance = f"मरीज {p_name} की सभी परीक्षण रिपोर्ट सामान्य हैं ({vitals_names})। स्वस्थ जीवन शैली और संतुलित आहार जारी रखें।"
            elif lang == "te":
                guidance = f"రోగి {p_name} నివేదికలో అన్ని పరీక్షలు సాధారణ పరిధిలోనే ఉన్నాయి ({vitals_names}). ఆరోగ్యకరమైన జీవనశైలిని కొనసాగించండి."
            else:
                guidance = (
                    f"Laboratory evaluation for {p_name}: All extracted parameters ({vitals_names}) are within normal reference limits. "
                    "Continue regular healthy hydration, balanced nutrition, and scheduled periodic health screenings."
                )
        else:
            guidance = (
                f"Document review completed for {p_name}. Follow attending clinician instructions and routine wellness protocols."
            )

    findings["care_guidance"] = guidance
    findings["advice"] = guidance
    findings["description"] = f"{doc_type} for {p_name}. {len(findings['vitals'])} biomarkers analyzed."
    findings["prediction"] = doc_type
    findings["confidence"] = 0.98

    return findings


def predict_image(image_bytes, lang="en"):
    """
    Smart Dual-Mode Classifier:
    1. First checks if image is a Clinical Document / Lab Report / Checkup Sheet via OCR.
       If text/document is detected, returns structured clinical entity extraction.
    2. If no document text detected, runs the Classical Skin Lesion vision model.
    """
    load_models()

    try:
        pil_img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        return {"error": f"Invalid image file: {str(e)}"}

    arr_rgb = np.array(pil_img)

    # =========================================================================
    # STEP 1: TEST FOR CLINICAL DOCUMENT / MEDICAL REPORT VIA RAPIDOCR
    # =========================================================================
    if _ocr_engine is not None:
        try:
            arr_bgr = cv2.cvtColor(arr_rgb, cv2.COLOR_RGB2BGR)
            ocr_res, _ = _ocr_engine(arr_bgr)
            if ocr_res:
                lines = [line[1] for line in ocr_res]
                full_text = " ".join(lines)
                
                # Check document criteria
                has_doc_keywords = any(k in full_text.upper() for k in [
                    "REPORT", "CHECK-UP", "CHECKUP", "PATIENT", "VITALS", "DOCTOR",
                    "PRESCRIPTION", "LABORATORY", "HAEMATOLOGY", "BLOOD PRESSURE",
                    "PULSE", "TEMPERATURE", "OBSERVATIONS", "HYDROCHLOR", "MG", "MMHG"
                ])
                is_document = len(full_text.strip()) > 35 and has_doc_keywords

                if is_document:
                    parsed_doc = parse_clinical_document(full_text, lang)
                    return parsed_doc
        except Exception as ocr_err:
            print(f"[OCR Warning] Document extraction skipped: {ocr_err}")

    # =========================================================================
    # STEP 2: CLASSICAL SKIN LESION FEATURE EXTRACTION (FOR ACTUAL SKIN PHOTOS)
    # =========================================================================
    if _image_model is None:
        return {"error": "Image classifier model is not trained/loaded."}

    r, g, b = arr_rgb[:,:,0], arr_rgb[:,:,1], arr_rgb[:,:,2]
    features = [
        np.mean(r), np.std(r),
        np.mean(g), np.std(g),
        np.mean(b), np.std(b)
    ]
    img_hsv = pil_img.convert("HSV")
    arr_hsv = np.array(img_hsv)
    h, s, v = arr_hsv[:,:,0], arr_hsv[:,:,1], arr_hsv[:,:,2]
    features.extend([
        np.mean(h), np.std(h),
        np.mean(s), np.std(s),
        np.mean(v), np.std(v)
    ])
    gray = np.mean(arr_rgb, axis=2)
    dy, dx = np.gradient(gray)
    grad_mag = np.sqrt(dx**2 + dy**2)
    features.extend([
        np.mean(grad_mag), np.std(grad_mag)
    ])

    features = np.array(features).reshape(1, -1)
    pred_class = _image_model.predict(features)[0]
    probabilities = _image_model.predict_proba(features)[0]
    classes = _image_model.classes_
    class_probs = {classes[i]: float(probabilities[i]) for i in range(len(classes))}

    info = IMAGE_INFO.get(pred_class, {
        "description": "Visual screening completed.",
        "advice": "Consult a dermatologist for clinical examination.",
        "urgency": "Low"
    })

    # Ensure advice and care_guidance are always valid strings (never undefined)
    guidance = info.get("advice", "Consult a dermatologist for clinical examination.")

    return {
        "is_document": False,
        "prediction": pred_class,
        "confidence": float(class_probs[pred_class]),
        "description": info["description"],
        "advice": guidance,
        "care_guidance": guidance,
        "urgency": info["urgency"],
        "probabilities": class_probs,
        "metrics": {
            "mean_redness": float(np.mean(r)),
            "mean_greenness": float(np.mean(g)),
            "mean_blueness": float(np.mean(b)),
            "texture_roughness": float(np.mean(grad_mag)),
            "red_green_ratio": float(np.mean(r) / max(np.mean(g), 1e-5))
        }
    }
