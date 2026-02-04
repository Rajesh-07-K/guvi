# 🎤 SIMPLE USAGE GUIDE - AI Voice Detection API

## ⚡ Super Quick Start (Copy & Paste These Commands)

### **Step 1:** Open Terminal and Start Server
```bash
cd r:\Project\Guvi
python app.py
```
✅ **Wait for:** "Uvicorn running on http://0.0.0.0:8000"

---

### **Step 2:** Get Your MP3 Voice File

**Choose ONE of these options:**

#### Option A: Record on Windows (Built-in App)
1. Press `Windows Key` → Type **"Voice Recorder"** → Open it
2. Click the **Red microphone button** to record
3. Speak anything: *"Hello, this is a test"*
4. Click **Stop** (square icon)
5. Right-click recording → **"Open file location"**
6. **Copy** the file to: `r:\Project\Guvi\sample.mp3`

#### Option B: Use Your Phone
1. Record voice on your phone
2. Transfer to computer via USB/Bluetooth/Email
3. Save as: `r:\Project\Guvi\sample.mp3`

#### Option C: Download Test Audio
- Visit: https://ttsmaker.com/
- Type any text
- Click "Convert to Speech"
- Download as MP3
- Save as: `r:\Project\Guvi\sample.mp3`

---

### **Step 3:** Test the API

**Open a NEW terminal** (keep server running):
```bash
cd r:\Project\Guvi
python test_with_audio.py
```

**That's it!** You'll see:
```
✅ Classification: HUMAN
📊 Confidence: 87.35%
💬 Explanation: Natural variations in pitch confirm human speech
```

---

## 📋 Complete Example

Here's a **complete real-world example**:

### Scenario: Compare Human vs AI Voice

**1. Start the server:**
```bash
python app.py
```

**2. Record YOUR voice:**
- Record yourself saying: "This is my natural voice"
- Save as: `human.mp3`

**3. Generate AI voice:**
- Go to: https://ttsmaker.com/
- Type: "This is my natural voice"
- Download as: `ai.mp3`

**4. Test HUMAN voice:**
```bash
python test_with_audio.py english human.mp3
```
**Expected:** `Classification: HUMAN`

**5. Test AI voice:**
```bash
python test_with_audio.py english ai.mp3
```
**Expected:** `Classification: AI_GENERATED`

---

## 🎯 Different Languages Example

### Test Tamil Voice:
```bash
python test_with_audio.py tamil my_tamil_audio.mp3
```

### Test Hindi Voice:
```bash
python test_with_audio.py hindi my_hindi_audio.mp3
```

### Test Malayalam Voice:
```bash
python test_with_audio.py malayalam my_malayalam_audio.mp3
```

### Test Telugu Voice:
```bash
python test_with_audio.py telugu my_telugu_audio.mp3
```

---

## 🛠️ Interactive PowerShell Method (Windows)

For even easier testing:

```powershell
# Run this interactive script
.\convert_and_test.ps1
```

It will ask you:
1. Which MP3 file?
2. Which language?
3. Test the API now?

**Just answer the prompts!**

---

## 📱 How to Get Voice Files

### **Method 1: Record Yourself (EASIEST)**

**Windows:**
```
Windows Key → "Voice Recorder" → Record → Stop → Save
```

**Mac:**
```
Applications → QuickTime Player → File → New Audio Recording
```

**Phone:**
```
Voice Recorder app → Record → Share to computer
```

---

### **Method 2: Generate AI Voices**

**Free TTS Tools:**
- https://ttsmaker.com/ ← **EASIEST**
- https://naturalreaders.com/
- https://www.text2speech.org/

**Steps:**
1. Type your text
2. Select language
3. Click "Convert"
4. Download MP3

---

### **Method 3: Download Sample Audio**

**Human Voice Samples:**
- LibriVox (audiobooks): https://librivox.org/
- Common Voice: https://commonvoice.mozilla.org/

**AI Voice Samples:**
- Generate from any TTS tool above

---

## 🔍 Understanding the Results

### **AI_GENERATED Result:**
```json
{
  "classification": "AI_GENERATED",
  "confidenceScore": 0.91,
  "explanation": "High consistency in pitch patterns typical of synthetic voices"
}
```
**Means:** The voice was likely created by a computer/TTS system

---

### **HUMAN Result:**
```json
{
  "classification": "HUMAN", 
  "confidenceScore": 0.85,
  "explanation": "Natural variations in pitch and energy confirm human speech"
}
```
**Means:** The voice was likely spoken by a real person

---

## ❓ Common Questions

### Q: What audio format is supported?
**A:** Only MP3

### Q: How long should the audio be?
**A:** 5-30 seconds works best

### Q: Can I test WAV or M4A files?
**A:** No, convert to MP3 first using:
- https://cloudconvert.com/
- Or Windows Media Player (Save As → MP3)

### Q: The server isn't starting?
**A:** Install dependencies first:
```bash
pip install -r requirements.txt
```

### Q: File not found error?
**A:** Make sure the MP3 file is in `r:\Project\Guvi\` folder

### Q: How accurate is it?
**A:** Demo model: ~65%  
Real model (with training): >85%

---

## 🎬 Quick Video Tutorial Script

**If you want to demo this:**

1. **Start:** `python app.py` → Show "Server running"
2. **Record:** Open Voice Recorder → Say "Hello" → Save as sample.mp3
3. **Test:** `python test_with_audio.py` → Show result
4. **AI Voice:** Go to ttsmaker.com → Generate → Download
5. **Compare:** Test AI voice → Show different result

**Done in 2 minutes!**

---

## 📊 File Size Guide

| Audio Length | File Size | Status |
|-------------|-----------|--------|
| 5 seconds | ~50 KB | ✅ Good |
| 10 seconds | ~100 KB | ✅ Perfect |
| 30 seconds | ~300 KB | ✅ Ideal |
| 60 seconds | ~600 KB | ✅ OK |
| 5+ minutes | 3+ MB | ⚠️ Works but slow |

**Recommended:** 10-30 seconds of audio

---

## 🚀 Advanced Usage

### Test Multiple Files at Once:
```python
# test_multiple.py
files = ["human1.mp3", "ai1.mp3", "human2.mp3"]
for file in files:
    os.system(f"python test_with_audio.py english {file}")
```

### Batch Testing:
```bash
# Windows
for %f in (*.mp3) do python test_with_audio.py english %f
```

---

## 💡 Pro Tips

✅ **Clear audio** = Better results  
✅ **No background noise** = More accurate  
✅ **Single speaker** = Works best  
✅ **Proper language selection** = Important  
✅ **Test both human and AI** = See the difference  

---

## 🎯 Summary - Three Simple Steps

```
┌─────────────────────────────────────────┐
│  Step 1: python app.py                  │  ← Start server
├─────────────────────────────────────────┤
│  Step 2: Get sample.mp3                 │  ← Record or download
├─────────────────────────────────────────┤
│  Step 3: python test_with_audio.py      │  ← Test!
└─────────────────────────────────────────┘
```

**That's all you need!** 🎤

---

## 📞 Need Help?

1. Read: `HOW_TO_RUN.md` (this file)
2. Read: `DOCUMENTATION.md` (detailed technical guide)
3. Read: `QUICK_REFERENCE.md` (quick commands)

---

**🎤 Ready? Start with:** `python app.py`
