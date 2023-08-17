from collections import defaultdict
from typing import Dict, Text
from fuzzywuzzy import fuzz
import json


class NLU:
    def __init__(self, qa_path: str, nlu_threshold: float = 0.6):
        self.nlu_threshold = nlu_threshold
        self.qa_path = qa_path
        self.load_question_set()

    def extract_intent(self, text: str) -> Dict:
        """
        1-initialize an empty dict to store extracted intents (w intent, type etc.)
        5-calc the similarity scores btwn the input and each question with fuzzy
        7-if max sem sim or fuzz match ratio >= nlu_threshold, update dict
        8-return dict of result
        """
        questions = []
        answers = []
        question_similarities = []

        for qa_set in self.questions_answers:
            question, answer = qa_set["question"], qa_set["answer"]
            questions.append(question)
            answers.append(answer)
        for question in questions:
            question_similarities.append(fuzz.ratio(text, question))
        
        max_sim = max(question_similarities)
        max_sim_index = question_similarities.index(max_sim)
        
        result = {
            "question": questions[max_sim_index],
            "answer": answers[max_sim_index],
            "similarity": max_sim,
        }

        questions_answers = []
        for i in range(len(questions)):
            qa_dict = {
                "question": questions[i],
                "answer": answers[i],
                "similarity": question_similarities[i]
            }
            questions_answers.append(qa_dict)
        
        result ["similarities"] = questions_answers

        return result

    def load_question_set(self):
        self.questions_answers = json.load(open(self.qa_path))

