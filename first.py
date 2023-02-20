from flask import Flask, request
from sizing_charts import sizing_charts 

# Define the Flask app
app = Flask(__name__)

@app.route('/')
def home():
    # Define the HTML code for the homepage
    html = """
    <script>
        function showFields() {
            var select = document.getElementById("clothing_type");
            var shirtsFields = document.getElementById("shirts_fields");
            var pantsFields = document.getElementById("pants_fields");

            if (select.value == "shirts") {
                shirtsFields.style.display = "block";
                pantsFields.style.display = "none";
            } else if (select.value == "pants") {
                shirtsFields.style.display = "none";
                pantsFields.style.display = "block";
            }
        }
    </script>

    <form action="/results" method="POST">
        <label for="clothing_type">Select a clothing type:</label>
        <select name="clothing_type" id="clothing_type" onchange="showFields()">
            <option value="shirts">Shirts</option>
            <option value="pants">Pants</option>
        </select><br><br>

        <div id="shirts_fields">
            <label for="chest">Chest measurement:</label>
            <input type="number" name="chest" id="chest"><br>
            <label for="waist">Waist measurement:</label>
            <input type="number" name="waist" id="waist"><br>
         </div>

        <div id="pants_fields">
            <label for="waist">Waist measurement:</label>
            <input type="number" name="waist" id="waist"><br>
            <label for="inseam">Inseam measurement:</label>
            <input type="number" name="inseam" id="inseam"><br><br>
        </div>

        <input type="submit" value="Submit">
    </form>
    """
    
    # Return the HTML code for the homepage
    return html
# Define the route for the results page
@app.route('/results', methods=['POST'])
def results():
# Get the user's measurements and selected clothing type
    clothing_type = request.form['clothing_type']
    if clothing_type == 'shirts':
        chest = request.form['chest']
        waist = request.form['waist']
        if not all([chest, waist]):
            return "Please enter values for chest and waist."
        measurements = {
            'chest': float(chest),
            'waist': float(waist),
        }
    elif clothing_type == 'pants':
        waist = request.form['waist']
        inseam = request.form['inseam']
        if not all([waist, inseam]):
            return "Please enter values for chest, waist, and inseam."
        measurements = {
            'waist': float(waist),
            'inseam': float(inseam)
        }
    else:
        return "Invalid clothing type."
    # Find the user's size based on their measurements and the sizing chart
    size = None
    for key, value in sizing_charts[clothing_type].items():
        if all(measurements[k] >= v for k, v in value.items()):
            size = key
            break
    
    comment = ""
    if size == "XS":
        comment = "You need to eat more stupid bitch!"
    elif size == "S":
        comment = "You're 1!"
    elif size == "M":
        comment = "You're 2!"
    elif size == "L":
        comment = "You're too fat you 3!"
    elif size == "XL":
        comment = "You're too fat you fuck!"
    
    html = f"""
        <p>Your size is: {size}</p>
        <p>{comment}</p>
    """
    return html
# Run the app
if __name__ == '__main__':
    app.run(debug=True)