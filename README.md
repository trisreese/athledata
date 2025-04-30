# AthleData: Fitness Tracking Backend

AthleData is a backend API built with FastAPI to help users track and log their workouts. It allows users to create custom routines, log individual exercises, and view progress over time.

## Features

- Create named workout routines (e.g., "Leg Day", "Push Day", "Glutes Focus")
- Log workouts with sets, reps, weight, and timestamps
- Retrieve most recent sessions for a specific routine
- View grouped workouts by routine and date
- Simple SQLite database setup

## Tech Stack

- FastAPI
- Python 3
- SQLite (via SQLAlchemy)
- Pydantic (for data validation)

## Getting Started

### Prerequisites

- Python 3.8+
- `virtualenv` or `pyenv` (recommended)

### Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/trisreese/athledata.git
   cd athledata
2. Create and activate a virtual environment
    python3 -m venv venv
    source venv/bin/activate
3. Install dependencies
    pip install -r requirements.txt
4. Run the app
    uvicorn main:app --reload
5. Open the API docs
    Visit http://127.0.0.1:8000/docs to access the auto-generated Swagger UI and test the endpoints.

API Endpoints

Method	Endpoint	Description
POST	/log_workout/	Log a new workout for a routine
GET	/recent_workouts/	Get 5 most recent workouts
POST	/routines/	Create a new routine
GET	/routines/{id}/workouts/	View workouts in a routine
GET	/grouped_workouts/	View workouts grouped by date/routine
GET	/latest_session/{routine}	Get the latest session for a routine

Future Plans

Add user authentication

Graphs and analytics for progress tracking

Frontend integration and Azure deployment


