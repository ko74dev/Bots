# test.py
import os
import db
import service

def cleanup_db():
    """Remove existing db to test fresh init."""
    if os.path.exists("salon.db"):
        os.remove("salon.db")

def test_db_init():
    print("=== Test: db.init_db() ===")
    cleanup_db()
    db.init_db()
    print("db.init_db() completed successfully.")

def test_get_all_services():
    print("\n=== Test: db.get_all_services() ===")
    services = db.get_all_services()
    print(f"get_all_services() returned: {services}")
    assert len(services) > 0, "Expected services to be loaded from DB"
    assert len(services) == 4, f"Expected 4 services, got {len(services)}"
    print("db.get_all_services() test passed.")

def test_service_get_services_dict():
    print("\n=== Test: service.get_services_dict() ===")
    services_dict = service.get_services_dict()
    print(f"get_services_dict() returned: {services_dict}")
    assert len(services_dict) > 0, "Expected services dictionary to be non-empty"
    assert len(services_dict) == 4, f"Expected 4 services, got {len(services_dict)}"
    assert "Стрижка" in services_dict
    assert "Маникюр" in services_dict
    assert "Макияж" in services_dict
    assert "Педикюр" in services_dict
    print("service.get_services_dict() test passed.")

def test_service_get_price_text():
    print("\n=== Test: service.get_price_text() ===")
    price_text = service.get_price_text()
    print(f"get_price_text() returned:\n{price_text}")
    assert "Наши услуги" in price_text, "Expected price text to contain 'Наши услуги'"
    assert "Стрижка" in price_text
    assert "Маникюр" in price_text
    assert "Макияж" in price_text
    assert "Педикюр" in price_text
    print("service.get_price_text() test passed.")

if __name__ == "__main__":
    test_db_init()
    test_get_all_services()
    test_service_get_services_dict()
    test_service_get_price_text()
    print("\n=== All tests passed! ===")
