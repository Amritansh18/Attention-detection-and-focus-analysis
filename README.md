# AI BASED FOCUS AND ATTENTION ANALYSIS SYSTEM 

## Project title and brief description

AI Based Focus and Attention Analysis System is an offline desktop application developed using computer vision techniques to analyze user focus in real time. The system captures webcam input and monitors behavioral signals such as blink rate, eye-closure duration, and face presence to generate a focus score between 0–100. The application is designed to help users improve concentration and productivity during study or work sessions while ensuring privacy through completely offline processing.

## Technology stack and tools used 
|Layer                |Technology|Purpose                           |
|:---:                |:---:     |:---:                             |
|Programming          |Python    |Core system Logic                 |
|Computer vision      |OpenCV    |webcam and frame processing       |
|AI/Landmark Detection|MediaPipe |Face and eye tracking             |
|Numerical Processing |NumPy     |Calculations and signal processing|
|Frontend             |Tkinter   |Desktop GUI                       |
|Data storage         |JSON      |Session history                   |

## Features and Functionality Implemented 

- Real-time webcam video capture
- Face and facial landmark detection
- Blink detection and counting
- Eye-closure duration tracking
- Face presence monitoring
- Rule-based focus score calculation
- Real-time focus score display
- Session timer
- Start/Stop session functionality
- Local session data storage using JSON
- Offline and privacy-preserving system

## Steps to run the project 

### Recommended Versions

| Tool | Version |
|------|---------|
| Python | 3.11 |
| MediaPipe | 0.10.14 |
| OpenCV | 4.10.0.84 |
| NumPy | 1.26.4 |

### Step 1: Install Python

Download and install Python 3.11 from the official website:
And during installation check the ADD to path checkbox

### Step 2: Verify Python Installation

Open terminal or PowerShell and run:

```
py -0
```

Python 3.11 should appear in the list of installed versions.

### Step 3: Clone and Open

```
git clone https://github.com/Amritansh18/Attention-detection-and-focus-analysis.git

cd "the cloned directory"
```

### Step 4: Create Virtual Environment

```
py -3.11 -m venv venv
venv\Scripts\activate
```

After activation, `(venv)` should appear in the terminal.

### Step 5: Install Required Libraries

```
pip install mediapipe==0.10.14
pip install opencv-python==4.10.0.84
pip install numpy==1.26.4
```

### Step 6: Run the Project

```
python main.py
```

## Team Members
|Name                     |Role                               |
|:---:                    |:---:                              |
|Member 1 (Ankit Lovanshi)|GUI & Integration                  |
|Member 2 (Ansh Gupta)    |Computer Vision & Signal Extraction|
|Member 3 (Amritansh Jain)|Focus Analysis & Documentation     |


## Screenshots

### Main GUI Window

![MainScreen](./Screenshots/main%20screen.png)

### Active Session Screen

![Active Session](./Screenshots/active%20session.png)

### Session Completion Screen

![Stopped Session](./Screenshots/stopped%20session.png)

### JSON Data Storage 

![json data 1](./Screenshots/json%20data%201.png)