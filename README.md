# Inventory_Management_System-FLask_Based
here’s a step-by-step guide for setting up and running this Flask application with MySQL. This guide assumes you have some basic familiarity with Python, Flask, and MySQL, but it will cover everything in detail.

### 1. **Install Required Software**

**a. Python:**
   - Ensure Python is installed. Download it from [python.org](https://www.python.org/downloads/) if needed.

**b. MySQL:**
   - Install MySQL from [mysql.com](https://dev.mysql.com/downloads/installer/).

**c. Flask and MySQL Connector:**
   - Install Flask and `mysql-connector-python` package. You can use pip to install these:

     ```sh
     pip install flask 
     ```
     ```sh
     pip install flask mysql-connector-python
     ```

### 2. **Set Up MySQL Database**
**you can setup your MySQL Database by watching any Youtube Tutorial**

### 3. Download provided folder and python file.
 - make sure to Place your CSS files (e.g., `adding.css`, `update.css`) into the `static` directory and HTML files(e.g., `adding.html`,`update.html`) into the `Templates` directory

### 3. **Configure Your Application**

**a. Update Database Credentials:**
   - Replace `USE_YOUR_USERNAME` and `USE_YOUR_PASSWORD_FOR_DATABASE` with your actual MySQL username and password in `app.py`.

**b. Set Flask Secret Key:**
   - Ensure `app.secret_key` is set to a random string (which you have already done).

### 4. **Run the Application**

**a. Initialize the Database:**
   - Ensure the `create_data(cur)` function runs to set up your database schema. It’s already called at the end of your script in the `if __name__ == "__main__":` block.

**b. Start the Flask Server:**
   - Run your Flask application with:

     ```sh
     python app.py
     ```

**c. Access the Application:**
   - Open a web browser and go to `http://127.0.0.1:5000/` to see your application running.

### 5. **Testing Your Application**

**a. Navigate Through the App:**
   - Use the dashboard to navigate to different pages (`Add`, `Remove`, `Update`, `Search`).

**b. Add Records:**
   - Test the "Add Data" page to add new records to your database.

**c. Remove Records:**
   - Test the "Remove Data" page to delete existing records.

**d. Update Records:**
   - Test the "Update Data" page to modify existing records.

**e. Search Records:**
   - Test the "Search Data" page to search for records based on criteria.

### 6. **Debugging**

If you encounter any issues:

- **Check Flask Logs:** Look at the terminal where you ran the Flask application for error messages.
- **Inspect HTML/CSS:** Ensure your HTML and CSS are correctly referenced and styled.
- **Verify Database Connection:** Ensure your MySQL connection details are correct and that the database is accessible.

If you need further assistance or run into specific issues, feel free to ask!
