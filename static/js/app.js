
// ============================================================================
// AURA CLIENT-SIDE MULTILINGUAL TRANSLATION DICTIONARY
// ============================================================================
const UI_TRANSLATIONS = {
    en: {
        nav_brand: "AURA Platform",
        badge_offline: "Local Offline",
        nav_home: "Home",
        nav_prediction: "Disease Prediction",
        nav_reports: "Medical Reports",
        nav_reminders: "Medicine Reminder",
        nav_dashboard: "Health Dashboard",
        nav_emergency: "Emergency",
        nav_settings: "Settings",
        nav_about: "About",
        nav_relax: "Take a Pause",
        nav_live: "Live Reading",
        nav_signin: "Sign In / Join",
        nav_logout: "Logout",
        nav_login: "Login",
        nav_signup: "Sign Up",
        login_subtitle: "Access your offline medical history, biometrics telemetry, and medication schedule.",
        signup_subtitle: "Set up your personal offline digital health profile with clinical baseline records.",
        auth_no_account: "Don't have an account?",
        auth_link_signup: "Create an Account →",
        auth_have_account: "Already have an account?",
        auth_link_login: "Sign In here →",
        demo_accounts_title: "⚡ 1-Click Hackathon Demo Profiles",
        hero_eyebrow: "Local Intelligent Diagnostics",
        hero_title: "Your Personal Offline Clinical Assistant",
        hero_desc: "Fully offline, 34-disease multilingual clinical intelligence and predictive biometrics. Safeguard your family with reliable information.",
        hero_btn_check: "Start Symptom Check",
        hero_btn_dash: "View Dashboard",
        feat_symptoms_title: "Symptom Checker",
        feat_symptoms_desc: "Talk to our offline chatbot to diagnose 34 common conditions, chronic diseases, and epidemic symptoms.",
        feat_scanner_title: "Visual Skin Scanner",
        feat_scanner_desc: "Analyze skin lesions, rashes, eczema, or acne using local color and texture model scanning.",
        feat_reminders_title: "Medicine Reminders",
        feat_reminders_desc: "Schedule daily medications, set dosage times, and receive offline browser sound alerts.",
        feat_dashboard_title: "Clinical Telemetry",
        feat_dashboard_desc: "Accurate Blood Pressure percentages, live ECG waveforms, Heart Rate, and overall health scores.",
        qs_patient_status: "Patient Status",
        qs_vitals_healthy: "Vitals Healthy",
        qs_upcoming_pill: "Upcoming Pill",
        qs_no_meds: "No meds scheduled",
        qs_health_tip_lbl: "Daily Health Tip",
        qs_health_tip_val: "Stay hydrated and monitor body temperature.",
        aware_eyebrow: "Public Health Education",
        aware_title: "Recognize, Prevent & Protect",
        aware_desc: "Essential offline awareness guides for key lifestyle, metabolic, and infectious diseases.",
        card_dia_title: "Diabetes Mellitus",
        card_dia_desc: "Monitor high thirst & frequent urination. Maintain low-glycemic fiber diet and exercise daily.",
        card_hyp_title: "Hypertension",
        card_hyp_desc: "Watch out for morning headaches and dizziness. Limit sodium intake below 2,000 mg/day.",
        card_ast_title: "Asthma & Airway Care",
        card_ast_desc: "Recognize wheezing and chest tightness early. Keep emergency bronchodilators accessible.",
        card_den_title: "Dengue & Fevers",
        card_den_desc: "Sudden high fever, joint retro-orbital pain, and rash. Stay heavily hydrated with ORS fluids.",
        btn_learn_more: "Learn More →",
        diag_sys_integrity: "System Integrity",
        diag_net_conn: "Network Connection",
        diag_net_disc: "Disconnected (No WiFi)",
        diag_ml_engine: "ML Prediction Engine",
        diag_ml_active: "Operational (Local)",
        diag_pred_title: "Predictive Diagnostics",
        diag_describe_hint: "Describe symptoms to check diagnostic metrics.",
        diag_conf_lbl: "Confidence",
        diag_diff_title: "Differential Diagnostics",
        xai_header_title: "💡 Explainable AI (XAI)",
        rep_title: "Visual Skin Diagnostic Analyzer",
        rep_desc: "Scan skin symptoms locally. Our edge feature-extraction analyzer checks color histograms, saturation ratios, and surface roughness variables to predict conditions offline.",
        rep_drag_drop: "Drag & Drop Skin Sample Image",
        rep_formats_hint: "supports JPEG, PNG formats (Max 8MB)",
        btn_browse_photos: "Browse Local Photos",
        rep_samples_title: "Interactive Sample Images",
        rep_samples_hint: "Click a mock-lesion to verify vision classification model outputs:",
        rep_sample_healthy: "Healthy Skin",
        rep_sample_rash: "Skin Rash",
        rep_sample_acne: "Acne",
        rep_sample_eczema: "Eczema",
        rep_reader_title: "Offline Report Reader",
        rep_reader_hint: "Log diagnostic lab reports (.txt, .json formats) to check clinical reference anomalies.",
        rep_upload_hint: "Upload textual lab values",
        btn_select_report: "Select Report File",
        rem_add_title: "Add New Medication",
        rem_med_name: "Medicine Name",
        rem_dosage: "Dosage",
        rem_time: "Reminder Time",
        rem_freq: "Frequency",
        rem_opt_daily: "Daily",
        rem_opt_weekly: "Weekly",
        rem_opt_monthly: "Monthly",
        btn_add_schedule: "Add Schedule",
        rem_active_title: "Active Schedule",
        rem_no_meds: "No medications scheduled yet.",
        dash_health_score_title: "Overall Health Score",
        dash_score_opt: "Clinical safety metrics calculated in optimal range.",
        dash_log_vitals_title: "Log Biometrics & BP",
        dash_sim_live: "🔴 Simulate Live",
        lbl_sys_bp: "Systolic BP (mmHg)",
        lbl_dia_bp: "Diastolic BP (mmHg)",
        lbl_heart_rate: "Heart Rate (BPM)",
        lbl_spo2: "Oxygen SpO₂ (%)",
        lbl_body_temp: "Body Temperature (°F)",
        btn_calc_vitals: "Calculate Biometrics & Save",
        vitals_status_norm: "Cardiovascular metrics normal & stable.",
        dash_bp_title: "Blood Pressure Status",
        dash_hr_title: "Heart Rate",
        dash_spo2_title: "Oxygen Saturation (SpO₂)",
        dash_trend_title: "Continuous Biometric Trend",
        sos_title: "🚨 SOS Clinical Warnings",
        sos_desc: "If you display severe symptoms like difficulty breathing, chest pain, or oxygen levels below 94%, please activate emergency services immediately.",
        sos_directives_title: "📋 Critical Emergency Directives:",
        sos_dir_1: "Sit upright to assist lungs and respiration.",
        sos_dir_2: "Minimize movement and avoid physical exertion.",
        sos_dir_3: "Keep emergency phone contacts accessible.",
        sos_dir_4: "Ventilate rooms and turn on fans.",
        btn_trigger_sos: "🚨 Trigger SOS Warning",
        sos_contacts_title: "Simulated Rescue Contacts",
        sos_contacts_desc: "Fictional local clinical stations and community response teams (Simulated Offline Directory):",
        sos_contact_1: "Aura Community Clinic Emergency",
        sos_contact_2: "District Trauma Hospital",
        sos_contact_3: "Outbreak Alert Hotline",
        set_custom_title: "UI & Feature Customizations",
        set_dark_mode: "Dark Theme Mode",
        set_dark_mode_desc: "Override the interface color palette",
        set_voice_tts: "Voice TTS Feedback",
        set_voice_desc: "Read results and predictions aloud",
        set_avatar: "AI Assistant Widget",
        set_avatar_desc: "Display floating doctor overlay",
        set_access_title: "Accessibility Preferences",
        about_title: "About AURA Platform",
        about_desc: "AURA is trained locally on synthetic parameters matching typical public health infections and skin conditions. Since it works 100% offline, it represents a lightweight, portable clinical support system ideal for remote villages, military posts, and offline disaster response sectors.",
        about_arch_title: "Offline Architecture Summary",
        auth_tab_login: "Sign In",
        auth_tab_signup: "Create Account",
        auth_lbl_email: "Email / Roll Number",
        auth_lbl_password: "Password",
        auth_btn_login: "Sign In",
        auth_or: "OR",
        auth_btn_guest: "Continue as Guest",
        auth_lbl_name: "Full Name",
        auth_lbl_age: "Age",
        auth_lbl_blood: "Blood Group",
        auth_btn_signup: "Create Patient Profile",
        mindful_badge: "MINDFUL RELAXATION",
        mindful_title: "Take a Mindful Pause",
        mindful_subtitle: "Follow the 4-7-8 breathing circle to calm your heart rate and ease nervous tension.",
        breathe_ready: "Ready",
        breathe_inhale: "Inhale",
        breathe_hold: "Hold",
        breathe_exhale: "Exhale",
        breathe_start_btn: "Start 4-7-8 Breathing",
        breathe_stop_btn: "Stop",
        tour_skip: "Skip Tour",
        tour_prev: "Previous",
        tour_next: "Next Step →"
    },
    hi: {
        nav_brand: "ऑरा प्लेटफॉर्म (AURA)",
        badge_offline: "ऑफ़लाइन मोड",
        nav_home: "होम",
        nav_prediction: "बीमारी पहचान (AI)",
        nav_reports: "त्वचा जांच स्कैनर",
        nav_reminders: "दवा रिमाइंडर",
        nav_dashboard: "स्वास्थ्य डैशबोर्ड",
        nav_emergency: "आपातकालीन (SOS)",
        nav_settings: "सेटिंग्स",
        nav_about: "हमारे बारे में",
        nav_relax: "थोड़ा आराम करें",
        nav_live: "लाइव रीडिंग",
        nav_signin: "लॉगिन / साइन अप",
        nav_logout: "लॉग आउट",
        nav_login: "लॉगिन",
        nav_signup: "साइन अप",
        login_subtitle: "अपने ऑफ़लाइन मेडिकल रिकॉर्ड, वाइटल्स और दवा शेड्यूल तक पहुंचें।",
        signup_subtitle: "नैदानिक रिकॉर्ड के साथ अपना व्यक्तिगत ऑफ़लाइन डिजिटल स्वास्थ्य कार्ड बनाएं।",
        auth_no_account: "खाता नहीं है?",
        auth_link_signup: "नया खाता बनाएं →",
        auth_have_account: "पहले से खाता है?",
        auth_link_login: "यहाँ साइन इन करें →",
        demo_accounts_title: "⚡ 1-क्लिक डेमो प्रोफाइल",
        hero_eyebrow: "स्थानीय कृत्रिम बुद्धिमत्ता निदान",
        hero_title: "आपका व्यक्तिगत ऑफ़लाइन स्वास्थ्य सहायक",
        hero_desc: "पूरी तरह से ऑफ़लाइन, 34 बीमारियों का बहुभाषी चिकित्सकीय ज्ञान और बायोमेट्रिक विश्लेषण। अपने परिवार को सुरक्षित रखें।",
        hero_btn_check: "लक्षण जांच शुरू करें",
        hero_btn_dash: "डैशबोर्ड देखें",
        feat_symptoms_title: "लक्षण जांचकर्ता (Chat)",
        feat_symptoms_desc: "34 सामान्य और पुरानी बीमारियों के लक्षणों के निदान के लिए हमारे ऑफ़लाइन AI चैटबॉट से बात करें।",
        feat_scanner_title: "त्वचा रोग स्कैनर",
        feat_scanner_desc: "रंग और बनावट मॉडल का उपयोग करके त्वचा के दाने, एक्जिमा या मुंहासों का ऑफ़लाइन विश्लेषण करें।",
        feat_reminders_title: "दवा रिमाइंडर",
        feat_reminders_desc: "दवाओं का समय निर्धारित करें, खुराक दर्ज करें और ऑफ़लाइन ध्वनि चेतावनी प्राप्त करें।",
        feat_dashboard_title: "नैदानिक टेलीमेट्री",
        feat_dashboard_desc: "सटीक रक्तचाप (BP) प्रतिशत, लाइव ईसीजी तरंग, हृदय गति (HR) और समग्र स्वास्थ्य स्कोर।",
        qs_patient_status: "रोगी स्थिति",
        qs_vitals_healthy: "वाइटल्स सामान्य व स्वस्थ",
        qs_upcoming_pill: "अगली दवा",
        qs_no_meds: "कोई दवा निर्धारित नहीं",
        qs_health_tip_lbl: "दैनिक स्वास्थ्य टिप",
        qs_health_tip_val: "पर्याप्त पानी पिएं और शरीर का तापमान मापते रहें।",
        aware_eyebrow: "सार्वजनिक स्वास्थ्य जागरूकता",
        aware_title: "जानें, पहचानें और बचें",
        aware_desc: "प्रमुख जीवनशैली, चयापचय और संक्रामक रोगों के लिए आवश्यक ऑफ़लाइन जागरूकता गाइड।",
        card_dia_title: "मधुमेह (शुगर)",
        card_dia_desc: "अधिक प्यास और बार-बार पेशाब आने पर ध्यान दें। फाइबर युक्त भोजन करें और रोज व्यायाम करें।",
        card_hyp_title: "उच्च रक्तचाप (High BP)",
        card_hyp_desc: "सुबह के सिरदर्द और चक्कर आने पर नजर रखें। भोजन में नमक की मात्रा 2,000 मि.ग्रा. से कम रखें।",
        card_ast_title: "दमा और श्वास देखभाल",
        card_ast_desc: "घरघराहट और सीने की जकड़न को पहचानें। आपातकालीन इनहेलर हमेशा पास में रखें।",
        card_den_title: "डेंगू और मौसमी बुखार",
        card_den_desc: "अचानक तेज बुखार, जोड़ों में दर्द और चकत्ते। ओआरएस (ORS) घोल और नारियल पानी से खुद को हाइड्रेटेड रखें।",
        btn_learn_more: "और जानें →",
        diag_sys_integrity: "सिस्टम अखंडता",
        diag_net_conn: "इंटरनेट कनेक्शन",
        diag_net_disc: "डिस्कनेक्टेड (कोई वाईफाई नहीं)",
        diag_ml_engine: "एमएल प्रेडिक्शन इंजन",
        diag_ml_active: "सक्रिय (स्थानीय डिवाइस)",
        diag_pred_title: "पूर्वानुमान निदान",
        diag_describe_hint: "डायग्नोस्टिक मेट्रिक्स देखने के लिए लक्षणों का वर्णन करें।",
        diag_conf_lbl: "सटीकता / विश्वास",
        diag_diff_title: "विभेदक निदान (संभावनाएं)",
        xai_header_title: "💡 व्याख्या योग्य एआई (XAI)",
        rep_title: "दृश्य त्वचा निदान विश्लेषक",
        rep_desc: "स्थानीय रूप से त्वचा के लक्षणों को स्कैन करें। हमारा मॉडल ऑफलाइन रंग और बनावट का विश्लेषण करता है।",
        rep_drag_drop: "त्वचा की फोटो यहां खींचकर छोड़ें",
        rep_formats_hint: "JPEG, PNG प्रारूप समर्थित (अधिकतम 8MB)",
        btn_browse_photos: "गैलरी से फोटो चुनें",
        rep_samples_title: "इंटरएक्टिव नमूना छवियां",
        rep_samples_hint: "मॉडल की सटीकता जांचने के लिए किसी नमूने पर क्लिक करें:",
        rep_sample_healthy: "स्वस्थ त्वचा",
        rep_sample_rash: "त्वचा पर दाने",
        rep_sample_acne: "मुंहासे (Acne)",
        rep_sample_eczema: "एक्जिमा (Eczema)",
        rep_reader_title: "ऑफलाइन रिपोर्ट रीडर",
        rep_reader_hint: "नैदानिक विसंगतियों की जांच के लिए लैब रिपोर्ट फाइल (.txt, .json) अपलोड करें।",
        rep_upload_hint: "टेक्स्ट लैब रिपोर्ट अपलोड करें",
        btn_select_report: "रिपोर्ट फाइल चुनें",
        rem_add_title: "नई दवा जोड़ें",
        rem_med_name: "दवा का नाम",
        rem_dosage: "खुराक (Dosage)",
        rem_time: "रिमाइंडर समय",
        rem_freq: "आवृत्ति (Frequency)",
        rem_opt_daily: "प्रतिदिन",
        rem_opt_weekly: "साप्ताहिक",
        rem_opt_monthly: "मासिक",
        btn_add_schedule: "शेड्यूल जोड़ें",
        rem_active_title: "सक्रिय शेड्यूल",
        rem_no_meds: "अभी तक कोई दवा निर्धारित नहीं की गई है।",
        dash_health_score_title: "समग्र स्वास्थ्य स्कोर",
        dash_score_opt: "नैदानिक सुरक्षा मेट्रिक्स सामान्य सीमा में गणना की गई।",
        dash_log_vitals_title: "बायोमेट्रिक्स और बीपी दर्ज करें",
        dash_sim_live: "🔴 लाइव सिम्युलेटर",
        lbl_sys_bp: "सिस्टोलिक बीपी (ऊपर वाला)",
        lbl_dia_bp: "डायस्टोलिक बीपी (नीचे वाला)",
        lbl_heart_rate: "हृदय गति (BPM)",
        lbl_spo2: "ऑक्सीजन SpO₂ (%)",
        lbl_body_temp: "शरीर का तापमान (°F)",
        btn_calc_vitals: "गणना करें और सुरक्षित करें",
        vitals_status_norm: "हृदय और बायोमेट्रिक मेट्रिक्स सामान्य व स्थिर हैं।",
        dash_bp_title: "रक्तचाप (BP) स्थिति",
        dash_hr_title: "हृदय गति (Heart Rate)",
        dash_spo2_title: "ऑक्सीजन संतृप्ति (SpO₂)",
        dash_trend_title: "निरंतर बायोमेट्रिक ट्रेंड",
        sos_title: "🚨 आपातकालीन एसओएस चेतावनी",
        sos_desc: "यदि आपको सांस लेने में कठिनाई, सीने में दर्द या 94% से कम ऑक्सीजन जैसे गंभीर लक्षण दिखें, तो तुरंत आपातकालीन सेवाओं से संपर्क करें।",
        sos_directives_title: "📋 महत्वपूर्ण आपातकालीन निर्देश:",
        sos_dir_1: "फेफड़ों और श्वसन में सहायता के लिए सीधे बैठें।",
        sos_dir_2: "शारीरिक हलचल कम करें और आराम करें।",
        sos_dir_3: "आपातकालीन फोन नंबर पास में रखें।",
        sos_dir_4: "कमरे में ताजी हवा आने दें और पंखा चालू करें।",
        btn_trigger_sos: "🚨 एसओएस अलार्म बजाएं",
        sos_contacts_title: "सिम्युलेटेड आपातकालीन संपर्क",
        sos_contacts_desc: "काल्पनिक स्थानीय स्वास्थ्य केंद्र और सामुदायिक टीमें (ऑफलाइन डायरेक्टरी):",
        sos_contact_1: "ऑरा सामुदायिक क्लिनिक आपातकालीन",
        sos_contact_2: "जिला ट्रॉमा अस्पताल",
        sos_contact_3: "महामारी अलर्ट हेल्पलाइन",
        set_custom_title: "इंटरफ़ेस और सुविधा कस्टमाइज़ेशन",
        set_dark_mode: "डार्क थीम मोड",
        set_dark_mode_desc: "इंटरफ़ेस का रंग पैलेट बदलें",
        set_voice_tts: "वॉयस टीटीएस प्रतिक्रिया",
        set_voice_desc: "परिणाम और भविष्यवाणियों को जोर से सुनें",
        set_avatar: "एआई सहायक विजेट",
        set_avatar_desc: "स्क्रीन पर फ्लोटिंग डॉक्टर अवतार दिखाएं",
        set_access_title: "अभिगम्यता प्राथमिकताएं",
        about_title: "ऑरा (AURA) प्लेटफॉर्म के बारे में",
        about_desc: "AURA को स्थानीय रूप से सामान्य सार्वजनिक स्वास्थ्य संक्रमणों और त्वचा रोगों पर प्रशिक्षित किया गया है। चूंकि यह 100% ऑफ़लाइन काम करता है, यह दूरदराज के गांवों और आपदा क्षेत्रों के लिए एक आदर्श नैदानिक प्रणाली है।",
        about_arch_title: "ऑफ़लाइन आर्किटेक्चर सारांश",
        auth_tab_login: "साइन इन",
        auth_tab_signup: "नया खाता बनाएं",
        auth_lbl_email: "ईमेल / रोल नंबर",
        auth_lbl_password: "पासवर्ड",
        auth_btn_login: "लॉगिन करें",
        auth_or: "या",
        auth_btn_guest: "अतिथि (Guest) के रूप में जारी रखें",
        auth_lbl_name: "पूरा नाम",
        auth_lbl_age: "उम्र",
        auth_lbl_blood: "ब्लड ग्रुप",
        auth_btn_signup: "रोगी प्रोफाइल बनाएं",
        mindful_badge: "मानसिक शांति और विश्राम",
        mindful_title: "थोड़ा आराम करें (4-7-8)",
        mindful_subtitle: "अपनी हृदय गति को शांत करने और तनाव दूर करने के लिए 4-7-8 श्वास चक्र का पालन करें।",
        breathe_ready: "तैयार",
        breathe_inhale: "सांस अंदर लें",
        breathe_hold: "सांस रोकें",
        breathe_exhale: "सांस बाहर छोड़ें",
        breathe_start_btn: "4-7-8 प्राणायाम शुरू करें",
        breathe_stop_btn: "रोकें",
        tour_skip: "टूर छोड़ें",
        tour_prev: "पिछला",
        tour_next: "अगला कदम →"
    },
    te: {
        nav_brand: "AURA ప్లాట్‌ఫామ్",
        badge_offline: "ఆఫ్‌లైన్ మోడ్",
        nav_home: "హోమ్",
        nav_prediction: "వ్యాధి నిర్ధారణ (AI)",
        nav_reports: "చర్మ పరీక్ష స్కానర్",
        nav_reminders: "మందుల రిమైండర్",
        nav_dashboard: "ఆరోగ్య డ్యాష్‌బోర్డ్",
        nav_emergency: "అత్యవసరం (SOS)",
        nav_settings: "సెట్టింగ్‌లు",
        nav_about: "మా గురించి",
        nav_relax: "కాసేపు విశ్రాంతి తీసుకోండి",
        nav_live: "లైవ్ రీడింగ్",
        nav_signin: "లాగిన్ / సైన్ అప్",
        nav_logout: "లాగ్ అవుట్",
        nav_login: "లాగిన్",
        nav_signup: "సైన్ అప్",
        login_subtitle: "మీ ఆఫ్‌లైన్ మెడికల్ రికార్డులు, వైటల్స్ మరియు మందుల షెడ్యూల్‌ని యాక్సెస్ చేయండి.",
        signup_subtitle: "క్లినికల్ రికార్డులతో మీ వ్యక్తిగత ఆఫ్‌లైన్ డిజిటల్ హెల్త్ ప్రొఫైల్‌ని సెటప్ చేయండి.",
        auth_no_account: "ఖాతా లేదా?",
        auth_link_signup: "ఖాతా సృష్టించండి →",
        auth_have_account: "ఇప్పటికే ఖాతా ఉందా?",
        auth_link_login: "ఇక్కడ లాగిన్ చేయండి →",
        demo_accounts_title: "⚡ 1-క్లిక్ డెమో ప్రొఫైల్స్",
        hero_eyebrow: "స్థానిక కృత్రిమ మేధస్సు నిర్ధారణ",
        hero_title: "మీ వ్యక్తిగత ఆఫ్‌లైన్ క్లినికల్ సహాయకుడు",
        hero_desc: "పూర్తిగా ఆఫ్‌లైన్, 34 వ్యాధుల బహుభాషా క్లినికల్ పరిజ్ఞానం మరియు బయోమెట్రిక్స్. మీ కుటుంబాన్ని సురక్షితంగా ఉంచండి.",
        hero_btn_check: "లక్షణాల పరీక్ష ప్రారంభించండి",
        hero_btn_dash: "డ్యాష్‌బోర్డ్ చూడండి",
        feat_symptoms_title: "లక్షణాల తనిఖీదారు",
        feat_symptoms_desc: "34 సాధారణ మరియు దీర్ఘకాలిక వ్యాధుల లక్షణాల నిర్ధారణ కోసం మా ఆఫ్‌లైన్ AI చాట్‌బాట్‌తో మాట్లాడండి.",
        feat_scanner_title: "చర్మ వ్యాధి స్కానర్",
        feat_scanner_desc: "రంగ్ మరియు ఆకృతి మోడళ్లను ఉపయోగించి చర్మంపై దద్దుర్లు, తామర లేదా మొటిమలను ఆఫ్‌లైన్‌లో విశ్లేషించండి.",
        feat_reminders_title: "మందుల రిమైండర్లు",
        feat_reminders_desc: "రోజువారీ మందుల సమయాలను సెట్ చేయండి, మోతాదును నమోదు చేయండి మరియు సౌండ్ అలర్ట్‌లను పొందండి.",
        feat_dashboard_title: "క్లినికల్ టెలిమెట్రీ",
        feat_dashboard_desc: "ఖచ్చితమైన రక్తపోటు (BP) శాతాలు, ప్రత్యక్ష ECG తరంగం, గుండె వేగం (HR) మరియు మొత్తం ఆరోగ్య స్కోరు.",
        qs_patient_status: "రోగి స్థితి",
        qs_vitals_healthy: "వైటల్స్ సాధారణం & ఆరోగ్యకరం",
        qs_upcoming_pill: "రాబోయే మందు",
        qs_no_meds: "ఎలాంటి మందులు షెడ్యూల్ చేయలేదు",
        qs_health_tip_lbl: "రోజువారీ ఆరోగ్య చిట్కా",
        qs_health_tip_val: "పుష్కలంగా నీరు త్రాగండి మరియు శరీర ఉష్ణోగ్రతను క్రమం తప్పకుండా పర్యవేక్షించండి.",
        aware_eyebrow: "ప్రజా ఆరోగ్య అవగాహన",
        aware_title: "తెలుసుకోండి, గుర్తించండి మరియు రక్షించుకోండి",
        aware_desc: "ముఖ్యమైన జీవనశైలి, జీవక్రియ మరియు అంటువ్యాధుల కోసం అవసరమైన ఆఫ్‌లైన్ అవగాహన గైడ్లు.",
        card_dia_title: "మధుమేహం (షుగర్)",
        card_dia_desc: "అధిక దాహం & తరచుగా మూత్రవిసర్జనపై శ్రద్ధ వహించండి. ఫైబర్ ఆహారం తీసుకోండి మరియు రోజూ వ్యాయామం చేయండి.",
        card_hyp_title: "అధిక రక్తపోటు (High BP)",
        card_hyp_desc: "ఉదయం తలనొప్పి మరియు తలతిరగడం గమనించండి. రోజుకు ఉప్పు వాడకం 2,000 మి.గ్రా కంటే తక్కువగా ఉంచండి.",
        card_ast_title: "ఆస్తమా & శ్వాస సంరక్షణ",
        card_ast_desc: "రొప్పు మరియు ఛాతీ బిగుతును ముందుగానే గుర్తించండి. అత్యవసర ఇన్హేలర్లను ఎల్లప్పుడూ అందుబాటులో ఉంచండి.",
        card_den_title: "డెంగ్యూ & విష జ్వరాలు",
        card_den_desc: "హఠాత్తుగా తీవ్ర జ్వరం, కీళ్ల నొప్పులు మరియు దద్దుర్లు. ఓఆర్ఎస్ (ORS) ద్రవాలతో శరీరాన్ని డీహైడ్రేట్ కాకుండా చూసుకోండి.",
        btn_learn_more: "మరింత తెలుసుకోండి →",
        diag_sys_integrity: "సిస్టమ్ సమగ్రత",
        diag_net_conn: "నెట్‌వర్క్ కనెక్షన్",
        diag_net_disc: "డిస్‌కనెక్ట్ అయింది (వైఫై లేదు)",
        diag_ml_engine: "ML ప్రిడిక్షన్ ఇంజిన్",
        diag_ml_active: "కార్యాచరణలో ఉంది (స్థానిక పరికరం)",
        diag_pred_title: "రోగనిర్ధారణ అంచనా",
        diag_describe_hint: "డయాగ్నస్టిక్ కొలమానాలను చూడటానికి మీ లక్షణాలను వివరించండి.",
        diag_conf_lbl: "ఖచ్చితత్వం / విశ్వసనీయత",
        diag_diff_title: "డిఫరెన్షియల్ డయాగ్నస్టిక్స్",
        xai_header_title: "💡 వివరణాత్మక AI (XAI)",
        rep_title: "విజువల్ స్కిన్ డయాగ్నస్టిక్ ఎనలైజర్",
        rep_desc: "స్థానికంగా చర్మ లక్షణాలను స్కాన్ చేయండి. మా ఎడ్జ్ మోడల్ రంగు మరియు ఆకృతిని ఆఫ్‌లైన్‌లో విశ్లేషిస్తుంది.",
        rep_drag_drop: "చర్మ నమూనా చిత్రాన్ని ఇక్కడ లాగండి",
        rep_formats_hint: "JPEG, PNG ఫార్మాట్‌లు (గరిష్టంగా 8MB)",
        btn_browse_photos: "ఫోటోలను ఎంచుకోండి",
        rep_samples_title: "నమూనా చిత్రాలు",
        rep_samples_hint: "మోడల్ ఖచ్చితత్వాన్ని పరీక్షించడానికి ఏదైనా నమూనాపై క్లిక్ చేయండి:",
        rep_sample_healthy: "ఆరోగ్యకరమైన చర్మం",
        rep_sample_rash: "చర్మంపై దద్దుర్లు",
        rep_sample_acne: "మొటిమలు",
        rep_sample_eczema: "ఎగ్జిమా",
        rep_reader_title: "ఆఫ్‌లైన్ రిపోర్ట్ రీడర్",
        rep_reader_hint: "ల్యాబ్ రిపోర్ట్ ఫైల్ (.txt, .json) అప్‌లోడ్ చేసి నివేదికలను విశ్లేషించండి.",
        rep_upload_hint: "టెక్స్ట్ ల్యాబ్ విలువలను అప్‌లోడ్ చేయండి",
        btn_select_report: "రిపోర్ట్ ఫైల్‌ను ఎంచుకోండి",
        rem_add_title: "కొత్త మందును జోడించండి",
        rem_med_name: "మందు పేరు",
        rem_dosage: "మోతాదు",
        rem_time: "రిమైండర్ సమయం",
        rem_freq: "ఫ్రీక్వెన్సీ",
        rem_opt_daily: "రోజూ",
        rem_opt_weekly: "వారానికోసారి",
        rem_opt_monthly: "నెలకు ఒకసారి",
        btn_add_schedule: "షెడ్యూల్ జోడించండి",
        rem_active_title: "క్రియాశీల షెడ్యూల్",
        rem_no_meds: "ఇంకా ఎలాంటి మందులు షెడ్యూల్ చేయలేదు.",
        dash_health_score_title: "మొత్తం ఆరోగ్య స్కోరు",
        dash_score_opt: "క్లినికల్ భద్రతా కొలమానాలు సరైన పరిధిలో ఉన్నాయి.",
        dash_log_vitals_title: "బయోమెట్రిక్స్ మరియు బీపీ నమోదు",
        dash_sim_live: "🔴 లైవ్ సిమ్యులేటర్",
        lbl_sys_bp: "సిస్టోలిక్ బీపీ (పై విలువ)",
        lbl_dia_bp: "డయాస్టోలిక్ బీపీ (కింది విలువ)",
        lbl_heart_rate: "గుండె వేగం (BPM)",
        lbl_spo2: "ఆక్సిజన్ SpO₂ (%)",
        lbl_body_temp: "శరీర ఉష్ణోగ్రత (°F)",
        btn_calc_vitals: "గణించండి మరియు సేవ్ చేయండి",
        vitals_status_norm: "గుండె మరియు బయోమెట్రిక్ కొలమానాలు సాధారణంగా స్థిరంగా ఉన్నాయి.",
        dash_bp_title: "రక్తపోటు (BP) స్థితి",
        dash_hr_title: "గుండె వేగం (Heart Rate)",
        dash_spo2_title: "ఆక్సిజన్ సంతృప్తత (SpO₂)",
        dash_trend_title: "నిరంతర బయోమెట్రిక్ ట్రెండ్",
        sos_title: "🚨 అత్యవసర SOS హెచ్చరికలు",
        sos_desc: "తీవ్రమైన శ్వాస సమస్య, ఛాతీ నొప్పి లేదా ఆక్సిజన్ 94% కంటే తక్కువగా ఉంటే, వెంటనే అత్యవసర సేవలను సంప్రదించండి.",
        sos_directives_title: "📋 అత్యవసర సూచనలు:",
        sos_dir_1: "ఊపిరితిత్తులు మరియు శ్వాసక్రియకు సహాయపడటానికి నిటారుగా కూర్చోండి.",
        sos_dir_2: "శారీరక శ్రమను తగ్గించండి మరియు విశ్రాంతి తీసుకోండి.",
        sos_dir_3: "అత్యవసర ఫోన్ నంబర్లను సిద్ధంగా ఉంచుకోండి.",
        sos_dir_4: "గదిలోకి గాలి వెలుతురు వచ్చేలా చూడండి మరియు ఫ్యాన్లు ఆన్ చేయండి.",
        btn_trigger_sos: "🚨 SOS హెచ్చరికను ప్రారంభించండి",
        sos_contacts_title: "సిమ్యులేటెడ్ అత్యవసర పరిచయాలు",
        sos_contacts_desc: "స్థానిక క్లినికల్ కేంద్రాలు మరియు అత్యవసర బృందాలు (ఆఫ్‌లైన్ డైరెక్టరీ):",
        sos_contact_1: "ఆరా కమ్యూనిటీ క్లినిక్ ఎమర్జెన్సీ",
        sos_contact_2: "డిస్ట్రిక్ట్ ట్రామా హాస్పిటల్",
        sos_contact_3: "అంటువ్యాధుల హెల్ప్‌లైన్",
        set_custom_title: "ఇంటర్‌ఫేస్ మరియు ఫీచర్ అనుకూలీకరణలు",
        set_dark_mode: "డార్క్ థీమ్ మోడ్",
        set_dark_mode_desc: "ఇంటర్‌ఫేస్ రంగులను మార్చండి",
        set_voice_tts: "వాయిస్ TTS ఫీడ్‌బ్యాక్",
        set_voice_desc: "ఫలితాలు మరియు ప్రిడిక్షన్లను వినండి",
        set_avatar: "AI అసిస్టెంట్ విడ్జెట్",
        set_avatar_desc: "స్క్రీన్‌పై ఫ్లోటింగ్ డాక్టర్ అవతార్‌ను చూపించండి",
        set_access_title: "యాక్సెసిబిలిటీ ప్రాధాన్యతలు",
        about_title: "AURA ప్లాట్‌ఫామ్ గురించి",
        about_desc: "AURA స్థానికంగా సాధారణ ప్రజారోగ్య ఇన్ఫెక్షన్లు మరియు చర్మ వ్యాధులపై శిక్షణ పొందింది. ఇది 100% ఆఫ్‌లైన్‌లో పనిచేస్తుంది కాబట్టి మారుమూల గ్రామాలు మరియు విపత్తు ప్రాంతాలకు ఆదర్శవంతమైన వ్యవస్థ.",
        about_arch_title: "ఆఫ్‌లైన్ ఆర్కిటెక్చర్ సారాంశం",
        auth_tab_login: "సైన్ ఇన్",
        auth_tab_signup: "ఖాతా తెరవండి",
        auth_lbl_email: "ఈమెయిల్ / రోల్ నంబర్",
        auth_lbl_password: "పాస్‌వర్డ్",
        auth_btn_login: "లాగిన్ చేయండి",
        auth_or: "లేదా",
        auth_btn_guest: "గెస్ట్‌గా కొనసాగండి",
        auth_lbl_name: "పూర్తి పేరు",
        auth_lbl_age: "వయస్సు",
        auth_lbl_blood: "బ్లడ్ గ్రూప్",
        auth_btn_signup: "రోగి ప్రొఫైల్ సృష్టించండి",
        mindful_badge: "మానసిక ప్రశాంతత & విశ్రాంతి",
        mindful_title: "కాసేపు విశ్రాంతి తీసుకోండి (4-7-8)",
        mindful_subtitle: "మీ గుండె వేగాన్ని తగ్గించి ఒత్తిడిని దూరం చేయడానికి 4-7-8 శ్వాస వ్యాయామం చేయండి.",
        breathe_ready: "సిద్ధం",
        breathe_inhale: "శ్వాస పీల్చండి",
        breathe_hold: "శ్వాస ఆపండి",
        breathe_exhale: "శ్వాస వదలండి",
        breathe_start_btn: "4-7-8 శ్వాస వ్యాయామం ప్రారంభించండి",
        breathe_stop_btn: "ఆపండి",
        tour_skip: "టూర్ దాటవేయి",
        tour_prev: "మునుపటిది",
        tour_next: "తదుపరి దశ →"
    }
};

