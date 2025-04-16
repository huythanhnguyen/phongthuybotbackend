google
Submodules
google.adk.agents module
Agent
BaseAgent
BaseAgent.after_agent_callback
BaseAgent.before_agent_callback
BaseAgent.description
BaseAgent.name
BaseAgent.parent_agent
BaseAgent.sub_agents
BaseAgent.find_agent()
BaseAgent.find_sub_agent()
BaseAgent.model_post_init()
BaseAgent.run_async()
BaseAgent.run_live()
BaseAgent.root_agent
LlmAgent
LlmAgent.after_model_callback
LlmAgent.after_tool_callback
LlmAgent.before_model_callback
LlmAgent.before_tool_callback
LlmAgent.code_executor
LlmAgent.disallow_transfer_to_parent
LlmAgent.disallow_transfer_to_peers
LlmAgent.examples
LlmAgent.generate_content_config
LlmAgent.global_instruction
LlmAgent.include_contents
LlmAgent.input_schema
LlmAgent.instruction
LlmAgent.model
LlmAgent.output_key
LlmAgent.output_schema
LlmAgent.planner
LlmAgent.tools
LlmAgent.canonical_global_instruction()
LlmAgent.canonical_instruction()
LlmAgent.canonical_model
LlmAgent.canonical_tools
LoopAgent
LoopAgent.max_iterations
ParallelAgent
SequentialAgent
google.adk.artifacts module
BaseArtifactService
BaseArtifactService.delete_artifact()
BaseArtifactService.list_artifact_keys()
BaseArtifactService.list_versions()
BaseArtifactService.load_artifact()
BaseArtifactService.save_artifact()
GcsArtifactService
GcsArtifactService.delete_artifact()
GcsArtifactService.list_artifact_keys()
GcsArtifactService.list_versions()
GcsArtifactService.load_artifact()
GcsArtifactService.save_artifact()
InMemoryArtifactService
InMemoryArtifactService.artifacts
InMemoryArtifactService.delete_artifact()
InMemoryArtifactService.list_artifact_keys()
InMemoryArtifactService.list_versions()
InMemoryArtifactService.load_artifact()
InMemoryArtifactService.save_artifact()
google.adk.code_executors module
BaseCodeExecutor
BaseCodeExecutor.optimize_data_file
BaseCodeExecutor.stateful
BaseCodeExecutor.error_retry_attempts
BaseCodeExecutor.code_block_delimiters
BaseCodeExecutor.execution_result_delimiters
BaseCodeExecutor.code_block_delimiters
BaseCodeExecutor.error_retry_attempts
BaseCodeExecutor.execution_result_delimiters
BaseCodeExecutor.optimize_data_file
BaseCodeExecutor.stateful
BaseCodeExecutor.execute_code()
CodeExecutorContext
CodeExecutorContext.add_input_files()
CodeExecutorContext.add_processed_file_names()
CodeExecutorContext.clear_input_files()
CodeExecutorContext.get_error_count()
CodeExecutorContext.get_execution_id()
CodeExecutorContext.get_input_files()
CodeExecutorContext.get_processed_file_names()
CodeExecutorContext.get_state_delta()
CodeExecutorContext.increment_error_count()
CodeExecutorContext.reset_error_count()
CodeExecutorContext.set_execution_id()
CodeExecutorContext.update_code_execution_result()
ContainerCodeExecutor
ContainerCodeExecutor.base_url
ContainerCodeExecutor.image
ContainerCodeExecutor.docker_path
ContainerCodeExecutor.base_url
ContainerCodeExecutor.docker_path
ContainerCodeExecutor.image
ContainerCodeExecutor.optimize_data_file
ContainerCodeExecutor.stateful
ContainerCodeExecutor.execute_code()
ContainerCodeExecutor.model_post_init()
UnsafeLocalCodeExecutor
UnsafeLocalCodeExecutor.optimize_data_file
UnsafeLocalCodeExecutor.stateful
UnsafeLocalCodeExecutor.execute_code()
VertexAiCodeExecutor
VertexAiCodeExecutor.resource_name
VertexAiCodeExecutor.resource_name
VertexAiCodeExecutor.execute_code()
VertexAiCodeExecutor.model_post_init()
google.adk.evaluation module
AgentEvaluator
AgentEvaluator.evaluate()
AgentEvaluator.find_config_for_test_file()
google.adk.events module
Event
Event.invocation_id
Event.author
Event.actions
Event.long_running_tool_ids
Event.branch
Event.id
Event.timestamp
Event.is_final_response
Event.get_function_calls
Event.actions
Event.author
Event.branch
Event.id
Event.invocation_id
Event.long_running_tool_ids
Event.timestamp
Event.get_function_calls()
Event.get_function_responses()
Event.has_trailing_code_exeuction_result()
Event.is_final_response()
Event.model_post_init()
Event.new_id()
EventActions
EventActions.artifact_delta
EventActions.escalate
EventActions.requested_auth_configs
EventActions.skip_summarization
EventActions.state_delta
EventActions.transfer_to_agent
google.adk.examples module
BaseExampleProvider
BaseExampleProvider.get_examples()
Example
Example.input
Example.output
Example.input
Example.output
VertexAiExampleStore
VertexAiExampleStore.get_examples()
google.adk.memory module
BaseMemoryService
BaseMemoryService.add_session_to_memory()
BaseMemoryService.search_memory()
InMemoryMemoryService
InMemoryMemoryService.add_session_to_memory()
InMemoryMemoryService.search_memory()
InMemoryMemoryService.session_events
VertexAiRagMemoryService
VertexAiRagMemoryService.add_session_to_memory()
VertexAiRagMemoryService.search_memory()
google.adk.models module
BaseLlm
BaseLlm.model
BaseLlm.model_config
BaseLlm.model
BaseLlm.connect()
BaseLlm.generate_content_async()
BaseLlm.supported_models()
Gemini
Gemini.model
Gemini.model
Gemini.connect()
Gemini.generate_content_async()
Gemini.supported_models()
Gemini.api_client
LLMRegistry
LLMRegistry.new_llm()
LLMRegistry.register()
LLMRegistry.resolve()
google.adk.planners module
BasePlanner
BasePlanner.build_planning_instruction()
BasePlanner.process_planning_response()
BuiltInPlanner
BuiltInPlanner.thinking_config
BuiltInPlanner.apply_thinking_config()
BuiltInPlanner.build_planning_instruction()
BuiltInPlanner.process_planning_response()
BuiltInPlanner.thinking_config
PlanReActPlanner
PlanReActPlanner.build_planning_instruction()
PlanReActPlanner.process_planning_response()
google.adk.runners module
InMemoryRunner
InMemoryRunner.agent
InMemoryRunner.app_name
Runner
Runner.app_name
Runner.agent
Runner.artifact_service
Runner.session_service
Runner.memory_service
Runner.agent
Runner.app_name
Runner.artifact_service
Runner.close_session()
Runner.memory_service
Runner.run()
Runner.run_async()
Runner.run_live()
Runner.session_service
google.adk.sessions module
BaseSessionService
BaseSessionService.append_event()
BaseSessionService.close_session()
BaseSessionService.create_session()
BaseSessionService.delete_session()
BaseSessionService.get_session()
BaseSessionService.list_events()
BaseSessionService.list_sessions()
DatabaseSessionService
DatabaseSessionService.append_event()
DatabaseSessionService.create_session()
DatabaseSessionService.delete_session()
DatabaseSessionService.get_session()
DatabaseSessionService.list_events()
DatabaseSessionService.list_sessions()
InMemorySessionService
InMemorySessionService.append_event()
InMemorySessionService.create_session()
InMemorySessionService.delete_session()
InMemorySessionService.get_session()
InMemorySessionService.list_events()
InMemorySessionService.list_sessions()
Session
Session.id
Session.app_name
Session.user_id
Session.state
Session.events
Session.last_update_time
Session.app_name
Session.events
Session.id
Session.last_update_time
Session.state
Session.user_id
State
State.APP_PREFIX
State.TEMP_PREFIX
State.USER_PREFIX
State.get()
State.has_delta()
State.to_dict()
State.update()
VertexAiSessionService
VertexAiSessionService.append_event()
VertexAiSessionService.create_session()
VertexAiSessionService.delete_session()
VertexAiSessionService.get_session()
VertexAiSessionService.list_events()
VertexAiSessionService.list_sessions()
google.adk.tools module
APIHubToolset
APIHubToolset.get_tool()
APIHubToolset.get_tools()
AuthToolArguments
AuthToolArguments.auth_config
AuthToolArguments.function_call_id
BaseTool
BaseTool.description
BaseTool.is_long_running
BaseTool.name
BaseTool.process_llm_request()
BaseTool.run_async()
ExampleTool
ExampleTool.examples
ExampleTool.process_llm_request()
FunctionTool
FunctionTool.func
FunctionTool.run_async()
LongRunningFunctionTool
LongRunningFunctionTool.is_long_running
ToolContext
ToolContext.invocation_context
ToolContext.function_call_id
ToolContext.event_actions
ToolContext.actions
ToolContext.get_auth_response()
ToolContext.list_artifacts()
ToolContext.request_credential()
ToolContext.search_memory()
VertexAiSearchTool
VertexAiSearchTool.data_store_id
VertexAiSearchTool.search_engine_id
VertexAiSearchTool.process_llm_request()
exit_loop()
transfer_to_agent()
Submodules
google.adk.agents module
google.adk.agents.Agent
alias of LlmAgent

