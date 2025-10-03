from gradio_client import Client

class ModelHandler:
    def __init__(self, space_name):
        self.client = Client(space_name)

    def generate_response(self, user_input):
        print(f"[DEBUG] Sending to HF Space: {user_input}")
        try:
            result = self.client.predict(
                message=user_input,
                api_name="/predict"
            )
            return result
        except Exception as e:
            print("[DEBUG] Exception:", str(e))
            return "Error connecting to VineBot Space."

    def stream_response(self, user_input):
        print(f"[DEBUG] Streaming (simulated) from HF Space: {user_input}")
        try:
            # normal blocking call
            result = self.client.predict(
                message=user_input,
                api_name="/predict"
            )
            # simulate streaming by sending piece by piece
            for word in result.split():
                yield word + " "
        except Exception as e:
            print(f"[DEBUG] Exception in stream_response: {str(e)}")
            yield f"Error: {str(e)}"

