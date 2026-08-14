from openai import OpenAI, APITimeoutError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)


def ask_ai(question, context):
    """
    Sends the user's question and the retrieved PDF context
    to the AI model and returns the answer.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "system",
                    "content": """
You are an AI Study Assistant.

Rules:

- Answer ONLY using the provided context.
- If the answer is not found in the context, reply:
  "I couldn't find that information in the uploaded PDF."
- Use headings and bullet points whenever appropriate.
- Keep explanations clear and suitable for students.
"""
                },
                {
                    "role": "user",
                    "content": f"""
Context:
{context}

Question:
{question}
"""
                }
            ],
            temperature=0.3,
            timeout=90
        )

        # Make sure the API returned an answer
        if not response.choices:
            return "⚠️ The AI did not return a response."

        answer = response.choices[0].message.content

        if not answer:
            return "⚠️ The AI returned an empty response."

        return answer

    except APITimeoutError:
        return "⏳ The AI took too long to respond. Please try again."

    except Exception as e:
        print("OpenRouter Error:", e)
        return f"❌ Error: {str(e)}"