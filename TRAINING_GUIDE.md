# 🎓 TRAINING GUIDE - Improve Model Accuracy

## 🎯 Why Your AI Voice Shows as HUMAN

**Current Issue:** The model uses **synthetic/demo training data**, not real voices.

**Solution:** Train with **real audio samples**!

---

## 📚 Quick Training Steps

### **Step 1: Collect Voice Samples** 🎤

I've created folders for you:
```
training_data/
├── human/     ← Put HUMAN voice MP3s here
└── ai/        ← Put AI-GENERATED voice MP3s here
```

**You need:**
- **Minimum:** 20-50 files per category
- **Recommended:** 100+ files per category
- **Best:** 500+ files per category

---

### **Step 2: Get Human Voices** 👤

#### Option 1: Record Yourself & Friends/Family
```
1. Use Windows Voice Recorder
2. Record different people speaking
3. Save each as separate MP3
4. Copy to: training_data/human/
```

**Tips:**
- Different people (male, female, young, old)
- Different languages (Tamil, English, Hindi, etc.)
- Different speaking styles (fast, slow, emotional, neutral)
- 10-30 seconds each

#### Option 2: Download Human Voice Datasets
- **LibriVox:** https://librivox.org/ (free audiobooks)
- **Common Voice:** https://commonvoice.mozilla.org/
- **YouTube:** Download speeches, interviews (with permission)

**Extract audio and save as MP3 in `training_data/human/`**

---

### **Step 3: Get AI-Generated Voices** 🤖

#### Generate AI Voices from Multiple TTS Systems:

**1. TTSMaker** (Free, Easy)
- Visit: https://ttsmaker.com/
- Type different texts
- Try different voices
- Download as MP3
- Save to: `training_data/ai/`

**2. Google Cloud TTS**
- https://cloud.google.com/text-to-speech
- Multiple voices available
- Generate samples

**3. Natural Readers**
- https://www.naturalreaders.com/online/
- Free online TTS
- Different voice options

**4. Other TTS Tools:**
- ElevenLabs (if you have access)
- Amazon Polly
- Microsoft Azure TTS
- IBM Watson TTS

**Important:** Use **different TTS systems** to make the model robust!

---

### **Step 4: Organize Your Files** 📁

```
training_data/
├── human/
│   ├── person1_english.mp3
│   ├── person2_tamil.mp3
│   ├── person3_hindi.mp3
│   ├── recording1.mp3
│   ├── recording2.mp3
│   └── ... (50+ files)
└── ai/
    ├── ttsmaker_voice1.mp3
    ├── ttsmaker_voice2.mp3
    ├── google_tts_1.mp3
    ├── amazon_polly_1.mp3
    ├── azure_tts_1.mp3
    └── ... (50+ files)
```

**File Naming Tips:**
- Use descriptive names
- Include source (e.g., `google_`, `human_`, etc.)
- Keep it organized!

---

### **Step 5: Train the Model** 🧠

```bash
python train_model.py
```

**You'll see:**
```
📂 Loading HUMAN voices from: training_data/human
   ✅ 1. person1_english.mp3
   ✅ 2. person2_tamil.mp3
   ... (50 files)

📂 Loading AI voices from: training_data/ai
   ✅ 1. ttsmaker_voice1.mp3
   ✅ 2. google_tts_1.mp3
   ... (50 files)

🎯 Training Accuracy: 95.00%
🎯 Test Accuracy: 87.50%

✅ Model saved successfully!
```

---

### **Step 6: Test the Improved Model** ✅

```bash
# Restart the server to load the new model
Ctrl+C  # Stop the old server
python app.py

# Test your AI voice again
python test_with_audio.py
```

**Now it should correctly identify AI voices!** 🎉

---

## 📊 Expected Results

| Dataset Size | Expected Accuracy |
|-------------|------------------|
| 20-50 samples/class | 60-75% |
| 50-100 samples/class | 75-85% |
| 100-500 samples/class | 85-95% |
| 500+ samples/class | 90-98% |

---

## 🎯 Quick Start - Minimal Training (10 minutes)

### For Quick Testing:

**1. Record 10 human voices:**
```bash
# You, family, friends
# Save to: training_data/human/
```

**2. Generate 10 AI voices:**
```bash
# Visit ttsmaker.com
# Generate 10 different voices
# Save to: training_data/ai/
```

**3. Train:**
```bash
python train_model.py
```

**4. Test:**
```bash
python test_with_audio.py
```

Even with just 20 samples, you'll see improvement!

---

