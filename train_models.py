import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from PIL import Image, ImageDraw

# Ensure directories exist
os.makedirs("models", exist_ok=True)
os.makedirs("static/assets/sample_images", exist_ok=True)

# ==========================================
# PART 1: 34-DISEASE SYMPTOM PREDICTION MODEL
# ==========================================
print("Generating expanded 34-disease medical symptom dataset...")

# 67 Clinical Symptoms covering infectious, chronic, cardiovascular, metabolic & dermatological domains
symptoms_list = [
    # General & Systemic
    "fever", "high_fever", "fatigue", "chills", "sweating", "night_sweats", 
    "unexplained_weight_loss", "unexplained_weight_gain", "weakness", "dizziness",
    
    # Head, ENT & Neurological
    "headache", "throbbing_headache", "sore_throat", "runny_nose", "sneezing",
    "loss_of_taste_smell", "itchy_eyes", "blurred_vision", "numbness_one_side", 
    "slurred_speech", "confusion",
    
    # Respiratory & Chest
    "cough", "cough_with_phlegm", "cough_with_blood", "shortness_of_breath",
    "wheezing", "chest_tightness", "chest_pain", "neck_radiating_pain",
    
    # Cardiovascular & Vitals
    "palpitations", "rapid_heartbeat", "swollen_legs_ankles", "cold_hands_feet",
    
    # Gastrointestinal & Abdominal
    "nausea", "vomiting", "diarrhea", "watery_diarrhea", "stomach_pain",
    "burning_stomach_pain", "heartburn", "acid_regurgitation", "loss_of_appetite",
    "increased_thirst", "increased_hunger",
    
    # Urinary & Renal
    "frequent_urination", "burning_urination", "dark_urine", "pale_stools",
    
    # Musculoskeletal
    "body_ache", "joint_pain", "joint_swelling", "joint_stiffness",
    "muscle_weakness", "muscle_cramps",
    
    # Dermatological & Skin
    "rash", "itching", "dry_skin", "skin_redness", "blisters",
    "silvery_scales", "acne_pimples", "slow_healing_sores", "yellow_skin_eyes",
    
    # Metabolic & Endocrine
    "excessive_body_fat", "cold_sensitivity", "heat_sensitivity", "tremors"
]

