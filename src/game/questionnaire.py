import discord
import random
import asyncio

from bot import Discord
from config import Config
from game import GameBase
from server import Server
from utils import debug_msg

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
        
    def __eq__(self, o):
        if isinstance(o, Question):
            return self.question == o.question
        
        return False
    
    def __hash__(self):
        return hash(self.question)

class Game(GameBase):
    cur_question: Question = None
    questions_asked: list[Question] = []
    points: dict[int, int] = {}
    users_answered: list[int] = []
    
    def __init__(self,
        bot: Discord,
        cfg: Config,
        srv: Server,
        questions: list[Question],
        channels: list[int] = [],
        default_channel: int = None,
        name: str = "Questionnaire",
        pick_weight: float = 50.0,
        time_per_question = 30.0,
        min_questions_per_round = 5,
        max_questions_per_round = 10
    ):
        self.bot = bot
        self.cfg = cfg
        self.srv = srv
        self.channels = channels
        self.default_channel = default_channel
        
        # If we don't have a default channel, try to pick a random channel from channels list.
        if self.default_channel is None and len(self.channels) > 0:
            self.default_channel = random.choice(self.channels)
        
        self.name = name
        self.pick_weight = pick_weight
        
        self.questions = questions
        self.time_per_question = time_per_question
        self.min_questions_per_round = min_questions_per_round
        self.max_questions_per_round = max_questions_per_round

        super().__init__(
            bot = bot,
            cfg = cfg,
            srv = srv
        )
    
    async def start(self, chan_id: int = None):
        # Execute base class.
        await super().start()
        
        # If channel is None, pick default channel.
        if chan_id is None:
            chan_id = self.default_channel
            
        # Make sure we have a channel.
        if chan_id is None:
            debug_msg(3, self.cfg, f"[Questionnaire] No channel found for game. Aborting...")
            
            return
        
        # Empty questions asked.
        self.questions_asked = []
        
        # Get max questions.
        questions_max = random.randint(self.min_questions_per_round, self.max_questions_per_round)
        
        debug_msg(3, self.cfg, f"[Questionnaire] Starting game for server #{self.srv.id} (questions => {questions_max}, per question time => {self.time_per_question})...")
        
        # Loop through amount of questions.      
        for cnt in range(questions_max):
            # Ask question.
            await self.ask_new_question(chan_id)
            
            # Make sure we got a valid question.
            if self.cur_question is None:
                break
            
            # Give it time.
            await asyncio.sleep(self.time_per_question)
            
            # Append to questions asked.
            self.questions_asked.append(self.cur_question)
            
        # Shut down game.
        await self.end()
        
    async def end(self):
        # Empty questions asked and users answered.
        self.questions_asked = []
        self.users_answered = []
        
        debug_msg(3, self.cfg, f"[Questionnaire] Ending game for server #{self.srv.id}...")
        
        # Execute base class.
        await super().end()    
        
    async def ask_new_question(self, chan_id: int):
        # We need to make sure we don't ask the same question twice in the same round!
        questions_available = [question for question in self.questions if question not in self.questions_asked]
        
        # Make sure we have more questions to pick from.
        if not questions_available:
            self.cur_question = None
            
            return
    
        # Get new question.
        self.cur_question = random.choice(self.questions)
        
        debug_msg(3, self.cfg, f"[Questionnaire] Picking new question '{self.cur_question['question']}' for server #{self.srv.id}!")
        
        # Get channel.
        chan = self.bot.get_channel(chan_id)
        
        if chan is None:
            debug_msg(3, self.cfg, f"[Questionnaire] Failed to retrieve channel #{chan_id} when sending questions for server #{self.srv.id}")
            
            return
        
        # Send the question.
        await chan.send(f"Question: {self.cur_question['question']}")
        
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
    
    async def process_msg(self, msg: discord.Message):
        if self.cur_question is None or msg.author.id == self.bot.user.id:
            return
        
        if len(self.channels) > 0 and msg.channel.id not in self.channels:
            return
        
        author_id = msg.author.id
        
        # Check if we've answered this question already.
        if author_id in self.users_answered:
            return
        
        # Check if our content's is correct to the current question.
        try:
            if self.is_correct(msg.content):
                await msg.channel.send(f"<@{author_id}> was correct!")
                
                # Add points.
                points = 1
                
                if "points" in self.cur_question:
                    points = int(self.cur_question["points"])
                    
                if author_id not in self.points:
                    self.points[author_id] = points
                else:
                    self.points[author_id] += points
                
                self.users_answered.append(author_id)
            else:
                print("Wrong answer")
        except Exception as e:
            debug_msg(0, self.cfg, f"[Questionnaire] Failed to process message due to exception.")
            debug_msg(0, self.cfg, e)