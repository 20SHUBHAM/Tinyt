#!/usr/bin/env python3
"""
Startup script for Agentic Focus Group Platform
Handles initialization, configuration validation, and graceful startup
"""

import os
import sys
import logging
from pathlib import Path

def setup_logging():
    """Set up logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('logs/app.log') if Path('logs').exists() else logging.NullHandler()
        ]
    )

def validate_environment():
    """Validate required environment variables and configuration"""
    required_vars = ['SECRET_KEY']
    llm_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY']
    
    missing_vars = []
    
    # Check required variables
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    # Check LLM API keys (at least one required)
    if not any(os.getenv(var) for var in llm_vars):
        missing_vars.extend(llm_vars)
        print("ERROR: At least one LLM API key is required (OpenAI or Anthropic)")
    
    if missing_vars:
        print("ERROR: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    directories = ['data', 'cache', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✓ Created/verified directory: {directory}")

def main():
    """Main startup function"""
    print("🚀 Starting Agentic Focus Group Platform...")
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create necessary directories
    create_directories()
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    try:
        # Import and validate configuration
        from utils.config import Config
        config = Config()
        
        if not config.validate_config():
            logger.error("Configuration validation failed")
            sys.exit(1)
        
        logger.info("✓ Configuration validated successfully")
        
        # Import and start the Flask app
        from app import app
        
        port = config.port
        debug = config.is_development()
        
        logger.info(f"✓ Starting server on port {port} (debug={debug})")
        print(f"🌐 Access the application at: http://localhost:{port}")
        print("📚 Check README.md for usage instructions")
        print("⚡ Ready for production deployment!")
        
        # Start the Flask application
        app.run(
            host='0.0.0.0',
            port=port,
            debug=debug,
            threaded=True
        )
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print("ERROR: Failed to import required modules. Please install dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Startup error: {e}")
        print(f"ERROR: Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()