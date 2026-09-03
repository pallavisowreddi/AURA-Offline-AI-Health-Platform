import os
import pickle
import re
import numpy as np
from PIL import Image
import io

# Paths to models
SYMPTOM_MODEL_PATH = "models/symptom_model.pkl"
SYMPTOMS_LIST_PATH = "models/symptoms_list.pkl"
IMAGE_MODEL_PATH = "models/image_model.pkl"

# Initialize caches
_symptom_model = None
_symptoms_list = None
_image_model = None

# Multilingual Symptom Vocabularies
SYMPTOM_VOCAB = {
    "en": {
        "fever": ["fever", "high temp", "temperature", "feverish", "hot body"],
        "cough": ["cough", "coughing", "dry cough", "throat cough"],
        "fatigue": ["fatigue", "tired", "exhausted", "weakness", "lethargy", "sleepy"],
        "headache": ["headache", "head pain", "throbbing head", "migraine ache"],
        "sore_throat": ["sore throat", "throat pain", "throat irritation", "swallowing pain"],
        "body_ache": ["body ache", "body pain", "muscle pain", "body aches", "muscle ache"],
        "runny_nose": ["runny nose", "congested", "congestion", "blocked nose", "nasal blockage", "sneezing nose"],
        "shortness_of_breath": ["shortness of breath", "breathless", "difficulty breathing", "breathing issue"],
        "loss_of_taste_smell": ["loss of taste", "loss of smell", "cannot taste", "cannot smell", "taste loss"],
        "nausea": ["nausea", "nauseous", "feeling sick", "vomit sensation"],
        "vomiting": ["vomiting", "vomit", "throw up", "vomited"],
        "diarrhea": ["diarrhea", "loose motion", "watery stool", "motions"],
        "stomach_pain": ["stomach pain", "stomach ache", "tummy ache", "abdominal pain"],
        "rash": ["rash", "skin rash", "spots", "red spots"],
        "itching": ["itching", "itch", "itchy", "scratching"],
        "dry_skin": ["dry skin", "flaky skin", "skin dryness"],
        "skin_redness": ["redness", "red skin", "inflammation", "skin red"],
        "blisters": ["blisters", "blister", "fluid-filled bumps", "bubbles on skin"],
        "joint_pain": ["joint pain", "joint ache", "pain in joints", "knee pain"],
        "muscle_weakness": ["muscle weakness", "weak muscles", "limb weakness"],
        "chills": ["chills", "cold shivers", "shivering", "feeling cold"],
        "sweating": ["sweating", "night sweats", "excessive sweat", "sweat"],
        "sneezing": ["sneezing", "sneeze", "sneezed"],
        "itchy_eyes": ["itchy eyes", "watery eyes", "red eyes", "eye irritation"]
    },
    "hi": { # Hindi
        "fever": ["बुखार", "ज्वर", "bukhar", "jwar", "tapman"],
        "cough": ["खांसी", "खाँसी", "khansi", "khokho"],
        "fatigue": ["थकान", "कमजोरी", "thakan", "kamzori", "alas"],
        "headache": ["सिरदर्द", "सर दर्द", "sir dard", "sir dukhna"],
        "sore_throat": ["गले में खराश", "गला खराब", "gale me kharash", "gala dard"],
        "body_ache": ["बदन दर्द", "शरीर में दर्द", "badan dard", "darad"],
        "runny_nose": ["बहती नाक", "नाक बहना", "naak behna", "naak band"],
        "shortness_of_breath": ["सांस की कमी", "सांस फूलना", "sans phulna", "saans lene me taklif"],
        "loss_of_taste_smell": ["स्वाद का जाना", "गंध का जाना", "swad chale jana", "sungna khona"],
        "nausea": ["जी मिचलाना", "उल्टी जैसा लगना", "jee michlana", "ulti jaisa"],
        "vomiting": ["उल्टी", "वमन", "ulti", "vomit"],
        "diarrhea": ["दस्त", "पेचिश", "dast", "loose motion"],
        "stomach_pain": ["पेट दर्द", "पेट में दर्द", "pet dard", "tummy dard"],
        "rash": ["चकत्ते", "लाल निशान", "skin rash", "chakte"],
        "itching": ["खुजली", "खारिश", "khujli", "khujlane"],
        "dry_skin": ["रूखी त्वचा", "सूखी चमड़ी", "dry skin", "rukhi twacha"],
        "skin_redness": ["त्वचा की लालिमा", "लाल त्वचा", "laal skin", "laal chakte"],
        "blisters": ["छाले", "फोड़े", "chhale", "phore"],
        "joint_pain": ["जोड़ों का दर्द", "घुटनों का दर्द", "jodon ka dard", "joint dard"],
        "muscle_weakness": ["मांसपेशियों की कमजोरी", "manspeshi kamzori"],
        "chills": ["कंपकंपी", "ठंड लगना", "thand lagna", "kampkampi"],
        "sweating": ["पसीना आना", "pasina ana", "pasina"],
        "sneezing": ["छींकना", "छींक", "chheenk", "chink"],
        "itchy_eyes": ["आंँखों में खुजली", "aankhon me khujli", "aankh laal"]
    },
    "te": { # Telugu
        "fever": ["జ్వరం", "jwaram", "jvara"],
        "cough": ["దగ్గు", "daggu"],
        "fatigue": ["అలసట", "నీరసం", "alasata", "neerasam", "nirasam"],
        "headache": ["తలనొప్పి", "tala noppi", "talanopii"],
        "sore_throat": ["గొంతు నొప్పి", "gontu noppi", "gontu kharash"],
        "body_ache": ["ఒళ్ళు నొప్పులు", "ollu noppulu", "body noppulu"],
        "runny_nose": ["జలుబు", "ముక్కు కారడం", "jalubu", "mukku karadam"],
        "shortness_of_breath": ["ఆయాసం", "శ్వాస ఆడకపోవడం", "aayasam", "swasa taklif"],
        "loss_of_taste_smell": ["రుచి కోల్పోవడం", "వాసన కోల్పోవడం", "ruchi lekapovadam", "vasana povadam"],
        "nausea": ["కడుపులో తిప్పడం", "వాంతి వచ్చేలా ఉండటం", "vanti vachinattu"],
        "vomiting": ["వాంతులు", "vanthulu", "vanti"],
        "diarrhea": ["విరేచనాలు", "virechanalu", "bhedulu"],
        "stomach_pain": ["కడుపు నొప్పి", "kadupu noppi"],
        "rash": ["దద్దుర్లు", "skin rash", "daddurlu"],
        "itching": ["దురద", "durada"],
        "dry_skin": ["పొడి చర్మం", "podi charmam"],
        "skin_redness": ["చర్మం ఎర్రబడటం", "charmam erra badadam"],
        "blisters": ["పొక్కులు", "pokkulu"],
        "joint_pain": ["కీళ్ల నొప్పులు", "keella noppulu", "knees noppulu"],
        "muscle_weakness": ["కండరాల బలహీనత", "kandarala balaheenatha"],
        "chills": ["చలి", "chali lagadam"],
        "sweating": ["చెమటలు", "chematalu"],
        "sneezing": ["తుమ్ములు", "tummulu"],
        "itchy_eyes": ["కళ్ళు దురద పెట్టడం", "kallu durada"]
    },
    "ta": { # Tamil
        "fever": ["காய்ச்சல்", "kayachal", "suram"],
        "cough": ["இருமல்", "irumal"],
        "fatigue": ["சோர்வு", "s थकan", "sorvu", "balaheenam"],
        "headache": ["தலைவலி", "thalai vali", "thalaivali"],
        "sore_throat": ["தொண்டை வலி", "thondai vali", "thondai erachal"],
        "body_ache": ["உடல் வலி", "udal vali"],
        "runny_nose": ["சளி", "மூக்கு ஒழுகுதல்", "sali", "mooku oluguthal"],
        "shortness_of_breath": ["மூச்சுத்திணறல்", "moochu thinarel", "moochu kashtam"],
        "loss_of_taste_smell": ["சுவை இழப்பு", "வாசனை இழப்பு", "suvai ilappu", "vasanai ilappu"],
        "nausea": ["குமட்டல்", "kumattal"],
        "vomiting": ["வாந்தி", "vanthi", "vaanthi"],
        "diarrhea": ["வயிற்றுப்போக்கு", "vayitru pokku", "bedhi"],
        "stomach_pain": ["வயிற்று வலி", "vayitru vali"],
        "rash": ["தடிப்பு", "thadippu", "sivappu thadumbal"],
        "itching": ["அரிப்பு", "arippu"],
        "dry_skin": ["வறண்ட சருமம்", "varanda sarumam"],
        "skin_redness": ["சரும சிவத்தல்", "saruma sivappu"],
        "blisters": ["கொப்புளங்கள்", "koppulangal"],
        "joint_pain": ["மூட்டு வலி", "moottu vali"],
        "muscle_weakness": ["தச பலவீனம்", "thasa balaheenam"],
        "chills": ["நடுக்கம்", "chali", "nadukkam"],
        "sweating": ["வியர்வை", "viyarvai"],
        "sneezing": ["தும்மல்", "thummal"],
        "itchy_eyes": ["கண் அரிப்பு", "kan arippu"]
    },
    "bn": { # Bengali
        "fever": ["জ্বর", "jwor", "jwar"],
        "cough": ["কাশি", "kashi", "keshe"],
        "fatigue": ["ক্লান্তি", "দুর্বলতা", "klanti", "durbolota"],
        "headache": ["মাথাব্যথা", "mathavyatha", "matha betha"],
        "sore_throat": ["গলা ব্যথা", "gola betha", "gola khashkhash"],
        "body_ache": ["গা ব্যথা", "শরীর ব্যথা", "ga betha", "shorir betha"],
        "runny_nose": ["সর্দি", "নাক দিয়ে জল পড়া", "sordi", "nak jol"],
        "shortness_of_breath": ["হাঁফানি", "শ্বাসকষ্ট", "shash kosto", "shas kosto"],
        "loss_of_taste_smell": ["স্বাদ চলে যাওয়া", "গন্ধ না পাওয়া", "shad nai", "gondho nai"],
        "nausea": ["বমি বমি ভাব", "bomi bomi bhab"],
        "vomiting": ["বমি", "bomi"],
        "diarrhea": ["পাতলা পায়খানা", "ডায়রিয়া", "patla paikhana", "diarrhea"],
        "stomach_pain": ["পেট ব্যথা", "pet betha"],
        "rash": ["র‍্যাশ", "লাল দাগ", "rash", "laal chakti"],
        "itching": ["চুলকানি", "chulkani", "khushki"],
        "dry_skin": ["খসখসে ত্বক", "shukno twach"],
        "skin_redness": ["ত্বক লাল হওয়া", "laal chamra"],
        "blisters": ["ফোস্কা", "phoska", "foshka"],
        "joint_pain": ["গাঁটে ব্যথা", "হাড়ের জয়েন্টে ব্যথা", "gate betha"],
        "muscle_weakness": ["পেশীর দুর্বলতা", "peshir durbolota"],
        "chills": ["কাঁপুনি", "শীত লাগা", "kapuni", "shit laga"],
        "sweating": ["ঘাম হওয়া", "gham"],
        "sneezing": ["হাঁচি", "hachi"],
        "itchy_eyes": ["চোখ চুলকানো", "chokh chulkani"]
    },
    "ko": { # Korean
        "fever": ["열", "고열", "yeol", "fever"],
        "cough": ["기침", "gichim", "cough"],
        "fatigue": ["피로", "피곤", "piro", "pigon", "weakness"],
        "headache": ["두통", "머리 아픔", "dutong", "head pain"],
        "sore_throat": ["목 통증", "목 아픔", "mok apum", "throat pain"],
        "body_ache": ["몸살", "근육통", "momsal", "geunyuktong"],
        "runny_nose": ["콧물", "코막힘", "kotmul", "komakhim"],
        "shortness_of_breath": ["숨가쁨", "호흡 곤란", "sumgabeum", "breathless"],
        "loss_of_taste_smell": ["미각 상실", "후각 상실", "taste loss", "smell loss"],
        "nausea": ["메스꺼움", "속 울렁거림", "nausea", "ulleong"],
        "vomiting": ["구토", "토함", "guto", "vomit"],
        "diarrhea": ["설사", "seolsa", "diarrhea"],
        "stomach_pain": ["복통", "배 아픔", "boktong", "stomach pain"],
        "rash": ["발진", "피부 발진", "baljin", "rash"],
        "itching": ["가려움", "피부 가려움", "garyeoum", "itch"],
        "dry_skin": ["건조한 피부", "건성 피부", "dry skin"],
        "skin_redness": ["피부 붉어짐", "홍반", "red skin"],
        "blisters": ["물집", "수포", "muljib"],
        "joint_pain": ["관절통", "관절 아픔", "gwanjeoltong"],
        "muscle_weakness": ["근력 약화", "근육 약해짐"],
        "chills": ["오한", "추위 느낌", "ohan", "chills"],
        "sweating": ["식은땀", "땀 흘림", "sweat"],
        "sneezing": ["재채기", "jaechaegi"],
        "itchy_eyes": ["눈 가려움", "눈 간지러움"]
    },
    "ur": { # Urdu
        "fever": ["بخار", "bukhar", "tez bukhar"],
        "cough": ["کھانسی", "khansi"],
        "fatigue": ["تھکن", "کمزوری", "thakan", "kamzori"],
        "headache": ["سر درد", "sar dard"],
        "sore_throat": ["گلے کی سوزش", "گلا خراب", "gala kharab", "gale me dard"],
        "body_ache": ["جسم میں درد", "jism dard", "badan dard"],
        "runny_nose": ["زکام", "ناک بہنا", "zukam", "naak behna"],
        "shortness_of_breath": ["سانس پھولنا", "sans lene me takleef"],
        "loss_of_taste_smell": ["ذائقہ ختم ہونا", "سنگھنے کی حس کا جانا"],
        "nausea": ["متلی", "دل خراب ہونا", "matli", "ulti jaisa"],
        "vomiting": ["الٹی", "قے", "ulti", "vomit"],
        "diarrhea": ["دست", "حیضہ", "dast", "loose motions"],
        "stomach_pain": ["پیٹ کا درد", "pet dard"],
        "rash": ["سرخ دھبے", "جلد پر خارش", "skin rash", "surkh nishan"],
        "itching": ["خارش", "کھجلی", "kharish", "khujli"],
        "dry_skin": ["خشک جلد", "dry skin", "khushk jild"],
        "skin_redness": ["سرخی", "جلد کا لال ہونا", "laal jild"],
        "blisters": ["آبلے", "چھالے", "chhale", "able"],
        "joint_pain": ["جوڑوں کا درد", "jodon ka dard"],
        "muscle_weakness": ["پٹھوں کی کمزوری", "pathon ki kamzori"],
        "chills": ["سردی لگنا", "کپکپی", "thand lagna", "shivering"],
        "sweating": ["पसीना", "پسینہ آنا", "pasina"],
        "sneezing": ["چھینکیں", "chheenk", "chinken"],
        "itchy_eyes": ["آنکھوں میں خارش", "aankhon me kharish"]
    },
    "or": { # Odia
        "fever": ["ଜ୍ୱର", "jwara", "jwar"],
        "cough": ["କାଶ", "kasa", "kasha"],
        "fatigue": ["କ୍ଲାନ୍ତି", "ଦୁର୍ବଳତା", "klanti", "durbalata"],
        "headache": ["ମୁଣ୍ଡବିନ୍ଧା", "munda binda", "munda byatha"],
        "sore_throat": ["ତଣ୍ଟି କାଟିବା", "gala betha", "tanti binda"],
        "body_ache": ["ଦେହ ହାତ ବିନ୍ଧା", "deha binda"],
        "runny_nose": ["ଥଣ୍ଡା", "ନାକ ବୋହିବା", "thanda", "naka bohiba"],
        "shortness_of_breath": ["ଶ୍ୱାସକଷ୍ଟ", "swasakasta", "nishwasa kashta"],
        "loss_of_taste_smell": ["ସ୍ୱାଦ ହରାଇବା", "ବାସନା ନ ପାଇବା"],
        "nausea": ["ବାନ୍ତି ବାନ୍ତି ଲାଗିବା", "banti bhab"],
        "vomiting": ["ବାନ୍ତି", "banti", "vomit"],
        "diarrhea": ["ଝାଡ଼ା", "jhada", "diarrhea"],
        "stomach_pain": ["ପେଟ ବ୍ୟଥା", "peta binda", "peta betha"],
        "rash": ["କୁଣ୍ଡିଆ", "ଲାଲ ଚିହ୍ନ", "rash", "laal chinha"],
        "itching": ["କୁଣ୍ଡେଇ ହେବା", "kundei heba"],
        "dry_skin": ["ଶୁଖିଲା ଚର୍ମ", "shukhila charmam"],
        "skin_redness": ["ଚର୍ମ ଲାଲ ପଡିବା", "laal charmam"],
        "blisters": ["ଫୋଟକା", "photoka"],
        "joint_pain": ["ଗଣ୍ଠି ବିନ୍ଧା", "ganthi binda"],
        "muscle_weakness": ["ମାଂସପେଶୀ ଦୁର୍ବଳତା"],
        "chills": ["କମ୍ପନ", "ଶୀତ ଲାଗିବା", "shit lagiba", "shivering"],
        "sweating": ["ଝାଳ ବୋହିବା", "jhala"],
        "sneezing": ["ଛିଙ୍କ", "chinka"],
        "itchy_eyes": ["ଆଖି କୁଣ୍ଡେଇ ହେବା"]
    },
    "ml": { # Malayalam
        "fever": ["പനി", "pani", "payuram"],
        "cough": ["ചുമ", "chuma"],
        "fatigue": ["ക്ഷീണം", "തളർച്ച", "ksheenam", "thalarcha"],
        "headache": ["തലവേദന", "thala vedana", "thalavedana"],
        "sore_throat": ["തൊണ്ടവേദന", "thonda vedana", "thondavedana"],
        "body_ache": ["ശരീരവേദന", "shareera vedana", "shareeravedana"],
        "runny_nose": ["ജലദോഷം", "മൂക്കൊലിപ്പ്", "jaladosham", "mookkolippu"],
        "shortness_of_breath": ["ശ്വസതടസ്സം", "swasam muttal", "shwasamuttal"],
        "loss_of_taste_smell": ["രുചിയില്ലായ്മ", "മണമില്ലായ്മ", "ruchi nashtam", "manam nashtam"],
        "nausea": ["ഓക്കാനം", "ഛർദ്ദിക്കാൻ വരിക", "okkanam"],
        "vomiting": ["ഛർദ്ദി", "chhardi", "vomiting"],
        "diarrhea": ["വയറിളക്കം", "vayarilakkam"],
        "stomach_pain": ["വയറുവേദന", "vayar vedana", "vayarvedana"],
        "rash": ["ചൊറി", "തടിപ്പ്", "tadippu", "rash"],
        "itching": ["ചൊറിച്ചിൽ", "chorichil"],
        "dry_skin": ["വരണ്ട ചർമ്മം", "varanda charmam"],
        "skin_redness": ["ചർമ്മം ചുവക്കുക", "chuvappu charmam"],
        "blisters": ["പോളകൾ", "pola", "neerkola"],
        "joint_pain": ["മൂട്ടു വേദന", "മുട്ട് വേദന", "muttu vedana"],
        "muscle_weakness": ["പേശീ ബലഹീനത"],
        "chills": ["വിറയൽ", "തണുപ്പ് വിറയൽ", "virayal", "chills"],
        "sweating": ["വിയർപ്പ്", "viyarppu"],
        "sneezing": ["തുമ്മൽ", "thummal"],
        "itchy_eyes": ["കണ്ണിൽ ചൊറിച്ചിൽ", "kannu chorichil"]
    }
}

