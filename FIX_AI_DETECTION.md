# TRAINING SOLUTION - Fix AI Voice Misclassification

## Problem
Your AI-generated voice was classified as HUMAN because the model uses **demo/synthetic data**.

## Solution
Train with **REAL voice samples!**

---

## Quick Training Steps

### 1. Folders are Ready
```
training_data/
├── human/   ← Add HUMAN voice MP3s here
└── ai/      ← Add AI voice MP3s here
```

### 2. Collect Voice Files

**Minimal (Quick Test - 20 files):**
- 10 human voices (record yourself, friends)
- 10 AI voices (visit ttsmaker.com and generate)

**Recommended (Better Results - 100 files):**
- 50 human voices (recordings + LibriVox audiobooks)
- 50 AI voices (ttsmaker.com + other TTS tools)

**Best (Production Quality - 200+ files):**
- 100+ human voices (diverse speakers, languages)
- 100+ AI voices (multiple TTS systems)

### 3. Generate AI Voices

**Easy Way - TTSMaker.com:**
1. Visit: https://ttsmaker.com/
2. Type text: "This is a test of AI voice generation"
3. Click "Convert to Speech"
4. Download MP3
5. Save to: `training_data/ai/`
6. Repeat 10-50 times with different texts/voices

**Other TTS Tools:**
- https://naturalreaders.com/online/
- https://www.text2speech.org/
- Google Cloud TTS (if you have account)

### 4. Get Human Voices

**Easy Way - Record Yourself:**
1. Windows Voice Recorder
2. Record 10-30 second clips
3. Different sentences, emotions
4. Save to: `training_data/human/`

**Download Free Audiobooks:**
1. Visit: https://librivox.org/
2. Download any audiobook MP3
3. Cut into 30-second clips
4. Save to: `training_data/human/`

### 5. Train the Model

```bash
python train_model.py
```

**You'll see:**
```
Loading HUMAN voices: 50 files
Loading AI voices: 50 files

Training...

Test Accuracy: 87.50%

Model saved successfully!
```

### 6. Test Again

```bash
# Restart server
Ctrl+C
python app.py

# Test your AI voice
python test_with_audio.py
```

**Now it will correctly identify AI voices!**

---

## Quick Commands

```bash
# Check folder structure and get instructions
python quick_dataset_setup.py

# After adding audio files, train
python train_model.py

# Restart server
python app.py

# Test
python test_with_audio.py
```

---

## Expected Results

| Training Samples | Accuracy |
|-----------------|----------|
| 20 total (10+10) | 65-75% |
| 100 total (50+50) | 80-90% |
| 200+ total (100+100) | 90-95% |

---

## Why This Works

AI voices have subtle patterns:
- Lower pitch variance (too smooth)
- Uniform energy (no natural breathing)
- Synthetic spectral artifacts

The model learns these differences from REAL examples, not synthetic data.

---

## What You Need To Do NOW

1. **Go to ttsmaker.com**
2. **Generate 10 AI voices** (different texts)
3. **Save to:** `training_data/ai/`
4. **Record yourself 10 times** (different sentences)
5. **Save to:** `training_data/human/`
6. **Run:** `python train_model.py`
7. **Test again!**

Even with just 20 samples you'll see improvement!

---

Read full guide: **TRAINING_GUIDE.md**
