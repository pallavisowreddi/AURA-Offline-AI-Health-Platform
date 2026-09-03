import os
import pickle
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from PIL import Image, ImageDraw

# Ensure model directory exists
os.makedirs("models", exist_ok=True)
os.makedirs("static/assets/sample_images", exist_ok=True)

# ==========================================
# PART 1: SYMPTOM TO DISEASE PREDICTION MODEL
# ==========================================
print("Generating symptom-to-disease dataset...")

# Define symptoms and disease rules
symptoms_list = [
    "fever", "cough", "fatigue", "headache", "sore_throat", "body_ache", 
    "runny_nose", "shortness_of_breath", "loss_of_taste_smell", "nausea", 
    "vomiting", "diarrhea", "stomach_pain", "rash", "itching", "dry_skin", 
    "skin_redness", "blisters", "joint_pain", "muscle_weakness", "chills", 
    "sweating", "sneezing", "itchy_eyes"
]

disease_symptoms = {
    "Common Cold": ["cough", "runny_nose", "sore_throat", "sneezing", "fatigue"],
    "Influenza": ["fever", "body_ache", "chills", "headache", "fatigue", "cough", "sore_throat"],
    "Covid-19": ["fever", "cough", "fatigue", "shortness_of_breath", "loss_of_taste_smell", "body_ache"],
    "Gastroenteritis": ["nausea", "vomiting", "diarrhea", "stomach_pain", "fatigue"],
    "Allergic Rhinitis": ["sneezing", "runny_nose", "itchy_eyes", "itching"],
    "Dengue Fever": ["fever", "headache", "joint_pain", "rash", "nausea", "fatigue"],
    "Malaria": ["fever", "chills", "sweating", "headache", "nausea", "body_ache"],
    "Chickenpox": ["fever", "fatigue", "rash", "itching", "blisters"],
    "Eczema": ["itching", "dry_skin", "skin_redness", "rash"],
    "Food Allergy": ["nausea", "stomach_pain", "rash", "vomiting", "itching"],
    "Migraine": ["headache", "nausea", "fatigue"]
}

# Generate synthetic dataset
np.random.seed(42)
data = []
target = []

for disease, key_symptoms in disease_symptoms.items():
    # Create 100 samples per disease
    for _ in range(100):
        sample = {symptom: 0 for symptom in symptoms_list}
        
        # Primary symptoms are present most of the time (70% - 100% chance)
        for sym in key_symptoms:
            if np.random.rand() > 0.15:
                sample[sym] = 1
                
        # Random noise: other symptoms present rarely (5% chance)
        for sym in symptoms_list:
            if sym not in key_symptoms and np.random.rand() < 0.05:
                sample[sym] = 1
                
        data.append(sample)
        target.append(disease)

df = pd.DataFrame(data)
df['disease'] = target

# Train symptom classifier
X = df.drop(columns=['disease'])
y = df['disease']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
symptom_model = RandomForestClassifier(n_estimators=100, random_state=42)
symptom_model.fit(X_train, y_train)

# Check accuracy
train_acc = symptom_model.score(X_train, y_train)
test_acc = symptom_model.score(X_test, y_test)
print(f"Symptom model trained. Train Acc: {train_acc:.2%}, Test Acc: {test_acc:.2%}")

# Save symptom model and columns
with open("models/symptom_model.pkl", "wb") as f:
    pickle.dump(symptom_model, f)
with open("models/symptoms_list.pkl", "wb") as f:
    pickle.dump(symptoms_list, f)


# ==========================================
# PART 2: SKIN IMAGE CLASSIFIER MODEL
# ==========================================
print("\nGenerating synthetic skin images for image classification...")

