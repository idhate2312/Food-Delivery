
import streamlit as st

from food_delivery import (
    Customer,
    DeliveryPartner,
    MenuItem,
    Restaurant
)

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="Food Delivery System",
    page_icon="🍔",
    layout="wide"
)

st.title("🍔 Food Delivery System")
st.caption("Object-Oriented Programming | Python + Streamlit")

# -----------------------------
# SESSION STATE
# -----------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "partner" not in st.session_state:
    st.session_state.partner = None

if "restaurant" not in st.session_state:
    restaurant = Restaurant("Bawarchi", "MG Road")
    restaurant.add_item(MenuItem("Chicken Biryani", 250, False))
    restaurant.add_item(MenuItem("Veg Biryani", 180, True))
    restaurant.add_item(MenuItem("Paneer Tikka", 220, True))
    restaurant.add_item(MenuItem("Chicken Kebab", 200, False))
    st.session_state.restaurant = restaurant

if "current_order" not in st.session_state:
    st.session_state.current_order = None

if "order_log" not in st.session_state:
    st.session_state.order_log = []


customer = st.session_state.customer
partner = st.session_state.partner
restaurant = st.session_state.restaurant
order = st.session_state.current_order

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Dashboard",
        "Register Customer",
        "Wallet",
        "Restaurant & Menu",
        "Place Order",
        "Delivery",
        "Order History"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("Current Session")

if customer:
    st.sidebar.success(f"Customer: {customer._name}")
    st.sidebar.write(
        f"Wallet: ₹{customer._wallet_balance:.2f}"
    )
else:
    st.sidebar.warning("No customer registered")

if partner:
    st.sidebar.write(f"Partner: {partner._name}")
    st.sidebar.write(
        "Available" if partner.is_available
        else "On delivery"
    )
else:
    st.sidebar.info("No delivery partner registered")

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":
    st.subheader("Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Customer",
            customer._name if customer else "Not registered"
        )

    with col2:
        st.metric(
            "Wallet Balance",
            f"₹{customer._wallet_balance:.2f}"
            if customer else "₹0.00"
        )

    with col3:
        st.metric(
            "Current Order",
            order._order_id if order else "None"
        )

    st.divider()

    st.subheader("Restaurant")
    st.write(f"**{restaurant.name}**")
    st.write(f"Location: {restaurant.location}")

    st.subheader("Delivery Partner")
    if partner:
        st.write(f"**{partner._name}**")
        st.write(f"Vehicle: {partner.vehicle}")
        st.write(
            f"Availability: "
            f"{'Available' if partner.is_available else 'Busy'}"
        )
    else:
        st.info("Register a delivery partner in the Delivery section.")

    st.subheader("How the system works")
    st.markdown("""
    1. Register a customer.
    2. Add money to the customer's wallet.
    3. Browse the restaurant menu.
    4. Select items and place an order.
    5. Assign a delivery partner.
    6. Verify OTP and complete delivery.
    """)

# -----------------------------
# REGISTER CUSTOMER
# -----------------------------
elif page == "Register Customer":
    st.subheader("👤 Register Customer")

    with st.form("customer_form"):
        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        address = st.text_area("Delivery Address")

        submitted = st.form_submit_button(
            "Register Customer",
            type="primary"
        )

        if submitted:
            if not name.strip() or not phone.strip() or not address.strip():
                st.error("Please fill in all fields.")
            else:
                st.session_state.customer = Customer(
                    name.strip(),
                    phone.strip(),
                    address.strip()
                )
                st.session_state.current_order = None
                st.success("Customer registered successfully!")
                st.rerun()

    if customer:
        st.divider()
        st.subheader("Customer Profile")
        st.write(f"**Name:** {customer._name}")
        st.write(f"**Phone:** {customer._phone}")
        st.write(f"**Address:** {customer.address}")
        st.write(
            f"**Wallet:** ₹{customer._wallet_balance:.2f}"
        )

# -----------------------------
# WALLET
# -----------------------------
elif page == "Wallet":
    st.subheader("💰 Customer Wallet")

    if not customer:
        st.warning("Register a customer first.")
    else:
        st.metric(
            "Available Balance",
            f"₹{customer._wallet_balance:.2f}"
        )

        with st.form("wallet_form"):
            amount = st.number_input(
                "Amount to add (₹)",
                min_value=0.0,
                step=50.0
            )

            add_money = st.form_submit_button(
                "Add Money",
                type="primary"
            )

            if add_money:
                if amount <= 0:
                    st.error("Enter an amount greater than zero.")
                else:
                    customer.add_to_wallet(amount)
                    st.success(
                        f"₹{amount:.2f} added successfully."
                    )
                    st.rerun()

        st.caption(
            "Wallet balance is managed by the Customer class."
        )

# -----------------------------
# RESTAURANT & MENU
# -----------------------------
elif page == "Restaurant & Menu":
    st.subheader("🍽️ Restaurant & Menu")

    st.markdown(f"### {restaurant.name}")
    st.write(f"📍 {restaurant.location}")
    st.success("Restaurant is currently open")

    st.divider()

    for item in restaurant.get_menu():
        col1, col2, col3 = st.columns([3, 1, 1])

        with col1:
            st.write(f"**{item.name}**")

        with col2:
            st.write(
                "Veg 🟢" if item.is_veg else "Non-Veg 🔴"
            )

        with col3:
            st.write(f"₹{item.price}")

