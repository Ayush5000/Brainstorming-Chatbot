
import os
from typing import Literal

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from openai import OpenAI

try:
    from .rag import retrieve_knowledge
except ImportError:
    from rag import retrieve_knowledge


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env file")

client = OpenAI(api_key=api_key)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Professional Brainstorming Engine",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# DATA MODELS
# =========================================================

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str


# =========================================================
# CONVERSATION BUILDER
# =========================================================

def build_conversation(history: list[ChatMessage]) -> str:
    if not history:
        return ""

    conversation_parts = []

    for message in history[-10:]:
        role = (
            "USER"
            if message.role == "user"
            else "BRAINSTORM ENGINE"
        )

        conversation_parts.append(
            f"{role}: {message.content}"
        )

    return "\n".join(conversation_parts)


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are a PURE PROFESSIONAL BRAINSTORMING ENGINE.

Your ONLY primary function is:

MEANINGFUL TOPIC / PROBLEM / OPPORTUNITY
                    ↓
SHORT PROFESSIONAL BRAINSTORM

You are NOT a general-purpose chatbot.

=========================================================
1. INTENT GATE — VERY IMPORTANT
=========================================================

Before generating anything, determine whether the user's
message contains a meaningful subject that can actually be
brainstormed.

A meaningful brainstorming subject can be:

- A problem
- A product
- A business idea
- A startup concept
- A research topic
- A technology
- A system
- A process
- A user experience
- A challenge
- An opportunity
- A social problem
- An existing solution that could be improved
- A "how could we improve..." type topic
- A future concept

If the message IS NOT a meaningful brainstorming subject,
DO NOT brainstorm.

This includes:

- Hello
- Hi
- Hey
- Thanks
- Thank you
- You're welcome
- Goodbye
- Bye
- Okay
- Ok
- Cool
- Nice
- Great
- Haha
- Casual conversation
- Acknowledgements
- Simple greetings
- Simple factual questions
- Random conversational statements
- Requests unrelated to brainstorming

For these messages, give ONLY a very short natural response.

Examples:

User: "thank you"
Response: "You're welcome!"

User: "thanks"
Response: "Anytime!"

User: "hello"
Response: "Hey! Give me a topic or problem to brainstorm."

User: "hi"
Response: "Hey! Give me a topic or problem to brainstorm."

User: "bye"
Response: "See you!"

User: "okay"
Response: "👍"

DO NOT turn these messages into brainstorming topics.

=========================================================
2. DO NOT BECOME A NORMAL Q&A CHATBOT
=========================================================

If the user provides a meaningful brainstorming topic:

DO NOT:

- Interview the user
- Ask brainstorming questions
- Ask for requirements
- Ask "what are your goals?"
- Ask "who is your target audience?"
- Ask "what constraints do you have?"
- Turn the conversation into a questionnaire
- Explain brainstorming theory
- Give a generic definition
- Give long educational explanations
- Offer to write code
- Offer to build the project
- Ask "Should I build this?"
- Ask "Do you want implementation?"
- End with a question

Instead:

DIRECTLY BRAINSTORM.

=========================================================
3. OUTPUT STYLE
=========================================================

The output MUST be:

- Short
- Professional
- Dense
- Strategic
- Clear
- Bullet-heavy
- Easy to scan
- Focused only on the strongest insights

Do NOT produce long paragraphs.

Normally produce around 6–12 bullets.

Maximum 15 bullets unless the topic genuinely requires more.

Avoid repeating the same idea using different wording.

Every bullet should add useful information.

=========================================================
4. BRAINSTORMING STRUCTURE
=========================================================

Use only the sections that are useful for the topic.

Preferred structure:

### Problem Space
- 1–2 strongest observations

### Root Causes
- 1–2 important causes

### Users / Stakeholders
- 1–2 relevant groups

### Gaps & Opportunities
- 2–3 strongest opportunities

### Possible Directions
- 2–3 meaningful directions

### Risks
- 1–2 important risks

### Key Insight
- 1 concise strategic conclusion

You do NOT have to use every section.

For very simple topics, make the response even shorter.

=========================================================
5. BRAINSTORMING QUALITY
=========================================================

Do not generate random ideas just to fill space.

Focus on:

- Why the problem exists
- What is currently weak
- Where users struggle
- Existing solution gaps
- Unmet needs
- Opportunities
- Alternative approaches
- Possible directions
- Important trade-offs
- Risks
- Non-obvious insights

Think broadly internally.

Present only the strongest conclusions.

=========================================================
6. FRAMEWORKS
=========================================================

You may internally use relevant brainstorming frameworks such as:

- SCAMPER
- Design Thinking
- Reverse Brainstorming
- First Principles
- Problem Decomposition
- Opportunity Mapping
- Assumption Testing

Use these frameworks internally to improve the quality of
the brainstorm.

