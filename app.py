import os
from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ── In-memory data store ──────────────────────────────────────────────────────

PRODUCTS = [
    {"id": 1, "name": "Shoes",       "price": 999,  "image": "images/shoes.jpg"},
    {"id": 2, "name": "Watch",       "price": 1499, "image": "images/watch.jpg"},
    {"id": 3, "name": "Bag",         "price": 799,  "image": "images/bag.jpg"},
    {"id": 4, "name": "Jeans",       "price": 1299, "image": "images/jeans.jpg"},
    {"id": 5, "name": "Sunglasses",  "price": 599,  "image": "images/sunglasses.jpg"},
    {"id": 6, "name": "Perfume",     "price": 899,  "image": "images/perfume.jpg"},
    {"id": 7, "name": "Cap",         "price": 299,  "image": "images/cap.jpg"},
]

ORDERS   = []   # list of placed orders
MESSAGES = []   # contact-form submissions
CHATS    = []   # support-chat messages

# ── Page routes ───────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

# ── REST API ──────────────────────────────────────────────────────────────────

@app.route("/api/products")
def api_products():
    """Return the full product catalogue as JSON."""
    return jsonify(PRODUCTS)

@app.route("/api/contact", methods=["POST"])
def api_contact():
    """Save a contact-form submission."""
    data = request.get_json()
    name    = (data.get("name")    or "").strip()
    email   = (data.get("email")   or "").strip()
    message = (data.get("message") or "").strip()

    if not (name and email and message):
        return jsonify({"success": False, "error": "All fields are required."}), 400

    MESSAGES.append({
        "name":      name,
        "email":     email,
        "message":   message,
        "timestamp": datetime.now().isoformat(),
    })
    print(f"[Contact] {name} <{email}>: {message}")
    return jsonify({"success": True, "message": "Message received!"})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Save a support-chat message and return a simple bot reply."""
    data    = request.get_json()
    user_msg = (data.get("message") or "").strip()

    if not user_msg:
        return jsonify({"success": False, "error": "Empty message."}), 400

    CHATS.append({"role": "user", "text": user_msg, "timestamp": datetime.now().isoformat()})

    # Simple keyword-based auto-reply
    lower = user_msg.lower()
    if any(w in lower for w in ("hello", "hi", "hey")):
        reply = "Hello! How can I help you today? 😊"
    elif any(w in lower for w in ("price", "cost", "how much")):
        reply = "You can find prices on our Products page. All prices are in ₹."
    elif any(w in lower for w in ("order", "buy", "purchase")):
        reply = "Add items to your cart and click 'Order Now' to place an order!"
    elif any(w in lower for w in ("return", "refund")):
        reply = "We accept returns within 7 days of delivery. Use the Contact form for help."
    elif any(w in lower for w in ("delivery", "ship", "track")):
        reply = "Orders are delivered within 3-5 business days across India."
    else:
        reply = "Thanks for reaching out! Our team will get back to you shortly."

    CHATS.append({"role": "bot", "text": reply, "timestamp": datetime.now().isoformat()})
    return jsonify({"success": True, "reply": reply})

@app.route("/api/order", methods=["POST"])
def api_order():
    """Place an order with the cart items sent from the frontend."""
    data  = request.get_json()
    items = data.get("items", [])

    if not items:
        return jsonify({"success": False, "error": "Cart is empty."}), 400

    total = sum(item.get("price", 0) for item in items)
    order = {
        "order_id":  len(ORDERS) + 1,
        "items":     items,
        "total":     total,
        "timestamp": datetime.now().isoformat(),
    }
    ORDERS.append(order)
    print(f"[Order #{order['order_id']}] ₹{total} — {[i['name'] for i in items]}")
    return jsonify({"success": True, "order_id": order["order_id"], "total": total})

# ── Admin helpers (optional, for debugging) ───────────────────────────────────

@app.route("/api/orders")
def api_orders():
    return jsonify(ORDERS)

@app.route("/api/messages")
def api_messages():
    return jsonify(MESSAGES)

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
