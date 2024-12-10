Flask Application for Product Classification, counting & freshness detection
It uses Python 3.12.4 and requires dependencies specified in the requirements.txt file.

Setup Instructions :

  Prerequisites
  1. Install Python 3.12.4.
  2. Install a virtual environment tool like venv (optional but recommended).
  
  Steps to Set Up and Run
  1. Clone the Repository:
	  1. git clone https://github.com/shadowashwin/flipkart.git
	  2. cd flipkart
  
  2. Create a Virtual Environment (Optional):
		1. python -m venv venv
	  2. source venv/bin/activate    # On Linux/Mac
	  3. venv\Scripts\activate       # On Windows
  
  3. Install Required Dependencies:
		1. python -m pip install --upgrade pip
		2. python -m pip install -r requirements.txt
  
  5. Run the Application:
		1. python app.py

Directory Structure:

	.
	├── app.py               # Main Flask application
	├── best_veg_latest.pt   # Pretrained model file
	├── detect.py            # Script for running detection
	├── Dockerfile           # Docker configuration
	├── export.py            # Additional script for exporting
	├── fresh_banana.jpg     # Example image
	├── rotten_apple.jpeg    # Example image
	├── models/              # Directory containing model definitions
	├── utils/               # Utility scripts
	├── requirements.txt     # Python dependencies




