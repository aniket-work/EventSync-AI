import random
import time

def get_venue_options(location, attendee_count):
    """Simulates searching for venues."""
    print(f"[Tool] Searching for venues in {location} for {attendee_count} people...")
    time.sleep(1)
    venues = [
        {"name": "Grand Plaza Hotel", "capacity": 500, "price_per_day": 5000, "rating": 4.8},
        {"name": "Skyline Convention Center", "capacity": 1000, "price_per_day": 8500, "rating": 4.5},
        {"name": "Boutique Art Gallery", "capacity": 150, "price_per_day": 3000, "rating": 4.9},
        {"name": "Metropolitan Suites", "capacity": 300, "price_per_day": 4200, "rating": 4.2}
    ]
    # Filter by capacity
    suitable = [v for v in venues if v["capacity"] >= attendee_count]
    return suitable

def get_catering_quotes(attendee_count, meal_type="Standard"):
    """Simulates getting catering quotes."""
    print(f"[Tool] Requesting {meal_type} catering quotes for {attendee_count} pax...")
    time.sleep(1)
    vendors = [
        {"vendor": "Elite Gourmet", "price_per_person": 75, "rating": 4.9},
        {"vendor": "City Bites Catering", "price_per_person": 45, "rating": 4.3},
        {"vendor": "Fusion Flavors", "price_per_person": 60, "rating": 4.6}
    ]
    for v in vendors:
        v["total_cost"] = v["price_per_person"] * attendee_count
    return vendors

def get_av_setup_cost(requirements):
    """Simulates AV setup estimation."""
    print(f"[Tool] Estimating AV costs for requirements: {requirements}...")
    time.sleep(1)
    base_cost = 1500
    if "streaming" in requirements.lower():
        base_cost += 2000
    if "lighting" in requirements.lower():
        base_cost += 1000
    return {"total_av_cost": base_cost, "status": "Available"}

def finalize_booking(booking_details):
    """Simulates final contract execution."""
    print(f"[Tool] EXECUTING FINAL CONTRACT: {booking_details['item']} for ${booking_details['cost']}...")
    time.sleep(2)
    return {"status": "Confirmed", "confirmation_id": f"EVT-{random.randint(10000, 99999)}"}