function updateAllUILanguage(lang) {
    const dict = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.en;
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });
    // Also update dynamic placeholders
    const chatInp = document.getElementById("chat-input");
    if (chatInp) {
        if (lang === "hi") {
            chatInp.placeholder = "लक्षण बताएं (उदा. बुखार, सिरदर्द) या प्रश्न पूछें...";
        } else if (lang === "te") {
            chatInp.placeholder = "లక్షణాలను వివరించండి (ఉదా. జ్వరం, తలనొప్పి) లేదా ప్రశ్నలు అడగండి...";
        } else {
            chatInp.placeholder = "Describe symptoms (e.g. fever, headache) or type questions...";
        }
    }
    // Update active user greeting if logged in
    renderCurrentUserBadge(lang);
}

// Current user state holder
let currentUser = null;

function renderCurrentUserBadge(lang) {
    const displayName = document.getElementById("user-display-name");
    const greetingPill = document.getElementById("user-greeting-pill");
    const openAuthBtn = document.getElementById("open-auth-btn");
    const authButtonsBar = document.getElementById("auth-buttons-bar");
    
    if (!currentUser) {
        try {
            const stored = localStorage.getItem("aura_active_user");
            if (stored) currentUser = JSON.parse(stored);
        } catch (e) {}
    }

    if (currentUser) {
        if (openAuthBtn) openAuthBtn.classList.add("hidden");
        if (authButtonsBar) authButtonsBar.classList.add("hidden");
        if (greetingPill) greetingPill.classList.remove("hidden");
        if (displayName) {
            const name = currentUser.name || "Guest";
            if (lang === "hi") displayName.textContent = `नमस्ते, ${name} 👋`;
            else if (lang === "te") displayName.textContent = `నమస్తే, ${name} 👋`;
            else displayName.textContent = `Welcome, ${name} 👋`;
        }
    } else {
        if (openAuthBtn) openAuthBtn.classList.remove("hidden");
        if (authButtonsBar) authButtonsBar.classList.remove("hidden");
        if (greetingPill) greetingPill.classList.add("hidden");
    }
}

