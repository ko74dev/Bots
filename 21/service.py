# service.py
from typing import Dict

from db import get_all_services

def get_services_dict() -> Dict[str, str]:
    """Returns the services as a dictionary."""
    services_list = get_all_services()
    return {service['name']: service['price'] for service in services_list}

def get_price_text() -> str:
    """Generates the price list text."""
    services = get_services_dict()
    return "📋 *Наши услуги:*\n\n" + "\n".join(f"• {k}: {v}" for k, v in services.items())