# We will extract 14 features from each image:
# - Mean & Std of R, G, B channels (6 features)
# - Mean & Std of H, S, V channels (6 features)
# - Mean & Std of image gradient magnitude (2 features)

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
    
    # Gradient/Texture stats (using simple differences for edges)
    gray = np.mean(arr_rgb, axis=2)
    dy, dx = np.gradient(gray)
    grad_mag = np.sqrt(dx**2 + dy**2)
    features.extend([
        np.mean(grad_mag), np.std(grad_mag)
    ])
    
    return features

# Categories for skin conditions
categories = ["Healthy Skin", "Skin Rash", "Acne", "Eczema"]

# Base skin tone configurations (mix of light, medium, dark skin tones)
skin_tones = [
    (240, 200, 175), # Light
    (210, 160, 125), # Medium/Tan
    (140, 95, 65),   # Dark
    (255, 220, 195)  # Fair
]

image_data = []
image_labels = []

# Generate synthetic images and extract features
for cat in categories:
    print(f"Generating training data for: {cat}...")
    for i in range(50):
        # Create base canvas (128x128)
        base_color = skin_tones[np.random.choice(len(skin_tones))]
        # Add subtle skin texture noise
        arr = np.zeros((128, 128, 3), dtype=np.uint8)
        for ch in range(3):
            arr[:, :, ch] = np.clip(base_color[ch] + np.random.normal(0, 3, (128, 128)), 0, 255)
            
        img = Image.fromarray(arr)
        draw = ImageDraw.Draw(img)
        
        if cat == "Skin Rash":
            # Draw red patches
            for _ in range(np.random.randint(4, 9)):
                cx, cy = np.random.randint(20, 108), np.random.randint(20, 108)
                r = np.random.randint(10, 25)
                # Soft red blend
                red_patch = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                draw_patch = ImageDraw.Draw(red_patch)
                draw_patch.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(220, 50, 50, np.random.randint(60, 150)))
                img = Image.alpha_composite(img.convert("RGBA"), red_patch).convert("RGB")
                draw = ImageDraw.Draw(img)
                
        elif cat == "Acne":
            # Draw distinct small red/yellow pimples
            for _ in range(np.random.randint(8, 15)):
                cx, cy = np.random.randint(15, 113), np.random.randint(15, 113)
                r = np.random.randint(2, 5)
                # Outer red halo
                draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(200, 40, 40))
                # Inner white/yellow head
                if np.random.rand() > 0.4:
                    draw.ellipse([cx-1, cy-1, cx+1, cy+1], fill=(255, 245, 200))
                    
        elif cat == "Eczema":
            # Draw patchy, rough, dry spots (brownish/grayish/red dry patches)
            for _ in range(np.random.randint(3, 7)):
                cx, cy = np.random.randint(20, 108), np.random.randint(20, 108)
                rx, ry = np.random.randint(8, 20), np.random.randint(8, 20)
                # Create a rough looking polygon
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
                
        # For "Healthy Skin", we do nothing (just keep base skin tone)
        
        # Save a sample image for the user to download/use in the UI
        if i == 0:
            filename = f"static/assets/sample_images/{cat.lower().replace(' ', '_')}.png"
            img.save(filename)
            print(f"Saved sample image: {filename}")
            
        features = extract_image_features(img)
        image_data.append(features)
        image_labels.append(cat)

# Train image classifier
X_img = np.array(image_data)
y_img = np.array(image_labels)

X_img_train, X_img_test, y_img_train, y_img_test = train_test_split(X_img, y_img, test_size=0.2, random_state=42)
image_model = RandomForestClassifier(n_estimators=50, random_state=42)
image_model.fit(X_img_train, y_img_train)

# Check accuracy
img_train_acc = image_model.score(X_img_train, y_img_train)
img_test_acc = image_model.score(X_img_test, y_img_test)
print(f"Image model trained. Train Acc: {img_train_acc:.2%}, Test Acc: {img_test_acc:.2%}")

# Save image classifier
with open("models/image_model.pkl", "wb") as f:
    pickle.dump(image_model, f)

print("\nModel training workflow complete. All models saved in ./models")
