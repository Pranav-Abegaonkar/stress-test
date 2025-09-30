# VideoSDK Single Room Load Test

Simple script to create multiple participants in a single meeting room for load testing.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
VIDEOSDK_TOKEN=your_videosdk_token_here
MEETING_ID=your_meeting_id_here
COUNT=10
```

## Usage

```bash
python main.py
```

## Environment Variables

- `VIDEOSDK_TOKEN` - Your VideoSDK token (required)
- `MEETING_ID` - The meeting room ID to join (required)
- `COUNT` - Number of participants to create (default: 1)

## Example

```bash
# Create 20 participants in a meeting
export VIDEOSDK_TOKEN=your_token
export MEETING_ID=abc123
export COUNT=20
python main.py
```
