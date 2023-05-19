import ipywidgets as widgets
from IPython.display import display
from .answer_and_probe import Stage1_Question_Clarification, set_api_key
import openai

def set_api_key(api_key):
    openai.api_key = api_key

def start_session():
    # Create API key input field
    api_key_input = widgets.Textarea(
        value='',
        placeholder='Enter your OpenAI API key here...',
        description='API Key:',
        disable=False
    )
    
    api_key_button = widgets.Button(
        description='Set API Key',
        disable=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click me',
        layout=widgets.Layout(width='auto')
    )
    
    def set_key(b):
        api_key = api_key_input.value
        set_api_key(api_key)
        print("API key set successfully.")
        print("Interview session is now started. Here is the coding problem: ...")
    
    api_key_button.on_click(set_key)
    display(api_key_input, api_key_button)

    # Start the sessoin
    session = Stage1_Question_Clarification()
    user_input = widgets.Textarea(
    value='',
    placeholder='Type your question here...',
    description='Your question:',
    disable=False
    )

    probe_button = widgets.Button(
        description='Get probing question from tutor',
        disable=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click me',
        layout=widgets.Layout(width='auto')
    )

    answer_button = widgets.Button(
        description='Get answer from interviewer',
        disable=False,
        button_style='', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Click me',
        layout=widgets.Layout(width='auto')
    )

    def probe(b):
        question = session.probe()
        print(f"Assistant: {question}")

    def answer(b):
        question = user_input.value
        print(f"You: {question}")
        response = session.answer(question)
        print(f"Assistant: {response}")

    probe_button.on_click(probe)
    answer_button.on_click(answer)

    display(user_input, probe_button, answer_button)