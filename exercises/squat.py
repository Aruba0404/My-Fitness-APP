from logic.rep_counter import count_squats

def evaluate_squat_logic(landmarks):
    """
    Evaluate the squat logic, count reps, and provide feedback.
    """
    rep_count, feedback, pose_state = count_squats(landmarks)
    
    # Provide additional feedback
    if pose_state == "standing":
        feedback += " Try to lower your hips more."
    elif pose_state == "squat_down":
        feedback += " Keep your back straight."

    return rep_count, feedback
