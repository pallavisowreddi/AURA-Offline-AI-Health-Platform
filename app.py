import os
import re
from flask import Flask, request, jsonify, render_template
import model_helper

app = Flask(__name__, 
            static_folder="static", 
            template_folder="templates")

# Ensure models are loaded
print("\n========================================================")
print("  [*] AURA AI - Offline Public Health Platform")
print("  [*] Loading machine learning models, please wait...")
print("========================================================")
model_helper.load_models()
print("  [+] Models loaded successfully!")
print("  [+] Starting local server on http://127.0.0.1:5000\n")

# SIH Hackathon Multilingual default responses & customized rule-based NLP database
SYSTEM_RESPONSES = {
    "en": {
        "greeting": "Hello! I am Aura, your local Public Health Assistant. 🏥\\n\\nI work fully offline. You can:\\n1. **Describe your symptoms** (E.g. 'I have high fever and muscle pain').\\n2. **Upload a skin photograph** (like a rash or eczema) for visual diagnostic analysis.\\n3. Ask **general questions** about common diseases or stress/wellness.\\n\\nHow can I help you today?",
        "help": "Here is how you can use me offline:\\n\\n- **Symptom Predictor**: Describe symptoms like fever, joint pain, or diarrhea. I will use a local machine learning classifier to predict the most likely condition.\\n- **Image Analyzer**: Upload a skin photograph. The system extracts color metrics and texture roughness to predict skin conditions.\\n- **Voice Assistance**: Toggle voice output, or click the mic button to speak to me in your language.\\n- **Disease Glossary**: Ask me about common conditions like Malaria, Dengue, or Flu.",
        "fallback": "I hear you! I am analyzing your query. As an offline public health assistant, I focus on general infectious diseases (such as Dengue, Malaria, Cold, Flu, COVID-19) and basic skin conditions. If you are experiencing symptoms, please mention them (e.g. fever, cough, joint pain) so I can run a prediction profile for you!",
        "thanks": "You're very welcome! Stay healthy and take care. Let me know if you have any other questions.",
        "diagnostics_error": "I detected potential references to symptoms but wasn't able to compile a clear diagnosis. Could you describe your symptoms in more detail?"
    },
    "hi": {
        "greeting": "नमस्ते! मैं ऑरा (Aura) हूँ, आपका स्थानीय सार्वजनिक स्वास्थ्य सहायक। 🏥\\n\\nमैं पूरी तरह से ऑफलाइन काम करता हूँ। आप:\\n1. **अपने लक्षणों का वर्णन कर सकते हैं** (जैसे 'मुझे तेज बुखार और बदन दर्द है')।\\n2. **त्वचा की तस्वीर अपलोड कर सकते हैं** (जैसे दाने या एक्जिमा) दृश्य विश्लेषण के लिए।\\n3. आम बीमारियों या तनाव/कल्याण के बारे में **सामान्य प्रश्न** पूछ सकते हैं।\\n\\nआज मैं आपकी क्या सहायता कर सकता हूँ?",
        "help": "आप मेरा ऑफलाइन उपयोग इस प्रकार कर सकते हैं:\\n\\n- **लक्षण भविष्यवक्ता**: बुखार, जोड़ों का दर्द या दस्त जैसे लक्षणों का वर्णन करें। मैं संभावित बीमारी की भविष्यवाणी करूँगा।\\n- **इमेज विश्लेषक**: त्वचा की तस्वीर अपलोड करें। सिस्टम रंग और त्वचा के खुरदरेपन के आधार पर स्थिति बताएगा।\\n- **वॉइस असिस्टेंस**: वॉइस आउटपुट चालू करें, या अपनी भाषा में बात करने के लिए माइक बटन दबाएं।\\n- **बीमारी शब्दावली**: मलेरिया, डेंगू या फ्लू जैसी आम बीमारियों के बारे में पूछें।",
        "fallback": "मैंने आपकी बात सुनी! चूंकि मैं एक ऑफलाइन सार्वजनिक स्वास्थ्य सहायक हूँ, मेरा ध्यान सामान्य संक्रामक रोगों (जैसे डेंगू, मलेरिया, सर्दी, फ्लू, कोविड-19) और बुनियादी त्वचा स्थितियों पर है। यदि आपको कोई शारीरिक लक्षण महसूस हो रहे हैं, तो कृपया उनका उल्लेख करें (जैसे बुखार, खांसी, जोड़ों का दर्द) ताकि मैं भविष्यवाणी कर सकूं!",
        "thanks": "आपका बहुत-बहुत स्वागत है! स्वस्थ रहें और अपना ख्याल रखें। यदि आपका कोई और प्रश्न हो तो अवश्य बताएं।",
        "diagnostics_error": "मैंने आपके लक्षणों को पहचाना लेकिन स्पष्ट बीमारी का पता नहीं लगा सका। कृपया अपने लक्षणों का अधिक विस्तार से वर्णन करें।"
    },
    "te": {
        "greeting": "నమస్తే! నేను ఆరా (Aura), మీ స్థానిక ప్రజా ఆరోగ్య సహాయకుడిని. 🏥\\n\\nనేను ఇంటర్నెట్ లేకుండా పూర్తిగా ఆఫ్-లైన్ లో పని చేస్తాను. మీరు:\\n1. **మీ లక్షణాలను చెప్పవచ్చు** (ఉదా. 'నాకు తీవ్రమైన జ్వరం మరియు ఒళ్ళు నొప్పులు ఉన్నాయి').\\n2. **చర్మం ఫోటోను అప్-లోడ్ చేయవచ్చు** (దద్దుర్లు లేదా ఎగ్జిమా వంటివి) విశ్లేషణ కోసం.\\n3. సాధారణ వ్యాధులు లేదా ఒత్తిడి/ఆరోగ్యం గురించి **ప్రశ్నలు అడగవచ్చు**.\\n\\nఈ రోజు నేను మీకు ఏ విధంగా సహాయం చేయగలను?",
        "help": "మీరు నన్ను ఆఫ్-లైన్ లో ఈ క్రింది విధంగా ఉపయోగించవచ్చు:\\n\\n- **లక్షణాల విశ్లేషణ**: జ్వరం, కీళ్ల నొప్పులు లేదా విరేచనాలు వంటి లక్షణాలను వివరించండి. అత్యంత సంభావ్య వ్యాధిని నేను అంచనా వేస్తాను.\\n- **ఇమేజ్ అనలైజర్**: చర్మం ఫోటోను అప్-లోడ్ చేయండి. రంగు మరియు చర్మం యొక్క గరుకుదనం ఆధారంగా విశ్లేషణ జరుగుతుంది.\\n- **వాయిస్ అసిస్టెన్స్**: వాయిస్ ఆన్ చేయండి, లేదా మీ భాషలో మాట్లాడటానికి మైక్ బటన్ నొక్కండి.\\n- **వ్యాధుల సమాచారం**: మలేరియా, డెంగ్యూ లేదా ఫ్లూ వంటి వ్యాధుల గురించి అడగండి.",
        "fallback": "నేను వింటున్నాను! ఒకవేళ మీరు అస్వస్థతగా ఉంటే, మీ లక్షణాలను (జ్వరం, దగ్గు లేదా దురద వంటివి) నాకు తెలపండి. నేను డెంగ్యూ, మలేరియా, జలుబు, ఫ్లూ, కోవిడ్ వంటి సాధారణ జ్వరాలు మరియు చర్మ వ్యాధులను విశ్లేషించగలను.",
        "thanks": "మీకు చాలాధన్యవాదాలు! ఆరోగ్యంగా ఉండండి మరియు జాగ్రత్త వహించండి. మీకు మరిన్ని ప్రశ్నలు ఉంటే నన్ను అడగవచ్చు.",
        "diagnostics_error": "నేను కొన్ని లక్షణాలను గుర్తించాను కానీ ఖచ్చితమైన వ్యాధిని అంచనా వేయలేకపోయాను. దయచేసి మీ లక్షణాలను మరింత వివరంగా చెప్పండి."
    }
}

