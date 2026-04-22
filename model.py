import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import streamlit as st

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# Image preprocessing pipeline
# -----------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Grayscale(num_output_channels=3),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# -----------------------------
# Load trained ResNet18
# -----------------------------
@st.cache_resource
def load_model():

    model = models.resnet18(pretrained=False)

    # binary classification
    model.fc = nn.Linear(model.fc.in_features, 2)

    model.load_state_dict(
        torch.load("resnet18_improved/resnet18_improved_spiral.pth", map_location=device)
    )

    model.to(device)
    model.eval()

    return model


model = load_model()

# -----------------------------
# Prediction function
# -----------------------------
def predict_spiral(image):

    try:

        # Convert PIL → tensor
        img = transform(image).unsqueeze(0).to(device)

        with torch.no_grad():

            outputs = model(img)

            probs = torch.softmax(outputs, dim=1)

            confidence, predicted = torch.max(probs, 1)

        confidence = confidence.item()
        predicted = predicted.item()

        if confidence>0.7 and predicted==1:

            prediction = True
            explanation = "Irregular spiral stroke patterns detected."

        else:

            prediction = False
            explanation = "Spiral pattern appears regular."

        return prediction, confidence, explanation

    except Exception as e:

        return None, 0.0, str(e)