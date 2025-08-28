# 🚀 Deployment Guide - Agentic Focus Group Platform

## Quick Start (5 minutes)

### Option 1: Replit (Recommended)
```bash
# 1. Fork/import this repository to Replit
# 2. Run the deployment script
./deploy_replit.sh

# 3. Set up environment variables in Replit Secrets:
#    - OPENAI_API_KEY or ANTHROPIC_API_KEY
#    - SECRET_KEY (generate a random string)

# 4. Click "Run" button
# 5. Access via the generated Replit URL
```

### Option 2: Local Development
```bash
# 1. Clone and setup
git clone <repository-url>
cd agentic-focus-group
cp .env.example .env

# 2. Edit .env with your API keys
# 3. Install and run
pip install -r requirements.txt
python run.py

# 4. Access at http://localhost:5000
```

## Complete Deployment Options

### 🔧 Replit Deployment

**Steps:**
1. Import this repository to Replit
2. Run `./deploy_replit.sh`
3. Configure Secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `SECRET_KEY`: Any random string (e.g., `abc123xyz789`)
4. Click "Run"
5. Share the generated URL

**Replit Secrets Configuration:**
```
OPENAI_API_KEY=sk-your-openai-key-here
SECRET_KEY=your-random-secret-key
DEFAULT_LLM_PROVIDER=openai
FLASK_ENV=production
```

### 🐳 Docker Deployment

**Single Container:**
```bash
# Build and run
docker build -t focus-group-platform .
docker run -p 5000:5000 --env-file .env focus-group-platform
```

**Docker Compose:**
```bash
# Configure .env file first
docker-compose up -d
```

### ☁️ Heroku Deployment

```bash
# Install Heroku CLI and login
heroku create your-app-name

# Set environment variables
heroku config:set OPENAI_API_KEY=your-key
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEFAULT_LLM_PROVIDER=openai

# Deploy
git push heroku main

# Open application
heroku open
```

### 🖥️ VPS/Server Deployment

**Ubuntu/Debian:**
```bash
# Install Python 3.11+
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# Clone and setup
git clone <repository-url>
cd agentic-focus-group
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run with gunicorn
gunicorn app:app --bind 0.0.0.0:5000 --workers 2
```

**With Nginx (Production):**
```nginx
# /etc/nginx/sites-available/focus-group
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Environment Configuration

### Required Variables
```env
# Security
SECRET_KEY=your-random-secret-key

# LLM Provider (choose one)
OPENAI_API_KEY=sk-your-openai-key
# OR
ANTHROPIC_API_KEY=your-anthropic-key
```

### Optional Variables
```env
# Application
FLASK_ENV=production
PORT=5000
DEFAULT_LLM_PROVIDER=openai

# Models
OPENAI_MODEL=gpt-4
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Session Management
SESSION_TIMEOUT=3600
MAX_SESSIONS=100

# TinyTroupe
TINYTROUPE_CACHE_DIR=./cache
TINYTROUPE_LOG_LEVEL=INFO
```

## Platform-Specific Instructions

### Replit
- Use Secrets for environment variables
- Files persist automatically
- URL is auto-generated
- No server management needed

### Heroku
- Use Config Vars for environment
- Ephemeral filesystem (sessions reset on restart)
- Custom domain available
- Automatic SSL

### Docker
- Mount volumes for data persistence
- Configure resource limits
- Use docker-compose for multi-service setup
- Consider container orchestration

### VPS/Cloud
- Setup reverse proxy (Nginx/Apache)
- Configure SSL certificates
- Setup process manager (systemd/supervisor)
- Monitor resource usage

## Testing Deployment

### 1. Run Setup Test
```bash
python test_setup.py
```

### 2. Manual Testing Checklist
- [ ] Application loads at correct URL
- [ ] All 5 steps are accessible
- [ ] Persona generation works
- [ ] Framework creation works
- [ ] Simulation runs successfully
- [ ] Summary generation works
- [ ] Q&A functionality works
- [ ] Export/download works

### 3. API Testing
```bash
# Test API endpoints
curl -X POST http://your-url/api/generate-personas \
  -H "Content-Type: application/json" \
  -d '{"description": "test users", "num_personas": 3}'
```

## Performance Optimization

### For High Traffic
- Use multiple workers: `gunicorn app:app --workers 4`
- Add Redis for session caching
- Configure CDN for static files
- Use application monitoring

### Resource Requirements
- **Minimum**: 512MB RAM, 1 CPU core
- **Recommended**: 2GB RAM, 2 CPU cores
- **Storage**: 1GB for application + cache

## Security Considerations

### Production Checklist
- [ ] Strong SECRET_KEY configured
- [ ] API keys stored securely
- [ ] HTTPS enabled
- [ ] Regular dependency updates
- [ ] Input validation enabled
- [ ] Error messages don't expose internals

### Environment Security
```bash
# Generate secure secret key
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Check file permissions
chmod 600 .env
```

## Monitoring & Maintenance

### Log Locations
- Application logs: `logs/app.log`
- Session data: `data/sessions.json`
- TinyTroupe cache: `cache/*.cache.json`

### Health Checks
```bash
# Check application health
curl http://your-url/

# Monitor resource usage
df -h        # Disk space
free -m      # Memory usage
top          # CPU usage
```

### Backup Strategy
```bash
# Backup session data
tar -czf backup-$(date +%Y%m%d).tar.gz data/ cache/ logs/

# Automate with cron
0 2 * * * /path/to/backup-script.sh
```

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Fix: Install dependencies
pip install -r requirements.txt
```

**2. API Key Errors**
```bash
# Fix: Check environment variables
echo $OPENAI_API_KEY
# Set in .env file or environment
```

**3. Port Already in Use**
```bash
# Fix: Change port or kill process
export PORT=5001
python run.py
```

**4. Permission Denied**
```bash
# Fix: Set proper permissions
chmod 755 run.py
mkdir -p data cache logs
```

**5. Memory Issues**
```bash
# Fix: Reduce personas or use smaller model
# In .env:
OPENAI_MODEL=gpt-3.5-turbo
```

### Debug Mode
```bash
# Enable debug logging
export FLASK_ENV=development
python run.py
```

### Support Resources
- Check `README.md` for detailed documentation
- Review `PROJECT_OVERVIEW.md` for architecture
- Run `python test_setup.py` for diagnostics
- Check logs in `logs/app.log`

## Success Checklist

✅ **Deployment Complete When:**
- [ ] Application accessible via URL
- [ ] All 5 workflow steps functional
- [ ] API endpoints responding
- [ ] No critical errors in logs
- [ ] Performance acceptable
- [ ] Security configured
- [ ] Monitoring setup

---

**🎉 Congratulations! Your Agentic Focus Group Platform is now deployed and ready for production use.**