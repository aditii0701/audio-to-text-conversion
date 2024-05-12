from flask import Flask, render_template, request, jsonify
import assemblyai as aai

app = Flask(__name__)

aai.settings.api_key = "22f832229ec14cde9eb71fe251062a63"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'audio_file' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400

        audio_file = request.files['audio_file']
        if audio_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_file)

        if transcript.status == aai.TranscriptStatus.error:
            return jsonify({'error': transcript.error}), 500
        else:
            return jsonify({'transcript': transcript.text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