pydantic model google.adk.agents.BaseAgent
Bases: BaseModel

Base class for all agents in Agent Development Kit.

Show JSON schema
Fields:
after_agent_callback (Callable[[google.adk.agents.callback_context.CallbackContext], google.genai.types.Content | None] | None)

before_agent_callback (Callable[[google.adk.agents.callback_context.CallbackContext], google.genai.types.Content | None] | None)

description (str)

name (str)

parent_agent (google.adk.agents.base_agent.BaseAgent | None)

sub_agents (list[google.adk.agents.base_agent.BaseAgent])

Validators:
__validate_name » name

field after_agent_callback: Optional[AfterAgentCallback] = None
Callback signature that is invoked after the agent run.

Parameters:
callback_context – MUST be named ‘callback_context’ (enforced).

Returns:
The content to return to the user. When set, the agent run will skipped and the provided content will be appended to event history as agent response.

field before_agent_callback: Optional[BeforeAgentCallback] = None
Callback signature that is invoked before the agent run.

Parameters:
callback_context – MUST be named ‘callback_context’ (enforced).

Returns:
The content to return to the user. When set, the agent run will skipped and the provided content will be returned to user.

field description: str = ''
Description about the agent’s capability.

The model uses this to determine whether to delegate control to the agent. One-line description is enough and preferred.

field name: str [Required]
The agent’s name.

Agent name must be a Python identifier and unique within the agent tree. Agent name cannot be “user”, since it’s reserved for end-user’s input.

Validated by:
__validate_name

field parent_agent: Optional[BaseAgent] = None
The parent agent of this agent.

Note that an agent can ONLY be added as sub-agent once.

If you want to add one agent twice as sub-agent, consider to create two agent instances with identical config, but with different name and add them to the agent tree.

field sub_agents: list[BaseAgent] [Optional]
The sub-agents of this agent.

find_agent(name)
Finds the agent with the given name in this agent and its descendants.

Return type:
Optional[BaseAgent]

Parameters:
name – The name of the agent to find.

Returns:
The agent with the matching name, or None if no such agent is found.

find_sub_agent(name)
Finds the agent with the given name in this agent’s descendants.

Return type:
Optional[BaseAgent]

Parameters:
name – The name of the agent to find.

Returns:
The agent with the matching name, or None if no such agent is found.

model_post_init(_BaseAgent__context)
Override this method to perform additional initialization after __init__ and model_construct. This is useful if you want to do some validation that requires the entire model to be initialized.

Return type:
None

final async run_async(parent_context)
Entry method to run an agent via text-based conversaction.

Return type:
AsyncGenerator[Event, None]

Parameters:
parent_context – InvocationContext, the invocation context of the parent agent.

Yields:
Event – the events generated by the agent.

final async run_live(parent_context)
Entry method to run an agent via video/audio-based conversaction.

Return type:
AsyncGenerator[Event, None]

Parameters:
parent_context – InvocationContext, the invocation context of the parent agent.

Yields:
Event – the events generated by the agent.

property root_agent: BaseAgent
Gets the root agent of this agent.

pydantic model google.adk.agents.LlmAgent
Bases: BaseAgent

LLM-based Agent.

Show JSON schema
Fields:
after_model_callback (Optional[AfterModelCallback])

after_tool_callback (Optional[AfterToolCallback])

before_model_callback (Optional[BeforeModelCallback])

before_tool_callback (Optional[BeforeToolCallback])

code_executor (Optional[BaseCodeExecutor])

disallow_transfer_to_parent (bool)

disallow_transfer_to_peers (bool)

examples (Optional[ExamplesUnion])

generate_content_config (Optional[types.GenerateContentConfig])

global_instruction (Union[str, InstructionProvider])

include_contents (Literal['default', 'none'])

input_schema (Optional[type[BaseModel]])

instruction (Union[str, InstructionProvider])

model (Union[str, BaseLlm])

output_key (Optional[str])

output_schema (Optional[type[BaseModel]])

planner (Optional[BasePlanner])

tools (list[ToolUnion])

Validators:
__model_validator_after » all fields

__validate_generate_content_config » generate_content_config

field after_model_callback: Optional[AfterModelCallback] = None
Called after calling LLM.

Parameters:
callback_context – CallbackContext,

llm_response – LlmResponse, the actual model response.

Returns:
The content to return to the user. When present, the actual model response will be ignored and the provided content will be returned to user.

Validated by:
__model_validator_after

field after_tool_callback: Optional[AfterToolCallback] = None
Called after the tool is called.

Parameters:
tool – The tool to be called.

args – The arguments to the tool.

tool_context – ToolContext,

tool_response – The response from the tool.

Returns:
When present, the returned dict will be used as tool result.

Validated by:
__model_validator_after

field before_model_callback: Optional[BeforeModelCallback] = None
Called before calling the LLM. :param callback_context: CallbackContext, :param llm_request: LlmRequest, The raw model request. Callback can mutate the :param request.:

Returns:
The content to return to the user. When present, the model call will be skipped and the provided content will be returned to user.

Validated by:
__model_validator_after

field before_tool_callback: Optional[BeforeToolCallback] = None
Called before the tool is called.

Parameters:
tool – The tool to be called.

args – The arguments to the tool.

tool_context – ToolContext,

Returns:
The tool response. When present, the returned tool response will be used and the framework will skip calling the actual tool.

Validated by:
__model_validator_after

field code_executor: Optional[BaseCodeExecutor] = None
Allow agent to execute code blocks from model responses using the provided CodeExecutor.

Check out available code executions in google.adk.code_executor package.

NOTE: to use model’s built-in code executor, don’t set this field, add google.adk.tools.built_in_code_execution to tools instead.

Validated by:
__model_validator_after

field disallow_transfer_to_parent: bool = False
Disallows LLM-controlled transferring to the parent agent.

Validated by:
__model_validator_after

