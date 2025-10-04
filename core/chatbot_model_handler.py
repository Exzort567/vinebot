from gradio_client import Client

class ModelHandler:
    def __init__(self, space_name):
        self.space_name = space_name
        self.client = None   # don’t connect yet

    def _ensure_client(self):
        """Initialize the Hugging Face client only once, when needed."""
        if self.client is None:
            print(f"[DEBUG] Connecting to Hugging Face Space: {self.space_name}")
            self.client = Client(self.space_name)

    def generate_response(self, user_input):
        """Blocking call — waits for full reply."""
        self._ensure_client()
        print(f"[DEBUG] Sending to HF Space: {user_input}")
        try:
            result = self.client.predict(
                user_input,       # ✅ positional, no keyword
                api_name="/predict"
            )
            return result
        except Exception as e:
            print("[DEBUG] Exception:", str(e))
            return "Error connecting to VineBot Space."

    def stream_response(self, user_input):
        self._ensure_client()
        print(f"[DEBUG] Streaming from HF Space: {user_input}")
        try:
            job = self.client.submit(user_input, api_name="/predict")
            for event in job:
                if event is None:
                    continue
                print(f"[DEBUG] Raw event from HF: {event!r}")
                yield str(event)   # ✅ yield chunk immediately
        except Exception as e:
            print(f"[DEBUG] Exception in stream_response: {str(e)}")
            yield f"Error: {str(e)}"

