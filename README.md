->-> for Windows

1. Download the Zip file from the github link then extract all the files in your designed folder

2. Open the Project:
            Click on "File" -> "Open Folder" and select the folder containing your project.

3. Open Terminal:
            In VS Code, click on "View" -> "Terminal" to open the integrated terminal.

4. Navigate to Project Directory:
  Use the `cd` command to navigate to your project directory
   
6. Create Virtual Environment:
    Run the following command to create a virtual environment: python -m venv venv
   
8. Activate Virtual Environment:
               Activate the virtual environment:  source venv/bin/activate
         
 You should see (`venv`) in the terminal prompt, indicating the active virtual environment.

7. Install Dependencies:
               Now, you can install the required packages within the virtual environment:  pip install flask pydub moviepy tgt python-docx

8. Run the Application:
               Run your Flask application as before:  python app.py
      
The server should start, and you can access the application in your web browser at `http://127.0.0.1:5000/`.

