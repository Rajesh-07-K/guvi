# Render Deployment Fixes

## Problem
Build was failing with error:
```
pip._vendor.pyproject_hooks._impl.BackendUnavailable: Cannot import 'setuptools.build_meta'
```

## Root Cause
- Render's Python environment doesn't have updated `setuptools` and `wheel` packages
- Packages like `librosa` and `scipy` require these build tools to compile binary extensions
- The default pip version might be outdated

## Solutions Implemented

### 1. Updated `requirements.txt`
Added build dependencies at the top:
```txt
# Build dependencies (required first)
setuptools>=65.0.0
wheel>=0.40.0
```

### 2. Updated `render.yaml`
Modified build command to upgrade pip/setuptools/wheel BEFORE installing other packages:
```yaml
buildCommand: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
```

### 3. Created `build.sh` (Alternative)
A dedicated build script that can be used instead:
```bash
#!/usr/bin/env bash
set -o errexit
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
pip install -r requirements.txt
```

## How to Deploy

### Option 1: Using render.yaml (Recommended)
1. Changes are already committed and pushed
2. Go to your Render dashboard
3. Click "Manual Deploy" or wait for auto-deploy
4. Build should succeed now

### Option 2: Using Render Web Dashboard
If you're configuring through the Render web interface:

1. **Build Command:**
   ```bash
   pip install --upgrade pip setuptools wheel && pip install -r requirements.txt
   ```

2. **Start Command:**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables:**
   - `PYTHON_VERSION`: 3.11.0
   - `API_KEY`: (your API key)

## Verification

After deployment succeeds, test with:

```bash
curl https://your-app.onrender.com/health
```

Should return:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
}
```

## Common Issues & Solutions

### If build still fails:

1. **Clear Render's build cache:**
   - In Render dashboard → Settings → Clear build cache
   - Then trigger manual deploy

2. **Check Python version:**
   - Make sure `PYTHON_VERSION` is set to `3.11.0` or `3.10.x`
   - Some packages don't support Python 3.12+ yet

3. **Memory issues:**
   - Render free tier has memory limits
   - If build fails due to memory, you may need to upgrade plan

4. **System dependencies:**
   - Render's Python environment includes most common libraries
   - If errors mention missing system packages, you may need Docker deployment

## Alternative: Deploy with Docker

If issues persist, create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Run
CMD uvicorn app:app --host 0.0.0.0 --port $PORT
```

Then update render.yaml to use Docker:
```yaml
services:
  - type: web
    name: guvi-ai-voice-detection
    env: docker
    dockerfilePath: ./Dockerfile
```

## Next Steps

1. ✅ Changes committed and pushed
2. ⏳ Monitor Render build logs
3. ✅ Test /health endpoint after deployment
4. ✅ Test API with sample request

## Support Links

- Render Python Docs: https://render.com/docs/deploy-fastapi
- Render Build Issues: https://render.com/docs/troubleshooting-builds
