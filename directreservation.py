import streamlit as st
from datetime import datetime, timedelta
import random

# Function to generate a booking ID
def generate_booking_id():
    base_date = datetime.now().strftime("%Y%m%d")
    random_suffix = str(random.randint(1, 999)).zfill(3)
    return f"TIE{base_date}{random_suffix}"

# Function to display a form for new direct reservations
def show_new_reservation_form(supabase: 'Client'):
    st.header("New Direct Reservation")
    
    # Form for entering reservation details
    with st.form(key="new_reservation_form"):
        # Reservation details
        property_name = st.selectbox(
            "Property Name",
            [
                "Villa Shakti", "La Millionaire Resort", "La Tamara Luxury", "Le Poshe Luxury",
                "La Paradise Residency", "Eden Beach Resort", "Le Poshe Suite", "La Villa Heritage",
                "Le Poshe Beach view", "La Tamara Suite", "Le Royce Villa", "La Paradise Luxury", "Le Park Resort"
            ]
        )
        room_no = st.text_input("Room Number (e.g., 101 or 101&102)")
        guest_name = st.text_input("Guest Name")
        mobile_no = st.text_input("Mobile Number (10 digits)")
        no_of_adults = st.number_input("Number of Adults", min_value=1, max_value=20, value=1)
        no_of_children = st.number_input("Number of Children", min_value=0, max_value=5, value=0)
        no_of_infants = st.number_input("Number of Infants", min_value=0, max_value=2, value=0)
        check_in = st.date_input("Check-In Date", min_value=datetime.today())
        check_out = st.date_input("Check-Out Date", min_value=check_in + timedelta(days=1))
        tariff = st.number_input("Tariff per Night", min_value=1000.0, max_value=21500.0, value=1000.0)
        advance_amount = st.number_input("Advance Amount", min_value=0.0, value=0.0)
        advance_mop = st.selectbox("Advance Payment Method", ["UPI", "Cash", "Card", "Pending", "Advance not paid"])
        mob = st.selectbox("Mode of Booking", ["Direct", "Booking-Drt", "Walk-in", "Website"])
        room_type = st.selectbox(
            "Room Type",
            [
                "Double Room", "2BHA Studio Room", "3BHA Appartment", "Deluex Family Room",
                "Triple Room", "Deluex Double Room Seaview", "4BHA Appartment", "Villa",
                "Deluex Family Room with Balcony", "Deluxe Double Room", "Deluxe Triple Room",
                "Family Room", "Double Room with Terrace", "2BHA with Balcony", "3BHA", "4BHA",
                "Family Retreate Villa", "Villa with Garden View"
            ]
        )
        breakfast = st.selectbox("Breakfast Plan", ["CP", "EP"])
        plan_status = st.selectbox("Plan Status", ["Confirmed", "Pending"])
        submitted_by = st.selectbox("Submitted By", ["Iswariya", "PRAKASH", "Gayathri", "ANAND", "Amrish", "Nandhini", "Baradhan", "Shan"])

        submit_button = st.form_submit_button("Submit Reservation")

        if submit_button:
            # Validate inputs
            if not guest_name or len(mobile_no) != 10 or not mobile_no.isdigit():
                st.error("Please provide a valid guest name and 10-digit mobile number.")
                return

            # Calculate derived fields
            no_of_days = (check_out - check_in).days
            total_pax = no_of_adults + no_of_children + no_of_infants
            total_tariff = tariff * no_of_days
            balance_amount = total_tariff - advance_amount
            balance_mop = "no balance" if balance_amount == 0 else random.choice(["UPI", "Cash", "Card", "Pending"])
            booking_id = generate_booking_id()
            enquiry_date = check_in - timedelta(days=random.randint(0, 10))
            booking_date = enquiry_date

            # Prepare data for Supabase
            reservation_data = {
                "booking_id": booking_id,
                "property_name": property_name,
                "room_no": room_no,
                "guest_name": guest_name,
                "mobile_no": mobile_no,
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
                "advance_mop": advance_mop,
                "balance_mop": balance_mop,
                "mob": mob,
                "online_source": "null",
                "invoice_no": "null",
                "enquiry_date": enquiry_date.strftime("%Y-%m-%d"),
                "booking_date": booking_date.strftime("%Y-%m-%d"),
                "room_type": room_type,
                "breakfast": breakfast,
                "plan_status": plan_status,
                "submitted_by": submitted_by,
                "modified_by": "",
                "modified_comments": "",
                "remarks": "",
                "payment_status": "Fully Paid" if balance_amount == 0 else random.choice(["Partially Paid", "Not Paid"])
            }

            try:
                # Insert into Supabase
                response = supabase.table("reservations").insert(reservation_data).execute()
                if response.data:
                    st.success(f"Reservation {booking_id} created successfully!")
                else:
                    st.error("Failed to save reservation to the database.")
            except Exception as e:
                st.error(f"Error saving reservation: {str(e)}")

# Function to display existing reservations
def show_reservations(supabase: 'Client'):
    st.header("Direct Reservations")
    try:
        # Fetch all reservations from Supabase
        response = supabase.table("reservations").select("*").eq("mob", "Direct").execute()
        if response.data:
            st.write("### Existing Direct Reservations")
            st.table(response.data)
        else:
            st.write("No direct reservations found.")
    except Exception as e:
        st.error(f"Error fetching reservations: {str(e)}")
