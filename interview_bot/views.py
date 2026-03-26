import json
import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

QUESTIONS = {
    "ai_ml": [
        {"q": "What is the difference between supervised and unsupervised learning?", "hint": "Think about labelled vs unlabelled data, and give an example of each."},
        {"q": "Explain overfitting. How do you prevent it?", "hint": "Mention regularisation, dropout, cross-validation, more data."},
        {"q": "What is the bias-variance trade-off?", "hint": "High bias = underfitting, high variance = overfitting."},
        {"q": "How does a Random Forest differ from a single Decision Tree?", "hint": "Ensemble, bagging, feature randomness, reduced variance."},
        {"q": "Explain how gradient descent works.", "hint": "Loss surface, learning rate, step size, convergence."},
        {"q": "What evaluation metrics would you use for an imbalanced dataset?", "hint": "Precision, recall, F1-score, AUC-ROC — not just accuracy."},
        {"q": "What is transfer learning and when would you use it?", "hint": "Pre-trained models, fine-tuning, limited data scenarios."},
        {"q": "Describe the architecture of a Transformer model.", "hint": "Encoder-decoder, attention heads, positional encoding, feed-forward layers."},
        {"q": "What is BERT and how is it different from GPT?", "hint": "BERT: bidirectional encoder. GPT: autoregressive decoder."},
        {"q": "How would you handle missing data in a dataset?", "hint": "Imputation, model-based imputation, or dropping rows/cols."},
    ],
    "data_science": [
        {"q": "Walk me through how you would approach a new data science problem.", "hint": "Problem definition, data collection, EDA, modelling, evaluation, deployment."},
        {"q": "What is feature engineering? Give an example.", "hint": "Creating new features from raw data."},
        {"q": "What is PCA and when would you apply it?", "hint": "Dimensionality reduction, variance explained."},
        {"q": "Explain the difference between correlation and causation.", "hint": "Use a concrete example."},
        {"q": "How would you detect and deal with outliers?", "hint": "Z-score, IQR, visualisation, domain knowledge."},
    ],
    "python": [
        {"q": "What are Python decorators? Give an example use case.", "hint": "Functions that wrap other functions."},
        {"q": "Explain the difference between a list and a generator in Python.", "hint": "Memory usage, lazy evaluation, yield keyword."},
        {"q": "What is the GIL in Python and how does it affect multithreading?", "hint": "Global Interpreter Lock, CPU-bound vs I/O-bound tasks."},
        {"q": "How does pandas handle missing values?", "hint": "NaN, isnull(), fillna(), dropna()."},
    ],
    "behavioural": [
        {"q": "Tell me about yourself and your background in AI/ML.", "hint": "Education, key project, what you are looking for."},
        {"q": "Describe a challenging project and how you overcame obstacles.", "hint": "Use the STAR method: Situation, Task, Action, Result."},
        {"q": "Why do you want to work in AI/ML remotely?", "hint": "Flexibility, global teams, focus on outcomes."},
        {"q": "Where do you see yourself in 3 years in the AI field?", "hint": "Show ambition but realistic planning."},
        {"q": "How do you stay up to date with the rapidly changing AI landscape?", "hint": "Papers, arXiv, Hugging Face, podcasts, communities."},
    ],
}

FEEDBACK_TEMPLATES = {
    "good": ["Great answer! You covered the key points well.", "Excellent! Clear and structured response.", "Very good — you demonstrated solid understanding."],
    "ok": ["Good start! Try to add a concrete example to strengthen your answer.", "Decent answer. Consider being more specific about how this applies in practice.", "You are on the right track. Adding a real-world scenario would make this stronger."],
    "improve": ["This needs more depth. Review the hint and try again.", "Partially correct. Think about the broader context of this concept.", "You have touched on it, but there is more to explore here."],
}

def get_feedback(answer_length):
    if answer_length > 200:
        return random.choice(FEEDBACK_TEMPLATES["good"])
    elif answer_length > 80:
        return random.choice(FEEDBACK_TEMPLATES["ok"])
    else:
        return random.choice(FEEDBACK_TEMPLATES["improve"])

def index(request):
    return render(request, "chatbot/index.html")

@csrf_exempt
def get_question(request):
    if request.method == "POST":
        data = json.loads(request.body)
        category = data.get("category", "ai_ml")
        questions = QUESTIONS.get(category, QUESTIONS["ai_ml"])
        q = random.choice(questions)
        return JsonResponse({"question": q["q"], "hint": q["hint"]})
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def submit_answer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        answer = data.get("answer", "").strip()
        feedback = get_feedback(len(answer))
        score = min(10, max(1, len(answer) // 30))
        return JsonResponse({
            "feedback": feedback,
            "score": score,
            "tip": "Tip: Structure your answers using the STAR method for behavioural questions, and include concrete examples for technical ones."
        })
    return JsonResponse({"error": "POST only"}, status=405)
