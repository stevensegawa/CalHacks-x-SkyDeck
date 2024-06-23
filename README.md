# Optifi

Hi! If you are reading this, this was our submission to the 2024 UC Berkeley AI Hackathon.

# 💥 - How it all started

As students, we always try to optimize everything from our study habits to our sleep schedules. But above all, we agreed that the most important thing to optimize was also the most neglected: health. After a careful look into the current status of health-tracking apps, we noticed a few main problems. 

A surplus of health apps: With an excessive number of health apps on the market, users can feel overwhelmed when choosing the right app for their needs while balancing trade-offs missed from other apps. This also leads to a variety of charges and memberships required for necessary health features. 

Lacks a call to action: While the mass amount of health data from wearables is beneficial, health apps lack actionable steps you can take to improve in areas you are lacking. 

Unclear impact: While metrics and health data are important, health apps fail to alert users of the severity of possible problems with their health. Users can’t differentiate a singularly bad day versus a heavy risk of depression with the current status of health apps. 


# 📖 - What it does

We built OptiFi to create a novel, multifaceted approach to creating an all-inclusive health app based on users' health data. We created four main features to fully encapsulate the main use cases of a variety of health apps shown in the slideshow above: Diagnosis, Nutrition Scanner, Health Overview, and Automated Scheduler. Using advanced data analytics, generative AI, and cloud computing, we can take health data, create personalized daily habits, and import them straight into their Google calendar. Check out the other features:

##### Diagnostic:
Based on the data collected by your wearable health data tracking device, we diagnose the user with their three most prevalent health concerns with GPT-4o. Specifically, with OpenAI Assistants we added the user’s parsed health data to the LLM’s context window. The list of worries is supplemented by its estimated risk factor to communicate the severity of the situation if any health category is lacking.

##### Nutrition Scanner:
Our app also includes a scanner that uses Anthropic’s Claude 3.5 Sonnet via the Amazon Bedrock API to analyze the amount of calories in each picture. Using the camera app on any phone, snap a picture of any food you are about to consume and let our AI log the amount of calories in that meal. In addition, utilizing OpenVINO on Intel Tiber Developer Cloud, we provide healthy food recommendations similar to the foods you like so you can be happy and healthy!

##### Health Overview:
The health overview page displays all of your important health data in one easily consumable format. The interactive page allows you to easily view your daily habits from hours slept to steps walked, all condensed into one cohesive page. Furthermore, you can talk to our live AI Voicebot Doctor to answer any questions or health concerns. It will listen to your symptoms, confirm your diagnosis, and provide steps for a path to recovery all in a hyperrealistic-sounding voice provided by ElevenLabs.

##### Automated Scheduler:
Recommends healthy activities to plan in your schedule based on your diagnosis results with GPT-4o. Automatically adds accepted events into your calendar with Google Calendar API. The scheduled event includes what it is, the location, a description explaining why it recommended this event based on citations from your health data, a start time and date, and an end time and date.


# 🔧 - How we built it

##### Building the Calendar Scheduler:
Google Cloud (gcloud): for Google account authentication to access user calendars
Google Calendar API: for managing our health calendars and events
OpenAI API (GPT-4o): for generation of event timing and details

##### Building the Nutrition Scanner:
Anthropic’s Claude-Sonnet 3.5: for computer vision to determine calories in food screenshots
AWS Amazon Bedrock API: for accessing and interfacing the vision LLM
Pillow (PIL): to perform lossless compression of food PNG image inputs
Watchdog: file system listener to access recently uploaded food screenshots to the backend

##### Collecting user fitness and health data:
Apple HealthKit: for exporting Apple watch and iPhone fitness and health data
NumPy: for math and data processing
Pandas: for data processing, organization, and storage

##### Adding personalized recommendations:
Intel Tiber Developer Cloud: development environment and compute engine
Intel OpenVINO: for optimizing and deploying the neural network model
PyTorch: for building the recommendation model with neural networks and for additional optimization

##### AI Voicebot Doctor:
Assembly AI: for transcription of the conversation (both speech-to-text and text-to-speech)
OpenAI (GPT-4o): inputs text response from user to generate an appropriate response
ElevenLabs: for realistic AI audio generation (text to speech)

