default = "{question}"
pdf_chat = """
Please reply based on following pdf:
```
{pdf}
```
Here is the question/task:
{question}
"""

resume_screening = """
Rate resumes based on each of the requirements in the position description and explain the reason. There are three levels of scoring: "不符合", "部分满足", and "完全匹配". 不符合 means that the resume does not meet or contain relevant information. 部分满足 means that the resume partially meets the requirements. 完全匹配 means that the resume fully meets the requirements.
Here is the resume:
```
{pdf}
```
The following is the position description:
```
{position_description}
```
Finally give a total score between 0/5 and 5/5. Reply in 中文.
"""

interview_questions = """
You are an interviewer. the job position has following requirement:
```
{requirement}
```
Ask some interview questions that can test the candidate, also provide a template answer. Reply in 中文.
"""
