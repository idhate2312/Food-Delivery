import streamlit as st
from food_delivery import Customer, DeliveryPartner, MenuItem, Restaurant

st.set_page_config(page_title="Food Delivery System", page_icon="🍔", layout="wide")

st.title("🍔 OOP Food Delivery System")
st.caption("Simple Streamlit interface using classes from food_delivery.py")

# -----------------------------
# Session state
# -----------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "restaurant" not in st.session_state:
    restaurant = Restaurant("Food Corner", "Chhatrapati Sambhajinagar")
    restaurant.add_item(MenuItem("Veg Burger", 120, True))
    restaurant.add_item(MenuItem("Pizza", 250, True))
    restaurant.add_item(MenuItem("Chicken Biryani", 220, False))
    restaurant.add_item(MenuItem("Paneer Tikka", 180, True))
    st.session_state.restaurant = restaurant

if "order" not in st.session_state:
    st.session_state.order = None

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = None

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Food Delivery Menu")
section = st.sidebar.radio(
    "Choose an action",
    [
        "1. Create Customer",
        "2. Add Wallet Balance",
        "3. Show Restaurant Menu",
        "4. Place an Order",
        "5. Create Delivery Partner",
        "6. Accept Order",
        "7. Enter OTP",
        "8. Complete Delivery",
    ],
)

customer = st.session_state.customer
restaurant = st.session_state.restaurant
order = st.session_state.order
partner = st.session_state.delivery_partner

# -----------------------------
# 1. Create Customer
# -----------------------------
if section == "1. Create Customer":
    st.header("👤 Create Customer")

    with st.form("customer_form"):
        name = st.text_input("Customer Name")
        phone = st.text_input("Phone Number")
        address = st.text_input("Delivery Address")
        submitted = st.form_submit_button("Create Customer")

        if submitted:
            if not name or not phone or not address:
                st.error("Please fill all fields.")
            else:
                st.session_state.customer = Customer(name, phone, address)
                st.success(f"Customer '{name}' created successfully.")

# -----------------------------
# 2. Add Wallet Balance
# -----------------------------
elif section == "2. Add Wallet Balance":
    st.header("💰 Add Wallet Balance")

    if customer is None:
        st.warning("Please create a customer first.")
    else:
        st.write(f"Customer: **{customer._name}**")
        st.write(f"Current Balance: **₹{customer._wallet_balance:.2f}**")

        amount = st.number_input("Amount to Add", min_value=0.0, step=50.0)

        if st.button("Add Money"):
            if amount < 0:
                st.error("Negative amount is not allowed.")
            else:
                customer.add_to_wallet(amount)
                st.success(f"₹{amount:.2f} added to wallet.")
                st.rerun()

# -----------------------------
# 3. Restaurant Menu
# -----------------------------
elif section == "3. Show Restaurant Menu":
    st.header("🍽️ Restaurant Menu")
    st.write(f"### {restaurant._name}")
    st.write(f"Location: {restaurant._location}")

    menu = restaurant.get_menu()

    for i, item in enumerate(menu, start=1):
        veg = "🟢 Veg" if item.is_veg else "🔴 Non-Veg"
        st.write(f"**{i}. {item.name}** — ₹{item.price} — {veg}")

# -----------------------------
# 4. Place an Order
# -----------------------------
elif section == "4. Place an Order":
    st.header("🛒 Place an Order")

    if customer is None:
        st.warning("Please create a customer first.")
    else:
        menu = restaurant.get_menu()

        selected_items = st.multiselect(
            "Select food items",
            options=menu,
            format_func=lambda x: f"{x.name} - ₹{x.price}",
        )

        if st.button("Place Order"):
            if not selected_items:
                st.error("Please select at least one item.")
            else:
                order = customer.place_order(restaurant, selected_items)
                st.session_state.order = order
                st.success(f"Order {order._order_id} placed successfully.")
                st.info(f"OTP: {order._otp}")

                st.write(f"**Status:** {order._status}")
                st.write(f"**Estimated Time:** {order.estimated_time()} minutes")
                st.write(f"**Total Bill:** ₹{order.calculate_bill():.2f}")

# -----------------------------
# 5. Create Delivery Partner
# -----------------------------
elif section == "5. Create Delivery Partner":
    st.header("🛵 Create Delivery Partner")

    with st.form("delivery_form"):
        name = st.text_input("Partner Name")
        phone = st.text_input("Phone Number")
        vehicle = st.selectbox("Vehicle", ["Bike", "Scooter", "Car"])
        submitted = st.form_submit_button("Create Partner")

        if submitted:
            if not name or not phone:
                st.error("Please fill all fields.")
            else:
                st.session_state.delivery_partner = DeliveryPartner(
                    name, phone, vehicle
                )
                st.success(f"Delivery partner '{name}' created successfully.")

# -----------------------------
# 6. Accept Order
# -----------------------------
elif section == "6. Accept Order":
    st.header("📦 Accept Order")

    if order is None:
        st.warning("Please place an order first.")
    elif partner is None:
        st.warning("Please create a delivery partner first.")
    else:
        st.write(f"Order: **{order._order_id}**")
        st.write(f"Current Status: **{order._status}**")
        st.write(f"Partner Available: **{partner.is_available}**")

        if st.button("Accept Order"):
            if partner.is_available and order._status == "Placed":
                partner.accept_order(order)
                st.success("Order accepted by delivery partner.")
                st.rerun()
            else:
                st.error("Order cannot be accepted.")

# -----------------------------
# 7. Enter OTP
# -----------------------------
elif section == "7. Enter OTP":
    st.header("🔐 Enter OTP")

    if order is None:
        st.warning("Please place an order first.")
    else:
        st.write(f"Order: **{order._order_id}**")
        st.write(f"Order Status: **{order._status}**")

        otp = st.number_input("Enter OTP", min_value=0, max_value=9999, step=1)

        if st.button("Verify OTP"):
            if order.verify_otp(otp):
                st.success("OTP is correct.")
            else:
                st.error("Invalid OTP.")

# -----------------------------
# 8. Complete Delivery
# -----------------------------
elif section == "8. Complete Delivery":
    st.header("✅ Complete Delivery")

    if order is None:
        st.warning("Please place an order first.")
    elif partner is None:
        st.warning("Please create a delivery partner first.")
    else:
        st.write(f"Order: **{order._order_id}**")
        st.write(f"Current Status: **{order._status}**")

        otp = st.number_input(
            "Enter delivery OTP",
            min_value=0,
            max_value=9999,
            step=1,
        )

        if st.button("Complete Delivery"):
            if order._status != "Accepted":
                st.error("Order must be accepted before delivery.")
            elif partner.deliver(order, otp):
                st.success("Delivery completed successfully.")
                st.rerun()
            else:
                st.error("Invalid OTP. Delivery not completed.")

# -----------------------------
# Current system status
# -----------------------------
st.sidebar.divider()
st.sidebar.subheader("Current Status")

if customer:
    st.sidebar.write(f"Customer: {customer._name}")
else:
    st.sidebar.write("Customer: Not created")

if order:
    st.sidebar.write(f"Order: {order._order_id}")
    st.sidebar.write(f"Status: {order._status}")
else:
    st.sidebar.write("Order: Not placed")

if partner:
    st.sidebar.write(f"Partner: {partner._name}")
    st.sidebar.write(f"Available: {partner.is_available}")
else:
    st.sidebar.write("Partner: Not created")