field disallow_transfer_to_peers: bool = False
Disallows LLM-controlled transferring to the peer agents.

Validated by:
__model_validator_after

field examples: Optional[ExamplesUnion] = None
Validated by:
__model_validator_after

field generate_content_config: Optional[types.GenerateContentConfig] = None
The additional content generation configurations.

NOTE: not all fields are usable, e.g. tools must be configured via tools, thinking_config must be configured via planner in LlmAgent.

For example: use this config to adjust model temperature, configure safety settings, etc.

Validated by:
__model_validator_after

__validate_generate_content_config

field global_instruction: Union[str, InstructionProvider] = ''
Instructions for all the agents in the entire agent tree.

global_instruction ONLY takes effect in root agent.

For example: use global_instruction to make all agents have a stable identity or personality.

Validated by:
__model_validator_after

field include_contents: Literal['default', 'none'] = 'default'
Whether to include contents in the model request.

When set to ‘none’, the model request will not include any contents, such as user messages, tool results, etc.

Validated by:
__model_validator_after

field input_schema: Optional[type[BaseModel]] = None
The input schema when agent is used as a tool.

Validated by:
__model_validator_after

field instruction: Union[str, InstructionProvider] = ''
Instructions for the LLM model, guiding the agent’s behavior.

Validated by:
__model_validator_after

field model: Union[str, BaseLlm] = ''
The model to use for the agent.

When not set, the agent will inherit the model from its ancestor.

Validated by:
__model_validator_after

field output_key: Optional[str] = None
The key in session state to store the output of the agent.

Typically use cases: - Extracts agent reply for later use, such as in tools, callbacks, etc. - Connects agents to coordinate with each other.

Validated by:
__model_validator_after

field output_schema: Optional[type[BaseModel]] = None
The output schema when agent replies.

NOTE: when this is set, agent can ONLY reply and CANNOT use any tools, such as function tools, RAGs, agent transfer, etc.

Validated by:
__model_validator_after

field planner: Optional[BasePlanner] = None
Instructs the agent to make a plan and execute it step by step.

NOTE: to use model’s built-in thinking features, set the thinking_config field in google.adk.planners.built_in_planner.

Validated by:
__model_validator_after

field tools: list[ToolUnion] [Optional]
Tools available to this agent.

Validated by:
__model_validator_after

canonical_global_instruction(ctx)
The resolved self.instruction field to construct global instruction.

This method is only for use by Agent Development Kit.

Return type:
str

canonical_instruction(ctx)
The resolved self.instruction field to construct instruction for this agent.

This method is only for use by Agent Development Kit.

Return type:
str

property canonical_model: BaseLlm
The resolved self.model field as BaseLlm.

This method is only for use by Agent Development Kit.

property canonical_tools: list[BaseTool]
The resolved self.tools field as a list of BaseTool.

This method is only for use by Agent Development Kit.

pydantic model google.adk.agents.LoopAgent
Bases: BaseAgent

A shell agent that run its sub-agents in a loop.

When sub-agent generates an event with escalate or max_iterations are reached, the loop agent will stop.

Show JSON schema
Fields:
max_iterations (Optional[int])

Validators:
field max_iterations: Optional[int] = None
The maximum number of iterations to run the loop agent.

If not set, the loop agent will run indefinitely until a sub-agent escalates.

pydantic model google.adk.agents.ParallelAgent
Bases: BaseAgent

A shell agent that run its sub-agents in parallel in isolated manner.

This approach is beneficial for scenarios requiring multiple perspectives or attempts on a single task, such as:

Running different algorithms simultaneously.

Generating multiple responses for review by a subsequent evaluation agent.

Show JSON schema
Fields:
Validators:
pydantic model google.adk.agents.SequentialAgent
Bases: BaseAgent

A shell agent that run its sub-agents in sequence.

Show JSON schema
Fields:
Validators:
google.adk.artifacts module
class google.adk.artifacts.BaseArtifactService
Bases: ABC

Abstract base class for artifact services.

abstract delete_artifact(*, app_name, user_id, session_id, filename)
Deletes an artifact.

Return type:
None

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

filename – The name of the artifact file.

abstract list_artifact_keys(*, app_name, user_id, session_id)
Lists all the artifact filenames within a session.

Return type:
list[str]

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

Returns:
A list of all artifact filenames within a session.

abstract list_versions(*, app_name, user_id, session_id, filename)
Lists all versions of an artifact.

Return type:
list[int]

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

filename – The name of the artifact file.

Returns:
A list of all available versions of the artifact.

abstract load_artifact(*, app_name, user_id, session_id, filename, version=None)
Gets an artifact from the artifact service storage.

The artifact is a file identified by the app name, user ID, session ID, and filename.

Return type:
Optional[Part]

Parameters:
app_name – The app name.

user_id – The user ID.

session_id – The session ID.

filename – The filename of the artifact.

version – The version of the artifact. If None, the latest version will be returned.

Returns:
The artifact or None if not found.

abstract save_artifact(*, app_name, user_id, session_id, filename, artifact)
Saves an artifact to the artifact service storage.

The artifact is a file identified by the app name, user ID, session ID, and filename. After saving the artifact, a revision ID is returned to identify the artifact version.

Return type:
int

Parameters:
app_name – The app name.

user_id – The user ID.

session_id – The session ID.

filename – The filename of the artifact.

artifact – The artifact to save.

Returns:
The revision ID. The first version of the artifact has a revision ID of 0. This is incremented by 1 after each successful save.

class google.adk.artifacts.GcsArtifactService(bucket_name, **kwargs)
Bases: BaseArtifactService

An artifact service implementation using Google Cloud Storage (GCS).

Initializes the GcsArtifactService.

Parameters:
bucket_name – The name of the bucket to use.

**kwargs – Keyword arguments to pass to the Google Cloud Storage client.

delete_artifact(*, app_name, user_id, session_id, filename)
Deletes an artifact.

Return type:
None

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

filename – The name of the artifact file.

list_artifact_keys(*, app_name, user_id, session_id)
Lists all the artifact filenames within a session.

Return type:
list[str]

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

Returns:
A list of all artifact filenames within a session.

list_versions(*, app_name, user_id, session_id, filename)
Lists all versions of an artifact.

Return type:
list[int]

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

filename – The name of the artifact file.

Returns:
A list of all available versions of the artifact.

load_artifact(*, app_name, user_id, session_id, filename, version=None)
Gets an artifact from the artifact service storage.

The artifact is a file identified by the app name, user ID, session ID, and filename.

Return type:
Optional[Part]

Parameters:
app_name – The app name.

user_id – The user ID.

session_id – The session ID.

filename – The filename of the artifact.

version – The version of the artifact. If None, the latest version will be returned.

Returns:
The artifact or None if not found.

save_artifact(*, app_name, user_id, session_id, filename, artifact)
Saves an artifact to the artifact service storage.

The artifact is a file identified by the app name, user ID, session ID, and filename. After saving the artifact, a revision ID is returned to identify the artifact version.

Return type:
int

Parameters:
app_name – The app name.

user_id – The user ID.

session_id – The session ID.

filename – The filename of the artifact.

artifact – The artifact to save.

Returns:
The revision ID. The first version of the artifact has a revision ID of 0. This is incremented by 1 after each successful save.

pydantic model google.adk.artifacts.InMemoryArtifactService
Bases: BaseArtifactService, BaseModel

An in-memory implementation of the artifact service.

Show JSON schema
Fields:
artifacts (dict[str, list[google.genai.types.Part]])

field artifacts: dict[str, list[Part]] [Optional]
delete_artifact(*, app_name, user_id, session_id, filename)
Deletes an artifact.

Return type:
None

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

filename – The name of the artifact file.