# Rule-based query mappings for specific keyword intents
INTENT_ANSWERS = {
    "prevention": {
        "en": "### 🛡️ Disease Prevention Guidelines\nTo protect yourself and your family from common infectious diseases, follow these key steps:\n- **Mosquito-Borne (Dengue, Malaria)**: Clear stagnant water, wear long clothing, and use insect repellents or mosquito nets.\n- **Respiratory (Flu, Cold, COVID-19)**: Wash hands with soap for 20 seconds, wear masks in crowds, and maintain respiratory hygiene (cough into elbows).\n- **Water-Borne (Gastroenteritis)**: Drink boiled or filtered water, wash vegetables thoroughly, and avoid open street foods.",
        "hi": "### 🛡️ बीमारी से बचाव के नियम\nअपने और अपने परिवार को संक्रामक बीमारियों से बचाने के लिए इन मुख्य नियमों का पालन करें:\n- **मच्छर जनित रोग (डेंगू, मलेरिया)**: रुके हुए पानी को साफ करें, पूरी आस्तीन के कपड़े पहनें और मच्छरदानी या रिपेलेंट का उपयोग करें।\n- **श्वसन रोग (फ्लू, सर्दी, कोविड-19)**: हाथों को नियमित साबुन से धोएं, भीड़ में मास्क पहनें और खांसते समय मुंह ढकें।\n- **जल जनित रोग (गैस्ट्रोएंटेराइटिस)**: उबला या छना हुआ पानी पिएं, सब्जियों को अच्छे से धोएं और खुले खाद्य पदार्थों से बचें।",
        "te": "### 🛡️ వ్యాధి నివారణ మార్గదర్శకాలు\nసాధారణ అంటువ్యాధుల నుండి మిమ్మల్ని మరియు మీ కుటుంబాన్ని రక్షించుకోవడానికి ఈ క్రింది నియమాలు పాటించండి:\n- **దోమల ద్వారా వ్యాపించేవి (డెంగ్యూ, మలేరియా)**: నిల్వ ఉన్న నీటిని తొలగించండి, కాళ్లు చేతులు కప్పి ఉంచే బట్టలు వేసుకోండి మరియు దోమతెరలు వాడండి.\n- **శ్వాసకోశ వ్యాధులు (ఫ్లూ, జలుబు, కోవిడ్-19)**: చేతులను క్రమం తప్పకుండా సబ్బుతో కడుక్కోండి, మాస్కులు ధరించండి.\n- **కలుషిత నీరు/ఆహార వ్యాధులు**: కాచి చల్లార్చిన నీటిని మాత్రమే తాగండి, వీధి ఆహారాలకు దూరంగా ఉండండి."
    },
    "diet": {
        "en": "### 🍎 Recommended Diet and Nutrition\nWhen recovering from infectious illnesses, focus on energy, hydration, and immunity:\n- **Hydration**: Drink coconut water, ORS (Oral Rehydration Salts), herbal tea, and plain water to replenish lost fluids.\n- **Digestible Food**: Consume light, soft meals such as rice gruel (khichdi), bananas, boiled vegetables, and plain toast.\n- **Immunity Boosters**: Eat foods rich in Vitamin C (citrus fruits like oranges, lemons) and proteins (lentils, paneer) to speed recovery.",
        "hi": "### 🍎 अनुशंसित आहार और पोषण\nबीमारी से उबरने के दौरान ऊर्जा, हाइड्रेशन और इम्युनिटी पर ध्यान दें:\n- **हाइड्रेशन**: पानी की कमी दूर करने के लिए नारियल पानी, ओआरएस (ORS), हर्बल चाय और साफ पानी पिएं।\n- **सुपाच्य भोजन**: हल्का और नरम भोजन लें जैसे खिचड़ी, दलिया, केला, उबली सब्जियां और टोस्ट।\n- **रोग प्रतिरोधक क्षमता**: रिकवरी तेज करने के लिए विटामिन सी युक्त खाद्य पदार्थ (संतरा, नींबू) और प्रोटीन (दालें, पनीर) खाएं।",
        "te": "### 🍎 అనారోగ్య సమయాల్లో తీసుకోవలసిన ఆహారం\nఅంటువ్యాధుల నుండి త్వరగా కోలుకోవడానికి ఈ ఆహార నియమాలు పాటించండి:\n- **ద్రవ పదార్థాలు**: డీహైడ్రేషన్ బారిన పడకుండా ఉండటానికి ఓఆర్ఎస్ (ORS), కొబ్బరి నీరు, గోరువెచ్చని నీరు తాగండి.\n- **తేలికపాటి ఆహారం**: గంజి, కిచిడీ, అరటిపండు, ఉడికించిన కూరగాయలు తీసుకోండి.\n- **రోగనిరోధక శక్తి పెంచేవి**: విसर्जन రసం, నారింజ, నిమ్మకాయ మరియు పప్పుధాన్యాలు తీసుకోండి."
    },
    "pain": {
        "en": "### 🤕 Muscle, Leg, or Joint Pain Management\nBody aches and joint pains are common responses to physical fatigue or viral infections like Dengue or Flu:\n- **Rest**: Avoid any strenuous physical activity and allow muscles to recover.\n- **Hydration**: Drink water regularly; dehydration causes muscles to cramp.\n- **Heat/Cold Compression**: Apply a warm compress or ice pack to the affected joints to soothe soreness.\n- **Warning**: Do not take pain killers like Ibuprofen or Aspirin if Dengue is suspected, as they can cause severe bleeding. Stick to Paracetamol under doctor advice.",
        "hi": "### 🤕 मांसपेशियों, पैरों या जोड़ों के दर्द का प्रबंधन\nशारीरिक थकान या डेंगू, फ्लू जैसे वायरल संक्रमणों के कारण बदन और जोड़ों में तेज दर्द होना आम है:\n- **विश्राम**: शारीरिक परिश्रम से पूरी तरह बचें और शरीर को आराम दें।\n- **हाइड्रेशन**: नियमित रूप से पानी पिएं; पानी की कमी से मांसपेशियों में ऐंठन होती है।\n- **सिकाई**: प्रभावित जोड़ों पर गर्म सिकाई या बर्फ की थैली का उपयोग करें।\n- **सावधानी**: डेंगू की शंका होने पर आईबुप्रोफेन या एस्पिरिन जैसी दर्द निवारक दवाएं न लें, क्योंकि इनसे ब्लीडिंग का खतरा रहता है। डॉक्टर की सलाह पर केवल पैरासिटामोल लें।",
        "te": "### 🤕 కండరాలు, కాళ్లు లేదా కీళ్ల నొప్పుల నివారణ\nతీవ్ర అలసట లేదా డెంగ్యూ, ఫ్లూ వంటి వైరల్ ఇన్ఫెక్షన్ల వల్ల ఒళ్ళు నొప్పులు మరియు కీళ్ల నొప్పులు రావడం సహజం:\n- **విశ్రాంతి**: శారీరక శ్రమను పూర్తిగా తగ్గించి విశ్రాంతి తీసుకోండి.\n- **ద్రవాలు**: డీహైడ్రేషన్ వల్ల కండరాల లాగడం జరుగుతుంది కాబట్టి ఎక్కువ నీరు తాగండి.\n- **వేడి కాపడం**: నొప్పి ఉన్న భాగంలో వేడి కాపడం పెట్టడం ద్వారా ఉపశమనం పొందవచ్చు.\n- **హెచ్చరిక**: డెంగ్యూ లక్షణాలు ఉంటే ఐబుప్రొఫెన్, ఆస్పిరిన్ వంటి నొప్పుల మందులు వాడకండి. ఇవి రక్తస్రావానికి దారితీస్తాయి. కేవలం పారాసిటమాల్ మాత్రమే వాడండి."
    },
    "hospital": {
        "en": "### 🏥 Finding Healthcare Facilities & Clinics\nIf you need clinical attention, please check the local locator map:\n1. Click the **'Nearby Clinics Map'** tab on the left dashboard to view simulated healthcare centers near you.\n2. **Emergency**: If you display warning signs (SpO2 below 94%, high fever for >3 days, or bleeding), click the **SOS Emergency Alert** button immediately.\n3. **Community Clinics**: Local community clinics can run blood diagnostic smear tests for Malaria and Dengue.",
        "hi": "### 🏥 स्वास्थ्य सुविधाएं और क्लीनिक खोजना\nयदि आपको चिकित्सकीय देखभाल की आवश्यकता है, तो इन चरणों का पालन करें:\n1. अपने पास के क्लीनिक देखने के लिए बाएं डैशबोर्ड पर **'Nearby Clinics Map'** टैब पर क्लिक करें।\n2. **आपातकाल**: यदि गंभीर लक्षण (जैसे ऑक्सीजन 94% से कम होना, 3 दिन से तेज बुखार, या मसूड़ों से खून आना) दिखें, तो तुरंत **SOS Emergency Alert** बटन दबाएं।\n3. **रक्त जांच**: स्थानीय स्वास्थ्य केंद्रों पर जाकर मलेरिया और डेंगू के लिए ब्लड टेस्ट करवाएं।",
        "te": "### 🏥 వైద్య సహాయం మరియు క్లినిక్‌ల వివరాలు\nమీకు వైద్య సలహా అవసరమైతే ఈ క్రింది విధంగా చేయండి:\n1. మీ సమీపంలోని వైద్య కేంద్రాల సమాచారం కొరకు ఎడమ వైపు ప్యానల్ లో ఉన్న **'Nearby Clinics Map'** క్లిక్ చేయండి.\n2. **అत्यవసర పరిస్థితి**: ఆక్సిజన్ స్థాయి 94% కన్నా తగ్గినా లేదా తీవ్ర జ్వరం ఉన్నా వెంటనే **SOS Emergency Alert** బటన్ ప్రెస్ చేయండి.\n3. **రక్త పరీక్ష**: మలేరియా లేదా డెంగ్యూ అనుమానం ఉంటే వెంటనే రక్త పరీక్ష చేయించుకోండి."
    },
    "wellness": {
        "en": "### 🧠 Stress Management & Mental Wellness\nExperiencing stress or anxiety is a very common response to sickness, pressure, or physical fatigue. Here are structured wellness guidelines:\n- **Deep Breathing (4-7-8 Technique)**: Inhale for 4 seconds, hold your breath for 7 seconds, and exhale slowly for 8 seconds. Repeat 4 times to calm your nervous system.\n- **Physical Movement**: Take light walks, do gentle stretching, or practice yoga. Physical activity releases endorphins which reduce stress.\n- **Rest and Sleep**: Ensure 7-8 hours of sound sleep. Disconnect from digital screens at least 30 minutes before bedtime.\n- **Talk to Someone**: Sharing how you feel with a trusted friend, family member, or healthcare professional can significantly relieve mental tension.",
        "hi": "### 🧠 मानसिक तनाव और कल्याण प्रबंधन\nबीमारी, दबाव या शारीरिक थकान के कारण तनाव या चिंता महसूस होना बहुत आम है। राहत के लिए निम्नलिखित नियमों का पालन करें:\n- **गहरी सांस लें (4-7-8 तकनीक)**: 4 सेकंड के लिए सांस लें, 7 सेकंड के लिए सांस रोकें, और 8 सेकंड तक धीरे-धीरे बाहर छोड़ें। यह तंत्रिका तंत्र को शांत करता है।\n- **शारीरिक गतिविधि**: हल्की सैर करें या योग करें। शारीरिक गतिविधि से एंडोर्फिन निकलता है जो तनाव कम करता है।\n- **पर्याप्त आराम**: रोजाना 7-8 घंटे की गहरी नींद लें। सोने से 30 मिनट पहले मोबाइल/टीवी स्क्रीन बंद कर दें।\n- **बातचीत करें**: अपने दोस्तों, परिवार या किसी विशेषज्ञ से अपनी चिंताओं को साझा करने से मन का बोझ बहुत कम हो जाता है।",
        "te": "### 🧠 ఒత్తిడి నివారణ & మానసిక ఆరోగ్యం\nఅనారోగ్యం, ఒత్తిడి లేదా అలసట వల్ల ఆందోళన చెందడం సహజం. దీని నివారణకు ఈ చిట్కాలు పాటించండి:\n- **శ్వాస వ్యాయామం (4-7-8 పద్ధతి)**: 4 సెకన్లు శ్వాస తీసుకోండి, 7 సెకన్లు శ్వాసను ఆపి ఉంచండి, 8 సెకన్ల పాటు నెమ్మదిగా వదలండి. ఇది మనస్సుకు ప్రశాంతతను ఇస్తుంది.\n- **శారీరక శ్రమ**: రోజువారీ వ్యాయామం లేదా యోగా చేయండి. శారీరక శ్రమ వల్ల హ్యాపీ హార్మోన్లు విడుదలవుతాయి.\n- **సరైన నిద్ర**: రోజుకు కనీసం 7-8 గంటలు నిద్రపోండి. నిద్రపోయే ముందు మొబైల్ ఫోన్లు వాడకండి.\n- **భావాలను పంచుకోండి**: మీ మనసులోని మాటలను కుటుంబ సభ్యులతో లేదా స్నేహితులతో పంచుకోవడం వల్ల ఒత్తిడి తగ్గుతుంది."
    }
}

