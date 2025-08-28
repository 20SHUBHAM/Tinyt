# Performance Optimization Guide

## Why Persona Generation Takes Time

The persona generation step can take 30-60 seconds because:

1. **Complex AI Processing**: Creating detailed, realistic personas requires significant LLM computation
2. **Model Choice**: GPT-4 is more thorough but slower than GPT-3.5-turbo
3. **Detailed Prompts**: Rich persona profiles require more processing time
4. **Network Latency**: API calls to OpenAI/Anthropic servers introduce delays

## Quick Fixes (Immediate)

### 1. Use Quick Mode
- ✅ **Enable Quick Mode checkbox** in the persona generation step
- ⚡ Reduces generation time from 60s to ~15s
- 📝 Provides basic but functional personas

### 2. Switch to Faster Models
Edit your `.env` file:
```env
# Faster models (recommended)
OPENAI_MODEL=gpt-3.5-turbo
ANTHROPIC_MODEL=claude-3-haiku-20240307

# Slower but higher quality
# OPENAI_MODEL=gpt-4
# ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### 3. Reduce Persona Count
- Start with 4-5 personas instead of 6-8
- You can always generate more later

### 4. Use Simpler Descriptions
- Keep audience descriptions concise (1-2 sentences)
- Avoid overly complex requirements

## Advanced Optimizations

### 1. Local LLM Setup (Future)
```bash
# Install local LLM (if available)
pip install ollama
# Use local models for faster response
```

### 2. Caching Strategy
```env
# Enable caching for repeated requests
TINYTROUPE_CACHE_DIR=./cache
```

### 3. Parallel Processing
```python
# Future enhancement: parallel persona generation
# Generate multiple personas simultaneously
```

## Expected Performance Benchmarks

| Mode | Model | Personas | Time | Quality |
|------|-------|----------|------|---------|
| Quick | GPT-3.5-turbo | 4 | ~10-15s | Basic |
| Quick | GPT-3.5-turbo | 6 | ~15-20s | Basic |
| Detailed | GPT-3.5-turbo | 4 | ~20-30s | High |
| Detailed | GPT-3.5-turbo | 6 | ~30-45s | High |
| Detailed | GPT-4 | 6 | ~45-60s | Highest |

## Troubleshooting Slow Performance

### If Generation Takes > 2 Minutes:
1. **Check Internet Connection**
   ```bash
   ping api.openai.com
   ```

2. **Verify API Key**
   ```bash
   echo $OPENAI_API_KEY
   ```

3. **Check API Limits**
   - Ensure you have available API quota
   - Check OpenAI/Anthropic dashboard for rate limits

4. **Restart Application**
   ```bash
   python run.py
   ```

### If Generation Fails:
1. **Check Logs**
   ```bash
   tail -f logs/app.log
   ```

2. **Test API Connection**
   ```python
   # Test script
   import openai
   client = openai.OpenAI(api_key="your-key")
   response = client.chat.completions.create(
       model="gpt-3.5-turbo",
       messages=[{"role": "user", "content": "Hello"}],
       max_tokens=10
   )
   print(response.choices[0].message.content)
   ```

3. **Use Fallback Mode**
   - Application automatically provides fallback personas if generation fails
   - These are basic but functional for testing

## Network Optimization

### For Slow Connections:
```env
# Reduce timeout if needed
LLM_TIMEOUT=30

# Use smaller models
OPENAI_MODEL=gpt-3.5-turbo
```

### For Corporate Networks:
```bash
# Configure proxy if needed
export https_proxy=http://your-proxy:port
export http_proxy=http://your-proxy:port
```

## Monitoring Performance

### Add Performance Logging:
```python
import time
start_time = time.time()
# ... persona generation ...
duration = time.time() - start_time
print(f"Generation took {duration:.2f} seconds")
```

### Track API Usage:
- Monitor OpenAI usage dashboard
- Set up billing alerts
- Track token consumption

## Production Optimizations

### 1. Use CDN for Static Assets
```nginx
# Nginx configuration
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 2. Enable Compression
```python
# Flask configuration
from flask_compress import Compress
Compress(app)
```

### 3. Database Caching
```python
# Redis caching for sessions
import redis
r = redis.Redis(host='localhost', port=6379)
```

### 4. Load Balancing
```yaml
# Docker compose with multiple workers
version: '3.8'
services:
  web:
    build: .
    scale: 3
    environment:
      - WORKERS=1
```

## Alternative Solutions

### 1. Pre-generated Persona Libraries
- Create libraries of common personas
- Mix and match for faster setup
- Customize as needed

### 2. Progressive Loading
- Generate 2 personas quickly
- Add more in background
- Show progress indicators

### 3. Async Processing
- Queue persona generation
- Show progress updates
- Allow other steps while processing

## Cost Optimization

### 1. Model Selection by Use Case
```env
# For development/testing
OPENAI_MODEL=gpt-3.5-turbo

# For production/important research
OPENAI_MODEL=gpt-4
```

### 2. Token Management
- Optimize prompt length
- Use precise instructions
- Cache common responses

### 3. Request Batching
- Generate multiple personas in single request
- Reduce API call overhead

## Quick Start Performance Setup

1. **Copy optimized environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

2. **Use recommended settings**:
   ```env
   OPENAI_MODEL=gpt-3.5-turbo
   DEFAULT_LLM_PROVIDER=openai
   ```

3. **Start with Quick Mode**:
   - Check "Quick Mode" for first test
   - Use 4-5 personas initially
   - Upgrade to detailed mode once familiar

4. **Monitor Performance**:
   - Check browser dev tools for timing
   - Monitor API usage on provider dashboard
   - Adjust settings based on needs

---

**⚡ With these optimizations, persona generation should complete in 15-30 seconds instead of 60+ seconds!**