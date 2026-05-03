🧠 AI-PD: Early Parkinson’s Detection using Spiral Analysis

AI-PD is a deep learning-based web application that enables early screening of Parkinson’s Disease using spiral drawing analysis. The system leverages computer vision and neural networks to detect subtle motor irregularities that may indicate Parkinsonian symptoms.

🔗 Live Demo: https://pd-detector.streamlit.app/

🚀 Features
🖼️ Upload spiral drawings (JPG/PNG)
🧠 AI-based prediction using ResNet-18
📊 Confidence score for predictions
📋 Structured explanation of results
🎨 Clean, responsive UI (desktop + mobile)
⚡ Real-time inference via Streamlit

🧠 How It Works
- User uploads a spiral drawing
- Image is preprocessed:
- Resized to 224×224
- Converted to 3-channel grayscale
- Normalized using ImageNet stats
- Passed through a ResNet-18 model
Model outputs:
- Prediction (PD / Healthy)
- Confidence score
UI displays:
- Result classification
- Explanation of detected patterns

🏗️ Tech Stack
Frontend: Streamlit
Backend / ML: PyTorch
Model Architecture: ResNet-18
Image Processing: PIL, torchvision
Deployment: Streamlit Cloud

⚙️ Installation (Run Locally)
1. Clone the repository

git clone https://github.com/mohhiiii/AI-PD.git
cd AI-PD

2. Create virtual environment

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

3. Install dependencies

pip install -r requirements.txt

4. Run the app

streamlit run app.py

⚠️ Disclaimer

This application is intended for screening and research purposes only.
It is not a medical diagnostic tool.

Users are strongly advised to consult a qualified healthcare professional for clinical evaluation.
