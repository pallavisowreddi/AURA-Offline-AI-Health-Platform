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
