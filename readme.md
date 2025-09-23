````markdown
# VideoSDK Dummy Moderator Worker

This repository provides a simple “dummy moderator” worker script that stays connected to a VideoSDK meeting to keep the session alive and prevent fragmented recordings. As long as the dummy moderator remains connected, VideoSDK treats the meeting as one continuous session, even if all real participants join and leave intermittently.

---

## Table of Contents

1. [Prerequisites](#prerequisites)  
2. [Installation](#installation)  
3. [Activate the Virtual Environment](#activate-the-virtual-environment)  
4. [Configure `.env`](#configure-env)  
5. [Run the Worker Script](#run-the-worker-script)  
6. [Verify Persistence](#verify-persistence)  
7. [Troubleshooting](#troubleshooting)  
8. [Contributing](#contributing)  
9. [License](#license)  

---

## Prerequisites

- **Python 3.8+**  
- `virtualenv` (optional, but recommended)  
- A valid VideoSDK account and token with `allow_join` permissions  
- Meeting ID you wish to keep alive  

---

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-org/videosdk-dummy-moderator.git
   cd videosdk-dummy-moderator
````

2. **Create a virtual environment** (optional but recommended)

   ```bash
   python3 -m venv venv
   ```

3. **Install dependencies after activating the venv**

---

## Activate the Virtual Environment

Depending on your OS/shell, run **one** of the following:

* **macOS/Linux (bash, zsh, etc.)**

  ```bash
  source venv/bin/activate
  ```

* **Windows (PowerShell)**

  ```powershell
  .\venv\Scripts\activate
  ```

> Once activated, your prompt should show `(venv)` indicating the virtual environment is in use.

### Install dependencies (after activating the venv)

With the virtual environment active, install the project dependencies:

```bash
pip install -r requirements.txt
```

---

## Configure `.env`

Create a file named `.env` in the project root with these entries:

```dotenv
VIDEOSDK_TOKEN="<your_videosdk_token>"
MEETING_ID="<your_meeting_id>"
NAME="DUMMY_MODERATOR"
```

* `VIDEOSDK_TOKEN`: Your VideoSDK token (must include `allow_join` scope).
* `MEETING_ID`: The ID of the meeting you want to keep alive.
* `NAME`: A placeholder display name for the dummy moderator (e.g., `DUMMY_MODERATOR`).

---

## Run the Worker Script

With your virtual environment activated and `.env` configured, start the dummy moderator:

```bash
python main.py
```

You should see console logs similar to:

```
TOKEN: eyJ…
adding event listener…
joining into meeting…
```

---

## Verify Persistence

1. **Join/Leave** real participants as usual (e.g., take breaks, disconnect/reconnect).
2. **Observe** that even if all real participants leave, the dummy moderator remains connected.
3. **Recordings** will now run as a single continuous session—no fragmented session IDs.

---

## Troubleshooting

* **No logs appear**:

  * Ensure your `.env` file is in the project root.
  * Double-check the format (`KEY="value"`) and that values are quoted.

* **Token rejected**:

  * Confirm your `VIDEOSDK_TOKEN` includes `allow_join` permissions.
  * Generate a fresh token from the VideoSDK dashboard.

* **Script crashes on start**:

  * Verify dependencies are installed: `pip install -r requirements.txt`.
  * Ensure you’re using Python 3.8+.

---