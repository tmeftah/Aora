# Aora | Ahead Of Rest, Always.

## 📜 About

Aora is an application designed to leverage AI for advanced document handling and natural language processing. This repository contains both backend and frontend components to get the application up and running.

![Aora LogIn](./images/aora_login.PNG)

## 📟 Recommended Setup

Highly recommended:

- [VSCode](https://code.visualstudio.com/)
- [Python](https://www.python.org/downloads/)
- [Docker](https://www.docker.com/get-started)
- [Node](https://nodejs.org/en/download/package-manager)
- [Vue - Official](https://marketplace.visualstudio.com/items?itemName=Vue.volar) by Vue: Inter alia code formatter used for Vue.
  - 🛑 Attention: Disable Vetur!
  - Remark: The extension is also called **Volar**.
- [Prettier](https://marketplace.visualstudio.com/items?itemName=esbenp.prettier-vscode)

Further helpful VSCode extensions:

- [Vue.js Extension Pack](https://marketplace.visualstudio.com/items?itemName=mubaidr.vuejs-extension-pack) by Muhammad Ubaid Raza (Collection of extensions providing syntax highlighting, code format, code snippets, IntelliSense, linting support, npm & node tools)
- [Vue 3 Snippets](https://marketplace.visualstudio.com/items?itemName=hollowtree.vue-snippets) by hollowtree
- [Peacock](https://marketplace.visualstudio.com/items?itemName=johnpapa.vscode-peacock) by John Papa: VSCode Workspace color scheme for multiple instances.

📑 Note: The VSCode `settings.json` is pushed to git. In order to properly use the defined formatting settings, you definitely will need the above mentioned extension.

## ⚙ Project Setup

### Clone the Git repository

```sh
git clone https://github.com/tmeftah/Aora.git
```

### Setup Backend

- **Navigate to the backend directory:**

  ```bash
  cd backend/
  ```

- **Create a virtual environment:**

  ```bash
  python -m venv venv
  ```

- **Activate the virtual environment:**

  - On Windows:
    ```bash
    venv\Scripts\activate
    ```
  - On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

- **Install all required packages:**

  ```bash
  pip install -r requirements.txt
  ```

- **Run the development server:**

  ```bash
  fastapi dev
  ```

### Setup Frontend

- **Navigate to the frontend directory:**

  ```bash
  cd frontend
  ```

- **Install all necessary packages:**

  ```bash
  npm install
  ```

- **Run the development server:**

  ```bash
  npm run dev
  ```

### Setup Ollama LLM with Docker

You need ollama to run llms locally. Ollama have to be installed as docker container on your machine (docker have to run also).

Install and Run Ollama Docker Container

Ensure Docker is installed and running on your machine. Then, install and run the Ollama container with the following command:

```bash
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

This will set up and start the Ollama container in the background, with the necessary volumes and ports configured.

After installing and running the ollama docker container, you have to connect to that container and pull the llm model you want to use.

#### Download LLM Model

```bash
docker exec -it ollama ollama pull llama3.1
```

Replace llama3.1 with the appropriate model version, if necessary.

#### Manage the Ollama Container

To start the Ollama container if it is stopped, run the following command:

```bash
docker start ollama
```

you can follow the official ollama documenation for more settings.

#### Create Embeddings

To create a vector datastore of your documents, you need follow this steps:

1.  Inside the **'backend/embeddings'** folder create folder named 'docs' and add you pdf documents.
2.  run following command

```bash
cd backend/embeddings

python ingest.py # create embeddings.

```

## 📚 Configuration Settings

### Backend Environment Configuration

- Create an `.env` file inside the `backend` folder with the following settings:

  ```env
  SECRET_KEY=<your_secret_key>
  PUBLIC_KEY=<your_public_key>
  LANGFUSE_HOST=<your_langfuse_host>
  DATABASE_PATH=<chroma_db>
  COLLECTION_NAME=<langchain>

  ```

### Frontend Environment Configuration

- Create an `.env` file inside the `frontend` folder with the following settings for the UI:

  ```env
  API=http://ip-address-of-api:port
  ```

## 💫 Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute to the project.

### **Branch Strategy**

- **`main` Branch:** Represents the production-ready codebase. Only fully tested and approved code gets merged here.
- **`develop` Branch:** The main integration branch. All feature branches are merged here for testing before going to `main`.
- **Feature Branches (one per feature):** Short-lived branches where each developer works on a specific feature, bug fix, or task in isolation.

### **Workflow (Developer A and Developer B)**

1. **Project Setup (Do This Once)**

   ```bash
   git init  # Initialize the repository if you haven't already
   git remote add origin [remote-repo-url] # Connect to your remote repository (e.g., GitHub, GitLab)
   git checkout -b develop # Create the `develop` branch
   git push -u origin develop # Push `develop` to the remote
   ```

2. **Starting a New Feature**

   - **Developer A:**
     ```bash
     git checkout develop
     git pull origin develop # Ensure you have the latest changes
     git checkout -b feature-<issue-number>/user-authentication # New branch for user authentication
     ```
   - **Developer B:**
     ```bash
     git checkout develop
     git pull origin develop
     git checkout -b feature-<issue-number>/product-catalog # New branch for a product catalog
     ```

3. **Working on Features (Independently)**

   - Both developers work on their respective branches, making commits and pushing changes frequently:
     ```bash
     git add .
     git commit -m "Implemented login logic"
     git push origin feature-<issue-number>/user-authentication
     ```

4. **Merging a Feature into `develop` (Example: Developer A)**

   - **Before Merging (Important!):**

     ```bash
     git checkout develop
     git pull origin develop  # Get the latest changes from the remote `develop`
     ```

   - **Merging:**
     ```bash
     git checkout feature-<issue-number>/user-authentication # Switch to your feature branch
     git merge develop  # Merge the updated `develop` into your feature branch
     # Resolve any conflicts that might occur (more on that later)
     git push origin feature-<issue-number>/user-authentication # Push the merged version
     ```
   - **Creating a Pull Request:** Open a pull request on your platform (GitHub) from `<issue-number>/user-authentication` to `develop`. This allows for code review before merging.

5. **Code Review and Merging to `develop`**

   - Developer B (or the other developer) reviews the pull request, provides feedback, and approves it.
   - Once approved, Developer A can merge the pull request into `develop` on the remote platform (GitHub).

6. **Repeating the Process (Developer B's Turn)**

   - Developer B now pulls the latest `develop`, merges it into their `feature-<issue-number>/product-catalog` branch (to resolve conflicts early), pushes, and creates a pull request for review.

7. **Deploying to `main`**

   - Once enough features are tested on `develop`, you can merge `develop` into `main`.
     ```bash
     git checkout main
     git pull origin main
     git merge develop
     git push origin main
     ```

### **Keys to Minimizing Conflicts**

- **Frequent Pulls and Merges:** Regularly pulling from `develop` and merging into your feature branches helps identify and resolve conflicts earlier.
- **Effective Communication:** Talk to your teammate! Discuss what you're working on to avoid overlapping changes in the same files.
- **Small, Focused Features:** Breaking work into smaller pieces makes conflicts less likely and easier to manage.

### **Resolving Conflicts (When They Happen)**

- If `git merge` encounters a conflict, it will mark the conflicting areas in your code.
- Open the affected files, manually edit them to choose the correct changes, and then use `git add [filename]` to stage the resolved files.
- Commit the resolution: `git commit -m "Resolved merge conflict in [filename]"`

This workflow emphasizes collaboration and regular integration to minimize the chances of major merge conflicts. Remember that clear communication and consistent practices are your best tools to keep your Git workflow running smoothly.

## License

This project is licensed under the MIT License.

## Contact

This project is a part of the GenAI project. In case there are any questions, please contact
