# VideoSDK Load Test - Simple Guide

This script helps you test how many people can join a single video meeting room at the same time.

## What This Does

- Creates multiple fake participants in your meeting room
- Tests if your meeting can handle many people joining at once
- Shows you how well your video system performs under load

## Step-by-Step Instructions

### Step 1: Get Your Information Ready

You need 3 pieces of information:
1. **VideoSDK Token** - Get this from your VideoSDK dashboard
2. **Meeting ID** - The room ID you want to test
3. **Number of Participants** - How many fake users you want to create (e.g., 10, 50, 100)

### Step 2: Install Required Software

**Install Python:**
- **On Mac:** Open Terminal, type `python3 --version`. If you see a version number, you're good! If not, install from: https://www.python.org/downloads/
- **On Windows:** Download Python from: https://www.python.org/downloads/ (make sure to check "Add Python to PATH" during installation)

**Install Git (if not already installed):**
- **On Mac:** Usually pre-installed. If not, install from: https://git-scm.com/download/mac
- **On Windows:** Download from: https://git-scm.com/download/win
- **On Linux:** Run `sudo apt-get install git` (Ubuntu/Debian) or `sudo yum install git` (CentOS/RHEL)

### Step 3: Download and Setup

1. **Open Terminal/Command Prompt**

2. **Clone this repository:**
   ```bash
   git clone https://github.com/yourusername/stress-test.git
   ```

3. **Navigate to the folder:**
   ```bash
   cd stress-test
   ```

4. **Install required software:**
   ```bash
   pip install -r requirements.txt
   ```

### Step 4: Create Your Settings File

1. **Create a new file** called `.env` in the same folder
2. **Add your information** to the file:
   ```
   VIDEOSDK_TOKEN=your_token_here
   MEETING_ID=your_meeting_id_here
   COUNT=10
   ```

   **Replace:**
   - `your_token_here` with your actual VideoSDK token
   - `your_meeting_id_here` with your actual meeting ID
   - `10` with how many participants you want (e.g., 20, 50, 100)

### Step 5: Run the Test

**In Terminal/Command Prompt, type:**
```bash
python3 main.py
```

**What you'll see:**
- The script will show progress messages
- It will create the number of participants you specified
- All participants will join your meeting room
- The test will keep running until you stop it

### Step 6: Stop the Test

**To stop the test:**
- Press `Ctrl + C` (on Mac) or `Ctrl + C` (on Windows)
- All fake participants will leave the meeting

## Example

Let's say you want to test with 20 participants:

1. **Create `.env` file with:**
   ```
   VIDEOSDK_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   MEETING_ID=abc123-def456
   COUNT=20
   ```

2. **Run the test:**
   ```bash
   python3 main.py
   ```

3. **You'll see output like:**
   ```
   VideoSDK Load Test - Single Room
   Meeting ID: abc123-def456
   Participant Count: 20
   
   🚀 Creating 20 participants...
   ✅ Participant 1 created successfully
   ✅ Participant 2 created successfully
   ...
   ```

## Troubleshooting

**"git: command not found" error:**
- Install Git from the links above
- On Windows, restart your computer after installing Git

**"Repository not found" error:**
- Make sure you're using the correct GitHub URL
- Check that the repository is public and accessible

**"Command not found" error:**
- Make sure Python is installed
- Try `python` instead of `python3`

**"Module not found" error:**
- Run: `pip install -r requirements.txt`

**"Token not found" error:**
- Check your `.env` file has the correct token
- Make sure there are no extra spaces

**"Meeting ID not found" error:**
- Check your `.env` file has the correct meeting ID
- Make sure there are no extra spaces

## Need Help?

If something doesn't work:
1. Check that all your information in `.env` is correct
2. Make sure Python is installed properly
3. Try with a smaller number first (like COUNT=5)
4. Check that your VideoSDK token is valid and has the right permissions
