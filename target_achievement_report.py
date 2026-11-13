        report_year, report_month = 2026, 2
    elif selected_month == "March 2026":
        report_year, report_month = 2026, 3
    elif selected_month == "April 2026":
        report_year, report_month = 2026, 4
    elif selected_month == "May 2026":
        report_year, report_month = 2026, 5
    elif selected_month == "June 2026":
        report_year, report_month = 2026, 6
    elif selected_month == "July 2026":
        report_year, report_month = 2026, 7
    elif selected_month == "August 2026":
        report_year, report_month = 2026, 8
    elif selected_month == "September 2026":
        report_year, report_month = 2026, 9
    elif selected_month == "October 2026":
        report_year, report_month = 2026, 10
    else:  # November 2026
        report_year, report_month = 2026, 11
    
    # Calculate balance days
    if current_date.year == report_year and current_date.month == report_month:
        _, days_in_month = calendar.monthrange(report_year, report_month)
        balance_days = days_in_month - current_date.day
    else:
        _, days_in_month = calendar.monthrange(report_year, report_month)
        if date(report_year, report_month, 1) > current_date:
            balance_days = days_in_month  # Future month
        else:
            balance_days = 0  # Past month
    
    _, days_in_month = calendar.monthrange(report_year, report_month)
    dates = [date(report_year, report_month, d) for d in range(1, days_in_month + 1)]
    
    targets = MONTHLY_TARGETS[selected_month]
    
    st.info(f"📅 Current Date: {current_date.strftime('%B %d, %Y')} | ⏳ Balance Days in {selected_month}: {balance_days}")

    properties = load_properties(report_year, report_month)

    with st.spinner("Generating report..."):
        bookings = {}
        total_bookings_count = 0
        for p in properties:
            try:
                bookings[p] = load_combined_bookings(p, dates[0], dates[-1])
                total_bookings_count += len(bookings[p])
            except:
                bookings[p] = []
        
        st.info(f"📊 Loaded {total_bookings_count} total bookings across all properties for {selected_month}")

        # Main Report
        df = build_target_achievement_report(properties, dates, bookings, current_date, targets)
        styled = style_dataframe(df)

    st.dataframe(styled, use_container_width=True, hide_index=True)

    if not df.empty and "TOTAL" in df["Property Name"].values:
        total = df[df["Property Name"] == "TOTAL"].iloc[0]
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        with c1: st.metric("Total Target", f"₹{total.Target:,.0f}")
        with c2: st.metric("Achieved", f"₹{total.Achieved:,.0f}", delta=f"{total['Achieved %']:.1f}%")
        with c3: st.metric("Balance", f"₹{total.Balance:,.0f}", delta=f"{balance_days} days")
        with c4: st.metric("GST", f"₹{total['GST']:,.0f}")
        with c5: st.metric("Commission", f"₹{total['Commission']:,.0f}")
        with c6: st.metric("Receivable", f"₹{total['Receivable']:,.0f}")

    # Till Today Report
    st.markdown("---")
    st.subheader(f"📊 Values Till Today - {selected_month}")
    
    if current_date >= dates[0]:
        st.caption(f"Performance metrics calculated from {dates[0].strftime('%B %d, %Y')} to {min(current_date, dates[-1]).strftime('%B %d, %Y')} | ARR = Revenue ÷ Total Room Inventory")
        
        df_today = build_till_today_report(properties, dates, bookings, current_date, targets)
        styled_today = style_dataframe(df_today)
        
        st.dataframe(styled_today, use_container_width=True, hide_index=True)

        if not df_today.empty and "TOTAL" in df_today["Property Name"].values:
            total_today = df_today[df_today["Property Name"] == "TOTAL"].iloc[0]
            c1, c2, c3, c4, c5, c6 = st.columns(6)
            with c1: st.metric("Target", f"₹{total_today.Target:,.0f}")
            with c2: st.metric("Achieved", f"₹{total_today.Achieved:,.0f}", delta=f"{total_today['Percent']:.1f}%")
            with c3: st.metric("Occupancy", f"{total_today['Occupancy %']:.1f}%")
            with c4: st.metric("Sold Rooms", f"{total_today['Sold Rooms']:,.0f}")
            with c5: st.metric("Unsold Rooms", f"{total_today['Unsold Rooms']:,.0f}")
            with c6: st.metric("Current ARR", f"₹{total_today['Current ARR']:,.0f}")
    else:
        st.info(f"📅 {selected_month} has not started yet. 'Till Today' report will be available from {dates[0].strftime('%B %d, %Y')} onwards.")

    # Download buttons
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Download Full Report (CSV)", 
            df.to_csv(index=False), 
            f"Target_Achievement_{selected_month.replace(' ', '_')}.csv", 
            "text/csv"
        )
    with col2:
        if current_date >= dates[0]:
            st.download_button(
                "📥 Download Till Today Report (CSV)", 
                df_today.to_csv(index=False), 
                f"Target_Achievement_TillToday_{selected_month.replace(' ', '_')}.csv", 
                "text/csv"
            )

if __name__ == "__main__":
    show_target_achievement_report()
