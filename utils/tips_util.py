import joblib
import shap
import pandas as pd
import random

model = joblib.load("./ml/productivity_model.pkl")

explainer = shap.TreeExplainer(model)

tips_dict={
    'focus_level':{"positive":["Your focus is sharp! You seem to have good control over distractions. Keep doing what’s working for you — whether it's your environment, routines, or mindset.",
            "Excellent focus levels! This shows you're in tune with what helps you concentrate. This kind of focus is a valuable tool. Remember to also build in moments of rest to avoid burnout and honor your body's need to recharge."], 
                    "negative":["It sounds like your focus is a little scattered, and that's okay—it happens to all of us. Instead of trying to force a long work session, let's try a small act of kindness for your brain: the 'Pomodoro Technique.' Set a timer for just 25 minutes to do one task, then take a 5-minute break. This makes starting feel so much easier.",
                    "Focus is average. Keep your momentum going by setting clear priorities for the day and doing the hardest task first. Short breaks every hour can boost productivity."]},

    'mood_level':{"positive":["Great mood levels! Positive emotions build resilience. Keep fueling this through gratitude, meaningful connections, or purpose-driven activities.",
                    "It’s so good to hear that you're in a positive space. This is a testament to the work you're doing. Focusing on gratitude can help you build resilience and continue to nurture this feeling.",
            "You’re in a great emotional space. This is a moment to celebrate. Pay attention to what uplifts you and how that feels in your body. Let's make more space for those things."],
                    "negative":["I hear that your mood has been a little low. It’s okay to not feel okay. Can we try a small act of self-kindness? This isn't about forcing yourself to be happy, but about giving yourself a moment of comfort. Maybe it's listening to a song you love, stepping outside for a minute, or just gently noticing how you're feeling without trying to change it.", 
                        "Your mood is dipping, let's see if we can add a little positive momentum. Think of one thing that you've been putting off that would bring you a small spark of joy—maybe calling a friend or spending 10 minutes on a hobby. Don't worry about the outcome, just enjoy the act of doing it."]},

    'overthinking_level':{'positive':["It sounds like you're trusting your decisions. That's a rare and powerful skill. Notice how this mental clarity feels. Let's lean into that trust and keep moving forward.",
            "You’re not getting caught in loops of overthinking, and that's fantastic. This shows a deep ability to stay present. Continue to practice this mindfulness."],
                          'negative':["Overthinking overload. Try asking yourself: *Is this fact or fear?* Reframe worst-case scenarios into steps you can control. Journaling can help too."]},

    'stress_level':{'positive':["It's wonderful to hear that stress is under control. This calm is a valuable resource. How did you get here? Let's notice the boundaries you've set and the routines that are working for you. Keep honoring them.",
            "You’ve found a healthy rhythm for managing life’s pressures. That’s a huge strength. Continue to build on this by scheduling moments of calm into your day, even when you don't feel stressed."],
                    'negative':["It sounds like stress is feeling pretty high. Let's pause and give your nervous system a break. Your body is trying to tell you something. Before you do anything else, try a grounding exercise. Put your feet on the floor and feel the ground beneath you. Then, slowly take three deep, calming breaths. This helps you reconnect with the present moment and find a sense of control.",
                                "I can sense some tension. Let's try to gently identify what's weighing on you. Sometimes, just writing it down can help. Take a minute and do a 'Brain Dump': write down everything that's on your mind. Don't worry about grammar or order, just get it all out. It's about creating space in your mind, not solving the problems immediately."]},

     'procrastination_level':{'positive':["You’re a person of action! That’s so impressive. What's one thing you can do right now to keep that momentum going? Your discipline is creating great results."],
                             'negative':["Procrastination alert. Instead of aiming for perfect, aim to just begin. Ask yourself: *What’s the smallest step I can take right now?* Even 5 minutes helps.",
                                         "It's common to put things off, especially when they feel big and overwhelming. Let's try to change the goal from 'finishing' to just 'starting.' Can you commit to working on that task for just one minute? Don't worry about doing it well. The goal is just to break the ice and prove to yourself that you can begin."]},

    'sleep_quality':{'positive':["You're getting great sleep! That's a huge sign of health and balance. Keep your routine consistent—even on weekends— to protect this valuable habit.",
            "That's fantastic. Quality sleep is the foundation for mental clarity and emotional resilience. Give yourself a pat on the back for prioritizing rest.",],
                     'negative':["Sleep is okay but has room to improve. Aim to sleep and wake at the same time daily. Reduce light at night, especially from screens.",
                                 "I'm concerned about your sleep. Poor sleep affects everything—from your mood to your ability to think clearly. It's not about being perfect, but about creating a more restful environment. Try a 'Digital Sunset' tonight. Turn off all screens an hour before bed. Your brain needs time to wind down without all that stimulating blue light."]},

    'screen_time':{'positive':["Healthy screen usage detected. Staying mindful about screen time boosts productivity and mental clarity.",
            "Your screen time is under control, and that's a huge win. Your focus and sleep will thank you for setting these healthy boundaries.",],
                   'negative':["It sounds like screen time is a big part of your day, and it's easy to get lost in the scroll. How does it feel when you put the phone down? Let's try a small challenge. When you're standing in line or in an elevator, keep your phone in your pocket. Use that time to just observe your surroundings and practice being present.",
                               "Moderate screen time. Be mindful of the content you consume. Try the 20-20-20 rule for eye health: every 20 mins, look 20 feet away for 20 seconds."]},

    'exercise_level':{'positive':["You have strong exercise habits. That's so good for your mental and physical health. What helps you stay consistent? Keep connecting with the feeling you get from moving your body and use that as motivation.",
            "You're physically active, and that's wonderful. Regular movement is medicine for both the body and mind. It helps with mood, energy, and resilience.",
            "You're moving your body, and that's a fantastic start! To build on this, let's explore what kind of movement feels good to you. Is it dancing? A walk in nature? A gentle yoga class? Finding joy in movement can make it something you look forward to, rather than a chore."],
                      'negative':["I notice that physical activity hasn’t been your priority lately, and that's okay. Let's not call it 'exercise.' Can we just think about 'movement'? The goal is just to feel your body. Maybe you can stretch for 5 minutes in the morning or walk around the block after dinner. Let's start with just a few minutes, with no pressure to make it a big workout."]},
    
    'hydration_liters':{'positive':["You're well-hydrated! That's so good for your skin, energy, and digestion. Keep up this great habit!",
            "Hydration goals met! Your body and brain perform so much better when they’re fueled by enough water. Keep sipping through the day."],
                        'negative':["I'm noticing that your water intake is quite low. This can affect your energy and concentration more than you think. Let's try to gently increase it. Can you get a water bottle and keep it in your sight all day? Just having it there will encourage you to take sips and build a new habit.",
                                    "You're almost at a healthy level of hydration. Let's try to get you there. Can you make a rule for yourself: 'Every time I finish a meal, I'll have a glass of water'?"]},

    'junk_food_intake':{'positive':["You’re fueling yourself with healthy foods, and that’s a wonderful investment in your well-being. Notice how these foods make you feel, and keep listening to your body.",
            "You're eating so well! A balanced diet supports your brain function and emotional regulation. Keep it fresh and colorful!"],
                        'negative':["I hear that you're relying on more processed or outside foods. Instead of judging yourself for this, let's try to understand it. When do you find yourself reaching for these foods? Is it when you're stressed, tired, or just busy? Let's aim for a small change: can you try to prepare just one more meal at home this week? It's not about being perfect, just about making a small, intentional shift."]}
}

def generate_tips(user_input: pd.DataFrame, top_n=5):
    shap_values = explainer.shap_values(user_input)

    feature_names = user_input.columns
    impacts = list(zip(feature_names, shap_values[0]))
    impacts_sorted = sorted(impacts, key=lambda x: abs(x[1]), reverse=True)

    tips = []
    used_msgs = set()

    for feature, impact in impacts_sorted:
        if feature not in tips_dict:
            continue

        sentiment = "positive" if impact >= 0 else "negative"
        msg = random.choice(tips_dict[feature][sentiment])

        if msg not in used_msgs:
            tips.append({
                "text": msg,
                "type": sentiment
            })
            used_msgs.add(msg)

        if len(tips) >= top_n:
            break

    return tips