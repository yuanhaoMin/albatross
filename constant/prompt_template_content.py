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
Rate resumes based on each of the requirements in the position description and explain the reason. There are three levels of scoring: "不符合", "部分满足", and "完全匹配".
不符合 means that the resume does not meet or contain relevant information.
部分满足 means that the resume partially meets the requirements.
完全匹配 means that the resume fully meets the requirements.
Finally give a total score between 0/5 and 5/5. Reply in 中文.
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

belbin_team_role_position_description = """
Here are 9 belbin team roles:
```
Role: Resource Investigator
Description: Uses their inquisitive nature to find ideas to bring back to the team. 
Strengths: Outgoing, enthusiastic. Explores opportunities and develops contacts.
Weaknesses: Might be over-optimistic, and can lose interest once the initial enthusiasm has passed. They might forget to follow up on a lead.

Role: Teamworker
Description: Helps the team to gel, using their versatility to identify the work required and complete it on behalf of the team.
Strengths: Co-operative, perceptive, and diplomatic. Listens and averts friction.
Weaknesses: Can be indecisive in crunch situations and tends to avoid confrontation. Might be hesitant to make unpopular decisions.

Role: Co-ordinator
Description: Needed to focus on the team's objectives, draw out team members, and delegate work appropriately.
Strengths: Mature, confident, identifies talent. Clarifies goals.
Weaknesses: Can be seen as manipulative and might offload their own share of the work. They might over-delegate, leaving themselves little work to do.

Role: Plant
Description: Tends to be highly creative and good at solving problems in unconventional ways.
Strengths: Creative, imaginative, free-thinking, generates ideas and solves difficult problems.
Weaknesses: Might ignore incidentals, and may be too preoccupied to communicate effectively. They could be absent-minded or forgetful.  


Role: Monitor Evaluator
Description: Provides a logical eye, making impartial judgements where required, and weighs up the team's options in a dispassionate way.
Strengths: Sober, strategic, and discerning. Sees all options and judges accurately.
Weaknesses: Sometimes lacks the drive and ability to inspire others and can be overly critical. They could be slow to come to decisions.

Role: Specialist
Description: Brings in-depth knowledge of a key area to the team.
Strengths: Single-minded, self-starting, and dedicated. They provide specialist knowledge and skills.
Weaknesses: Tends to contribute on a narrow front and can dwell on the technicalities. They overload you with information.

Role: Shaper
Description: Provides the necessary drive to ensure that the team keeps moving and does not lose focus or momentum.
Strengths: Challenging, dynamic, thrives on pressure. Has the drive and courage to overcome obstacles.
Weaknesses: Can be prone to provocation, and may sometimes offend people's feelings. They could risk becoming aggressive and bad-humoured in their attempts to get things done.

Role: Implementer
Description: Needed to plan a workable strategy and carry it out as efficiently as possible.
Strengths: Practical, reliable, efficient. Turns ideas into actions and organises work that needs to be done.
Weaknesses: Can be a bit inflexible and slow to respond to new possibilities. They might be slow to relinquish their plans in favour of positive changes.

Role: Completer Finisher
Description: Most effectively used at the end of tasks to polish and scrutinise the work for errors, subjecting it to the highest standards of quality control.
Strengths: Painstaking, conscientious, anxious. Searches out errors. Polishes and perfects.
Weaknesses: Can be inclined to worry unduly, and reluctant to delegate. They could be accused of taking their perfectionism to extremes.

Here is the position description:
```
{position_description}
```
Please choose 3 roles that you think are most important for this position and explain why. Reply in 中文.
"""
java_rename = """
I want you to act as a senior developer and respect code naming convention.
Here is the function description:
```
{description}
```
Here is the code:
```
{code}
```
Please generate an api document for the above function. You can rename the function and its parameter to respect code naming conventions, making it easy to understand and accurately express the meaning.
Your output should not contain any code, just the api document.
Reply in 中文.
"""
