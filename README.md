# AURA: Offline AI-Driven Public Health Chatbot

AURA (AI-Driven Public Health Assistant) is a premium, fully local, and offline machine learning application built for predictive disease awareness. It analyzes symptoms (text/voice) and skin conditions (visual images) using local classifiers, requiring **no WiFi, no internet connection, and no external API keys**.

## 🌟 Key Features
- **100% Offline Capability**: Runs entirely on your local machine using lightweight, fast-loading `scikit-learn` models.
- **Predictive Symptom Analysis**: Processes colloquial descriptions of symptoms using a rule-based NLP parser, then runs a Random Forest Classifier to identify potential conditions.
- **Visual Skin Analysis**: Extracts RGB/HSV channel metrics and spatial gradient variance (texture index) to predict conditions like Skin Rash, Acne, and Eczema.
- **Voice Assistance (Speech-to-Text & Text-to-Speech)**: Allows speaking to the chatbot via browser-native Speech Recognition, and reads out care instructions using the Web Speech Synthesis engine.
- **Interactive Telemetry Dashboard**: Displays real-time feature breakdowns, class probability distributions, and animated confidence gauges.
- **Premium Glassmorphic UI**: High-fidelity dark mode with neon accents, responsive layouts, hover zoom cards, and vertical micro-animation waves.

---

## 🛠️ Tech Stack & Architecture
1. **Backend**: Python (Flask)
2. **Predictive Analytics**: `scikit-learn` (Random Forest Classifiers), `numpy`, `pandas`
3. **Image Analytics**: `Pillow` (PIL) & `numpy` (for pixel parameter extraction)
4. **Voice Engines**: Browser Web Speech API (STT & TTS)
5. **Frontend**: HTML5, Vanilla CSS3 (Custom Glassmorphism), JavaScript (ES6)

---

## 📂 Project Structure
Open this project folder in **VS Code** to explore the codebase:
```text
health-assistant-chatbot/
├── models/                     # Directory for saved pickle models
│   ├── symptom_model.pkl       # Trained Random Forest symptom classifier
│   ├── symptoms_list.pkl       # Serialized list of symptom column headers
│   └── image_model.pkl         # Trained Random Forest skin classifier
├── static/
│   ├── css/
│   │   └── style.css           # Premium styling & transitions
│   ├── js/
│   │   └── app.js              # Speech recognition, canvas telemetry, API requests
│   └── assets/
│       └── sample_images/      # Synthetic training/testing skin condition photos
│           ├── healthy_skin.png
│           ├── skin_rash.png
│           ├── acne.png
│           └── eczema.png
├── templates/
│   └── index.html              # Main dashboard view
├── app.py                      # Flask backend API & routing
├── train_models.py             # Script to generate datasets and train ML models
├── model_helper.py             # Rule matching, preprocessing, and model inference
├── requirements.txt            # Python dependencies list
├── run.bat                     # Windows double-click setup & launch script
└── README.md                   # Project documentation (this file)
```

---

## 🚀 How to Run the App (Windows)

The simplest way to set up and run the app is using the provided automation script:

1. **Double-click the `run.bat` file** in the project directory.
2. The script will automatically:
   - Create a local virtual environment (`.venv`).
   - Upgrade `pip` and install all required libraries.
   - Run `train_models.py` to create the training data and save the models.
   - Start the Flask backend.
   - Open `http://127.0.0.1:5000/` in your default web browser.

### Manual Setup (Optional)
If you prefer to run the commands manually:
```bash
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate the virtual environment
.venv\Scripts\activate

# 3. Install requirements
pip install -r requirements.txt

# 4. Train the models
python train_models.py

# 5. Start the web server
python app.py
```

---

## 🧪 Verification & Testing Guide

Once the browser loads the dashboard, you can verify its offline functions using the built-in elements:

1. **Symptom Analytics**:
   - In the chat box, type: *"I am experiencing a high fever, body aches, a severe headache, and joint pain."*
   - Press **Send**.
   - Verify that **Dengue Fever** is predicted on the left telemetry panel, displaying the confidence rate and classification breakdown.
   - Try clicking one of the text sample buttons (e.g. `🧴 Eczema Symptoms` or `🤢 Stomach Infection`) to test other paths.

2. **Visual Image Analytics**:
   - Scroll to the **Sample Skin Images** section on the right side.
   - Click one of the cards (e.g., `Acne` or `Skin Rash`).
   - The app will fetch the image, generate a bubble in the chat, run the visual metrics on the backend, and return the predicted classification.
   - Observe the **Extracted Features** bar charts update with redness averages and roughness coefficients.

3. **Voice Assistance**:
   - Click the microphone button in the input bar.
   - Grant permission (if prompted) and say: *"I have dry itchy skin and dry patches."*
   - The text will transcribe into the box and automatically submit, returning the diagnosis.
   - Enable **Voice Assistance (TTS)** to hear the bot speak the response.