list_artifact_keys(*, app_name, user_id, session_id)
Lists all the artifact filenames within a session.

Return type:
list[str]

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

Returns:
A list of all artifact filenames within a session.

list_versions(*, app_name, user_id, session_id, filename)
Lists all versions of an artifact.

Return type:
list[int]

Parameters:
app_name – The name of the application.

user_id – The ID of the user.

session_id – The ID of the session.

filename – The name of the artifact file.

Returns:
A list of all available versions of the artifact.

load_artifact(*, app_name, user_id, session_id, filename, version=None)
Gets an artifact from the artifact service storage.

The artifact is a file identified by the app name, user ID, session ID, and filename.

Return type:
Optional[Part]

Parameters:
app_name – The app name.

user_id – The user ID.

session_id – The session ID.

filename – The filename of the artifact.

version – The version of the artifact. If None, the latest version will be returned.

Returns:
The artifact or None if not found.

save_artifact(*, app_name, user_id, session_id, filename, artifact)
Saves an artifact to the artifact service storage.

The artifact is a file identified by the app name, user ID, session ID, and filename. After saving the artifact, a revision ID is returned to identify the artifact version.

Return type:
int

Parameters:
app_name – The app name.

user_id – The user ID.

session_id – The session ID.

filename – The filename of the artifact.

artifact – The artifact to save.

Returns:
The revision ID. The first version of the artifact has a revision ID of 0. This is incremented by 1 after each successful save.

google.adk.code_executors module
pydantic model google.adk.code_executors.BaseCodeExecutor
Bases: BaseModel

Abstract base class for all code executors.

The code executor allows the agent to execute code blocks from model responses and incorporate the execution results into the final response.

optimize_data_file
If true, extract and process data files from the model request and attach them to the code executor. Supported data file MimeTypes are [text/csv]. Default to False.

stateful
Whether the code executor is stateful. Default to False.

error_retry_attempts
The number of attempts to retry on consecutive code execution errors. Default to 2.

code_block_delimiters
The list of the enclosing delimiters to identify the code blocks.

execution_result_delimiters
The delimiters to format the code execution result.

Show JSON schema
Fields:
code_block_delimiters (List[tuple[str, str]])

error_retry_attempts (int)

execution_result_delimiters (tuple[str, str])

optimize_data_file (bool)

stateful (bool)

field code_block_delimiters: List[tuple[str, str]] = [('```tool_code\n', '\n```'), ('```python\n', '\n```')]
The list of the enclosing delimiters to identify the code blocks. For example, the delimiter (’```python

‘, ‘ ```’) can be

used to identify code blocks with the following format:

`python print("hello") `

field error_retry_attempts: int = 2
The number of attempts to retry on consecutive code execution errors. Default to 2.

field execution_result_delimiters: tuple[str, str] = ('```tool_output\n', '\n```')
The delimiters to format the code execution result.

field optimize_data_file: bool = False
If true, extract and process data files from the model request and attach them to the code executor. Supported data file MimeTypes are [text/csv].

Default to False.

field stateful: bool = False
Whether the code executor is stateful. Default to False.

abstract execute_code(invocation_context, code_execution_input)
Executes code and return the code execution result.

Return type:
CodeExecutionResult

Parameters:
invocation_context – The invocation context of the code execution.

code_execution_input – The code execution input.

Returns:
The code execution result.

class google.adk.code_executors.CodeExecutorContext(session_state)
Bases: object

The persistent context used to configure the code executor.

Initializes the code executor context.

Parameters:
session_state – The session state to get the code executor context from.

add_input_files(input_files)
Adds the input files to the code executor context.

Parameters:
input_files – The input files to add to the code executor context.

add_processed_file_names(file_names)
Adds the processed file name to the session state.

Parameters:
file_names – The processed file names to add to the session state.

clear_input_files()
Removes the input files and processed file names to the code executor context.

get_error_count(invocation_id)
Gets the error count from the session state.

Return type:
int

Parameters:
invocation_id – The invocation ID to get the error count for.

Returns:
The error count for the given invocation ID.

get_execution_id()
Gets the session ID for the code executor.

Return type:
Optional[str]

Returns:
The session ID for the code executor context.

get_input_files()
Gets the code executor input file names from the session state.

Return type:
list[File]

Returns:
A list of input files in the code executor context.

get_processed_file_names()
Gets the processed file names from the session state.

Return type:
list[str]

Returns:
A list of processed file names in the code executor context.

get_state_delta()
Gets the state delta to update in the persistent session state.

Return type:
dict[str, Any]

Returns:
The state delta to update in the persistent session state.

increment_error_count(invocation_id)
Increments the error count from the session state.

Parameters:
invocation_id – The invocation ID to increment the error count for.

reset_error_count(invocation_id)
Resets the error count from the session state.

Parameters:
invocation_id – The invocation ID to reset the error count for.

set_execution_id(session_id)
Sets the session ID for the code executor.

Parameters:
session_id – The session ID for the code executor.

update_code_execution_result(invocation_id, code, result_stdout, result_stderr)
Updates the code execution result.

Parameters:
invocation_id – The invocation ID to update the code execution result for.

code – The code to execute.

result_stdout – The standard output of the code execution.

result_stderr – The standard error of the code execution.

pydantic model google.adk.code_executors.ContainerCodeExecutor
Bases: BaseCodeExecutor

A code executor that uses a custom container to execute code.

base_url
Optional. The base url of the user hosted Docker client.

image
The tag of the predefined image or custom image to run on the container. Either docker_path or image must be set.

docker_path
The path to the directory containing the Dockerfile. If set, build the image from the dockerfile path instead of using the predefined image. Either docker_path or image must be set.

Initializes the ContainerCodeExecutor.

Parameters:
base_url – Optional. The base url of the user hosted Docker client.

image – The tag of the predefined image or custom image to run on the container. Either docker_path or image must be set.

docker_path – The path to the directory containing the Dockerfile. If set, build the image from the dockerfile path instead of using the predefined image. Either docker_path or image must be set.

**data – The data to initialize the ContainerCodeExecutor.

Show JSON schema
Fields:
base_url (str | None)

docker_path (str)

image (str)

optimize_data_file (bool)

stateful (bool)

field base_url: Optional[str] = None
Optional. The base url of the user hosted Docker client.

field docker_path: str = None
The path to the directory containing the Dockerfile. If set, build the image from the dockerfile path instead of using the predefined image. Either docker_path or image must be set.

field image: str = None
The tag of the predefined image or custom image to run on the container. Either docker_path or image must be set.

field optimize_data_file: bool = False
If true, extract and process data files from the model request and attach them to the code executor. Supported data file MimeTypes are [text/csv].

Default to False.

field stateful: bool = False
Whether the code executor is stateful. Default to False.

execute_code(invocation_context, code_execution_input)
Executes code and return the code execution result.

Return type:
CodeExecutionResult

Parameters:
invocation_context – The invocation context of the code execution.

code_execution_input – The code execution input.

Returns:
The code execution result.

model_post_init(context, /)
This function is meant to behave like a BaseModel method to initialise private attributes.

It takes context as an argument since that’s what pydantic-core passes when calling it.

Return type:
None

Parameters:
self – The BaseModel instance.

context – The context.

pydantic model google.adk.code_executors.UnsafeLocalCodeExecutor
Bases: BaseCodeExecutor

A code executor that unsafely execute code in the current local context.

Initializes the UnsafeLocalCodeExecutor.

Show JSON schema
Fields:
optimize_data_file (bool)

stateful (bool)

field optimize_data_file: bool = False
If true, extract and process data files from the model request and attach them to the code executor. Supported data file MimeTypes are [text/csv].

Default to False.

field stateful: bool = False
Whether the code executor is stateful. Default to False.

