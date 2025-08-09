# import the packages
import openai
import gradio as gr
import json
from typing import List, Dict, Tuple

client = openai.OpenAI()

# Check if you have set your ChatGPT API successfully
# You should see "Set ChatGPT API sucessfully!!" if nothing goes wrong.
try:
    response = client.responses.create(
            model="gpt-4o-mini-2024-07-18",
            input = "test",
    )
    print("Set ChatGPT API sucessfully!!")
except:
    print("There seems to be something wrong with your ChatGPT API. Please follow our demonstration in the slide to get a correct one.")




# function to clear the conversation
def reset() -> List:
    return [], None

# function to call the model to generate
def interact_customize(chatbot: List[Tuple[str, str]], previous_id: str, user_input: str, temperature = 1.0) -> Tuple[str, List[Tuple[str, str]]]:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - previous_id: the id of the previous response, used to continue the conversation

      - prompt: the prompt for your desginated task

      - user_input: the user input of each round of conversation

      - temp: the temperature parameter of this model. Temperature is used to control the output of the chatbot.
              The higher the temperature is, the more creative response you will get.

    '''
    try:

        response = client.responses.create(
            model="gpt-4o-mini-2024-07-18",
            input = user_input,
            temperature = temperature,
            # reasoning={"effort": "low"},
            previous_response_id=previous_id,
            # max_tokens=200,
        )

        chatbot.append((user_input, response.output_text))
        return response.id, chatbot

    except Exception as e:
        print(f"Error occurred: {e}")
        chatbot.append((user_input, f"Sorry, an error occurred: {e}"))
        return previous_id, chatbot

# function to export the whole conversation log
def export_customized(chatbot: List[Tuple[str, str]]) -> None:
    '''
    * Arguments

      - chatbot: the model itself, the conversation is stored in list of tuples

      - description: the description of this task

    '''
    target = {"chatbot": chatbot}
    with open("part3.json", "w") as file:
        json.dump(target, file)

# this part constructs the Gradio UI interface
with gr.Blocks() as demo:
    gr.Markdown("# Part3: Customized task\nThe chatbot is able to perform a certain task. Try to interact with it!!")
    chatbot = gr.Chatbot()
    previous_id = gr.State()
    input_textbox = gr.Textbox(label="Input")
    with gr.Column():
        gr.Markdown("#  Temperature\n Temperature is used to control the output of the chatbot. The higher the temperature is, the more creative response you will get.")
        temperature_slider = gr.Slider(0.0, 2.0, 1.0, step = 0.1, label="Temperature")
    with gr.Row():
        sent_button = gr.Button(value="Send")
        reset_button = gr.Button(value="Reset")
    with gr.Column():
        gr.Markdown("#  Save your Result.\n After you get a satisfied result. Click the export button to recode it.")
        export_button = gr.Button(value="Export")
    sent_button.click(interact_customize, inputs=[chatbot, previous_id, input_textbox, temperature_slider], outputs=[previous_id,chatbot])
    reset_button.click(reset, outputs=[chatbot,previous_id])
    export_button.click(export_customized, inputs=[chatbot])

demo.launch(debug = True)