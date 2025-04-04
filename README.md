# Chatbot 🤖

A Flask-based chatbot for DigiDARA Technologies, designed to assist users by collecting information (name, email, phone, course interest, duration) and providing free chat and enquiry submission features. The chatbot leverages Ollama (phi4-mini model) for natural language responses and SQLite for data storage. It features an interactive frontend with checkboxes for course and duration selection, making it user-friendly and efficient.

## 🚀 Features
**User Information Collection**: Collects name, email, phone, course interest, and duration with a step-by-step conversational flow.
**Checkbox Selection**: Allows users to select courses and durations using checkboxes for a seamless experience.
**Formatted Course and Duration Lists**: Displays course and duration options with serial numbers (S.No) and newlines for better readability.
**Free Chat**: Supports open-ended conversations using Ollama's phi4-mini model for natural language responses.
**Enquiry Submission**: Users can submit enquiries, which are saved to a SQLite database.
**Responsive Frontend**: A clean, modern chat widget with HTML, CSS, and JavaScript, integrated into the website’s chat icon.
**Database Integration**: Stores user information and enquiries in a SQLite database (users.db).

## 📂 Project Structure
```
digidara-chatbot/
│
├── .gitignore              # Git ignore file to exclude sensitive files
├── Modelfile               # Ollama model configuration (optional)
├── app.py                  # Flask backend handling chatbot logic
├── database.py             # SQLite database logic for storing user information
├── package.json            # Node.js dependencies (optional, if used)
├── package-lock.json       # Node.js dependency lock file (optional, if used)
├── public/                 # Frontend files
│   ├── index.html          # Main chat widget (HTML, CSS, JavaScript)
│   ├── script.js           # JavaScript logic for the chat widget
│   └── styles.css          # CSS styles for the chat widget
├── requirements.txt        # Python dependencies
├── server.js               # Node.js server (optional, if used)
└── README.md               # Project documentation
```
**Note**: The SQLite database (users.db) is excluded from the repository via .gitignore to prevent sensitive data from being uploaded. It will be created automatically when you run the app for the first time.

## 🛠️ Setup Instructions
Follow these steps to set up and run the chatbot locally.

### Prerequisites
  - **Python 3.7+**: Ensure Python is installed on your system.
  - **Git**: To clone the repository.
  - **Ollama**: For natural language processing (phi4-mini model).
  - **Node.js (optional)**: If you’re using the server.js file for a Node.js-based frontend.

### 1. Clone the Repository
```bash
git clone https://github.com/Ranjeeth11/Chatbot.git
cd Chatbot
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

This installs the required Python packages:

flask
requests
beautifulsoup4
flask-cors

### 3. Set Up Ollama
Ollama is used for natural language responses. You’ll need to run Ollama on a separate server or locally.

  1. **Install Ollama**: ```bash curl -fsSL https://ollama.com/install.sh | sh ```
  2. **Start Ollama**: ```bash ollama serve ```
  3. **Pull the phi4-mini Model**: ```bash ollama pull phi4-mini ```
  4. **Update the Ollama URL in app.py**: Open app.py and update the run_ollama function with the correct URL of your Ollama server: ```python response = requests.post( "http://<your-ollama-server-ip>:11434/api/generate", ... ) ``` If running locally, use http://localhost:11434/api/generate.

### 4. Run the Chatbot
```bash
python app.py
```

### 5. Access the Chatbot
  - Open your browser and navigate to http://localhost:5000.
  - The chat widget will appear, and you can start interacting with the chatbot.

## 🌐 Deployment on GoDaddy
To deploy the chatbot on GoDaddy (e.g., on a subdomain like chatbot.digidaratechnologies.com) and integrate it with your website (digidaratechnologies.com), follow these steps.

### 1. Deploy the Flask App on GoDaddy
  1. Set Up a Subdomain:
     - In cPanel, go to "Domains" → "Create a New Domain."
     - Create a subdomain, e.g., chatbot.digidaratechnologies.com.
     - Set the document root to /home/username/chatbot.
  2. Set Up the Python App:
     - In cPanel, go to "Setup Python App" → "Create Application":
         - Python Version: Select the highest available (e.g., 3.7 or later).
         - Application Root: /home/username/chatbot.
         - Application URL: chatbot.digidaratechnologies.com.
         - Application Startup File: passenger_wsgi.py.
         - Application Entry Point: application.
         - Passenger Log File: /home/username/logs/chatbot.log.
    - Click "Create."
  3. Create passenger_wsgi.py:
     ```python
     import sys
     import os
     sys.path.insert(0, os.path.dirname(file))
     from app import app as application
     ```
  4. Upload Files:
       - In cPanel, go to "File Manager" → /home/username/chatbot.
       - Upload:
           - app.py
           - database.py
           - passenger_wsgi.py
           - requirements.txt
      - Set permissions:
          - 755 for app.py, database.py, and passenger_wsgi.py.
          - 644 for requirements.txt.
  5. Install Dependencies:
       - In "Setup Python App," click "Run Pip Install" → select requirements.txt.
  6. Restart the Application:
       - Click "Restart."

### 2. Host Ollama on a Separate Server
GoDaddy shared hosting cannot run Ollama. You need to host Ollama on a separate VPS:

  1. Rent a VPS:
       - Use DigitalOcean, Linode, or another provider ($5/month, 4 GB RAM minimum).
  2. Install Ollama:
     ```bash
     curl -fsSL https://ollama.com/install.sh
     ollama serve
     ollama pull phi4-mini
      ```
  3. Expose Ollama:
       - Run Ollama on port 11434 and secure it with a firewall (allow only your GoDaddy server’s IP).
  4. Update app.py:
       - Replace http://<vps-ip>:11434/api/generate with your VPS IP.

### 3. Integrate with Your Website
Add the chat widget to your website (digidaratechnologies.com) by embedding the HTML, CSS, and JavaScript from public/index.html into your website’s main HTML file (e.g., /home/username/public_html/index.html). Update the JavaScript to point to your deployed backend (https://chatbot.digidaratechnologies.com/chat).

## 📝 Notes
- **Database**: The SQLite database (users.db) is excluded from the repository. It will be created automatically when you run the app for the first time.
- **Ollama**: Ensure you have a VPS to host Ollama, as GoDaddy shared hosting cannot run it.
- **Node.js Files**: The repository includes package.json, package-lock.json, and server.js, which suggest a Node.js setup. If these are not used, you can remove them to clean up the project.
  
## 🐛 Troubleshooting
- **CORS Error**: If you see a CORS error in the browser console, ensure flask-cors is installed and configured correctly in app.py.
- **Ollama Connection Error**: Ensure your Ollama server is running and accessible from the GoDaddy server.
- **Database Not Saving**: Check the GoDaddy logs (/home/username/logs/chatbot.log) for errors. Verify the database content:
  ```bash
  sqlite3 users.db "SELECT * FROM users"
  ```

## 🤝 Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request.

## 📧 Contact
For any questions or support, reach out to Ranjeeth.

## 📜 License
MIT License

Copyright (c) 2025 Ranjeeth

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