## 🚀 Comprehensive Training (Best Results)

### Goal: 200+ Total Samples

**Human Voices (100 files):**
- 20 recordings of yourself
- 20 recordings of friends/family
- 60 from LibriVox audiobooks (split into 30-second clips)

**AI Voices (100 files):**
- 30 from TTSMaker (different voices)
- 20 from Google TTS
- 20 from NaturalReaders
- 30 from other TTS systems

**Commands:**
```bash
# After collecting all files
python train_model.py
```

**Expected:** 85-95% accuracy! 🎉

---

## 💡 Pro Tips for Better Accuracy

### ✅ **Diversity is Key:**
- Different speakers (age, gender, accent)
- Different languages (Tamil, English, Hindi, etc.)
- Different TTS systems (Google, Amazon, Microsoft)
- Different speaking styles (news, conversation, reading)

### ✅ **Quality Matters:**
- Clear audio (no background noise)
- Good recording quality
- Proper MP3 format
- 10-30 seconds each

### ✅ **Balance Your Dataset:**
- Equal number of human and AI samples
- If you have 100 human, get 100 AI
- Imbalanced data = poor performance

### ✅ **Test Different TTS:**
Your AI voice might be from a specific TTS system. Make sure to include that system in training!

---

## 🔧 Troubleshooting

### Issue: "Accuracy is below 70%"

**Solutions:**
1. Add more training samples
2. Ensure audio quality is good
3. Balance human and AI samples
4. Use diverse TTS systems

### Issue: "Model still misclassifies"

**Check:**
1. Is your test AI voice from a TTS system NOT in training?
2. Add samples from that specific TTS
3. Retrain the model

### Issue: "Not enough data"

**Quick fix:**
- Download 50 audiobook clips from LibriVox
- Generate 50 voices from ttsmaker.com
- Train → Should improve immediately

---

## 📥 Quick Data Collection Script

I'll create a helper script for you:

```bash
# Run this to get started quickly
python quick_dataset_setup.py
```

*(This will guide you through collecting data)*

---

## 🎬 Complete Example Workflow

### Real-World Example:

**Day 1:** Collect data (2 hours)
- Record 30 human voices (yourself, family, friends)
- Download 30 LibriVox clips
- Generate 60 AI voices from ttsmaker.com

**Day 1:** Train model (5 minutes)
```bash
python train_model.py
```

**Day 1:** Test (2 minutes)
```bash
python test_with_audio.py
```

**Result:** 80-90% accuracy! ✅

---

## 📊 Training Output Example

```
======================================================================
📂 Loading HUMAN voices from: training_data/human
   Found 100 MP3 files
   ✅ 1. recording1.mp3
   ✅ 2. recording2.mp3
   ... (100 total)

📂 Loading AI voices from: training_data/ai
   Found 100 MP3 files
   ✅ 1. ttsmaker1.mp3
   ✅ 2. google_tts1.mp3
   ... (100 total)

======================================================================
📊 Dataset Summary
======================================================================
👤 Human voices: 100
🤖 AI voices: 100
📦 Total samples: 200

======================================================================
🧠 Training the Model
======================================================================
📊 Data Split:
   Training samples: 160
   Test samples: 40

⏳ Training Random Forest classifier...

======================================================================
✅ Training Complete!
======================================================================
🎯 Training Accuracy: 96.25%
🎯 Test Accuracy: 87.50%

📊 Detailed Performance Report:
======================================================================
              precision    recall  f1-score   support

       HUMAN       0.85      0.90      0.87        20
AI_GENERATED       0.90      0.85      0.87        20

    accuracy                           0.88        40

💪 Average Confidence: 91.23%

💾 Saving trained model...
✅ Model saved successfully!

🎉 Excellent! Model is performing well!
✅ Ready for production use
```

---

## 🎯 Summary - What You Need to Do

```
1. Collect 50-100 HUMAN voice MP3s
   ↓
2. Collect 50-100 AI voice MP3s
   ↓
3. Put them in the correct folders
   ↓
4. Run: python train_model.py
   ↓
5. Restart server: python app.py
   ↓
6. Test: python test_with_audio.py
   ↓
7. ✅ Accurate results!
```

---

## 📞 Need Help?

**Quick Resources:**
- **Human voices:** https://librivox.org/
- **AI voices:** https://ttsmaker.com/
- **Training script:** `python train_model.py`
- **This guide:** `TRAINING_GUIDE.md`

---

**🎓 Ready to train? Collect your audio files and run: `python train_model.py`**
