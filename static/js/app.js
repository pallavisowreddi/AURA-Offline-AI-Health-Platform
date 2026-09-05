
// ============================================================================
// AURA CLIENT-SIDE UTILITIES & CRYPTOGRAPHY
// ============================================================================
function toTitleCase(str) {
    if (!str) return "";
    return String(str).replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());
}

// Local-only offline demo authentication (SHA-256 hashed localStorage). Not production-grade backend security; designed for offline hackathon demonstration.
function jsSha256(ascii) {
    function rightRotate(value, amount) {
        return (value >>> amount) | (value << (32 - amount));
    }
    const mathPow = Math.pow;
    const maxWord = mathPow(2, 32);
    let lengthProperty = 'length';
    let i, j;
    let result = '';
    const words = [];
    const asciiBitLength = ascii[lengthProperty] * 8;
    let hash = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
    const k = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ];
    let isCompound = false;
    for (i = 0; i < asciiBitLength; i += 8) {
        words[i >> 5] |= (ascii.charCodeAt(i / 8) & 0xff) << (24 - (i % 32));
    }
    words[asciiBitLength >> 5] |= 0x80 << (24 - (asciiBitLength % 32));
    words[(((asciiBitLength + 64) >> 9) << 4) + 15] = asciiBitLength;
    for (let j = 0; j < words[lengthProperty]; j += 16) {
        const w = words.slice(j, j + 16);
        const oldHash = hash.slice(0);
        hash = hash.slice(0, 8);
        for (i = 0; i < 64; i++) {
            const i2 = i + j;
            const w15 = w[i - 15], w2 = w[i - 2];
            const a = hash[0], e = hash[4];
            const temp1 = hash[7]
                + (rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25))
                + ((e & hash[5]) ^ ((~e) & hash[6]))
                + k[i]
                + (w[i] = (i < 16) ? w[i] : (
                    w[i - 16]
                    + (rightRotate(w15, 7) ^ rightRotate(w15, 18) ^ (w15 >>> 3))
                    + w[i - 7]
                    + (rightRotate(w2, 17) ^ rightRotate(w2, 19) ^ (w2 >>> 10))
                ) | 0);
            const temp2 = (rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22))
                + ((a & hash[1]) ^ (a & hash[2]) ^ (hash[1] & hash[2]));
            hash = [(temp1 + temp2) | 0, a, hash[1], hash[2], (hash[3] + temp1) | 0, hash[4], hash[5], hash[6]];
        }
        for (i = 0; i < 8; i++) {
            hash[i] = (hash[i] + oldHash[i]) | 0;
        }
    }
    for (i = 0; i < 8; i++) {
        for (let b = 3; b >= 0; b--) {
            const byte = (hash[i] >> (b * 8)) & 0xff;
            result += ((byte < 16 ? '0' : '') + byte.toString(16));
        }
    }
    return result;
}

async function hashPasswordSHA256(password) {
    if (!password) return "";
    try {
        if (window.crypto && window.crypto.subtle) {
            const msgBuffer = new TextEncoder().encode(password);
            const hashBuffer = await window.crypto.subtle.digest("SHA-256", msgBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, "0")).join("");
        }
    } catch (e) {
        console.warn("WebCrypto unavailable, falling back to local JS SHA-256", e);
    }
    return jsSha256(password);
}

function getActiveUser() {
    try {
        const stored = localStorage.getItem("aura_active_user");
        return stored ? JSON.parse(stored) : null;
    } catch (e) {
        return null;
    }
}

window.returnToHomeOrLanding = function() {
    if (getActiveUser()) {
        window.navigateToTab("home");
    } else {
        window.navigateToTab("landing");
    }
};


