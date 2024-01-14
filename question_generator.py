import openai
import json
from openai import OpenAI

prompt_template = """
You have an optimization problem statement. You want to design a question for an optimization exam to evaluate the skills of students in asking relevant clarifying questions. Your task is to remove different parts of an optimization problem, and generate a clarifying question that would address the consequent ambiguity. Generate a list of jsons in the following format:

[{{
     "vague_problem_description": str,
      "clarifying_question": str
}},
...
]

Note that the ambiguities are only about the abstract problem statement, and the exact values of parameters are available in a data file. Some examples of interesting ambiguities are as follows:

- Undefined Variables: you can remove information about the variables in the problem and what are the things that the user can control.

- Implicit constraints: you can consider descriptions where certain constraints are not explicitly mentioned, but might hold because of the problem domain or common sense. For instance "is the number of products produced integral/non-negative?", or "Can the investor short stocks?".

- Unclear Objectives: You can omit some information about the objective to make it unclear. For instance, does an investor want to minimize the risk, or maximize the profit? or maybe a mix of both?

Here is the original problem statement:

{problem_description}

- The vague description must still be almost as long as the original description (at least aound 80 percent as long). Just modify a small part of the description to add the ambiguity.
- Generate 1 to 3 questions.
- Do not explicitly mention the problem is vague in the vague description. It should look like a clear problem. 
- Only generate the JSON list and nothing else.
Take a deep breath and solve the problem step by step.
"""

# Read raw.txt file
with open("raw.txt", "r") as file:
    content = file.read()

# Separate content by "---"
items = content.split("---")


client = OpenAI(
    api_key="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",
    organization="org-h7YtgEYseIptBaP1VKWbf8V8",
)

# Create separate json files for each item
for i, item in enumerate(items, 6):
    print("====", i, "====")
    item = item.strip()
    if len(item) < 20:
        continue
    prompt = prompt_template.format(problem_description=item.strip())

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {
                "role": "system",
                "content": "You are a university professor in optimizatoin, and you are desining an exam for your class.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    output = completion.choices[0].message.content

    print(output)
    # separate the part between ```json and ```
    if "```json" in output:
        output = output.split("```json")[1].split("```")[0]
        output = output.strip()
    output = json.loads(output)

    print(json.dumps(output, indent=4))
    output = {
        "original_problem_description": item,
        "questions": output,
    }
    # save it to file:

    with open(f"dataset/index{i}.json", "w") as file:
        json.dump(output, file, indent=4)
