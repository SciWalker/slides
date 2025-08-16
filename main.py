import os
from typing import TypedDict
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama
from langgraph.graph import StateGraph, END

# --- LLM Definition ---
# This script now uses ChatOllama to connect to a local Ollama server.
# Make sure you have Ollama running and the 'gpt:oss' model pulled.
# You can pull the model by running: `ollama pull gpt:oss`
try:
    llm = ChatOllama(model="gpt-oss")
except Exception as e:
    print(f"Error initializing Ollama: {e}")
    print("Please ensure Ollama is running and the 'gpt:oss' model is available.")
    exit()

# --- Graph State Definition ---
class GraphState(TypedDict):
    markdown_script: str
    presentation_html: str
    feedback: str
    revision_count: int

# --- Node Definitions ---

def generate_presentation_node(state: GraphState):
    """
    Generates the initial Reveal.js presentation from the markdown script using an LLM.
    """
    print("--- 🧠 Node: generate_presentation ---")
    markdown = state['markdown_script']
    
    prompt = PromptTemplate(
        template="""You are an expert at creating web presentations.
Convert the following markdown script into a complete, single-file Reveal.js HTML presentation.
The HTML must be fully functional, including the necessary Reveal.js CSS and JS links from a CDN.
Create a new slide for each heading starting with '#' or '##'.
Use the content under the headings as the slide content.
For content within backticks like `assets/image.jpg`, convert it to an `<img>` tag using the exact relative path inside the backticks.
For lists, convert them to `<ul>` or `<ol>` tags.
Return only the raw HTML code, without any explanations or markdown code blocks.

Markdown:
{markdown}""",
        input_variables=["markdown"],
    )

    # Create the generation chain
    generate_chain = prompt | llm | StrOutputParser()
    
    generated_html = generate_chain.invoke({"markdown": markdown})
    
    return {
        "presentation_html": generated_html,
        "revision_count": 0
    }

def evaluate_presentation_node(state: GraphState):
    """
    Evaluates the generated HTML using an LLM and provides feedback.
    """
    print("--- 🧐 Node: evaluate_presentation ---")
    html = state['presentation_html']
    
    prompt = PromptTemplate(
        template="""You are a web development expert who reviews code.
Review the following Reveal.js HTML presentation. Provide a short, bulleted list of actionable suggestions for improvement.
Focus on things like changing the theme (e.g., from 'black.css' to 'white.css' or 'sky.css'), improving the layout, or making the HTML title more specific based on the H1 tag.
If the presentation is good and needs no changes, respond with the exact phrase: 'No improvements needed.'.

HTML Code:
{html}""",
        input_variables=["html"],
    )

    # Create the evaluation chain
    evaluate_chain = prompt | llm | StrOutputParser()
    
    feedback = evaluate_chain.invoke({"html": html})
    
    print(f"Feedback received:\n{feedback}")
    
    return {"feedback": feedback}

def improve_presentation_node(state: GraphState):
    """
    Applies the feedback to improve the presentation using an LLM.
    """
    print("--- ✨ Node: improve_presentation ---")
    html = state['presentation_html']
    feedback = state['feedback']
    
    prompt = PromptTemplate(
        template="""You are a web development expert who applies feedback to code.
You are given an HTML file and a list of suggestions for improvement.
Apply the suggestions to the original HTML code and return ONLY the new, complete, and raw HTML file.
Do not add any commentary, explanations, or markdown code blocks.

Original HTML:
{html}

Suggestions:
{feedback}

Improved HTML:
""",
        input_variables=["html", "feedback"],
    )

    # Create the improvement chain
    improve_chain = prompt | llm | StrOutputParser()

    improved_html = improve_chain.invoke({"html": html, "feedback": feedback})
    
    revision_count = state.get('revision_count', 0) + 1
    
    return {
        "presentation_html": improved_html,
        "revision_count": revision_count
    }

# --- Conditional Edge Logic ---

def should_continue_edge(state: GraphState):
    """
    Determines whether to continue to the improvement step or finish.
    """
    print("--- 🤔 Edge: should_continue ---")
    feedback = state['feedback']
    if "No improvements needed" in feedback:
        print("Decision: No improvements needed. Finishing.")
        return "end"
    else:
        print("Decision: Improvements suggested. Continuing to revision.")
        return "continue"

# --- Build the Graph ---
workflow = StateGraph(GraphState)

# Add the nodes
workflow.add_node("generator", generate_presentation_node)
workflow.add_node("evaluator", evaluate_presentation_node)
workflow.add_node("improver", improve_presentation_node)

# Set the entry point
workflow.set_entry_point("generator")

# Add the edges
workflow.add_edge("generator", "evaluator")
workflow.add_conditional_edges(
    "evaluator",
    should_continue_edge,
    {
        "continue": "improver",
        "end": END,
    },
)
# After one improvement, we'll end the process. You could loop back to the evaluator for more revisions.
workflow.add_edge("improver", END) 

# Compile the graph
app = workflow.compile()

# --- Run the Graph ---

# Sample Markdown Input from the user
markdown_input = """
# 主祷文（上）

## 主祷文
`assets/jesus_praying.jpg`

## 复习:祷告的目的
1. 目的一：荣耀神
2. 目的二：借着我们在福音上结果子，让世人认识神
3. 目的三：面对属灵征战

## 复习：祷告的陷阱
1. 依靠个人情感
2. 律法主义
3. 懒惰

## 经文
- 马太福音6:5-15
5. “你们祷告的时候，不可像那假冒为善的人，爱站在会堂里和十字路口祷告，故意让人看见。我实在告诉你们，他们已经得了他们的赏赐。 
6. 你祷告的时候，要进入内室，关上门，向那在隐秘中的父祷告；你父在隐秘中察看，必将赏赐你。 
7. 你们祷告，不可像外邦人那样重复一些空话，他们以为话多了必蒙垂听。 \
8. 你们不可效法他们。因为在你们祈求以前，你们所需要的，你们的父早已知道了。”
9. “所以，你们要这样祷告：‘我们在天上的父：愿人都尊你的名为圣。
10. 愿你的国降临；愿你的旨意行在地上，如同行在天上。
"""

# The initial state for the graph
initial_state = {"markdown_script": markdown_input}

# Invoke the graph and get the final state
final_state = app.invoke(initial_state, {"recursion_limit": 5})

# --- Final Output ---
final_html = final_state['presentation_html']

# Save the final HTML to a file to view it
output_filename = "presentation_ollama.html"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(final_html)

print(f"\n✅ Final presentation saved to '{output_filename}'")
print(f"Total revisions: {final_state['revision_count']}")
