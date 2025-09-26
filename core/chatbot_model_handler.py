from gradio_client import Client

class ModelHandler:
    def __init__(self, space_name):
        # space_name should be like "exzort/VinebotNew"
        self.client = Client(space_name)

    def generate_response(self, user_input):
        print(f"[DEBUG] Sending to HF Space via gradio_client: {user_input}")
        try:
            result = self.client.predict(
                message=user_input,
                api_name="/predict"
            )
            print(f"[DEBUG] Response: {result}")
            return result
        except Exception as e:
            print("[DEBUG] Exception occurred:", str(e))
            return "Error connecting to VineBot Space."

    # ✅ New method for streaming
    def stream_response(self, user_input):
        print(f"[DEBUG] Streaming (simulated) from HF Space: {user_input}")
        try:
            result = self.client.predict(
                message=user_input,
                api_name="/predict"
            )
            yield result  # Send the whole reply at once
        except Exception as e:
            print(f"[DEBUG] Exception in stream_response: {str(e)}")
            yield f"Error: {str(e)}"
