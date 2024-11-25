from openai import OpenAI

client = OpenAI()

async def generate_review(assignment_description: str, repo_contents: str, candidate_level: str):

    prompt = f"""
        You are a senior software engineer tasked with reviewing a coding assignment submitted by a {candidate_level}-level candidate.
        Provide a thorough analysis of the repository and assess the code quality based on industry best practices.
        
        ## Details of the Assignment:
        - **Assignment Description**: {assignment_description}
        - **Candidate Level**: {candidate_level}
        
        ### Instructions:
        1. **Identify and list the files in the repository**.
        2. **Analyze the code for the following criteria**:
           - Code organization and structure
           - Readability (variable names, comments, and documentation)
           - Code quality (best practices, performance, modularity)
           - Error handling and edge-case management
           - Use of testing (unit tests or integration tests)
        3. **Identify any potential issues or areas for improvement** in the codebase.
        4. **Provide a rating out of 5** based on the candidate's level and the code's quality.
        5. Write a **conclusion** summarizing the overall evaluation.

        Respond in the following structured format:
        ```
        ## Review Results
        **Found Files**:
        - <file1>
        - <file2>

        **Downsides/Comments**:
        1. <Comment on file1>
        2. <Comment on file2>

        **Rating**:
        <Rating>/5 (for {candidate_level}-level)

        **Conclusion**:
        <Your conclusion>
        ```

        ## Repo Contents:
        Here is the list of file contents provided in the repository:
        {repo_contents}

        Begin the review.
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a skilled software engineer providing a code review."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7,
    )

    return response.choices[0].message.content