DISEASE_ALIASES = {
    "Diabetes": ["diabetes", "sugar", "मधुमेह", "డయాబెటిస్", "షుగర్"],
    "Hypertension": ["hypertension", "high bp", "blood pressure", "bp", "उच्च रक्तचाप", "రక్తపోటు", "బీపీ"],
    "Asthma": ["asthma", "bronchial asthma", "wheezing", "दमा", "అస్తమా", "ఉబ్బసం"],
    "Arthritis": ["arthritis", "joint inflammation", "गठिया", "కీళ్లవాతం", "ఆర్థరైటిస్"],
    "Cancer (Early Warning)": ["cancer", "tumor", "malignancy", "कैंसर", "క్యాన్సర్"],
    "Obesity": ["obesity", "overweight", "excess fat", "मोटापा", "స్థూలకాయం", "ఊబకాయం"],
    "Dengue Fever": ["dengue", "dengue fever", "डेंगू", "డెంగ్యూ"],
    "Malaria": ["malaria", "मलेरिया", "మలేరియా"],
    "Typhoid Fever": ["typhoid", "enteric fever", "टाइफाइड", "టైఫాయిడ్"],
    "Tuberculosis": ["tuberculosis", "tb", "टीबी", "तपेदिक", "క్షయ", "టిబి"],
    "Pneumonia": ["pneumonia", "निमोनिया", "న్యుమోనియా"],
    "COVID-19": ["covid", "covid-19", "coronavirus", "कोविड", "కోవిడ్"],
    "Influenza": ["influenza", "flu", "फ्लू", "ఫ్లూ"],
    "Common Cold": ["common cold", "cold", "जुकाम", "सर्दी", "జలుబు"],
    "Chickenpox": ["chickenpox", "varicella", "चेचक", "छोटी माता", "ఆటలమ్మ", "మశూచి"],
    "Gastroenteritis": ["gastroenteritis", "stomach flu", "food poison", "पेट संक्रमण"],
    "Cholera": ["cholera", "हैजा", "కలరా"],
    "Hepatitis": ["hepatitis", "hep", "हेपेटाइटिस", "హెపటైటిస్"],
    "Jaundice": ["jaundice", "पीलिया", "కామెర్లు"],
    "Coronary Artery Disease": ["coronary", "heart attack", "heart disease", "angina", "हार्ट अटैक", "हृदय रोग", "గుండెపోటు", "గుండె జబ్బు"],
    "Stroke (TIA Warning)": ["stroke", "paralysis", "tia", "स्ट्रोक", "लकवा", "పక్షవాతం"],
    "Chronic Kidney Disease": ["kidney disease", "renal", "ckd", "kidney failure", "गुर्दे की बीमारी", "కిడ్నీ వ్యాధి"],
    "Anemia": ["anemia", "anaemia", "low hemoglobin", "खून की कमी", "రక్తహీనత"],
    "Hypothyroidism": ["hypothyroidism", "thyroid", "थायराइड", "థైరాయిడ్"],
    "Hyperthyroidism": ["hyperthyroidism", "overactive thyroid"],
    "Migraine": ["migraine", "माइग्रेन", "आधासीसी", "పార్శ్వపు తలనొప్పి"],
    "GERD (Acid Reflux)": ["gerd", "acid reflux", "heartburn", "acidity", "एसिडिटी", "గ్యాస్ట్రిక్", "ఎసిడిటీ"],
    "Peptic Ulcer": ["peptic ulcer", "stomach ulcer", "gastric ulcer", "पेट का अल्सर", "కడుపులో పుండు"],
    "Urinary Tract Infection": ["urinary tract infection", "uti", "urine infection", "यूटीआई", "మూత్ర ఇన్ఫెక్షన్"],
    "Allergic Rhinitis": ["allergic rhinitis", "hay fever", "rhinitis", "एलर्जी"],
    "Food Allergy": ["food allergy", "खाद्य एलर्जी", "ఆహార అలర్జీ"],
    "Eczema": ["eczema", "atopic dermatitis", "एक्जिमा", "ఎగ్జిమా"],
    "Psoriasis": ["psoriasis", "सोरायसिस", "సోరియాసిస్"],
    "Acne Vulgaris": ["acne", "pimples", "मुंहासे", "మొటిమలు"]
}

