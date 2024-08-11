# Aora | Access, Organize, Retrieve, Archive.

Aora is an application designed to leverage AI for advanced document handling and natural language processing. This repository contains both backend and frontend components to get the application up and running.

## Installation

### Backend

1. **Navigate to the backend directory:**

   ```bash
   cd backend/
   ```
3. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install all required packages:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run the development server:**

   ```bash
   fastapi dev
   ```

### Frontend

1. **Navigate to the frontend directory:**

   ```bash
   cd frontend
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

   Create an `.env` file inside the `backend` folder with the following settings:

   ```env
   SECRET_KEY=<your_secret_key>
   PUBLIC_KEY=<your_public_key>
   LANGFUSE_HOST=<your_langfuse_host>
   DATABASE_PATH=<chroma_db>
   COLLECTION_NAME=<langchain>
   
   ```

2. **Frontend Environment Settings:**

   Create an `.env` file inside the `frontend` folder with the following settings for the UI:

   ```env
   API=http://ip-address-of-api:port
   ```


## Contributing

Contributions are welcome! Please open an issue or submit a pull request to contribute to the project.

**Branch Strategy**

* **`main` Branch:**  Represents the production-ready codebase. Only fully tested and approved code gets merged here.
* **`develop` Branch:** The main integration branch. All feature branches are merged here for testing before going to `main`.
* **Feature Branches (one per feature):**  Short-lived branches where each developer works on a specific feature, bug fix, or task in isolation.

**Workflow (Developer A and Developer B)**

1. **Project Setup (Do This Once)**

   ```bash
   git init  # Initialize the repository if you haven't already
   git remote add origin [remote-repo-url] # Connect to your remote repository (e.g., GitHub, GitLab) 
   git checkout -b develop # Create the `develop` branch
   git push -u origin develop # Push `develop` to the remote
   ```

2. **Starting a New Feature**

   * **Developer A:**
     ```bash
     git checkout develop
     git pull origin develop # Ensure you have the latest changes 
     git checkout -b feature/user-authentication # New branch for user authentication
     ```
   * **Developer B:**
     ```bash
     git checkout develop 
     git pull origin develop
     git checkout -b #<issue-number>/product-catalog # New branch for a product catalog 
     ```

3. **Working on Features (Independently)**

   * Both developers work on their respective branches, making commits and pushing changes frequently:
     ```bash
     git add .
     git commit -m "Implemented login logic"
     git push origin #<issue-number>/user-authentication 
     ```

4. **Merging a Feature into `develop` (Example: Developer A)**

   * **Before Merging (Important!):**
     ```bash
     git checkout develop
     git pull origin develop  # Get the latest changes from the remote `develop`
     ```

   * **Merging:**
     ```bash
     git checkout #<issue-number>/user-authentication # Switch to your feature branch
     git merge develop  # Merge the updated `develop` into your feature branch  
     # Resolve any conflicts that might occur (more on that later)
     git push origin #<issue-number>/user-authentication # Push the merged version
     ```
   * **Creating a Pull Request:** Open a pull request on your platform (GitHub) from `#<issue-number>/user-authentication` to `develop`. This allows for code review before merging.

5. **Code Review and Merging to `develop`**

   * Developer B (or the other developer) reviews the pull request, provides feedback, and approves it.
   * Once approved, Developer A can merge the pull request into `develop` on the remote platform (GitHub). 

6. **Repeating the Process (Developer B's Turn)**

   * Developer B now pulls the latest `develop`, merges it into their `#<issue-number>/product-catalog` branch (to resolve conflicts early), pushes, and creates a pull request for review. 

7. **Deploying to `main`**

   * Once enough features are tested on `develop`, you can merge `develop` into `main`.
     ```bash
     git checkout main
     git pull origin main
     git merge develop
     git push origin main
     ```

**Keys to Minimizing Conflicts**

* **Frequent Pulls and Merges:** Regularly pulling from `develop` and merging into your feature branches helps identify and resolve conflicts earlier.
* **Effective Communication:** Talk to your teammate! Discuss what you're working on to avoid overlapping changes in the same files.
* **Small, Focused Features:** Breaking work into smaller pieces makes conflicts less likely and easier to manage.

**Resolving Conflicts (When They Happen)**

* If `git merge` encounters a conflict, it will mark the conflicting areas in your code.
* Open the affected files, manually edit them to choose the correct changes, and then use `git add [filename]` to stage the resolved files.
* Commit the resolution: `git commit -m "Resolved merge conflict in [filename]"`

This workflow emphasizes collaboration and regular integration to minimize the chances of major merge conflicts. Remember that clear communication and consistent practices are your best tools to keep your Git workflow running smoothly. 


## License

This project is licensed under the MIT License.

## Contact

For any questions or inquiries, please contact.
