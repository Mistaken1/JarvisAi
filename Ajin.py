from google import genai
from google.genai import types
from google.genai import errors
from voice import speak
from declarations import FUNCTIONS, tools
from API_KEYS import KEYS

# ── Client setup with key rotation ──
current_key_index = 0

def create_client():
    return genai.Client(api_key=KEYS[current_key_index])

def rotate_key():
    """Rotates to the next API key and rebuilds the client + chat."""
    global current_key_index, client, chat
    current_key_index = (current_key_index + 1) % len(KEYS)
    client = create_client()
    chat = create_chat()
    print(f"[Rotated to key index {current_key_index}]")

SYSTEM_PROMPT = """
You are Jarvis, a sharp and reliable AI assistant running on the user's Windows PC and some smart wit Refer to me the user as sir or Ujing.
Your personality: calm, capable, slightly dry wit — like a competent personal aide.
Speak in first person. Keep replies short and natural (under 60 words) unless asked for more.
Never repeat the same phrasing twice in a row. Vary your acknowledgments.
When a function runs and returns a result, acknowledge it naturally — don't read back the raw result string.
If a function returns an error string (starts with 'error:'), explain what went wrong plainly.
You CAN and SHOULD solve math, answer questions, help with homework, and anything else the user asks — not just computer control tasks.
When the user asks what's on screen, use analyze_screen immediately without asking for clarification.
""".strip()

def create_chat():
    return client.chats.create(
        model="gemini-2.5-flash-lite",
        config=types.GenerateContentConfig(
            temperature=0.85,
            max_output_tokens=750,
            system_instruction=SYSTEM_PROMPT,
            tools=[tools]
        )
    )

client = create_client()
chat = create_chat()

print("[starting...]")

def send_with_retry(message, max_retries=len(KEYS)):
    """Sends a message to the chat, rotating keys on 429 errors."""
    global chat
    for attempt in range(max_retries):
        try:
            return chat.send_message(message)
        except Exception as e:
            if "429" in str(e):
                print(f"[Rate limit hit, rotating key... attempt {attempt + 1}]")
                rotate_key()
            else:
                raise
    raise RuntimeError("All API keys exhausted or rate limited.")

def handle_function_call(function_name: str, arguments: dict) -> str | None:
    if function_name == "analyze_screen":
        img_base64 = FUNCTIONS[function_name](**arguments)
        # Fix: send as a list of Parts, not types.Content
        followup = send_with_retry([
            types.Part(inline_data=types.Blob(
                mime_type="image/png",
                data=img_base64
            )),
            types.Part(text=arguments.get("question", "What's on screen?"))
        ])
        for part in followup.candidates[0].content.parts:
            if hasattr(part, 'text') and part.text:
                speak(part.text)
                return None
        return None

    result = FUNCTIONS[function_name](**arguments)
    return str(result) if result else None

def process_response(response) -> bool:
    had_function_call = False

    for part in response.candidates[0].content.parts:
        if part.function_call:
            had_function_call = True
            function_name = part.function_call.name
            arguments = dict(part.function_call.args)

            print(f"[Calling: {function_name}({arguments})]")

            try:
                result = handle_function_call(function_name, arguments)
                if result is not None:
                    # Fix: send as types.Part directly, not types.Content
                    followup = send_with_retry(
                        types.Part(
                            function_response=types.FunctionResponse(
                                name=function_name,
                                response={"result": result}
                            )
                        )
                    )
                    for fpart in followup.candidates[0].content.parts:
                        if hasattr(fpart, 'text') and fpart.text:
                            speak(fpart.text)
                            break

            except Exception as e:
                speak(f"Something went wrong with {function_name}: {str(e)}")

        elif hasattr(part, 'text') and part.text:
            speak(part.text)

    return had_function_call
password = "ujingski123124"
# ── Main loop ──
while True:
    try:
        user_input = input(">> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            speak("Signing off.")
            break

        response = send_with_retry(user_input)
        process_response(response)

    except KeyboardInterrupt:
        speak("Shutting down.")
        break
    except Exception as e:
        speak(f"Something went wrong: {str(e)}")
        print(f"[Error]: {e}")

