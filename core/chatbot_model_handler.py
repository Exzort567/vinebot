from gradio_client import Client
import psutil
import time

class ModelHandler:
    def __init__(self, space_name):
        self.space_name = space_name
        self.client = None 

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
                user_input,     
                api_name="/predict"
            )
            return result
        except Exception as e:
            print("[DEBUG] Exception:", str(e))
            return "Error connecting to VineBot Space."

    def stream_response(self, user_input):
        self._ensure_client()
        print(f"[DEBUG] Streaming from HF Space: {user_input}")
        print(f"[MEMORY] Before stream: {psutil.Process().memory_info().rss / (1024 ** 2):.2f} MB")

        start_time = time.time()  
        first_chunk_time = None

        try:
            job = self.client.submit(user_input, api_name="/predict")

            for event in job:
                if event is None:
                    continue

                # Record lap time only on first chunk
                if first_chunk_time is None:
                    first_chunk_time = time.time()
                    lap_duration = first_chunk_time - start_time
                    print(f"[TIME] First chunk received after {lap_duration:.2f} seconds")

                print(f"[DEBUG] Raw event from HF: {event!r}")
                print(f"[MEMORY] During stream: {psutil.Process().memory_info().rss / (1024 ** 2):.2f} MB")

                yield str(event) 

            # After the final chunk
            total_duration = time.time() - start_time
            print(f"[TIME] Total response time: {total_duration:.2f} seconds")

        except Exception as e:
            print(f"[DEBUG] Exception in stream_response: {str(e)}")
            yield f"Error: {str(e)}"

        print(f"[MEMORY] After stream: {psutil.Process().memory_info().rss / (1024 ** 2):.2f} MB")