# -----------------------------
# PLACE ORDER
# -----------------------------
elif page == "Place Order":
    st.subheader("🛒 Place an Order")

    if not customer:
        st.warning("Please register a customer first.")
    else:
        st.write(f"Ordering for: **{customer._name}**")
        st.write(f"Address: {customer.address}")

        menu = restaurant.get_menu()

        selected_names = st.multiselect(
            "Select food items",
            options=[item.name for item in menu]
        )

        selected_items = [
            item for item in menu
            if item.name in selected_names
        ]

        if selected_items:
            st.divider()
            st.subheader("Your Cart")

            subtotal = sum(
                item.price for item in selected_items
            )
            gst = subtotal * 0.05
            packaging = 20
            total = subtotal + gst + packaging

            for item in selected_items:
                st.write(
                    f"{item.name} — ₹{item.price}"
                )

            st.divider()

            c1, c2 = st.columns(2)
            with c1:
                st.write("Subtotal")
                st.write("GST (5%)")
                st.write("Packaging")
                st.markdown("**Total**")

            with c2:
                st.write(f"₹{subtotal:.2f}")
                st.write(f"₹{gst:.2f}")
                st.write(f"₹{packaging:.2f}")
                st.markdown(f"**₹{total:.2f}**")

            st.write(
                f"Wallet balance: "
                f"₹{customer._wallet_balance:.2f}"
            )

            if st.button(
                "Confirm Order",
                type="primary",
                disabled=st.session_state.current_order is not None
            ):
                new_order = customer.place_order(
                    restaurant,
                    selected_items
                )

                if new_order:
                    st.session_state.current_order = new_order
                    st.session_state.order_log.append(
                        new_order
                    )
                    st.success(
                        f"Order {new_order._order_id} placed!"
                    )
                    st.rerun()
                else:
                    st.error(
                        "Order could not be placed. "
                        "Check your wallet and restaurant."
                    )

        else:
            st.info("Select one or more menu items.")

        if st.session_state.current_order:
            st.warning(
                "An order is already active. "
                "Complete it before placing another."
            )

# -----------------------------
# DELIVERY PARTNER & DELIVERY
# -----------------------------
elif page == "Delivery":
    st.subheader("🛵 Delivery Management")

    if not partner:
        st.markdown("### Register Delivery Partner")

        with st.form("partner_form"):
            partner_name = st.text_input("Partner Name")
            partner_phone = st.text_input("Partner Phone")
            vehicle = st.selectbox(
                "Vehicle",
                ["Bike", "Scooter", "Bicycle"]
            )

            register_partner = st.form_submit_button(
                "Register Partner",
                type="primary"
            )

            if register_partner:
                if not partner_name.strip() or not partner_phone.strip():
                    st.error("Enter the partner's name and phone.")
                else:
                    st.session_state.partner = DeliveryPartner(
                        partner_name.strip(),
                        partner_phone.strip(),
                        vehicle
                    )
                    st.success("Delivery partner registered!")
                    st.rerun()

    else:
        st.markdown("### Delivery Partner")
        st.write(f"**Name:** {partner._name}")
        st.write(f"**Vehicle:** {partner.vehicle}")
        st.write(
            f"**Availability:** "
            f"{'Available' if partner.is_available else 'Busy'}"
        )

        if order is None:
            st.info("No active order to deliver.")

        else:
            st.divider()
            st.subheader("Active Order")
            st.write(f"Order ID: **{order._order_id}**")
            st.write(f"Status: **{order._status}**")

            if order._status == "Placed":
                if st.button(
                    "Accept Order",
                    type="primary",
                    disabled=not partner.is_available
                ):
                    accepted = partner.accept_order(order)

                    if accepted:
                        st.success("Order accepted!")
                    else:
                        st.error("Could not accept order.")

                    st.rerun()

            elif order._status == "Accepted":
                st.info(
                    "Order accepted. Ask the customer for "
                    "their delivery OTP."
                )

                with st.form("otp_form"):
                    otp = st.text_input(
                        "Enter OTP",
                        max_chars=4
                    )

                    verify = st.form_submit_button(
                        "Verify OTP & Deliver",
                        type="primary"
                    )

                    if verify:
                        if not otp.isdigit() or len(otp) != 4:
                            st.error("Enter a valid 4-digit OTP.")
                        else:
                            success = partner.deliver(
                                order,
                                otp
                            )

                            if success:
                                customer.notify(
                                    f"Your order {order._order_id} "
                                    "has been delivered."
                                )
                                st.success(
                                    "Delivery completed successfully!"
                                )
                            else:
                                st.error(
                                    "Incorrect OTP or delivery failed."
                                )

                            st.rerun()

            elif order._status == "Delivered":
                st.success("This order has been delivered.")

# -----------------------------
# ORDER HISTORY
# -----------------------------
elif page == "Order History":
    st.subheader("📋 Order History")

    if not customer:
        st.warning("Register a customer first.")
    elif not customer.order_history:
        st.info("No orders have been placed yet.")
    else:
        for previous_order in reversed(
            customer.order_history
        ):
            with st.expander(
                f"{previous_order._order_id} — "
                f"{previous_order._status}"
            ):
                st.write("Items:")
                for item in previous_order._items:
                    st.write(
                        f"- {item.name}: ₹{item.price}"
                    )

                st.write(
                    f"Total: "
                    f"₹{previous_order.calculate_bill():.2f}"
                )
                st.write(
                    f"Estimated time: "
                    f"{previous_order.estimated_time()} minutes"
                )


