AI Personal Assistant with LangChain Tool Calling
A beginner-friendly educational project that shows how an LLM can call tools to perform actions, instead of only generating text.
This project is designed for YouTube lectures on LangChain and GenAI. The code stays simple on purpose so you can explain it line by line.

Project Overview
The assistant understands natural-language requests and can:
Book meetings (saved to a local CSV)
Manage todos (add / update / list tasks)
Book simulated flights
Place simulated shopping orders
Nothing connects to real external APIs. Every tool is a normal Python function with deterministic business logic and local file storage.

Architecture
User Message
      ↓
Conversation Memory
      ↓
LLM
      ↓
Tool Selection
      ↓
Tool Arguments
      ↓
Python Tool
      ↓
Deterministic Business Logic
      ↓
Tool Result
      ↓
LLM
      ↓
Final Response

Important distinction
Step
Who decides / runs it?
Which tool to call
LLM
What arguments to pass
LLM
Actual booking / CSV update
Python tool function
Final natural-language reply
LLM


The LLM decides. The tool executes.

Why Tools?
Without tools
The LLM only generates an answer.
It might say "Meeting booked", but nothing really happened.
With tools
The LLM calls a tool to perform an action.
A real Python function runs, updates a CSV file, and returns a confirmation.
Then the LLM explains that result to the user.
That is the core lesson of this project.

Available Tools
Tool
Purpose
Required info
book_meeting
Book a meeting
participants, date, time
add_task
Add a todo item
task_name
update_task_status
Change task status
task_name, status
list_tasks
Show tasks
optional status filter
book_flight
Simulate a flight booking
destination, date, time
place_order
Simulate a shopping order
list of items with name + quantity


If required information is missing, the assistant asks a clarifying question.
It should not invent missing values.

Project Structure
ai-personal-assistant/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── app.py                      # Terminal chat interface
├── data/
│   ├── todo.csv                # Local todo list
│   ├── meetings.csv            # Meeting bookings
│   ├── flight_bookings.csv     # Flight bookings
│   └── orders.csv              # Shopping orders
├── prompts/
│   └── assistant_prompt.txt    # System prompt (not hard-coded)
└── src/
    ├── llm.py                  # Create OpenAI or Gemini LLM from .env
    ├── tools.py                # Python tools + CSV business logic
    ├── memory.py               # Simple conversation memory
    └── assistant.py            # Tool-calling loop (main LangChain file)

Responsibility of each file
src/llm.py — load .env and create OpenAI or Gemini chat model
src/tools.py — define tools as normal Python functions
src/memory.py — keep chat history in a simple list
src/assistant.py — bind tools, run tool calls, return the final reply
app.py — read user input and print responses

Setup
1. Python environment
Use Python 3.10+ (3.11 or 3.12 recommended).
cd ai-personal-assistant
python -m venv .venv

Activate it:
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

2. Get an API key
You only need one provider key for the provider you choose:
OpenAI: create a key at https://platform.openai.com/api-keys
Gemini: create a key at https://aistudio.google.com/apikey
3. Environment variables
copy .env.example .env

On macOS/Linux:
cp .env.example .env

Edit .env and set your provider + key:
# Choose: openai  OR  gemini
LLM_PROVIDER=openai

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash

Examples:
Use OpenAI: set LLM_PROVIDER=openai and fill OPENAI_API_KEY
Use Gemini: set LLM_PROVIDER=gemini and fill GEMINI_API_KEY
src/llm.py reads LLM_PROVIDER and creates the matching client.
4. Install dependencies
pip install -r requirements.txt


Running
python app.py

Example session:
========================================
AI PERSONAL ASSISTANT
========================================
Type 'exit' or 'quit' to leave.

You: Book a meeting with Rahul tomorrow at 3 PM.

[Tool Call]
Tool: book_meeting
Arguments:
{
    "participants": ["Rahul"],
    "date": "2026-08-26",
    "time": "15:00"
}

[Tool Result]
Meeting booked successfully.
...

Assistant: Meeting booked successfully. Meeting ID: MTG-1024 ...

You: exit
Goodbye!


Example Conversations
1. Complete meeting request
You: Book a meeting with Rahul tomorrow at 3 PM.
Assistant: Confirms the booking (after a tool call).
2. Missing meeting information
You: Book a meeting tomorrow at 3 PM.
Assistant: Who would you like to meet with?
3. Todo creation
You: Add 'Prepare tool calling lecture' to my task list.
Assistant: Confirms the new task was added.
4. Todo completion
You: I finished preparing the tool calling lecture.
Assistant: Updates the task status to completed.
5. Listing pending tasks
You: Show me all my pending tasks.
Assistant: Lists tasks with status pending.
6. Flight booking
You: Book me a flight to Delhi on September 15 at 10 AM.
Assistant: Returns a simulated flight confirmation.
7. Missing flight information
You: Book me a flight to Delhi.
Assistant: Asks for date and time.
8. Shopping order
You: Buy two notebooks, one pack of blue pens and a laptop sleeve.
Assistant: Places a simulated order with structured item quantities.
9. Multi-tool request
You: Show me my pending tasks and then book a meeting with Rahul tomorrow at 3 PM.
Assistant: May call list_tasks and then book_meeting, then summarize both results.
10. Follow-up conversation using memory
You: Add 'Finish the RAG project' to my task list.
Assistant: Task added.
You: Mark that as completed.
Assistant: Understands "that" from conversation memory and updates the task.

Educational Flow
Use this project to teach:
1. Define a normal Python function
2. Convert it into a LangChain Tool (@tool)
3. Give tools to the LLM (bind_tools)
4. User asks for an action
5. LLM decides which tool to call
6. LLM generates structured tool arguments
7. Python function executes
8. Tool returns result
9. Result goes back to the LLM
10. LLM generates final response

Look at:
src/tools.py → normal Python functions that perform actions
src/assistant.py → where LangChain connects the LLM with those tools
Tool call logs printed in the terminal help learners see the internal steps.

Future Improvements
Not included in Version 1 (on purpose):
Real Calendar APIs
Real flight / airline APIs
Real shopping APIs
Authentication
Databases
MCP
LangGraph
Human approval steps
Web UI (Streamlit / FastAPI)
Version 1 focuses only on:
LangChain Tool Calling + Memory + Deterministic Python Tools

License
Educational / demo project. Use freely for learning and teaching.
