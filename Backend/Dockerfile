# Step 1: Use an official Python image as a base
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements.txt file into the container
COPY requirements.txt .

# Step 4: Install the dependencies from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code into the container
COPY . .

# Step 6: Run langchain_helper.py to generate the faiss_index folder
RUN python langchain_helper.py

# Step 7: Expose port 5000
EXPOSE 5000

# Step 8: Run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "api:app"]
