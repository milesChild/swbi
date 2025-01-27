# imports
import os
import pandas as pd
from typing import List, Optional
from dotenv import load_dotenv
from src.bland import Bland
import asyncio
from datetime import datetime

# load environment variables
load_dotenv()

class CallApp():
    
    def __init__(self,
                 phone_numbers: List[str],
                 first_sentences: List[str],
                 task: Optional[str] = None,
                 pathway_id: Optional[str] = None
                 ) -> None:
        # param integrity
        if len(phone_numbers) != len(first_sentences):
            raise ValueError("Phone numbers and first sentences must be the same length.")
        if not task and not pathway_id:
            raise ValueError("Task or pathway ID must be provided.")
        if task and pathway_id:
            raise ValueError("Task and pathway ID cannot be provided together.")
        
        self.__bland = Bland(api_key=os.getenv("BLAND_API_KEY"))
        self.phone_numbers = phone_numbers
        self.first_sentences = first_sentences
        self.task = task
        self.pathway_id = pathway_id

    async def run(self) -> List[dict]:
        responses = []
        tasks = []
        for phone_number, first_sentence in zip(self.phone_numbers, self.first_sentences):
            kwargs = {
                "phone_number": phone_number,
                "first_sentence": first_sentence if first_sentence else None,
                "task": self.task if self.task else None,
                "pathway_id": self.pathway_id if self.pathway_id else None
            }
            tasks.append(self.call(**kwargs))
        
        # Wait for all calls to complete
        responses = await asyncio.gather(*tasks)
        return responses
    
    async def call(self, **kwargs) -> dict:
        # Assuming Bland.call is a synchronous operation, we'll run it in a thread pool
        response = await asyncio.to_thread(self.__bland.call, **kwargs)
        return response

phone_numbers = pd.read_csv("data/sw_phone_numbers.xlsx")["phone_number"].tolist()

app = CallApp(
    phone_numbers=phone_numbers,
    pathway_id=os.getenv("PATHWAY_ID")
)
responses = asyncio.run(app.run())
print(responses)

# write responses to a text file in data/
time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
with open(f"data/responses_{time}.txt", "w") as f:
    for response in responses:
        f.write(str(response) + "\n")