# Detailed disease symptom mappings
disease_symptoms = {
    "Common Cold": ["fever", "cough", "fatigue", "sore_throat", "runny_nose", "sneezing"],
    "Influenza": ["fever", "cough", "fatigue", "headache", "sore_throat", "body_ache", "chills"],
    "Covid-19": ["fever", "cough", "fatigue", "shortness_of_breath", "loss_of_taste_smell"],
    "Gastroenteritis": ["nausea", "vomiting", "diarrhea", "stomach_pain"],
    "Allergic Rhinitis": ["runny_nose", "sneezing", "itchy_eyes"],
    "Dengue Fever": ["fever", "headache", "rash", "joint_pain", "chills"],
    "Malaria": ["fever", "headache", "nausea", "vomiting", "chills", "sweating"],
    "Chickenpox": ["fever", "fatigue", "headache", "rash", "itching", "blisters"],
    "Eczema": ["itching", "dry_skin", "skin_redness"],
    "Food Allergy": ["nausea", "vomiting", "diarrhea", "stomach_pain", "rash", "itching"],
    "Migraine": ["headache", "nausea", "vomiting"]
}

# Symptom specificity weights — higher values discriminate diseases better
SYMPTOM_WEIGHTS = {
    "fever": 1.0, "cough": 1.2, "fatigue": 0.7, "headache": 1.0, "sore_throat": 1.1,
    "body_ache": 1.3, "runny_nose": 1.4, "shortness_of_breath": 3.2, "loss_of_taste_smell": 3.5,
    "nausea": 1.2, "vomiting": 2.0, "diarrhea": 2.5, "stomach_pain": 2.0,
    "rash": 2.8, "itching": 2.0, "dry_skin": 2.5, "skin_redness": 2.3, "blisters": 3.2,
    "joint_pain": 2.5, "muscle_weakness": 2.0, "chills": 2.0, "sweating": 2.0,
    "sneezing": 1.5, "itchy_eyes": 2.2
}

# Defining symptoms — a disease needs at least one of these to be a valid top match
DISEASE_SIGNATURE = {
    "Chickenpox": {"rash", "blisters", "itching"},
    "Allergic Rhinitis": {"runny_nose", "sneezing", "itchy_eyes"},
    "Eczema": {"dry_skin", "skin_redness", "itching"},
    "Gastroenteritis": {"diarrhea", "vomiting", "stomach_pain"},
    "Food Allergy": {"rash", "vomiting", "stomach_pain", "itching"},
    "Migraine": {"headache"},
    "Covid-19": {"cough", "shortness_of_breath", "loss_of_taste_smell"},
    "Common Cold": {"runny_nose", "sneezing", "sore_throat", "cough"},
}

GENERIC_SYMPTOMS = {"fever", "fatigue", "headache", "body_ache", "nausea"}

# Red-flag combinations that need urgent attention
RED_FLAG_RULES = [
    ({"shortness_of_breath", "fever"}, "Breathing difficulty with fever — seek emergency care immediately."),
    ({"shortness_of_breath"}, "Difficulty breathing detected — monitor SpO2 and seek medical help if below 94%."),
    ({"loss_of_taste_smell", "fever"}, "Fever with loss of taste/smell — isolate and test for COVID-19."),
    ({"vomiting", "diarrhea", "fever"}, "Persistent vomiting, diarrhea and fever — risk of severe dehydration."),
    ({"rash", "fever", "joint_pain"}, "Fever with rash and joint pain — dengue warning signs possible."),
    ({"chills", "sweating", "fever"}, "Cyclic fever with chills and sweating — malaria screening recommended."),
]

FOLLOW_UP_BY_SYMPTOM = {
    "fever": [
        "Do you have a cough, sore throat, or runny nose?",
        "Any skin rash, blisters, or intense itching?",
        "Do you feel joint pain, body aches, or chills?",
        "Any nausea, vomiting, or stomach pain?",
        "Have you lost your sense of taste or smell?"
    ],
    "cough": [
        "Do you also have fever or shortness of breath?",
        "Any loss of taste or smell?",
        "Is the cough dry or producing phlegm?"
    ],
    "headache": [
        "Is the pain on one side of the head (migraine-like)?",
        "Do you feel nauseous or have sensitivity to light?",
        "Do you also have fever or neck stiffness?"
    ],
    "rash": [
        "Are there fluid-filled blisters on the skin?",
        "Is the rash itchy or painful?",
        "Do you also have fever?"
    ],
    "diarrhea": [
        "Any vomiting or stomach cramps?",
        "Have you eaten anything unusual recently?",
        "Signs of dehydration — dry mouth or dizziness?"
    ]
}

INSUFFICIENT_SYMPTOM_LABELS = {
    "en": "General Febrile Illness (Needs More Symptoms)",
    "hi": "सामान्य बुखार (अधिक लक्षण आवश्यक)",
    "te": "సాధారణ జ్వరం (మరిన్ని లక్షణాలు అవసరం)",
    "ta": "பொது காய்ச்சல் (மேலும் அறிகுறிகள் தேவை)",
    "bn": "সাধারণ জ্বর (আরও লক্ষণ প্রয়োজন)",
    "ko": "일반 발열 (추가 증상 필요)",
    "ur": "عام بخار (مزید علامات درکار)",
    "or": "ସାଧାରଣ ଜ୍ୱର (ଅଧିକ ଲକ୍ଷଣ ଆବଶ୍ୟକ)",
    "ml": "പൊതുവായ പനി (കൂടുതൽ ലക്ഷണങ്ങൾ ആവശ്യം)"
}

# Image Info definitions
IMAGE_INFO = {
    "Healthy Skin": {
        "description": "The skin shows standard pigmentation, regular epidermal cellular layers, and no indications of localized inflammation, papules, or abnormal scaling.",
        "advice": "1. Maintain normal hygiene and moisturize regularly.\n2. Apply broad-spectrum sunscreen (SPF 30+).\n3. Keep hydrated and eat a balanced diet.",
        "color_features": "R/G Ratio ~1.1-1.2, Texture Contrast <10.0"
    },
    "Skin Rash": {
        "description": "Indicates areas of dermal irritation, capillary dilation, and superficial epidermal scaling, typical of contact dermatitis or heat rash.",
        "advice": "1. Keep the skin cool, dry, and ventilated.\n2. Apply over-the-counter hydrocortisone or calamine lotion.\n3. Avoid scratching and wear soft cotton clothing.",
        "color_features": "High Red Channel Value, Red/Green Ratio >1.4"
    },
    "Acne": {
        "description": "Presents as localized inflammation, papules, pustules, or plugged sebaceous glands (blackheads/whiteheads) due to sebum excess and bacterial colonizations.",
        "advice": "1. Wash face twice daily with a mild salicylic acid cleanser.\n2. Do not squeeze or pop lesions to prevent deep scarring.\n3. Avoid heavy makeup and oil-based moisturizers.",
        "color_features": "High Red Std Dev, Multi-point Peak Contours"
    },
    "Eczema": {
        "description": "Characterized by chronic barrier disruption, severe superficial cracking, dry scaling, and localized redness indicative of dermatitis.",
        "advice": "1. Apply thick emollient creams immediately after bathing.\n2. Avoid scented soaps, hot water, and synthetic fabrics.\n3. Consult a dermatologist for topical steroid options.",
        "color_features": "High Texture Contrast Index (>25.0), Low Greenness"
    }
}