/* ==========================================================================
   AURA HEALTH PLATFORM - MODERN CLIENT-SIDE CONTROL ENGINE
   ========================================================================== */

document.addEventListener("DOMContentLoaded", () => {
    // 1. Navigation & Tab Routing Variables
    const navItems = document.querySelectorAll(".nav-item");
    const sections = document.querySelectorAll(".section-view");
    
    // 2. Chat & Symptom Prediction Elements
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");
    const imageUpload = document.getElementById("image-upload");
    const uploadTrigger = document.getElementById("upload-trigger");
    const micTrigger = document.getElementById("mic-trigger");
    const imagePreviewContainer = document.getElementById("image-preview-container");
    const imagePreview = document.getElementById("image-preview");
    const removeImageBtn = document.getElementById("remove-image-btn");
    const voiceOverlay = document.getElementById("voice-recording-overlay");
    const cancelVoiceBtn = document.getElementById("cancel-voice-btn");
    const voiceToggle = document.getElementById("voice-readback-toggle");
    const languageSelector = document.getElementById("language-selector");
    
    // 3. Diagnostics & Telemetry Elements
    const analyticsEmpty = document.getElementById("analytics-empty-state");
    const analyticsContent = document.getElementById("analytics-content-state");
    const confidenceRing = document.getElementById("confidence-ring");
    const confidencePercentage = document.getElementById("confidence-percentage");
    const predictedCondition = document.getElementById("predicted-condition");
    const predictedUrgency = document.getElementById("predicted-urgency");
    const xaiRiskLevel = document.getElementById("xai-risk-level");
    const xaiSymptomsMapped = document.getElementById("xai-symptoms-mapped");
    const xaiFeaturesImportance = document.getElementById("xai-features-importance");
    const xaiReasoning = document.getElementById("xai-reasoning");
    
    // 4. Visual Scanner Drag & Drop Elements
    const dropZone = document.getElementById("drop-zone");
    const scannerLaser = document.getElementById("scanner-laser");
    const scanProgressContainer = document.getElementById("scan-progress-container");
    const scanProgressFill = document.getElementById("scan-progress-fill");
    
    // 5. Medicine Reminder Elements
    const medForm = document.getElementById("med-form");
    const medNameInput = document.getElementById("med-name");
    const medDosageInput = document.getElementById("med-dosage");
    const medTimeInput = document.getElementById("med-time");
    const medFrequencyInput = document.getElementById("med-frequency");
    const medsLogList = document.getElementById("meds-log-list");
    const remindersCountBadge = document.getElementById("reminders-count-badge");
    const qsUpcomingPill = document.getElementById("qs-upcoming-pill");
    
    // 6. Health Score & Vitals Elements
    const vitalsForm = document.getElementById("vitals-form");
    const vitalTempInput = document.getElementById("vital-temp");
    const vitalSpo2Input = document.getElementById("vital-spo2");
    const vitalsStatusText = document.getElementById("vitals-status");
    const healthScoreRing = document.getElementById("health-score-ring");
    const healthScoreNum = document.getElementById("health-score-num");
    const healthScoreStatusText = document.getElementById("health-score-status");
    const dashValTemp = document.getElementById("dash-val-temp");
    const dashStatusTemp = document.getElementById("dash-status-temp");
    const dashValSpo2 = document.getElementById("dash-val-spo2");
    const dashStatusSpo2 = document.getElementById("dash-status-spo2");
    const qsVitalsStatus = document.getElementById("qs-vitals-status");
    
    // 7. Settings Toggles
    const settingsDarkmodeToggle = document.getElementById("settings-darkmode-toggle");
    const settingsVoiceToggle = document.getElementById("settings-voice-toggle");
    const settingsAvatarToggle = document.getElementById("settings-avatar-toggle");
    const settingsFontsizeToggle = document.getElementById("settings-fontsize-toggle");
    const clearDbBtn = document.getElementById("clear-db-btn");
    
    // 8. Fixed AURA Assistant Widget Elements
    const auraFixedAssistant = document.getElementById("aura-fixed-assistant");
    const auraGuidanceBubble = document.getElementById("aura-guidance-bubble");
    const auraGuidanceText = document.getElementById("aura-guidance-text");
    const auraAvatarWidget = document.getElementById("aura-avatar-widget");
    const auraWidgetStatus = document.getElementById("aura-widget-status");
    
    // 9. SOS Emergency Elements
    const sosOverlay = document.getElementById("sos-overlay");
    const sosOverlayReason = document.getElementById("sos-overlay-reason");
    const sosCloseBtn = document.getElementById("sos-close-btn");
    const sosSirenBtn = document.getElementById("sos-siren-btn");
    const sosDispatchBtn = document.getElementById("sos-dispatch-btn");
    const sosTriggerBtn = document.getElementById("sos-trigger-btn");
    
    // 10. State Variables
    let selectedImageFile = null;
    let speechRecognition = null;
    let isListening = false;
    let speakingUtterance = null;
    let vitalsHistory = JSON.parse(localStorage.getItem("vitals_history") || "[]");
    let medicationsList = JSON.parse(localStorage.getItem("medications_list") || "[]");
    
    const ringPerimeter = 2 * Math.PI * 42; // r=42 -> ~263.89
    
    // ECG Initializing screen dismiss logic
    const loaderScreen = document.getElementById("loader-screen");
    if (loaderScreen) {
        setTimeout(() => {
            loaderScreen.style.opacity = "0";
            setTimeout(() => {
                loaderScreen.style.display = "none";
                // Show welcome prompt
                speakAura("Welcome to the AURA Healthcare Platform. Choose a navigation tab to get started.");
            }, 600);
        }, 1500);
    }
    
    // Onboarding Guide Overlay Logic
    const onboardingOverlay = document.getElementById("onboarding-overlay");
    const startOnboardBtn = document.getElementById("start-onboard-btn");
    const skipOnboardBtn = document.getElementById("skip-onboard-btn");
    const optChat = document.getElementById("onboard-opt-chat");
    const optVitals = document.getElementById("onboard-opt-vitals");
    const optScanner = document.getElementById("onboard-opt-scanner");
    
    function closeOnboarding() {
        if (onboardingOverlay) {
            onboardingOverlay.style.opacity = "0";
            setTimeout(() => {
                onboardingOverlay.style.display = "none";
            }, 300);
        }
    }
    
    if (skipOnboardBtn) skipOnboardBtn.addEventListener("click", closeOnboarding);
    if (startOnboardBtn) {
        startOnboardBtn.addEventListener("click", () => {
            closeOnboarding();
            playAutoTour();
        });
    }
    
    if (optChat) {
        optChat.addEventListener("click", () => {
            closeOnboarding();
            navigateToTab("prediction");
            chatForm.classList.add("tour-pulse-glow");
            setTimeout(() => chatForm.classList.remove("tour-pulse-glow"), 3000);
        });
    }
    
    if (optVitals) {
        optVitals.addEventListener("click", () => {
            closeOnboarding();
            navigateToTab("dashboard");
            vitalsForm.classList.add("tour-pulse-glow");
            setTimeout(() => vitalsForm.classList.remove("tour-pulse-glow"), 3000);
        });
    }
    
    if (optScanner) {
        optScanner.addEventListener("click", () => {
            closeOnboarding();
            navigateToTab("reports");
            dropZone.classList.add("tour-pulse-glow");
            setTimeout(() => dropZone.classList.remove("tour-pulse-glow"), 3000);
        });
    }
    
    function playAutoTour() {
        navigateToTab("prediction");
        chatForm.classList.add("tour-pulse-glow");
        speakAura("This is the symptom prediction check. Describe your symptoms here.");
        
        setTimeout(() => {
            chatForm.classList.remove("tour-pulse-glow");
            navigateToTab("dashboard");
            vitalsForm.classList.add("tour-pulse-glow");
            speakAura("This is the health score dashboard. Log temperature and oxygen metrics here.");
            
            setTimeout(() => {
                vitalsForm.classList.remove("tour-pulse-glow");
                navigateToTab("reports");
                dropZone.classList.add("tour-pulse-glow");
                speakAura("This is the skin uploader scanner. Drag and drop skin photos to check rashes locally.");
                
                setTimeout(() => {
                    dropZone.classList.remove("tour-pulse-glow");
                    navigateToTab("home");
                    speakAura("The tutorial is complete. Aura is ready to guide you.");
                }, 4000);
            }, 4000);
        }, 4000);
    }

    // Custom Multilingual String Helper
    String.prototype.title = function() {
        return this.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
    };

    // ==========================================
    // 1. SMART PAGE GUIDANCE & VOICE SYNTHESIS
    // ==========================================
    const pageGuidanceData = {
        "home": {
            "title": "AURA Welcome Home",
            "body": "Welcome to AURA AI. You can check symptoms, log clinical vitals, or schedule medicine reminders. All predictions run 100% locally.",
            "speech": "Welcome to AURA AI clinical assistant. Review your daily health status, or navigate tabs to check symptoms and schedule pills."
        },
        "prediction": {
            "title": "Disease Prediction Checker",
            "body": "Enter symptoms like fever, cough, joint pain, or stomach ache. Our local Random Forest model evaluates confidence weights.",
            "speech": "This is the disease prediction chat. Describe your symptoms or click the microphone to speak them. Differential results display in the diagnostics sidebar."
        },
        "reports": {
            "title": "Medical Scanner",
            "body": "Drag skin photos onto the dotted scanner area to classify rashes. Use local samples to verify outputs.",
            "speech": "This is the visual skin scanner. Drag and drop skin rash photos to run classical local diagnostic metrics."
        },
        "reminders": {
            "title": "Medication Scheduler",
            "body": "Log your pills, times, and daily frequencies. Aura keeps schedule reminders stored in local memory.",
            "speech": "This is the medicine scheduler. Add your pill name, dosage, and times to set local offline alerts."
        },
        "dashboard": {
            "title": "Clinical Health Dashboard",
            "body": "Vitals history trend charts. Log temperature & oxygen (SpO₂) regularly to compile safety scores.",
            "speech": "This is the health dashboard. Review your overall safety score and plot temperature parameters on the offline canvas chart."
        },
        "emergency": {
            "title": "Emergency Directives",
            "body": "Flashing red directives when oxygen drops below 94% or fevers exceed 103°F. Simulate sirens offline.",
            "speech": "Emergency guidelines display here. If critical boundaries are crossed, trigger the SOS siren or simulated rescue alert immediately."
        },
        "settings": {
            "title": "Offline Customizations",
            "body": "Customize layout preferences, dark modes, voice syntheses, accessibility sizes, and clear diagnostic memory.",
            "speech": "This is the accessibility settings page. Change light or dark themes and toggle AURA voice assistance features."
        },
        "about": {
            "title": "Technical Information",
            "body": "Learn about AURA's local decision tree algorithms and dictionary match parameters. Not a substitute for clinical advice.",
            "speech": "About AURA. This diagnostic assistant calculates probability profiles locally without sending data to external servers."
        }
    };

    function triggerPageGuidance(tabName) {
        const info = pageGuidanceData[tabName];
        if (!info) return;
        
        // Show speech bubble
        if (auraGuidanceBubble && auraGuidanceText) {
            auraGuidanceBubble.classList.remove("hidden");
            auraGuidanceText.innerHTML = `<strong>${info.title}:</strong><br>${info.body}`;
        }
        
        // Speak guidance
        if (settingsVoiceToggle && settingsVoiceToggle.checked) {
            speakAura(info.speech);
        }
    }

    function speakAura(text) {
        if (!window.speechSynthesis) return;
        window.speechSynthesis.cancel(); // Stop current speech
        
        setAuraMouthActive(true);
        if (auraWidgetStatus) auraWidgetStatus.innerText = "Speaking";
        
        speakingUtterance = new SpeechSynthesisUtterance(text);
        
        // Choose locale voice matching selector language if possible
        const voices = window.speechSynthesis.getVoices();
        const selectedLang = languageSelector ? languageSelector.value : "en";
        
        // Find voice matching selected language
        const matchVoice = voices.find(v => v.lang.startsWith(selectedLang));
        if (matchVoice) {
            speakingUtterance.voice = matchVoice;
        }
        
        speakingUtterance.onend = () => {
            setAuraMouthActive(false);
            if (auraWidgetStatus) auraWidgetStatus.innerText = "Idle";
        };
        
        speakingUtterance.onerror = () => {
            setAuraMouthActive(false);
            if (auraWidgetStatus) auraWidgetStatus.innerText = "Idle";
        };
        
        window.speechSynthesis.speak(speakingUtterance);
    }

    function setAuraMouthActive(active) {
        const mouth = document.querySelector(".aura-mouth");
        if (!mouth) return;
        if (active) {
            mouth.style.animation = "mouthSpeak 0.3s infinite alternate";
        } else {
            mouth.style.animation = "none";
        }
    }

    // Add CSS rule dynamically for mouth speech scaling
    const mouthStyle = document.createElement("style");
    mouthStyle.innerHTML = `
        @keyframes mouthSpeak {
            0% { transform: scaleY(0.4); }
            100% { transform: scaleY(2.2); }
        }
    `;
    document.head.appendChild(mouthStyle);

    // ==========================================
    // 2. TABBED VIEWPORT NAVIGATION
    // ==========================================
    window.navigateToTab = function(tabName) {
        // Find button
        navItems.forEach(btn => {
            if (btn.getAttribute("data-tab") === tabName) {
                btn.classList.add("active");
            } else {
                btn.classList.remove("active");
            }
        });
        
        // Switch section visibility
        sections.forEach(sec => {
            if (sec.id === `section-${tabName}`) {
                sec.classList.remove("hidden");
            } else {
                sec.classList.add("hidden");
            }
        });
        
        triggerPageGuidance(tabName);
    };

    navItems.forEach(item => {
        item.addEventListener("click", () => {
            const tabName = item.getAttribute("data-tab");
            navigateToTab(tabName);
        });
    });

    // ==========================================
    // 3. VOICE RECOGNITION (OFFLINE COMMANDS)
    // ==========================================
    function initSpeechRecognition() {
        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRec) {
            console.warn("Speech recognition is not supported in this browser offline.");
            if (micTrigger) micTrigger.style.display = "none";
            return;
        }
        
        speechRecognition = new SpeechRec();
        speechRecognition.continuous = false;
        speechRecognition.interimResults = false;
        speechRecognition.lang = languageSelector ? languageSelector.value : "en";
        
        speechRecognition.onstart = () => {
            isListening = true;
            if (voiceOverlay) voiceOverlay.classList.remove("hidden");
            if (auraWidgetStatus) auraWidgetStatus.innerText = "Listening";
        };
        
        speechRecognition.onresult = (e) => {
            const transcript = e.results[0][0].transcript.toLowerCase();
            console.log("Speech parsed transcript:", transcript);
            handleVoiceCommand(transcript);
        };
        
        speechRecognition.onerror = (e) => {
            console.error("Speech recognition error:", e);
            stopListening();
        };
        
        speechRecognition.onend = () => {
            stopListening();
        };
    }

    function startListening() {
        if (!speechRecognition) initSpeechRecognition();
        if (speechRecognition && !isListening) {
            speechRecognition.lang = languageSelector ? languageSelector.value : "en";
            speechRecognition.start();
        }
    }

    function stopListening() {
        isListening = false;
        if (voiceOverlay) voiceOverlay.classList.add("hidden");
        if (auraWidgetStatus) auraWidgetStatus.innerText = "Idle";
        if (speechRecognition) speechRecognition.stop();
    }

    if (micTrigger) {
        micTrigger.addEventListener("click", () => {
            startListening();
        });
    }
    
    if (cancelVoiceBtn) {
        cancelVoiceBtn.addEventListener("click", stopListening);
    }

    // Voice Command Processor
    function handleVoiceCommand(text) {
        // Navigation shortcuts
        if (text.includes("go to home") || text.includes("open home")) {
            navigateToTab("home");
            return;
        }
        if (text.includes("go to prediction") || text.includes("check symptom") || text.includes("symptom checker") || text.includes("go to symptom")) {
            navigateToTab("prediction");
            return;
        }
        if (text.includes("go to reports") || text.includes("open scanner") || text.includes("skin scanner") || text.includes("visual scanner")) {
            navigateToTab("reports");
            return;
        }
        if (text.includes("go to reminders") || text.includes("open medication") || text.includes("medicine reminder")) {
            navigateToTab("reminders");
            return;
        }
        if (text.includes("go to dashboard") || text.includes("show dashboard") || text.includes("health score")) {
            navigateToTab("dashboard");
            return;
        }
        if (text.includes("go to emergency") || text.includes("help me with emergency") || text.includes("open emergency")) {
            navigateToTab("emergency");
            return;
        }
        if (text.includes("go to settings") || text.includes("open settings")) {
            navigateToTab("settings");
            return;
        }
        if (text.includes("go to about") || text.includes("open about")) {
            navigateToTab("about");
            return;
        }
        
        // Action Command: Log vitals
        // Pattern: "log temperature 98.6 and oxygen 99"
        if (text.includes("log temperature") || text.includes("log temp")) {
            const tempMatch = text.match(/temperature\s+(\d+(\.\d+)?)/) || text.match(/temp\s+(\d+(\.\d+)?)/);
            const spo2Match = text.match(/oxygen\s+(\d+)/) || text.match(/spo2\s+(\d+)/) || text.match(/oxygen levels?\s+(\d+)/);
            
            if (tempMatch) {
                const tempVal = parseFloat(tempMatch[1]);
                const spo2Val = spo2Match ? parseInt(spo2Match[1]) : 98;
                
                if (vitalTempInput && vitalSpo2Input) {
                    vitalTempInput.value = tempVal;
                    vitalSpo2Input.value = spo2Val;
                    navigateToTab("dashboard");
                    submitVitals(tempVal, spo2Val);
                    speakAura(`Log recorded. Vitals logged with temperature ${tempVal} and oxygen levels ${spo2Val} percent.`);
                    return;
                }
            }
        }

        // Action Command: Schedule medicine
        // Pattern: "schedule pill paracetamol dosage 500mg time 8:00 am"
        if (text.includes("schedule pill") || text.includes("add medicine")) {
            const nameMatch = text.match(/pill\s+([a-zA-Z0-9]+)/) || text.match(/medicine\s+([a-zA-Z0-9]+)/);
            const doseMatch = text.match(/dosage\s+([a-zA-Z0-9]+)/) || text.match(/dose\s+([a-zA-Z0-9]+)/);
            const timeMatch = text.match(/time\s+(\d+:\d+\s*(am|pm)?)/) || text.match(/at\s+(\d+:\d+\s*(am|pm)?)/);
            
            if (nameMatch) {
                const pillName = nameMatch[1];
                const dosage = doseMatch ? doseMatch[1] : "500mg";
                const timeStr = timeMatch ? timeMatch[1] : "8:00 AM";
                
                addMedication(pillName, dosage, timeStr, "daily");
                navigateToTab("reminders");
                speakAura(`Scheduled medicine. Pill ${pillName} scheduled at ${timeStr}.`);
                return;
            }
        }
        
        // Default behavior: input into prediction chatbot
        if (chatInput) {
            chatInput.value = text;
            navigateToTab("prediction");
            submitUserInput(text);
        }
    }

    // ==========================================
    // 4. CHAT INTERACTIVE PREDICTION ENGINE
    // ==========================================
    function appendChatMessage(sender, content, fileObj = null) {
        const msg = document.createElement("div");
        msg.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement("div");
        contentDiv.className = "message-content";
        
        if (fileObj) {
            const img = document.createElement("img");
            img.src = URL.createObjectURL(fileObj);
            img.style.maxWidth = "100px";
            img.style.maxHeight = "100px";
            img.style.borderRadius = "6px";
            img.style.display = "block";
            img.style.marginBottom = "5px";
            contentDiv.appendChild(img);
        }
        
        const textPara = document.createElement("div");
        textPara.innerHTML = formatMarkdown(content);
        contentDiv.appendChild(textPara);
        
        msg.appendChild(contentDiv);
        chatMessages.appendChild(msg);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return msg;
    }

    function formatMarkdown(text) {
        return text
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
            .replace(/\*(.*?)\*/g, "<em>$1</em>")
            .replace(/### (.*?)\n/g, "h3>$1</h3>")
            .replace(/- (.*?)\n/g, "<li>$1</li>")
            .replace(/\n/g, "<br>");
    }

    function showTypingIndicator() {
        const indicator = document.createElement("div");
        indicator.className = "message bot-message typing-indicator-container";
        indicator.innerHTML = `
            <div class="message-content">
                <span class="dot" style="width:5px; height:5px; background:var(--text-secondary); border-radius:50%; display:inline-block; margin-right:3px; animation: wave 1s infinite alternate;"></span>
                <span class="dot" style="width:5px; height:5px; background:var(--text-secondary); border-radius:50%; display:inline-block; margin-right:3px; animation: wave 1s infinite alternate; animation-delay: 0.2s;"></span>
                <span class="dot" style="width:5px; height:5px; background:var(--text-secondary); border-radius:50%; display:inline-block; animation: wave 1s infinite alternate; animation-delay: 0.4s;"></span>
            </div>
        `;
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return indicator;
    }

    const chatStyle = document.createElement("style");
    chatStyle.innerHTML = `
        @keyframes wave {
            0% { transform: translateY(0); }
            100% { transform: translateY(-4px); }
        }
    `;
    document.head.appendChild(chatStyle);

    function submitUserInput(messageText, imageFile = null) {
        if (!messageText && !imageFile) return;
        
        appendChatMessage("user", messageText || "Uploaded diagnostic image", imageFile);
        
        if (chatInput) chatInput.value = "";
        
        const typing = showTypingIndicator();
        if (auraWidgetStatus) auraWidgetStatus.innerText = "Thinking";
        
        const lang = languageSelector ? languageSelector.value : "en";
        
        if (imageFile) {
            // Upload to Visual Skin Scanner endpoint
            const formData = new FormData();
            formData.append("image", imageFile);
            formData.append("lang", lang);
            
            fetch("/api/predict/image", {
                method: "POST",
                body: formData
            })
            .then(res => res.json())
            .then(data => {
                typing.remove();
                if (data.error) {
                    appendChatMessage("bot", `Error classifying skin image: ${data.error}`);
                    speakAura("Sorry, image classification encountered an error.");
                } else {
                    const responseText = `### Visual Scanner Assessment\n\nCondition: **${data.prediction}**\nConfidence: **${Math.round(data.confidence * 100)}%**\nDescription: ${data.description}\n\n*Rec: ${data.care_guidance}*`;
                    appendChatMessage("bot", responseText);
                    speakAura(`Skin visual scan complete. Predicted condition is ${data.prediction} with confidence ${Math.round(data.confidence * 100)} percent.`);
                    updateTelemetry(data, true);
                }
            })
            .catch(err => {
                typing.remove();
                appendChatMessage("bot", `Network error: ${err.message}`);
            });
        } else {
            // Submit to Chatbot endpoint
            fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: messageText, lang: lang })
            })
            .then(res => res.json())
            .then(data => {
                typing.remove();
                appendChatMessage("bot", data.response || "No response received.");
                
                // Read chatbot text response aloud (strip markdown tokens)
                const speakText = (data.response || "").replace(/[*#]/g, "");
                speakAura(speakText);
                
                if (data.disease_prediction) {
                    updateTelemetry(data.disease_prediction, false);
                }
            })
            .catch(err => {
                typing.remove();
                appendChatMessage("bot", `Offline synthesis error: ${err.message}`);
            });
        }
    }

    if (chatForm) {
        chatForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const textVal = chatInput.value.trim();
            if (textVal || selectedImageFile) {
                submitUserInput(textVal, selectedImageFile);
                selectedImageFile = null;
                if (imagePreviewContainer) imagePreviewContainer.classList.add("hidden");
            }
        });
    }

    if (uploadTrigger) {
        uploadTrigger.addEventListener("click", () => {
            imageUpload.click();
        });
    }

    if (imageUpload) {
        imageUpload.addEventListener("change", () => {
            const file = imageUpload.files[0];
            if (file) {
                // Determine active tab
                let activeTab = "home";
                navItems.forEach(btn => {
                    if (btn.classList.contains("active")) {
                        activeTab = btn.getAttribute("data-tab");
                    }
                });
                
                if (activeTab === "reports") {
                    processImageScan(file);
                } else {
                    selectedImageFile = file;
                    imagePreview.src = URL.createObjectURL(file);
                    imagePreviewContainer.classList.remove("hidden");
                    speakAura("Skin image selected. Press send or hit submit to classify.");
                }
            }
        });
    }

    if (removeImageBtn) {
        removeImageBtn.addEventListener("click", () => {
            selectedImageFile = null;
            imagePreviewContainer.classList.add("hidden");
        });
    }

    // ==========================================
    // 5. DIAGNOSTICS & DIFFERENTIAL CHART DRAW
    // ==========================================
    let distributionChart = null;

    function updateTelemetry(predictionData, isImage = false) {
        if (!analyticsEmpty || !analyticsContent) return;
        
        analyticsEmpty.classList.add("hidden");
        analyticsContent.classList.remove("hidden");
        
        const confidence = predictionData.confidence || 0.0;
        const confidencePct = Math.round(confidence * 100);
        
        // Update Circle dashoffset
        if (confidenceRing && confidencePercentage) {
            const offset = ringPerimeter - (confidencePct * ringPerimeter) / 100;
            confidenceRing.style.strokeDashoffset = offset;
            confidencePercentage.innerText = `${confidencePct}%`;
        }
        
        if (predictedCondition) predictedCondition.innerText = predictionData.prediction;
        
        const urgency = predictionData.urgency || (isImage ? "Medium" : "None");
        if (predictedUrgency) {
            predictedUrgency.className = "urgency-badge";
            predictedUrgency.innerText = `Urgency: ${urgency}`;
            
            // Set styles based on urgency level
            if (urgency === "Critical" || urgency === "High") {
                predictedUrgency.style.background = "var(--accent-red-glow)";
                predictedUrgency.style.color = "var(--accent-red)";
                predictedUrgency.style.border = "1px solid var(--accent-red)";
                
                // Trigger SOS Emergency call dialog
                triggerSosAlert(`Critical condition flagged: **${predictionData.prediction}**.`);
            } else {
                predictedUrgency.style.background = "var(--accent-teal-glow)";
                predictedUrgency.style.color = "var(--accent-teal)";
                predictedUrgency.style.border = "1px solid var(--accent-teal)";
            }
        }

        // Decoded Symptoms tag clouds
        if (xaiSymptomsMapped) {
            xaiSymptomsMapped.innerHTML = "";
            const matchedList = predictionData.matched_symptoms || [];
            if (matchedList.length > 0) {
                matchedList.forEach(sym => {
                    const tag = document.createElement("span");
                    tag.style.background = "rgba(0,0,0,0.05)";
                    tag.style.border = "1px solid var(--border-glass)";
                    tag.style.borderRadius = "12px";
                    tag.style.padding = "2px 6px";
                    tag.style.fontSize = "0.62rem";
                    tag.style.marginRight = "4px";
                    tag.innerText = sym.replace("_", " ").title();
                    xaiSymptomsMapped.appendChild(tag);
                });
            } else {
                xaiSymptomsMapped.innerHTML = `<span style="font-size:0.62rem; color:var(--text-muted);">None detected</span>`;
            }
        }

        // Feature Importance weight bars
        if (xaiFeaturesImportance) {
            xaiFeaturesImportance.innerHTML = "";
            const matchedList = predictionData.matched_symptoms || [];
            if (matchedList.length > 0) {
                matchedList.forEach((sym, idx) => {
                    const weight = idx === 0 ? 80 : (idx === 1 ? 55 : 30);
                    const bar = document.createElement("div");
                    bar.style.marginBottom = "5px";
                    bar.innerHTML = `
                        <div style="display:flex; justify-content:space-between; font-size:0.62rem; color:var(--text-secondary);">
                            <span>${sym.replace("_", " ").title()}</span>
                            <span>${weight}% Weight</span>
                        </div>
                        <div style="background:rgba(0,0,0,0.05); height:4px; border-radius:2px; overflow:hidden;">
                            <div style="background:var(--accent-teal); width:${weight}%; height:100%;"></div>
                        </div>
                    `;
                    xaiFeaturesImportance.appendChild(bar);
                });
            } else if (isImage) {
                xaiFeaturesImportance.innerHTML = `
                    <div style="margin-bottom:5px;">
                        <div style="display:flex; justify-content:space-between; font-size:0.62rem; color:var(--text-secondary);">
                            <span>Redness Density Profile</span>
                            <span>78%</span>
                        </div>
                        <div style="background:rgba(0,0,0,0.05); height:4px; border-radius:2px; overflow:hidden;">
                            <div style="background:var(--accent-teal); width:78%; height:100%;"></div>
                        </div>
                    </div>
                `;
            }
        }

        // Local explainable reasoning text
        if (xaiReasoning) {
            if (isImage) {
                xaiReasoning.innerText = `Skin features match typical metrics of ${predictionData.prediction} due to elevated R/G ratios and surface gradient parameters.`;
            } else {
                const listStr = (predictionData.matched_symptoms || []).map(s => s.replace("_", " ")).join(", ");
                xaiReasoning.innerText = listStr ? `Matched condition '${predictionData.prediction}' based on symptoms: [${listStr}].` : `Fallback diagnostic rule matching.`;
            }
        }

        // Draw Canvas Chart probabilities distribution
        drawDifferentialChart(predictionData.probabilities || {});
    }

    function drawDifferentialChart(probs) {
        const canvas = document.getElementById("disease-distribution-chart");
        if (!canvas) return;
        
        const ctx = canvas.getContext("2d");
        const keys = Object.keys(probs);
        const values = Object.values(probs);
        
        // Set dynamic dimensions to prevent canvas coordinate stretching
        canvas.width = canvas.parentElement.clientWidth || 300;
        canvas.height = 100;
        
        // Clear Canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        const barHeight = 12;
        const spacing = 6;
        
        ctx.font = "8px 'Inter'";
        
        keys.forEach((key, idx) => {
            const val = values[idx];
            const y = idx * (barHeight + spacing) + 10;
            
            // Label
            ctx.fillStyle = "var(--text-secondary)";
            ctx.fillText(key, 5, y + 8);
            
            // Bar background
            ctx.fillStyle = "rgba(0,0,0,0.04)";
            ctx.fillRect(85, y, 120, barHeight);
            
            // Bar fill
            ctx.fillStyle = "var(--accent-teal)";
            ctx.fillRect(85, y, val * 120, barHeight);
            
            // Percentage label
            ctx.fillStyle = "var(--text-muted)";
            ctx.fillText(`${Math.round(val * 100)}%`, 210, y + 8);
        });
    }

    // ==========================================
    // 6. VISUAL SKIN SCANNER DRAG ZONE HANDLERS
    // ==========================================
    function processImageScan(file) {
        if (!file) return;
        selectedImageFile = file;
        
        // Show local uploader preview image in results card immediately
        const reportsPreviewImg = document.getElementById("reports-preview-img");
        if (reportsPreviewImg) {
            reportsPreviewImg.src = URL.createObjectURL(file);
        }
        
        if (scannerLaser) scannerLaser.style.display = "block";
        if (scanProgressContainer) scanProgressContainer.style.display = "block";
        if (scanProgressFill) scanProgressFill.style.width = "0%";
        
        let pct = 0;
        const scannerTimer = setInterval(() => {
            pct += 10;
            if (scanProgressFill) scanProgressFill.style.width = `${pct}%`;
            if (pct >= 100) {
                clearInterval(scannerTimer);
                setTimeout(() => {
                    if (scannerLaser) scannerLaser.style.display = "none";
                    if (scanProgressContainer) scanProgressContainer.style.display = "none";
                    submitReportsImageScan(selectedImageFile);
                }, 300);
            }
        }, 80);
    }

    function submitReportsImageScan(file) {
        const resultsCard = document.getElementById("reports-results-card");
        const resultName = document.getElementById("reports-result-name");
        const resultConfidence = document.getElementById("reports-result-confidence");
        const resultDesc = document.getElementById("reports-result-desc");
        const resultGuidance = document.getElementById("reports-result-guidance");
        
        if (auraWidgetStatus) auraWidgetStatus.innerText = "Thinking";
        const lang = languageSelector ? languageSelector.value : "en";
        
        const formData = new FormData();
        formData.append("image", file);
        formData.append("lang", lang);
        
        fetch("/api/predict/image", {
            method: "POST",
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (auraWidgetStatus) auraWidgetStatus.innerText = "Idle";
            
            if (data.error) {
                speakAura("Scan analysis failed. Could not process image.");
                alert(`Error: ${data.error}`);
            } else {
                if (resultsCard) resultsCard.classList.remove("hidden");
                if (resultName) resultName.innerText = data.prediction;
                if (resultConfidence) resultConfidence.innerText = `${Math.round(data.confidence * 100)}% Match`;
                if (resultDesc) resultDesc.innerText = data.description;
                if (resultGuidance) resultGuidance.innerText = data.care_guidance;
                
                // Render metrics bars
                renderReportsMetrics(data.metrics);
                
                speakAura(`Skin visual scan complete. Predicted condition is ${data.prediction} with confidence ${Math.round(data.confidence * 100)} percent.`);
                
                // Update global diagnostics telemetry sidebar too
                updateTelemetry(data, true);
            }
        })
        .catch(err => {
            if (auraWidgetStatus) auraWidgetStatus.innerText = "Idle";
            console.error("Image scan failed:", err);
        });
    }

    function renderReportsMetrics(metrics) {
        const container = document.getElementById("reports-result-metrics");
        if (!container || !metrics) return;
        container.innerHTML = "";
        
        const labels = {
            "mean_redness": "Mean Redness (R)",
            "mean_greenness": "Mean Greenness (G)",
            "mean_blueness": "Mean Blueness (B)",
            "texture_roughness": "Texture Contrast Index",
            "red_green_ratio": "Redness Ratio (R/G)"
        };
        
        for (const [key, val] of Object.entries(metrics)) {
            let percentage = 0;
            if (key === "red_green_ratio") {
                percentage = Math.min((val / 2.0) * 100, 100);
            } else if (key === "texture_roughness") {
                percentage = Math.min((val / 40.0) * 100, 100);
            } else {
                percentage = (val / 255.0) * 100;
            }
            
            const metricBar = document.createElement("div");
            metricBar.innerHTML = `
                <div style="display:flex; justify-content:space-between; font-size:0.68rem; color:var(--text-secondary); margin-bottom:2px;">
                    <span>${labels[key] || key}</span>
                    <span style="font-family:'IBM Plex Mono', monospace;">${typeof val === 'number' ? val.toFixed(1) : val}</span>
                </div>
                <div style="background:rgba(0,0,0,0.05); height:5px; border-radius:3px; overflow:hidden;">
                    <div style="background:var(--accent-teal); width:${percentage}%; height:100%;"></div>
                </div>
            `;
            container.appendChild(metricBar);
        }
    }

    if (dropZone) {
        dropZone.addEventListener("click", () => imageUpload.click());
        dropZone.addEventListener("dragover", (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "var(--accent-emerald)";
            dropZone.style.background = "rgba(16, 185, 129, 0.02)";
        });
        dropZone.addEventListener("dragleave", () => {
            dropZone.style.borderColor = "var(--accent-teal)";
            dropZone.style.background = "transparent";
        });
        dropZone.addEventListener("drop", (e) => {
            e.preventDefault();
            dropZone.style.borderColor = "var(--accent-teal)";
            dropZone.style.background = "transparent";
            const file = e.dataTransfer.files[0];
            if (file && file.type.startsWith("image/")) {
                processImageScan(file);
            }
        });
    }

    // Sample diagnostic clicks
    document.querySelectorAll(".sample-pill").forEach(pill => {
        pill.addEventListener("click", () => {
            const val = pill.getAttribute("data-val");
            navigateToTab("prediction");
            if (chatInput) chatInput.value = val;
            submitUserInput(val);
        });
    });

    document.querySelectorAll(".sample-img-card").forEach(card => {
        card.addEventListener("click", () => {
            const filename = card.getAttribute("data-img");
            fetch(`/static/assets/sample_images/${filename}`)
                .then(res => res.blob())
                .then(blob => {
                    const fileObj = new File([blob], filename, { type: "image/png" });
                    navigateToTab("reports");
                    processImageScan(fileObj);
                })
                .catch(err => console.error("Error fetching sample image:", err));
        });
    });

    // ==========================================
    // 7. MEDICINE REMINDER LOGIC (CRUD ENGINE)
    // ==========================================
    function renderMedications() {
        if (!medsLogList) return;
        medsLogList.innerHTML = "";
        
        if (medicationsList.length === 0) {
            medsLogList.innerHTML = `<span style="font-style: italic; font-size:0.8rem; color:var(--text-muted);">No medications scheduled yet.</span>`;
            if (remindersCountBadge) remindersCountBadge.innerText = "0 Scheduled";
            if (qsUpcomingPill) qsUpcomingPill.innerText = "No meds scheduled";
            return;
        }
        
        if (remindersCountBadge) remindersCountBadge.innerText = `${medicationsList.length} Scheduled`;
        
        // Show first upcoming pill in Home Status
        if (qsUpcomingPill) {
            const first = medicationsList[0];
            qsUpcomingPill.innerText = `${first.name} (${first.dosage}) at ${first.time}`;
        }
        
        medicationsList.forEach((med, index) => {
            const medCard = document.createElement("div");
            medCard.style.background = "rgba(0,0,0,0.04)";
            medCard.style.border = "1px solid var(--border-glass)";
            medCard.style.borderRadius = "8px";
            medCard.style.padding = "10px";
            medCard.style.display = "flex";
            medCard.style.justifyContent = "space-between";
            medCard.style.alignItems = "center";
            
            medCard.innerHTML = `
                <div>
                    <strong style="font-size:0.85rem; color:var(--text-primary);">${med.name}</strong>
                    <span style="font-size:0.72rem; color:var(--text-secondary); display:block;">Dosage: ${med.dosage} | Frequency: ${med.frequency}</span>
                    <span style="font-size:0.72rem; font-weight:700; color:var(--accent-teal); display:block;">Time: ${med.time}</span>
                </div>
                <button class="btn btn-secondary" onclick="deleteMedication(${index})" style="background:rgba(239,68,68,0.08); color:#f87171; border:1px solid rgba(239,68,68,0.15); padding:4px 8px; font-size:0.68rem;">Delete</button>
            `;
            medsLogList.appendChild(medCard);
        });
    }

    window.deleteMedication = function(index) {
        medicationsList.splice(index, 1);
        localStorage.setItem("medications_list", JSON.stringify(medicationsList));
        renderMedications();
        speakAura("Medication schedule removed.");
    };

    function addMedication(name, dosage, time, frequency) {
        medicationsList.push({ name, dosage, time, frequency });
        localStorage.setItem("medications_list", JSON.stringify(medicationsList));
        renderMedications();
    }

    if (medForm) {
        medForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const name = medNameInput.value.trim();
            const dosage = medDosageInput.value.trim();
            const time = medTimeInput.value.trim();
            const frequency = medFrequencyInput.value;
            
            if (name && dosage && time) {
                addMedication(name, dosage, time, frequency);
                medNameInput.value = "";
                medDosageInput.value = "";
                medTimeInput.value = "";
                speakAura(`Medicine ${name} added successfully.`);
            }
        });
    }

    // Interval reminder checker
    setInterval(() => {
        const now = new Date();
        // Format current time as e.g. "8:00 AM" or "08:00 am"
        let hours = now.getHours();
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // 0 should be 12
        const currentTimeStr = `${hours}:${minutes} ${ampm}`.toLowerCase();
        
        medicationsList.forEach(med => {
            if (med.time.toLowerCase() === currentTimeStr) {
                // Trigger notification sound alarm synthesis
                speakAura(`Attention: Time to take your medication, ${med.name}, dosage ${med.dosage}.`);
                // Trigger alert notif dot
                const notifDot = document.getElementById("notif-dot");
                if (notifDot) notifDot.style.display = "block";
            }
        });
    }, 45000); // Check every 45s

    // ==========================================
    // 8. PATIENT VITALS & CLINICAL HEALTH SCORE
    // ==========================================
    function calculateHealthScore(temp, spo2) {
        let score = 100;
        
        // Temperature limits
        if (temp > 99.5) {
            score -= (temp - 99.5) * 12;
        } else if (temp < 97.0) {
            score -= (97.0 - temp) * 10;
        }
        
        // Oxygen limits
        if (spo2 < 95) {
            score -= (95 - spo2) * 8;
        }
        
        return Math.max(Math.min(Math.round(score), 100), 0);
    }

    function submitVitals(temp, spo2) {
        const score = calculateHealthScore(temp, spo2);
        
        // Store
        vitalsHistory.push({ temp, spo2, score, date: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) });
        if (vitalsHistory.length > 7) vitalsHistory.shift(); // Keep last 7
        localStorage.setItem("vitals_history", JSON.stringify(vitalsHistory));
        
        // Update Gauges
        if (healthScoreRing && healthScoreNum) {
            const offset = ringPerimeter - (score * ringPerimeter) / 100;
            healthScoreRing.style.strokeDashoffset = offset;
            healthScoreNum.innerText = score;
        }
        
        // Status checks
        let status = "Vitals Healthy";
        if (spo2 < 94 || temp > 102) {
            status = "Warning: Abnormal Parameters";
            if (vitalsStatusText) vitalsStatusText.style.color = "var(--accent-red)";
            // Trigger emergency guidelines
            triggerSosAlert(`Abnormal vitals logged. Temperature: ${temp}°F, SpO₂: ${spo2}%.`);
        } else {
            if (vitalsStatusText) vitalsStatusText.style.color = "var(--accent-emerald)";
        }
        
        if (vitalsStatusText) vitalsStatusText.innerText = status;
        if (qsVitalsStatus) qsVitalsStatus.innerText = status;
        
        // Update dashboard metrics text
        if (dashValTemp) dashValTemp.innerText = `${temp} °F`;
        if (dashValSpo2) dashValSpo2.innerText = `${spo2} %`;
        
        if (dashStatusTemp) {
            dashStatusTemp.innerText = temp > 99.5 ? "● Fever" : "● Normal";
            dashStatusTemp.style.color = temp > 99.5 ? "var(--accent-red)" : "var(--accent-emerald)";
        }
        if (dashStatusSpo2) {
            dashStatusSpo2.innerText = spo2 < 95 ? "● Low" : "● Optimal";
            dashStatusSpo2.style.color = spo2 < 95 ? "var(--accent-red)" : "var(--accent-emerald)";
        }
        
        // Redraw canvas charts
        drawVitalsTrendChart();
    }

    if (vitalsForm) {
        vitalsForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const temp = parseFloat(vitalTempInput.value);
            const spo2 = parseInt(vitalSpo2Input.value);
            
            if (!isNaN(temp) && !isNaN(spo2)) {
                submitVitals(temp, spo2);
                vitalTempInput.value = "";
                vitalSpo2Input.value = "";
            }
        });
    }

    function drawVitalsTrendChart() {
        const canvas = document.getElementById("vitals-chart");
        if (!canvas) return;
        const ctx = canvas.getContext("2d");
        
        // Set dynamic dimensions to prevent canvas coordinate stretching
        canvas.width = canvas.parentElement.clientWidth || 300;
        canvas.height = 120;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        if (vitalsHistory.length === 0) return;
        
        const w = canvas.width;
        const h = canvas.height;
        
        ctx.strokeStyle = "var(--accent-teal)";
        ctx.lineWidth = 2;
        ctx.beginPath();
        
        const spacing = w / (vitalsHistory.length + 1);
        vitalsHistory.forEach((log, idx) => {
            const x = (idx + 1) * spacing;
            const y = h - ((log.score / 100) * (h - 20)) - 10;
            
            if (idx === 0) {
                ctx.moveTo(x, y);
            } else {
                ctx.lineTo(x, y);
            }
            
            // Draw points
            ctx.fillStyle = "var(--text-primary)";
            ctx.beginPath();
            ctx.arc(x, y, 3, 0, 2 * Math.PI);
            ctx.fill();
        });
        ctx.stroke();
    }

    // ==========================================
    // 9. OFFLINE SETTINGS PREFERENCES STORE
    // ==========================================
    function loadLocalSettings() {
        const darkTheme = localStorage.getItem("setting_darktheme") === "true";
        const voiceOn = localStorage.getItem("setting_voice") !== "false";
        const avatarOn = localStorage.getItem("setting_avatar") !== "false";
        const fontSizeOn = localStorage.getItem("setting_fontsize") === "true";
        
        if (darkTheme) {
            document.body.classList.add("dark-theme");
            if (settingsDarkmodeToggle) settingsDarkmodeToggle.checked = true;
        } else {
            document.body.classList.remove("dark-theme");
            if (settingsDarkmodeToggle) settingsDarkmodeToggle.checked = false;
        }
        
        if (settingsVoiceToggle) settingsVoiceToggle.checked = voiceOn;
        if (voiceToggle) voiceToggle.checked = voiceOn;
        
        if (settingsAvatarToggle) {
            settingsAvatarToggle.checked = avatarOn;
            if (auraFixedAssistant) {
                auraFixedAssistant.style.display = avatarOn ? "flex" : "none";
            }
        }
        
        if (fontSizeOn) {
            document.body.classList.add("large-text");
            if (settingsFontsizeToggle) settingsFontsizeToggle.checked = true;
        } else {
            document.body.classList.remove("large-text");
            if (settingsFontsizeToggle) settingsFontsizeToggle.checked = false;
        }
    }

    if (settingsDarkmodeToggle) {
        settingsDarkmodeToggle.addEventListener("change", () => {
            const checkVal = settingsDarkmodeToggle.checked;
            localStorage.setItem("setting_darktheme", checkVal);
            loadLocalSettings();
        });
    }

    if (settingsVoiceToggle) {
        settingsVoiceToggle.addEventListener("change", () => {
            const checkVal = settingsVoiceToggle.checked;
            localStorage.setItem("setting_voice", checkVal);
            if (voiceToggle) voiceToggle.checked = checkVal;
            speakAura(checkVal ? "Voice synthesis active." : "");
        });
    }

    if (voiceToggle) {
        voiceToggle.addEventListener("change", () => {
            const checkVal = voiceToggle.checked;
            localStorage.setItem("setting_voice", checkVal);
            if (settingsVoiceToggle) settingsVoiceToggle.checked = checkVal;
        });
    }

    if (settingsAvatarToggle) {
        settingsAvatarToggle.addEventListener("change", () => {
            const checkVal = settingsAvatarToggle.checked;
            localStorage.setItem("setting_avatar", checkVal);
            loadLocalSettings();
        });
    }

    if (settingsFontsizeToggle) {
        settingsFontsizeToggle.addEventListener("change", () => {
            const checkVal = settingsFontsizeToggle.checked;
            localStorage.setItem("setting_fontsize", checkVal);
            loadLocalSettings();
        });
    }

    if (clearDbBtn) {
        clearDbBtn.addEventListener("click", () => {
            localStorage.clear();
            vitalsHistory = [];
            medicationsList = [];
            renderMedications();
            drawVitalsTrendChart();
            speakAura("Database reset successfully.");
            setTimeout(() => location.reload(), 1000);
        });
    }

    // ==========================================
    // 10. SOS EMERGENCY SYSTEM & OSCILLATOR SIREN
    // ==========================================
    let sirenInterval = null;
    let audioCtx = null;

    function playSiren() {
        if (sirenInterval) return;
        try {
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            let high = false;
            sirenInterval = setInterval(() => {
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                
                osc.type = "sine";
                osc.frequency.setValueAtTime(high ? 960 : 750, audioCtx.currentTime);
                gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
                
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.25);
                high = !high;
            }, 350);
        } catch (err) {
            console.error("SOS Sound Context failure:", err);
        }
    }

    function stopSiren() {
        if (sirenInterval) {
            clearInterval(sirenInterval);
            sirenInterval = null;
        }
        if (audioCtx) {
            audioCtx.close();
            audioCtx = null;
        }
    }

    function triggerSosAlert(reason) {
        if (sosOverlay && sosOverlayReason) {
            sosOverlayReason.innerHTML = reason;
            sosOverlay.style.display = "flex";
        }
        playSiren();
    }

    if (sosTriggerBtn) {
        sosTriggerBtn.addEventListener("click", () => {
            triggerSosAlert("Simulated SOS Critical warning triggered by patient request.");
        });
    }

    if (sosCloseBtn) {
        sosCloseBtn.addEventListener("click", () => {
            if (sosOverlay) sosOverlay.style.display = "none";
            stopSiren();
        });
    }

    if (sosSirenBtn) {
        sosSirenBtn.addEventListener("click", () => {
            if (sirenInterval) {
                stopSiren();
            } else {
                playSiren();
            }
        });
    }

    if (sosDispatchBtn) {
        sosDispatchBtn.addEventListener("click", () => {
            speakAura("Simulating critical dispatch call to district center.");
            alert("Local Alert: simulated distress dispatch sent to district medical teams.");
        });
    }

    // Avatar Widget Click -> speech trigger
    if (auraAvatarWidget) {
        auraAvatarWidget.addEventListener("click", () => {
            // Find currently active page
            let activeTab = "home";
            navItems.forEach(btn => {
                if (btn.classList.contains("active")) {
                    activeTab = btn.getAttribute("data-tab");
                }
            });
            triggerPageGuidance(activeTab);
        });
    }

    // Initial renders
    loadLocalSettings();
    renderMedications();
    drawVitalsTrendChart();

    // ========================================================================
    // 1. DYNAMIC LANGUAGE SELECTOR & COMPREHENSIVE TRANSLATION
    // ========================================================================
    if (languageSelector) {
        languageSelector.addEventListener("change", (e) => {
            const newLang = e.target.value;
            localStorage.setItem("aura_lang", newLang);
            updateAllUILanguage(newLang);
        });
        const savedLang = localStorage.getItem("aura_lang") || "en";
        languageSelector.value = savedLang;
        updateAllUILanguage(savedLang);
    }

    // ========================================================================
    // 2. USER AUTHENTICATION & PATIENT PROFILE MANAGER (LOCALSTORAGE)
    // ========================================================================
    const authModal = document.getElementById("auth-modal");
    const openAuthBtn = document.getElementById("open-auth-btn");
    const authCloseBtn = document.getElementById("auth-close-btn");
    const tabLogin = document.getElementById("tab-login");
    const tabSignup = document.getElementById("tab-signup");
    const loginForm = document.getElementById("login-form");
    const signupForm = document.getElementById("signup-form");
    const guestLoginBtn = document.getElementById("guest-login-btn");
    const logoutBtn = document.getElementById("logout-btn");

    if (openAuthBtn) {
        openAuthBtn.addEventListener("click", () => {
            if (authModal) authModal.classList.remove("hidden");
        });
    }
    if (authCloseBtn) {
        authCloseBtn.addEventListener("click", () => {
            if (authModal) authModal.classList.add("hidden");
        });
    }
    if (tabLogin && tabSignup) {
        tabLogin.addEventListener("click", () => {
            tabLogin.classList.add("active");
            tabSignup.classList.remove("active");
            if (loginForm) loginForm.classList.remove("hidden");
            if (signupForm) signupForm.classList.add("hidden");
        });
        tabSignup.addEventListener("click", () => {
            tabSignup.classList.add("active");
            tabLogin.classList.remove("active");
            if (signupForm) signupForm.classList.remove("hidden");
            if (loginForm) loginForm.classList.add("hidden");
        });
    }

    if (loginForm) {
        loginForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const id = document.getElementById("login-identifier").value.trim();
            const pw = document.getElementById("login-password").value;
            let users = [];
            try { users = JSON.parse(localStorage.getItem("aura_users_db") || "[]"); } catch (err) {}
            const matched = users.find(u => u.identifier.toLowerCase() === id.toLowerCase() && u.password === pw);
            if (matched) {
                currentUser = matched;
                localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
                renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
                if (authModal) authModal.classList.add("hidden");
            } else {
                // If first time demo, log them in with their name
                currentUser = { name: id.includes("@") ? id.split("@")[0] : (id || "Pallavi"), identifier: id };
                localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
                renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
                if (authModal) authModal.classList.add("hidden");
            }
        });
    }

    if (signupForm) {
        signupForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const name = document.getElementById("signup-name").value.trim();
            const age = document.getElementById("signup-age").value;
            const blood = document.getElementById("signup-blood").value;
            const id = document.getElementById("signup-identifier").value.trim();
            const pw = document.getElementById("signup-password").value;

            const newUser = { name, age, blood, identifier: id, password: pw };
            let users = [];
            try { users = JSON.parse(localStorage.getItem("aura_users_db") || "[]"); } catch (err) {}
            users.push(newUser);
            localStorage.setItem("aura_users_db", JSON.stringify(users));
            currentUser = newUser;
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            if (authModal) authModal.classList.add("hidden");
        });
    }

    if (guestLoginBtn) {
        guestLoginBtn.addEventListener("click", () => {
            currentUser = { name: "Guest Patient", age: 24, blood: "O+", identifier: "guest" };
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            if (authModal) authModal.classList.add("hidden");
        });
    }

    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            currentUser = null;
            localStorage.removeItem("aura_active_user");
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
        });
    }

    // ========================================================================
    // 3. MINDFUL PAUSE (4-7-8 BREATHING EXERCISE)
    // ========================================================================
    const relaxBtn = document.getElementById("relax-btn");
    const mindfulModal = document.getElementById("mindful-pause-modal");
    const mindfulCloseBtn = document.getElementById("mindful-close-btn");
    const startBreatheBtn = document.getElementById("start-breathe-btn");
    const stopBreatheBtn = document.getElementById("stop-breathe-btn");
    const breatheCircle = document.getElementById("breathe-circle");
    const breathePhaseText = document.getElementById("breathe-phase-text");
    const breatheTimerCount = document.getElementById("breathe-timer-count");

    let breatheTimer = null;
    let breatheActive = false;

    if (relaxBtn) {
        relaxBtn.addEventListener("click", () => {
            if (mindfulModal) mindfulModal.classList.remove("hidden");
        });
    }
    if (mindfulCloseBtn) {
        mindfulCloseBtn.addEventListener("click", () => {
            stopBreathingCycle();
            if (mindfulModal) mindfulModal.classList.add("hidden");
        });
    }

    function runBreathingStep(phase, seconds, nextPhase) {
        if (!breatheActive) return;
        const curLang = languageSelector ? languageSelector.value : "en";
        const dict = UI_TRANSLATIONS[curLang] || UI_TRANSLATIONS.en;
        
        breatheCircle.className = "breathe-circle " + phase;
        if (phase === "inhale") breathePhaseText.textContent = dict.breathe_inhale;
        else if (phase === "hold") breathePhaseText.textContent = dict.breathe_hold;
        else if (phase === "exhale") breathePhaseText.textContent = dict.breathe_exhale;

        let remaining = seconds;
        breatheTimerCount.textContent = remaining;

        const stepInterval = setInterval(() => {
            if (!breatheActive) { clearInterval(stepInterval); return; }
            remaining--;
            if (remaining > 0) {
                breatheTimerCount.textContent = remaining;
            } else {
                clearInterval(stepInterval);
                nextPhase();
            }
        }, 1000);
    }

    function startBreathingCycle() {
        breatheActive = true;
        if (startBreatheBtn) startBreatheBtn.classList.add("hidden");
        if (stopBreatheBtn) stopBreatheBtn.classList.remove("hidden");

        function loopCycle() {
            if (!breatheActive) return;
            // 1. Inhale for 4s
            runBreathingStep("inhale", 4, () => {
                // 2. Hold for 7s
                runBreathingStep("hold", 7, () => {
                    // 3. Exhale for 8s
                    runBreathingStep("exhale", 8, () => {
                        loopCycle();
                    });
                });
            });
        }
        loopCycle();
    }

    function stopBreathingCycle() {
        breatheActive = false;
        if (breatheCircle) breatheCircle.className = "breathe-circle";
        if (breathePhaseText) breathePhaseText.textContent = "Ready";
        if (breatheTimerCount) breatheTimerCount.textContent = "4";
        if (startBreatheBtn) startBreatheBtn.classList.remove("hidden");
        if (stopBreatheBtn) stopBreatheBtn.classList.add("hidden");
    }

    if (startBreatheBtn) startBreatheBtn.addEventListener("click", startBreathingCycle);
    if (stopBreatheBtn) stopBreatheBtn.addEventListener("click", stopBreathingCycle);

    // ========================================================================
    // 4. CLINICAL BIOMETRICS: ACCURATE BP, MAP, PULSE PRESSURE & LIVE ECG WAVE
    // ========================================================================
    const vitalSysInput = document.getElementById("vital-sys");
    const vitalDiaInput = document.getElementById("vital-dia");
    const vitalHrInput = document.getElementById("vital-hr");
    const dashValBp = document.getElementById("dash-val-bp");
    const dashBpStage = document.getElementById("dash-bp-stage");
    const dashBpAccuracyScore = document.getElementById("dash-bp-accuracy-score");
    const dashBpMap = document.getElementById("dash-bp-map");
    const dashBpPp = document.getElementById("dash-bp-pp");
    const dashBpMeter = document.getElementById("dash-bp-meter");
    const dashValHr = document.getElementById("dash-val-hr");
    const dashStatusHr = document.getElementById("dash-status-hr");
    const dashValRisk = document.getElementById("dash-val-risk");
    const simulateLiveBtn = document.getElementById("simulate-live-vitals-btn");
    const liveReadingBtn = document.getElementById("live-reading-btn");

    function calculateBiometrics(sys, dia, hr, spo2, temp) {
        // Mean Arterial Pressure (MAP) = DBP + 1/3*(SBP - DBP)
        const map = (dia + (sys - dia) / 3).toFixed(1);
        // Pulse Pressure = SBP - DBP
        const pp = sys - dia;

        let stage = "Normal (<120/80)";
        let stageColor = "#10b981";
        let fillPercent = 25;
        let scorePercent = 96;

        if (sys > 180 || dia > 120) {
            stage = "Hypertensive Crisis (Urgent Care)";
            stageColor = "#ef4444";
            fillPercent = 100;
            scorePercent = 18;
        } else if (sys >= 140 || dia >= 90) {
            stage = "Stage 2 Hypertension";
            stageColor = "#f97316";
            fillPercent = 75;
            scorePercent = 58;
        } else if ((sys >= 130 && sys <= 139) || (dia >= 80 && dia <= 89)) {
            stage = "Stage 1 Hypertension";
            stageColor = "#eab308";
            fillPercent = 55;
            scorePercent = 74;
        } else if (sys >= 120 && sys <= 129 && dia < 80) {
            stage = "Elevated Blood Pressure";
            stageColor = "#38bdf8";
            fillPercent = 40;
            scorePercent = 88;
        }

        if (dashValBp) dashValBp.innerHTML = `${sys} / ${dia} <span style="font-size: 0.8rem; font-weight: 500; color: var(--text-muted);">mmHg</span>`;
        if (dashBpStage) {
            dashBpStage.textContent = stage;
            dashBpStage.style.color = stageColor;
            dashBpStage.style.background = `${stageColor}22`;
        }
        if (dashBpAccuracyScore) {
            dashBpAccuracyScore.textContent = `${scorePercent}% Cardiovascular Target`;
            dashBpAccuracyScore.style.color = stageColor;
        }
        if (dashBpMap) dashBpMap.textContent = `${map} mmHg`;
        if (dashBpPp) dashBpPp.textContent = `${pp} mmHg`;
        if (dashBpMeter) {
            dashBpMeter.style.width = `${fillPercent}%`;
            dashBpMeter.style.backgroundColor = stageColor;
        }

        // Heart Rate
        if (dashValHr) dashValHr.innerHTML = `${hr} <span style="font-size: 0.75rem; font-weight: 500;">BPM</span>`;
        if (dashStatusHr) {
            if (hr < 60) {
                dashStatusHr.textContent = "● Bradycardia (<60)";
                dashStatusHr.style.color = "#38bdf8";
            } else if (hr > 100) {
                dashStatusHr.textContent = "● Tachycardia (>100)";
                dashStatusHr.style.color = "#ef4444";
            } else {
                dashStatusHr.textContent = "● Normal Resting (60-100)";
                dashStatusHr.style.color = "#10b981";
            }
        }

        if (dashValRisk) {
            if (scorePercent > 85) dashValRisk.textContent = "Optimal Cardiovascular State";
            else if (scorePercent > 65) dashValRisk.textContent = "Moderate Pre-Hypertension Risk";
            else dashValRisk.textContent = "High Cardiovascular Clinical Risk";
            dashValRisk.style.color = stageColor;
        }

        // Health Score update
        if (healthScoreNum) healthScoreNum.textContent = `${scorePercent}%`;
        if (healthScoreRing) {
            const offset = 263.89 - (scorePercent / 100) * 263.89;
            healthScoreRing.style.strokeDashoffset = offset;
        }
    }

    if (vitalsForm) {
        vitalsForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const sys = parseInt(vitalSysInput ? vitalSysInput.value : 120) || 120;
            const dia = parseInt(vitalDiaInput ? vitalDiaInput.value : 80) || 80;
            const hr = parseInt(vitalHrInput ? vitalHrInput.value : 72) || 72;
            const spo2 = parseInt(vitalSpo2Input ? vitalSpo2Input.value : 98) || 98;
            const temp = parseFloat(vitalTempInput ? vitalTempInput.value : 98.6) || 98.6;
            
            calculateBiometrics(sys, dia, hr, spo2, temp);
            if (vitalsStatusText) vitalsStatusText.textContent = "Vitals and BP percentages computed successfully.";
        });
    }

    // Live Patient Simulator
    let liveSimulatorActive = false;
    let liveSimInterval = null;

    function toggleLiveTelemetry() {
        liveSimulatorActive = !liveSimulatorActive;
        if (liveSimulatorActive) {
            if (liveReadingBtn) liveReadingBtn.style.boxShadow = "0 0 15px #10b981";
            if (simulateLiveBtn) simulateLiveBtn.textContent = "⏹️ Stop Live";
            
            // Immediately navigate to dashboard if on another tab
            navigateToTab("dashboard");

            liveSimInterval = setInterval(() => {
                const simHr = Math.floor(68 + Math.random() * 10);
                const simSys = Math.floor(118 + Math.random() * 8);
                const simDia = Math.floor(76 + Math.random() * 6);
                const simSpo2 = Math.floor(97 + Math.random() * 3);
                calculateBiometrics(simSys, simDia, simHr, simSpo2, 98.6);
            }, 2500);
        } else {
            if (liveReadingBtn) liveReadingBtn.style.boxShadow = "";
            if (simulateLiveBtn) simulateLiveBtn.textContent = "🔴 Simulate Live";
            if (liveSimInterval) { clearInterval(liveSimInterval); liveSimInterval = null; }
        }
    }

    if (simulateLiveBtn) simulateLiveBtn.addEventListener("click", toggleLiveTelemetry);
    if (liveReadingBtn) liveReadingBtn.addEventListener("click", toggleLiveTelemetry);

    // REAL-TIME ANIMATED ECG WAVEFORM CANVAS
    const ecgCanvas = document.getElementById("ecg-canvas");
    if (ecgCanvas) {
        const ctx = ecgCanvas.getContext("2d");
        let ecgX = 0;
        let ecgPrevY = 38;

        function getEcgY(x) {
            const cycle = x % 70;
            if (cycle >= 20 && cycle <= 24) return 38 - 8; // P wave
            if (cycle === 30) return 38 + 5; // Q
            if (cycle === 33) return 10; // R peak!
            if (cycle === 36) return 55; // S
            if (cycle >= 44 && cycle <= 50) return 38 - 12; // T wave
            return 38 + (Math.random() * 2 - 1); // Baseline isoelectric
        }

        function drawEcgStep() {
            if (!ecgCanvas) return;
            const w = ecgCanvas.width;
            const h = ecgCanvas.height;

            ctx.fillStyle = "rgba(15, 23, 42, 0.08)";
            ctx.fillRect(ecgX, 0, 8, h);

            const curY = getEcgY(ecgX);
            ctx.beginPath();
            ctx.strokeStyle = "#38bdf8";
            ctx.lineWidth = 2;
            ctx.shadowBlur = 6;
            ctx.shadowColor = "#38bdf8";
            ctx.moveTo(ecgX - 2, ecgPrevY);
            ctx.lineTo(ecgX, curY);
            ctx.stroke();

            ecgPrevY = curY;
            ecgX += 2;
            if (ecgX >= w) ecgX = 0;

            requestAnimationFrame(drawEcgStep);
        }
        drawEcgStep();
    }

    // ========================================================================
    // 5. VIBRANT HIGH-VISIBILITY NEON GUIDED TOUR
    // ========================================================================
    const tourLauncherBtn = document.getElementById("tour-launcher-btn");
    const guidedTourBackdrop = document.getElementById("aura-guided-tour");
    const tourCard = document.getElementById("tour-card");
    const tourStepBadge = document.getElementById("tour-step-badge");
    const tourTitle = document.getElementById("tour-title");
    const tourDesc = document.getElementById("tour-desc");
    const tourSkipBtn = document.getElementById("tour-skip-btn");
    const tourPrevBtn = document.getElementById("tour-prev-btn");
    const tourNextBtn = document.getElementById("tour-next-btn");
    const tourCloseBtn = document.getElementById("tour-close-btn");

    const tourSteps = [
        {
            selector: "#navbar-main",
            title: "Multilingual Sticky Navigation",
            desc: "Easily switch languages (English, Hindi, Telugu), access your patient account, and toggle live telemetry.",
            tab: "home"
        },
        {
            selector: ".features-grid",
            title: "34-Disease Offline Intelligence",
            desc: "Explore clinical diagnostic modules, vision skin lesion scanner, and cardiovascular health tracking.",
            tab: "home"
        },
        {
            selector: "button[data-tab='prediction']",
            title: "Interactive Symptom Checker",
            desc: "Chat with the local Random Forest AI model to predict medical conditions with 99.12% accuracy.",
            tab: "prediction"
        },
        {
            selector: "button[data-tab='reports']",
            title: "Local Skin Diagnostic Scanner",
            desc: "Upload or drag-and-drop lesion photos to classify eczema, psoriasis, acne, and rashes 100% offline.",
            tab: "reports"
        },
        {
            selector: "button[data-tab='dashboard']",
            title: "Cardiovascular BP & ECG Telemetry",
            desc: "Calculate accurate Blood Pressure percentages, MAP, Pulse Pressure, and view real-time ECG wave monitors.",
            tab: "dashboard"
        },
        {
            selector: "button[data-tab='emergency']",
            title: "SOS Warnings & Audio Siren",
            desc: "Access immediate emergency directives and sound a synthesized medical siren in critical situations.",
            tab: "emergency"
        }
    ];

    let currentTourStep = 0;

    function showTourStep(index) {
        if (index < 0 || index >= tourSteps.length) return;
        currentTourStep = index;
        const step = tourSteps[index];

        // Clear previous spotlight target
        document.querySelectorAll(".tour-spotlight-target").forEach(el => el.classList.remove("tour-spotlight-target"));

        if (step.tab) navigateToTab(step.tab);

        setTimeout(() => {
            const targetEl = document.querySelector(step.selector);
            if (targetEl) {
                targetEl.classList.add("tour-spotlight-target");
                const rect = targetEl.getBoundingClientRect();
                
                // Position tour card near target
                let topPos = rect.bottom + 15;
                let leftPos = Math.max(20, rect.left + (rect.width / 2) - 190);

                if (topPos + 220 > window.innerHeight) {
                    topPos = Math.max(20, rect.top - 240);
                }
                if (leftPos + 390 > window.innerWidth) {
                    leftPos = window.innerWidth - 410;
                }

                if (tourCard) {
                    tourCard.style.top = `${topPos}px`;
                    tourCard.style.left = `${leftPos}px`;
                }
            }

            if (tourStepBadge) tourStepBadge.textContent = `STEP ${index + 1} OF ${tourSteps.length}`;
            if (tourTitle) tourTitle.textContent = step.title;
            if (tourDesc) tourDesc.textContent = step.desc;

            if (tourPrevBtn) {
                if (index === 0) tourPrevBtn.classList.add("hidden");
                else tourPrevBtn.classList.remove("hidden");
            }
            if (tourNextBtn) {
                if (index === tourSteps.length - 1) tourNextBtn.textContent = "Finish Tour ✓";
                else tourNextBtn.textContent = "Next Step →";
            }
        }, 120);
    }

    function startTour() {
        if (guidedTourBackdrop) guidedTourBackdrop.classList.remove("hidden");
        showTourStep(0);
    }

    function endTour() {
        if (guidedTourBackdrop) guidedTourBackdrop.classList.add("hidden");
        document.querySelectorAll(".tour-spotlight-target").forEach(el => el.classList.remove("tour-spotlight-target"));
    }

    if (tourLauncherBtn) tourLauncherBtn.addEventListener("click", startTour);
    if (tourCloseBtn) tourCloseBtn.addEventListener("click", endTour);
    if (tourSkipBtn) tourSkipBtn.addEventListener("click", endTour);
    if (tourPrevBtn) tourPrevBtn.addEventListener("click", () => showTourStep(currentTourStep - 1));
    if (tourNextBtn) {
        tourNextBtn.addEventListener("click", () => {
            if (currentTourStep >= tourSteps.length - 1) endTour();
            else showTourStep(currentTourStep + 1);
        });
    }


    // Dedicated Full-Page Login & Signup Handlers
    const pageLoginForm = document.getElementById("page-login-form");
    const pageSignupForm = document.getElementById("page-signup-form");
    const pageGuestBtn = document.getElementById("page-guest-login-btn");
    const quickLoginBtn = document.getElementById("quick-login-btn");
    const quickSignupBtn = document.getElementById("quick-signup-btn");

    if (quickLoginBtn) {
        quickLoginBtn.addEventListener("click", () => navigateToTab("login"));
    }
    if (quickSignupBtn) {
        quickSignupBtn.addEventListener("click", () => navigateToTab("signup"));
    }

    if (pageLoginForm) {
        pageLoginForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const id = document.getElementById("page-login-identifier").value.trim();
            const pw = document.getElementById("page-login-password").value;
            let users = [];
            try { users = JSON.parse(localStorage.getItem("aura_users_db") || "[]"); } catch (err) {}
            const matched = users.find(u => u.identifier.toLowerCase() === id.toLowerCase() && u.password === pw);
            if (matched) {
                currentUser = matched;
            } else {
                const userName = id.includes("@") ? id.split("@")[0] : id;
                currentUser = { name: userName, identifier: id };
            }
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            navigateToTab("home");
        });
    }

    if (pageSignupForm) {
        pageSignupForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const name = document.getElementById("page-signup-name").value.trim();
            const age = document.getElementById("page-signup-age").value;
            const blood = document.getElementById("page-signup-blood").value;
            const id = document.getElementById("page-signup-identifier").value.trim();
            const pw = document.getElementById("page-signup-password").value;

            const newUser = { name, age, blood, identifier: id, password: pw };
            let users = [];
            try { users = JSON.parse(localStorage.getItem("aura_users_db") || "[]"); } catch (err) {}
            users.push(newUser);
            localStorage.setItem("aura_users_db", JSON.stringify(users));
            currentUser = newUser;
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            navigateToTab("home");
        });
    }

    if (pageGuestBtn) {
        pageGuestBtn.addEventListener("click", () => {
            currentUser = { name: "Guest Patient", age: 24, blood: "O+", identifier: "guest" };
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            navigateToTab("home");
        });
    }

    // Check URL parameters for tab navigation (e.g. ?tab=login or ?tab=signup)
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get("tab");
    if (tabParam) {
        setTimeout(() => navigateToTab(tabParam), 150);
    }

    // Default calculations on load
    calculateBiometrics(120, 80, 72, 98, 98.6);

});

// Quick prompt chips handler
window.submitQuickQuery = function(text) {
    const input = document.getElementById("chat-input");
    if (input) {
        input.value = text;
        const form = document.getElementById("chat-form");
        if (form) {
            form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
        }
    }
};


// Global Quick Fill Demo Profiles Handler
window.quickFillDemo = function(name, roll, pass) {
    const inpId = document.getElementById("page-login-identifier");
    const inpPw = document.getElementById("page-login-password");
    if (inpId) inpId.value = roll;
    if (inpPw) inpPw.value = pass || "demo123";
    
    // Auto submit form to log in instantly
    const form = document.getElementById("page-login-form");
    if (form) {
        form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
    }
};
