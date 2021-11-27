# CS-6360-Project
Online auction site for CS 6360

## How to Run
1. Install python 3.
2. Install pip and set the path of the pip. 
3. Execute: `pip install -r requirements.txt`. 
4. Download the github repository: `git clone https://github.com/ez314/CS-6360-Project.git`. 
5. [Create `config.json`](#configuration)
6. Execute main.py: `python main.py` (or use `python3` if `python` links to Python 2)
7. 

## Configuration
Right now, the config file just contains information for connecting to the local MySQL database. 

1. Create a duplicate of `config.example.json` called `config.json`.  
2. Fill in the configuration values to fit your MySQL setup.

Do not commit the `config.json` file! It contains your password.