# Detailed descriptions and advice for each disease predicted
DISEASE_INFO = {
    "Common Cold": {
        "en": {
            "prediction": "Common Cold",
            "description": "A benign viral infection of your upper respiratory tract (nose and throat). It is highly contagious but usually resolves on its own within 7 to 10 days.",
            "advice": "1. Prioritize bed rest and prevent physical exertion.\n2. Hydrate actively with warm liquids (herbal teas, warm water, broths).\n3. Use saline nasal sprays to relieve nasal congestion.\n4. Gargle with warm salt water to soothe a sore throat.",
            "urgency": "Low"
        },
        "hi": {
            "prediction": "सामान्य सर्दी (Common Cold)",
            "description": "ऊपरी श्वसन पथ (नाक और गले) का एक सामान्य वायरल संक्रमण। यह अत्यधिक संक्रामक है लेकिन आमतौर पर 7 से 10 दिनों में अपने आप ठीक हो जाता है।",
            "advice": "1. बिस्तर पर आराम करें और शारीरिक परिश्रम से बचें।\n2. गर्म तरल पदार्थों (हर्बल चाय, गर्म पानी, काढ़ा) का भरपूर सेवन करें।\n3. बंद नाक खोलने के लिए सलाइन नेसल स्प्रे का उपयोग करें।\n4. नमक के गुनगुने पानी से गरारे करें ताकि गले के दर्द में आराम मिले।",
            "urgency": "Low"
        },
        "te": {
            "prediction": "సాధారణ జలుబు (Common Cold)",
            "description": "ముక్కు మరియు గొంతుకు సంబంధించిన తేలికపాటి వైరల్ ఇన్ఫెక్షన్. ఇది త్వరగా వ్యాపిస్తుంది, కానీ 7 నుండి 10 రోజులలో దానంతట అదే తగ్గిపోతుంది.",
            "advice": "1. తగినంత విశ్రాంతి తీసుకోండి, శారీరక శ్రమ తగ్గించండి.\n2. వేడి ద్రవాలు (గోరువెచ్చని నీరు, హెర్బల్ టీ) ఎక్కువగా తీసుకోండి.\n3. ముక్కు దిబ్బడ తగ్గడానికి సెలైన్ నాజల్ డ్రాప్స్ వాడండి.\n4. గొంతు నొప్పి తగ్గడానికి గోరువెచ్చని ఉప్పు నీటితో గొంతు శుభ్రం చేసుకోండి.",
            "urgency": "Low"
        },
        "ta": {
            "prediction": "சாதாரண சளி (Common Cold)",
            "description": "மூக்கு மற்றும் தொண்டை பகுதியை பாதிக்கும் லேசான வைரஸ் தொற்று. இது எளிதில் பரவக்கூடியது, ஆனால் 7-10 நாட்களில் தானாகவே சரியாகிவிடும்.",
            "advice": "1. உடலுக்கு முழு ஓய்வு கொடுங்கள்.\n2. வெதுவெதுப்பான நீர், மூலிகை தேநீர் போன்ற சூடான திரவங்களை குடிக்கவும்.\n3. உப்பு நீர் கொண்டு தொண்டையை கொப்பளிக்கவும்.\n4. அடைபட்ட மூக்கை சரிசெய்ய உப்பு நீர் நாசி சொட்டு மருந்துகளைப் பயன்படுத்தவும்.",
            "urgency": "Low"
        },
        "bn": {
            "prediction": "সাধারণ সর্দি (Common Cold)",
            "description": "নাক ও গলার একটি মৃদু ভাইরাল সংক্রমণ। এটি সংক্রামক হলেও সাধারণত ৭ থেকে ১০ দিনের মধ্যে নিজে থেকেই নিরাময় হয়ে যায়।",
            "advice": "1. পর্যাপ্ত বিশ্রাম নিন এবং ভারী কাজ এড়িয়ে চলুন।\n2. হালকা গরম জল, তুলসী চা বা স্যুপের মতো তরল খাবার বেশি খান।\n3. লবণ জল দিয়ে গড়গড়া বা কুলকুচি করুন।\n4. বন্ধ নাক খুলতে স্যালাইন নেজাল স্প্রে ব্যবহার করুন।",
            "urgency": "Low"
        },
        "ko": {
            "prediction": "감기 (Common Cold)",
            "description": "코와 목구멍 등 상기도에 발생하는 가벼운 바이러스성 감염 증상입니다. 전염성이 높지만 보통 7~10일 이내에 자연적으로 치유됩니다.",
            "advice": "1. 충분한 휴식을 취하고 무리한 활동을 피하십시오.\n2. 미지근한 물이나 따뜻한 음료를 자주 마셔 수분을 보충하십시오.\n3. 목 통증 완화를 위해 따뜻한 소금물로 가글을 하십시오.\n4. 가습기를 사용하여 실내 습도를 조절하십시오.",
            "urgency": "Low"
        },
        "ur": {
            "prediction": "نزلہ و زکام (Common Cold)",
            "description": "ناک اور गले का एक आम वائرल انفیکشن۔ یہ ایک سے دوسرے کو جلدی لگ سکتا ہے لیکن عام طور پر 7 سے 10 دنوں में खुद ही ठीक हो जाता है।",
            "advice": "1. ज्यादा से ज्यादा आराम करें और भारी कामों से गुरेज करें।\n2. गर्म मशरूबात (जैसे हर्बल चाय, सूप या नीम गर्म पानी) पीएं।\n3. गले की सोजिश के लिए नीम गर्म नमकीन पानी से गरारे करें।\n4. बंद नाक खोलने के लिए भाप लें।",
            "urgency": "Low"
        },
        "or": {
            "prediction": "ସାଧାରଣ ଥଣ୍ଡା (Common Cold)",
            "description": "ନାକ ଏବଂ ଗଳାର ଏକ ଭୂତାଣୁ ଜନିତ ସଂକ୍ରମଣ | ଏହା ସଂକ୍ରାମକ କିନ୍ତୁ ସାଧାରଣତଃ ୭ ରୁ ୧୦ ଦିନରେ ନିଜେ ସୁସ୍ଥ ହୋଇଯାଏ |",
            "advice": "1. ବିଛଣାରେ ବିଶ୍ରାମ ନିଅନ୍ତୁ ଓ ଅଧିକ ଶାରୀରିକ ପରିଶ୍ରମ କରନ୍ତୁ ନାହିଁ |\n2. ପ୍ରଚୁର ମାତ୍ରାରେ ଗରମ ପାଣି, ଚା କିମ୍ବା କାଢ଼ା ପିଅନ୍ତୁ |\n3. ଲୁଣ ପାଣିରେ କୁଳକୁଳି କରନ୍ତୁ, ଯାହାଦ୍ୱାରା ତଣ୍ଟି କାଟିବାରୁ ଆରାମ ମିଳିବ |",
            "urgency": "Low"
        },
        "ml": {
            "prediction": "ജലദോഷം (Common Cold)",
            "description": "മൂക്കിനെയും തൊണ്ടയെയും ബാധിക്കുന്ന ലഘുവായ വൈറൽ അണുബാധ. ഇത് പകരുന്നതാണെങ്കിലും സാധാരണയായി 7 മുതൽ 10 ദിവസത്തിനുള്ളിൽ സ്വയം ഭേദമാകും.",
            "advice": "1. നന്നായി വിശ്രമിക്കുകയും അമിത അധ്വാനം ഒഴിവാക്കുകയും ചെയ്യുക.\n2. ചൂടുവെള്ളം, കഷായങ്ങൾ എന്നിവ ധാരാളം കുടിക്കുക.\n3. തൊണ്ടവേദന മാറാൻ ചെറുചൂടുള്ള ഉപ്പുവെള്ളം ഉപയോഗിച്ച് തൊണ്ട കഴുകുക.",
            "urgency": "Low"
        }
    },
    "Influenza": {
        "en": {
            "prediction": "Influenza (Flu)",
            "description": "A contagious viral respiratory infection affecting the nose, throat, and lungs, characterized by sudden high fever, severe body aches, and fatigue.",
            "advice": "1. Isolate immediately to prevent spreading the virus.\n2. Hydrate continuously and get abundant bed rest.\n3. Take antipyretics like paracetamol for muscle pain and fever reduction under advisory.\n4. Seek early doctor consultation for antiviral medication (e.g. Tamiflu).",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "इन्फ्लुएंजा (फ्लू)",
            "description": "श्वसन तंत्र (नाक, गले और फेफड़ों) को प्रभावित करने वाला एक तीव्र वायरल संक्रमण। इसमें अचानक तेज बुखार, गंभीर बदन दर्द और अत्यधिक थकान होती है।",
            "advice": "1. वायरस के फैलाव को रोकने के लिए खुद को अलग (आइसोलेट) करें।\n2. प्रचुर मात्रा में तरल पदार्थ लें और पर्याप्त विश्राम करें।\n3. बदन दर्द और बुखार कम करने के लिए डॉक्टर की सलाह पर पैरासिटामोल लें।\n4. एंटीवायरल दवाओं के लिए जल्द चिकित्सक से परामर्श करें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "ఇన్ఫ్లుఎంజా (ఫ్లూ)",
            "description": "ముక్కు, గొంతు మరియు ఊపిరితిత్తులపై తీవ్రంగా ప్రభావం చూపే వైరల్ ఇన్ఫెక్షన్. అకస్మాత్తుగా తీవ్ర జ్వరం, ఒళ్ళు నొప్పులు మరియు తీవ్ర అలసట దీని లక్షణాలు.",
            "advice": "1. ఇతరులకు వ్యాపించకుండా ఉండటానికి వెంటనే ఐసోలేట్ అవ్వండి.\n2. ఎక్కువ నీరు తాగుతూ, బెడ్ రెస్ట్ తీసుకోండి.\n3. జ్వరం మరియు నొప్పుల నివారణకు వైద్యుల సలహాతో పారాసిటమాల్ వాడండి.\n4. త్వరగా కోలుకోవడానికి యాంటీవైరల్ మందుల కొరకు డాక్టరును సంప్రదించండి.",
            "urgency": "Medium"
        },
        "ta": {
            "prediction": "இன்ஃப்ளூயன்ஸா (புளூ காய்ச்சல்)",
            "description": "மூக்கு, தொண்டை மற்றும் நுரையீரலை பாதிக்கும் கடுமையான வைரஸ் தொற்று. திடீர் அதிக காய்ச்சல், கடுமையான உடல் வலி மற்றும் சோர்வு இதன் அறிகுறிகள்.",
            "advice": "1. காய்ச்சல் பரவாமல் இருக்க உடனடியாக மற்றவர்களிடம் இருந்து தனிமைப்படுத்திக் கொள்ளவும்.\n2. காய்ச்சல் மற்றும் உடல் வலியை குறைக்க மருத்துவ ஆலோசனையுடன் பாராசிட்டமால் உட்கொள்ளவும்.\n3. தகுந்த ஓய்வு மற்றும் நீர்ச்சத்து உணவுகளை உட்கொள்ளவும்.\n4. தேவைப்பட்டால் ஆரம்ப கட்டத்திலேயே மருத்துவரை அணுகவும்.",
            "urgency": "Medium"
        },
        "bn": {
            "prediction": "ইনফ্লুয়েঞ্জা (ফ্লু)",
            "description": "শ্বাসনালী, নাক ও ফুসফুসকে আক্রমণকারী একটি তীব্র সংক্রামক ভাইরাল রোগ। হঠাৎ তীব্র জ্বর, গায়ে প্রচণ্ড ব্যথা ও অবসাদ এর প্রধান লক্ষণ।",
            "advice": "1. রোগ ছড়ানো বন্ধ করতে অবিলম্বে নিজেকে আলাদা বা আইসোলেট করুন।\n2. প্রচুর জল পান করুন এবং সম্পূর্ণ বেড রেস্টে থাকুন।\n3. জ্বর ও পেশীর ব্যথা কমাতে ডাক্তারের পরামর্শ মতো প্যারাসিটামল ব্যবহার করুন।\n4. প্রাথমিক পর্যায়ে চিকিৎসকের পরামর্শ নিয়ে অ্যান্টিভাইরাল ওষুধ গ্রহণ করতে পারেন।",
            "urgency": "Medium"
        },
        "ko": {
            "prediction": "인플루엔자 (독감)",
            "description": "갑작스러운 고열, 심한 근육통, 두통, 전신 쇠약감을 동반하며 코, 목, 폐를 공격하는 급성 바이러스성 호흡기 감염병입니다.",
            "advice": "1. 타인에게 전파되는 것을 막기 위해 즉시 격리 조치하십시오.\n2. 수분을 계속 보충하고 절대 안정을 취하며 휴식하십시오.\n3. 열과 전신 통증 조절을 위해 의사의 처방에 따라 해열 진통제를 복용하십시오.\n4. 증상 초기(48시간 이내)에 병원을 찾아 항바이러스제 처방을 고려하십시오.",
            "urgency": "Medium"
        },
        "ur": {
            "prediction": "انفلونزا (فلو)",
            "description": "ناک، گلے اور پھیپھڑوں کو متاثر کرنے والا ایک خطرناک وائرل انفیکشن، جس میں اچانک تیز بخار، شدید جسم کا درد اور نقاہت ہوتی ہے۔",
            "advice": "1. وائرس کو پھیلنے سے روکنے کے لیے فوری طور پر علیحدگی اختیار کریں۔\n2. نیم گرم پانی زیادہ سے زیادہ پیئیں اور مکمل آرام کریں۔\n3. درد اور بخار کو کم کرنے کے لیے ڈاکٹر کی ہدایت کے مطابق پیراسیٹامول لیں۔\n4. ابتدائی مرحلے میں ہی ڈاکٹر سے معائنہ کروائیں۔",
            "urgency": "Medium"
        },
        "or": {
            "prediction": "ଇନ୍‌ଫ୍ଲୁଏଞ୍ଜା (ଫ୍ଲୁ)",
            "description": "ନାକ, ଗଳା ଏବଂ ଫୁସଫୁସକୁ ଆକ୍ରାନ୍ତ କରୁଥିବା ଏକ ଭୂତାଣୁ ଜନିତ ଶ୍ୱାସକ୍ରିୟା ସଂକ୍ରମଣ | ଏଥିରେ ହଠାତ ତୀବ୍ର ଜ୍ୱର, ଦେହ-ହାତ ବିନ୍ଧା ହୁଏ |",
            "advice": "1. ସଂକ୍ରମଣକୁ ରୋକିବା ପାଇଁ ଅନ୍ୟମାନଙ୍କ ଠାରୁ ଦୂରେଇ ରୁହନ୍ତୁ |\n2. ପ୍ରଚୁର ପରିମାଣରେ ପାଣି ପିଅନ୍ତು ଏବଂ ସମ୍ପୂର୍ଣ୍ଣ ବିଶ୍ରାମ କରନ୍ତុ |\n3. ଦେହ ବିନ୍ଧା ଓ ଜ୍ୱର କମ କରିବା ପାଇଁ ଡାକ୍ତরଙ୍କ ପରାମର୍ଶରେ ପାରାସିଟାମଲ୍ ନିଅନ୍ତୁ |",
            "urgency": "Medium"
        },
        "ml": {
            "prediction": "ഇൻഫ്ലുവൻസ (ഫ്ലൂ)",
            "description": "പെട്ടെന്നുണ്ടാകുന്ന ശക്തമായ പനി, കടുത്ത ശരീരവേദന, തളർച്ച എന്നിവയോടുകൂടി മൂക്ക്, തൊണ്ട, ശ്വാസകോശം എന്നിവയെ ബാധിക്കുന്ന വൈറൽ അണുബാധ.",
            "advice": "1. മറ്റുള്ളവരിലേക്ക് പകരാതിരിക്കാൻ സ്വയം മാറിപ്പാർക്കുക (Isolate).\n2. കടുത്ത ശരീരവേദനയ്ക്കും പനിക്കും ഡോക്ടറുടെ നിർദ്ദേശപ്രകാരം പാരസിറ്റമോൾ കഴിക്കുക.\n3. ആവശ്യത്തിന് വിശ്രമിക്കുകയും ധാരാളം ദ്രവരൂപത്തിലുള്ള ആഹാരങ്ങൾ കഴിക്കുകയും ചെയ്യുക.",
            "urgency": "Medium"
        }
    },
    "Covid-19": {
        "en": {
            "prediction": "Covid-19",
            "description": "An infectious respiratory syndrome caused by the SARS-CoV-2 coronavirus. Symptoms vary widely and can quickly escalate to breathing distress.",
            "advice": "1. Strict self-isolation for at least 7 days.\n2. Monitor your peripheral oxygen levels (SpO2) using a pulse oximeter.\n3. Take warm steam inhalations and keep hydrated.\n4. Seek critical care immediately if SpO2 drops below 94% or you experience chest constriction.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "कोविड-19 (Covid-19)",
            "description": "SARS-CoV-2 कोरोनावायरस के कारण होने वाला एक संक्रामक श्वसन संक्रमण। इसके लक्षण हल्के से लेकर गंभीर श्वसन संकट तक हो सकते हैं।",
            "advice": "1. कम से कम 7 दिनों तक सख्त आइसोलेशन (अलग रहना) बनाए रखें।\n2. पल्स ऑक्सीजन मीटर से अपने ऑक्सीजन स्तर (SpO2) की नियमित जांच करें।\n3. गर्म पानी की भाप लें और गले को हाइड्रेटेड रखें।\n4. यदि ऑक्सीजन स्तर 94% से कम हो जाए या सांस लेने में बहुत कठिनाई हो, तो तुरंत अस्पताल जाएं।",
            "urgency": "High"
        },
        "te": {
            "prediction": "కోవిడ్-19 (Covid-19)",
            "description": "SARS-CoV-2 కరోనావైరస్ వల్ల వచ్చే తీవ్రమైన శ్వాసకోశ అంటువ్యాధి. దీని లక్షణాలు వేగంగా తీవ్ర శ్వాస ఇబ్బందులకు దారితీయవచ్చు.",
            "advice": "1. కనీసం 7 రోజులు ఖచ్చితమైన హోమ్ ఐసోలేషన్ పాటించండి.\n2. పల్స్ ఆక్సిమీటర్ సాయంతో మీ ఆక్సిజన్ స్థాయిలను (SpO2) క్రమం తప్పకుండా చూసుకోండి.\n3. ఆవిరి పట్టండి మరియు గోరువెచ్చని నీరు తాగుతూ ఉండండి.\n4. ఒకవేళ ఆక్సిజన్ స్థాయి 94% కన్నా తగ్గినా లేదా శ్వాస తీసుకోవడం కష్టంగా మారినా వెంటనే అత్యవసర చికిత్స పొందండి.",
            "urgency": "High"
        },
        "ta": {
            "prediction": "கோவிட்-19 (கொரோனா)",
            "description": "சார்ஸ்-கோவ்-2 corona வைரஸால் ஏற்படும் தொற்று நோய். இதன் அறிகுறிகள் லேசான பாதிப்பிலிருந்து கடுமையான மூச்சுத்திணறல் வரை செல்லலாம்.",
            "advice": "1. குறைந்தது 7 நாட்களுக்கு கண்டிப்பான வீட்டு தனிமைப்படுத்தலை மேற்கொள்ளவும்.\n2. ஆக்ஸிஜன் அளவை (SpO2) துடிப்பு ஆக்சிமீட்டர் மூலம் தொடர்ந்து கண்காணிக்கவும்.\n3. நீராவியை சுவாசித்து தொண்டையை ஈரப்பதத்துடன் வைத்திருக்கவும்.\n4. ஆக்ஸிஜன் அளவு 94%-க்கு கீழ் குறைந்தாலோ அல்லது கடுமையான மூச்சுத்திணறல் ஏற்பட்டாலோ உடனடியாக மருத்துவமனைக்குச் செல்லவும்.",
            "urgency": "High"
        },
        "bn": {
            "prediction": "কোভিড-১৯ (করোনা)",
            "description": "SARS-CoV-2 कोरोनावायरस द्वारा সৃষ্ট একটি মারাত্মক সংক্রামक শ্বাসকষ্টজনিত রোগ। এর লক্ষণ মৃদু থেকে তীব্র শ্বাসকষ্টে রূপ নিতে পারে।",
            "advice": "1. কমপক্ষে ৭ দিন কঠোরভাবে সেলফ-আইসোলেশনে থাকুন।\n2. পাল্স অক্সিমিটার ব্যবহার করে রক্তে অক্সিজেনের মাত্রা (SpO2) নিয়মিত পর্যবেক্ষণ করুন।\n3. দিনে দুবার গরম জলের ভাপ বা স্টিম নিন এবং প্রচুর জল পান করুন।\n4. যদি অক্সিজেনের মাত্রা ৯৪%-এর নিচে নেমে যায় বা বুকে ব্যথা ও অতিরিক্ত শ্বাসকষ্ট হয়, তবে অবিলম্বে হাসপাতালে যোগাযোগ করুন।",
            "urgency": "High"
        },
        "ko": {
            "prediction": "코로나바이러스감염증-19 (COVID-19)",
            "description": "SARS-CoV-2 바이러스에 의해 유발되는 급성 호흡기 감염증입니다. 무증상부터 심각한 폐렴 및 호흡부전까지 다양한 임상 양상을 보입니다.",
            "advice": "1. 최소 7일간 외부와의 접촉을 차단하고 엄격하게 자가격리하십시오.\n2. 맥박산소측정기를 사용하여 혈중 산소포화도(SpO2)를 모니터링하십시오.\n3. 따뜻한 음료를 마시고 실내 가습을 충분히 하십시오.\n4. 산소포화도가 94% 미만으로 떨어지거나 호흡이 곤란하고 가슴 통증이 지속되면 즉시 응급 진료를 받으십시오.",
            "urgency": "High"
        },
        "ur": {
            "prediction": "کووڈ-19 (Covid-19)",
            "description": "سارس-سی او وی-2 کورونا وائرس کی وجہ سے ہونے والا ایک خطرناک اور متعدی سانس کا انفیکشن۔ اس کے اثرات ہلکے سے لے کر سانس لینے میں شدید تکلیف تک ہو سکتے ہیں۔",
            "advice": "1. کم از کم 7 دن تک مکمل طور پر قرنطینہ (آئسولیشن) میں رہیں۔\n2. پلس آکسی میٹر کے ذریعے اپنے آکسیجن کی مقدار (SpO2) کو مسلسل چک کرتے رہیں۔\n3. گرم بھاپ لیں اور نیم گرم پانی پیتے رہیں۔\n4. اگر آکسیجن کا لیول 94 سے کم ہو جائے تو فوری طور پر قریبی ہسپتال سے رجوع کریں۔",
            "urgency": "High"
        },
        "or": {
            "prediction": "କୋଭିଡ୍-୧୯ (Covid-19)",
            "description": "SARS-CoV-2 କରୋନାଭୂତାଣୁ ଦ୍ୱାରା ସୃଷ୍ଟି ହେଉଥିବା ଏକ ସଂକ୍ରାମକ ଶ୍ୱାସକ୍ରିୟା ଜନିତ ରୋଗ | ଏହାର ଲକ୍ଷଣ ହଠାତ୍ ଅଣନିଶ୍ୱାସୀ ସ୍ଥିତି ସୃଷ୍ଟି କରିପାରେ |",
            "advice": "1. ଅନ୍ତତଃ ପକ୍ଷେ ୭ ଦିନ ପର୍ଯ୍ୟନ୍ତ ନିଜକୁ ସମ୍ପୂର୍ଣ୍ଣ ଆଇସୋଲେସନରେ ରଖନ୍ତୁ |\n2. ପଲ୍ସ ଅକ୍ସିମିଟର ସାହାଯ୍ୟରେ ଶରୀରର ଅକ୍ସିଜେନ ସ୍ତର (SpO2) ନିୟମିତ ମାପନ୍ତୁ |\n3. ଗରମ ପାଣିର ଭାପ ନିଅନ୍ତୁ ଓ ଶରୀରକୁ ସୁସ୍ଥ ରଖନ୍ତୁ |\n4. ଯଦି ଅକ୍ସିଜେନ ସ୍ତର ୯୪% ରୁ କମିଯାଏ କିମ୍ବା ନିଶ୍ୱାସ ନେବାରେ କଷ୍ଟ ହୁଏ, ତେବે ତୁରନ୍ତ ଡାକ୍ତରଖାନା ଯାଆନ୍ତୁ |",
            "urgency": "High"
        },
        "ml": {
            "prediction": "കോവിഡ്-19 (Covid-19)",
            "description": "SARS-CoV-2 കൊറോണ വൈറസ് ഉണ്ടാക്കുന്ന പകർച്ചവ്യാധി. ഇതിന്റെ ലക്ഷണങ്ങൾ പലരിലും പല രീതിയിലാണ് പ്രകടമാകുന്നത്, ചിലപ്പോൾ കടുത്ത ശ്വാസതടസ്സത്തിന് കാരണമാകാം.",
            "advice": "1. കുറഞ്ഞത് 7 ദിവസത്തേക്ക് കർശനമായി മുറിയിൽ കഴിയുക (Isolation).\n2. പൾസ് ഓക്സിമീറ്റർ ഉപയോഗിച്ച് രക്തത്തിലെ ഓക്സിജൻ അളവ് (SpO2) കൃത്യമായി പരിശോധിക്കുക.\n3. ഓക്സിജൻ അളവ് 94%-ൽ താഴെയാകുകയോ കടുത്ത ശ്വാസംമുട്ടൽ ഉണ്ടാകുകയോ ചെയ്താൽ അടിയന്തരമായി ചികിൽസ തേടുക.",
            "urgency": "High"
        }
    },
    "Gastroenteritis": {
        "en": {
            "prediction": "Gastroenteritis",
            "description": "Inflammation of the stomach and intestines, usually caused by viral or bacterial infection via contaminated food or water.",
            "advice": "1. Prevent dehydration: Sip Oral Rehydration Salts (ORS) or coconut water continuously.\n2. Avoid milk products, oily, spicy, or heavy foods.\n3. Eat soft, plain food (rice gruel, bananas, toast).\n4. Seek a doctor if vomiting persists for over 24 hours or blood is found in stool.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "गैस्ट्रोएंटेराइटिस (पेट का संक्रमण)",
            "description": "पेट और आंतों का संक्रमण, जो आमतौर पर दूषित भोजन या पानी के माध्यम से वायरल या बैक्टीरियल संक्रमण के कारण होता है। इसे सामान्य भाषा में 'पेट का फ्लू' कहते हैं।",
            "advice": "1. निर्जलीकरण (Dehydration) को रोकें: नियमित रूप से ओआरएस (ORS) या नारियल पानी का सेवन करें।\n2. डेयरी उत्पाद, तैलीय, मसालेदार या भारी भोजन से पूरी तरह परहेज करें।\n3. सुपाच्य भोजन लें (जैसे खिचड़ी, केला, उबले चावल, टोस्ट)।\n4. यदि लगातार उल्टी हो या मल में खून आए, तो तुरंत चिकित्सक से मिलें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "గ్యాస్ట్రోఎంటరైటిస్ (కడుపు ఇన్ఫెక్షన్)",
            "description": "కలుషితమైన ఆహారం లేదా నీటి ద్వారా కడుపు మరియు ప్రేగులలో వచ్చే ఇన్ఫెక్షన్. దీనివల్ల వాంతులు, విరేచనాలు సంభవిస్తాయి.",
            "advice": "1. డీహైడ్రేషన్ బారిన పడకుండా ఉండటానికి క్రమం తప్పకుండా ఓఆర్ఎస్ (ORS) లేదా కొబ్బరి నీళ్లు తాగండి.\n2. పాలు/పాల పదార్థాలు, నూనె, కారం మరియు మసాలా వస్తువులను అస్సలు తినకండి.\n3. తేలికగా అరిగే ఆహారం (గంజి, అరటిపండు, బ్రెడ్) మాత్రమే తీసుకోండి.\n4. ఒకవేళ వాంతులు ఆగకుండా ఉంటే వెంటనే డాక్టరును సంప్రదించండి.",
            "urgency": "Medium"
        },
        "ta": {
            "prediction": "இரைப்பை குடல் அழற்சி (வயிற்றுப்போக்கு)",
            "description": "உணவு அல்லது நீர் மாசுபடுவதால் வயிறு மற்றும் குடலில் ஏற்படும் தொற்று பாதிப்பு. இதனால் வாந்தி மற்றும் வயிற்றுப்போக்கு ஏற்படும்.",
            "advice": "1. நீர்ச்சத்து இழப்பைத் தடுக்க ORS கரைசல் அல்லது இளநீர் அடிக்கடி குடிக்கவும்.\n2. பால் பொருட்கள், எண்ணெய் மற்றும் காரமான உணவுகளைத் தவிர்க்கவும்.\n3. எளிதில் செரிமானமாகும் உணவுகளை (கஞ்சி, வாழைப்பழம், ரொட்டி) உட்கொள்ளவும்.\n4. வாந்தி அல்லது வயிற்றுப்போக்கு 24 மணி நேரத்திற்கு மேல் நீடித்தால் மருத்துவரை அணுகவும்.",
            "urgency": "Medium"
        },
        "bn": {
            "prediction": "গ্যাস্ট্রোএন্টেরাইটিস (পেটের সংক্রমণ)",
            "description": "পাকস্থলী এবং অন্ত্রের প্রদাহ বা অণুজীব সংক্রমণ, যা সাধারণত दूষিত খাবার বা জলের মাধ্যমে ভাইরাস বা ব্যাকটেরিয়ার সংক্রমণে ঘটে থাকে।",
            "advice": "1. ডিহাইড্রেশন প্রতিরোধ করুন: ওআরএস (ORS) বা ডাবের জল অল্প অল্প করে বারবার পান করুন।\n2. দুগ্ধজাত খাবার, তৈলাক্ত, ঝাল বা গুরুপাক খাবার এড়িয়ে চলুন।\n3. নরম ও সহজপাচ্য খাবার khan (যেমন ভাতের ফ্যান, কলা, পাউরুটি)।\n4. ২৪ ঘণ্টার বেশি বমি হলে বা মলের সঙ্গে রক্ত গেলে দ্রুত চিকিৎসকের শরণাপন্ন হন।",
            "urgency": "Medium"
        },
        "ko": {
            "prediction": "위장염 (식중독/장염)",
            "description": "위와 장의 점막에 생긴 염증성 질환으로, 주로 오염된 음식이나 물을 통해 바이러스나 세균에 감염되어 발생합니다.",
            "advice": "1. 탈수 방지가 가장 중요합니다: 경구수액제(ORS)나 전해질 음료, 보리차 등을 자주 마시십시오.\n2. 유제품, 자극적이고 기름진 음식, 매운 음식 섭취를 금하십시오.\n3. 죽, 미음, 바나나 등 소화가 잘되고 부드러운 음식을 소량씩 섭취하십시오.\n4. 구토가 24시간 이상 지속되거나 혈변이 관찰되면 즉시 병원을 방문하십시오.",
            "urgency": "Medium"
        },
        "ur": {
            "prediction": "معدے کا وائرل انفیکشن (Gastroenteritis)",
            "description": "معدے اور انتڑیوں کی سوزش جو عام طور پر آلودہ پانی یا غذا کے استعمال سے وائرل یا بیکٹیریل انفیکشن کی وجہ سے ہوتی ہے۔",
            "advice": "1. جسم میں پانی کی کمی نہ ہونے دیں: نمکول (ORS) یا ناریل کا پانی مسلسل پئیں۔\n2. دودھ سے بنی اشیاء اور مصالحے دار کھانوں سے پرہیز کریں۔\n3. ہلکی غذا (جیسے دلیہ، کھچڑی یا کیلا) کھائیں۔\n4. اگر مسلسل الٹیاں ہو رہی ہوں تو فوراً ڈاکٹر سے رابطہ کریں۔",
            "urgency": "Medium"
        },
        "or": {
            "prediction": "ଗ୍ୟାଷ୍ଟ୍ରୋଏଣ୍ଟେରାଇଟିସ (ପେଟ ସଂକ୍ରମଣ)",
            "description": "ପେଟ ଏବଂ ଅନ୍ତ୍ରର ପ୍ରଦାହ, ଯାହା ପ୍ରାୟତଃ ଦୂଷିତ ଖାଦ୍ୟ କିମ୍ବା ଜଳ ମାଧ୍ୟମରେ ସଂକ୍ରମଣ ଯୋଗୁଁ ହୋଇଥାଏ |",
            "advice": "1. ଶରୀରର ଜଳୀୟ ଅଂଶ ରକ୍ଷା କରନ୍ତୁ: ପ୍ରଚୁର ଓଆରଏସ (ORS) କିମ୍ବା ନଡ଼ିଆ ପାଣି ପିଅନ୍ତୁ |\n2. ତେଲ, ମସଲା ଓ ଗରିଷ୍ଠ ଖାଦ୍ୟ ଖାଇବା ଠାରୁ ଦୂରେଇ ରୁହନ୍ତୁ |\n3. ହାଲୁକା ଖାଦ୍ୟ (ପେଜ, କଦଳୀ, ଟୋଷ୍ଟ) ଖାଆନ୍ତୁ |\n4. ଯଦି ୨୪ ଘଣ୍ଟାରୁ ଅଧିକ ବାନ୍ତି ହୁଏ, ତୁରନ୍ତ ଡାକ୍ତରଙ୍କ ସହ ପରାମର୍ଶ କରନ୍ତୁ |",
            "urgency": "Medium"
        },
        "ml": {
            "prediction": "ഗ്യാസ്ട്രോഎൻട്രൈറ്റിസ് (വയറിളക്ക രോഗം)",
            "description": "കേടായ ആഹാരത്തിലൂടെയോ മലിനമായ വെള്ളത്തിലൂടെയോ ഉണ്ടാകുന്ന അണുബാധ കാരണം വയറിലും കുടലിലും വീക്കവും അസ്വസ്ഥതയും ഉണ്ടാകുന്ന അവസ്ഥ.",
            "advice": "1. നിർജ്ജലീകരണം തടയാൻ ഒ.ആർ.എസ് (ORS) ലായനി, കരിക്കിൻ വെള്ളം എന്നിവ കുടിക്കുക.\n2. എണ്ണമയമുള്ളതും എരിവുള്ളതുമായ ഭക്ഷണങ്ങളും പാലുൽപ്പന്നങ്ങളും പൂർണ്ണമായി ഒഴിവാക്കുക.\n3. കഞ്ഞി, ഏത്തപ്പഴം എന്നിവ പോലുള്ള ദഹിക്കാൻ എളുപ്പമുള്ള ആഹാരങ്ങൾ കഴിക്കുക.",
            "urgency": "Medium"
        }
    },
    "Allergic Rhinitis": {
        "en": {
            "prediction": "Allergic Rhinitis",
            "description": "An allergic reaction in the nasal passages caused by airborne allergens like pollen, dust mites, or pet dander.",
            "advice": "1. Identify triggers and reduce environmental exposure to dust or pollen.\n2. Keep windows closed during high pollen seasons and wash bedding in hot water.\n3. Take over-the-counter antihistamines as advised by a pharmacist.\n4. Use saline nasal rinses to clear allergen particles.",
            "urgency": "Low"
        },
        "hi": {
            "prediction": "एलर्जिक राइनाइटिस (एलर्जी)",
            "description": "हवा में मौजूद धूल, परागकण (pollen) या पालतू जानवरों की रूसी के कारण नाक के मार्ग में होने वाली एक एलर्जी प्रतिक्रिया।",
            "advice": "1. एलर्जी के कारणों (धूल, मिट्टी) की पहचान करें और उनसे दूर रहें।\n2. धूल भरे स्थानों पर मास्क पहनें और घर की खिड़कियां बंद रखें।\n3. फार्मासिस्ट की सलाह पर एंटीहिस्टामाइन (एंटी-एलर्जी) दवाएं लें।\n4. नाक को साफ करने के लिए सलाइन वाटर का उपयोग करें।",
            "urgency": "Low"
        },
        "te": {
            "prediction": "అలెర్జిక్ రైనైటిస్ (Allergic Rhinitis)",
            "description": "గాలిలోని పరాగరేణువులు, దుమ్ము, లేదా పెంపుడు జంతువుల వెంట్రుకల వల్ల ముక్కు లోపలి పొరలలో వచ్చే అలెర్జీ ప్రతిచర్య.",
            "advice": "1. అలెర్జీ కలిగించే కారణాలను గుర్తించి, దుమ్ము-ధూళికి దూరంగా ఉండండి.\n2. కిటికీలు మూసి ఉంచడం ద్వారా గాలిలోని దుమ్ము ఇంట్లోకి రాకుండా చూసుకోండి.\n3. వైద్యుల సలహాతో యాంటీ-అలెర్జీ మందులు (Antihistamines) వాడండి.\n4. ముక్కును సెలైన్ నీటితో క్రమం తప్పకుండా శుభ్రం చేసుకోండి.",
            "urgency": "Low"
        },
        "ta": {
            "prediction": "ஒவ்வாமை மூக்கு அழற்சி (Allergic Rhinitis)",
            "description": "காற்றில் உள்ள மகரந்தம், தூசி அல்லது செல்லப்பிராணிகளின் உரோமம் ஆகியவற்றால் ஏற்படும் ஒவ்வாமை எதிர்வினை.",
            "advice": "1. ஒவ்வாமையை ஏற்படுத்தும் காரணிகளை கண்டறிந்து, தூசிகள் நிறைந்த இடங்களை தவிர்க்கவும்.\n2. ஜன்னல்களை மூடி வைக்கவும், படுக்கை விரிப்புகளை வெந்நீரில் துவைக்கவும்.\n3. மருந்தக ஆலோசனையுடன் ஒவ்வாமை எதிர்ப்பு மாத்திரைகளை (Antihistamines) உட்கொள்ளவும்.\n4. நாசிப் பாதையை சுத்தப்படுத்த உப்பு நீரைப் பயன்படுத்தவும்.",
            "urgency": "Low"
        },
        "bn": {
            "prediction": "অ্যালার্জিক রাইনাইটিস (অ্যালার্জি)",
            "description": "বাতাসে ভেসে থাকা ধূলিকণা, পরাগরেণু বা পোষা প্রাণীর লোম नाक দিয়ে প্রবেশ করার ফলে নাকের ভেতরের অংশে সৃষ্ট অ্যালার্জির বিক্রিয়া।",
            "advice": "1. অ্যালার্জির উৎসগুলি চিহ্নিত করুন এবং ধুলোবালি से दूर रहें।\n2. ঘর পরিষ্কার করার সময় মাস্ক ব্যবহার করুন এবং বিছানার চাদর গরম জলে ধুয়ে নিন।\n3. চিকিৎসকের পরামর্শ অনুযায়ী অ্যান্টিহিস্টামিন জাতীয় ওষুধ সেবন করতে পারেন।\n4. নাকের ভেতরের অ্যালার্জেন দূর করতে স্যালাইন ওয়াটার স্প্রে ব্যবহার করুন।",
            "urgency": "Low"
        },
        "ko": {
            "prediction": "알레르기성 비염 (Allergic Rhinitis)",
            "description": "꽃가루, 집먼지진드기, 동물의 털 등 공기 중의 알레르기 유발 물질에 의해 코점막이 자극을 받아 발생하는 알레르기 반응입니다.",
            "advice": "1. 원인 물질을 파악하고 먼지나 꽃가루가 많은 환경의 노출을 최소화하십시오.\n2. 황사나 미세먼지가 심한 날에는 외출 시 마스크를 반드시 착용하십시오.\n3. 침구류를 뜨거운 물로 자주 세탁하여 집먼지진드기를 제거하십시오.\n4. 약사와 상의하여 항히스타민제를 복용하거나 식염수로 코를 세척하십시오.",
            "urgency": "Low"
        },
        "ur": {
            "prediction": "الرجک رینائٹس (Allergic Rhinitis)",
            "description": "ہوا میں موجود گرد و غبار، پھولوں کے ذرات، یا پالتو جانوروں کے بالوں کی وجہ سے ناک کی نالیوں میں ہونے والا ایک الرجی ردعمل۔",
            "advice": "1. الرجی پیدا کرنے والی چیزوں سے دور رہیں اور مٹی والے مقامات پر ماسک پہنیں۔\n2. گھر کے بستر اور چادریں گرم پانی سے دھوئیں۔\n3. ڈاکٹر کی ہدایت کے مطابق اینٹی الرجک ادویات کا استعمال کریں۔\n4. نیم گرم نمکین پانی سے ناک صاف کریں۔",
            "urgency": "Low"
        },
        "or": {
            "prediction": "ଆଲର୍ଜିକ୍ ରାଇନାଇଟ୍‌ସ (Allergic Rhinitis)",
            "description": "ଧୂଳି, ଗଛର ପରାଗରେଣୁ କିମ୍ବା ଗୃହପାଳିତ ପଶୁଙ୍କ ଲୋମ ଦ୍ୱାରା ନାକର ଭିତର ପାର୍ଶ୍ୱରେ ସୃଷ୍ଟି ହେଉଥିବା ଏକ ଆଲର୍ଜି ପ୍ରତିକ୍ରିୟା |",
            "advice": "1. ଉତ୍ତେଜକଗୁଡ଼ିକୁ ଚିହ୍ନଟ କରନ୍ତୁ ଏବଂ ଧୂଳି କିମ୍ବା ମାଟି ସଂସ୍ପର୍ଶରୁ ଦୂରେଇ ରୁହନ୍ତୁ |\n2. ବାହାରକୁ ଗଲାବେଳେ ମାସ୍କ ବ୍ୟବହାର କରନ୍ତୁ |\n3. ଆବଶ୍ୟକ ହେଲେ ଆଲର୍ଜି ପ୍ରତିରୋଧକ ଔଷଧ ବ୍ୟବହାର କରନ୍ତୁ |",
            "urgency": "Low"
        },
        "ml": {
            "prediction": "അലർജിക് റൈനൈറ്റിസ് (അലർജി ജലദോഷം)",
            "description": "പൊടിപടലങ്ങൾ, പൂമ്പൊടി, വളർത്തുമൃഗങ്ങളുടെ രോമം എന്നിവ ശ്വസിക്കുന്നത് വഴി മൂക്കിനുള്ളിൽ ഉണ്ടാകുന്ന അലർജി പ്രതിപ്രവർത്തനം.",
            "advice": "1. അലർജി ഉണ്ടാക്കുന്ന ഘടകങ്ങളെ തിരിച്ചറിഞ്ഞ് അവയിൽ നിന്ന് അകന്നു നിൽക്കുക.\n2. പൊടിയടിക്കുന്ന സാഹചര്യങ്ങളിൽ മാസ്ക് ധരിക്കുക.\n3. ഡോക്ടറുടെയോ ഫാർമസിസ്റ്റിന്റെയോ നിർദ്ദേശപ്രകാരം അലർജി ഗുളികകൾ (Antihistamines) കഴിക്കുക.",
            "urgency": "Low"
        }
    },
    "Dengue Fever": {
        "en": {
            "prediction": "Dengue Fever",
            "description": "A mosquito-borne tropical viral disease transmitted by Aedes mosquitoes, causing sudden high fever, intense headache, bone/joint pain, and skin rash.",
            "advice": "1. Rest extensively and maintain high fluid intake (ORS, juices, water).\n2. Strictly take only paracetamol for pain and fever. Avoid ibuprofen, aspirin, or diclofenac as they can induce severe internal bleeding.\n3. Monitor blood platelet counts daily.\n4. Watch for warning signs like severe abdominal pain, persistent vomiting, or bleeding gums.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "डेंगू बुखार (Dengue Fever)",
            "description": "मादा एडीज मच्छर के काटने से फैलने वाला एक गंभीर वायरल संक्रमण। इसमें अचानक तेज बुखार, आँखों के पीछे दर्द, जोड़ों में असहनीय दर्द ('हड्डी तोड़ बुखार') और चकत्ते होते हैं।",
            "advice": "1. पूरी तरह आराम करें और शरीर में पानी की कमी न होने दें (ORS, नारियल पानी, पपीते के पत्तों का रस लें)।\n2. दर्द और बुखार के लिए केवल पैरासिटामोल लें। आईबुप्रोफेन या एस्पिरिन बिल्कुल न लें, क्योंकि इनसे ब्लीडिंग का खतरा बढ़ जाता है।\n3. रक्त में प्लेटलेट्स (Platelets) की संख्या की रोजाना जांच करवाएं।\n4. मसूड़ों से खून आना या पेट में तेज दर्द होने पर तुरंत डॉक्टर के पास जाएं।",
            "urgency": "High"
        },
        "te": {
            "prediction": "డెంగ్యూ జ్వరం (Dengue Fever)",
            "description": "ఎడెస్ దోమల ద్వారా వ్యాపించే తీవ్రమైన వైరల్ జ్వరం. విపరీతమైన జ్వరం, కీళ్ల నొప్పులు (ఎముకలు విరిగినట్లు అనిపించే నొప్పి), కంటి వెనుక నొప్పి మరియు దద్దుర్లు దీని లక్షణాలు.",
            "advice": "1. పూర్తిగా విశ్రాంతి తీసుకోండి మరియు ద్రవపదార్థాలు (ఓఆర్ఎస్, కొబ్బరి నీరు) అధికంగా తీసుకోండి.\n2. జ్వరం మరియు నొప్పుల నివారణకు కేవలం పారాసిటమాల్ మాత్రమే వాడండి. ఐబుప్రొఫెన్, ఆస్పిరిన్ వంటి మందులు రక్తస్రావం ముప్పును పెంచుతాయి కాబట్టి వాడకండి.\n3. ప్రతిరోజూ రక్త పరీక్ష ద్వారా ప్లేట్‌లెట్ల కౌంట్ (Platelet count) పరిశీలించండి.\n4. చిగుళ్ళ నుండి రక్తం కారడం లేదా తీవ్రమైన కడుపు నొప్పి ఉంటే వెంటనే ఆసుపత్రికి వెళ్ళండి.",
            "urgency": "High"
        },
        "ta": {
            "prediction": "டெங்கு காய்ச்சல் (Dengue Fever)",
            "description": "ஏடிஸ் கொசுக்களால் பரவும் கடுமையான வைரஸ் காய்ச்சல். திடீர் அதிக காய்ச்சல், கண் பின் பகுதி வலி, கடுமையான மூட்டு வலி மற்றும் தோல் தடிப்புகள் இதன் அறிகுறிகள்.",
            "advice": "1. முழு ஓய்வு மற்றும் அதிக நீர்ச்சத்து ஆகாரங்கள் (ORS, பப்பாளி இலை சாறு, இளநீர்) எடுத்துக்கொள்ளவும்.\n2. வலி நிவாரணத்திற்கு பாராசிட்டமால் மட்டுமே பயன்படுத்த வேண்டும். அஸ்பிரின் அல்லது ஐபுப்ரோஃபென் போன்ற மருந்துகளை கண்டிப்பாக தவிர்க்கவும், இவை இரத்தப்போக்கை ஏற்படும்.\n3. தினசரி இரத்த தட்டுக்களின் (Platelet counts) அளவை பரிசோதிக்கவும்.\n4. கடுமையான வயிற்று வலி அல்லது இரத்த கசிவு ஏற்பட்டால் உடனடியாக மருத்துவமனைக்குச் செல்லவும்.",
            "urgency": "High"
        },
        "bn": {
            "prediction": "ডেঙ্গু জ্বর (Dengue Fever)",
            "description": "এডিস মশার কামড়ের মাধ্যমে ছড়ানো একটি গ্রীষ্মমণ্ডলীয় ভাইরাসঘটিত রোগ। তীব্র জ্বর, চোখের পেছনে ব্যথা, জয়েন্টে প্রচণ্ড ব্যথা এবং চামড়ায় লাল র‍্যাশ এর লক্ষণ।",
            "advice": "1. সম্পূর্ণ বিশ্রামে থাকুন এবং প্রচুর পরিমাণে তরল খাবার (স্যালাইন জল, ডাবের জল, ফলের রস) পান করুন।\n2. জ্বর ও ব্যথার জন্য শুধুমাত্র প্যারাসিটামল সেবন করুন। অ্যাসপিরিন বা আইবুপ্রোফেন জাতীয় ওষুধ একেবারেই খাবেন না, কারণ এগুলো রক্তক্ষরণের ঝুঁকি বাড়ায়।\n3. প্রতিদিন রক্তে প্লাটিলেট কাউন্ট (Platelet Count) পরীক্ষা করুন।\n4. মাড়ি দিয়ে রক্ত পড়া, অনবরত বমি বা তীব্র পেট ব্যথার মতো লক্ষণ দেখা দিলে অবিলম্বে রোগীকে হাসপাতালে ভর্তি করুন।",
            "urgency": "High"
        },
        "ko": {
            "prediction": "뎅기열 (Dengue Fever)",
            "description": "뎅기 바이러스를 가진 모기(이집트숲모기 등)에 물려 전파되는 급성 열성 질환입니다. 고열, 심한 두통, 안구통, 근육통, 관절통 및 피부 발진이 특징입니다.",
            "advice": "1. 절대 안정을 취하고 탈수를 막기 위해 수액이나 물을 충분히 섭취하십시오.\n2. 열과 통증 완화를 위해 반드시 아세트아미노펜(타이레놀 등)만 복용하십시오. 아스피린이나 이부프로펜은 출혈 위험을 크게 높이므로 절대 복용하지 마십시오.\n3. 매일 혈소판 수치를 검사하여 모니터링하십시오.\n4. 코피, 잇몸 출혈, 극심한 복통 등 출혈 경향성이 나타나면 즉시 응급실로 가십시오.",
            "urgency": "High"
        },
        "ur": {
            "prediction": "ڈینگی بخار (Dengue Fever)",
            "description": "ایڈیز مچھر کے کاٹنے سے پھیلنے والا ایک خطرناک وائرل بخار، جس میں شدید بخار، ہڈیوں اور جوڑوں میں شدید درد، اور جسم پر سرخ دھبے پڑتے ہیں۔",
            "advice": "1. مکمل آرام کریں اور پانی کی کمی کو پورا کرنے کے لیے او آر ایس اور جوسز کا کثرت سے استعمال کریں۔\n2. بخار کے لیے صرف پیراسیٹامول لیں۔ ڈسپرین یا آئیبوپروفین ہرگز نہ لیں کیونکہ اس سے اندرونی خون بہنے کا خطرہ ہوتا ہے۔\n3. روزانہ کی بنیاد پر خون کے پلیٹلیٹس (Platelets) چیک کروائیں۔\n4. مسوڑھوں سے خون آنے کی صورت میں فوراً ہسپتال پہنچیں۔",
            "urgency": "High"
        },
        "or": {
            "prediction": "ଡେଙ୍ଗୁ ଜ୍ୱର (Dengue Fever)",
            "description": "ଏଡିସ୍ ମଶା କାମୁଡ଼ିବା ଦ୍ୱାରା ବ୍ୟାପୁଥିବା ଏକ ଗମ୍ଭୀର ଜ୍ୱର | ଏଥିରେ ହଠାତ ତୀବ୍ର ଜ୍ୱର, ଆଖି ପଛପଟେ ଯନ୍ତ୍ରଣା ଏବଂ ଗଣ୍ଠି ଯନ୍ତ୍ରଣା ହୋଇଥାଏ |",
            "advice": "1. ଶଯ୍ୟାଶାୟୀ ରହି ସମ୍ପୂର୍ଣ୍ଣ ବିଶ୍ରାମ କରନ୍ତୁ ଓ ଅଧିକ ପାଣି ପିଅନ୍ତୁ |\n2. ଯନ୍ତ୍ରଣା ଏବଂ ଜ୍ୱର ପାଇଁ କେବଳ ପାରାସିଟାമଲ୍ ବ୍ୟବହାର କରନ୍ତୁ, ଆଇବୁପ୍ରୋଫେନ୍ କିମ୍ବା ଆସ୍ପିରିନ୍ ଜମାରୁ ଖାଆନ୍ତୁ ନାହିଁ |\n3. ରକ୍ତରେ ପ୍ଲେଟଲେଟ୍ସ ପରିମାଣ ପ୍ରତିଦିନ ଯାଞ୍ଚ କରାନ୍ତୁ |",
            "urgency": "High"
        },
        "ml": {
            "prediction": "ഡെങ്കിപ്പനി (Dengue Fever)",
            "description": "ഈഡിസ് കൊതുകുകൾ പരത്തുന്ന മാരകമായ വൈറൽ പനി. ശക്തമായ പനി, കണ്ണിന് പിന്നിൽ വേദന, അസ്ഥികൾ ഒടിയുന്നതുപോലുള്ള കടുത്ത സന്ധിവേദന, ചുവന്ന തടിപ്പുകൾ എന്നിവയാണ് ലക്ഷണങ്ങൾ.",
            "advice": "1. പൂർണ്ണമായി വിശ്രമിക്കുക, ധാരാളം വെള്ളവും ഒ.ആർ.എസ് ലായനിയും കുടിക്കുക.\n2. പനിക്കും വേദനയ്ക്കും പാരസിറ്റമോൾ മാത്രം കഴിക്കുക. ആസ്പിരിൻ, ഐബുപ്രൂഫിൻ എന്നിവ കഴിക്കരുത് (ഇത് രക്തസ്രാവത്തിന് കാരണമാകും).\n3. രക്തത്തിലെ പ്ലേറ്റ്ലെറ്റ് കൗണ്ട് ദിവസവും പരിശോധിക്കുക.",
            "urgency": "High"
        }
    },
    "Malaria": {
        "en": {
            "prediction": "Malaria",
            "description": "A parasitic blood disease transmitted by the bite of an infected female Anopheles mosquito, characterized by cycles of high fever, shaking chills, and sweating.",
            "advice": "1. Must get a blood test (thick/thin smear) immediately for definitive diagnosis.\n2. Requires prescription antimalarial drugs (e.g. Artemisinin-based combinations) immediately.\n3. Do not self-treat; delayed treatment can result in life-threatening complications.\n4. Stay under a mosquito net to prevent infective mosquito bites.",
            "urgency": "Critical"
        },
        "hi": {
            "prediction": "मलेरिया (Malaria)",
            "description": "संक्रमित मादा एनोफिलीज मच्छर के काटने से होने वाला एक परजीवी (Parasitic) रक्त रोग। इसमें कंपकंपी के साथ तेज बुखार आना, फिर पसीना आकर बुखार उतरने का चक्र होता है।",
            "advice": "1. बीमारी की पुष्टि के लिए तुरंत रक्त की जांच (Blood Test) करवाएं।\n2. चिकित्सक की सलाह पर तुरंत मलेरिया-रोधी दवाएं (Antimalarial Drugs) शुरू करें।\n3. स्वयं कोई दवा न लें; समय पर इलाज न होने से यह जानलेवा हो सकता है।\n4. मच्छरदानी का प्रयोग करें और आस-पास पानी जमा न होने दें।",
            "urgency": "Critical"
        },
        "te": {
            "prediction": "మలేరియా (Malaria)",
            "description": "ఆనాఫిలిస్ దోమ కాటు ద్వారా వ్యాపించే పరాన్నజీవి రక్త వ్యాధి. చలితో వణుకు రావడం, జ్వరం రావడం మరియు చెమటలు పట్టి జ్వరం తగ్గడం దీని ప్రధాన లక్షణాలు.",
            "advice": "1. మలేరియా ఉందో లేదో తెలుసుకోవడానికి వెంటనే రక్త పరీక్ష చేయించుకోండి.\n2. డాక్టర్ సిఫార్సు చేసిన యాంటీ-మలేరియల్ మందులను వెంటనే వాడటం ప్రారంభించండి.\n3. సొంత వైద్యం చేసుకోకండి; ఆలస్యం చేస్తే ప్రాణాపాయం కలగవచ్చు.\n4. దోమతెరలను వాడండి మరియు ఇళ్ల చుట్టూ మురికి నీరు నిల్వ ఉండకుండా చూసుకోండి.",
            "urgency": "Critical"
        },
        "ta": {
            "prediction": "மலேரியா (Malaria)",
            "description": "பெண் அனாபிலிஸ் கொசு கடிப்பதால் பரவும் ஒட்டுண்ணி நோய். குளிர் நடுக்கத்துடன் கூடிய காய்ச்சல், வியர்வை வெளியேறி காய்ச்சல் குறைவது இதன் முக்கிய அறிகுறிகள்.",
            "advice": "1. காய்ச்சல் வந்தவுடன் உடனடியாக இரத்தப் பரிசோதனை செய்து கொள்ள வேண்டும்.\n2. மருத்துவர் பரிந்துரைக்கும் மலேரியா எதிர்ப்பு மருந்துகளை (Antimalarial drugs) உடனடியாக எடுக்கவும்.\n3. சுய மருத்துவம் செய்ய வேண்டாம்; அலட்சியப்படுத்தினால் உயிருக்கு ஆபத்தாக முடியும்.\n4. கொசுவலைகளைப் பயன்படுத்தவும், வீட்டைச் சுற்றி நீர் தேங்காமல் பார்த்துக் கொள்ளவும்.",
            "urgency": "Critical"
        },
        "bn": {
            "prediction": "ম্যালেরিয়া (Malaria)",
            "description": "অ্যানোফিলিস মশার কামড়ের মাধ্যমে ছড়ানো প্লাজমোডিয়াম পরজীবীঘটিত রক্ত রোগ। কাঁপুনি দিয়ে পর্যায়ক্রমিক তীব্র জ্বর, ঘাম এবং গা ব্যথা এর লক্ষণ।",
            "advice": "1. লক্ষণ দেখা দেওয়ার সাথে সাথে রক্তের পরীক্ষা (Blood Slide Test) করান।\n2. চিকিৎসকের ব্যবস্থাপত্র অনুযায়ী অবিলম্বে ম্যালেরিয়া-বিরোধী ওষুধ শুরু করুন।\n3. নিজে নিজে কোনো ওষুধ খাবেন না; অবহেলা করলে এটি প্রাণঘাতী হতে পারে।\n4. মশারি ব্যবহার করুন এবং ঘুমানোর সময় শরীর ঢেকে রাখুন।",
            "urgency": "Critical"
        },
        "ko": {
            "prediction": "말라리아 (Malaria)",
            "description": "말라리아 원충에 감염된 얼룩날개모기에 물려 전파되는 기생충성 혈액 질환입니다. 주기적인 고열, 오한(독한 추위로 몸이 떨림), 발한(땀 흘림) 증상이 반복되는 것이 특징입니다.",
            "advice": "1. 정확한 진단을 위해 즉시 혈액 검사(말라리아 도말 검사)를 받으십시오.\n2. 진단 즉시 의사의 처방 하에 말라리아 치료제를 복용해야 합니다.\n3. 자가 치료를 하지 마십시오. 치료 지연 시 다발성 장기 부전 등 치명적인 합병증이 생길 수 있습니다.\n4. 감염 모기 접촉 차단을 위해 모기장을 사용하십시오.",
            "urgency": "Critical"
        },
        "ur": {
            "prediction": "ملیریا (Malaria)",
            "description": "مادہ اینوفلیز مچھر کے کاٹنے سے پھیلنے والی خون کی ایک طفیلی (Parasitic) بیماری، جس میں کپکپی کے ساتھ تیز بخار چڑھتا ہے اور پسینہ آنے کے ساتھ اتر جاتا ہے۔",
            "advice": "1. فوری طور پر خون کا ٹیسٹ کروائیں تاکہ بیماری کی تصدیق ہو سکے۔\n2. ڈاکٹر کی تجویز کردہ ملیریا کش ادویات کا استعمال فوراً شروع کریں۔\n3. خود سے علاج کرنے کی کوشش نہ کریں کیونکہ یہ جان لیوا بھی ہو سکتا ہے۔\n4. سوتے وقت مچھر دانی کا استعمال لازمی کریں۔",
            "urgency": "Critical"
        },
        "or": {
            "prediction": "ମ୍ୟାଲେରିଆ (Malaria)",
            "description": "ମାଈ ଆନୋଫିଲିସ୍ ମଶା କାମୁଡ଼ିବା ଦ୍ୱାରା ବ୍ୟାପୁଥିବା ଏକ ପରଜୀବୀ ଜନିତ ରକ୍ତ ରୋଗ | ଏଥିରେ ପ୍ରବଳ ଶୀତ ସହ କମ୍ପନ ଦେଇ ଜ୍ୱର ଆସେ |",
            "advice": "1. ରୋଗ ଚିହ୍ନଟ ପାଇଁ ତୁରନ୍ତ ରକ୍ତ ପରୀକ୍ଷା କରାଇ ନିଅନ୍ତୁ |\n2. ଡାକ୍ତରଙ୍କ ପରାମର୍ଶ କ୍ରମେ ତୁରନ୍ତ ଆଣ୍ଟି-ମ୍ୟାଲେରିଆଲ୍ ଔଷଧ ସେବନ କରନ୍ତୁ |\n3. ଅବହେଳା କଲେ ଏହା ପ୍ରାଣଘାତୀ ହୋଇପାରେ, ତେଣୁ ସ୍ୱେଚ୍ଛାଚାରୀ ଔଷଧ ଖାଆନ୍ତୁ ନାହିଁ |",
            "urgency": "Critical"
        },
        "ml": {
            "prediction": "മലേറിയ (അന്തരീക്ഷ പനി)",
            "description": "അനോഫിലസ് കൊതുകുകൾ വഴി പകരുന്ന പരാദരോഗം. കടുത്ത വിറയലോടുകൂടിയ ശക്തമായ പനിയും പിന്നീട് ശരീരം വിയർത്ത് പനി കുറയുന്നതുമാണ് ഇതിന്റെ ലക്ഷണം.",
            "advice": "1. പനി കണ്ടാലുടൻ രക്തപരിശോധന നടത്തി രോഗം സ്ഥിരീകരിക്കുക.\n2. ഡോക്ടറുടെ നിർദ്ദേശാനുസരണം ഉടൻ തന്നെ മലേറിയ മരുന്നുകൾ കഴിച്ചു തുടങ്ങുക.\n3. സ്വയം ചികിത്സ അരുത്; വൈകിയാൽ ഇത് ജീവന് തന്നെ അപകടമാണ്.",
            "urgency": "Critical"
        }
    },
    "Chickenpox": {
        "en": {
            "prediction": "Chickenpox",
            "description": "A highly contagious viral infection caused by the Varicella-Zoster virus, resulting in itchy red skin rashes that develop into fluid-filled blisters.",
            "advice": "1. Isolate fully from non-immune individuals to prevent transmission.\n2. Avoid scratching blisters to prevent bacterial secondary infections and scarring.\n3. Apply cooling calamine lotion to soothe skin itching.\n4. Maintain good hygiene and wear soft cotton clothing.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "चेचक / छोटी माता (Chickenpox)",
            "description": "वेरिसेला-जोस्टर वायरस के कारण होने वाला एक अत्यधिक संक्रामक वायरल संक्रमण। इसमें शरीर पर खुजलीदार लाल दाने होते हैं जो बाद में पानी से भरे छालों (Blisters) में बदल जाते हैं।",
            "advice": "1. संक्रमण को फैलने से रोकने के लिए मरीज को पूरी तरह अलग रखें।\n2. छालों को खुजलाने से बचें, अन्यथा दाग पड़ सकते हैं या संक्रमण फैल सकता है।\n3. खुजली शांत करने के लिए शरीर पर कैलामाइन लोशन लगाएं।\n4. सूती और ढीले कपड़े पहनें तथा स्वच्छता का विशेष ध्यान रखें।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "ఆటలమ్మ (Chickenpox)",
            "description": "వారిసెల్లా-జోస్టర్ వైరస్ వల్ల వచ్చే అత్యంత అంటువ్యాధి. శరీరంపై ఎర్రటి దద్దుర్లు వచ్చి, క్రమంగా నీటి గుల్లలుగా (Blisters) మారుతాయి.",
            "advice": "1. వ్యాధి వ్యాప్తి చెందకుండా రోగిని పూర్తిగా వేరే గదిలో ఉంచండి.\n2. నీటి గుల్లలను అస్సలు గిల్లవద్దు; అలా చేస్తే మచ్చలు పడతాయి లేదా ఇన్ఫెక్షన్ పెరుగుతుంది.\n3. దురదను తగ్గించడానికి శరీరానికి క్యాలమైన్ లోషన్ రాయండి.\n4. వదులుగా ఉండే కాటన్ బట్టలు మాత్రమే ధరించండి.",
            "urgency": "Medium"
        },
        "ta": {
            "prediction": "சின்னம்மை (Chickenpox)",
            "description": "பாரிசெல்லா-ஜோஸ்டர் வைரஸால் ஏற்படும் மிக எளிதாகப் பரவக்கூடிய தொற்று நோய். அரிப்புடன் கூடிய சிவப்பு நிற தடிப்புகள் ஏற்பட்டு நீர் கொப்புளங்களாக மாறும்.",
            "advice": "1. காய்ச்சல் பாதித்தவரை மற்றவர்களிடம் இருந்து முற்றிலும் தனிமைப்படுத்தவும்.\n2. கொப்புளங்களை கிள்ளவோ கீறவோ கூடாது, இது வடுக்கள் மற்றும் தொற்றுக்களை உருவாக்கும்.\n3. அரிப்பைக் குறைக்க கேலமைன் லோஷனைப் பயன்படுத்தவும்.\n4. மென்மையான பருத்தி ஆடைகளை அணியவும் மற்றும் சுகாதாரத்தை பராமரிக்கவும்.",
            "urgency": "Medium"
        },
        "bn": {
            "prediction": "জলবসন্ত (Chickenpox)",
            "description": "ভেরিসেला-জোস্টার ভাইরাস দ্বারা সৃষ্ট অত্যন্ত সংক্রামক রোগ। এর ফলে সারা শরীরে চুলকানিযুক্ত লাল লাল দানা বের হয়, যা পরে জলভর্তি ফোস্কায় পরিণত হয়।",
            "advice": "1. অন্য সবার থেকে রোগীকে সম্পূর্ণ আলাদা রাখুন।\n2. ফোস্কাগুলিতে নখ লাগাবেন না বা চুলকাবেন না, এতে ইনফেকশন ও স্থায়ী দাগ হতে পারে।\n3. চুলকানি কমাতে ক্যালামাইন লোশন লাগাতে পারেন।\n4. হালকা সুতির আলগা পোশাক ব্যবহার করুন এবং রোগীর বিছানা পরিষ্কার রাখুন।",
            "urgency": "Medium"
        },
        "ko": {
            "prediction": "수두 (Chickenpox)",
            "description": "바리셀라-조스터 바이러스에 의한 전염성이 매우 강한 감염 질환입니다. 가려움증을 동반한 붉은 발진이 수포(물집)로 변하고 딱지가 앉는 과정을 거칩니다.",
            "advice": "1. 전염성이 매우 높으므로 발진이 가라앉고 딱지가 앉을 때까지 완전히 격리하십시오.\n2. 2차 세균 감염과 흉터를 예방하기 위해 수포를 절대 긁지 마십시오.\n3. 가려움증 완화를 위해 칼라민 로션을 도포하십시오.\n4. 목욕 시 피부를 문지르지 말고 가볍게 물기를 닦아내십시오.",
            "urgency": "Medium"
        },
        "ur": {
            "prediction": "چکن پاکس (Chickenpox)",
            "description": "ویریسیلا زوسٹر وائرس سے ہونے والا ایک شدید متعدی انفیکشن، جس میں جسم پر خارش زدہ سرخ دانے نکلتے ہیں جو بعد میں پانی بھرے چھالوں کی شکل اختیار کر لیتے ہیں۔",
            "advice": "1. دوسرے افراد سے فاصلہ اختیار کریں تاکہ وائرس نہ پھیلے۔\n2. چھالوں کو نوچنے یا کھجلانے سے گریز کریں تاکہ جلد پر مستقل نشان نہ بنیں۔\n3. خارش کو کم کرنے کے لیے کیلامائن لوشن کا استعمال کریں۔\n4. سوتی اور ڈھیلے کپڑے پہنیں۔",
            "urgency": "Medium"
        },
        "or": {
            "prediction": "ହାଡ଼ଫୁଟି (Chickenpox)",
            "description": "ଭାରିସେଲା-ଜୋଷ୍ଟର ଭୂତାଣୁ ଯୋଗୁଁ ହେଉଥିବା ଏକ ଅତି ସଂକ୍ରାମକ ସଂକ୍ରମଣ | ଏଥିରେ ଦେହରେ କୁଣ୍ଡେଇ ହେବା ସହ ଫୋଟକା ବାହାରିଥାଏ |",
            "advice": "1. ରୋଗୀକୁ ଅନ୍ୟମାନଙ୍କ ଠାରୁ ଅଲଗା ରଖନ୍ତុ |\n2. ଫୋଟକାଗୁଡ଼ିକୁ ଆଦୌ କୁଣ୍ଡାନ୍ତୁ ନାହିଁ, ନଚେତ୍ ଦାଗ ରହିଯିବ |\n3. କୁଣ୍ଡିଆ କମାଇବା ପାଇଁ ଶରୀରରେ କ୍ୟାଲାମାଇନ୍ ଲୋସନ୍ ଲଗାନ୍ତୁ |",
            "urgency": "Medium"
        },
        "ml": {
            "prediction": "ചിക്കൻപോക്സ് (വസൂരി)",
            "description": "വാരിസെല്ല-സോസ്റ്റർ വൈറസ് പരത്തുന്ന പകർച്ചവ്യാധി. ശരീരത്തിൽ ചൊറിച്ചിലുള്ള ചുവന്ന തടിപ്പുകൾ പ്രത്യക്ഷപ്പെടുകയും പിന്നീട് അവ നീർക്കുമിളകളായി മാറുകയും ചെയ്യും.",
            "advice": "1. രോഗിയെ പൂർണ്ണമായും മുറിയിൽ മാറ്റിപ്പാർപ്പിക്കുക.\n2. കുമിളകൾ നഖം കൊണ്ട് പൊട്ടിക്കരുത് (ഇത് സ്ഥിരമായ പാടുകൾ വീഴാൻ കാരണമാകും).\n3. ചൊറിച്ചിൽ മാറാൻ കലാമിൻ ലോഷൻ പുരട്ടുക.",
            "urgency": "Medium"
        }
    },
    "Eczema": {
        "en": {
            "prediction": "Eczema",
            "description": "A chronic inflammatory skin condition marked by a compromised skin barrier, leading to dry, intensely itchy, scaly, and red patches.",
            "advice": "1. Apply thick, fragrance-free moisturizers or barrier creams twice daily.\n2. Avoid harsh chemical soaps, hot water, and synthetic fabrics.\n3. Do not scratch; scratching exacerbates the skin inflammation.\n4. Consult a dermatologist for topical corticosteroid management.",
            "urgency": "Low"
        },
        "hi": {
            "prediction": "एक्जिमा (Eczema)",
            "description": "त्वचा की एक दीर्घकालिक सूजन संबंधी स्थिति (Inflammatory condition), जिसमें त्वचा की सुरक्षात्मक परत कमजोर हो जाती है और त्वचा सूखी, लाल और अत्यधिक खुजलीदार हो जाती है।",
            "advice": "1. दिन में कम से कम दो बार बिना खुशबू वाले मोटे मॉइस्चराइज़र या नारियल का तेल लगाएं।\n2. रासायनिक साबुन, गर्म पानी और सिंथेटिक कपड़ों के उपयोग से बचें।\n3. प्रभावित जगह को बिल्कुल न खुजलाएं; खुजली से सूजन बढ़ती है।\n4. अधिक समस्या होने पर त्वचा विशेषज्ञ (Dermatologist) से परामर्श लें।",
            "urgency": "Low"
        },
        "te": {
            "prediction": "ఎగ్జిమా (Eczema)",
            "description": "చర్మం పొడిబారి, ఎర్రగా మారి, విపరీతమైన దురద పెట్టే దీర్ఘకాలిక చర్మ వ్యాధి. ఇది అంటువ్యాధి కాదు.",
            "advice": "1. రోజుకు కనీసం రెండు సార్లు వాసన లేని మాయిశ్చరైజర్ లేదా కొబ్బరి నూనె రాయండి.\n2. కెమికల్స్ ఎక్కువగా ఉండే సబ్బులు, వేడి నీటి స్నానాలు మరియు సింథటిక్ బట్టలు వాడకండి.\n3. దురద పెడుతున్నా సరే గిల్లవద్దు; గిల్లడం వల్ల చర్మం మరింత పాడవుతుంది.\n4. అవసరాన్ని బట్టి చర్మ వ్యాధి నిపుణుడిని (Dermatologist) సంప్రదించండి.",
            "urgency": "Low"
        },
        "ta": {
            "prediction": "எக்ஸிமா / கரப்பான் நோய்",
            "description": "சரும தடையை பாதிக்கும் நீண்ட கால தோல் அழற்சி நோய். இதனால் தோல் வறண்டு, கடுமையான அரிப்பு மற்றும் சிவப்பு நிற தடிப்புகளுடன் காணப்படும்.",
            "advice": "1. வாசனை இல்லாத தடிமனான ஈரப்பதமூட்டும் கிரீம்களை (Moisturizers) தினமும் இருமுறை தடவவும்.\n2. இரசாயன சோப்புகள், அதிக சுடுநீர் மற்றும் செயற்கை துணிகளை தவிர்க்கவும்.\n3. சொறிய வேண்டாம், இது தோலின் பாதிப்பை அதிகரிக்கும்.\n4. தீவிர பாதிப்பு இருந்தால் தோல் மருத்துவரை அணுகவும்.",
            "urgency": "Low"
        },
        "bn": {
            "prediction": "একজিমা (Eczema)",
            "description": "ত্বকের একটি দীর্ঘমেয়াদী প্রদাহজনিত সমস্যা, যার ফলে ত্বক শুষ্ক, খসখসে, লালচে হয়ে যায় এবং তীব্র চুলকানি অনুভূত হয়। এটি ছোঁয়াচে নয়।",
            "advice": "1. দিনে অন্তত দুবার সুগন্ধিহীন ময়েশ্চারাইজার বা নারকেল তেল ব্যবহার করুন।\n2. ক্ষারযুক্ত সাবান, অতিরিক্ত গরম জল এবং কৃত্রিম কাপড়ের ব্যবহার এড়িয়ে চলুন।\n3. চুলকানো বন্ধ করুন; নখ লাগালে ক্ষত বেড়ে যেতে পারে।\n4. প্রয়োজনে একজন चর্মরোগ विशेषज्ञের পরামর্শ অনুযায়ী মলম ব্যবহার করুন।",
            "urgency": "Low"
        },
        "ko": {
            "prediction": "아토피/습진 (Eczema)",
            "description": "피부 장벽의 손상으로 인해 피부가 매우 건조해지고, 심한 가려움증, 붉은 반점, 비늘 같은 각질이 생기는 만성 염증성 피부 질환입니다.",
            "advice": "1. 향료가 없는 보습제나 크림을 매일 최소 2회 이상 충분히 도포하십시오.\n2. 화학 성분이 강한 비누, 뜨거운 물 샤워, 합성 섬유 의류를 피하십시오.\n3. 피부를 긁지 마십시오. 긁으면 장벽이 파괴되어 2차 감염이 발생할 수 있습니다.\n4. 증상이 심하면 피부과를 찾아 국소 스테로이드제 처방을 받으십시오.",
            "urgency": "Low"
        },
        "ur": {
            "prediction": "ایگزیما (Eczema)",
            "description": "جلد کی ایک دیرینہ بیماری جس میں جلد کی اوپری سطح خشک، کھردری، سرخ ہو جاتی ہے اور اس میں شدید خارش ہوتی ہے۔",
            "advice": "1. دن میں دو بار خوشبو سے پاک موئسچرائزر یا ناریل کا تیل لگائیں।\n2. تیز کیمیکل والے صابن اور گرم پانی کے استعمال سے پرہیز کریں۔\n3. خارش والی جگہ کو ناخنوں سے نہ رگڑیں کیونکہ اس سے سوزش بڑھتی ہے۔\n4. جلد کے ماہر ڈاکٹر سے معائنے کروائیں۔",
            "urgency": "Low"
        },
        "or": {
            "prediction": "ଏକଜିମା (Eczema)",
            "description": "ଚର୍ମର ଏକ ଦୀର୍ଘକାଳୀନ ପ୍ରଦାହ ଜନିତ ସମସ୍ୟା | ଏଥିରେ ଚର୍ମ ଶୁଖିଲା ହୋଇଯାଏ ଓ ପ୍ରବଳ କୁଣ୍ଡେଇ ହୁଏ |",
            "advice": "1. ଦିନକୁ ଅନ୍ତତଃ ଦୁଇଥର ଭଲ ମଶ୍ଚରାଇଜର୍ କିମ୍ବା ନଡ଼ିଆ ତେଲ ବ୍ୟବହାର କରନ୍ତୁ |\n2. କେମିକାଲ୍ ଯୁକ୍ତ ସାବୁନ ଓ ଗରମ ପାଣି ବ୍ୟବହାର କରନ୍ତୁ ନାହିଁ |\n3. ପ୍ରଭାବିତ ସ୍ଥାନକୁ ଆଦୌ କୁଣ୍ଡାନ୍ତୁ ନାହିଁ |",
            "urgency": "Low"
        },
        "ml": {
            "prediction": "എക്സിമ (കരപ്പൻ രോഗം)",
            "description": "ചർമ്മത്തിന്റെ സ്വാഭാവിക ഈർപ്പം നഷ്ടപ്പെടുകയും ചൊറിച്ചിലും ചുവന്ന പാടുകളും കായകളും ഉണ്ടാകുകയും ചെയ്യുന്ന വിട്ടുമാറാത്ത ചർമ്മരോഗം.",
            "advice": "1. ദിവസവും രണ്ടു തവണയെങ്കിലും വാസനയില്ലാത്ത മോയ്സ്ചറൈസർ ക്രീമുകൾ പുരട്ടുക.\n2. രാസവസ്തുക്കൾ അടങ്ങിയ സോപ്പുകളും ചൂടുവെള്ളത്തിലുള്ള കുളിയും ഒഴിവാക്കുക.\n3. ചൊറിയുന്നത് ഒഴിവാക്കുക (ഇത് ചർമ്മത്തിന് കൂടുതൽ കേടുപാടുകൾ വരുത്തും).",
            "urgency": "Low"
        }
    },
    "Food Allergy": {
        "en": {
            "prediction": "Food Allergy",
            "description": "An immune system hypersensitivity triggered by consuming certain food proteins, manifesting as hives, swelling, or nausea.",
            "advice": "1. Identify and strictly avoid the allergen food (nuts, dairy, shellfish, etc.).\n2. Carry emergency antihistamines if symptoms are recurrent.\n3. Educate family and friends about the allergy.\n4. Call emergency services immediately if lips swell or you experience chest tightness.",
            "urgency": "High"
        },
        "hi": {
            "prediction": "खाद्य एलर्जी (Food Allergy)",
            "description": "किसी विशेष खाद्य पदार्थ (जैसे मूंगफली, दूध, अंडा, सीफूड) में मौजूद प्रोटीन के प्रति प्रतिरक्षा प्रणाली (Immune System) की अतिसंवेदनशीलता। इसके लक्षणों में पित्ती (Hives), चेहरे पर सूजन या मतली शामिल हैं।",
            "advice": "1. एलर्जी पैदा करने वाले खाद्य पदार्थ की पहचान करें और उससे पूरी तरह दूर रहें।\n2. यदि पहले भी तीव्र प्रतिक्रिया हुई हो, तो आपातकालीन दवाएं पास रखें।\n3. होटल या किसी के घर भोजन करने से पहले एलर्जी के बारे में स्पष्ट बताएं।\n4. यदि होंठ या जीभ सूज जाए या सांस लेने में दिक्कत हो, तो तुरंत आपातकालीन चिकित्सा प्राप्त करें।",
            "urgency": "High"
        },
        "te": {
            "prediction": "ఆహార అలెర్జీ (Food Allergy)",
            "description": "కొన్ని రకాల ఆహార పదార్థాలు (వేరుశెనగ, పాలు, గుడ్లు మొదలైనవి) తిన్నప్పుడు శరీర రోగనిరోధక వ్యవస్థ చూపే తీవ్ర ప్రతిచర్య. దీనివల్ల పెదాల వాపు, దద్దుర్లు రావచ్చు.",
            "advice": "1. అలెర్జీ కలిగించే ఆహార పదార్థాన్ని గుర్తించి, దాన్ని తినడం పూర్తిగా మానేయండి.\n2. ప్యాక్ చేసిన ఆహారాన్ని కొనేటప్పుడు లేబుల్స్ జాగ్రత్తగా చదవండి.\n3. అలెర్జీ లక్షణాలు కనిపించినప్పుడు వాడటానికి యాంటీ-అలెర్జీ టాబ్లెట్లు అందుబాటులో ఉంచుకోండి.\n4. పెదాలు లేదా నాలుక వాపు వచ్చి, శ్వాస తీసుకోవడం కష్టమైతే వెంటనే ఆసుపత్రికి వెళ్ళండి.",
            "urgency": "High"
        },
        "ta": {
            "prediction": "உணவு ஒவ்வாமை (Food Allergy)",
            "description": "குறிப்பிட்ட சில உணவுப் பொருட்களை உட்கொள்வதால் உடலின் நோய் எதிர்ப்பு மண்டலம் காட்டும் ஒவ்வாமை எதிர்வினை. உதடு வீக்கம், தோல் அரிப்பு ஆகியவை இதன் அறிகுறிகள்.",
            "advice": "1. ஒவ்வாமையை ஏற்படுத்தும் உணவுகளை (கடலை, முட்டை, கடல் உணவுகள்) கண்டறிந்து முற்றிலுமாக தவிர்க்கவும்.\n2. உணவு வாங்கும் போது லேபிள்களை கவனமாகப் படித்து வாங்கவும்.\n3. முந்தைய ஒவ்வாமை பாதிப்பு இருப்பின் அதற்கான அவசர கால மருந்துகளை வைத்திருக்கவும்.\n4. மூச்சுத்திணறல் அல்லது உதடு வீக்கம் ஏற்பட்டால் உடனடியாக அவசர சிகிச்சையை நாடவும்.",
            "urgency": "High"
        },
        "bn": {
            "prediction": "খাদ্য অ্যালার্জি (Food Allergy)",
            "description": "নির্দিষ্ট কোনো খাবার (যেমন চীনাবাদাম, চিংড়ি, ডিম বা দুধ) খাওয়ার পর শরীরের রোগ প্রতিরোধ ব্যবস্থার অস্বাভাবিক প্রতিক্রিয়া। এর ফলে ঠোঁট ফোলা, চুলকানি বা বমি হতে পারে।",
            "advice": "1. অ্যালার্জি সৃষ্টিকারী খাবারটি চিহ্নিত করুন এবং তা খাওয়া সম্পূর্ণরূপে বর্জন করুন।\n2. যেকোনো প্রক্রিয়াজাত খাবার কেনার আগে প্যাকেটের গায়ে লেখা উপাদানগুলি ভালোভাবে পড়ুন।\n3. অ্যালার্জি বেশি হলে তাৎক্ষণিক ব্যবহারের জন্য প্রয়োজনীয় অ্যান্টি-অ্যালার্জি ওষুধ সঙ্গে রাখুন।\n4. শ্বাসকষ্ট হলে বা মুখ ও জিব ফুলে উঠলে দেরি না করে দ্রুত জরুরি চিকিৎসা নিন।",
            "urgency": "High"
        },
        "ko": {
            "prediction": "식품 알레르기 (Food Allergy)",
            "description": "특정 식품(땅콩, 우유, 달걀, 갑각류 등)의 단백질에 대해 몸의 면역계가 과민 반응을 일으키는 질환입니다. 두드러기, 입술 부종, 구토 등이 유발될 수 있습니다.",
            "advice": "1. 알레르기 유발 식품을 정확히 진단받고, 해당 성분이 포함된 모든 음식의 섭취를 엄격히 제한하십시오.\n2. 가공식품 구매 시 제품 뒷면의 식품 알레르기 유발 물질 표시를 반드시 확인하십시오.\n3. 알레르기 반응 시 대처를 위해 비상 약물(항히스타민제 등)을 소지하십시오.\n4. 호흡 곤란이나 목구멍 및 입술 부종 등 아나필락시스 증상이 나타나면 즉시 응급실로 가십시오.",
            "urgency": "High"
        },
        "ur": {
            "prediction": "فوڈ الرجی (Food Allergy)",
            "description": "مخصوص غذاؤں (جیسے مونگ پھلی, دودھ، انڈا، یا مچھلی) کے استعمال پر قوت مدافعت کا شدید ردعمل، جس سے جسم پر سوجن، دل خراب ہونا، یا خارش ہو سکتی ہے۔",
            "advice": "1. الرجی پیدا کرنے والی غذا کی پہچان کریں اور اس کے استعمال سے پرہیز کریں۔\n2. باہر کھانا کھاتے وقت احتیاط کریں اور الرجی کے بارے میں آگاہ کریں۔\n3. ہونٹوں یا زبان پر سوجن ہونے کی صورت میں فوری طور پر قریبی ڈاکٹر سے رجوع کریں۔",
            "urgency": "High"
        },
        "or": {
            "prediction": "ଖାଦ୍ୟ ଆଲର୍ଜି (Food Allergy)",
            "description": "କେତେକ ନିର୍ଦ୍ଦିଷ୍ଟ ଖାଦ୍ୟ ଖାଇବା ଦ୍ୱାରା ଶରୀରର ରୋଗ ପ୍ରତିରୋଧକ ଶକ୍ତି ଦ୍ୱାରା ସୃଷ୍ଟି ହେଉଥିବା ଆଲର୍ଜି ପ୍ରତିକ୍ରିୟା | ଏଥିରେ ଓଠ ଫୁଲିଯିବା ବା ଚକତ୍ତେ ବାହାରିବା ଦେଖାଯାଏ |",
            "advice": "1. ଆଲର୍ଜି କରାଉଥିବା ଖାଦ୍ୟ ଚିହ୍ନଟ କରି ସେଥିରୁ ସମ୍ପୂର୍ଣ୍ଣ ଦୂରେଇ ରୁହନ୍ତୁ |\n2. ବାହାରେ ଖାଇବା ପୂର୍ବରୁ ସାବଧାନ ରୁହନ୍ତୁ |\n3. ଓଠ କିମ୍ବା ଜିଭ ଫୁଲିଗଲେ ତୁରନ୍ତ ଡାକ୍ତରଖାନା ଯାଆନ୍ତୁ |",
            "urgency": "High"
        },
        "ml": {
            "prediction": "ഭക്ഷണ അലർജി (Food Allergy)",
            "description": "ചില തരം ഭക്ഷണങ്ങൾ (കശുവണ്ടി, പാൽ, മുട്ട, ചെമ്മീൻ മുതലായവ) കഴിക്കുമ്പോൾ ശരീരത്തിന്റെ പ്രതിരോധ സംവിധാനം ഉണ്ടാക്കുന്ന അമിതമായ പ്രതിപ്രവർത്തനം.",
            "advice": "1. അലർജി ഉണ്ടാക്കുന്ന ഭക്ഷണങ്ങൾ കണ്ടെത്തി അവ പൂർണ്ണമായും ഒഴിവാക്കുക.\n2. പാക്കേജ് ചെയ്ത ഭക്ഷണങ്ങൾ വാങ്ങുമ്പോൾ അതിലെ ചേരുവകൾ ശ്രദ്ധാപൂർവ്വം വായിക്കുക.\n3. മുഖത്തോ ചുണ്ടിലോ വാക്കോ ഉണ്ടാകുന്ന വീക്കം, ശ്വാസതടസ്സം എന്നിവ ഉണ്ടായാൽ ഉടൻ അടിയന്തര ചികിത്സ തേടുക.",
            "urgency": "High"
        }
    },
    "Migraine": {
        "en": {
            "prediction": "Migraine",
            "description": "A complex neurological disorder characterized by recurrent, severe headaches, often localized to one side, frequently accompanied by nausea and light/sound sensitivity.",
            "advice": "1. Rest in a dark, quiet, well-ventilated room.\n2. Apply a cold compress to your forehead or the temples.\n3. Hydrate actively; avoid caffeine withdrawal or trigger foods (chocolate, aged cheese).\n4. Consult a physician for acute and preventive pharmacological therapies.",
            "urgency": "Medium"
        },
        "hi": {
            "prediction": "माइग्रेन (आधासीसी)",
            "description": "एक न्यूरोलॉजिकल विकार जिसमें सिर के एक हिस्से में तेज, धड़कता हुआ दर्द होता है। इसके साथ मतली, उल्टी, और तेज रोशनी या आवाज के प्रति संवेदनशीलता हो सकती है।",
            "advice": "1. एक अंधेरे, शांत और हवादार कमरे में आराम करें।\n2. सिर या माथे पर ठंडी पट्टी (Cold compress) रखें।\n3. भरपूर पानी पीकर खुद को हाइड्रेटेड रखें।\n4. उन चीजों (तेज धूप, शोर, चाय/कॉफी की कमी) से बचें जो दर्द को बढ़ाती हैं।",
            "urgency": "Medium"
        },
        "te": {
            "prediction": "మైగ్రేన్ (Migraine)",
            "description": "తల భాగంలో ఒక వైపు వచ్చే తీవ్రమైన, గుచ్చుకున్నట్లు ఉండే తలనొప్పి. దీనితో పాటు వాంతులు కావడం, వెలుతురు లేదా శబ్దం భరించలేకపోవడం జరుగుతుంది.",
            "advice": "1. ప్రశాంతంగా, చీకటిగా ఉన్న గదిలో విశ్రాంతి తీసుకోండి.\n2. నుదుటిపై లేదా తల వెనుక తడి బట్ట లేదా ఐస్ ప్యాక్ పెట్టుకోండి.\n3. శరీరంలో నీటి శాతం తగ్గకుండా చూసుకోండి.\n4. నిద్రలేమి, విపరీతమైన ఒత్తిడి మరియు మైగ్రేన్ పెంచే ఆహారాలకు దూరంగా ఉండండి.",
            "urgency": "Medium"
        },
        "ta": {
            "prediction": "ஒற்றைத் தலைவலி (Migraine)",
            "description": "தலைவலி மற்றும் நரம்பு மண்டலம் சார்ந்த கோளாறு. பொதுவாக தலையின் ஒரு பக்கத்தில் கடுமையான துடிப்பு போன்ற வலி, வாந்தி மற்றும் வெளிச்சம்/ஒலியின் மீதான ஒவ்வாமை ஏற்படும்.",
            "advice": "1. அமைதியான, இருட்டான அறையில் படுத்து ஓய்வெடுக்கவும்.\n2. நெற்றியில் குளிர்ந்த ஒத்தடம் கொடுக்கவும்.\n3. நீர்ச்சத்து குறையாமல் பார்த்துக் கொள்ளவும், காஃபின் பயன்பாட்டை குறைக்கவும்.\n4. வலி குறையவில்லை எனில் மருத்துவரை அணுகவும்.",
            "urgency": "Medium"
        },
        "bn": {
            "prediction": "মাইগ্রেন (Migraine)",
            "description": "একটি জটিল স্নায়বিক সমস্যা যার কারণে মাথার যেকোনো একদিকে তীব্র ও স্পন্দনশীল ব্যথা হয়। এর সাথে বমি বমি ভাব এবং আলো বা শব্দের প্রতি সংবেদনশীলতা থাকে।",
            "advice": "1. একটি অন্ধকার ও শান্ত ঘরে নিরিবিলিতে বিশ্রাম নিন।\n2. কপালে বা ঘাড়ের পেছনে ঠান্ডা কাপড়ের ভাপ বা বরফ ব্যাগ দিন।\n3. পর্যাপ্ত জল পান করুন এবং নির্দিষ্ট সময়ে ঘুমানোর অভ্যাস করুন।\n4. তীব্র রোদে ছাতা ব্যবহার করুন এবং অতিরিক্ত চা বা কফি খাওয়া পরিহার করুন।",
            "urgency": "Medium"
        },
        "ko": {
            "prediction": "편두통 (Migraine)",
            "description": "주로 머리의 한쪽에서 박동성(쿵쾅거리는 느낌) 통증이 반복적으로 발생하며, 오심(메스꺼움), 구토 및 빛이나 소리에 대한 과민 반응을 동반하는 만성 신경학적 두통 질환입니다.",
            "advice": "1. 불빛을 끄고 어둡고 조용한 방에서 안정을 취하십시오.\n2. 관자놀이나 이마 부위에 차가운 냉찜질을 하십시오.\n3. 탈수가 두통을 유발할 수 있으므로 물을 충분히 섭취하십시오.\n4. 수면 부족, 카페인 과다 섭취 등 자신만의 편두통 유발 요인을 기록하고 피하십시오.",
            "urgency": "Medium"
        },
        "ur": {
            "prediction": "آدھے سر کا درد (Migraine)",
            "description": "ایک اعصابی بیماری جس میں سر کے ایک حصے میں شدید اور ٹیسیں مارنے والا درد ہوتا ہے، جس کے ساتھ متلی اور تیز روشنی یا آواز سے چڑچڑاہٹ ہوتی ہے۔",
            "advice": "1. اندھیرے اور پرسکون کمرے میں لیٹ کر آرام کریں۔\n2. سر پر ٹھنڈی پٹی یا برف کا استعمال کریں۔\n3. پانی زیادہ پیئیں اور کیفین کا استعمال کم کریں۔\n4. وقت پر سونے اور جاگنے کی عادت ڈالیں۔",
            "urgency": "Medium"
        },
        "or": {
            "prediction": "ମାଇଗ୍ରେନ୍ (Migraine)",
            "description": "ମୁଣ୍ଡର ଗୋଟିଏ ପାର୍ଶ୍ୱରେ ହେଉଥିବା ପ୍ରବଳ ମୁଣ୍ଡବିନ୍ଧା | ଏହି ସହିତ ବାନ୍ତି ଲାଗିବା ଏବଂ ଅଧିକ ଆଲୋକ ବା ଶବ୍ଦରେ କଷ୍ଟ ହେବା ଦେଖାଯାଏ |",
            "advice": "1. ଅନ୍ଧାରିଆ ଓ ଶାନ୍ତ କୋଠରୀରେ ବିଶ୍ରାମ କରନ୍ତୁ |\n2. ମୁଣ୍ଡରେ କିମ୍ବା କପାଳରେ ଥଣ୍ଡା ପାଣି ପଟି ଦିଅନ୍ତୁ |\n3. ପ୍ରଚୁର ପରିମାଣରେ ପାଣି ପିଅନ୍ତୁ |\n4. ଅଧିକ ସମୟ ଖରାରେ ରୁହନ୍ତୁ ନାହିଁ |",
            "urgency": "Medium"
        },
        "ml": {
            "prediction": "ഒറ്റത്തലവേദന (Migraine)",
            "description": "തലയുടെ ഒരു ഭാഗത്തുണ്ടാകുന്ന കടുത്ത വേദനയോടൊപ്പം ഓക്കാനം, വെളിച്ചവും ശബ്ദവും സഹിക്കാൻ കഴിയാത്ത അവസ്ഥ എന്നിവയുണ്ടാക്കുന്ന വിട്ടുമാറാത്ത തലവേദന.",
            "advice": "1. ഇരുണ്ടതും ശാന്തവുമായ ഒരു മുറിയിൽ വിശ്രമിക്കുക.\n2. நெറ്റിയിലോ തലയിലോ തണുത്ത വെള്ളത്തിൽ മുക്കിയ തുണി വെക്കുക (Cold compress).\n3. നിർജ്ജലീകരണം ഒഴിവാക്കാൻ ആവശ്യത്തിന് വെള്ളം കുടിക്കുക.",
            "urgency": "Medium"
        }
    }
}