execute_code(invocation_context, code_execution_input)
Executes code and return the code execution result.

Return type:
CodeExecutionResult

Parameters:
invocation_context – The invocation context of the code execution.

code_execution_input – The code execution input.

Returns:
The code execution result.

pydantic model google.adk.code_executors.VertexAiCodeExecutor
Bases: BaseCodeExecutor

A code executor that uses Vertex Code Interpreter Extension to execute code.

resource_name
If set, load the existing resource name of the code interpreter extension instead of creating a new one. Format: projects/123/locations/us-central1/extensions/456

Initializes the VertexAiCodeExecutor.

Parameters:
resource_name – If set, load the existing resource name of the code interpreter extension instead of creating a new one. Format: projects/123/locations/us-central1/extensions/456

**data – Additional keyword arguments to be passed to the base class.

Show JSON schema
Fields:
resource_name (str)

field resource_name: str = None
If set, load the existing resource name of the code interpreter extension instead of creating a new one. Format: projects/123/locations/us-central1/extensions/456

execute_code(invocation_context, code_execution_input)
Executes code and return the code execution result.

Return type:
CodeExecutionResult

Parameters:
invocation_context – The invocation context of the code execution.

code_execution_input – The code execution input.

Returns:
The code execution result.

model_post_init(context, /)
This function is meant to behave like a BaseModel method to initialise private attributes.

It takes context as an argument since that’s what pydantic-core passes when calling it.

Return type:
None

Parameters:
self – The BaseModel instance.

context – The context.

google.adk.evaluation module
class google.adk.evaluation.AgentEvaluator
Bases: object

An evaluator for Agents, mainly intented for helping with test cases.

static evaluate(agent_module, eval_dataset_file_path_or_dir, num_runs=2, agent_name=None, initial_session_file=None)
Evaluates an Agent given eval data.

Parameters:
agent_module – The path to python module that contains the definition of the agent. There is convention in place here, where the code is going to look for ‘root_agent’ in the loaded module.

eval_dataset – The eval data set. This can be either a string representing full path to the file containing eval dataset, or a directory that is recusively explored for all files that have a .test.json suffix.

num_runs – Number of times all entries in the eval dataset should be assessed.

agent_name – The name of the agent.

initial_session_file – File that contains initial session state that is needed by all the evals in the eval dataset.

static find_config_for_test_file(test_file)
Find the test_config.json file in the same folder as the test file.

google.adk.events module
pydantic model google.adk.events.Event
Bases: LlmResponse

Represents an event in a conversation between agents and users.

It is used to store the content of the conversation, as well as the actions taken by the agents like function calls, etc.

invocation_id
The invocation ID of the event.

author
“user” or the name of the agent, indicating who appended the event to the session.

actions
The actions taken by the agent.

long_running_tool_ids
The ids of the long running function calls.

branch
The branch of the event.

id
The unique identifier of the event.

timestamp
The timestamp of the event.

is_final_response
Whether the event is the final response of the agent.

get_function_calls
Returns the function calls in the event.

Show JSON schema
Fields:
actions (google.adk.events.event_actions.EventActions)

author (str)

branch (str | None)

id (str)

invocation_id (str)

long_running_tool_ids (set[str] | None)

timestamp (float)

field actions: EventActions [Optional]
The actions taken by the agent.

field author: str [Required]
‘user’ or the name of the agent, indicating who appended the event to the session.

field branch: Optional[str] = None
The branch of the event.

The format is like agent_1.agent_2.agent_3, where agent_1 is the parent of agent_2, and agent_2 is the parent of agent_3.

Branch is used when multiple sub-agent shouldn’t see their peer agents’ conversaction history.

field id: str = ''
The unique identifier of the event.

field invocation_id: str = ''
The invocation ID of the event.

field long_running_tool_ids: Optional[set[str]] = None
Set of ids of the long running function calls. Agent client will know from this field about which function call is long running. only valid for function call event

field timestamp: float [Optional]
The timestamp of the event.

get_function_calls()
Returns the function calls in the event.

Return type:
list[FunctionCall]

get_function_responses()
Returns the function responses in the event.

Return type:
list[FunctionResponse]

has_trailing_code_exeuction_result()
Returns whether the event has a trailing code execution result.

Return type:
bool

is_final_response()
Returns whether the event is the final response of the agent.

Return type:
bool

model_post_init(_Event__context)
Post initialization logic for the event.

static new_id()
pydantic model google.adk.events.EventActions
Bases: BaseModel

Represents the actions attached to an event.

Show JSON schema
Fields:
artifact_delta (dict[str, int])

escalate (bool | None)

requested_auth_configs (dict[str, google.adk.auth.auth_tool.AuthConfig])

skip_summarization (bool | None)

state_delta (dict[str, object])

transfer_to_agent (str | None)

field artifact_delta: dict[str, int] [Optional]
Indicates that the event is updating an artifact. key is the filename, value is the version.

field escalate: Optional[bool] = None
The agent is escalating to a higher level agent.

field requested_auth_configs: dict[str, AuthConfig] [Optional]
Will only be set by a tool response indicating tool request euc. dict key is the function call id since one function call response (from model) could correspond to multiple function calls. dict value is the required auth config.

field skip_summarization: Optional[bool] = None
If true, it won’t call model to summarize function response.

Only used for function_response event.

field state_delta: dict[str, object] [Optional]
Indicates that the event is updating the state with the given delta.

field transfer_to_agent: Optional[str] = None
If set, the event transfers to the specified agent.

google.adk.examples module
class google.adk.examples.BaseExampleProvider
Bases: ABC

Base class for example providers.

This class defines the interface for providing examples for a given query.

abstract get_examples(query)
Returns a list of examples for a given query.

Return type:
list[Example]

Parameters:
query – The query to get examples for.

Returns:
A list of Example objects.

pydantic model google.adk.examples.Example
Bases: BaseModel

A few-shot example.

input
The input content for the example.

output
The expected output content for the example.

Show JSON schema
Fields:
input (google.genai.types.Content)

output (list[google.genai.types.Content])

field input: Content [Required]
field output: list[Content] [Required]
class google.adk.examples.VertexAiExampleStore(examples_store_name)
Bases: BaseExampleProvider

Provides examples from Vertex example store.

Initializes the VertexAiExampleStore.

Parameters:
examples_store_name – The resource name of the vertex example store, in the format of projects/{project}/locations/{location}/exampleStores/{example_store}.

get_examples(query)
Returns a list of examples for a given query.

Return type:
list[Example]

Parameters:
query – The query to get examples for.

Returns:
A list of Example objects.

google.adk.memory module
class google.adk.memory.BaseMemoryService
Bases: ABC

Base class for memory services.

The service provides functionalities to ingest sessions into memory so that the memory can be used for user queries.

abstract add_session_to_memory(session)
Adds a session to the memory service.

A session may be added multiple times during its lifetime.

Parameters:
session – The session to add.

abstract search_memory(*, app_name, user_id, query)
Searches for sessions that match the query.

Return type:
SearchMemoryResponse

Parameters:
app_name – The name of the application.

user_id – The id of the user.

query – The query to search for.

Returns:
A SearchMemoryResponse containing the matching memories.

class google.adk.memory.InMemoryMemoryService
Bases: BaseMemoryService

An in-memory memory service for prototyping purpose only.

Uses keyword matching instead of semantic search.

add_session_to_memory(session)
Adds a session to the memory service.

A session may be added multiple times during its lifetime.

Parameters:
session – The session to add.

search_memory(*, app_name, user_id, query)
Prototyping purpose only.

Return type:
SearchMemoryResponse

session_events: dict[str, list[Event]]
keys are app_name/user_id/session_id

