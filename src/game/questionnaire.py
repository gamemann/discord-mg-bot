import discord
import random

from bot import Discord
from config import Config
from game import GameBase
from server import Server

class Answer():
    def __init__(self, answer: str, case_sensitive: bool = False, contains: bool = False):
        self.answer = answer
        self.case_sensitive = case_sensitive
        self.contains = contains

class Question():
    def __init__(self, question: str, answers: list[Answer], points: int = 1):
        self.question = question
        self.answers = answers
        self.points = points

class Game(GameBase):
    cur_question: Question = None
    
    def __init__(self,
        bot: Discord,
        cfg: Config,
        srv: Server,
        questions: list[Question],
        name: str = "Questionnaire",
        pick_weight: float = 50.0,
    ):
        self.bot = bot
        self.cfg = cfg
        self.srv = srv
        self.name = name
        self.pick_weight = pick_weight
        self.questions = questions
        
        super().__init__(
            bot = bot,
            cfg = cfg,
            srv = srv
        )
    
    def start(self):
        # Execute base class.
        super().start()
        
        # We need to choose a random question!
        self.cur_question = random.choice(self.questions)
        
                        
    def end(self):
        # Execute base class.
        super().end()
    
    def is_correct(self, input: str):        
        if self.cur_question is None:
            return False
        
        if "answers" not in self.cur_question:
            return False
        
        # Loop through answers
        for answer in self.cur_question["answers"]:
            if "answer" not in answer:
                continue
            
            # Strip input and answer.
            input_f = input.strip()
            answer_f = answer["answer"].strip()
            
            # Retrieve case sensitive.
            case_sensitive = False
            
            if "case_sensitive" in answer and answer["case_sensitive"]:
                case_sensitive = True
                
            # Retrieve contains.
            contains = False
            
            if "contains" in answer and answer["contains"]:
                contains = True
            
            # Check if we should lower-case.
            if not case_sensitive:
                input_f = input_f.lower()
                answer_f = answer_f.lower()
                
            # Check input and answer.
            if input_f == answer_f or (contains and input_f in answer_f):
                return True
        
        return False
    
    def process_msg(self, msg: discord.Message):
        if self.cur_question is None:
            return
        
        # Check if our content's is correct to the current question.
        try:
            if self.is_correct(msg.content):
                print("Correct answer!")
            else:
                print("Wrong answer")
        except Exception as e:
            print(e)