def load_models():
    """Load the models from disk, caching them in memory."""
    global _symptom_model, _symptoms_list, _image_model
    
    # Load symptom model
    if _symptom_model is None or _symptoms_list is None:
        if os.path.exists(SYMPTOM_MODEL_PATH) and os.path.exists(SYMPTOMS_LIST_PATH):
            with open(SYMPTOM_MODEL_PATH, "rb") as f:
                _symptom_model = pickle.load(f)
            with open(SYMPTOMS_LIST_PATH, "rb") as f:
                _symptoms_list = pickle.load(f)
        else:
            print("Symptom models not found. Please run train_models.py first!")

    # Load image model
    if _image_model is None:
        if os.path.exists(IMAGE_MODEL_PATH):
            with open(IMAGE_MODEL_PATH, "rb") as f:
                _image_model = pickle.load(f)
        else:
            print("Image model not found. Please run train_models.py first!")


def extract_symptoms_from_text(text, lang="en"):
    """Parse text query to extract symptom keywords, supporting multiple languages."""
    text_lower = text.lower()
    matched_symptoms = []
    
    # 1. Match using chosen language vocabulary
    vocab = SYMPTOM_VOCAB.get(lang, SYMPTOM_VOCAB["en"])
    for symptom_key, terms in vocab.items():
        for term in terms:
            pattern = r'\b' + re.escape(term) + r'\b'
            if re.search(pattern, text_lower) or term in text_lower:
                matched_symptoms.append(symptom_key)
                break
                
    # 2. Hybrid Fallback: Also match using English vocabulary (in case of mixed-language inputs)
    if lang != "en":
        eng_vocab = SYMPTOM_VOCAB["en"]
        for symptom_key, terms in eng_vocab.items():
            if symptom_key in matched_symptoms:
                continue
            for term in terms:
                pattern = r'\b' + re.escape(term) + r'\b'
                if re.search(pattern, text_lower) or term in text_lower:
                    matched_symptoms.append(symptom_key)
                    break
                    
    return list(set(matched_symptoms))