class google.adk.memory.VertexAiRagMemoryService(rag_corpus=None, similarity_top_k=None, vector_distance_threshold=10)
Bases: BaseMemoryService

A memory service that uses Vertex AI RAG for storage and retrieval.

Initializes a VertexAiRagMemoryService.

Parameters:
rag_corpus – The name of the Vertex AI RAG corpus to use. Format: projects/{project}/locations/{location}/ragCorpora/{rag_corpus_id} or {rag_corpus_id}

similarity_top_k – The number of contexts to retrieve.

vector_distance_threshold – Only returns contexts with vector distance smaller than the threshold..

add_session_to_memory(session)
Adds a session to the memory service.

A session may be added multiple times during its lifetime.

Parameters:
session – The session to add.

search_memory(*, app_name, user_id, query)
Searches for sessions that match the query using rag.retrieval_query.

Return type:
SearchMemoryResponse

google.adk.models module
Defines the interface to support a model.

pydantic model google.adk.models.BaseLlm
Bases: BaseModel

The BaseLLM class.

model
The name of the LLM, e.g. gemini-1.5-flash or gemini-1.5-flash-001.

model_config
The model config

Show JSON schema
Fields:
model (str)

field model: str [Required]
The name of the LLM, e.g. gemini-1.5-flash or gemini-1.5-flash-001.

connect(llm_request)
Creates a live connection to the LLM.

Return type:
BaseLlmConnection

Parameters:
llm_request – LlmRequest, the request to send to the LLM.

Returns:
BaseLlmConnection, the connection to the LLM.

abstract async generate_content_async(llm_request, stream=False)
Generates one content from the given contents and tools.

Return type:
AsyncGenerator[LlmResponse, None]

Parameters:
llm_request – LlmRequest, the request to send to the LLM.

stream – bool = False, whether to do streaming call.

Yields:
a generator of types.Content.

For non-streaming call, it will only yield one Content.

For streaming call, it may yield more than one content, but all yielded contents should be treated as one content by merging the parts list.

classmethod supported_models()
Returns a list of supported models in regex for LlmRegistry.

Return type:
list[str]

pydantic model google.adk.models.Gemini
Bases: BaseLlm

Integration for Gemini models.

model
The name of the Gemini model.

Show JSON schema
Fields:
model (str)

field model: str = 'gemini-1.5-flash'
The name of the LLM, e.g. gemini-1.5-flash or gemini-1.5-flash-001.

connect(llm_request)
Connects to the Gemini model and returns an llm connection.

Return type:
BaseLlmConnection

Parameters:
llm_request – LlmRequest, the request to send to the Gemini model.

Yields:
BaseLlmConnection, the connection to the Gemini model.

async generate_content_async(llm_request, stream=False)
Sends a request to the Gemini model.

Return type:
AsyncGenerator[LlmResponse, None]

Parameters:
llm_request – LlmRequest, the request to send to the Gemini model.

stream – bool = False, whether to do streaming call.

Yields:
LlmResponse – The model response.

static supported_models()
Provides the list of supported models.

Return type:
list[str]

Returns:
A list of supported models.

property api_client: Client
Provides the api client.

Returns:
The api client.

class google.adk.models.LLMRegistry
Bases: object

Registry for LLMs.

static new_llm(model)
Creates a new LLM instance.

Return type:
BaseLlm

Parameters:
model – The model name.

Returns:
The LLM instance.

static register(llm_cls)
Registers a new LLM class.

Parameters:
llm_cls – The class that implements the model.

static resolve(model)
Resolves the model to a BaseLlm subclass.

Return type:
type[BaseLlm]

Parameters:
model – The model name.

Returns:
The BaseLlm subclass.

Raises:
ValueError – If the model is not found.

google.adk.planners module
class google.adk.planners.BasePlanner
Bases: ABC

Abstract base class for all planners.

The planner allows the agent to generate plans for the queries to guide its action.

abstract build_planning_instruction(readonly_context, llm_request)
Builds the system instruction to be appended to the LLM request for planning.

Return type:
Optional[str]

Parameters:
readonly_context – The readonly context of the invocation.

llm_request – The LLM request. Readonly.

Returns:
The planning system instruction, or None if no instruction is needed.

abstract process_planning_response(callback_context, response_parts)
Processes the LLM response for planning.

Return type:
Optional[List[Part]]

Parameters:
callback_context – The callback context of the invocation.

response_parts – The LLM response parts. Readonly.

Returns:
The processed response parts, or None if no processing is needed.

class google.adk.planners.BuiltInPlanner(*, thinking_config)
Bases: BasePlanner

The built-in planner that uses model’s built-in thinking features.

thinking_config
Config for model built-in thinking features. An error will be returned if this field is set for models that don’t support thinking.

Initializes the built-in planner.

Parameters:
thinking_config – Config for model built-in thinking features. An error will be returned if this field is set for models that don’t support thinking.

apply_thinking_config(llm_request)
Applies the thinking config to the LLM request.

Return type:
None

Parameters:
llm_request – The LLM request to apply the thinking config to.

build_planning_instruction(readonly_context, llm_request)
Builds the system instruction to be appended to the LLM request for planning.

Return type:
Optional[str]

Parameters:
readonly_context – The readonly context of the invocation.

llm_request – The LLM request. Readonly.

Returns:
The planning system instruction, or None if no instruction is needed.

process_planning_response(callback_context, response_parts)
Processes the LLM response for planning.

Return type:
Optional[List[Part]]

Parameters:
callback_context – The callback context of the invocation.

response_parts – The LLM response parts. Readonly.

Returns:
The processed response parts, or None if no processing is needed.

thinking_config: ThinkingConfig
Config for model built-in thinking features. An error will be returned if this field is set for models that don’t support thinking.

class google.adk.planners.PlanReActPlanner
Bases: BasePlanner

Plan-Re-Act planner that constraints the LLM response to generate a plan before any action/observation.

Note: this planner does not require the model to support buil-in thinking features or setting the thinking config.

build_planning_instruction(readonly_context, llm_request)
Builds the system instruction to be appended to the LLM request for planning.

Return type:
str

Parameters:
readonly_context – The readonly context of the invocation.

llm_request – The LLM request. Readonly.

Returns:
The planning system instruction, or None if no instruction is needed.

process_planning_response(callback_context, response_parts)
Processes the LLM response for planning.

Return type:
Optional[List[Part]]

Parameters:
callback_context – The callback context of the invocation.

response_parts – The LLM response parts. Readonly.

Returns:
The processed response parts, or None if no processing is needed.

google.adk.runners module
class google.adk.runners.InMemoryRunner(agent, *, app_name='InMemoryRunner')
Bases: Runner

An in-memory Runner for testing and development.

This runner uses in-memory implementations for artifact, session, and memory services, providing a lightweight and self-contained environment for agent execution.

agent
The root agent to run.

app_name
The application name of the runner. Defaults to ‘InMemoryRunner’.

Initializes the InMemoryRunner.

Parameters:
agent – The root agent to run.

app_name – The application name of the runner. Defaults to ‘InMemoryRunner’.

class google.adk.runners.Runner(*, app_name, agent, artifact_service=None, session_service, memory_service=None)
Bases: object

The Runner class is used to run agents.

It manages the execution of an agent within a session, handling message processing, event generation, and interaction with various services like artifact storage, session management, and memory.

app_name
The application name of the runner.

agent
The root agent to run.

artifact_service
The artifact service for the runner.

session_service
The session service for the runner.

memory_service
The memory service for the runner.

Initializes the Runner.

Parameters:
app_name – The application name of the runner.

agent – The root agent to run.

artifact_service – The artifact service for the runner.

session_service – The session service for the runner.

