import mysql.connector
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = '6d9e4e8b9aaf4a3e88b89a3f9a7e4b65'

# Establish connection to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="USE_YOUR_USERNAME",
    password="USE_YOUR_PASSWORD_FOR_DATABASE",
    database="Inventory_Management"  # Select the database here
)
cur = db.cursor()

# Utility function for handling database execution
def execute_query(cur, query, params=None, fetch=False):
    try:
        cur.execute(query, params)
        if fetch:
            return cur.fetchall()
        db.commit()
    except mysql.connector.Error as err:
        flash(f"Database Error: {err}")
        return None

def create_data(cur):
    try:
        cur.execute("CREATE DATABASE IF NOT EXISTS Inventory_Management")
        cur.execute("USE Inventory_Management")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Data (
                id INT AUTO_INCREMENT PRIMARY KEY,
                item_ID VARCHAR(10),
                item_name VARCHAR(50),
                quantity INT,
                price INT,
                category VARCHAR(20)
            )
        """)
    except mysql.connector.Error as err:
        flash(f"Error: {err}")

def add_data(cur, item_id, item_name, quantity, price, category):
    if not all([item_id, item_name, quantity, price, category]):
        return "All fields are required!"
    
    if not quantity.isdigit() or not price.isdigit():
        return "Quantity and Price must be numeric values!"

    result = execute_query(cur, "SELECT COUNT(*) FROM Data WHERE item_ID = %s", (item_id,), fetch=True)
    if result and result[0][0] > 0:
        return f"Record with the same item_ID {item_id} already exists!"
    
    sql = "INSERT INTO Data (item_ID, item_name, quantity, price, category) VALUES (%s, %s, %s, %s, %s)"
    execute_query(cur, sql, (item_id, item_name, quantity, price, category))
    return "Record Inserted!"

def remove_data(cur, item_id):
    result = execute_query(cur, "SELECT COUNT(*) FROM Data WHERE item_ID = %s", (item_id,), fetch=True)
    if result and result[0][0] == 0:
        return f"Record with item_ID {item_id} does not exist!"
    
    execute_query(cur, "DELETE FROM Data WHERE item_ID = %s", (item_id,))
    return "Record Deleted!"

def update_data(cur, item_id, item_name=None, quantity=None, price=None, category=None):
    if not item_id:
        return "Item ID is required!"
    
    result = execute_query(cur, "SELECT COUNT(*) FROM Data WHERE item_ID = %s", (item_id,), fetch=True)
    if result and result[0][0] == 0:
        return f"Record with item_ID {item_id} does not exist!"
    
    updates = []
    values = []
    if item_name:
        updates.append("item_name = %s")
        values.append(item_name)
    if quantity:
        if not quantity.isdigit():
            return "Quantity must be a numeric value!"
        updates.append("quantity = %s")
        values.append(quantity)
    if price:
        if not price.isdigit():
            return "Price must be a numeric value!"
        updates.append("price = %s")
        values.append(price)
    if category:
        updates.append("category = %s")
        values.append(category)

    if not updates:
        return "No updates provided!"

    sql = "UPDATE Data SET " + ", ".join(updates) + " WHERE item_ID = %s"
    values.append(item_id)
    execute_query(cur, sql, tuple(values))
    return "Record Updated!"

def search_data(cur, item_id=None, item_name=None, category=None):
    criteria = []
    values = []

    if item_id:
        criteria.append("item_ID = %s")
        values.append(item_id)
    if item_name:
        criteria.append("item_name LIKE %s")
        values.append(f"%{item_name}%")
    if category:
        criteria.append("category = %s")
        values.append(category)

    if not criteria:
        return "No search criteria provided!"

    sql = "SELECT * FROM Data WHERE " + " AND ".join(criteria)
    results = execute_query(cur, sql, tuple(values), fetch=True)

    if not results:
        return "No records found!"

    return results


def get_all_data(cur):
    return execute_query(cur, "SELECT * FROM Data", fetch=True)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        operation = request.form.get("operation")
        if operation == 'add':
            return redirect(url_for('adding'))
        elif operation == 'remove':
            return redirect(url_for('removing'))
        elif operation == 'update':
            return redirect(url_for('update'))
        elif operation == 'search':
            return redirect(url_for('search'))
    return render_template("dashboard.html")

@app.route("/adding", methods=['GET', 'POST'])
def adding():
    if request.method == 'POST':
        item_id = request.form['itemID']
        item_name = request.form['itemName']
        quantity = request.form['quantity']
        price = request.form['price']
        category = request.form['category']
        
        result = add_data(cur, item_id, item_name, quantity, price, category)
        flash(result)
    
    data = get_all_data(cur)
    return render_template("adding.html", data=data)

@app.route("/removing", methods=['GET', 'POST'])
def removing():
    if request.method == 'POST':
        item_id = request.form['itemID']
        result = remove_data(cur, item_id)
        flash(result)

    data = get_all_data(cur)
    return render_template("removing.html", data=data)

@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        item_id = request.form['itemID']
        item_name = request.form['itemName']
        quantity = request.form['quantity']
        price = request.form['price']
        category = request.form['category']
        
        result = update_data(cur, item_id, item_name, quantity, price, category)
        flash(result)
    
    data = get_all_data(cur)
    return render_template("update.html", data=data)

@app.route("/search", methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        item_id = request.form.get('itemID')
        item_name = request.form.get('itemName')
        category = request.form.get('category')
        
        search_result = search_data(cur, item_id, item_name, category)
        if isinstance(search_result, str):  # If results is an error message
            flash(search_result)
        else:
            results = search_result

    return render_template("search.html", data=results)


if __name__ == "__main__":
    create_data(cur)
    app.run(debug=True)