def _compute_rule_scores(symptom_keys):
    """Score each disease using weighted symptom overlap and signature requirements."""
    symptom_set = set(symptom_keys)
    scores = {}

    for disease, disease_syms in disease_symptoms.items():
        matched = symptom_set & set(disease_syms)
        if not matched:
            scores[disease] = 0.0
            continue

        signature = DISEASE_SIGNATURE.get(disease, set())
        if signature and not (symptom_set & signature):
            # Disease needs a defining symptom that wasn't reported — heavy penalty
            penalty = 0.08
        else:
            penalty = 1.0

        weighted_match = sum(SYMPTOM_WEIGHTS.get(s, 1.0) for s in matched)
        weighted_profile = sum(SYMPTOM_WEIGHTS.get(s, 1.0) for s in disease_syms)
        coverage = len(matched) / len(disease_syms)
        specificity = weighted_match / max(weighted_profile, 1.0)

        # Boost when multiple non-generic symptoms match
        specific_count = len(matched - GENERIC_SYMPTOMS)
        specificity_bonus = 1.0 + (specific_count * 0.15)

        scores[disease] = (coverage * 0.35 + specificity * 0.65) * penalty * specificity_bonus

    return scores


def _normalize_scores(score_dict):
    """Convert raw scores to probability-like distribution."""
    total = sum(score_dict.values())
    if total <= 0:
        n = len(score_dict)
        return {k: 1.0 / n for k in score_dict}
    return {k: v / total for k, v in score_dict.items()}


