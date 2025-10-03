from gradio_client import Client

class ModelHandler:
    def __init__(self, space_name):
        self.client = Client(space_name)

    def generate_response(self, user_input):
        """Blocking call — waits for full reply."""
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
        """True streaming — yields tokens as they arrive from HF Space."""
        print(f"[DEBUG] Streaming from HF Space: {user_input}")
        try:
            # Submit returns a Job, no stream=True argument
            job = self.client.submit(
                user_input,
                api_name="/predict"
            )

            # Iterate over job to get chunks
            for event in job:
                if event is None:
                    continue
                yield str(event)
                print(f"[DEBUG] Raw event from HF: {event!r}")

        except Exception as e:
            print(f"[DEBUG] Exception in stream_response: {str(e)}")
            yield f"Error: {str(e)}"


