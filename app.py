from flask import Flask, jsonify
import datetime
import random

app = Flask(__name__)

EXERCISES = {
    "chest": {
        "beginner": ["Push-ups 3x12", "Incline Push-ups 3x10", "Dumbbell Flyes 3x12"],
        "intermediate": ["Bench Press 4x8", "Incline Bench Press 3x10", "Cable Flyes 3x12"],
        "advanced": ["Heavy Bench Press 5x5", "Weighted Dips 4x8", "Incline DB Press 4x10", "Cable Crossover 3x15"]
    },
    "back": {
        "beginner": ["Assisted Pull-ups 3x8", "Seated Cable Row 3x12", "Lat Pulldown 3x12"],
        "intermediate": ["Pull-ups 4x8", "Bent Over Row 4x10", "Single Arm DB Row 3x12"],
        "advanced": ["Weighted Pull-ups 5x5", "Deadlift 4x6", "T-Bar Row 4x8", "Face Pulls 3x15"]
    },
    "legs": {
        "beginner": ["Bodyweight Squats 3x15", "Lunges 3x10", "Leg Press 3x12"],
        "intermediate": ["Barbell Squats 4x10", "Romanian Deadlift 3x10", "Leg Curl 3x12"],
        "advanced": ["Heavy Squats 5x5", "Bulgarian Split Squats 4x8", "Hack Squats 4x10", "Calf Raises 5x15"]
    },
    "shoulders": {
        "beginner": ["DB Shoulder Press 3x12", "Lateral Raises 3x12", "Front Raises 3x12"],
        "intermediate": ["Overhead Press 4x8", "Arnold Press 3x10", "Face Pulls 3x15"],
        "advanced": ["Heavy OHP 5x5", "DB Lateral Raises 4x12", "Rear Delt Flyes 4x12", "Shrugs 4x12"]
    },
    "arms": {
        "beginner": ["Bicep Curls 3x12", "Tricep Pushdowns 3x12", "Hammer Curls 3x12"],
        "intermediate": ["Barbell Curls 4x10", "Skull Crushers 3x10", "Preacher Curls 3x12"],
        "advanced": ["Heavy Barbell Curls 4x8", "Close Grip Bench 4x8", "Incline DB Curls 3x12", "Tricep Dips 3x12"]
    },
    "core": {
        "beginner": ["Plank 3x30s", "Crunches 3x15", "Leg Raises 3x12"],
        "intermediate": ["Hanging Knee Raises 3x12", "Cable Crunches 3x15", "Russian Twists 3x20"],
        "advanced": ["Hanging Leg Raises 4x12", "Ab Wheel 4x10", "Dragon Flag 3x8", "Weighted Plank 3x45s"]
    }
}

SPLITS = {
    "3": {
        "name": "Push/Pull/Legs (3 days)",
        "schedule": {
            "Day 1": ["chest", "shoulders"],
            "Day 2": ["back", "arms"],
            "Day 3": ["legs", "core"]
        }
    },
    "4": {
        "name": "Upper/Lower Split (4 days)",
        "schedule": {
            "Day 1": ["chest", "back"],
            "Day 2": ["legs", "core"],
            "Day 3": ["shoulders", "arms"],
            "Day 4": ["legs", "core"]
        }
    },
    "5": {
        "name": "Bro Split (5 days)",
        "schedule": {
            "Day 1": ["chest"],
            "Day 2": ["back"],
            "Day 3": ["legs"],
            "Day 4": ["shoulders"],
            "Day 5": ["arms", "core"]
        }
    },
    "6": {
        "name": "PPL x2 (6 days)",
        "schedule": {
            "Day 1": ["chest", "shoulders"],
            "Day 2": ["back", "arms"],
            "Day 3": ["legs", "core"],
            "Day 4": ["chest", "shoulders"],
            "Day 5": ["back", "arms"],
            "Day 6": ["legs", "core"]
        }
    }
}

