FROM python:3.11-slim

# Set working directory to the service folder
WORKDIR /code

# Copy dependency files first (for caching)
COPY ./SportsAppModels/pyproject.toml /code/SportsAppModels/pyproject.toml
COPY ./SportsAppService/pyproject.toml /code/SportsAppService/pyproject.toml

# Install dependencies (cached unless pyproject.toml changes)
RUN pip install --no-cache-dir /code/SportsAppModels
RUN pip install --no-cache-dir /code/SportsAppService

# Now copy the actual code
COPY ./SportsAppModels /code/SportsAppModels
COPY ./SportsAppService /code/SportsAppService

# Reinstall to include actual code (editable mode)
RUN pip install --no-cache-dir -e /code/SportsAppModels
RUN pip install --no-cache-dir -e /code/SportsAppService

EXPOSE 8000

# Correct module path for your project structure
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