@app.route("/")
def index():
    """Render the main single-page application dashboard."""
    return render_template("index.html")


@app.route("/login")
def login_page():
    """Render the standalone patient and clinician sign-in portal."""
    return render_template("login.html")


@app.route("/signup")
def signup_page():
    """Render the standalone patient health card registration portal."""
    return render_template("signup.html")


@app.route("/api/predict/symptoms", methods=["POST"])
def predict_symptoms():
    """Predict disease based on an explicit array of symptoms and chosen language."""
    data = request.get_json() or {}
    symptoms = data.get("symptoms", [])
    lang = data.get("lang", "en")
    
    if not isinstance(symptoms, list):
        return jsonify({"error": "Symptoms must be a list of strings."}), 400
        
    result = model_helper.predict_disease(symptoms, lang)
    return jsonify(result)


@app.route("/api/predict/image", methods=["POST"])
def predict_image():
    """Analyze skin condition from an uploaded image file."""
    if "image" not in request.files:
        return jsonify({"error": "No image file provided."}), 400
        
    file = request.files["image"]
    lang = request.form.get("lang", "en")
    
    if file.filename == "":
        return jsonify({"error": "No selected file."}), 400
        
    try:
        image_bytes = file.read()
        result = model_helper.predict_image(image_bytes, lang)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Multilingual chat route.
    Parses symptoms, runs predictions, or handles general disease information.
    """
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    lang = data.get("lang", "en")
    
    responses = SYSTEM_RESPONSES.get(lang, SYSTEM_RESPONSES["en"])
    
    if not message:
        return jsonify({"response": "..."})
    
    message_lower = message.lower()
    
    response_data = {
        "detected_symptoms": [],
        "disease_prediction": None,
        "response": ""
    }

    # Step 0: Greeting / thanks / help — respond before symptom parsing
    greeting_words = ["hello", "hi", "hey", "namaste", "namaskar", "good morning", "good evening",
                      "नमस्ते", "नमस्कार", "హలో", "నమస్తే", "ନମସ୍କାର"]
    thanks_words = ["thank", "thanks", "धन्यवाद", "ధన్యవాద", "ଧନ୍ୟବାଦ"]
    help_words = ["help", "how to use", "guide", "मदद", "सहायता", "సహాయం", "ସାହାଯ୍ୟ"]

    if any(w in message_lower for w in greeting_words) and len(message.split()) <= 4:
        response_data["response"] = responses["greeting"].replace("\\n", "\n")
        return jsonify(response_data)
    if any(w in message_lower for w in thanks_words):
        response_data["response"] = responses["thanks"].replace("\\n", "\n")
        return jsonify(response_data)
    if any(w in message_lower for w in help_words):
        response_data["response"] = responses["help"].replace("\\n", "\n")
        return jsonify(response_data)
        
    # Step 1: Check for symptoms in user's query text using language matching
    detected_symptoms = model_helper.extract_symptoms_from_text(message, lang)
    response_data["detected_symptoms"] = detected_symptoms
    
    # Step 2: If symptoms are detected, perform predictive analytics
    if detected_symptoms:
        prediction = model_helper.predict_disease(detected_symptoms, lang)
        response_data["disease_prediction"] = prediction
        
        # Translate symptom display list
        translated_syms = []
        for s in detected_symptoms:
            # simple lookup translations for display
            vocab_terms = model_helper.SYMPTOM_VOCAB.get(lang, {}).get(s, [s])
            translated_syms.append(vocab_terms[0].title())
            
        symptoms_str = ", ".join(translated_syms)
        
        if prediction["prediction"] == "No Symptoms Detected":
            response_data["response"] = responses["diagnostics_error"]
        else:
            urgency = prediction["urgency"]
            urgency_icon = "⚠️" if urgency in ["High", "Critical"] else "ℹ️"
            mode = prediction.get("prediction_mode", "confirmed")
            mode_labels = {
                "confirmed": {"en": "Confirmed Assessment", "hi": "पुष्ट निदान", "te": "నిర్ధారిత అంచనా", "or": "ନିଶ୍ଚିତ ମୂଲ୍ୟାଙ୍କନ"},
                "differential": {"en": "Differential Diagnosis (Preliminary)", "hi": "प्रारंभिक विभेदक निदान", "te": "ప్రాథమిక వ్యత్యాస నిర్ధారణ", "or": "ପ୍ରାଥମିକ ବିଭେଦନ"},
                "insufficient": {"en": "Preliminary Screening (More Info Needed)", "hi": "प्रारंभिक जांच (अधिक जानकारी चाहिए)", "te": "ప్రాథమిక పరీక్ష (మరింత సమాచారం)", "or": "ପ୍ରାଥମିକ ଯାଞ୍ଚ (ଅଧିକ ସୂଚନା)"}
            }
            mode_label = mode_labels.get(mode, mode_labels["confirmed"]).get(lang, mode_labels.get(mode, mode_labels["confirmed"])["en"])

            # Build follow-up questions block
            follow_ups = prediction.get("follow_up_questions", [])
            follow_up_block = ""
            if follow_ups and mode in ("insufficient", "differential"):
                q_header = {"en": "To improve accuracy, please also tell me:", "hi": "सटीकता बढ़ाने के लिए बताएं:",
                            "te": "ఖచ్చితత్వం కోసం ఇవి కూడా చెప్పండి:", "or": "ସଠିକତା ପାଇଁ ଏହା ମଧ୍ୟ ଜଣାନ୍ତୁ:"}
                follow_up_block = f"\n\n**{q_header.get(lang, q_header['en'])}**\n"
                for i, q in enumerate(follow_ups, 1):
                    follow_up_block += f"{i}. {q}\n"

            # Red flags block
            red_flags = prediction.get("red_flags", [])
            red_flag_block = ""
            if red_flags:
                red_flag_block = "\n\n**🚨 Urgent Warning Signs Detected:**\n"
                for flag in red_flags:
                    red_flag_block += f"- {flag}\n"

            care_guidance = prediction.get("care_guidance", "")

            # Format custom detailed output
            if lang == "hi":
                response_text = (
                    f"### 🩺 {mode_label}\n\n"
                    f"आपके बताए लक्षणों (**{symptoms_str}**) के आधार पर, AURA का हाइब्रिड निदान इंजन "
                    f"**{prediction['prediction']}** की ओर इशारा करता है "
                    f"(आत्मविश्वास: **{prediction['confidence']:.1%}**).\n\n"
                    f"**विवरण:** {prediction['description']}\n\n"
                    f"{urgency_icon} **तात्कालिकता:** {prediction['urgency']}\n\n"
                    f"**देखभाल सलाह:**\n{prediction['advice']}\n\n"
                    f"{care_guidance}"
                    f"{red_flag_block}{follow_up_block}\n"
                    f"--- \n"
                    f"*यह एक ऑफलाइन शैक्षणिक उपकरण है। गंभीर लक्षणों पर डॉक्टर से संपर्क करें।*"
                )
            elif lang == "te":
                response_text = (
                    f"### 🩺 {mode_label}\n\n"
                    f"మీరు తెలిపిన (**{symptoms_str}**) లక్షణాల ఆధారంగా, AURA హైబ్రిడ్ మోడల్ "
                    f"**{prediction['prediction']}** ఉండవచ్చని అంచనా వేస్తోంది "
                    f"(ఖచ్చితత్వం: **{prediction['confidence']:.1%}**).\n\n"
                    f"**వివరణ:** {prediction['description']}\n\n"
                    f"{urgency_icon} **అవసర స్థాయి:** {prediction['urgency']}\n\n"
                    f"**సంరక్షణ సలహా:**\n{prediction['advice']}\n\n"
                    f"{care_guidance}"
                    f"{red_flag_block}{follow_up_block}\n"
                    f"--- \n"
                    f"*ఇది అవగాహన కోసం ఆఫ్-లైన్ AI సాధనం. తీవ్ర అనారోగ్య సమయాలలో వైద్యుడిని సంప్రదించండి.*"
                )
            elif lang == "or":
                response_text = (
                    f"### 🩺 {mode_label}\n\n"
                    f"ଆପଣଙ୍କ ଲକ୍ଷଣ (**{symptoms_str}**) ଆଧାରରେ, AURA ହାଇବ୍ରିଡ୍ ମୋଡେଲ୍ "
                    f"**{prediction['prediction']}** ସମ୍ଭାବନା ଦର୍ଶାଉଛି "
                    f"(ବିଶ୍ୱାସ: **{prediction['confidence']:.1%}**).\n\n"
                    f"**ବିବରଣ:** {prediction['description']}\n\n"
                    f"{urgency_icon} **ଜରୁରୀତା:** {prediction['urgency']}\n\n"
                    f"**ସତର୍କତା:**\n{prediction['advice']}\n\n"
                    f"{care_guidance}"
                    f"{red_flag_block}{follow_up_block}\n"
                    f"--- \n"
                    f"*ଏହା ଶିକ୍ଷାମୂଳକ ଯଞ୍ତ୍ର | ଗମ୍ଭୀର ଲକ୍ଷଣରେ ଡାକ୍ତରଙ୍କୁ ଦେଖାନ୍ତୁ |*"
                )
            else:
                response_text = (
                    f"### 🩺 {mode_label}\n\n"
                    f"Based on your reported symptoms (**{symptoms_str}**), AURA's hybrid clinical engine "
                    f"suggests **{prediction['prediction']}** "
                    f"with **{prediction['confidence']:.1%}** confidence.\n\n"
                    f"**Condition Summary:** {prediction['description']}\n\n"
                    f"{urgency_icon} **Urgency Class:** {prediction['urgency']}\n\n"
                    f"**Care and Advice:**\n{prediction['advice']}\n\n"
                    f"{care_guidance}"
                    f"{red_flag_block}{follow_up_block}\n"
                    f"--- \n"
                    f"*Notice: Offline educational screening tool. Seek professional care if seriously ill.*"
                )
            response_data["response"] = response_text
            return jsonify(response_data)
            
    # Step 3: Handle direct disease inquiries (comprehensive 34-disease medical glossary)
    matched_disease = None
    for disease_name, aliases in DISEASE_ALIASES.items():
        if any(re.search(r'\b' + re.escape(alias) + r'\b', message_lower) or alias in message_lower for alias in aliases):
            matched_disease = disease_name
            break
            
    if not matched_disease:
        for disease_name in model_helper.DISEASE_INFO.keys():
            if disease_name.lower() in message_lower:
                matched_disease = disease_name
                break

    if matched_disease:
        info = model_helper.DISEASE_INFO.get(matched_disease, {}).get(lang, model_helper.DISEASE_INFO.get(matched_disease, {}).get("en", {}))
        symptoms_keys = model_helper.disease_symptoms.get(matched_disease, [])
        display_symptom_names = []
        for skey in symptoms_keys:
            vocab_terms = model_helper.SYMPTOM_VOCAB.get(lang, {}).get(skey, [skey])
            display_symptom_names.append(vocab_terms[0].title())
            
        sym_header = {"en": "Key Clinical Symptoms", "hi": "मुख्य लक्षण", "te": "ముఖ్య లక్షణాలు"}
        adv_header = {"en": "Management and Clinical Advice", "hi": "प्रबंधन और चिकित्सकीय सलाह", "te": "నిర్వహణ మరియు వైద్య సలహా"}
        urg_header = {"en": "Urgency Classification", "hi": "तात्कालिकता स्तर", "te": "అవసర స్థాయి"}
        
        response_data["response"] = (
            f"### 🩺 **{info.get('prediction', matched_disease)}**\n\n"
            f"**Overview:** {info.get('description', '')}\n\n"
            f"**{sym_header.get(lang, sym_header['en'])}:** {', '.join(display_symptom_names)}\n\n"
            f"**{adv_header.get(lang, adv_header['en'])}:**\n{info.get('advice', '')}\n\n"
            f"**{urg_header.get(lang, urg_header['en'])}:** {info.get('urgency', 'Medium')}\n\n"
            f"---\n*AURA Offline Health Intelligence System*"
        )
        return jsonify(response_data)
            
    # Step 4: Handle specific rule-based INTENT matching (Diet, Prevention, Muscle Pain, Clinics, Wellness)
    # Prevention check
    if any(k in message_lower for k in ["prevent", "prevention", "protection", "safe", "बचाव", "सुरक्षा", "నివారణ", "రక్షణ"]):
        response_data["response"] = INTENT_ANSWERS["prevention"].get(lang, INTENT_ANSWERS["prevention"]["en"])
        return jsonify(response_data)
        
    # Diet check
    if any(k in message_lower for k in ["diet", "food", "eat", "nutrition", "आहार", "भोजन", "ఆహారం", "కూరగాయలు"]):
        response_data["response"] = INTENT_ANSWERS["diet"].get(lang, INTENT_ANSWERS["diet"]["en"])
        return jsonify(response_data)
        
    # Stress / Wellness check
    if any(k in message_lower for k in ["stress", "anxiety", "depression", "mental", "tension", "worry", "panic", "तनाव", "चिंता", "अवसाद", "ఒత్తిడి", "ఆందోళన", "కంగారు"]):
        response_data["response"] = INTENT_ANSWERS["wellness"].get(lang, INTENT_ANSWERS["wellness"]["en"])
        return jsonify(response_data)
        
    # Muscle or Leg Pain check
    if any(k in message_lower for k in ["leg", "pain", "muscle", "joint", "body ache", "दर्द", "नొప్పి", "కీళ్లు", "ఒళ్ళు నొప్పులు"]):
        response_data["response"] = INTENT_ANSWERS["pain"].get(lang, INTENT_ANSWERS["pain"]["en"])
        return jsonify(response_data)
        
    # Hospital/Clinic locator check
    if any(k in message_lower for k in ["hospital", "clinic", "doctor", "nearby", "map", "अस्पताल", "डॉक्टर", "ఆసుపత్రి", "క్లినిక్"]):
        response_data["response"] = INTENT_ANSWERS["hospital"].get(lang, INTENT_ANSWERS["hospital"]["en"])
        return jsonify(response_data)

    # Step 5: Dynamic context echo fallback (prevents static/generic replies!)
    # Filter message to extract nouns/topics
    filler_words = [
        "have", "with", "from", "please", "help", "what", "where", "about", 
        "this", "that", "some", "more", "less", "much", "very", "feel", "feeling",
        "like", "want", "need", "normal", "matter", "thing", "things", "only", 
        "just", "doing", "does", "done", "make", "made", "good", "well", "find",
        "getting", "gets", "give", "given", "give", "what"
    ]
    words = [w for w in message.split() if len(w) > 3 and w.lower() not in filler_words]
    topic = f"'{words[0]}'" if words else f"'{message}'"
    
    if lang == "hi":
        fallback_text = (
            f"आपने **{topic}** के बारे में पूछा। चूंकि मैं एक ऑफलाइन सार्वजनिक स्वास्थ्य सहायक हूँ, "
            f"मैं केवल सामान्य बीमारियों (डेंगू, मलेरिया, सर्दी, फ्लू, कोविड-19) और बुनियादी त्वचा स्थितियों को ही पहचान सकता हूँ।\n\n"
            f"यदि आप अस्वस्थ महसूस कर रहे हैं, तो कृपया अपने शारीरिक लक्षण बताएं (जैसे बुखार, खांसी, बदन दर्द, दस्त, या त्वचा पर लाल चकत्ते) ताकि मैं नैदानिक विश्लेषण कर सकूं।"
        )
    elif lang == "te":
        fallback_text = (
            f"మీరు **{topic}** గురించి అడిగారు. నేను ఆఫ్-లైన్ పబ్లిక్ హెల్త్ అసిస్టెంట్ కావడంతో, "
            f"నేను కేవలం సాధారణ జ్వరాలు (డెంగ్యూ, మలేరియా, జలుబు, ఫ్లూ, కోవిడ్) మరియు చర్మ వ్యాధులను మాత్రమే విశ్లేషించగలను.\n\n"
            f"దయచేసి మీ శారీరక లక్షణాలను చెప్పండి (ఉదాహరణకు: జ్వరం, దగ్గు, ఒళ్ళు నొప్పులు, వాంతులు, లేదా దద్దుర్లు)."
        )
    else:
        fallback_text = (
            f"You asked about: **{topic}**.\n\n"
            f"As an offline public health assistant, my built-in ML database focuses on general infectious diseases (such as Dengue, Malaria, Cold, Flu, COVID-19) and basic skin conditions.\n\n"
            f"If you are feeling unwell, please describe your physical symptoms (e.g. fever, cough, joint pain, diarrhea, rash) so I can run a prediction profile for you!"
        )
        
    response_data["response"] = fallback_text
    return jsonify(response_data)

if __name__ == "__main__":
    # Ensure templates and static folders exist
    os.makedirs("templates", exist_ok=True)
    os.makedirs("static/css", exist_ok=True)
    os.makedirs("static/js", exist_ok=True)
    
    print("Starting Flask web server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
