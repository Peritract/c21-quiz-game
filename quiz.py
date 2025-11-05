"""A CLI quiz game implemented in Python."""

from random import shuffle
from html import unescape

from requests import get

BASE_URL = "https://opentdb.com/api.php"


class Question:
    """A class that represents a single question."""

    def __init__(self, question_dict: dict):
        """Create a new question instance."""

        self.question_type = question_dict["type"]
        self.category = question_dict["category"]
        self.difficulty = question_dict["difficulty"]

        # Load question data as punctuated strings
        self.question_text = unescape(question_dict["question"])
        self.correct_answer = unescape(question_dict["correct_answer"])
        self.answers = [unescape(q)
                        for q in
                        question_dict["incorrect_answers"]]
        
        # Shuffle answers to avoid easy wins
        self.answers.append(self.correct_answer)
        shuffle(self.answers)
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"<Question ({self.category}, {self.difficulty})>"

    def display(self):
        """Display the question details."""

        # Colour code by difficulty/category

        print(self.question_text)
        for i, a in enumerate(self.answers):
            print(f"{i} - {a}")

    def validate_answer(self, other: str) -> bool:
        """Return if a given answer is correct."""
        return self.correct_answer == other


    def pose(self) -> bool:
        """Prompts the user to answer a question and returns whether
        or not they were correct."""

        self.display()

        # Get the user to type something
        user_answer = -1
        while user_answer not in range(0, len(self.answers)):
            user_answer = int(input("Enter answer number: "))
            # Add error handling
            # Extract input section to method

        # Get the actual answer from the index
        user_answer = self.answers[user_answer]

        return self.validate_answer(user_answer)


def get_questions(number: int=5,
                  difficulty: str="medium") -> list[Question]:
    """Return a set of quiz questions from the API."""
    # Manage no difficulty specified
    # Allow category selection (probably needs 1 more function)
    
    url = f"{BASE_URL}?amount={number}&difficulty={difficulty}"

    res = get(url, timeout=10)

    return [Question(q) for q in res.json()["results"]]

if __name__ == "__main__":
    
    questions = get_questions(1)

    print(questions[0].pose())