GOALS = {
    "strength": {
        "reps": "3-6 reps",
        "sets": "4-5 sets",
        "rest": "3-5 min rest",
        "tip": "Focus on progressive overload — add weight every week"
    },
    "hypertrophy": {
        "reps": "8-12 reps",
        "sets": "3-4 sets",
        "rest": "60-90 sec rest",
        "tip": "Focus on time under tension and mind-muscle connection"
    },
    "endurance": {
        "reps": "15-20 reps",
        "sets": "3 sets",
        "rest": "30-45 sec rest",
        "tip": "Keep intensity high and rest periods short"
    }
}

MOTIVATION_QUOTES = [
    "The pain you feel today is the strength you feel tomorrow.",
    "No days off mentality. Every rep counts.",
    "Hard work beats talent when talent doesn't work hard.",
    "Be the hardest worker in the room.",
    "Your only competition is who you were yesterday.",
    "The grind never stops.",
    "Push yourself because no one else is going to do it for you.",
    "Success starts with self-discipline."
    "Pressure is a privilege."
]


@app.route("/")
def home():
    return jsonify({
        "name": "Workout Tracker API",
        "author": "kossyfa",
        "description": "Personal workout planner — splits, exercises and motivation",
        "version": "2.0.0",
        "endpoints": {
            "/split/<days>/<goal>": "Get a workout split by available days and goal",
            "/workout/<muscle>/<level>": "Get exercises for a muscle group",
            "/today/<days>/<goal>/<level>": "Get today's workout based on your split",
            "/motivation": "Get a motivational quote",
            "/goals": "See all available training goals"
        }
    })


@app.route("/split/<days>/<goal>")
def get_split(days, goal):
    if days not in SPLITS:
        return jsonify({
            "error": f"No split available for {days} days",
            "available_days": list(SPLITS.keys())
        }), 404

    if goal not in GOALS:
        return jsonify({
            "error": f"Goal '{goal}' not found",
            "available_goals": list(GOALS.keys())
        }), 404

    return jsonify({
        "split_name": SPLITS[days]["name"],
        "goal": goal,
        "training_parameters": GOALS[goal],
        "schedule": SPLITS[days]["schedule"]
    })


@app.route("/workout/<muscle>/<level>")
def get_workout(muscle, level):
    if muscle not in EXERCISES:
        return jsonify({
            "error": f"Muscle group '{muscle}' not found",
            "available": list(EXERCISES.keys())
        }), 404

    if level not in ["beginner", "intermediate", "advanced"]:
        return jsonify({
            "error": f"Level '{level}' not found",
            "available": ["beginner", "intermediate", "advanced"]
        }), 404

    return jsonify({
        "muscle_group": muscle,
        "level": level,
        "exercises": EXERCISES[muscle][level],
        "date": datetime.date.today().isoformat()
    })


@app.route("/today/<days>/<goal>/<level>")
def today_workout(days, goal, level):
    if days not in SPLITS:
        return jsonify({"error": "Invalid days", "available": list(SPLITS.keys())}), 404
    if goal not in GOALS:
        return jsonify({"error": "Invalid goal", "available": list(GOALS.keys())}), 404

    day_index = (datetime.date.today().weekday() % int(days)) + 1
    day_key = f"Day {day_index}"
    muscles_today = SPLITS[days]["schedule"].get(day_key, [])

    all_exercises = []
    for muscle in muscles_today:
        if level in EXERCISES.get(muscle, {}):
            all_exercises.extend(EXERCISES[muscle][level])

    return jsonify({
        "date": datetime.date.today().strftime("%A, %d %B %Y"),
        "day_in_split": day_key,
        "muscle_groups": muscles_today,
        "goal": goal,
        "training_parameters": GOALS[goal],
        "exercises": all_exercises,
        "motivation": random.choice(MOTIVATION_QUOTES)
    })


@app.route("/motivation")
def motivation():
    return jsonify({
        "quote": random.choice(MOTIVATION_QUOTES),
        "date": datetime.datetime.now().isoformat()
    })


@app.route("/goals")
def goals():
    return jsonify({
        "available_goals": GOALS
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

### Αρχείο 2: `requirements.txt`
```
flask==2.2.5
werkzeug==2.2.3
