# Import the Flask application instance from the VertechX module
from VertechX import app



# Check if the script is being run directly (as the main program)
if __name__ == '__main__':
    # Start the Flask development server with debug mode enabled
    app.run(debug=1)
