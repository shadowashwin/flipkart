FROM python:3.12.4-slim
RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0 && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
# RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./app.py