disease_symptoms = {
    # 1. From User Kaggle Healthcare Dataset
    "Diabetes": {
        "primary": ["increased_thirst", "frequent_urination", "unexplained_weight_loss", "fatigue"],
        "secondary": ["blurred_vision", "slow_healing_sores", "increased_hunger", "weakness"]
    },
    "Hypertension": {
        "primary": ["headache", "dizziness", "shortness_of_breath", "palpitations"],
        "secondary": ["blurred_vision", "chest_pain", "fatigue"]
    },
    "Asthma": {
        "primary": ["shortness_of_breath", "wheezing", "chest_tightness", "cough"],
        "secondary": ["fatigue", "rapid_heartbeat"]
    },
    "Arthritis": {
        "primary": ["joint_pain", "joint_stiffness", "joint_swelling"],
        "secondary": ["muscle_weakness", "fatigue", "skin_redness"]
    },
    "Cancer (Early Warning)": {
        "primary": ["unexplained_weight_loss", "fatigue", "weakness", "night_sweats"],
        "secondary": ["loss_of_appetite", "fever", "cough"]
    },
    "Obesity": {
        "primary": ["excessive_body_fat", "shortness_of_breath", "fatigue"],
        "secondary": ["joint_pain", "sweating", "weakness"]
    },

    # 2. Infectious & Tropical Epidemics
    "Dengue Fever": {
        "primary": ["high_fever", "fever", "headache", "joint_pain", "rash"],
        "secondary": ["nausea", "vomiting", "fatigue", "body_ache"]
    },
    "Malaria": {
        "primary": ["fever", "high_fever", "chills", "sweating", "headache"],
        "secondary": ["nausea", "body_ache", "fatigue"]
    },
    "Typhoid Fever": {
        "primary": ["high_fever", "fever", "stomach_pain", "headache", "weakness"],
        "secondary": ["diarrhea", "loss_of_appetite", "fatigue", "body_ache"]
    },
    "Tuberculosis": {
        "primary": ["cough_with_blood", "cough", "night_sweats", "unexplained_weight_loss"],
        "secondary": ["chest_pain", "cough_with_phlegm", "fever", "fatigue"]
    },
    "Pneumonia": {
        "primary": ["cough_with_phlegm", "high_fever", "chills", "shortness_of_breath", "chest_pain"],
        "secondary": ["fatigue", "sweating", "rapid_heartbeat"]
    },
    "COVID-19": {
        "primary": ["fever", "cough", "fatigue", "shortness_of_breath", "loss_of_taste_smell"],
        "secondary": ["sore_throat", "body_ache", "headache"]
    },
    "Influenza": {
        "primary": ["high_fever", "fever", "body_ache", "chills", "headache", "fatigue"],
        "secondary": ["cough", "sore_throat", "runny_nose"]
    },
    "Common Cold": {
        "primary": ["runny_nose", "sneezing", "sore_throat", "cough"],
        "secondary": ["fatigue", "headache"]
    },
    "Chickenpox": {
        "primary": ["blisters", "rash", "itching", "fever"],
        "secondary": ["fatigue", "loss_of_appetite", "headache", "body_ache"]
    },
    "Gastroenteritis": {
        "primary": ["watery_diarrhea", "diarrhea", "vomiting", "nausea", "stomach_pain"],
        "secondary": ["fever", "fatigue", "muscle_cramps"]
    },
    "Cholera": {
        "primary": ["watery_diarrhea", "vomiting", "muscle_cramps"],
        "secondary": ["increased_thirst", "weakness", "cold_hands_feet"]
    },
    "Hepatitis": {
        "primary": ["yellow_skin_eyes", "dark_urine", "pale_stools", "fatigue"],
        "secondary": ["nausea", "stomach_pain", "loss_of_appetite", "joint_pain"]
    },
    "Jaundice": {
        "primary": ["yellow_skin_eyes", "dark_urine", "itching"],
        "secondary": ["fatigue", "loss_of_appetite", "pale_stools"]
    },

    # 3. Cardiovascular, Neurological & Organ-Specific
    "Coronary Artery Disease": {
        "primary": ["chest_pain", "neck_radiating_pain", "shortness_of_breath", "palpitations"],
        "secondary": ["cold_hands_feet", "dizziness", "sweating", "nausea"]
    },
    "Stroke (TIA Warning)": {
        "primary": ["numbness_one_side", "slurred_speech", "confusion"],
        "secondary": ["dizziness", "throbbing_headache", "blurred_vision"]
    },
    "Chronic Kidney Disease": {
        "primary": ["swollen_legs_ankles", "frequent_urination", "fatigue", "dark_urine"],
        "secondary": ["shortness_of_breath", "nausea", "loss_of_appetite", "itching"]
    },
    "Anemia": {
        "primary": ["fatigue", "weakness", "cold_hands_feet"],
        "secondary": ["dizziness", "shortness_of_breath", "palpitations", "headache"]
    },
    "Hypothyroidism": {
        "primary": ["unexplained_weight_gain", "fatigue", "cold_sensitivity", "dry_skin"],
        "secondary": ["muscle_weakness", "joint_stiffness", "body_ache"]
    },
    "Hyperthyroidism": {
        "primary": ["unexplained_weight_loss", "rapid_heartbeat", "palpitations", "heat_sensitivity", "tremors"],
        "secondary": ["sweating", "increased_hunger", "fatigue"]
    },
    "Migraine": {
        "primary": ["throbbing_headache", "headache", "nausea", "blurred_vision"],
        "secondary": ["vomiting", "fatigue", "dizziness"]
    },
    "GERD (Acid Reflux)": {
        "primary": ["heartburn", "acid_regurgitation", "burning_stomach_pain"],
        "secondary": ["chest_pain", "cough", "sore_throat", "nausea"]
    },
    "Peptic Ulcer": {
        "primary": ["burning_stomach_pain", "stomach_pain", "heartburn"],
        "secondary": ["nausea", "vomiting", "loss_of_appetite", "unexplained_weight_loss"]
    },
    "Urinary Tract Infection": {
        "primary": ["burning_urination", "frequent_urination", "stomach_pain"],
        "secondary": ["dark_urine", "fever", "fatigue"]
    },

    # 4. Dermatological & Allergic
    "Allergic Rhinitis": {
        "primary": ["sneezing", "runny_nose", "itchy_eyes", "itching"],
        "secondary": ["sore_throat", "headache", "fatigue"]
    },
    "Food Allergy": {
        "primary": ["itching", "rash", "stomach_pain", "vomiting"],
        "secondary": ["nausea", "diarrhea", "shortness_of_breath"]
    },
    "Eczema": {
        "primary": ["itching", "dry_skin", "skin_redness", "rash"],
        "secondary": ["blisters", "body_ache"]
    },
    "Psoriasis": {
        "primary": ["silvery_scales", "skin_redness", "dry_skin", "itching"],
        "secondary": ["joint_pain", "joint_stiffness"]
    },
    "Acne Vulgaris": {
        "primary": ["acne_pimples", "skin_redness"],
        "secondary": ["dry_skin", "itching"]
    }
}

