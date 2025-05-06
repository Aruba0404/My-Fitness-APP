from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from logic.timer_utils import PlankTimer

def evaluate_posture(pose_landmarks, exercise_type, analyzer=None, timer=None):
    """
    Evaluate posture and return feedback_text and rep_count only.
    """

    if not pose_landmarks or len(pose_landmarks) == 0:
        return "No landmarks detected", 0

    feedback_text = ""
    rep_count = 0

    if exercise_type == "Squat" and isinstance(analyzer, SquatAnalyzer):
        rep_count, feedback_text = analyzer.update(pose_landmarks)

    elif exercise_type == "Pushup" and isinstance(analyzer, PushupAnalyzer):
        rep_count, feedback_text = analyzer.update(pose_landmarks)

    elif exercise_type == "Plank" and isinstance(timer, PlankTimer):
        feedback_text = timer.update(pose_landmarks)
        rep_count = timer.get_elapsed_time()

    return feedback_text, rep_count
