import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Function to generate a booking ID
def generate_booking_id():
    base_date = datetime.now().strftime("%Y%m%d")
    random_suffix = str(random.randint(1, 999)).zfill(3)
    return f"TIE{base_date}{random_suffix}"

# Function to load reservations from Supabase
def load_reservations_from_supabase():
    try:
        response = st.session_state.supabase.table("reservations").select("*").eq("mob", "Direct").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error fetching direct reservations: {e}")
        return []

# Function to display form for new direct reservations
def show_new_reservation_form():
    if not st.session_state.permissions.get("add", False):
        st.error("❌ You do not have permission to add reservations.")
        return

    st.header("New Direct Reservation")
    
    # Load property and room map from session state or app.py
    property_room_map = st.session_state.get("property_room_map", {
        "Le Poshe Beach view": {"Double Room": ["101", "102", "202", "203", "204"], "Standard Room": ["201"], "Deluex Double Room Seaview": ["301", "302", "303", "304"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "La Millionaire Resort": {"Double Room": ["101", "102", "103", "105"], "Deluex Double Room with Balcony": ["205", "304", "305"], "Deluex Triple Room with Balcony": ["201", "202", "203", "204", "301", "302", "303"], "Deluex Family Room with Balcony": ["206", "207", "208", "306", "307", "308"], "Deluex Triple Room": ["402"], "Deluex Family Room": ["401"], "Day Use": ["Day Use 1", "Day Use 2", "Day Use 3", "Day Use 5"], "No Show": ["No Show"]},
        "Le Poshe Luxury": {"2BHA Appartment": ["101&102", "101", "102"], "2BHA Appartment with Balcony": ["201&202", "201", "202", "301&302", "301", "302", "401&402", "401", "402"], "3BHA Appartment": ["203to205", "203", "204", "205", "303to305", "303", "304", "305", "403to405", "403", "404", "405"], "Double Room with Private Terrace": ["501"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "Le Poshe Suite": {"2BHA Appartment": ["601&602", "601", "602", "603", "604", "703", "704"], "2BHA Appartment with Balcony": ["701&702", "701", "702"], "Double Room with Terrace": ["801"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "La Paradise Residency": {"Double Room": ["101", "102", "103", "301", "302", "304"], "Family Room": ["201", "203"], "Triple Room": ["202", "303"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "La Paradise Luxury": {"3BHA Appartment": ["101to103", "101", "102", "103", "201to203", "201", "202", "203"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "La Villa Heritage": {"Double Room": ["101", "102", "103"], "4BHA Appartment": ["201to203&301", "201", "202", "203", "301"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "Le Pondy Beach Side": {"Villa": ["101to104", "101", "102", "103", "104"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "Le Royce Villa": {"Villa": ["101to102&201to202", "101", "102", "201", "202"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "La Tamara Luxury": {"3BHA": ["101to103", "101", "102", "103", "104to106", "104", "105", "106", "201to203", "201", "202", "203", "204to206", "204", "205", "206", "301to303", "301", "302", "303", "304to306", "304", "305", "306"], "4BHA": ["401to404", "401", "402", "403", "404"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "La Antilia Luxury": {"Deluex Suite Room": ["101"], "Deluex Double Room": ["203", "204", "303", "304"], "Family Room": ["201", "202", "301", "302"], "Deluex suite Room with Tarrace": ["404"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "La Tamara Suite": {"Two Bedroom apartment": ["101&102"], "Deluxe Apartment": ["103&104"], "Deluxe Double Room": ["203", "204", "205"], "Deluxe Triple Room": ["201", "202"], "Deluxe Family Room": ["206"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "Le Park Resort": {"Villa with Swimming Pool View": ["555&666", "555", "666"], "Villa with Garden View": ["111&222", "111", "222"], "Family Retreate Villa": ["333&444", "333", "444"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "Villa Shakti": {"2BHA Studio Room": ["101&102"], "2BHA with Balcony": ["202&203", "302&303"], "Family Suite": ["201"], "Family Room": ["301"], "Terrace Room": ["401"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]},
        "Eden Beach Resort": {"Double Room": ["101", "102"], "Deluex Room": ["103", "202"], "Triple Room": ["201"], "Day Use": ["Day Use 1", "Day Use 2"], "No Show": ["No Show"]}
    })

    with st.form(key="new_reservation_form"):
        # Property and room selection
        property_name = st.selectbox("Property Name", list(property_room_map.keys()))
        room_types = list(property_room_map[property_name].keys())
        room_type = st.selectbox("Room Type", room_types)
        room_no = st.selectbox("Room Number", property_room_map[property_name][room_type])
        
        # Guest details
        guest_name = st.text_input("Guest Name")
        mobile_no = st.text_input("Mobile Number (10 digits)")
        no_of_adults = st.number_input("Number of Adults", min_value=1, max_value=20, value=1)
        no_of_children = st.number_input("Number of Children", min_value=0, max_value=5, value=0)
        no_of_infants = st.number_input("Number of Infants", min_value=0, max_value=2, value=0)
        
        # Dates
        check_in = st.date_input("Check-In Date", min_value=datetime.today())
        check_out = st.date_input("Check-Out Date", min_value=check_in + timedelta(days=1))
        
        # Financial details
        tariff = st.number_input("Tariff per Night", min_value=1000.0, max_value=21500.0, value=1000.0)
        advance_amount = st.number_input("Advance Amount", min_value=0.0, value=0.0)
        advance_mop = st.selectbox("Advance Payment Method", ["UPI", "Cash", "Card", "Pending", "Advance not paid"])
        
        # Other details
        mob = st.selectbox("Mode of Booking", ["Direct", "Booking-Drt", "Walk-in", "Website"])
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
                response = st.session_state.supabase.table("reservations").insert(reservation_data).execute()
                if response.data:
                    st.success(f"Reservation {booking_id} created successfully!")
                    from log import log_activity
                    log_activity(st.session_state.supabase, st.session_state.username, f"Created reservation {booking_id}")
                    st.session_state.reservations = load_reservations_from_supabase()  # Refresh data
                else:
                    st.error("Failed to save reservation to the database.")
            except Exception as e:
                st.error(f"Error saving reservation: {str(e)}")

# Function to display existing direct reservations
def show_reservations():
    st.header("View Direct Reservations")
    reservations = st.session_state.get("reservations", load_reservations_from_supabase())
    if not reservations:
        st.info("No direct reservations found.")
        return
    
    df = pd.DataFrame(reservations)
    st.dataframe(df[["booking_id", "property_name", "room_no", "guest_name", "check_in", "check_out", "total_tariff", "payment_status"]])

# Function to edit existing direct reservations
def show_edit_reservations():
    if not st.session_state.permissions.get("edit", False):
        st.error("❌ You do not have permission to edit reservations.")
        return

    st.header("Edit Direct Reservations")
    reservations = st.session_state.get("reservations", load_reservations_from_supabase())
    if not reservations:
        st.info("No direct reservations available to edit.")
        return

    # Select reservation to edit
    booking_ids = [r["booking_id"] for r in reservations]
    selected_booking_id = st.selectbox("Select Reservation to Edit", booking_ids, key="edit_reservation_select")
    if not selected_booking_id:
        return

    # Find selected reservation
    reservation = next(r for r in reservations if r["booking_id"] == selected_booking_id)
    
    with st.form(key="edit_reservation_form"):
        property_room_map = st.session_state.get("property_room_map", {})
        property_name = st.selectbox("Property Name", list(property_room_map.keys()), index=list(property_room_map.keys()).index(reservation["property_name"]))
        room_types = list(property_room_map[property_name].keys())
        room_type = st.selectbox("Room Type", room_types, index=room_types.index(reservation["room_type"]) if reservation["room_type"] in room_types else 0)
        room_no = st.selectbox("Room Number", property_room_map[property_name][room_type], index=property_room_map[property_name][room_type].index(reservation["room_no"]) if reservation["room_no"] in property_room_map[property_name][room_type] else 0)
        
        guest_name = st.text_input("Guest Name", value=reservation["guest_name"])
        mobile_no = st.text_input("Mobile Number (10 digits)", value=reservation["mobile_no"])
        no_of_adults = st.number_input("Number of Adults", min_value=1, max_value=20, value=reservation["no_of_adults"])
        no_of_children = st.number_input("Number of Children", min_value=0, max_value=5, value=reservation["no_of_children"])
        no_of_infants = st.number_input("Number of Infants", min_value=0, max_value=2, value=reservation["no_of_infants"])
        check_in = st.date_input("Check-In Date", value=datetime.strptime(reservation["check_in"], "%Y-%m-%d"))
        check_out = st.date_input("Check-Out Date", value=datetime.strptime(reservation["check_out"], "%Y-%m-%d"))
        tariff = st.number_input("Tariff per Night", min_value=1000.0, max_value=21500.0, value=float(reservation["tariff"]))
        advance_amount = st.number_input("Advance Amount", min_value=0.0, value=float(reservation["advance_amount"]))
        advance_mop = st.selectbox("Advance Payment Method", ["UPI", "Cash", "Card", "Pending", "Advance not paid"], index=["UPI", "Cash", "Card", "Pending", "Advance not paid"].index(reservation["advance_mop"]))
        mob = st.selectbox("Mode of Booking", ["Direct", "Booking-Drt", "Walk-in", "Website"], index=["Direct", "Booking-Drt", "Walk-in", "Website"].index(reservation["mob"]))
        breakfast = st.selectbox("Breakfast Plan", ["CP", "EP"], index=["CP", "EP"].index(reservation["breakfast"]))
        plan_status = st.selectbox("Plan Status", ["Confirmed", "Pending"], index=["Confirmed", "Pending"].index(reservation["plan_status"]))
        submitted_by = st.selectbox("Submitted By", ["Iswariya", "PRAKASH", "Gayathri", "ANAND", "Amrish", "Nandhini", "Baradhan", "Shan"], index=["Iswariya", "PRAKASH", "Gayathri", "ANAND", "Amrish", "Nandhini", "Baradhan", "Shan"].index(reservation["submitted_by"]))
        modified_comments = st.text_area("Modified Comments", value=reservation["modified_comments"])

        submit_button = st.form_submit_button("Update Reservation")

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

            # Prepare updated data
            updated_data = {
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
                "room_type": room_type,
                "breakfast": breakfast,
                "plan_status": plan_status,
                "submitted_by": submitted_by,
                "modified_by": st.session_state.username,
                "modified_comments": modified_comments,
                "payment_status": "Fully Paid" if balance_amount == 0 else random.choice(["Partially Paid", "Not Paid"])
            }

            try:
                # Update in Supabase
                response = st.session_state.supabase.table("reservations").update(updated_data).eq("booking_id", selected_booking_id).execute()
                if response.data:
                    st.success(f"Reservation {selected_booking_id} updated successfully!")
                    from log import log_activity
                    log_activity(st.session_state.supabase, st.session_state.username, f"Updated reservation {selected_booking_id}")
                    st.session_state.reservations = load_reservations_from_supabase()  # Refresh data
                else:
                    st.error("Failed to update reservation.")
            except Exception as e:
                st.error(f"Error updating reservation: {str(e)}")

# Function to show analytics for direct reservations
def show_analytics():
    if st.session_state.role != "Management":
        st.error("❌ Access Denied: Analytics is available only for Management.")
        return

    st.header("Direct Reservations Analytics")
    reservations = st.session_state.get("reservations", load_reservations_from_supabase())
    if not reservations:
        st.info("No direct reservations available for analytics.")
        return

    df = pd.DataFrame(reservations)
    
    # Summary statistics
    st.subheader("Summary")
    total_bookings = len(df)
    total_revenue = df["total_tariff"].sum()
    avg_tariff = df["total_tariff"].mean()
    st.write(f"Total Bookings: {total_bookings}")
    st.write(f"Total Revenue: ₹{total_revenue:,.2f}")
    st.write(f"Average Tariff per Booking: ₹{avg_tariff:,.2f}")

    # Bookings by property
    st.subheader("Bookings by Property")
    property_counts = df["property_name"].value_counts()
    st.bar_chart(property_counts)

    # Payment status distribution
    st.subheader("Payment Status Distribution")
    payment_status_counts = df["payment_status"].value_counts()
    st.bar_chart(payment_status_counts)

    # Revenue by property
    st.subheader("Revenue by Property")
    revenue_by_property = df.groupby("property_name")["total_tariff"].sum()
    st.bar_chart(revenue_by_property)
