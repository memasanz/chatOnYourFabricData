#streamlit web app that uses the semantic kernel to generate jokes
#on local machine run: streamlit run 001_jokewebapp.py

import streamlit as st
import asyncio
from typing import Annotated
import os
from semantic_kernel.agents import ChatCompletionAgent
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.contents.utils.author_role import AuthorRole
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (AzureChatPromptExecutionSettings,)
from semantic_kernel.functions.kernel_function_decorator import kernel_function
from semantic_kernel.kernel import Kernel
from semantic_kernel.functions import KernelArguments

from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments


from semantic_kernel import Kernel
from semantic_kernel.functions import kernel_function
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.connectors.ai import FunctionChoiceBehavior
from semantic_kernel.connectors.ai.chat_completion_client_base import ChatCompletionClientBase
from semantic_kernel.contents.chat_history import ChatHistory
from semantic_kernel.functions.kernel_arguments import KernelArguments
from semantic_kernel.connectors.ai.open_ai.prompt_execution_settings.azure_chat_prompt_execution_settings import (
    AzureChatPromptExecutionSettings,
)

from semantic_kernel.contents import ChatMessageContent, TextContent, ImageContent
from semantic_kernel.contents.utils.author_role import AuthorRole

import os
from Plugin.FabricSQLPlugin import FabricSQLPlugin


@st.cache_resource
def setup_kernel_and_chat():
    kernel = Kernel()
    # Remove all services so that this cell can be re-run without restarting the kernel
    kernel.remove_all_services()

    service_id = "default"
    kernel.add_service(AzureChatCompletion(service_id=service_id,),)
    kernel.add_plugin(FabricSQLPlugin(),plugin_name="FabricSQL",)
 

    chat_completion : AzureChatCompletion = kernel.get_service(type=ChatCompletionClientBase)

    return kernel, chat_completion

global_kernel, global_chat = setup_kernel_and_chat()

# A helper method to invoke the agent with the user input
async def invoke_agent(input_text):
   
    
    # Enable planning
    execution_settings = AzureChatPromptExecutionSettings(tool_choice="auto")
    execution_settings.function_choice_behavior = FunctionChoiceBehavior.Auto()


    st.session_state["history"].add_user_message(input_text)

    result = (await global_chat.get_chat_message_contents(
            chat_history=st.session_state["history"],
            settings=execution_settings,
            kernel=global_kernel,
            arguments=KernelArguments(),
        ))[0]
    print(str(result))

    st.session_state["history"].add_assistant_message(str(result))
    return str(result)




async def run_app():
    st.title("PlugIn Bot")
    st.write('gpt model with Fabric SQL Plugin')
    #st.write('This assumes you have a SQL Server')

    reset = st.button('Reset Messages')

    system_message = """
        You are a Fabric SQL expert.  You have tools to explore the database by getting tables, getting the schema and executing SQL select statements.
        Explore the schema of tables to create sql to answer the questions asked.
        You can ask clarifying questions if needed.

        You have information regarding World Wide Importers Customer Profiles from a Fabric SQL Endpoint
        To Write Valid SQL - you must use the Fully Qualifed Name [warehouse].[schema].[table] in ALL SQL queries.

        You do have a tool to determine what the warehouse is, what tables are available, and what their schema is.
        The correct schema will be required for any joins you do on the data to answer complex questions.
        """

    if reset:
            st.write('Sure thing!')
            history = ChatHistory()
            st.session_state["history"] = history
            st.session_state["history"].add_system_message(system_message) 
            print("completed reset")
            reset = False

    if "history" not in st.session_state:  
        history = ChatHistory()
        st.session_state["history"] = history
        st.session_state["history"].add_system_message(system_message) 

    
 


    for msg in st.session_state["history"]:
        print(msg.role + ":" + msg.content)
        if msg.role != AuthorRole.TOOL and len(msg.content) > 0:
            with st.chat_message(msg.role):
                st.markdown(msg.content)

    # React to user input
    if prompt := st.chat_input("Tell me about a Question that you have.."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        result = await invoke_agent( prompt)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(result)

asyncio.run(run_app())  