def _blend_predictions(ml_probs, rule_probs, symptom_count):
    """Blend ML and rule-based scores; trust rules more when symptoms are sparse."""
    if symptom_count <= 1:
        ml_weight, rule_weight = 0.15, 0.85
    elif symptom_count == 2:
        ml_weight, rule_weight = 0.35, 0.65
    else:
        ml_weight, rule_weight = 0.55, 0.45

    all_diseases = set(ml_probs.keys()) | set(rule_probs.keys())
    blended = {}
    for disease in all_diseases:
        ml_val = ml_probs.get(disease, 0.0)
        rule_val = rule_probs.get(disease, 0.0)
        blended[disease] = ml_val * ml_weight + rule_val * rule_weight

    return _normalize_scores(blended)


def _get_follow_up_questions(symptom_keys, lang="en"):
    """Generate contextual follow-up questions based on detected symptoms."""
    questions = []
    seen = set()

    for sym in symptom_keys:
        for q in FOLLOW_UP_BY_SYMPTOM.get(sym, []):
            if q not in seen:
                questions.append(q)
                seen.add(q)

    if not questions and symptom_keys:
        questions = FOLLOW_UP_BY_SYMPTOM.get("fever", [])[:3]

    # Keep top 4 most relevant
    return questions[:4]


def _detect_red_flags(symptom_keys):
    """Return red-flag warnings based on symptom combinations."""
    symptom_set = set(symptom_keys)
    flags = []
    for required, message in RED_FLAG_RULES:
        if required.issubset(symptom_set):
            flags.append(message)
    return flags


