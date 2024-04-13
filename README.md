# ChatBot Setup

# Create VirualEnv

 - `python -m venv venv`
 
 # Activate VirtualEnv and Deactivate VirtualENV
 
 - Activate for windows
	 - source venv/Scripts/Activate
 - Activate for ubnutu
	 - source venv/bin/activate
# Install Requirement
- `pip install -r requirement.txt`
	
#  Create PostgresSQL Database 
- `ai_bot_flask`

# Create Extension 
- Follow the link for create extension for embedding data
- `https://dev.to/bkmalan/how-to-add-pgembedding-extension-to-postgresql-2ii6`    

# Migrate the database 
	     - Activate Venv for windows
			 - source venv/Scripts/Activate
		 - Activate Venv for ubnutu
			 - source venv/bin/activate
		 - set veriable in venv
			 - export FLASK_APP = app.py
		 - Migrate Databse follow command
			 - flask db init
			 - flask db migrate
			 - flask db upgrade 	
# Set the OPENAI_KEY and PGADMIN_URL
- In this project structure config_template.py into config folder you can simpliy add the OPENAI_KEY="ai_key" and 
  PGADMIN_URL="pgadmin_url (ex:postgresql+psycopg2://username:password@localhost:5432/dbname)"

# Git .gitignore 
- Here all mention file git ignore does not push on repo
	- __pycache__ file containe cache file it auto created  
	- config file containe private key so does not provide to remote directory  

# Run the FLASK APP 
- Run Debug mode :
	- `flask --app app --debug run`
- Run Normal : 
	- `flask run`



