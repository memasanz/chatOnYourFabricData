# Chat on Your Fabric Data

This repository demonstrates multiple approaches to building conversational AI agents that can interact with Microsoft Fabric data warehouses. The project explores different architectures and technologies including Azure AI Foundry Agents, Semantic Kernel, and direct SQL connectivity to enable natural language querying of your Fabric data.

## Project Overview

The notebooks in this repository showcase various methods to create "chat with your data" experiences using Microsoft Fabric as the data source. Each approach has different strengths and use cases:

- **Azure AI Foundry Data Agents**: Leverages built-in Fabric connectivity through AI Foundry's native data agent tools
- **Semantic Kernel with SQL**: Combines Microsoft's Semantic Kernel framework with direct SQL connectivity to Fabric endpoints
- **Custom SQL Tools**: Creates custom agents with specialized SQL query capabilities for Fabric warehouses

## Notebook Breakdown

### 000_AgentDataAgentConnection.ipynb
**Purpose**: Azure AI Foundry Data Agent Setup and Connection  
**What it accomplishes**: 
- Demonstrates how to create and configure an Azure AI Foundry Data Agent
- Shows the connection process to Microsoft Fabric through AI Foundry's native data agent capabilities
- Provides examples of getting run IDs and managing agent interactions
- Serves as the foundation for understanding AI Foundry's built-in Fabric integration

### 001_CallFabricThroughSQL.ipynb  
**Purpose**: Direct Fabric SQL Endpoint Connectivity Testing  
**What it accomplishes**:
- Tests and validates direct programmatic connection to Microsoft Fabric SQL endpoints
- Demonstrates proper ODBC driver configuration and authentication setup
- Provides troubleshooting guidance for Fabric SQL connectivity issues
- Serves as a foundation for building custom SQL-based agents when native Fabric Data Agents are insufficient
- Includes examples of querying table schemas and executing basic SQL operations

### 002_SemanticKernelHelloWorld.ipynb
**Purpose**: Semantic Kernel Introduction and Setup Validation  
**What it accomplishes**:
- Introduces Microsoft's Semantic Kernel framework with basic "hello world" examples
- Validates Azure OpenAI service connectivity and configuration
- Demonstrates fundamental chat completion functionality
- Provides a foundation for understanding Semantic Kernel concepts before integrating with Fabric data
- Includes sample conversational AI interactions (email writing example)

### 003_SemanticKernelFabricChat.ipynb
**Purpose**: Semantic Kernel + Fabric SQL Integration  
**What it accomplishes**:
- Combines Semantic Kernel's conversational AI capabilities with Fabric SQL connectivity
- Implements a custom Fabric SQL plugin that enables natural language querying of Fabric data
- Demonstrates how to create a conversational agent that can explore database schemas and answer data questions
- Provides the core logic that powers the Streamlit web application
- Shows advanced function calling and tool integration patterns

### 003_SemanticKernelFabricChat.py
**Purpose**: Streamlit Web Application  
**What it accomplishes**:
- Provides a user-friendly web interface for the Semantic Kernel + Fabric integration
- Implements a chat-based UI where users can ask natural language questions about their Fabric data
- Demonstrates how to deploy the conversational data agent as a web application
- **Usage**: Run with `python -m streamlit run 003_SemanticKernelFabricChat.py`

![Chat on Your Data Front End](images/ChatOnYourDataFrontEnd.jpg)

### 004_AIFoundryAgentWithSQLTool.ipynb
**Purpose**: AI Foundry Agent with Custom SQL Tools  
**What it accomplishes**:
- Creates an Azure AI Foundry agent equipped with specialized SQL query tools
- Demonstrates advanced agent capabilities including schema exploration and intelligent query generation
- Shows how to combine AI Foundry's agent framework with custom SQL functionality
- Provides an alternative architecture when you need more control over SQL operations than native Fabric Data Agents provide
- Includes examples of complex data exploration and question-answering workflows

## Prerequisites

Before running the notebooks, ensure you have the following:

### Software Requirements
- **Python 3.11+**: All notebooks are tested with Python 3.11.9
- **ODBC Driver 18 for SQL Server**: Required for direct Fabric SQL connectivity
- **Azure CLI**: For authentication (`az login` required)

### Azure Resources Required
- **Microsoft Fabric Workspace**: With a data warehouse containing your data
- **Azure OpenAI Service**: With deployed models (GPT-4 and text-embedding models)
- **Azure AI Foundry Project**: For AI agent-based approaches
- **Appropriate Azure Permissions**: To access Fabric, OpenAI, and AI Foundry resources

### Installation
1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your environment variables (see below)
4. Authenticate with Azure: `az login`

## Environment Configuration

Create a `.env` file in the root directory with the following configuration:

```env
# Fabric Connection Settings
FABRIC_CONNECTION_STRING=your-fabric-warehouse.datawarehouse.fabric.microsoft.com
FABRIC_WAREHOUSE=your-fabric-warehouse-name
FABRIC_TEST_TABLE=your-test-table-name

# Azure OpenAI Settings
GLOBAL_LLM_SERVICE="AzureOpenAI"
AZURE_OPENAI_API_KEY="your-openai-api-key"
AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-4"
AZURE_OPENAI_TEXT_DEPLOYMENT_NAME="gpt-4"
AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME="text-embedding-3-large"
AZURE_OPENAI_API_VERSION="2024-12-01-preview"

# Azure AI Search Settings (Optional)
AZURE_AISEARCH_API_KEY=""
AZURE_AISEARCH_URL=""

# Azure AI Foundry Settings
AZURE_AI_AGENT_NAME="AIFoundryAgentWithSQLTool05"
PROJECT_ENDPOINT="https://your-resource.services.ai.azure.com/api/projects/your-project"
AZURE_AI_AGENT_DEPLOYMENT_NAME="AIFoundryAgentWithSQLTool"
AZURE_AI_FABRIC_AGENT_NAME="AIFoundryDataAgent"
AZURE_FABRIC_CONNECTION_ID="/subscriptions/your-subscription-id/resourceGroups/your-rg/providers/Microsoft.CognitiveServices/accounts/your-resource/projects/your-project/connections/FabricConnection"
```

## Getting Started

1. **Start with Prerequisites**: Ensure all Azure resources are properly configured
2. **Test Basic Connectivity**: Run `002_SemanticKernelHelloWorld.ipynb` to validate your Azure OpenAI setup
3. **Validate Fabric Connection**: Run `001_CallFabricThroughSQL.ipynb` to test Fabric SQL connectivity
4. **Choose Your Approach**: 
   - For built-in Fabric integration: Start with `000_AgentDataAgentConnection.ipynb`
   - For custom SQL control: Try `003_SemanticKernelFabricChat.ipynb`
   - For advanced agent capabilities: Explore `004_AIFoundryAgentWithSQLTool.ipynb`
5. **Deploy Web Interface**: Use `003_SemanticKernelFabricChat.py` for a user-friendly web application

## Architecture Considerations

This repository demonstrates multiple architectural approaches, each with different trade-offs:

- **Native Fabric Data Agents** (000, 004): Best for out-of-the-box functionality with minimal custom code
- **Semantic Kernel + SQL** (003): Provides more control over query generation and data processing
- **Direct SQL Connectivity** (001): Offers maximum flexibility but requires more manual implementation

Choose the approach that best fits your specific requirements for data access patterns, customization needs, and deployment constraints.