def _determine_prediction_mode(symptom_keys, confidence, top_disease):
    """Classify how reliable the current prediction is."""
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


def _get_care_level(urgency, red_flags, prediction_mode):
    """Map urgency and flags to actionable care guidance."""
    if red_flags or urgency in ("Critical", "High"):
        return "seek_emergency"
    if urgency == "Medium" or prediction_mode == "differential":
        return "see_doctor_soon"
    if prediction_mode == "insufficient":
        return "monitor_and_report"
    return "home_care_ok"


CARE_LEVEL_TEXT = {
    "seek_emergency": {
        "en": "🚨 **Action:** Seek emergency medical care immediately.",
        "hi": "🚨 **कार्रवाई:** तुरंत आपातकालीन चिकित्सा सहायता लें।",
        "te": "🚨 **చర్య:** వెంటనే అత్యవసర వైద్య సహాయం పొందండి.",
        "or": "🚨 **କାର୍ଯ୍ୟ:** ତୁରନ୍ତ ଡାକ୍ତରଖାନା ଯାଆନ୍ତୁ |"
    },
    "see_doctor_soon": {
        "en": "🏥 **Action:** Consult a doctor within 24–48 hours if symptoms persist or worsen.",
        "hi": "🏥 **कार्रवाई:** यदि लक्षण बने रहें या बढ़ें, तो 24–48 घंटे में डॉक्टर से मिलें।",
        "te": "🏥 **చర్య:** లక్షణాలు కొనసాగితే 24–48 గంటలలో డాక్టరును సంప్రదించండి.",
        "or": "🏥 **କାର୍ଯ୍ୟ:** ଲକ୍ଷଣ ବଢ଼ିଲେ ୨୪-୪୮ ଘଣ୍ଟା ମଧ୍ୟରେ ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ |"
    },
    "monitor_and_report": {
        "en": "👁️ **Action:** Monitor at home, log vitals, and describe any additional symptoms for a clearer diagnosis.",
        "hi": "👁️ **कार्रवाई:** घर पर निगरानी करें, वाइटल्स लॉग करें, और अधिक लक्षण बताएं।",
        "te": "👁️ **చర్య:** ఇంట్లో పర్యవేక్షించండి, వైటల్స్ నమోదు చేయండి, మరిన్ని లక్షణాలు చెప్పండి.",
        "or": "👁️ **କାର୍ଯ୍ୟ:** ଘରେ ନିରୀକ୍ଷଣ କରନ୍ତୁ, ଅଧିକ ଲକ୍ଷଣ ଜଣାନ୍ତୁ |"
    },
    "home_care_ok": {
        "en": "✅ **Action:** Home rest and hydration are appropriate; watch for worsening signs.",
        "hi": "✅ **कार्रवाई:** घर पर आराम और हाइड्रेशन पर्याप्त है; बिगड़ते लक्षणों पर ध्यान दें।",
        "te": "✅ **చర్య:** ఇంట్లో విశ్రాంతి, ద్రవాలు తీసుకోండి; మెరుగుపడకపోతే డాక్టరును సంప్రదించండి.",
        "or": "✅ **କାର୍ଯ୍ୟ:** ଘରେ ବିଶ୍ରାମ ନିଅନ୍ତୁ; ଲକ୍ଷଣ ବଢ଼ିଲେ ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ |"
    }
}


