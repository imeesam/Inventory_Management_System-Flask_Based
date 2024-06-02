from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = '6d9e4e8b9aaf4a3e88b89a3f9a7e4b65' 

# Establish connection to MySQL
db = mysql.connector.connect(
    host=" sql12.freesqldatabase.com",
    user="sql12709648",
    password="tjGukNlQ2f"
)
# r.B4-ib6i&9%uLY
cur = db.cursor()
def create_data(cur):
    # cur.execute("CREATE DATABASE IF NOT EXISTS Inventory_Management")
    cur.execute("USE sql12709648")

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

def add_data(cur, db, item_id, item_name, quantity, price, category):
    try:
        cur.execute("SELECT COUNT(*) FROM Data WHERE item_ID = %s", (item_id,))
        if cur.fetchone()[0] > 0:
            return f"Record with the same item_ID {item_id} already exists!"
        
        sql = "INSERT INTO Data (item_ID, item_name, quantity, price, category) VALUES (%s, %s, %s, %s, %s)"
        val = (item_id, item_name, quantity, price, category)
        cur.execute(sql, val)
        db.commit()
        return "Record Inserted!"
    except mysql.connector.Error as err:
        return f"Error: {err}"

def remove_data(cur, db, item_id):
    try:
        cur.execute("SELECT COUNT(*) FROM Data WHERE item_ID = %s", (item_id,))
        if cur.fetchone()[0] == 0:
            return f"Record with item_ID {item_id} does not exist!"
        
        sql = "DELETE FROM Data WHERE item_ID = %s"
        val = (item_id,)
        cur.execute(sql, val)
        db.commit()
        return "Record Deleted!"
    except mysql.connector.Error as err:
        return f"Error: {err}"



def update_data(cur, db, item_id, item_name=None, quantity=None, price=None, category=None):
    try:
        cur.execute("SELECT COUNT(*) FROM Data WHERE item_ID = %s", (item_id,))
        if cur.fetchone()[0] == 0:
            return f"Record with item_ID {item_id} does not exist!"
        
        sql = "UPDATE Data SET "
        updates = []
        values = []
        if item_name:
            updates.append("item_name = %s")
            values.append(item_name)
        if quantity:
            updates.append("quantity = %s")
            values.append(quantity)
        if price:
            updates.append("price = %s")
            values.append(price)
        if category:
            updates.append("category = %s")
            values.append(category)

        sql += ", ".join(updates) + " WHERE item_ID = %s"
        values.append(item_id)

        cur.execute(sql, tuple(values))
        db.commit()
        return "Record Updated!"
    except mysql.connector.Error as err:
        return f"Error: {err}"


def search_data(cur, item_id=None, item_name=None, category=None):
    try:
        cur.execute("SELECT COUNT(*) FROM Data WHERE item_ID = %s", (item_id,))
        if cur.fetchone()[0] == 0:   # returns a tuple
            return f"Record with item_ID {item_id} does not exist!"
        
        sql = "SELECT * FROM Data WHERE "
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

        sql += " AND ".join(criteria)

        cur.execute(sql, tuple(values))
        results = cur.fetchall()
        return results
    except mysql.connector.Error as err:
        return f"Error: {err}"


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
        create_data(cur)
        result = add_data(cur, db, item_id, item_name, quantity, price, category)
        flash(result)
    return render_template("adding.html")


@app.route("/removing", methods=['GET', 'POST'])
def removing():
    if request.method == 'POST':
        item_id = request.form['itemID']
        create_data(cur)
        result = remove_data(cur, db, item_id)
        flash(result)
    return render_template("removing.html")



@app.route("/update", methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        item_id = request.form['itemID']
        item_name = request.form['itemName']
        quantity = request.form['quantity']
        price = request.form['price']
        category = request.form['category']
        create_data(cur)
        result = update_data(cur, db, item_id, item_name, quantity, price, category)
        flash(result)
    return render_template("update.html")

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        item_id = request.form['itemID']
        item_name = request.form['itemName']
        category = request.form['category']
        create_data(cur)
        result = search_data(cur, item_id, item_name, category)
        if isinstance(result, list):
            flash("Search successful!")
            return render_template("result.html", results=result)
        else:
            flash(result)
            return redirect(url_for('/'))
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)