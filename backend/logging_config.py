"""
Logging Configuration for DMCAShield System
Centralized logging for all 12 departments.
"""

import logging
import os
from datetime import datetime

def setup_logging():
    """Set up centralized logging configuration."""
    log_dir = "F:/Anti gravity projects/Dmca company/dmcashield-agency/logs"
    os.makedirs(log_dir, exist_ok=True)
    
    # Main log file
    log_file = f"{log_dir}/dmcashield_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Department-specific loggers
    departments = [
        'scraping', 'validation', 'marketing', 'email_sending',
        'tracking', 'sales', 'sheets', 'accounts', 
        'tasks', 'ml', 'jarvis', 'memory'
    ]
    
    for dept in departments:
        logger = logging.getLogger(dept)
        dept_handler = logging.FileHandler(f"{log_dir}/{dept}.log")
        dept_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(dept_handler)
    
    return logging.getLogger('main')

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("DMCAShield logging system initialized")