##### Building our web demos:
Gradio: an open-sourced Python package with customizable UI components to demo the many different features integrated into our application


# 📒 - The Efficacy of our Models

##### Collecting health and fitness data for our app:

By exporting data from the iPhone Health app, we can gain insights into sleep, exercise, and other activities. The Apple HealthKit data is stored in an XML file with each indicator paired with a value and datetime. So we chose to parse the data to a CSV, then aggregate the data with NumPy and Pandas to extract daily user data and data clean. Our result is tabular data that includes insights on sleep cycle durations, daily steps, heart rate variability when sleeping, basal energy burned, active energy burned, exercise minutes, and standing hours. 

For aggregating sleep cycle data, we first identified “sessions”, which are periods in which an activity took place, like a sleep cycle. To do this we built an algorithm that analyzes the gaps between indicators, with large gaps (> 1hr) distinguishing between two different sessions. With these sessions, we could aggregate based on the datetimes of the sessions starts and ends to compute heart rate variability and sleep cycle data (REM, Core, Deep, Awake). The rest of our core data is combined using similar methodology and summations over datetimes to compile averages, durations, and sums (totals) statistics into an exported data frame for easy and comprehensive information access. This demonstrates our team’s commitment to scalability and building robust data pipelines, as our data processing techniques are suited for any data exported from the iPhone health app to organize as input for the LLMs context window. We chose GPT-4o as our LLM to diagnose the user’s top three most prevalent health concerns and the corresponding risk factor of each. We used an AI Assistant to parse the relevant information from the Health App data and limited the outputs to a large list of potential illnesses.

##### AI Voicebot Doctor

This script exemplifies an advanced, multi-service AI integration for real-time medical diagnostics using sophisticated natural language processing (NLP) and high-fidelity text-to-speech synthesis. The AI_Assistant class initializes with secure environment configuration, instantiating AssemblyAI for real-time audio transcription, OpenAI for contextual NLP processing, and ElevenLabs for speech synthesis. It employs AssemblyAI’s RealtimeTranscriber to capture and process audio, dynamically handling transcription data through asynchronous callbacks. User inputs are appended to a persistent conversation history and processed by OpenAI’s gpt-4o model, generating diagnostic responses. These responses are then converted to speech using ElevenLabs' advanced synthesis, streamed back to the user. The script’s architecture demonstrates sophisticated concurrency and state management, ensuring robust, real-time interactive capabilities.

##### Our recommendation model:

We used the Small VM - Intel® Xeon 4th Gen ® Scalable processor compute instance in the Intel Tiber Developer Cloud as a development environment with compute resources to build our model. We collect user ratings and food data to store for further personalization. We then organize it into three tensor objects to prepare for model creation: Users, Food, and Ratings. Next, we build our recommendation model using PyTorch’s neural network library, stacking multiple embedding and linear layers and optimizing with mean squared error loss. After cross-checking with our raw user data, we tuned our hyperparameters and compiled the model with the Adam optimizer to achieve results that closely match our user’s preferences. Then, we exported our model into ONNX format for compatibility with OpenVINO. Converting our model into OpenVINO optimized our model inference, allowing for instant user rating predictions on food dishes and easy integration with our existing framework. To provide the user with the best recommendations while ensuring we keep some variability, we randomize a large sample from a pool of food dishes, taking the highest-rated dishes from that sample according to our model.


# 🚩 - Challenges we ran into
We did not have enough compute resources on our Intel Developer Cloud instance. The only instance available did not have enough memory to support fine tuning a large LLM, crashing our Jupyter notebooks upon run.

# 🏆 - Accomplishments that we're proud of
Connecting phone screenshots to the backend on our computers → implemented a file system listener to manipulate a Dropbox file path connecting to our smart devices
Automatically scheduling a Google Calendar event → used two intermediary LLMs between input and output with one formatted to give Event Name, Location, Description, Start Time and Date, and End Time and Date and the other to turn it into a JSON output. The JSON could then be reliably extracted as parameters into our Google Calendar API
Configuring cloud compute services and instances in both our local machine and virtual machine instance terminals

