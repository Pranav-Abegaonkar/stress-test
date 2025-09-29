# VideoSDK Load Test Documentation

This repository contains a comprehensive load testing solution for VideoSDK that creates 500 meetings with 2 participants each, simulating a high-load scenario for testing VideoSDK's performance and scalability.

## Overview

The load test creates:
- **500 meetings** (configurable)
- **2 participants per meeting** (configurable)
- **1000 total participants** (500 × 2)
- **Concurrent execution** with batching to avoid rate limiting
- **Real-time monitoring** and logging
- **Automatic recording** enabled for all meetings (120s duration)

## Project Structure

```
stress-test-1/
├── load_test.py          # Main load test script
├── api.py                # VideoSDK API wrapper
├── meeting_events.py     # Meeting event handlers
├── participant_events.py # Participant event handlers
├── setup_env.py          # Interactive environment setup
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
├── venv/                 # Virtual environment
└── LOAD_TEST_README.md  # This documentation
```

## 🚀 Quick Start Guide

### Step 1: Prerequisites
- **Python 3.8+** installed
- **VideoSDK Account** with valid token
- **Sufficient API limits** for your test size

### Step 2: Setup
```bash
# 1. Navigate to project directory
cd /path/to/stress-test-1

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure
```bash
# Option A: Interactive setup (recommended)
python setup_env.py

# Option B: Manual setup
echo "VIDEOSDK_TOKEN=your_token_here" > .env
echo "TOTAL_MEETINGS=5" >> .env
echo "PARTICIPANTS_PER_MEETING=2" >> .env
```

### Step 4: Run
```bash
python load_test.py
```

## 📋 How to Use

### Example 1: Small Test (5 calls, 2 participants each)
```bash
# In your .env file:
VIDEOSDK_TOKEN=your_token_here
TOTAL_MEETINGS=5
PARTICIPANTS_PER_MEETING=2

# Run the test:
python load_test.py
```

### Example 2: Medium Test (50 calls, 3 participants each)
```bash
# In your .env file:
VIDEOSDK_TOKEN=your_token_here
TOTAL_MEETINGS=50
PARTICIPANTS_PER_MEETING=3

# Run the test:
python load_test.py
```

### Example 3: Large Test (500 calls, 2 participants each)
```bash
# In your .env file:
VIDEOSDK_TOKEN=your_token_here
TOTAL_MEETINGS=500
PARTICIPANTS_PER_MEETING=2

# Run the test:
python load_test.py
```

## Prerequisites

1. **Python 3.8+** installed
2. **VideoSDK Account** with valid token
3. **Sufficient API limits** for creating meetings
4. **Network bandwidth** for concurrent participants

## Installation

1. **Clone or download** this repository
2. **Create virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### 1. Create Environment File

Create a `.env` file in the project root:

```bash
# VideoSDK Configuration
VIDEOSDK_TOKEN=your_videosdk_token_here

# Load Test Configuration
TOTAL_MEETINGS=500
PARTICIPANTS_PER_MEETING=2

# Optional: Performance Tuning
BATCH_SIZE=10
REQUEST_DELAY=0.1
BATCH_DELAY=2.0

# Optional: Media Settings
MIC_ENABLED=false
WEBCAM_ENABLED=false

# Optional: Logging
LOG_LEVEL=INFO
LOG_FILE=load_test.log
```

### 2. Get VideoSDK Token

1. Visit [VideoSDK Dashboard](https://app.videosdk.live/)
2. Generate a token with `allow_join` permissions
3. Copy the token to your `.env` file

## Running the Load Test

### Quick Start (Recommended)

1. **Set up your environment**:
   ```bash
   # Navigate to the project directory
   cd /path/to/stress-test-1
   
   # Activate virtual environment
   source venv/bin/activate
   
   # Set up your configuration
   python setup_env.py
   ```

2. **Run the load test**:
   ```bash
   python load_test.py
   ```

### Manual Setup

1. **Create .env file**:
   ```bash
   # Create .env file with your parameters
   echo "VIDEOSDK_TOKEN=your_token_here" > .env
   echo "TOTAL_MEETINGS=5" >> .env
   echo "PARTICIPANTS_PER_MEETING=2" >> .env
   ```

2. **Run the load test**:
   ```bash
   python load_test.py
   ```

### Customizing Parameters

You can customize the load test by modifying the `.env` file:

```bash
# Smaller test (10 meetings, 2 participants each)
TOTAL_MEETINGS=10
PARTICIPANTS_PER_MEETING=2

