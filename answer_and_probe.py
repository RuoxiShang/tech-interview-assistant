import os
import openai
import argparse
openai.api_key = "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"

def tag_stage1(user_input, coding_problem):
    instruction = """Now is the question clarification stage of a technical interview. 
    You need to flag their question using the following schema, if the input is:
    Unrelated to solving the coding problem, answer "N1";
    Directly asking for solution or code samples, answer "N2";
    Not a question, answer "N3".
    Otherwise, answer "Y"."""
    
    conversation = [
        {"role": "system", "content": instruction},
        {"role": "assistant", "content": coding_problem},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=conversation
    )
    tag = response['choices'][0]['message']['content']
    return tag

class Stage1_Question_Clarification:
    _instruction = """
    You are an interviewer. 
    This is the time for the interviewee to ask clarification questions during the interview.
    If the interviewee is not asking questions, ask probign questions to encourage them.
    Start with a broad question and gradually get more specific based on their responses. 
    For example, start with "Don't you have any questions?" and progress to "Do you understand what the input data type is?" 
    Remember to adapt your probing questions based on the programmer's responses. 
    If they ask a clarifying question, provide an answer. 
    Avoid being repetitive in your questions."""
    
    _coding_problem = """
    Here's the coding problem. 
    You are given two non-empty linked lists representing two non-negative integers. 
    The digits are stored in reverse order, and each of their nodes contains a single digit. 
    Add the two numbers and return the sum as a linked list. 
    You can only ask me clarification questions."""

    def __init__(self):
        self.conversation = [
        {"role": "system", "content": self._instruction},
        {"role": "assistant", "content": self._coding_problem}
        ]
    
    def answer(self, user_input):
        if tag_stage1(user_input, self._coding_problem) != 'Y':
            return "Please ask a question relevant to clarifying the coding problem."
        self.conversation.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=self.conversation
        )
        answer = response['choices'][0]['message']['content']
        self.conversation.append({"role": "assistant", "content": answer})
        return answer

    def probe(self):
        response = openai.ChatCompletion.create(
          model="gpt-4",
          messages=self.conversation
        )
        question = response['choices'][0]['message']['content']
        self.conversation.append({"role": "assistant", "content": question})
        return question

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--answer", type=str, help="Input string for the 'answer' function")
    parser.add_argument("--probe", action='store_true', help="Call the 'probe' function")
    args = parser.parse_args()

    stage1 = Stage1_Question_Clarification()

    if args.answer:
        print(stage1.answer(args.answer))
    elif args.probe:
        print(stage1.probe())