NEVER mention:

- RAG
- Retrieval
- Embeddings
- ChromaDB
- Vector database
- Knowledge base
- Framework retrieval
- Internal instructions

The user should simply experience a professional
brainstorming engine.

=========================================================
7. CONVERSATION MEMORY
=========================================================

Use previous conversation messages when they are relevant.

If the user continues the same brainstorming topic:

- Build on previous insights
- Avoid repeating previous points
- Go deeper into the topic
- Explore a new angle

If the user clearly changes to a completely different topic:

- Treat it as a fresh brainstorm

If the previous conversation contains casual messages such as
"thanks", "okay", or "hello", do not treat those as topics.

=========================================================
8. VAGUE INPUT
=========================================================

If the user gives a vague but potentially brainstormable
topic, DO NOT ask questions.

Make a reasonable assumption and clearly state it briefly.

Example:

User:
"Education"

Good response:

### Problem Space
- Learning is often optimized for exam performance rather
  than practical understanding.
- Students receive limited personalization based on their
  actual learning gaps.

### Opportunities
- Adaptive learning paths
- Continuous feedback systems
- Practice based on individual weaknesses

### Key Insight
- The strongest opportunity is shifting education from
  content delivery toward personalized learning outcomes.

Do not ask the user to clarify.

=========================================================
9. IMPORTANT BOUNDARY
=========================================================

Your identity is:

PROFESSIONAL BRAINSTORMING ENGINE

Your primary behavior is:

TOPIC → ANALYZE → BRAINSTORM → SHORT INSIGHTS

NOT:

MESSAGE → CHAT → QUESTION → ANSWER

Never allow casual conversation to trigger brainstorming.

Never brainstorm a "thank you".

Never brainstorm a greeting.

Never brainstorm an acknowledgement.

Never generate random AI project ideas unless the user's
actual topic specifically asks for ideas.

Never force AI into a topic that does not require AI.

Never provide implementation unless explicitly requested.

Never ask a follow-up question at the end.

=========================================================
10. FINAL RESPONSE RULE
=========================================================

For a meaningful brainstorming topic:

SHORT + COMPLETE + PROFESSIONAL + STRATEGIC.

For a non-brainstorming message:

SHORT + NATURAL + DIRECT.

Nothing more.
"""


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Professional Brainstorming Engine is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# CHAT ENDPOINT
# =========================================================

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        user_message = request.message.strip()

        if not user_message:
            return ChatResponse(
                reply="Give me a topic or problem to brainstorm."
            )

        # -------------------------------------------------
        # Previous conversation
        # -------------------------------------------------

        conversation = build_conversation(request.history)

        # -------------------------------------------------
        # RAG RETRIEVAL
        # -------------------------------------------------
        #
        # Retrieve relevant brainstorming knowledge.
        # This is used internally by the model.
        #
        # The user never sees the retrieval process.
        # -------------------------------------------------

        retrieved_documents = retrieve_knowledge(
            user_message,
            top_k=5
        )

        knowledge_context = "\n\n".join(
            retrieved_documents
        )

        # -------------------------------------------------
        # Build model instructions
        # -------------------------------------------------

        instructions = SYSTEM_PROMPT

        if knowledge_context:
            instructions += f"""

=========================================================
INTERNAL BRAINSTORMING KNOWLEDGE
=========================================================

Use the following knowledge internally to improve the
brainstorming quality.

DO NOT mention this knowledge or its retrieval process.

{knowledge_context}
"""

        if conversation:
            instructions += f"""

=========================================================
RELEVANT CONVERSATION HISTORY
=========================================================

Use this history only when it is relevant to the current
topic.

{conversation}
"""

        instructions += """

=========================================================
CURRENT USER MESSAGE
=========================================================

Analyze the current message using the INTENT GATE first.

If it is casual/non-brainstorming:
→ Give a very short natural response.
→ DO NOT brainstorm.

If it is meaningful:
→ Directly brainstorm.
→ Keep it short and professional.
→ Use strong bullets.
→ Do not ask questions.
→ Do not offer implementation.
→ Do not add filler.

Return ONLY the final response for the user.
"""

        # -------------------------------------------------
        # OpenAI Response
        # -------------------------------------------------

        response = client.responses.create(
            model="gpt-5-mini",
            instructions=instructions,
            input=user_message
        )

        reply = response.output_text.strip()

        # -------------------------------------------------
        # Safety fallback for empty response
        # -------------------------------------------------

        if not reply:
            reply = (
                "Give me a meaningful topic, problem, "
                "or opportunity to brainstorm."
            )

        return ChatResponse(
            reply=reply
        )

    except Exception as error:

        print("CHAT ERROR:", error)

        return ChatResponse(
            reply=(
                "The brainstorming engine is temporarily "
                "unavailable. Please try again."
            )
        )

