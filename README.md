# RAGGI AI-Oracle

RAGGI AI-Oracle is an application designed to leverage AI for advanced document handling and natural language processing. This repository contains both backend and frontend components to get the application up and running.

## Installation

### Backend

1. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install all required packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the development server:**

   ```bash
   fastapi dev
   ```

### Frontend

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend/raggi
   ```

2. **Install all necessary packages:**

   ```bash
   npm install
   ```

3. **Run the development server:**

   ```bash
   npm run dev
   ```

## Settings

### Environments

1. **Backend Environment Settings:**

   Create an `.env` file inside the `rag` folder with the following settings for Langfuse:

   ```env
   SECRET_KEY=your_secret_key
   PUBLIC_KEY=your_public_key
   LANGFUSE_HOST=your_langfuse_host
   ```

2. **Frontend Environment Settings:**

   Create an `.env` file inside the `frontend/raggi` folder with the following settings for the UI:

   ```env
   API=http://ip-address-of-api:port
   ```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute to the project.

## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact.
