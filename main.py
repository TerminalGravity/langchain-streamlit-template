import streamlit as st
from streamlit_chat import message

from langchain.chains import ConversationChain
from langchain.llms import OpenAI

from langchain.document_loaders import GitLoader

def load_repo_content(repo_url):
    # Define the path where you want to clone the repository
    repo_path = "./repo"

    # Create a GitLoader instance
    loader = GitLoader(clone_url=repo_url, repo_path=repo_path, branch="master")

    # Load the content of the repository
    data = loader.load()

    # You might want to process the data further depending on your needs
    # For now, let's just join all the content into a single string
    content = "\n".join(doc.page_content for doc in data)

    return content

loader = GitLoader(clone_url=repo_url, repo_path=repo_path, branch="master", file_filter=lambda file_path: file_path.endswith(".py"))

def load_chain():
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm)
    return chain

chain = load_chain()

# From here down is all the StreamLit UI.
st.set_page_config(page_title="LangChain", page_icon=":robot:")
st.header("LangChain")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

repo_url = st.text_input("GitHub Repo URL: ", key="repo")

if repo_url:
    repo_content = load_repo_content(repo_url)  # This is your custom function to load the repo content
    output = chain.run(input=repo_content)

def get_text():
    input_text = st.text_input("You: ", "Hello, how are you?", key="input")
    return input_text



user_input = get_text()

if user_input:
    output = chain.run(input=user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

