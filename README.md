# Flask Utility App

This is a lightweight Python Flask app that runs small utility tools locally on your machine.

## Project Structure
- `app.py` - Main Flask application entry point
- `templates/index.html` - HTML template rendered by the app
- `requirements.txt` - Python package dependencies
- `manual_install_requirements.txt` - External tools to install manually

## Prerequisites

- Python 3.x installed on your machine
- Required Python packages installed (see Installation below)
- Additional tools specified in `manual_install_requirements.txt` installed manually

## Installation

1. Clone this repository.

2. It is highly recommended to create and activate a Python virtual environment:

    ```
    python -m venv venv
    source venv/bin/activate    # On Windows: venv\Scripts\activate
    ```

3. Install Python dependencies via pip:

    ```
    pip install -r requirements.txt
    ```

4. Follow instructions in `manual_install_requirements.txt` to install any external tools needed.

## Running the App

Run the Flask app with:
    python app.py


The app will be available at `http://localhost:5000/`. The main page is rendered from `templates/index.html`.

## Usage

- Upload files as prompted by the various utility functionalities.
- The app converts, compresses, or processes files locally depending on the chosen utility.

## Notes

- Do not commit your virtual environment (`venv/`) to version control.
- Customize or extend utilities by editing `app.py`.
- Make sure external tools in `manual_install_requirements.txt` are installed and accessible via system PATH.

