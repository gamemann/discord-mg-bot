import discord

from bot import Discord
from .base import GameBase

class Answer():
    def __init__(self, answer: str, case_sensitive: bool = False):
        self.answer = answer
        self.case_sensitive = case_sensitive

class Question():
    def __init__(self, question: str, answers: list[Answer], points: int = 1):
        self.question = question
        self.answers = answers
        self.points = points

class Game(GameBase):
    cur_question: Question = None
    
    def __init__(self,
        bot: Discord,
        name: str,
        pick_weight: float,
        questions: list[Question]            
    ):
        self.bot = bot
        self.name = name
        self.pick_weight = pick_weight
        self.questions = questions
        
        super().__init__()
    
    def start(self):
        # Execute base class.
        super().start()
    
    def end(self):
        # Execute base class.
        super().end()
    
    def is_correct(self, input: str):        
        if self.cur_question is None:
            return False
        
        # Loop through answers
        for answer in self.cur_question.answers:
            # Strip input and answer.
            input_f = input.strip()
            answer_f = answer.answer.strip()
            
            # Check if we should lower-case.
            if not answer.case_sensitive:
                input_f = input.lower()
                answer_f = answer.answer.lower()
                
            # Check input and answer.
            if input_f == answer_f:
                return True
        
        return False
    
    def process_msg(self, msg: discord.Message):
        if self.cur_question is None:
            return
        
        # Check if our content's is correct to the current question.
        if self.is_correct(msg.content):
            print("Correct answer!")        