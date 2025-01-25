# imports
import os
from typing import List, Optional
from dotenv import load_dotenv
from src.bland import Bland
import asyncio

# load environment variables
load_dotenv()

# # create bland client
# bland = Bland(api_key=os.getenv("BLAND_API_KEY"))

# my_task = "Just have a casual conversation with the caller about their day."



# # make call
# resp = bland.call(
#     phone_number="412-443-7255",
#     pathway_id=os.getenv("PATHWAY_ID"),
#     wait_for_greeting=True,
#     first_sentence="Hey, is this the Sportsman's Warehouse in Bellingham?"
# )

# print(resp)



class App():
    
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
    
phone_numbers = ["412-443-7255", "857-366-2214"]
first_sentences = ["Hey, is this the Sportsman's Warehouse in Bellingham?", "Hey, is this the Sportsman's Warehouse in Washington?"]

app = App(
    phone_numbers=phone_numbers, 
    first_sentences=first_sentences,
    pathway_id=os.getenv("PATHWAY_ID")
)
responses = asyncio.run(app.run())
print(responses)