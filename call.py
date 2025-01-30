# imports
import os
import pandas as pd
from typing import List, Optional
from dotenv import load_dotenv
from src.bland import Bland
import asyncio
from datetime import datetime
import time

# load environment variables
load_dotenv()

class CallApp():
    
    def __init__(self,
                 phone_numbers: List[str],
                 task: Optional[str] = None,
                 pathway_id: Optional[str] = None
                 ) -> None:
        # param integrity
        if not task and not pathway_id:
            raise ValueError("Task or pathway ID must be provided.")
        if task and pathway_id:
            raise ValueError("Task and pathway ID cannot be provided together.")
        
        self.__bland = Bland(api_key=os.getenv("BLAND_API_KEY"))
        self.phone_numbers = phone_numbers
        self.task = task
        self.pathway_id = pathway_id

    def run(self) -> List[dict]:
        responses = []
        for phone_number in self.phone_numbers:
            try:
                # Add a small delay between calls to avoid rate limiting
                time.sleep(20)  # 20 second delay
                
                kwargs = {
                    "phone_number": phone_number,
                    "task": self.task if self.task else None,
                    "pathway_id": self.pathway_id if self.pathway_id else None
                }
                response = self.call(**kwargs)
                
                # Convert error responses to a consistent format
                if isinstance(response, dict) and "error" in response:
                    responses.append({
                        "phone_number": phone_number,
                        "status": "error",
                        "message": response["error"]
                    })
                else:
                    responses.append(response)
                    
            except Exception as e:
                responses.append({
                    "phone_number": phone_number,
                    "status": "error",
                    "message": str(e)
                })
                time.sleep(30)
        
        return responses
    
    def call(self, **kwargs) -> dict:
        try:
            response = self.__bland.call(**kwargs)
            return response
        except Exception as e:
            print(f"Error calling {kwargs['phone_number']}: {e}")
            return {"error": str(e)}

phone_numbers = pd.read_csv("data/bass_pro_stores.csv", nrows=10)["Phone Number"].tolist()

app = CallApp(
    phone_numbers=phone_numbers,
    pathway_id=os.getenv("PATHWAY_ID")
)
responses = app.run()

try:
    df = pd.DataFrame(responses)
    
    time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(f"data/bland/responses_{time}.csv", index=False)
            
except Exception as e:
    print(f"Error converting responses to DataFrame: {e}")
    with open(f"data/bland/responses_{time}.txt", "w") as f:
        for response in responses:
            f.write(str(response) + "\n")
