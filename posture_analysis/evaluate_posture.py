from logic.rep_counter import SquatAnalyzer, PushupAnalyzer
from logic.timer_utils import PlankTimer

def evaluate_posture(pose_landmarks, exercise_type, analyzer=None, timer=None):
    """
    Evaluate posture and return: feedback_text, rep_count, incorrect_count, accuracy_score.
    """

    if pose_landmarks is None:
        return "", 0, 0, 0

    feedback_text = ""
    accuracy_score = 0
    rep_count = 0
    incorrect_count = 0

    if exercise_type == "Squat" and analyzer:
        feedback_text, rep_count, incorrect_count, accuracy_score = analyzer.analyze(pose_landmarks)

    elif exercise_type == "Pushup" and analyzer:
        feedback_text, rep_count, incorrect_count, accuracy_score = analyzer.analyze(pose_landmarks)

    elif exercise_type == "Plank" and timer:
        feedback_text, timer_state = timer.update(pose_landmarks)
        accuracy_score = timer.get_accuracy_score()
        rep_count = timer.get_elapsed_time()
        incorrect_count = timer.incorrect_hold_count

    return feedback_text, rep_count, incorrect_count, accuracy_score