// ============================================================================
// AURA CLIENT-SIDE MULTILINGUAL TRANSLATION DICTIONARY
// ============================================================================
const UI_TRANSLATIONS = {
    en: {
        nav_brand: "AURA Platform",
        badge_offline: "Local Offline",
        nav_home: "Home",
        nav_prediction: "Disease Prediction",
        nav_vaccines: "Vaccination",
        vac_title: "Universal Immunization & Vaccine Schedules",
        vac_subtitle: "Official National Immunization Schedule (NIS) & WHO life-course vaccine guidelines.",
        vac_print_card: "Print Vaccine Card",
        rep_tab_visual: "Visual Skin Pathology Scanner",
        rep_tab_lab: "Digital Lab Report Biomarker Analyzer",
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
        tip_eyebrow: "DAILY REMINDER",
        tip_headline: "Health tip of the moment",
        tip_content_1: "Consult a healthcare professional if symptoms persist beyond a few days.",
        login_welcome: "Welcome back",
        signup_welcome: "Create your account",
        auth_remember_me: "Remember me",
        auth_forgot_pw: "Forgot Password?",
        auth_lbl_confirm_pw: "Confirm Password",
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
        hero_desc: "Fully offline, multilingual clinical intelligence and predictive diagnostics. Safeguard your family with reliable information.",
        hero_btn_check: "Start Symptom Check",
        hero_btn_dash: "View Dashboard",
        feat_symptoms_title: "Symptom Checker",
        feat_symptoms_desc: "Talk to our offline chatbot to check symptoms across a wide range of common conditions, chronic diseases, and epidemic symptoms.",
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
        tip_eyebrow: "दैनिक स्वास्थ्य अनुस्मारक",
        tip_headline: "आज की महत्वपूर्ण स्वास्थ्य सलाह",
        tip_content_1: "यदि लक्षण कुछ दिनों से अधिक समय तक बने रहें तो किसी स्वास्थ्य विशेषज्ञ से सलाह लें।",
        login_welcome: "स्वागत है (Welcome back)",
        signup_welcome: "नया खाता बनाएं",
        auth_remember_me: "मुझे याद रखें",
        auth_forgot_pw: "पासवर्ड भूल गए?",
        auth_lbl_confirm_pw: "पासवर्ड की पुष्टि करें",
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
        hero_desc: "पूरी तरह से ऑफ़लाइन, बहुभाषी चिकित्सकीय ज्ञान और भविष्य कहनेवाला निदान। अपने परिवार को सुरक्षित रखें।",
        hero_btn_check: "लक्षण जांच शुरू करें",
        hero_btn_dash: "डैशबोर्ड देखें",
        feat_symptoms_title: "लक्षण जांचकर्ता (Chat)",
        feat_symptoms_desc: "सामान्य और पुरानी बीमारियों के लक्षणों की जांच के लिए हमारे ऑफ़लाइन AI चैटबॉट से बात करें।",
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
        tip_eyebrow: "రోజువారీ ఆరోగ్య సూచన",
        tip_headline: "ఈ క్షణపు ఆరోగ్య చిట్కా",
        tip_content_1: "లక్షణాలు కొన్ని రోజులకు మించి కొనసాగితే వెంటనే వైద్య నిపుణుడిని సంప్రదించండి.",
        login_welcome: "స్వాగతం (Welcome back)",
        signup_welcome: "ఖాతా తెరవండి",
        auth_remember_me: "నన్ను గుర్తుంచుకో",
        auth_forgot_pw: "పాస్‌వర్డ్ మర్చిపోయారా?",
        auth_lbl_confirm_pw: "పాస్‌వర్డ్ నిర్ధారించండి",
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
        hero_desc: "పూర్తిగా ఆఫ్‌లైన్, బహుభాషా క్లినికల్ పరిజ్ఞానం మరియు ప్రిడిక్టివ్ డయాగ్నస్టిక్స్. మీ కుటుంబాన్ని సురక్షితంగా ఉంచండి.",
        hero_btn_check: "లక్షణాల పరీక్ష ప్రారంభించండి",
        hero_btn_dash: "డ్యాష్‌బోర్డ్ చూడండి",
        feat_symptoms_title: "లక్షణాల తనిఖీదారు",
        feat_symptoms_desc: "సాధారణ మరియు దీర్ఘకాలిక వ్యాధుల లక్షణాల తనిఖీ కోసం మా ఆఫ్‌లైన్ AI చాట్‌బాట్‌తో మాట్లాడండి.",
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
            const cleanName = (currentUser.name || "Guest").replace(/\s*\([A-Za-z0-9\+\-]+\)\s*$/, "").trim();
            if (lang === "hi") displayName.textContent = `नमस्ते, ${cleanName}`;
            else if (lang === "te") displayName.textContent = `నమస్తే, ${cleanName}`;
            else displayName.textContent = `Hello, ${cleanName}`;
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
        "vaccines": {
            "title": "Universal Immunization Hub",
            "body": "Explore comprehensive life-course immunization schedules from infant birth doses to senior booster vaccines. Mark doses as taken to track immunity.",
            "speech": "This is the Universal Immunization Hub. Browse official vaccine schedules across all age categories and track completed doses offline."
        },
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
    const PROTECTED_TABS = ["home", "prediction", "reports", "vaccines", "reminders", "dashboard", "emergency", "settings"];

    function updateAuthUIState() {
        const user = getActiveUser();
        const authBar = document.getElementById("auth-buttons-bar");
        const greetingPill = document.getElementById("user-greeting-pill");
        const displayName = document.getElementById("user-display-name");

        if (user) {
            if (authBar) authBar.classList.add("hidden");
            if (greetingPill) {
                greetingPill.classList.remove("hidden");
                const cleanName = (user.name || "Pallavi Sowreddi").replace(/\s*\([A-Za-z0-9\+\-]+\)\s*$/, "").trim();
                if (displayName) displayName.textContent = `Hello, ${cleanName}`;
            }
        } else {
            if (authBar) authBar.classList.remove("hidden");
            if (greetingPill) greetingPill.classList.add("hidden");
        }
    }

    window.navigateToTab = function(tabName) {
        const user = getActiveUser();
        // Route Guard: enforce authentication for clinical modules
        if (!user && PROTECTED_TABS.includes(tabName)) {
            console.warn(`[RouteGuard] Protected route '${tabName}' requires login. Redirecting to landing gate.`);
            tabName = "landing";
        }

        // Find button (both desktop and mobile)
        document.querySelectorAll(".nav-item, .mobile-nav-item").forEach(btn => {
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

        // Reset scroll position to top
        const wrapper = document.querySelector(".app-content-wrapper");
        if (wrapper) wrapper.scrollTop = 0;
        
        updateAuthUIState();
        triggerPageGuidance(tabName);
        if (tabName === "vaccines" && typeof renderVaccinesList === "function") {
            renderVaccinesList();
        }
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
                } else if (data.is_document) {
                    const docText = `### 📋 ${data.doc_type}\n\n**Patient:** ${data.patient_name || 'Patient (from report)'} (${data.patient_age ? data.patient_age + ' y/o' : 'Age not specified'}, ${data.patient_gender || 'Clinical Record'})\n**Doctor:** ${data.doctor || 'Attending Clinician'}\n\n**Key Clinical Assessment:**\n${data.care_guidance || data.advice}`;
                    appendChatMessage("bot", docText);
                    speakAura(`Medical report analyzed for ${data.patient_name || 'patient'}.`);
                    updateTelemetry(data, true);
                } else {
                    const responseText = `### Visual Scanner Assessment\n\nCondition: **${data.prediction}**\nConfidence: **${Math.round(data.confidence * 100)}%**\nDescription: ${data.description}\n\n*Rec: ${data.care_guidance || data.advice}*`;
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
                    tag.innerText = toTitleCase(sym);
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
                            <span>${toTitleCase(sym)}</span>
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
            } else if (data.is_document) {
                renderDocumentAnalysisCard(data);
            } else {
                if (resultsCard) resultsCard.classList.remove("hidden");
                document.getElementById("doc-scan-results-view")?.classList.add("hidden");
                document.getElementById("skin-scan-results-view")?.classList.remove("hidden");
                document.getElementById("doc-scan-results-view")?.classList.add("hidden");
                document.getElementById("skin-scan-results-view")?.classList.remove("hidden");
                if (resultName) resultName.innerText = data.prediction;
                if (resultConfidence) resultConfidence.innerText = `${Math.round(data.confidence * 100)}% Match`;
                if (resultDesc) resultDesc.innerText = data.description;
                if (resultGuidance) resultGuidance.innerText = data.care_guidance || data.advice || 'Consult a dermatologist for clinical examination.';
                
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
            const confirmed = confirm("Are you sure you want to reset the demo database? This will restore clean factory defaults, default accounts, and clear transient testing data.");
            if (!confirmed) return;

            localStorage.clear();

            // Re-seed default demo accounts
            const defaultUsers = [
                { name: "S. Pallavi", age: "21", blood: "O+", identifier: "2461783993", password_hash: DEMO_PW_HASH, registeredAt: new Date().toISOString() },
                { name: "Pallavi Sowreddi", age: "21", blood: "O+", identifier: "pallavi@aura.health", password_hash: DEMO_PW_HASH, registeredAt: new Date().toISOString() }
            ];
            localStorage.setItem("aura_users_db", JSON.stringify(defaultUsers));

            // Set clean demo patient
            const demoPatient = { name: "Pallavi Sowreddi", age: "21", blood: "O+", identifier: "pallavi@aura.health" };
            localStorage.setItem("aura_active_user", JSON.stringify(demoPatient));
            currentUser = demoPatient;

            // Reset state arrays
            vitalsHistory = [];
            medicationsList = [];
            renderMedications();
            drawVitalsTrendChart();

            updateAuthUIState();
            renderCurrentUserBadge("en");

            speakAura("Demo database restored to factory state.");
            alert("✅ Demo Database Reset: Clean factory state restored with default presentation accounts (pallavi@aura.health / 2461783993).");
            setTimeout(() => {
                navigateToTab("home");
                location.reload();
            }, 600);
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
            if (typeof updateAuthUIState === "function") updateAuthUIState();
            if (typeof renderCurrentUserBadge === "function") renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            if (typeof navigateToTab === "function") navigateToTab("landing");
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
            title: "Offline Clinical Intelligence",
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

    // Helper function to show notifications on auth forms
    function showAuthAlert(elemId, message, type = "error") {
        const alertEl = document.getElementById(elemId);
        if (!alertEl) return;
        alertEl.innerHTML = message;
        alertEl.style.display = "block";
        if (type === "error") {
            alertEl.style.background = "#fef2f2";
            alertEl.style.color = "#dc2626";
            alertEl.style.border = "1px solid #f87171";
        } else {
            alertEl.style.background = "#ecfdf5";
            alertEl.style.color = "#059669";
            alertEl.style.border = "1px solid #34d399";
        }
    }

    // Password strength evaluation
    function evaluatePasswordStrength(pw) {
        if (!pw || pw.length === 0) return { score: 0, text: "Empty", color: "#94a3b8", width: "0%" };
        let score = 0;
        if (pw.length >= 6) score += 1;
        if (pw.length >= 8) score += 1;
        if (/[A-Z]/.test(pw)) score += 1;
        if (/[0-9]/.test(pw)) score += 1;
        if (/[^A-Za-z0-9]/.test(pw)) score += 1;

        if (score <= 2) {
            return { score, text: "Weak", color: "#ef4444", width: "25%" };
        } else if (score === 3 || score === 4) {
            return { score, text: "Medium / Moderate", color: "#f59e0b", width: "65%" };
        } else {
            return { score, text: "Strong & Secure ✓", color: "#10b981", width: "100%" };
        }
    }

    function updatePasswordStrengthMeter(val) {
        const res = evaluatePasswordStrength(val);
        const bar = document.getElementById("pw-strength-bar");
        const label = document.getElementById("pw-strength-label");
        if (bar) {
            bar.style.width = res.width;
            bar.style.background = res.color;
        }
        if (label) {
            label.textContent = res.text;
            label.style.color = res.color;
        }
    }

    const signupPwInput = document.getElementById("page-signup-password");
    if (signupPwInput) {
        signupPwInput.addEventListener("input", (e) => {
            updatePasswordStrengthMeter(e.target.value);
        });
    }

    // Suggest strong password button
    const suggestPwBtn = document.getElementById("btn-suggest-pw");
    if (suggestPwBtn) {
        suggestPwBtn.addEventListener("click", () => {
            const uppers = "ABCDEFGHJKLMNPQRSTUVWXYZ";
            const lowers = "abcdefghijkmnpqrstuvwxyz";
            const nums = "23456789";
            const syms = "@#$%&*!";

            let p = "";
            p += uppers[Math.floor(Math.random() * uppers.length)];
            p += lowers[Math.floor(Math.random() * lowers.length)];
            p += lowers[Math.floor(Math.random() * lowers.length)];
            p += lowers[Math.floor(Math.random() * lowers.length)];
            p += nums[Math.floor(Math.random() * nums.length)];
            p += nums[Math.floor(Math.random() * nums.length)];
            p += syms[Math.floor(Math.random() * syms.length)];
            p += uppers[Math.floor(Math.random() * uppers.length)];

            const pwField = document.getElementById("page-signup-password");
            const confField = document.getElementById("page-signup-confirm-pw");
            if (pwField && confField) {
                pwField.value = p;
                confField.value = p;
                pwField.type = "text";
                confField.type = "text";
                const toggle1 = document.getElementById("toggle-page-signup-pw");
                const toggle2 = document.getElementById("toggle-page-confirm-pw");
                if (toggle1) toggle1.textContent = "Hide";
                if (toggle2) toggle2.textContent = "Hide";
                updatePasswordStrengthMeter(p);
                showAuthAlert("page-signup-alert", `✨ Suggested strong password applied: <strong>${p}</strong>`, "success");
            }
        });
    }

        // Local-only offline demo authentication (SHA-256 hashed localStorage). Not production-grade backend security; designed for offline hackathon demonstration.
    const DEMO_PW_HASH = "bd4efad903df700dbe8ca80d3b3c569ff7f6fb4a0d4d7e8838cd35b9fb0dacff"; // SHA-256 of "Aura@2026!"

    function getLocalUsersDb() {
        let users = [];
        try { users = JSON.parse(localStorage.getItem("aura_users_db") || "[]"); } catch (err) {}
        if (users.length === 0) {
            users = [
                { name: "S. Pallavi", age: "21", blood: "O+", identifier: "2461783993", password_hash: DEMO_PW_HASH, registeredAt: new Date().toISOString() },
                { name: "Pallavi Sowreddi", age: "21", blood: "O+", identifier: "pallavi@aura.health", password_hash: DEMO_PW_HASH, registeredAt: new Date().toISOString() }
            ];
            localStorage.setItem("aura_users_db", JSON.stringify(users));
        }
        return users;
    }

    // STRICT LOGIN HANDLER WITH SHA-256 HASH VERIFICATION
    if (pageLoginForm) {
        pageLoginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const idEl = document.getElementById("page-login-identifier");
            const pwEl = document.getElementById("page-login-password");
            const id = idEl ? idEl.value.trim() : "";
            const pw = pwEl ? pwEl.value : "";

            if (!id || !pw) {
                showAuthAlert("page-login-alert", "Please enter your Email / Roll Number and Password.", "error");
                return;
            }

            const users = getLocalUsersDb();
            const existingUser = users.find(u => u.identifier.toLowerCase() === id.toLowerCase());

            if (!existingUser) {
                showAuthAlert("page-login-alert", `❌ Account <strong>${id}</strong> not found. You must create your profile first by clicking <a onclick="navigateToTab('signup')" style="text-decoration: underline; cursor: pointer; color: #b45309; font-weight: bold;">Sign Up</a>.`, "error");
                return;
            }

            const inputHash = await hashPasswordSHA256(pw);
            const isMatch = (existingUser.password_hash && existingUser.password_hash === inputHash) ||
                            (existingUser.password && (existingUser.password === inputHash || existingUser.password === pw));

            if (!isMatch) {
                showAuthAlert("page-login-alert", "❌ Incorrect password. Please check your credentials and try again.", "error");
                return;
            }

            // Credentials verified
            currentUser = existingUser;
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            updateAuthUIState();
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            showAuthAlert("page-login-alert", `✓ Welcome back, ${existingUser.name}! Logging you in...`, "success");
            setTimeout(() => {
                navigateToTab("home");
                speakAura(`Welcome back, ${existingUser.name}.`);
            }, 600);
        });
    }

    // SIGNUP HANDLER WITH SHA-256 HASH ENCRYPTION
    if (pageSignupForm) {
        pageSignupForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const nameEl = document.getElementById("page-signup-name");
            const ageEl = document.getElementById("page-signup-age");
            const bloodEl = document.getElementById("page-signup-blood");
            const idEl = document.getElementById("page-signup-identifier");
            const pwEl = document.getElementById("page-signup-password");
            const confirmEl = document.getElementById("page-signup-confirm-pw");

            const name = nameEl ? nameEl.value.trim() : "";
            const age = ageEl ? ageEl.value.trim() : "21";
            const blood = bloodEl ? bloodEl.value : "O+";
            const id = idEl ? idEl.value.trim() : "";
            const pw = pwEl ? pwEl.value : "";
            const confirm = confirmEl ? confirmEl.value : "";

            if (!name || !id || !pw) {
                showAuthAlert("page-signup-alert", "Please fill in your name, email/roll number, and password.", "error");
                return;
            }

            if (pw !== confirm) {
                const mismatch = document.getElementById("page-pw-mismatch");
                if (mismatch) mismatch.style.display = "block";
                showAuthAlert("page-signup-alert", "⚠️ Passwords do not match. Please verify both fields.", "error");
                return;
            } else {
                const mismatch = document.getElementById("page-pw-mismatch");
                if (mismatch) mismatch.style.display = "none";
            }

            if (pw.length < 6) {
                showAuthAlert("page-signup-alert", "Password must be at least 6 characters long. Click 'Suggest Strong Password' for a secure password.", "error");
                return;
            }

            const users = getLocalUsersDb();

            // Check if user already exists
            const duplicate = users.find(u => u.identifier.toLowerCase() === id.toLowerCase());
            if (duplicate) {
                showAuthAlert("page-signup-alert", `An account with ID <strong>${id}</strong> already exists. Please <a onclick="navigateToTab('login')" style="text-decoration: underline; cursor: pointer; color: #b45309; font-weight: bold;">Log In here</a>.`, "error");
                return;
            }

            const pwHash = await hashPasswordSHA256(pw);

            const newUser = {
                name,
                age: age || "21",
                blood: blood || "O+",
                identifier: id,
                password_hash: pwHash,
                registeredAt: new Date().toISOString()
            };

            users.push(newUser);
            localStorage.setItem("aura_users_db", JSON.stringify(users));

            currentUser = newUser;
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            updateAuthUIState();
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");

            showAuthAlert("page-signup-alert", `✓ Patient Profile created successfully! Welcome, <strong>${name}</strong>!`, "success");

            setTimeout(() => {
                navigateToTab("home");
                speakAura(`Welcome, ${name}. Your patient profile has been created successfully.`);
            }, 1000);
        });
    }

    if (pageGuestBtn) {
        pageGuestBtn.addEventListener("click", () => {
            currentUser = { name: "Guest Patient", age: 24, blood: "O+", identifier: "guest" };
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            updateAuthUIState();
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            navigateToTab("home");
        });
    }

    // 1-Click Hackathon Demo Login Button on Landing Gate
    const landingDemoBtn = document.getElementById("landing-demo-login-btn");
    if (landingDemoBtn) {
        landingDemoBtn.addEventListener("click", () => {
            const users = getLocalUsersDb();
            currentUser = users[0] || { name: "S. Pallavi", age: "21", blood: "O+", identifier: "2461783993" };
            localStorage.setItem("aura_active_user", JSON.stringify(currentUser));
            updateAuthUIState();
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            navigateToTab("home");
            speakAura(`Welcome, ${currentUser.name}. Demo workspace activated.`);
        });
    }


    // Initialize application route on startup
    const urlParams = new URLSearchParams(window.location.search);
    const tabParam = urlParams.get("tab");
    const activeUser = getActiveUser();

    if (activeUser) {
        currentUser = activeUser;
        updateAuthUIState();
        const initialTab = (tabParam && !tabParam.startsWith("login") && !tabParam.startsWith("signup")) ? tabParam : "home";
        navigateToTab(initialTab);
    } else {
        updateAuthUIState();
        const initialTab = (tabParam === "login" || tabParam === "signup" || tabParam === "about") ? tabParam : "landing";
        navigateToTab(initialTab);
    }

    // ========================================================================
    // HEALTH TIP OF THE MOMENT (8 MULTILINGUAL TIPS CAROUSEL)
    // ========================================================================
    const HEALTH_TIPS_DATA = {
        en: [
            "Consult a healthcare professional if symptoms persist beyond a few days.",
            "Stay hydrated: Drink at least 8 to 10 glasses of clean water daily to assist renal function.",
            "Wash your hands with soap for at least 20 seconds before eating and after returning home.",
            "Prevent mosquito breeding by eliminating stagnant water around your home weekly.",
            "Maintain a balanced diet rich in leafy greens, proteins, and fresh seasonal fruits.",
            "Prioritize 7 to 8 hours of uninterrupted sleep every night to rebuild cellular immunity.",
            "Take short brisk walks daily: 30 minutes of physical movement lowers hypertension risks.",
            "Keep emergency contact numbers handy and monitor fever using a digital thermometer."
        ],
        hi: [
            "यदि लक्षण कुछ दिनों से अधिक समय तक बने रहें तो किसी स्वास्थ्य विशेषज्ञ से सलाह लें।",
            "हाइड्रेटेड रहें: गुर्दे के सुचारू कार्य के लिए रोजाना कम से कम 8 से 10 गिलास साफ पानी पिएं।",
            "खाना खाने से पहले और घर लौटने के बाद कम से कम 20 सेकंड तक साबुन से हाथ धोएं।",
            "हफ्ते में एक बार घर के आसपास जमा पानी को साफ करके मच्छरों के पनपने को रोकें।",
            "हरी पत्तेदार सब्जियों, दालों और ताजे मौसमी फलों से भरपूर संतुलित आहार लें।",
            "रोग प्रतिरोधक क्षमता बढ़ाने के लिए रोजाना 7 से 8 घंटे की गहरी नींद अवश्य लें।",
            "रोजाना 30 मिनट तेज सैर करें; नियमित शारीरिक गतिविधि उच्च रक्तचाप के खतरे को कम करती है।",
            "आपातकालीन नंबर हमेशा पास रखें और डिजिटल थर्मामीटर से बुखार की सटीक जांच करें।"
        ],
        te: [
            "లక్షణాలు కొన్ని రోజులకు మించి కొనసాగితే వెంటనే వైద్య నిపుణుడిని సంప్రదించండి.",
            "శరీరానికి తగినంత నీరు: కిడ్నీల పనితీరు మెరుగ్గా ఉండటానికి రోజూ 8-10 గ్లాసుల స్వచ్ఛమైన నీరు తాగండి.",
            "భోజనానికి ముందు మరియు బయటి నుండి వచ్చిన తర్వాత చేతులను 20 సెకన్ల పాటు సబ్బుతో శుభ్రం చేసుకోండి.",
            "ఇంటి చుట్టూ నీరు నిల్వ ఉండకుండా వారానికొకసారి శుభ్రం చేసి దోమల వృద్ధిని అరికట్టండి.",
            "ఆకుకూరలు, పప్పుధాన్యాలు మరియు తాజా పండ్లతో కూడిన సమతుల్య పోషకాహారాన్ని తీసుకోండి.",
            "రోగనిరోధక శక్తిని పెంచడానికి ప్రతి రాత్రి 7 నుండి 8 గంటల నిరంతర నిద్ర అవసరం.",
            "రోజూ 30 నిమిషాల వేగవంతమైన నడక చేయండి; ఇది రక్తపోటు ప్రమాదాన్ని చాలా వరకు తగ్గిస్తుంది.",
            "అత్యవసర ఫోన్ నంబర్లను సిద్ధంగా ఉంచుకోండి మరియు డిజిటల్ థర్మామీటర్‌తో జ్వరాన్ని కొలవండి."
        ]
    };

    let currentTipIndex = 0;
    let tipAutoInterval = null;

    const tipTextEl = document.getElementById("health-tip-text");
    const tipDotsContainer = document.getElementById("health-tip-dots");
    const tipPrevBtn = document.getElementById("tip-prev-btn");
    const tipNextBtn = document.getElementById("tip-next-btn");
    const tipSpeakBtn = document.getElementById("health-tip-speak-btn");

    function renderHealthTip(index) {
        const curLang = languageSelector ? languageSelector.value : (localStorage.getItem("aura_lang") || "en");
        const tips = HEALTH_TIPS_DATA[curLang] || HEALTH_TIPS_DATA.en;
        currentTipIndex = (index + tips.length) % tips.length;

        if (tipTextEl) {
            tipTextEl.style.opacity = "0";
            setTimeout(() => {
                tipTextEl.textContent = tips[currentTipIndex];
                tipTextEl.style.opacity = "1";
            }, 200);
        }

        // Render dots
        if (tipDotsContainer) {
            tipDotsContainer.innerHTML = "";
            tips.forEach((_, i) => {
                const dot = document.createElement("span");
                dot.className = "health-tip-dot" + (i === currentTipIndex ? " active" : "");
                dot.title = `Tip ${i + 1}`;
                dot.addEventListener("click", () => {
                    renderHealthTip(i);
                    resetTipTimer();
                });
                tipDotsContainer.appendChild(dot);
            });
        }
    }

    function resetTipTimer() {
        if (tipAutoInterval) clearInterval(tipAutoInterval);
        tipAutoInterval = setInterval(() => {
            renderHealthTip(currentTipIndex + 1);
        }, 6500);
    }

    if (tipPrevBtn) {
        tipPrevBtn.addEventListener("click", () => {
            renderHealthTip(currentTipIndex - 1);
            resetTipTimer();
        });
    }
    if (tipNextBtn) {
        tipNextBtn.addEventListener("click", () => {
            renderHealthTip(currentTipIndex + 1);
            resetTipTimer();
        });
    }

    if (tipSpeakBtn) {
        tipSpeakBtn.addEventListener("click", () => {
            if (tipTextEl) {
                speakAura(tipTextEl.textContent);
            }
        });
    }

    renderHealthTip(0);
    resetTipTimer();

    // ========================================================================
    // PASSWORD SHOW/HIDE TOGGLES FOR SPA LOGIN & SIGNUP
    // ========================================================================
    function setupPwToggle(btnId, inpId) {
        const btn = document.getElementById(btnId);
        const inp = document.getElementById(inpId);
        if (btn && inp) {
            btn.addEventListener("click", () => {
                if (inp.type === "password") {
                    inp.type = "text";
                    btn.textContent = "Hide";
                } else {
                    inp.type = "password";
                    btn.textContent = "Show";
                }
            });
        }
    }

    setupPwToggle("toggle-page-login-pw", "page-login-password");
    setupPwToggle("toggle-page-signup-pw", "page-signup-password");
    setupPwToggle("toggle-page-confirm-pw", "page-signup-confirm-pw");

// Redundant listener removed - unified in main pageSignupForm submit handler


    // ========================================================================
    // VACCINATION SCHEDULES MODULE
    // ========================================================================
    const VACCINE_DATABASE = [
        { id: "bcg", name: "BCG (Bacillus Calmette-Guérin)", cat: "infants", age: "At Birth", route: "Intradermal", target: "Tuberculosis (TB)", notes: "Essential for pediatric TB meningitis prevention." },
        { id: "hepb_birth", name: "Hepatitis B (Birth Dose)", cat: "infants", age: "At Birth (<24h)", route: "Intramuscular", target: "Hepatitis B Virus", notes: "Prevents perinatal transmission from mother to baby." },
        { id: "opv_0", name: "OPV-0 (Oral Polio Vaccine)", cat: "infants", age: "At Birth", route: "Oral Drops (2 drops)", target: "Poliomyelitis (Polio)", notes: "Birth dose gives early mucosal gut immunity." },
        { id: "penta_1", name: "Pentavalent-1 (DTP-HepB-Hib)", cat: "infants", age: "6 Weeks", route: "Intramuscular", target: "Diphtheria, Pertussis, Tetanus, Hep B, Hib", notes: "5-in-1 combo vaccine saving infants from 5 fatal diseases." },
        { id: "rota_1", name: "Rotavirus Vaccine (RVV-1)", cat: "infants", age: "6 Weeks", route: "Oral (5 drops)", target: "Rotavirus Severe Diarrhea", notes: "Protects infants against dehydration from viral diarrhea." },
        { id: "pcv_1", name: "PCV-1 (Pneumococcal Conjugate)", cat: "infants", age: "6 Weeks", route: "Intramuscular", target: "Streptococcus Pneumoniae", notes: "Shields against severe pneumonia & bacterial sepsis." },
        { id: "mr_1", name: "MR-1 (Measles & Rubella)", cat: "children", age: "9-12 Months", route: "Subcutaneous", target: "Measles & Rubella Virus", notes: "Prevents fatal measles complications & congenital rubella." },
        { id: "je_1", name: "JE Vaccine (Japanese Encephalitis)", cat: "children", age: "9-12 Months", route: "Subcutaneous", target: "Japanese Encephalitis Virus", notes: "Crucial in endemic agricultural & wetland regions." },
        { id: "dtp_b1", name: "DTP Booster-1", cat: "children", age: "16-24 Months", route: "Intramuscular", target: "Diphtheria, Tetanus, Pertussis", notes: "Reinforces waning infant immunity." },
        { id: "typhoid_c", name: "Typhoid Conjugate Vaccine (TCV)", cat: "children", age: "2 Years", route: "Intramuscular", target: "Salmonella Typhi (Typhoid)", notes: "Long-lasting protection against enteric typhoid fever." },
        { id: "hpv", name: "HPV Vaccine (Human Papillomavirus)", cat: "teens", age: "9-14 Years", route: "Intramuscular (2 Doses)", target: "Cervical Cancer & Genital Warts", notes: "Protects young girls against high-risk oncogenic strains." },
        { id: "td_teens", name: "Td (Tetanus & adult Diphtheria)", cat: "teens", age: "10 & 16 Years", route: "Intramuscular", target: "Tetanus & Diphtheria", notes: "Routine decennial adolescent boosters." },
        { id: "flu_annual", name: "Influenza (Annual Flu Shot)", cat: "adults", age: "Yearly", route: "Intramuscular", target: "Seasonal Influenza (H1N1/H3N2)", notes: "Recommended for healthcare workers and individuals with asthma." },
        { id: "covid_booster", name: "COVID-19 Updated Booster", cat: "adults", age: "Annual / High Risk", route: "Intramuscular", target: "SARS-CoV-2 Variants", notes: "Sustains neutralizing spike antibodies." },
        { id: "pneumo_senior", name: "Pneumococcal Polysaccharide (PPSV23)", cat: "seniors", age: "65+ Years", route: "Intramuscular", target: "Invasive Pneumococcal Disease", notes: "Prevents bacteremic pneumonia and meningitis in seniors." },
        { id: "shingles", name: "Recombinant Zoster Vaccine (Shingrix)", cat: "seniors", age: "50+ Years", route: "Intramuscular (2 Doses)", target: "Herpes Zoster (Shingles)", notes: "Over 90% protection against painful postherpetic neuralgia." }
    ];

    let currentVacFilter = "all";

    function renderVaccinesList() {
        const container = document.getElementById("vac-cards-grid");
        if (!container) return;

        const searchVal = (document.getElementById("vac-search-input")?.value || "").toLowerCase();
        let takenSet = new Set(JSON.parse(localStorage.getItem("aura_taken_vaccines") || "[]"));

        const filtered = VACCINE_DATABASE.filter(v => {
            const matchesCat = (currentVacFilter === "all" || v.cat === currentVacFilter);
            const matchesSearch = v.name.toLowerCase().includes(searchVal) || 
                                  v.target.toLowerCase().includes(searchVal) || 
                                  v.age.toLowerCase().includes(searchVal);
            return matchesCat && matchesSearch;
        });

        container.innerHTML = "";
        if (filtered.length === 0) {
            container.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 30px; color: var(--text-muted);">No immunization schedules matched your search.</div>`;
            return;
        }

        filtered.forEach(v => {
            const isTaken = takenSet.has(v.id);
            const card = document.createElement("div");
            card.className = "vac-card" + (isTaken ? " vac-taken" : "");
            card.innerHTML = `
                <div>
                    <div class="vac-card-header">
                        <span class="vac-card-title">${v.name}</span>
                        <span class="vac-age-tag">${v.age}</span>
                    </div>
                    <div class="vac-target-disease">🛡️ <strong>Prevents:</strong> ${v.target}</div>
                    <div style="font-size: 0.76rem; color: var(--text-secondary); margin-bottom: 10px;">${v.notes}</div>
                </div>
                <div class="vac-footer-row">
                    <span>Route: <strong>${v.route}</strong></span>
                    <label class="vac-check-label">
                        <input type="checkbox" ${isTaken ? "checked" : ""} onchange="toggleVaccineDose('${v.id}')">
                        <span>${isTaken ? "✅ Administered" : "Mark as Taken"}</span>
                    </label>
                </div>
            `;
            container.appendChild(card);
        });
    }

    window.toggleVaccineDose = function(id) {
        let taken = JSON.parse(localStorage.getItem("aura_taken_vaccines") || "[]");
        let set = new Set(taken);
        if (set.has(id)) set.delete(id);
        else set.add(id);
        localStorage.setItem("aura_taken_vaccines", JSON.stringify(Array.from(set)));
        renderVaccinesList();
    };

    document.querySelectorAll(".vac-pill").forEach(pill => {
        pill.addEventListener("click", () => {
            document.querySelectorAll(".vac-pill").forEach(p => p.classList.remove("active"));
            pill.classList.add("active");
            currentVacFilter = pill.getAttribute("data-vac-filter");
            renderVaccinesList();
        });
    });

    const vacSearchInp = document.getElementById("vac-search-input");
    if (vacSearchInp) vacSearchInp.addEventListener("input", renderVaccinesList);
    renderVaccinesList();

    // ========================================================================
    // MEDICAL REPORTS: SUB-TAB SWITCHER & 1-CLICK LAB PRESETS
    // ========================================================================
    window.switchReportSubTab = function(sub) {
        const btnVisual = document.getElementById("tab-btn-visual");
        const btnLab = document.getElementById("tab-btn-lab");
        const subVisual = document.getElementById("rep-subview-visual");
        const subLab = document.getElementById("rep-subview-lab");

        if (sub === "visual") {
            btnVisual?.classList.add("active");
            btnLab?.classList.remove("active");
            subVisual?.classList.remove("hidden");
            subLab?.classList.add("hidden");
        } else {
            btnLab?.classList.add("active");
            btnVisual?.classList.remove("active");
            subLab?.classList.remove("hidden");
            subVisual?.classList.add("hidden");
            if (!window.labTableInitialized) {
                applyLabPreset("normal");
                window.labTableInitialized = true;
            }
        }
    };

    function evaluateBiomarkerStatus(valStr, rangeStr) {
    if (!valStr || !rangeStr) return { status: "normal", label: "NORMAL", triage: "Normal range observation" };
    // Blood pressure handling (e.g. 118/76)
    if (valStr.includes("/")) {
        const parts = valStr.split("/");
        const sys = parseFloat(parts[0]);
        const dia = parseFloat(parts[1]);
        if (sys >= 140 || dia >= 90) return { status: "high", label: "HIGH", triage: "Stage-2 hypertension threshold" };
        if (sys >= 120 || dia >= 80) return { status: "high", label: "ELEVATED", triage: "Pre-hypertension reading" };
        return { status: "normal", label: "NORMAL", triage: "Optimal arterial hemodynamic pressure" };
    }

    const numVal = parseFloat(valStr.replace(/,/g, ""));
    if (isNaN(numVal)) return { status: "normal", label: "NORMAL", triage: "Clinical parameter verified" };

    let minRef = null;
    let maxRef = null;

    if (rangeStr.includes("-")) {
        const parts = rangeStr.split("-");
        minRef = parseFloat(parts[0].replace(/,/g, "").trim());
        maxRef = parseFloat(parts[1].replace(/,/g, "").trim());
    } else if (rangeStr.startsWith("<")) {
        maxRef = parseFloat(rangeStr.replace("<", "").replace(/,/g, "").trim());
    } else if (rangeStr.startsWith(">")) {
        minRef = parseFloat(rangeStr.replace(">", "").replace(/,/g, "").trim());
    }

    if (minRef !== null && numVal < minRef) {
        const ratio = numVal / minRef;
        if (ratio < 0.6) {
            return { status: "low", label: "CRITICAL LOW", triage: `Severely depressed below lower reference threshold (${minRef})` };
        }
        return { status: "low", label: "LOW", triage: `Below reference limit (${minRef} - ${maxRef})` };
    }
    if (maxRef !== null && numVal > maxRef) {
        const ratio = numVal / maxRef;
        if (ratio > 1.4) {
            return { status: "high", label: "CRITICAL HIGH", triage: `Significantly elevated above reference threshold (${maxRef})` };
        }
        return { status: "high", label: "HIGH", triage: `Above reference limit (${maxRef})` };
    }
    return { status: "normal", label: "NORMAL", triage: "Safely within international clinical reference intervals" };
}

const LAB_PRESETS_DATA = {
    dengue: {
        title: "Dengue Suspect (CBC)",
        statusBadge: "🚨 Severe Thrombocytopenia Warning",
        statusColor: "#dc2626",
        summary: "Dengue Suspect (CBC): Critical low Platelets (62,000 /µL), elevated Hematocrit (52%), and Leukopenia (WBC 2,800 /µL) with Hemoglobin at 15.1 g/dL indicate acute hemoconcentration and plasma leakage. Urgent clinical hydration required.",
        biomarkers: [
            { test: "Platelets", val: "62,000", unit: "/µL", range: "150,000-450,000", status: "low", label: "CRITICAL LOW", triage: "Severe thrombocytopenia (critical bleeding risk, urgent fluid resuscitation)" },
            { test: "Hematocrit", val: "52", unit: "%", range: "36-46% F / 41-53% M", status: "high", label: "HIGH", triage: "Hemoconcentration indicating significant vascular plasma leakage" },
            { test: "Hemoglobin", val: "15.1", unit: "g/dL", range: "12.0-16.0", status: "normal", label: "NORMAL", triage: "Within standard physiological reference interval" },
            { test: "WBC", val: "2,800", unit: "/µL", range: "4,500-11,000", status: "low", label: "LOW", triage: "Leukopenia consistent with acute viral bone marrow suppression" }
        ]
    },
    diabetes: {
        title: "Diabetes Workup",
        statusBadge: "🚨 Hyperglycemia Alert",
        statusColor: "#d97706",
        summary: "Diabetes Workup: Marked Fasting Glucose (210 mg/dL), Random Glucose (260 mg/dL), and HbA1c (9.2%) confirm uncontrolled Type 2 Diabetes Mellitus requiring clinical endocrinological intervention.",
        biomarkers: [
            { test: "Fasting Glucose", val: "210", unit: "mg/dL", range: "70-99", status: "high", label: "HIGH", triage: "Marked fasting hyperglycemia well above diabetic threshold" },
            { test: "HbA1c", val: "9.2", unit: "%", range: "<5.7%", status: "high", label: "HIGH", triage: "Significantly elevated glycated hemoglobin indicating poor long-term glycemic control" },
            { test: "Random Glucose", val: "260", unit: "mg/dL", range: "<140", status: "high", label: "HIGH", triage: "Severe post-glucose elevation confirming diabetic metabolic state" }
        ]
    },
    jaundice: {
        title: "Liver Function (LFT)",
        statusBadge: "🚨 Acute Hepatic Inflammation",
        statusColor: "#dc2626",
        summary: "Liver Function (LFT): Hyperbilirubinemia (Total Bilirubin 4.2 mg/dL) and marked transaminitis (ALT 180 U/L, AST 165 U/L) demonstrate acute hepatocellular injury / hepatitis requiring clinical evaluation.",
        biomarkers: [
            { test: "Total Bilirubin", val: "4.2", unit: "mg/dL", range: "0.1-1.2", status: "high", label: "HIGH", triage: "Marked Jaundice / Hyperbilirubinemia" },
            { test: "ALT", val: "180", unit: "U/L", range: "7-56", status: "high", label: "HIGH", triage: "Marked alanine aminotransferase elevation (acute hepatocellular damage)" },
            { test: "AST", val: "165", unit: "U/L", range: "8-48", status: "high", label: "HIGH", triage: "Significant aspartate aminotransferase elevation" }
        ]
    },
    anemia: {
        title: "Severe Anemia",
        statusBadge: "🚨 Severe Anemia Alert",
        statusColor: "#dc2626",
        summary: "Severe Anemia: Critically depressed Hemoglobin (7.4 g/dL), depleted Serum Ferritin (8 ng/mL), and reduced RBC (3.1 million/µL) indicate profound microcytic hypochromic iron-deficiency anemia.",
        biomarkers: [
            { test: "Hemoglobin", val: "7.4", unit: "g/dL", range: "12.0-16.0", status: "low", label: "CRITICAL LOW", triage: "Severe Anemia near transfusion threshold (Critical threshold < 8.0 g/dL)" },
            { test: "Ferritin", val: "8", unit: "ng/mL", range: "12-150 F / 12-300 M", status: "low", label: "LOW", triage: "Exhausted iron storage reserves (Profound iron deficiency)" },
            { test: "RBC", val: "3.1", unit: "million/µL", range: "4.2-5.4", status: "low", label: "LOW", triage: "Depleted circulating erythrocytes" }
        ]
    },
    normal: {
        title: "Healthy Baseline",
        statusBadge: "✅ Normative Baseline",
        statusColor: "#059669",
        summary: "Healthy Baseline: All biomarker parameters (Hemoglobin 14.2 g/dL, Platelet Count 245,000 /µL, Fasting Glucose 88 mg/dL, and ALT 24 U/L) fall squarely within healthy normative clinical intervals.",
        biomarkers: [
            { test: "Hemoglobin", val: "14.2", unit: "g/dL", range: "12.0-16.0", status: "normal", label: "NORMAL", triage: "Optimal red blood cell oxygen carrying capacity" },
            { test: "Platelet Count", val: "245,000", unit: "/µL", range: "150,000-450,000", status: "normal", label: "NORMAL", triage: "Optimal hemostatic thrombocyte count" },
            { test: "Fasting Glucose", val: "88", unit: "mg/dL", range: "70-99", status: "normal", label: "NORMAL", triage: "Euglycemic fasting blood glucose level" },
            { test: "ALT", val: "24", unit: "U/L", range: "7-56", status: "normal", label: "NORMAL", triage: "Normal baseline hepatic transaminase activity" }
        ]
    }
};

window.applyLabPreset = function(presetKey) {
        const data = LAB_PRESETS_DATA[presetKey];
        if (!data) return;

        const tbody = document.getElementById("lab-table-body");
        const statusBadge = document.getElementById("lab-overall-status");
        const summaryText = document.getElementById("lab-summary-text");

        if (statusBadge) {
            statusBadge.textContent = data.statusBadge;
            statusBadge.style.background = data.statusColor;
        }
        if (summaryText) summaryText.textContent = data.summary;

        if (tbody) {
            tbody.innerHTML = "";
            data.biomarkers.forEach(b => {
                const tr = document.createElement("tr");
                const label = b.label || (b.status === "normal" ? "NORMAL" : b.status.toUpperCase());
                const badgeClass = b.status === "normal" 
                    ? "lab-badge-normal" 
                    : ((label.includes("CRITICAL")) ? "lab-badge-critical" : (b.status === "low" ? "lab-badge-low" : "lab-badge-high"));
                tr.innerHTML = `
                    <td><strong>${b.test}</strong></td>
                    <td style="font-weight: 800; font-family: 'IBM Plex Mono', monospace;">${b.val}</td>
                    <td style="color: var(--text-muted);">${b.unit}</td>
                    <td style="color: var(--text-secondary);">${b.range}</td>
                    <td><span class="${badgeClass}">${label}</span></td>
                    <td style="font-size: 0.74rem; color: var(--text-secondary);">${b.triage}</td>
                `;
                tbody.appendChild(tr);
            });
        }
    };

    window.printLabReport = function() {
        window.print();
    };

    // ========================================================================
    // SOCIAL-MEDIA GRADE SETTINGS ENGINE
    // ========================================================================
    // 1. Theme Switcher
    const themeSelect = document.getElementById("cfg-theme-selector");
    if (themeSelect) {
        const savedTheme = localStorage.getItem("aura_theme") || "light";
        themeSelect.value = savedTheme;
        applyTheme(savedTheme);
        themeSelect.addEventListener("change", (e) => {
            const t = e.target.value;
            applyTheme(t);
            localStorage.setItem("aura_theme", t);
        });
    }

    function applyTheme(theme) {
        if (theme === "dark") {
            document.body.classList.add("dark-theme");
            document.body.classList.remove("oled-theme");
        } else if (theme === "oled") {
            document.body.classList.add("oled-theme");
            document.body.classList.remove("dark-theme");
        } else {
            document.body.classList.remove("dark-theme");
            document.body.classList.remove("oled-theme");
        }
    }

    // 2. Font Size Scaler
    const fontSelect = document.getElementById("cfg-font-size");
    if (fontSelect) {
        const savedFont = localStorage.getItem("aura_font_size") || "normal";
        fontSelect.value = savedFont;
        applyFontSize(savedFont);
        fontSelect.addEventListener("change", (e) => {
            const f = e.target.value;
            applyFontSize(f);
            localStorage.setItem("aura_font_size", f);
        });
    }

    function applyFontSize(size) {
        document.documentElement.style.fontSize = size === "xlarge" ? "18px" : (size === "large" ? "16.5px" : "15px");
    }

    // 3. Voice Rate Slider
    const rateSlider = document.getElementById("cfg-voice-rate");
    const rateValText = document.getElementById("cfg-rate-val");
    if (rateSlider && rateValText) {
        const savedRate = localStorage.getItem("aura_voice_rate") || "1.0";
        rateSlider.value = savedRate;
        rateValText.textContent = `Speed: ${savedRate}x`;
        rateSlider.addEventListener("input", (e) => {
            rateValText.textContent = `Speed: ${e.target.value}x`;
            localStorage.setItem("aura_voice_rate", e.target.value);
        });
    }

    // 4. Patient Profile Save
    const profileForm = document.getElementById("settings-profile-form");
    if (profileForm) {
        try {
            const stored = JSON.parse(localStorage.getItem("aura_active_user") || "{}");
            if (stored.name) document.getElementById("cfg-profile-name").value = stored.name;
            if (stored.age) document.getElementById("cfg-profile-age").value = stored.age;
            if (stored.blood) document.getElementById("cfg-profile-blood").value = stored.blood;
            if (stored.phone) document.getElementById("cfg-profile-phone").value = stored.phone;
            if (stored.allergies) document.getElementById("cfg-profile-allergies").value = stored.allergies;
        } catch(e) {}

        profileForm.addEventListener("submit", (e) => {
            e.preventDefault();
            const profile = {
                name: document.getElementById("cfg-profile-name").value || "Pallavi Sowreddi",
                age: document.getElementById("cfg-profile-age").value || "21",
                blood: document.getElementById("cfg-profile-blood").value || "O+",
                phone: document.getElementById("cfg-profile-phone").value || "",
                allergies: document.getElementById("cfg-profile-allergies").value || "",
                identifier: "patient"
            };
            localStorage.setItem("aura_active_user", JSON.stringify(profile));
            currentUser = profile;
            renderCurrentUserBadge(languageSelector ? languageSelector.value : "en");
            alert("✅ Patient profile updated successfully!");
        });
    }

    // 5. Export Health Data to JSON Backup
    window.exportHealthDataJSON = function() {
        const backupData = {
            platform: "AURA AI Offline Health Assistant",
            version: "2026.1",
            exportDate: new Date().toISOString(),
            patientProfile: JSON.parse(localStorage.getItem("aura_active_user") || "{}"),
            administeredVaccines: JSON.parse(localStorage.getItem("aura_taken_vaccines") || "[]"),
            prescriptions: JSON.parse(localStorage.getItem("medications_list") || "[]"),
            vitalsHistory: JSON.parse(localStorage.getItem("vitals_history") || "[]")
        };
        const blob = new Blob([JSON.stringify(backupData, null, 2)], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `AURA_Health_Data_${new Date().toISOString().slice(0, 10)}.json`;
        a.click();
        URL.revokeObjectURL(url);
    };

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


    // =========================================================================
    // MOBILE NAVIGATION DRAWER CONTROLLER
    // =========================================================================
    const mobileMenuBtn = document.getElementById("mobile-menu-btn");
    const mobileNavDrawer = document.getElementById("mobile-nav-drawer");
    const mobileDrawerOverlay = document.getElementById("mobile-drawer-overlay");
    const drawerCloseBtn = document.getElementById("drawer-close-btn");

    function openMobileDrawer() {
        if (mobileNavDrawer) mobileNavDrawer.classList.add("open");
        if (mobileDrawerOverlay) mobileDrawerOverlay.classList.remove("hidden");
        document.body.style.overflow = "hidden";
    }

    function closeMobileDrawer() {
        if (mobileNavDrawer) mobileNavDrawer.classList.remove("open");
        if (mobileDrawerOverlay) mobileDrawerOverlay.classList.add("hidden");
        document.body.style.overflow = "";
    }

    window.closeMobileDrawer = closeMobileDrawer;

    if (mobileMenuBtn) mobileMenuBtn.addEventListener("click", openMobileDrawer);
    if (drawerCloseBtn) drawerCloseBtn.addEventListener("click", closeMobileDrawer);
    if (mobileDrawerOverlay) mobileDrawerOverlay.addEventListener("click", closeMobileDrawer);

    // Mobile nav links click
    document.querySelectorAll(".mobile-nav-item").forEach(btn => {
        btn.addEventListener("click", () => {
            const tab = btn.getAttribute("data-tab");
            if (tab && typeof navigateToTab === "function") {
                navigateToTab(tab);
            }
            document.querySelectorAll(".mobile-nav-item").forEach(b => b.classList.remove("active"));
            btn.classList.add("active");
            closeMobileDrawer();
        });
    });

    // Mobile drawer secondary triggers
    document.getElementById("mobile-drawer-relax-btn")?.addEventListener("click", () => {
        closeMobileDrawer();
        document.getElementById("relax-btn")?.click();
    });
    document.getElementById("mobile-drawer-live-btn")?.addEventListener("click", () => {
        closeMobileDrawer();
        document.getElementById("live-reading-btn")?.click();
    });
    document.getElementById("mobile-drawer-tour-btn")?.addEventListener("click", () => {
        closeMobileDrawer();
        document.getElementById("tour-launcher-btn")?.click();
    });

    // =========================================================================
    // ENHANCED REPORTS SCANNER: DOCUMENT OCR VS SKIN LESION HANDLER
    // =========================================================================
    function renderDocumentAnalysisCard(data) {
        const docView = document.getElementById("doc-scan-results-view");
        const skinView = document.getElementById("skin-scan-results-view");
        const resultsCard = document.getElementById("reports-results-card");
        
        if (!docView || !skinView || !resultsCard) return;

        // Switch to Document View
        docView.classList.remove("hidden");
        skinView.classList.add("hidden");
        resultsCard.classList.remove("hidden");

        // Document Details
        const titleEl = document.getElementById("doc-title-text");
        if (titleEl) titleEl.innerText = data.doc_type || "General Clinical Check-up Report";

        const confBadge = document.getElementById("doc-confidence-badge");
        if (confBadge) confBadge.innerText = `${Math.round((data.confidence || 0.98) * 100)}% OCR Match`;

        // Patient Strip
        if (document.getElementById("doc-patient-name")) document.getElementById("doc-patient-name").innerText = data.patient_name || "Patient (from report)";
        if (document.getElementById("doc-patient-age")) {
            const a = data.patient_age ? `${data.patient_age} Yrs` : "Age unspecified";
            const d = data.patient_dob ? ` (${data.patient_dob})` : "";
            document.getElementById("doc-patient-age").innerText = `${a}${d}`;
        }
        if (document.getElementById("doc-patient-gender")) document.getElementById("doc-patient-gender").innerText = data.patient_gender || "Clinical Record";
        if (document.getElementById("doc-doctor-name")) document.getElementById("doc-doctor-name").innerText = data.doctor || "Attending Clinician";
        if (document.getElementById("doc-report-date")) document.getElementById("doc-report-date").innerText = data.date || new Date().toISOString().split("T")[0];

        // Vitals Grid
        const vitalsGrid = document.getElementById("doc-vitals-grid");
        if (vitalsGrid) {
            vitalsGrid.innerHTML = "";
            const vitals = data.vitals || [];
            vitals.forEach(v => {
                const card = document.createElement("div");
                card.className = `doc-vital-card ${v.type || 'info'}`;
                card.innerHTML = `
                    <div style="font-size: 1.4rem;">${v.icon || '💓'}</div>
                    <div style="flex: 1;">
                        <div style="font-size: 0.68rem; color: var(--text-muted);">${v.name}</div>
                        <div style="font-size: 0.95rem; font-weight: 800; color: var(--text-primary);">${v.value}</div>
                        <div style="font-size: 0.66rem; font-weight: 600; color: ${v.type === 'danger' ? '#ef4444' : (v.type === 'warning' ? '#d97706' : '#10b981')};">${v.status}</div>
                    </div>
                `;
                vitalsGrid.appendChild(card);
            });
        }

        // Diagnoses
        const condList = document.getElementById("doc-conditions-list");
        if (condList) {
            condList.innerHTML = (data.diagnoses && data.diagnoses.length > 0)
                ? data.diagnoses.map(d => `<div style="margin-bottom: 3px;">• <strong>${d}</strong></div>`).join("")
                : "None recorded.";
        }

        // Medications
        const medList = document.getElementById("doc-medications-list");
        if (medList) {
            medList.innerHTML = (data.medications && data.medications.length > 0)
                ? data.medications.map(m => `<div style="margin-bottom: 3px;">• <strong>${m}</strong></div>`).join("")
                : "None recorded.";
        }

        // Guidance
        const guideEl = document.getElementById("doc-guidance-text");
        if (guideEl) {
            guideEl.innerText = data.care_guidance || data.advice || "Follow attending physician directives.";
        }

        // Audio announcement
        speakAura(`Medical report analyzed. Identified ${data.doc_type} for ${data.patient_name || 'patient'}. Key finding: ${data.vitals && data.vitals.length > 0 ? data.vitals[0].name + ' ' + data.vitals[0].value : 'Vitals recorded'}.`);
    }