def predict_disease(symptom_keys, lang="en"):
    """Predict disease using hybrid ML + clinical rule engine with calibrated confidence."""
    load_models()

    if _symptom_model is None or _symptoms_list is None:
        return {"error": "Symptom prediction model is not trained/loaded."}

    if not symptom_keys:
        translations = {
            "en": "Please list your symptoms (e.g. fever, cough) for an analysis.",
            "hi": "कृपया विश्लेषण के लिए अपने लक्षणों (जैसे बुखार, खांसी) को बताएं।",
            "te": "దయచేసి విశ్లేషణ కొరకు మీ లక్షణాలను (జ్వరం, దగ్గు వంటివి) తెలపండి.",
            "ta": "தயவுசெய்து பகுப்பாய்விற்காக உங்கள் அறிகுறிகளை (காய்ச்சல், இருமல்) குறிப்பிடவும்.",
            "bn": "অনুগ্রহ করে বিশ্লেষণের জন্য আপনার উপসর্গগুলি (যেমন জ্বর, কাশি) উল্লেখ করুন।",
            "ko": "분석을 위해 증상(예: 열, 기침)을 나열해 주십시오.",
            "ur": "براہ کرم تجزیہ کے لیے اپنی علامات (جیسے بخار، کھانسی) بتائیں۔",
            "or": "ଦୟାକରି ବିଶ୍ଳେଷଣ ପାଇଁ ଆପଣଙ୍କର ଲକ୍ଷଣ (ଜ୍ୱର, କାଶ ଇତ୍ୟାଦି) ଲେଖନ୍ତୁ |",
            "ml": "പരിശോധനയ്ക്കായി നിങ്ങളുടെ ലക്ഷണങ്ങൾ (പനി, ചുമ പോലുള്ളവ) ദയവായി പറയുക."
        }
        return {
            "prediction": "No Symptoms Detected",
            "confidence": 0.0,
            "description": translations.get(lang, translations["en"]),
            "advice": "",
            "urgency": "None",
            "probabilities": {},
            "prediction_mode": "none",
            "follow_up_questions": [],
            "red_flags": [],
            "care_level": "monitor_and_report"
        }

    # Clinical Guardrail: Intercept single "fever" input to prevent false alarms
    if len(symptom_keys) == 1 and "fever" in symptom_keys:
        viral_fever_info = {
            "en": {
                "prediction": "Viral Fever / Mild Flu",
                "description": "You reported only a fever. While fever is a common symptom for many conditions, it is most frequently associated with a common viral fever or flu when no secondary symptoms (like skin rashes, chest tightness, or vomiting) are present. Please monitor your symptoms.",
                "advice": "1. Rest extensively and avoid physical strain.\n2. Stay hydrated with clean water, ORS, or warm broths.\n3. Take paracetamol under medical advisory if temperature rises.\n4. Log your temperature every 4 hours using the Vitals tab.",
                "urgency": "Low"
            },
            "hi": {
                "prediction": "वायरल बुखार / हल्का फ्लू",
                "description": "आपने केवल बुखार की शिकायत की है। हालांकि बुखार कई बीमारियों का लक्षण है, लेकिन जब अन्य लक्षण (जैसे लाल चकत्ते, गंभीर बदन दर्द, या सांस लेने में परेशानी) मौजूद न हों, तो यह आमतौर पर एक सामान्य वायरल बुखार या हल्का फ्लू होता है।",
                "advice": "1. बिस्तर पर आराम करें और शारीरिक परिश्रम से बचें।\n2. पानी, ओआरएस या गर्म सूप पीकर खुद को हाइड्रेटेड रखें।\n3. तापमान बढ़ने पर डॉक्टर की सलाह पर पैरासिटामोल लें।\n4. वाइटल्स टैब का उपयोग करके हर 4 घंटे में अपना तापमान दर्ज करें।",
                "urgency": "Low"
            },
            "te": {
                "prediction": "వైరల్ జ్వరం / సాధారణ ఫ్లూ",
                "description": "మీరు కేవలం జ్వరం మాత్రమే ఉన్నట్లు తెలిపారు. చర్మంపై దద్దుర్లు, తీవ్రమైన ఒళ్ళు నొప్పులు లేదా శ్వాస ఇబ్బంది వంటి ఇతర అనుబంధ లక్షణాలు లేనప్పుడు, ఇది సాధారణంగా ఒక వైరల్ జ్వరం లేదా సాధారణ ఫ్లూ కావచ్చు.",
                "advice": "1. బాగా విశ్రాంతి తీసుకోండి, ఎలాంటి శారీరక శ్రమ చేయవద్దు.\n2. నీరు, కొబ్బరి నీరు లేదా వేడి సూప్‌లు ఎక్కువగా తాగుతూ ఉండండి.\n3. జ్వరం తగ్గడానికి అవసరమైతే వైద్యుల సలహాతో పారాసిటమాల్ తీసుకోండి.\n4. Vitals ట్యాబ్ ఉపయోగించి ప్రతి 4 గంటలకు ఒకసారి జ్వరాన్ని నమోదు చేసుకోండి.",
                "urgency": "Low"
            }
        }
        info = viral_fever_info.get(lang, viral_fever_info["en"])
        return {
            "prediction": info["prediction"],
            "confidence": 0.75,
            "description": info["description"],
            "advice": info["advice"],
            "urgency": info["urgency"],
            "probabilities": {info["prediction"]: 0.75, "Influenza": 0.15, "Common Cold": 0.10},
            "prediction_mode": "insufficient",
            "follow_up_questions": [
                "Do you have a skin rash or blisters?",
                "Do you have severe joint pain or muscle ache?",
                "Do you have chills, shivering, or sweats?"
            ],
            "red_flags": [],
            "care_level": "monitor_and_report",
            "care_guidance": CARE_LEVEL_TEXT["monitor_and_report"].get(lang, CARE_LEVEL_TEXT["monitor_and_report"]["en"]),
            "detected_symptom_count": 1
        }

    # --- ML prediction ---
    vector = [1 if sym in symptom_keys else 0 for sym in _symptoms_list]
    vector = np.array(vector).reshape(1, -1)
    ml_prediction = _symptom_model.predict(vector)[0]
    ml_probabilities = _symptom_model.predict_proba(vector)[0]
    ml_classes = _symptom_model.classes_
    ml_probs = {ml_classes[i]: float(ml_probabilities[i]) for i in range(len(ml_classes))}

    # --- Rule-based prediction ---
    rule_scores = _compute_rule_scores(symptom_keys)
    rule_probs = _normalize_scores(rule_scores)

    # --- Blend both engines ---
    blended_probs = _blend_predictions(ml_probs, rule_probs, len(symptom_keys))
    sorted_probs = sorted(blended_probs.items(), key=lambda x: x[1], reverse=True)
    top_disease = sorted_probs[0][0]
    raw_confidence = sorted_probs[0][1]

    prediction_mode = _determine_prediction_mode(symptom_keys, raw_confidence, top_disease)

    # Calibrate confidence — never show high confidence on sparse/generic input
    if prediction_mode == "insufficient":
        confidence = min(raw_confidence, 0.32)
        top_disease = "General Febrile Illness"
    elif prediction_mode == "differential":
        confidence = min(raw_confidence, 0.55)
    else:
        confidence = raw_confidence

    red_flags = _detect_red_flags(symptom_keys)
    follow_ups = _get_follow_up_questions(symptom_keys, lang)

    # Build top probability dict (filter noise)
    top_probs = {k: round(v, 4) for k, v in sorted_probs if v > 0.02}

    # Fetch disease info
    if top_disease == "General Febrile Illness":
        info = {
            "prediction": INSUFFICIENT_SYMPTOM_LABELS.get(lang, INSUFFICIENT_SYMPTOM_LABELS["en"]),
            "description": _get_insufficient_description(symptom_keys, lang),
            "advice": _get_insufficient_advice(lang),
            "urgency": "Low"
        }
    else:
        all_lang_info = DISEASE_INFO.get(top_disease, {})
        info = all_lang_info.get(lang, all_lang_info.get("en", {
            "prediction": top_disease,
            "description": "Unknown condition.",
            "advice": "Please consult a doctor.",
            "urgency": "Medium"
        }))

    care_level = _get_care_level(info["urgency"], red_flags, prediction_mode)

    # Translate probability keys
    translated_top_probs = {}
    for k, v in top_probs.items():
        if k == "General Febrile Illness":
            label = INSUFFICIENT_SYMPTOM_LABELS.get(lang, INSUFFICIENT_SYMPTOM_LABELS["en"])
        else:
            label = DISEASE_INFO.get(k, {}).get(lang, {}).get("prediction", k)
        translated_top_probs[label] = v

    return {
        "prediction": info["prediction"],
        "confidence": round(confidence, 4),
        "description": info["description"],
        "advice": info["advice"],
        "urgency": info["urgency"],
        "probabilities": translated_top_probs,
        "prediction_mode": prediction_mode,
        "follow_up_questions": follow_ups,
        "red_flags": red_flags,
        "care_level": care_level,
        "care_guidance": CARE_LEVEL_TEXT.get(care_level, CARE_LEVEL_TEXT["monitor_and_report"]).get(lang,
            CARE_LEVEL_TEXT.get(care_level, CARE_LEVEL_TEXT["monitor_and_report"])["en"]),
        "detected_symptom_count": len(symptom_keys)
    }


def _get_insufficient_description(symptom_keys, lang):
    """Explain why a definitive diagnosis isn't possible yet."""
    sym_names = ", ".join(s.replace("_", " ") for s in symptom_keys)
    texts = {
        "en": (
            f"You reported **{sym_names}**, which is too general for a specific diagnosis. "
            f"Fever alone can indicate Flu, Dengue, Malaria, COVID-19, or a common viral infection. "
            f"Please share additional symptoms so AURA can narrow the results accurately."
        ),
        "hi": (
            f"आपने **{sym_names}** बताया, जो विशिष्ट निदान के लिए अपर्याप्त है। "
            f"केवल बुखार फ्लू, डेंगू, मलेरिया, COVID-19 या सामान्य वायरल संक्रमण का संकेत हो सकता है। "
            f"सटीक परिणाम के लिए अधिक लक्षण बताएं।"
        ),
        "te": (
            f"మీరు **{sym_names}** చెప్పారు — ఇది ఖచ్చితమైన నిర్ధారణకు సరిపోదు. "
            f"జ్వరం మాత్రమే ఫ్లూ, డెంగ్యూ, మలేరియా, COVID-19 లేదా వైరల్ ఇన్ఫెక్షన్‌కు సూచన. "
            f"మరిన్ని లక్షణాలు చెప్పండి."
        ),
        "or": (
            f"ଆପଣ **{sym_names}** କହିଛନ୍ତି — ଏହା ନିର୍ଦ୍ଦିଷ୍ଟ ରୋଗ ଚିହ୍ନଟ ପାଇଁ ଯଥେଷ୍ଟ ନୁହେଁ | "
            f"କେବଳ ଜ୍ୱର ଫ୍ଲୁ, ଡେଙ୍ଗୁ, ମ୍ୟାଲେରିଆ, COVID-19 କିମ୍ବା ଭୂତାଣୁ ସଂକ୍ରମଣ ହୋଇପାରେ | "
            f"ଅଧିକ ଲକ୍ଷଣ ଜଣାନ୍ତୁ |"
        )
    }
    return texts.get(lang, texts["en"])


def _get_insufficient_advice(lang):
    texts = {
        "en": (
            "1. Log your temperature every 4–6 hours using the Vitals panel.\n"
            "2. Stay hydrated with water, ORS, or coconut water.\n"
            "3. Take paracetamol for fever if needed (avoid aspirin/ibuprofen until dengue is ruled out).\n"
            "4. Tell me about cough, rash, joint pain, chills, or vomiting for a precise match."
        ),
        "hi": (
            "1. वाइटल्स पैनल से हर 4–6 घंटे में तापमान लॉग करें।\n"
            "2. पानी, ORS या नारियल पानी पिएं।\n"
            "3. बुखार के लिए पैरासिटामोल लें (डेंगू исключить होने तक एस्पिरिन/आईबुप्रोफेन न लें)।\n"
            "4. खांसी, चकत्ते, जोड़ों का दर्द, ठंड या उल्टी के बारे में बताएं।"
        ),
        "te": (
            "1. Vitals ప్యానెల్‌లో ప్రతి 4–6 గంటలకు температуру నమోదు చేయండి.\n"
            "2. నీరు, ORS లేదా కొబ్బరి నీరు తాగండి.\n"
            "3. అవసరమైతే పారాసిటమాల్ వాడండి (డెంగ్యూ తొలగించే వరకు ఆస్పిరిన్/ఐబుప్రొఫెన్ వద్దు).\n"
            "4. దగ్గు, దద్దుర్లు, కీళ్ల నొప్పి, చలి లేదా వాంతులు ఉంటే చెప్పండి."
        ),
        "or": (
            "1. Vitals ପ୍ୟାନେଲରେ ପ୍ରତି ୪-୬ ଘଣ୍ଟା ଜ୍ୱର ଲେଖନ୍ତୁ |\n"
            "2. ପାଣି, ORS କିମ୍ବା ନଡ଼ିଆ ପାଣି ପିଅନ୍ତୁ |\n"
            "3. ପାରାସିଟାମଲ୍ ନିଅନ୍ତୁ (ଡେଙ୍ଗୁ ବାଦ ଦେବା ପର୍ଯ୍ୟନ୍ତ ଆସ୍ପିରିନ୍ ନ ନିଅନ୍ତୁ) |\n"
            "4. କାଶ, ଦାଗ, ଗଣ୍ଠି ଯନ୍ତ୍ରଣା, କମ୍ପନ କିମ୍ବା ବାନ୍ତି ଥିଲେ ଜଣାନ୍ତୁ |"
        )
    }
    return texts.get(lang, texts["en"])


def extract_image_features_from_bytes(image_bytes):
    """Extract color and texture descriptors from image bytes."""
    img = Image.open(io.BytesIO(image_bytes))
    img = img.resize((128, 128))
    
    img_rgb = img.convert("RGB")
    arr_rgb = np.array(img_rgb)
    
    r, g, b = arr_rgb[:,:,0], arr_rgb[:,:,1], arr_rgb[:,:,2]
    features = [
        float(np.mean(r)), float(np.std(r)),
        float(np.mean(g)), float(np.std(g)),
        float(np.mean(b)), float(np.std(b))
    ]
    
    img_hsv = img.convert("HSV")
    arr_hsv = np.array(img_hsv)
    h, s, v = arr_hsv[:,:,0], arr_hsv[:,:,1], arr_hsv[:,:,2]
    features.extend([
        float(np.mean(h)), float(np.std(h)),
        float(np.mean(s)), float(np.std(s)),
        float(np.mean(v)), float(np.std(v))
    ])
    
    gray = np.mean(arr_rgb, axis=2)
    dy, dx = np.gradient(gray)
    grad_mag = np.sqrt(dx**2 + dy**2)
    features.extend([
        float(np.mean(grad_mag)), float(np.std(grad_mag))
    ])
    
    return features, r, g, b, grad_mag


def predict_image(image_bytes, lang="en"):
    """Classify the skin condition image and return translated metrics/descriptions."""
    load_models()
    
    if _image_model is None:
        return {"error": "Image prediction model is not trained/loaded."}
        
    try:
        features, r, g, b, grad_mag = extract_image_features_from_bytes(image_bytes)
        features_arr = np.array(features).reshape(1, -1)
        prediction = _image_model.predict(features_arr)[0]
        probabilities = _image_model.predict_proba(features_arr)[0]
        
        classes = _image_model.classes_
        prob_dict = {classes[i]: float(probabilities[i]) for i in range(len(classes))}
        confidence = prob_dict[prediction]
        
        # Translate skin condition predictions
        translations = {
            "Healthy Skin": {
                "en": "Healthy Skin",
                "hi": "स्वस्थ त्वचा (Healthy Skin)",
                "te": "ఆరోగ్యకరమైన చర్మం (Healthy Skin)",
                "ta": "ஆரோக்கியமான தோல் (Healthy Skin)",
                "bn": "সুস্থ ত্বক (Healthy Skin)",
                "ko": "건강한 피부 (Healthy Skin)",
                "ur": "صحت مند جلد (Healthy Skin)",
                "or": "ସୁସ୍ଥ ଚର୍ମ (Healthy Skin)",
                "ml": "ആരോഗ്യമുള്ള ചർമ്മം (Healthy Skin)"
            },
            "Skin Rash": {
                "en": "Skin Rash",
                "hi": "त्वचा पर चकत्ते (Skin Rash)",
                "te": "చర్మంపై దద్దుర్లు (Skin Rash)",
                "ta": "தோல் தடிப்பு (Skin Rash)",
                "bn": "ত্বকের ফুসকুড়ি (Skin Rash)",
                "ko": "피부 발진 (Skin Rash)",
                "ur": "سرخ دھبے (Skin Rash)",
                "or": "ଲାଲ ଚର୍ମ (Skin Rash)",
                "ml": "ചർമ്മത്തിലെ തടിപ്പ് (Skin Rash)"
            },
            "Acne": {
                "en": "Acne",
                "hi": "मुँहासे (Acne)",
                "te": "మొటిమలు (Acne)",
                "ta": "முகப்பரு (Acne)",
                "bn": "ব্রণ (Acne)",
                "ko": "여드름 (Acne)",
                "ur": "دانیں (Acne)",
                "or": "ବ୍ରଣ (Acne)",
                "ml": "முகക്കുരു (Acne)"
            },
            "Eczema": {
                "en": "Eczema",
                "hi": "एक्जिमा (Eczema)",
                "te": "ఎగ్జిమా (Eczema)",
                "ta": "எக்ஸிமா (Eczema)",
                "bn": "একজিমা (Eczema)",
                "ko": "습진 (Eczema)",
                "ur": "ایگزیما (Eczema)",
                "or": "ଏକଜିମା (Eczema)",
                "ml": "കരപ്പൻ (Eczema)"
            }
        }
        
        info = IMAGE_INFO.get(prediction, {
            "description": "Unknown skin condition.",
            "advice": "Please consult a dermatologist.",
            "color_features": "N/A"
        })
        
        # Translate description and advice
        translated_desc = info["description"]
        translated_advice = info["advice"]
        
        # Simple translation replacements for skin conditions advice
        if lang == "hi":
            descs = {
                "Healthy Skin": "त्वचा का रंग समान, चिकनी बनावट, कोई सूजन या दाने नहीं है।",
                "Skin Rash": "जलन और लाल चकत्ते दिखे हैं। यह संपर्क जिल्द की सूजन या गर्मी के कारण हो सकता है।",
                "Acne": "त्वचा पर मुँहासे या फुंसियों के गुच्छे दिखे हैं, जो छिद्र बंद होने या बैक्टीरिया के कारण हो सकते हैं।",
                "Eczema": "सूखी, पपड़ीदार त्वचा और गंभीर खुजली के पैच दिखे हैं, जो एक्जिमा का संकेत हो सकते हैं।"
            }
            advices = {
                "Healthy Skin": "नियमित स्किनकेयर जारी रखें, सनस्क्रीन लगाएं और पानी भरपूर पीएं।",
                "Skin Rash": "प्रभावित क्षेत्र को ठंडा और साफ रखें। खुजली शांत करने के लिए कैलामाइन लोशन लगाएं।",
                "Acne": "चेहरे को दिन में दो बार धोएं। दानों को न फोड़ें। सैलिसिलिक एसिड वाले फेसवॉश का उपयोग करें।",
                "Eczema": "त्वचा को दिन में दो बार खुशबू रहित मॉइस्चराइज़र से नम रखें। गर्म पानी से स्नान न करें।"
            }
            translated_desc = descs.get(prediction, translated_desc)
            translated_advice = advices.get(prediction, translated_advice)
        elif lang == "te":
            descs = {
                "Healthy Skin": "చర్మం సమానమైన రంగులో, నునుపుగా ఉండి ఎలాంటి దద్దుర్లు లేకుండా ఉంది.",
                "Skin Rash": "చర్మంపై ఎర్రటి పొక్కులు మరియు దద్దుర్లు కనిపించాయి.",
                "Acne": "చర్మ రంధ్రాలు మూసుకుపోవడం లేదా బ్యాక్టీరియా వల్ల మొటిమల గుంపులు వచ్చాయి.",
                "Eczema": "పొడిబారిన మరియు పొట్టు తేలిన చర్మం కనిపించింది, ఇది ఎగ్జిమా కావచ్చు."
            }
            advices = {
                "Healthy Skin": "సాధారణ చర్మ రక్షణ పద్ధతులు పాటించండి, సన్‌స్క్రీన్ వాడండి.",
                "Skin Rash": "భాగాన్ని చల్లగా మరియు శుభ్రంగా ఉంచండి. గిల్లకండి. క్యాలమైన్ లోషన్ రాయండి.",
                "Acne": "రోజుకు రెండుసార్లు మొఖం కడుక్కోండి. మొటిమలను గిల్లకండి.",
                "Eczema": "వాసన లేని మాయిశ్చరైజర్లు రాస్తూ చర్మాన్ని తడిగా ఉంచుకోండి."
            }
            translated_desc = descs.get(prediction, translated_desc)
            translated_advice = advices.get(prediction, translated_advice)
        
        # Make translated probabilities keys
        translated_probs = {}
        for k, v in prob_dict.items():
            name = translations.get(k, {}).get(lang, k)
            translated_probs[name] = v
            
        metrics = {
            "mean_redness": float(np.mean(r)),
            "mean_greenness": float(np.mean(g)),
            "mean_blueness": float(np.mean(b)),
            "texture_roughness": float(np.mean(grad_mag)),
            "red_green_ratio": float(np.mean(r) / (np.mean(g) + 1e-5))
        }
        
        return {
            "prediction": translations.get(prediction, {}).get(lang, prediction),
            "confidence": round(confidence, 4),
            "description": translated_desc,
            "advice": translated_advice,
            "color_features": info["color_features"],
            "probabilities": {k: round(v, 4) for k, v in translated_probs.items()},
            "metrics": {k: round(v, 2) for k, v in metrics.items()}
        }
        
    except Exception as e:
        return {"error": f"Image processing error: {str(e)}"}