# 📝 - What we learned
Nicholas: "Creating animated high-fidelity mockups in Figma and leading a full software team as PM.”
Marcus: "Using cloud compute engines such as Intel Developer Cloud, AWS, and Google Cloud to bring advanced AI technology to my projects"
Steven: "Integrating file listeners to connect phone images uploaded to Dropbox with computer vision from LLMs on my local computer."
Sean: "How to data clean from XML files with Pandas for cohesive implementation with LLMs."


# ✈️ - What's next for OptiFi

We envision OptiFi’s future plans in phases. Each of these phases were inspired by leaders in the tech-startup space.

### PHASE 1: PRIORITIZE SPEED OF EXECUTION
Phase 1 involves the following goals:

- Completing a fully interactive frontend that connects with each other instead of disconnected parts
- Any investment will be spent towards recruiting a team of more engineers to speed up the production of our application
- Based on “the agility and speed of startups allow them to capitalize on new opportunities more effectively” (Sam Altman, CEO of OpenAI)

### PHASE 2: UNDERSTANDING USERS

- Mass user test our MVP through surveys, interviews, and focus groups
- Tools: Qualtrics, Nielsen, UserTesting, Hotjar, Optimizely, and the best of all – personal email/call reach out
- Based on “Hey, I’m the CEO. What do you need? That’s the most powerful thing.” (Jerry Tan, President and CEO of YCombinator)

### PHASE 3: SEEKING BRANDING MENTORSHIP
Phase 3 involves the following goals:

- Follow pioneers in becoming big in an existing market by establishing incredible branding like Dollar Shave Club and Patagonia
- Align with advocating for preventative care and early intervention
- Based on “Find mentors who will really support your company and cheerlead you on” (Caroline Winnett, SkyDeck Executive Director)

## 📋 - Evaluator's Guide to OptiFi

##### Intended for judges, however the viewing public is welcome to take a look.

Hey! We wanted to make this guide to help provide you with further information on our implementations of our AI and other programs and provide a more in-depth look to cater to both the viewing audience and evaluators like yourself.

#### Sponsor Services and Technologies We Have Used This Hackathon

##### AWS Bedrock

Diet is an important part of health! So we wanted a quick and easy way to introduce this without the user having to constantly input information.
In our project, we used AWS Bedrock for our Nutrition Scanner. We accessed Anthropic’s Claude 3.5 Sonnet, which has vision capabilities, with Amazon Bedrock’s API.


##### Gradio

- **Project Demos and Hosting:** We hosted our demo on a Gradio playground, utilizing their easy-to-use widgets for fast prototyping.
- **Frontend:** Gradio rendered all the components we needed, such as text input, buttons, images, and more.
- **Backend:** Gradio played an important role in our project in letting us connect all of our different modules. In this backend implementation, we seamlessly integrated our features, including the nutrition scanner, diagnostic, and calendar.


##### Intel Developer Cloud

Our project needed the computing power of Intel cloud computers to quickly train our custom AI model, our food recommendation system.
This leap in compute speed powered by Intel® cloud computing and OpenVINO enabled us to re-train our models with lightning speed as we worked to debug and integrate them into our backend. It also made fine-tuning our model much easier as we could tweak the hyperparameters and see their effects on model performance within seconds.
As more users join our app and scan their food with the Nutrition Scanner, the need for speed becomes increasingly important, so by running our model on Intel Developer Cloud, we are building a prototype that is scalable for a production-level app.


##### Open AI

To create calendar events and generate responses for our Voicebot, we used Open AI’s generative AI technology. We used GPT-3.5-turbo to create our Voicebot responses to the user, quickly getting information to the user. However, a more advanced model, GPT-4o, was necessary to not only follow the strict response guidelines for parsing responses but also to properly analyze user health data and metrics and determine the best solutions in the form of calendar events. 


##### Assembly AI and ElevenLabs

We envision a future where it would be more convenient to find information by talking to an AI assistant versus a search function, enabling a hands-free experience.
With Assembly AI’s speech-to-text streaming technology, we could stream audio input from the user device’s microphone and send it to an LLM for prompting in real time! ElevenLabs on the other hand, we used for text-to-speech, speaking the output from the LLM prompt also in real time! Together, they craft an easy and seamless experience for the user.

##### GitHub

We used GitHub for our project by creating a GitHub repository to host our hackathon project's code. We leveraged GitHub not only for code hosting but also as a platform to collaborate, push code, and receive feedback.