print(f"Total diseases configured: {len(disease_symptoms)}")
print(f"Total symptoms tracked: {len(symptoms_list)}")

# Generate balanced synthetic medical dataset (200 clinical profiles per disease = 6,800 records)
np.random.seed(42)
data = []
target = []

for disease, profile in disease_symptoms.items():
    primary_syms = profile["primary"]
    secondary_syms = profile.get("secondary", [])
    
    for _ in range(200):
        sample = {symptom: 0 for symptom in symptoms_list}
        
        # Primary symptoms present with 85-98% probability
        for sym in primary_syms:
            if sym in symptoms_list and np.random.rand() > 0.08:
                sample[sym] = 1
                
        # Secondary symptoms present with 40-75% probability
        for sym in secondary_syms:
            if sym in symptoms_list and np.random.rand() > 0.40:
                sample[sym] = 1
                
        # Minimal background noise (0.8% chance) to simulate clinical reality
        for sym in symptoms_list:
            if sym not in primary_syms and sym not in secondary_syms and np.random.rand() < 0.008:
                sample[sym] = 1
                
        data.append(sample)
        target.append(disease)

df = pd.DataFrame(data)
df['disease'] = target

# Save dataset to CSV for transparent reference and evaluation
csv_path = "medical_symptoms_dataset.csv"
df.to_csv(csv_path, index=False)
print(f"Saved medical dataset to {csv_path} (Shape: {df.shape})")

# Train symptom classifier
X = df.drop(columns=['disease'])
y = df['disease']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
symptom_model = RandomForestClassifier(n_estimators=150, max_depth=None, random_state=42)
symptom_model.fit(X_train, y_train)

# Check accuracy metrics
train_acc = symptom_model.score(X_train, y_train)
test_acc = symptom_model.score(X_test, y_test)
print(f"Symptom Model Trained. Train Acc: {train_acc:.2%}, Test Acc: {test_acc:.2%}")

# Save symptom model and symptoms list
with open("models/symptom_model.pkl", "wb") as f:
    pickle.dump(symptom_model, f)
with open("models/symptoms_list.pkl", "wb") as f:
    pickle.dump(symptoms_list, f)
print("Saved models/symptom_model.pkl and models/symptoms_list.pkl")


# ==========================================
# PART 2: SKIN IMAGE CLASSIFIER MODEL
# ==========================================
print("\nGenerating synthetic skin images for image classification...")