# Medium test (100 meetings, 3 participants each)
TOTAL_MEETINGS=100
PARTICIPANTS_PER_MEETING=3

# Large test (500 meetings, 2 participants each)
TOTAL_MEETINGS=500
PARTICIPANTS_PER_MEETING=2
```

## What the Load Test Does

### Phase 1: Meeting Creation
- Creates 500 meetings using VideoSDK API
- Uses batching (10 meetings per batch) to avoid rate limiting
- Includes delays between requests to prevent API throttling

### Phase 2: Participant Joining
- Joins 2 participants to each meeting
- Uses concurrent execution for better performance
- Processes meetings in batches to manage system resources

### Phase 3: Monitoring
- Keeps all meetings alive for monitoring
- Logs real-time statistics
- Tracks participant counts and meeting status

## Monitoring and Logs

### Console Output
The script provides real-time feedback:
```
2024-01-15 10:30:15 - INFO - Creating 500 meetings...
2024-01-15 10:30:20 - INFO - Created meeting: abc123...
2024-01-15 10:30:25 - INFO - Processing batch 1/50 (10 meetings)
2024-01-15 10:30:30 - INFO - Participant Participant-1-abc123 joined meeting abc123
```

### Log File
All events are logged to `load_test.log`:
- Meeting creation events
- Participant join/leave events
- Error messages and exceptions
- Performance metrics

### Performance Metrics
At the end of the test, you'll see:
```
Load test completed!
Duration: 120.45 seconds
Total meetings: 500
Active meetings: 500
Total participants: 1000
Meetings per second: 4.15
Participants per second: 8.30
```

## Stopping the Test

- **Graceful stop**: Press `Ctrl+C` to stop the test
- **Cleanup**: The script will automatically leave all meetings
- **Logs preserved**: All logs are saved to `load_test.log`

## Troubleshooting

### Common Issues

1. **Token Errors**
   ```
   ERROR - Failed to create meeting: 401 Unauthorized
   ```
   **Solution**: Verify your `VIDEOSDK_TOKEN` is valid and has `allow_join` permissions

2. **Rate Limiting**
   ```
   ERROR - Failed to create meeting: 429 Too Many Requests
   ```
   **Solution**: Increase `REQUEST_DELAY` and `BATCH_DELAY` in `.env`

3. **Memory Issues**
   ```
   ERROR - Out of memory
   ```
   **Solution**: Reduce `BATCH_SIZE` or `TOTAL_MEETINGS`

4. **Network Issues**
   ```
   ERROR - Connection timeout
   ```
   **Solution**: Check your internet connection and VideoSDK service status

### Performance Tuning

For better performance, adjust these parameters in `.env`:

```bash
# For faster execution (if your system can handle it)
BATCH_SIZE=20
REQUEST_DELAY=0.05
BATCH_DELAY=1.0

# For more stable execution (if experiencing issues)
BATCH_SIZE=5
REQUEST_DELAY=0.2
BATCH_DELAY=3.0
```

## Expected Results

### Successful Load Test
- All 500 meetings created successfully
- 1000 participants joined (2 per meeting)
- Meetings remain active for monitoring
- No significant errors in logs

### Performance Benchmarks
- **Meeting creation**: ~4-5 meetings per second
- **Participant joining**: ~8-10 participants per second
- **Total duration**: 2-3 minutes for 500 meetings
- **Memory usage**: ~200-500MB depending on system

## Cleanup

The script automatically cleans up when stopped:
- All participants leave their meetings
- Resources are freed
- Logs are preserved for analysis

## Support

If you encounter issues:

1. **Check logs**: Review `load_test.log` for error details
2. **Verify configuration**: Ensure `.env` file is correct
3. **Test with smaller numbers**: Try `TOTAL_MEETINGS=10` first
4. **Check VideoSDK status**: Visit VideoSDK dashboard for service status

## Next Steps

After running the load test:

1. **Analyze logs** for performance insights
2. **Monitor VideoSDK dashboard** for meeting statistics
3. **Adjust parameters** based on your needs
4. **Scale up/down** as required for your testing

---

**Note**: This load test is designed for testing VideoSDK's scalability. Ensure you have appropriate API limits and system resources before running large-scale tests.
