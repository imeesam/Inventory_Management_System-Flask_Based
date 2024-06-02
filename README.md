# Inventory_Management_System-FLask_Based
here's a brief description of the code,

1. Necessary modules: `Flask` for creating the web application, `render_template` for rendering HTML templates, `request` for accessing request data, `flash` for flashing messages to the user, `redirect` and `url_for` for redirecting requests, and `mysql.connector` for interacting with a MySQL database.

2. Database Connection: Connection to a MySQL database is established using `mysql.connector.connect()`. The connection details such as host, username, and password are provided you can use your own if you want to.

3. Database Operations: Functions are defined to perform various database operations:

   --> `create_data()`: Creates a database table named `Data` if it doesn't exist.
   --> `add_data()`: 	Adds a new record to the `Data` table.
   --> `remove_data()`: Removes a record from the `Data` table based on the provided item ID.
   --> `update_data()`: Updates a record in the `Data` table based on the provided item ID.
   --> `search_data()`: Searches for records in the `Data` table based on the provided criteria.

4. Routes: Different routes are defined for various functionalities of the application:

   --> `/`: 	Renders the dashboard template and handles form submissions for various operations like add, remove, update, and search.
   --> `/adding`: Renders the adding template and handles form submissions to add new records.
   --> `/removing`: Renders the removing template and handles form submissions to remove records.
   --> `/update`: Renders the update template and handles form submissions to update records.
   -->`/search`: Renders the search template and handles form submissions to search for records.

5. Templates : HTML templates are provided for each route to render the corresponding web pages with forms for user interaction.

6. Main Execution: The application will run if the script is executed directly.

7. Host: You can use 'PythonAnyWhere' for Hosting (+ point for this code)

Overall,my code defines a simple Flask web application for managing inventory data stored in a MySQL database, allowing users to add, remove, update, and search for inventory items.
