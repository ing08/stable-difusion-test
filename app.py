import io
import os
import warnings
from PIL import Image
from dotenv import load_dotenv
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from flask import Flask, request, send_file

load_dotenv()
# STABILITY_KEY = "sk-CNeRXRX7rSPcCfRaD644PY3BLYztMx3cAa7aMU3nKHR7VRCA"
stability_api = client.StabilityInference(
    key="sk-nW3lraO8IMswS2wrcZyXf0MdRRfK27GwgZDln6RqsohYSpQA",
    verbose=True,
)

app = Flask(__name__)

@app.route("/")
def generate():
    req = request.args
    propmt = req.get("prompt", "")
    answers = stability_api.generate(
        prompt=propmt
    )
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                return send_file(
                    io.BytesIO(artifact.binary),
                    mimetype='image/png'
                )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ['PORT'])