def extract_image_features(img):
    img_rgb = img.convert("RGB")
    arr_rgb = np.array(img_rgb)
    
    # RGB stats
    r, g, b = arr_rgb[:,:,0], arr_rgb[:,:,1], arr_rgb[:,:,2]
    features = [
        np.mean(r), np.std(r),
        np.mean(g), np.std(g),
        np.mean(b), np.std(b)
    ]
    
    # HSV stats
    img_hsv = img.convert("HSV")
    arr_hsv = np.array(img_hsv)
    h, s, v = arr_hsv[:,:,0], arr_hsv[:,:,1], arr_hsv[:,:,2]
    features.extend([
        np.mean(h), np.std(h),
        np.mean(s), np.std(s),
        np.mean(v), np.std(v)
    ])
    
    # Gradient/Texture stats
    gray = np.mean(arr_rgb, axis=2)
    dy, dx = np.gradient(gray)
    grad_mag = np.sqrt(dx**2 + dy**2)
    features.extend([
        np.mean(grad_mag), np.std(grad_mag)
    ])
    
    return features

categories = ["Healthy Skin", "Skin Rash", "Acne", "Eczema"]
skin_tones = [
    (240, 200, 175), # Light
    (210, 160, 125), # Medium/Tan
    (140, 95, 65),   # Dark
    (255, 220, 195)  # Fair
]

image_data = []
image_labels = []

for cat in categories:
    print(f"Generating training data for: {cat}...")
    for i in range(50):
        base_color = skin_tones[np.random.choice(len(skin_tones))]
        arr = np.zeros((128, 128, 3), dtype=np.uint8)
        for ch in range(3):
            arr[:, :, ch] = np.clip(base_color[ch] + np.random.normal(0, 3, (128, 128)), 0, 255)
            
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        
        if cat == "Skin Rash":
            for _ in range(np.random.randint(4, 9)):
                cx, cy = np.random.randint(20, 108), np.random.randint(20, 108)
                r = np.random.randint(10, 25)
                red_patch = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                draw_patch = ImageDraw.Draw(red_patch)
                draw_patch.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(220, 50, 50, np.random.randint(60, 150)))
                img = Image.alpha_composite(img.convert("RGBA"), red_patch).convert("RGB")
                draw = ImageDraw.Draw(img)
                
        elif cat == "Acne":
            for _ in range(np.random.randint(8, 15)):
                cx, cy = np.random.randint(15, 113), np.random.randint(15, 113)
                r = np.random.randint(2, 5)
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(200, 40, 40))
                if np.random.rand() > 0.4:
                    draw.ellipse([cx-1, cy-1, cx+1, cy+1], fill=(255, 245, 200))
                    
        elif cat == "Eczema":
            for _ in range(np.random.randint(3, 7)):
                cx, cy = np.random.randint(20, 108), np.random.randint(20, 108)
                rx, ry = np.random.randint(8, 20), np.random.randint(8, 20)
                points = []
                for angle in range(0, 360, 45):
                    rad = np.radians(angle)
                    dist_x = rx + np.random.randint(-4, 4)
                    dist_y = ry + np.random.randint(-4, 4)
                    points.append((cx + dist_x * np.cos(rad), cy + dist_y * np.sin(rad)))
                
                patch = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                draw_patch = ImageDraw.Draw(patch)
                draw_patch.polygon(points, fill=(160, 90, 70, np.random.randint(100, 180)))
                img = Image.alpha_composite(img.convert("RGBA"), patch).convert("RGB")
                draw = ImageDraw.Draw(img)
                
        if i == 0:
            filename = f"static/assets/sample_images/{cat.lower().replace(' ', '_')}.png"
            img.save(filename)
            print(f"Saved sample image: {filename}")
            
        features = extract_image_features(img)
        image_data.append(features)
        image_labels.append(cat)

X_img = np.array(image_data)
y_img = np.array(image_labels)

X_img_train, X_img_test, y_img_train, y_img_test = train_test_split(X_img, y_img, test_size=0.2, random_state=42)
image_model = RandomForestClassifier(n_estimators=50, random_state=42)
image_model.fit(X_img_train, y_img_train)

img_train_acc = image_model.score(X_img_train, y_img_train)
img_test_acc = image_model.score(X_img_test, y_img_test)
print(f"Image model trained. Train Acc: {img_train_acc:.2%}, Test Acc: {img_test_acc:.2%}")

with open("models/image_model.pkl", "wb") as f:
    pickle.dump(image_model, f)

print("\nModel training workflow complete. All models saved in ./models")
