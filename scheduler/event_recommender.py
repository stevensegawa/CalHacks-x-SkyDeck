from openai import OpenAI
from google_calendar import create_recommended_event
import json
import os

def event_recommender(
        csv_file: str,
        prompt: str,
) -> str:
    os.environ["OPENAI_API_KEY"] = "sk-proj-7Fvjyy6R1HzENEQmXRECT3BlbkFJ5IKW1tl8vpcvnsiHYRoe"

    client = OpenAI()
    csv_file = csv_file
    file = client.files.create(
    file=open(csv_file, "rb"),
    purpose='assistants'
    )

    potential_events = 'Napping, Yoga, Workout, Morning Walk, Running, Strength Training, Meditation, Journaling, Sun Bathing, Cold Shower, Intermittent Fasting'

    assistant = client.beta.assistants.create(
    name="Data visualizer",
    instructions=f"You recommend when to schedule events in Google Calendar for health wellness suggestions based on the person's Health Data in the CSV file given to you. These events should aim to improve potential deficiencies or problems from the health statistic, based on what is needed most. Only schedule ONE SPECIFIC future event and include the following information in your response and nothing else: Event Name, Location, Description, Start Time and Date, End Time and Date. The event should be chosen from one of the following options: {potential_events} Analyze the average wakeup and bedtime hours to ensure the event is within the person's average waking hours. For the description, write 1-3 sentences of reasoning CITING SPECIFIC DATES within the past week or month AND DATA POINTS from the CSV file to justify why you are recommending this activity. Examples of this would include number of steps yesterday: 1000 or daily heart rate percent increase over the past week: 5 percent or average sleep duration over the past month: 6 hours or daily protein intake over the past week: 30g. This data should be reasonable for a human. Do not use any bold, italics, etc. in the response. For both the Time and Date entries make it sure it is close to the current date June 22nd, 2024 at 11PM, base the formatting off of this example -- 2024-06-24T09:00:00-07:00",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}],
    tool_resources={
        "code_interpreter": {
        "file_ids": [file.id]
        }
    }
    )

    thread = client.beta.threads.create(
    messages=[
        {
        "role": "user",
        "content": prompt,
        "attachments": [
            {
            "file_id": file.id,
            "tools": [{"type": "code_interpreter"}]
            }
        ]
        }
    ]
    )

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions=f"You recommend when to schedule events in Google Calendar for health wellness suggestions based on the person's Health Data in the CSV file given to you. These events should aim to improve potential deficiencies or problems from the health statistic, based on what is needed most. Only schedule FOUR SPECIFIC future events and include the following information in your response and nothing else: Event Name, Location, Description, Start Time and Date, End Time and Date. The events should be chosen from one of the following options: {potential_events} The events should be between 30, 60, or 90 minutes long. Put a title at the top called Events. Analyze the average wakeup and bedtime hours to ensure the event is within the person's average waking hours. For the description, write 2-3 sentences of reasoning CITING SPECIFIC DATES within the past week or month of the current year AND DATA POINTS from the CSV file to justify why you are recommending this activity. DO NOT REFERENCE ANYTHING BEFORE THIS MONTH. Examples of this would include number of steps yesterday: 1000 or daily heart rate percent increase over the past week: 5 percent or average sleep duration over the past month: 6 hours or daily protein intake over the past week: 30g. This data should be reasonable for a human. Do not use any bold, italics, etc. in the response. For both the Time and Date entries make it sure it is close to the current date June 23rd, 2024 at 12AM, base the formatting off of this example -- 2050-06-24T09:00:00-07:00",
    )

    if run.status == 'completed': 
        messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
    else:
        print(run.status)

    response = messages.data[0].content[0].text.value

    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are taking in a string with four events intended to be converted into JSON. Create a list storing the four events and call the feature Events. Please only get the following fields: Event Name, Location, Description, Start Time and Date, End Time and Date"},
            {"role": "user", "content": response}
        ]
    )
    json_response = response.choices[0].message.content
    return json_response

def csv_to_event(csv_path):
    text_response = event_recommender(
        csv_file = csv_path,
        prompt = 'Give me suggestions.',
    )

    document = json.loads(text_response)
    for event in document["Events"]:
        create_recommended_event(
            event_name = event['Event Name'],
            location = event['Location'],
            description = event['Description'],
            start_timedate = event['Start Time and Date'],
            end_timedate = event['End Time and Date'],
        )
    return text_response

def main():
    text_response = event_recommender(
        csv_file = 'Health Data/merged_health_data_first.csv',
        prompt = 'Give me suggestions.',
    )
    print(text_response)

    document = json.loads(text_response)
    for event in document["Events"]:
        create_recommended_event(
            event_name = event['Event Name'],
            location = event['Location'],
            description = event['Description'],
            start_timedate = event['Start Time and Date'],
            end_timedate = event['End Time and Date'],
        )

if __name__ == "__main__":
    main()