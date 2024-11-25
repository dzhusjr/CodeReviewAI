## Part 1 – Prototype (Code)

### **Overview**
The Coding Assignment Auto-Review Tool is designed to streamline the code review process by leveraging the GitHub API for fetching repository contents and the OpenAI API for generating detailed code reviews. The application is implemented using FastAPI and follows best practices for modularity, maintainability, and scalability.

---

### **Features**
1. **FastAPI Backend**:
   - Implements a `/review` POST endpoint to handle review requests.
   - Processes user input with Pydantic models to validate request data.

2. **GitHub API Integration**:
   - Retrieves file structure and content for the specified repository.
   - Supports nested directories and paginated file retrieval.

3. **OpenAI API Integration**:
   - Generates structured code reviews with detailed analysis.
   - Adapts reviews based on the candidate's experience level (Junior, Mid, Senior).

4. **Input Validation**:
   - Uses Pydantic for strict validation of request payloads, including checks for URL format and candidate level.

5. **Modularity**:
   - The project is divided into dedicated modules for models, services, and utility functions.

---

### **Endpoints**
#### POST `/review`
- **Description**: Accepts request data, fetches repository contents, and generates a code review.
- **Request Body**:
  ```json
  {
      "assignment_description": "Description of the coding assignment.",
      "github_repo_url": "https://github.com/example/repository",
      "candidate_level": "Junior"
  }
  ```
- **Response**:
  ```json
  {
      "response": "Generated code review."
  }
  ```

### **How to Run**
1. **Clone the Repository**:
   ```bash
   git clone [<repository-url>](https://github.com/dzhusjr/CodeReviewAI.git)
   cd CodeReviewAI
   ```
2. **Setup Environment Variables**:
   - Create a `.env` file and define environment variables for GitHub token and OpenAI API key.

   ```bash
   OPENAI_API_KEY=<your-openai-api-key>
   GITHUB_TOKEN=<your-github-token>
   ```

3. **Install Dependencies**:
   ```bash
   pip install poetry
   poetry install
   ```

4. **Run the Application**:
   ```bash
   docker compose up --build -d
   ```
---
## Part 2 – Scaling the System

### **Proposed Solution**

1. **System Design**
   - **Load Balancing**: Deploy the system behind a load balancer (e.g., AWS ALB or Nginx) to distribute traffic across multiple application instances.
   - **Autoscaling**: Use container orchestration platforms like Kubernetes to scale application instances dynamically based on traffic.

2. **Efficient Repository Handling**
   - **File Retrieval**:
     - Use **Redis** or a similar in-memory cache to store repository metadata and file contents temporarily, reducing redundant API calls.
     - Paginate file requests for repositories with many files to avoid overloading the system.
   - **Asynchronous Processing**: Process large repositories in parallel using libraries like `asyncio` or a task queue system such as **Celery** with Redis or RabbitMQ.
   
3. **High Throughput and Rate Limit Management**
   - **Batch Requests**: Aggregate multiple API requests (e.g., file retrieval) into fewer batch requests to reduce the number of calls to the GitHub API.
     - Implement an extra query listing all files in the repository and asking for a file-by-file estimate of how important each file is to be downloaded and evaluated. (e.g., migrations, tests, etc.)
   - **API Rate Limit Handling**:
     - Cache responses for repositories already fetched within a certain time window.
     - Use GitHub’s GraphQL API to retrieve repository metadata efficiently in a single request.
   - **OpenAI API Usage**:
     - Queue and throttle AI review requests to control OpenAI API costs and avoid exceeding rate limits.
     - Optimize prompts to reduce token usage and improve processing efficiency.

4. **Database for Persistent Storage**
   - Use a database (e.g., **PostgreSQL**) to store processed review results, file metadata, and repository analysis, allowing for reuse and reducing repeated computations.

5. **Cost Control**
   - Implement **request quotas** to limit free-tier usage and encourage customers to upgrade for higher capacity.
   - Optimize the AI review process by caching intermediate results and reusing previously generated analyses for identical repository states.

---

### **Diagram Overview**
The architecture includes:
- **Frontend**: Sends review requests to the backend.
- **Backend**:
  - Handles review requests via FastAPI.
  - Interacts with Redis for caching.
  - Uses Celery for background tasks (e.g., file retrieval and AI review generation).
- **APIs**:
  - Connects to GitHub API with rate-limit-aware logic.
  - Interacts with OpenAI API for review generation.
- **Database**: Stores repository metadata and review results.
- **Infrastructure**:
  - Kubernetes for autoscaling.
  - Load balancer for traffic distribution.
