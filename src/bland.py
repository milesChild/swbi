# imports
import requests
from typing import Optional, List, Dict, Any

MODELS = [
    "enhanced",
    "turbo"
]

class Bland:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def heartbeat(self):
        """
        Send a heartbeat to the Bland API to test / keep the connection alive.
        """
        pass

    def __connect(self):
        """
        Connect to the Bland API.
        """
        pass

    def __disconnect(self):
        """
        Disconnect from the Bland API.
        """
        pass

    def __get_headers(self):
        """
        Get the headers for the Bland API.
        """
        return {
            "authorization": self.api_key,
            "Content-Type": "application/json"
        }

    def call(self,
             phone_number: str,
             pathway_id: Optional[str] = None,
             task: Optional[str] = None,
             voice: Optional[str] = None,
             background_track: Optional[str] = None,
             first_sentence: Optional[str] = None,
             wait_for_greeting: Optional[bool] = True,
             block_interruptions: Optional[bool] = None,
             interruption_threshold: Optional[int] = None,
             model: Optional[str] = "enhanced",
             temperature: Optional[int] = None,
             keywords: Optional[List[str]] = None,
             pronunciation_guide: Optional[List[Dict[str, Any]]] = None,
             transfer_phone_number: Optional[str] = None,
             transfer_list: Optional[Dict[str, Any]] = None,
             language: Optional[str] = None,
             pathway_version: Optional[int] = None,
             local_dialing: Optional[bool] = None,
             voicemail_sms: Optional[bool] = None,
             dispatch_hours: Optional[Dict[str, Any]] = None,
             sensitive_voicemail_detection: Optional[bool] = None,
             noise_cancellation: Optional[bool] = None,
             ignore_button_press: Optional[bool] = None,
             language_detection_period: Optional[int] = None,
             language_detection_options: Optional[List[str]] = None,
             timezone: Optional[str] = None,
             request_data: Optional[Dict[str, Any]] = None,
             tools: Optional[List[Dict[str, Any]]] = None,
             start_time: Optional[str] = None,
             voicemail_message: Optional[str] = None,
             voicemail_action: Optional[Dict[str, Any]] = None,
             retry: Optional[Dict[str, Any]] = None,
             max_duration: Optional[int] = None,
             record: Optional[bool] = None,
             from_call: Optional[str] = None,
             webhook: Optional[str] = None,
             webhook_events: Optional[List[str]] = None,
             metadata: Optional[Dict[str, Any]] = None,
             analysis_preset: Optional[str] = None,
             ):
        """
        Initiate a call using the Bland.ai API.

        Args:
            phone_number (str): The phone number to call (E.164 format recommended)
            pathway_id (str, optional): The ID of the pathway to use for the call
            task (str, optional): Natural language description of what the AI should do on the call
            voice (str, optional): The voice to use for the call (default is "rachel")
            background_track (str, optional): URL of background music/audio to play during the call
            first_sentence (str, optional): First sentence the AI should say when the call connects
            wait_for_greeting (bool, optional): Whether to wait for a greeting before speaking
            block_interruptions (bool, optional): Whether to prevent the AI from being interrupted
            interruption_threshold (int, optional): Minimum volume threshold for interruptions (0-100)
            model (str, optional): The LLM to use (default is "gpt-4")
            temperature (int, optional): Creativity of responses (0-100)
            keywords (List[str], optional): Keywords to listen for during the call
            pronunciation_guide (List[Dict], optional): Guide for pronouncing specific words
            transfer_phone_number (str, optional): Number to transfer the call to
            transfer_list (Dict, optional): List of transfer options and their phone numbers
            language (str, optional): Language code for the call (e.g., "en-US")
            pathway_version (int, optional): Version number of the pathway to use
            local_dialing (bool, optional): Whether to use local dialing format
            voicemail_sms (bool, optional): Whether to send voicemail transcripts via SMS
            dispatch_hours (Dict, optional): Scheduling configuration for calls
            sensitive_voicemail_detection (bool, optional): Enhanced voicemail detection
            noise_cancellation (bool, optional): Whether to enable noise cancellation
            ignore_button_press (bool, optional): Whether to ignore DTMF tones
            language_detection_period (int, optional): Time to detect language in seconds
            language_detection_options (List[str], optional): List of languages to detect
            timezone (str, optional): Timezone for the call (e.g., "America/New_York")
            request_data (Dict, optional): Custom data to include in webhook requests
            tools (List[Dict], optional): Custom functions the AI can use during the call
            start_time (str, optional): When to start the call (ISO 8601 format)
            voicemail_message (str, optional): Message to leave if voicemail is detected
            voicemail_action (Dict, optional): Action to take when voicemail is detected
            retry (Dict, optional): Configuration for retry attempts
            max_duration (int, optional): Maximum duration of the call in seconds
            record (bool, optional): Whether to record the call
            from_call (str, optional): Caller ID to use for the call
            webhook (str, optional): URL to receive webhook events
            webhook_events (List[str], optional): List of events to trigger webhooks
            metadata (Dict, optional): Custom metadata for the call
            analysis_preset (str, optional): Preset configuration for call analysis

        Returns:
            Dict: Response from the API containing call details

        Raises:
            Exception: If both task and pathway_id are provided, or if the API call fails
        """

        if task and pathway_id:
            raise Exception("Cannot have task and pathway_id")
        if not task and not pathway_id:
            raise Exception("Must have task or pathway_id")
        if model and model not in MODELS:
            raise Exception("Invalid model")
        
        url = "https://api.bland.ai/v1/calls"
        payload = {
            "phone_number": phone_number,
            "pathway_id": pathway_id,
            "task": task,
            "voice": voice,
            "background_track": background_track,
            "first_sentence": first_sentence,
            "wait_for_greeting": wait_for_greeting,
            "block_interruptions": block_interruptions,
            "interruption_threshold": interruption_threshold,
            "model": model,
            "temperature": temperature,
            "keywords": keywords,
            "pronunciation_guide": pronunciation_guide,
            "transfer_phone_number": transfer_phone_number,
            "transfer_list": transfer_list,
            "language": language,
            "pathway_version": pathway_version,
            "local_dialing": local_dialing,
            "voicemail_sms": voicemail_sms,
            "dispatch_hours": dispatch_hours,
            "sensitive_voicemail_detection": sensitive_voicemail_detection,
            "noise_cancellation": noise_cancellation,
            "ignore_button_press": ignore_button_press,
            "language_detection_period": language_detection_period,
            "language_detection_options": language_detection_options,
            "timezone": timezone,
            "request_data": request_data,
            "tools": tools,
            "start_time": start_time,
            "voicemail_message": voicemail_message,
            "voicemail_action": voicemail_action,
            "retry": retry,
            "max_duration": max_duration,
            "record": record,
            "from": from_call,
            "webhook": webhook,
            "webhook_events": webhook_events,
            "metadata": metadata,
            "analysis_preset": analysis_preset
        }

        # remove everything from payload that is None
        payload = {k: v for k, v in payload.items() if v is not None}

        print(payload)
        print(self.__get_headers())

        response = requests.request("POST", url, json=payload, headers=self.__get_headers())
        response_json = response.json()
        if "status" in response_json:
            if response_json["status"] == "success":
                return response_json
            else:
                raise Exception(response.text)
        else:
            raise Exception("Failed Call: " + response.text)
    