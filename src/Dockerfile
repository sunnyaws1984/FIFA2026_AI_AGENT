
FROM python:3.11-slim
# Set working directory inside container
WORKDIR /app

RUN pip install uv

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN uv pip install --system --no-cache -r requirements.txt

# Copy all source files
COPY agent.py .
COPY tools.py .
COPY ui.py .

# Expose Gradio port
EXPOSE 7860

# Start the app
CMD ["python", "ui.py"]