memory_service – The memory service for the runner.

agent: BaseAgent
The root agent to run.

app_name: str
The app name of the runner.

artifact_service: Optional[BaseArtifactService] = None
The artifact service for the runner.

close_session(session)
Closes a session and adds it to the memory service (experimental feature).

Parameters:
session – The session to close.

memory_service: Optional[BaseMemoryService] = None
The memory service for the runner.

run(*, user_id, session_id, new_message, run_config=RunConfig(speech_config=None, response_modalities=None, save_input_blobs_as_artifacts=False, support_cfc=False, streaming_mode=<StreamingMode.NONE: None>, output_audio_transcription=None, max_llm_calls=500))
Runs the agent.

NOTE: This sync interface is only for local testing and convenience purpose. Consider to use run_async for production usage.

Return type:
Generator[Event, None, None]

Parameters:
user_id – The user ID of the session.

session_id – The session ID of the session.

new_message – A new message to append to the session.

run_config – The run config for the agent.

Yields:
The events generated by the agent.

async run_async(*, user_id, session_id, new_message, run_config=RunConfig(speech_config=None, response_modalities=None, save_input_blobs_as_artifacts=False, support_cfc=False, streaming_mode=<StreamingMode.NONE: None>, output_audio_transcription=None, max_llm_calls=500))
Main entry method to run the agent in this runner.

Return type:
AsyncGenerator[Event, None]

Parameters:
user_id – The user ID of the session.

session_id – The session ID of the session.

new_message – A new message to append to the session.

run_config – The run config for the agent.

Yields:
The events generated by the agent.

async run_live(*, session, live_request_queue, run_config=RunConfig(speech_config=None, response_modalities=None, save_input_blobs_as_artifacts=False, support_cfc=False, streaming_mode=<StreamingMode.NONE: None>, output_audio_transcription=None, max_llm_calls=500))
Runs the agent in live mode (experimental feature).

Return type:
AsyncGenerator[Event, None]

Parameters:
session – The session to use.

live_request_queue – The queue for live requests.

run_config – The run config for the agent.

Yields:
The events generated by the agent.

session_service: BaseSessionService
The session service for the runner.

google.adk.sessions module
class google.adk.sessions.BaseSessionService
Bases: ABC

Base class for session services.

The service provides a set of methods for managing sessions and events.

append_event(session, event)
Appends an event to a session object.

Return type:
Event

close_session(*, session)
Closes a session.

abstract create_session(*, app_name, user_id, state=None, session_id=None)
Creates a new session.

Return type:
Session

Parameters:
app_name – the name of the app.

user_id – the id of the user.

state – the initial state of the session.

session_id – the client-provided id of the session. If not provided, a generated ID will be used.

Returns:
The newly created session instance.

Return type:
session

abstract delete_session(*, app_name, user_id, session_id)
Deletes a session.

Return type:
None

abstract get_session(*, app_name, user_id, session_id, config=None)
Gets a session.

Return type:
Optional[Session]

abstract list_events(*, app_name, user_id, session_id)
Lists events in a session.

Return type:
ListEventsResponse

abstract list_sessions(*, app_name, user_id)
Lists all the sessions.

Return type:
ListSessionsResponse

class google.adk.sessions.DatabaseSessionService(db_url)
Bases: BaseSessionService

A session service that uses a database for storage.

Parameters:
db_url – The database URL to connect to.

append_event(session, event)
Appends an event to a session object.

Return type:
Event

create_session(*, app_name, user_id, state=None, session_id=None)
Creates a new session.

Return type:
Session

Parameters:
app_name – the name of the app.

user_id – the id of the user.

state – the initial state of the session.

session_id – the client-provided id of the session. If not provided, a generated ID will be used.

Returns:
The newly created session instance.

Return type:
session

delete_session(app_name, user_id, session_id)
Deletes a session.

Return type:
None

get_session(*, app_name, user_id, session_id, config=None)
Gets a session.

Return type:
Optional[Session]

list_events(*, app_name, user_id, session_id)
Lists events in a session.

Return type:
ListEventsResponse

list_sessions(*, app_name, user_id)
Lists all the sessions.

Return type:
ListSessionsResponse

class google.adk.sessions.InMemorySessionService
Bases: BaseSessionService

An in-memory implementation of the session service.

append_event(session, event)
Appends an event to a session object.

Return type:
Event

create_session(*, app_name, user_id, state=None, session_id=None)
Creates a new session.

Return type:
Session

Parameters:
app_name – the name of the app.

user_id – the id of the user.

state – the initial state of the session.

session_id – the client-provided id of the session. If not provided, a generated ID will be used.

Returns:
The newly created session instance.

Return type:
session

delete_session(*, app_name, user_id, session_id)
Deletes a session.

Return type:
None

get_session(*, app_name, user_id, session_id, config=None)
Gets a session.

Return type:
Session

list_events(*, app_name, user_id, session_id)
Lists events in a session.

Return type:
ListEventsResponse

list_sessions(*, app_name, user_id)
Lists all the sessions.

Return type:
ListSessionsResponse

pydantic model google.adk.sessions.Session
Bases: BaseModel

Represents a series of interactions between a user and agents.

id
The unique identifier of the session.

app_name
The name of the app.

user_id
The id of the user.

state
The state of the session.

events
The events of the session, e.g. user input, model response, function call/response, etc.

last_update_time
The last update time of the session.

Show JSON schema
Fields:
app_name (str)

events (list[google.adk.events.event.Event])

id (str)

last_update_time (float)

state (dict[str, Any])

user_id (str)

field app_name: str [Required]
The name of the app.

field events: list[Event] [Optional]
The events of the session, e.g. user input, model response, function call/response, etc.

field id: str [Required]
The unique identifier of the session.

field last_update_time: float = 0.0
The last update time of the session.

field state: dict[str, Any] [Optional]
The state of the session.

field user_id: str [Required]
The id of the user.

class google.adk.sessions.State(value, delta)
Bases: object

A state dict that maintain the current value and the pending-commit delta.

Parameters:
value – The current value of the state dict.

delta – The delta change to the current value that hasn’t been commited.

APP_PREFIX = 'app:'
TEMP_PREFIX = 'temp:'
USER_PREFIX = 'user:'
get(key, default=None)
Returns the value of the state dict for the given key.

Return type:
Any

has_delta()
Whether the state has pending detla.

Return type:
bool

to_dict()
Returns the state dict.

Return type:
dict[str, Any]

update(delta)
Updates the state dict with the given delta.

class google.adk.sessions.VertexAiSessionService(project=None, location=None)
Bases: BaseSessionService

Connects to the managed Vertex AI Session Service.

append_event(session, event)
Appends an event to a session object.

Return type:
Event

create_session(*, app_name, user_id, state=None, session_id=None)
Creates a new session.

Return type:
Session

Parameters:
app_name – the name of the app.

user_id – the id of the user.

state – the initial state of the session.

session_id – the client-provided id of the session. If not provided, a generated ID will be used.

Returns:
The newly created session instance.

Return type:
session

delete_session(*, app_name, user_id, session_id)
Deletes a session.

Return type:
None

get_session(*, app_name, user_id, session_id, config=None)
Gets a session.

Return type:
Session

list_events(*, app_name, user_id, session_id)
Lists events in a session.

Return type:
ListEventsResponse

list_sessions(*, app_name, user_id)
Lists all the sessions.

Return type:
ListSessionsResponse

google.adk.tools module
class google.adk.tools.APIHubToolset(*, apihub_resource_name, access_token=None, service_account_json=None, name='', description='', lazy_load_spec=False, auth_scheme=None, auth_credential=None, apihub_client=None)
Bases: object

APIHubTool generates tools from a given API Hub resource.

