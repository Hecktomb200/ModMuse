Running the Backend (FastAPI)
1. Navigate to the backend folder
cd modmuse-backend

2. Create & activate a virtual environment

Windows (PowerShell):

python -m venv .venv
.venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the development server
uvicorn app.main:app --reload

5. Open the API documentation

Visit:

http://localhost:8000/docs