import random
import json
import csv
from datetime import datetime, timedelta

# Lists for randomization based on dataset patterns
properties = [
    "Villa Shakti", "La Millionaire Resort", "La Tamara Luxury", "Le Poshe Luxury",
    "La Paradise Residency", "Eden Beach Resort", "Le Poshe Suite", "La Villa Heritage",
    "Le Poshe Beach view", "La Tamara Suite", "Le Royce Villa", "La Paradise Luxury", "Le Park Resort"
]
room_types = [
    "Double Room", "2BHA Studio Room", "3BHA Appartment", "Deluex Family Room",
    "Triple Room", "Deluex Double Room Seaview", "4BHA Appartment", "Villa",
    "Deluex Family Room with Balcony", "Deluxe Double Room", "Deluxe Triple Room",
    "Family Room", "Double Room with Terrace", "2BHA with Balcony", "3BHA", "4BHA",
    "Family Retreate Villa", "Villa with Garden View"
]
guest_names = [
    "Amit Sharma", "Priya Patel", "Ravi Kumar", "Sneha Reddy", "Vikram Singh",
    "Anjali Desai", "Karthik Nair", "Deepa Menon", "Rohan Gupta", "Meera Joshi",
    "Suresh Iyer", "Lakshmi Rao", "Arjun Verma", "Pooja Shah", "Rahul Gupta"
]
submitted_by = ["Iswariya", "PRAKASH", "Gayathri", "ANAND", "Amrish", "Nandhini", "Baradhan", "Shan"]
payment_statuses = ["Fully Paid", "Partially Paid", "Not Paid"]
mop_options = ["UPI", "Cash", "Pending", "Advance not paid", "Card", "MMT", "AIRBNB", "not paid"]
mob_options = ["Direct", "Booking-Drt", "Walk-in", "Website", "MAKEMYTRIP", "AIRBNB"]

# Function to generate random 10-digit Indian mobile number
def generate_mobile():
    return ''.join([str(random.randint(6, 9))] + [str(random.randint(0, 9)) for _ in range(9)])

# Function to generate random room numbers
def generate_room_no():
    if random.random() > 0.3:
        return str(random.randint(101, 404))
    else:
        return f"{random.randint(101, 404)}&{random.randint(101, 404)}"

# Function to generate bookings
def generate_bookings(num_bookings, start_id=4):
    bookings = []
    base_date = datetime(2025, 10, 24)  # Start after last dataset date

    for i in range(num_bookings):
        booking_id = f"TIE2025102400{start_id + i}"
        check_in = base_date + timedelta(days=random.randint(1, 15))
        no_of_days = random.randint(1, 5)
        check_out = check_in + timedelta(days=no_of_days)
        enquiry_date = check_in - timedelta(days=random.randint(0, 10))
        booking_date = enquiry_date

        tariff = round(random.uniform(1000.0, 21500.0), 2)
        total_tariff = round(tariff * no_of_days, 2)
        advance_amount = round(random.uniform(0, total_tariff * 0.8), 2) if random.random() > 0.2 else 0.0
        balance_amount = round(total_tariff - advance_amount, 2)

        no_of_adults = random.randint(1, 15)
        no_of_children = random.randint(0, 2)
        no_of_infants = 0
        total_pax = no_of_adults + no_of_children + no_of_infants

        payment_status = random.choices(payment_statuses, weights=[0.8, 0.15, 0.05])[0]
        balance_mop = random.choice(mop_options) if balance_amount > 0 else "no balance"

        booking = {
            "booking_id": booking_id,
            "property_name": random.choice(properties),
            "room_no": generate_room_no(),
            "guest_name": random.choice(guest_names),
            "mobile_no": generate_mobile(),
            "no_of_adults": no_of_adults,
            "no_of_children": no_of_children,
            "no_of_infants": no_of_infants,
            "total_pax": total_pax,
            "check_in": check_in.strftime("%Y-%m-%d"),
            "check_out": check_out.strftime("%Y-%m-%d"),
            "no_of_days": no_of_days,
            "tariff": tariff,
            "total_tariff": total_tariff,
            "advance_amount": advance_amount,
            "balance_amount": balance_amount,
            "advance_mop": random.choice(mop_options),
            "balance_mop": balance_mop,
            "mob": random.choice(mob_options),
            "online_source": "null",
            "invoice_no": "null",
            "enquiry_date": enquiry_date.strftime("%Y-%m-%d"),
            "booking_date": booking_date.strftime("%Y-%m-%d"),
            "room_type": random.choice(room_types),
            "breakfast": "CP" if random.random() > 0.2 else "EP",
            "plan_status": "Confirmed" if random.random() > 0.1 else "Pending",
            "submitted_by": random.choice(submitted_by),
            "modified_by": "",
            "modified_comments": "",
            "remarks": "",
            "payment_status": payment_status
        }
        bookings.append(booking)
    
    return bookings

# Function to save bookings to CSV
def save_to_csv(bookings, filename="new_bookings.csv"):
    fieldnames = [
        "booking_id", "property_name", "room_no", "guest_name", "mobile_no", "no_of_adults",
        "no_of_children", "no_of_infants", "total_pax", "check_in", "check_out", "no_of_days",
        "tariff", "total_tariff", "advance_amount", "balance_amount", "advance_mop", "balance_mop",
        "mob", "online_source", "invoice_no", "enquiry_date", "booking_date", "room_type",
        "breakfast", "plan_status", "submitted_by", "modified_by", "modified_comments", "remarks",
        "payment_status"
    ]
    
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(bookings)
        print(f"Bookings saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

# Main execution
def main():
    num_bookings = 10  # Number of bookings to generate
    try:
        bookings = generate_bookings(num_bookings)
        
        # Print JSON output
        print("Generated Bookings (JSON):")
        print(json.dumps(bookings, indent=2))
        
        # Save to CSV
        save_to_csv(bookings)
        
    except Exception as e:
        print(f"Error generating bookings: {e}")

if __name__ == "__main__":
    main()