Examples:

``` apihub_toolset = APIHubToolset(

apihub_resource_name=”projects/test-project/locations/us-central1/apis/test-api”, service_account_json=”…”,

)

# Get all available tools agent = LlmAgent(tools=apihub_toolset.get_tools())

# Get a specific tool agent = LlmAgent(tools=[

… apihub_toolset.get_tool(‘my_tool’),

])
apihub_resource_name is the resource name from API Hub. It must include
API name, and can optionally include API version and spec name. - If apihub_resource_name includes a spec resource name, the content of that

spec will be used for generating the tools.

If apihub_resource_name includes only an api or a version name, the first spec of the first version of that API will be used.

Initializes the APIHubTool with the given parameters.

Examples: ``` apihub_toolset = APIHubToolset(

apihub_resource_name=”projects/test-project/locations/us-central1/apis/test-api”, service_account_json=”…”,

)

# Get all available tools agent = LlmAgent(tools=apihub_toolset.get_tools())

# Get a specific tool agent = LlmAgent(tools=[

… apihub_toolset.get_tool(‘my_tool’),

])
apihub_resource_name is the resource name from API Hub. It must include API name, and can optionally include API version and spec name. - If apihub_resource_name includes a spec resource name, the content of that

spec will be used for generating the tools.

If apihub_resource_name includes only an api or a version name, the first spec of the first version of that API will be used.

Example: * projects/xxx/locations/us-central1/apis/apiname/… * https://console.cloud.google.com/apigee/api-hub/apis/apiname?project=xxx

param apihub_resource_name:
The resource name of the API in API Hub. Example: projects/test-project/locations/us-central1/apis/test-api.

param access_token:
Google Access token. Generate with gcloud cli gcloud auth auth print-access-token. Used for fetching API Specs from API Hub.

param service_account_json:
The service account config as a json string. Required if not using default service credential. It is used for creating the API Hub client and fetching the API Specs from API Hub.

param apihub_client:
Optional custom API Hub client.

param name:
Name of the toolset. Optional.

param description:
Description of the toolset. Optional.

param auth_scheme:
Auth scheme that applies to all the tool in the toolset.

param auth_credential:
Auth credential that applies to all the tool in the toolset.

param lazy_load_spec:
If True, the spec will be loaded lazily when needed. Otherwise, the spec will be loaded immediately and the tools will be generated during initialization.

get_tool(name)
Retrieves a specific tool by its name.

Return type:
Optional[RestApiTool]

Example: ` apihub_tool = apihub_toolset.get_tool('my_tool') `

Parameters:
name – The name of the tool to retrieve.

Returns:
The tool with the given name, or None if no such tool exists.

get_tools()
Retrieves all available tools.

Return type:
List[RestApiTool]

Returns:
A list of all available RestApiTool objects.

pydantic model google.adk.tools.AuthToolArguments
Bases: BaseModel

the arguments for the special long running function tool that is used to

request end user credentials.

Show JSON schema
Fields:
auth_config (google.adk.auth.auth_tool.AuthConfig)

function_call_id (str)

field auth_config: AuthConfig [Required]
field function_call_id: str [Required]
class google.adk.tools.BaseTool(*, name, description, is_long_running=False)
Bases: ABC

The base class for all tools.

description: str
The description of the tool.

is_long_running: bool = False
Whether the tool is a long running operation, which typically returns a resource id first and finishes the operation later.

name: str
The name of the tool.

async process_llm_request(*, tool_context, llm_request)
Processes the outgoing LLM request for this tool.

Use cases: - Most common use case is adding this tool to the LLM request. - Some tools may just preprocess the LLM request before it’s sent out.

Return type:
None

Parameters:
tool_context – The context of the tool.

llm_request – The outgoing LLM request, mutable this method.

async run_async(*, args, tool_context)
Runs the tool with the given arguments and context.

NOTE :rtype: Any

Required if this tool needs to run at the client side.

Otherwise, can be skipped, e.g. for a built-in GoogleSearch tool for Gemini.

Parameters:
args – The LLM-filled arguments.

ctx – The context of the tool.

Returns:
The result of running the tool.

class google.adk.tools.ExampleTool(examples)
Bases: BaseTool

A tool that adds (few-shot) examples to the LLM request.

examples
The examples to add to the LLM request.

async process_llm_request(*, tool_context, llm_request)
Processes the outgoing LLM request for this tool.

Use cases: - Most common use case is adding this tool to the LLM request. - Some tools may just preprocess the LLM request before it’s sent out.

Return type:
None

Parameters:
tool_context – The context of the tool.

llm_request – The outgoing LLM request, mutable this method.

class google.adk.tools.FunctionTool(func)
Bases: BaseTool

A tool that wraps a user-defined Python function.

func
The function to wrap.

async run_async(*, args, tool_context)
Runs the tool with the given arguments and context.

NOTE :rtype: Any

Required if this tool needs to run at the client side.

Otherwise, can be skipped, e.g. for a built-in GoogleSearch tool for Gemini.

Parameters:
args – The LLM-filled arguments.

ctx – The context of the tool.

Returns:
The result of running the tool.

class google.adk.tools.LongRunningFunctionTool(func)
Bases: FunctionTool

A function tool that returns the result asynchronously.

This tool is used for long-running operations that may take a significant amount of time to complete. The framework will call the function. Once the function returns, the response will be returned asynchronously to the framework which is identified by the function_call_id.

Example: `python tool = LongRunningFunctionTool(a_long_running_function) `

is_long_running
Whether the tool is a long running operation.

class google.adk.tools.ToolContext(invocation_context, *, function_call_id=None, event_actions=None)
Bases: CallbackContext

The context of the tool.

This class provides the context for a tool invocation, including access to the invocation context, function call ID, event actions, and authentication response. It also provides methods for requesting credentials, retrieving authentication responses, listing artifacts, and searching memory.

invocation_context
The invocation context of the tool.

function_call_id
The function call id of the current tool call. This id was returned in the function call event from LLM to identify a function call. If LLM didn’t return this id, ADK will assign one to it. This id is used to map function call response to the original function call.

event_actions
The event actions of the current tool call.

property actions: EventActions
get_auth_response(auth_config)
Return type:
AuthCredential

list_artifacts()
Lists the filenames of the artifacts attached to the current session.

Return type:
list[str]

request_credential(auth_config)
Return type:
None

search_memory(query)
Searches the memory of the current user.

Return type:
SearchMemoryResponse

class google.adk.tools.VertexAiSearchTool(*, data_store_id=None, search_engine_id=None)
Bases: BaseTool

A built-in tool using Vertex AI Search.

data_store_id
The Vertex AI search data store resource ID.

search_engine_id
The Vertex AI search engine resource ID.

Initializes the Vertex AI Search tool.

Parameters:
data_store_id – The Vertex AI search data store resource ID in the format of “projects/{project}/locations/{location}/collections/{collection}/dataStores/{dataStore}”.

search_engine_id – The Vertex AI search engine resource ID in the format of “projects/{project}/locations/{location}/collections/{collection}/engines/{engine}”.

Raises:
ValueError – If both data_store_id and search_engine_id are not specified

or both are specified. –

async process_llm_request(*, tool_context, llm_request)
Processes the outgoing LLM request for this tool.

Use cases: - Most common use case is adding this tool to the LLM request. - Some tools may just preprocess the LLM request before it’s sent out.

Return type:
None

Parameters:
tool_context – The context of the tool.

llm_request – The outgoing LLM request, mutable this method.

google.adk.tools.exit_loop(tool_context)
Exits the loop.

Call this function only when you are instructed to do so.

google.adk.tools.transfer_to_agent(agent_name, tool_context)
Transfer the question to another agent.