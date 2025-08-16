
# Building Effective Agents

Over the past year, we have collaborated with dozens of teams across industries to build large language model (LLM) agents. Consistently, the most successful implementations did not rely on complex frameworks or specialized libraries. Instead, they used simple, composable patterns.

In this article, we share lessons learned from working with clients and building agents ourselves, offering practical advice for developers building effective agents.

**What is an Agent?**  
"Agent" can have multiple definitions. Some clients define agents as fully autonomous systems capable of operating independently for extended periods, using various tools to complete complex tasks. Others use the term to describe more prescriptive implementations that follow predefined workflows. At Anthropic, we categorize all these variants as agent systems but draw an important architectural distinction between workflows and agents:

- **Workflows** are systems that orchestrate LLMs and tools through predefined code paths.
- **Agents** are systems where LLMs dynamically guide their own processes and tool usage, maintaining control over how tasks are completed.

Below, we explore both types of agent systems in detail. In Appendix 1 ("Agents in Practice"), we describe two areas where clients have found these systems particularly valuable.

**When (and When Not) to Use Agents**  
When building applications with LLMs, we recommend finding the simplest solution and only adding complexity when necessary. This may mean not building an agent system at all. Agent systems typically trade latency and cost for better task performance, and you should consider when this tradeoff is justified.

When more complexity is needed, workflows provide predictability and consistency for well-defined tasks, while agents are better choices when flexibility and model-driven decision-making are required. However, for many applications, optimizing single LLM calls through retrieval and contextual examples is often sufficient.

**When and How to Use Frameworks**  
Many frameworks can make agent systems easier to implement, including:

- LangChain's LangGraph;
- Amazon Bedrock's AI Agent Framework;
- Rivet, a drag-and-drop GUI LLM workflow builder; and
- Vellum, another GUI tool for building and testing complex workflows.

These frameworks make getting started easier by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls. However, they often create additional abstraction layers that can obscure underlying prompts and responses, making debugging harder. They may also tempt you to add complexity when a simpler setup would suffice.

We recommend developers start by using LLM APIs directly: many patterns can be implemented in just a few lines of code. If you do use a framework, make sure you understand the underlying code. Incorrect assumptions about underlying components are a common source of client errors.

See our recipes for some example implementations.

**Building Blocks, Workflows, and Agents**  
In this section, we explore common patterns for agent systems we've seen in production. We'll start with our foundational building block—the augmented LLM—and gradually increase complexity from simple compositional workflows to autonomous agents.

**Building Block: Augmented LLM**  
The fundamental building block of agent systems is an LLM enhanced with capabilities like retrieval, tools, and memory. Our current models can actively use these enhancements—generating their own search queries, selecting appropriate tools, and determining what information to retain.

We recommend focusing on two key aspects of implementation: customizing these enhancements for your specific use case and ensuring they provide easy-to-use, well-documented interfaces for your LLM. While there are many ways to implement these enhancements, one approach is through our recently released Model Context Protocol, which allows developers to integrate with a growing ecosystem of third-party tools through simple client implementations.

For the remainder of this article, we'll assume each LLM call has access to these enhancements.

**Workflow: Prompt Chaining**  
Prompt chaining breaks tasks into a series of steps where each LLM call processes the output of the previous call. You can add programmatic checks at any intermediate step (the "gates" shown in the diagram below) to ensure the process remains on track.

**When to use this workflow**: This workflow is ideal for tasks that can be easily and cleanly decomposed into fixed subtasks. The primary goal is to trade latency for higher accuracy by making each LLM call a simpler task.

**Examples where prompt chaining is useful**:

- Generating marketing copy and then translating it into different languages.
- Writing a document outline, checking if the outline meets certain criteria, and then writing the document based on the outline.

**Workflow: Routing**  
Routing classifies inputs and directs them to specialized subsequent tasks. This workflow enables separation of concerns and building more specialized prompts. Without this workflow, optimizing for one type of input might degrade performance for others.

**When to use this workflow**: Routing is appropriate for complex tasks where there are distinct categories that are better handled separately, and classification can be accurately handled by an LLM or more traditional classification models/algorithms.

**Examples where routing is useful**:

- Directing different types of customer service queries (general questions, refund requests, technical support) to different downstream processes, prompts, and tools.
- Routing simple/common questions to smaller models (like Claude 3.5 Haiku) and difficult/rare questions to more powerful models (like Claude 3.5 Sonnet) to optimize cost and speed.

**Workflow: Parallelization**  
LLMs can sometimes process tasks simultaneously and programmatically aggregate their outputs. This workflow, parallelization, manifests in two key variants:

- **Segmentation**: Breaking a task into independent subtasks that run in parallel.
- **Voting**: Running the same task multiple times to get diverse outputs.

**When to use this workflow**: Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher-confidence results. For complex tasks with multiple considerations, LLMs often perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect.

**Examples where parallelization is useful**:

- **Segmentation**:
  - Implementing guardrails where one model instance processes user queries while another filters them for inappropriate content or requests. This often performs better than having the same LLM call handle both guardrails and core responses.
  - Automating evaluation of LLM performance where each LLM call assesses the model's performance on different aspects of a given prompt.
- **Voting**:
  - Reviewing code for vulnerabilities where several different prompts review and flag code if issues are found.
  - Evaluating whether given content is inappropriate, with multiple prompts assessing different aspects or requiring different voting thresholds to balance false positives and negatives.

**Workflow: Orchestrator-Worker**  
In the orchestrator-worker workflow, a central LLM dynamically decomposes tasks, delegates them to worker LLMs, and synthesizes their results.

**When to use this workflow**: This workflow is ideal for complex tasks where you cannot predict the required subtasks (e.g., in coding, the number of files needing changes and the nature of changes in each file may depend on the task). While topologically similar to parallelization, the key difference is its flexibility—the subtasks are not predefined but determined by the orchestrator based on specific inputs.

**Examples where orchestrator-worker is useful**:

- Coding products that make complex changes across multiple files with each iteration.
- Search tasks involving gathering and analyzing information from multiple sources to obtain potentially relevant information.

**Workflow: Evaluator-Optimizer**  
In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop.

**When to use this workflow**: This workflow is particularly effective when we have clear evaluation criteria and iterative improvement provides measurable value. Two good indicators are, first, when human expression of feedback can noticeably improve LLM responses; and second, when LLMs can provide such feedback. This resembles the iterative writing process a human writer might go through when generating refined documents.

**Examples where evaluator-optimizer is useful**:

- Literary translation where nuances initially missed by the translation LLM can be addressed with useful criticism from an evaluator LLM.
- Complex search tasks requiring multiple rounds of searching and analysis to gather comprehensive information, where the evaluator determines if further searching is needed.

**Agents**  
As LLMs mature in key capabilities—understanding complex inputs, engaging in reasoning and planning, reliably using tools, and recovering from errors—agents are emerging in production. Agents begin working either from a command from a human user or through an interactive discussion with a human user. Once the task is clear, the agent independently plans and operates, potentially returning to humans for more information or judgment. Crucially, during execution, the agent gathers "ground truth" from the environment at each step (such as tool call results or code execution) to assess its progress. Agents can pause at checkpoints or when encountering obstacles to get human feedback. Tasks typically terminate upon completion, but often include stop conditions (like maximum iteration counts) to maintain control.

Agents can handle complex tasks, but their implementations are often simple. They're typically just LLMs using tools in an environment feedback loop. Therefore, designing the toolset and its documentation clearly and thoughtfully is critical. We expand on best practices for tool development in Appendix 2 ("Prompt Engineering Your Tools").

**When to use agents**: Agents can be used for open-ended problems where the number of required steps is difficult or impossible to predict, and you cannot hardcode fixed paths. The LLM may run multiple times, and you must have a certain level of trust in its decisions. An agent's autonomy makes it ideal for scaling tasks in trusted environments.

An agent's autonomy means higher costs and potential error accumulation. We recommend extensive testing in sandboxed environments and setting appropriate guardrails.

**Examples where agents are useful**:

The following examples come from our own implementations:

- A coding agent for solving SWE-bench tasks, which involve editing multiple files based on task descriptions;
- Our "Computer Use" reference implementation where Claude uses a computer to complete tasks.

**Advanced Flow for Coding Agents**  
**Combining and Customizing These Patterns**  
These building blocks aren't prescriptive. They're common patterns developers can shape and combine to fit different use cases. As with any LLM capability, the key to success is measuring performance and iterating on implementations. Again: you should only consider adding complexity when it clearly improves results.

**Summary**  
Success in the LLM space isn't about building the most complex system. It's about building the system that fits your needs. Start with simple prompts, optimize them through comprehensive evaluation, and only add multi-step agent systems when simpler solutions fall short.

When implementing agents, we try to follow three core principles:

1. Keep agent designs simple.
2. Prioritize transparency by clearly showing the agent's planning steps.
3. Carefully design the Agent-Computer Interface (ACI) through thorough documentation and testing.

Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components when moving to production. By following these principles, you can create agents that are not only powerful but also reliable, maintainable, and trusted by users.

**Acknowledgments**  
Written by Erik Schluntz and Barry Zhang. This work draws on our experience building agents at Anthropic and valuable insights shared by clients, for which we're deeply grateful.

**Appendix 1: Agents in Practice**  
Our work with clients has revealed two particularly promising applications of AI agents, demonstrating the practical value of the patterns above. Both applications illustrate where agents add the most value: in tasks that require conversation and action, have clear success criteria, enable feedback loops, and incorporate meaningful human oversight.

**A. Customer Support**  
Customer support combines the familiar chatbot interface with functionality enhanced through tool integration. This is a natural fit for more open-ended agents because:

- Support interactions naturally follow conversational flows while requiring access to external information and actions;
- Tools can be integrated to extract customer data, order history, and knowledge base articles;
- Actions like issuing refunds or updating tickets can be handled programmatically; and
- Success can be measured explicitly through user-defined solutions.

Several companies have demonstrated the viability of this approach through usage-based pricing models that charge only for successful resolutions, showing confidence in their agents' effectiveness.

**B. Coding Agents**  
The software development domain showcases significant potential for LLM capabilities, evolving from code completion to autonomous problem-solving. Agents are particularly effective because:

- Code solutions can be verified through automated testing;
- Agents can iterate on solutions using test results as feedback;
- The problem space is well-defined and structured; and
- Output quality can be objectively measured.

In our own implementations, agents can now solve real GitHub issues from the SWE-bench Verified benchmark individually based on pull request descriptions. However, while automated testing helps verify functionality, human review remains crucial to ensure solutions meet broader system requirements.

**Appendix 2: Prompt Engineering Your Tools**  
Regardless of which agent system you build, tools are likely to be a critical component of your agent. Tools enable Claude to interact with external services and APIs by specifying their exact structure in our API. When Claude responds, if it plans to call a tool, it will include a tool use block in the API response. Tool definitions and specifications should receive as much prompt engineering attention as your overall prompt. In this brief appendix, we describe how to prompt engineer your tools.

There are often multiple ways to specify the same action. For example, you could specify a file edit by writing a diff or rewriting the entire file. For structured output, you could return code in markdown or JSON. In software engineering, these differences are superficial and can be losslessly converted from one to another. However, certain formats are harder for LLMs to write than others. Writing diffs requires knowing how many lines are changing in the block header before writing new code. Writing code in JSON (compared to markdown) requires additional escaping of newlines and quotes.

Our recommendations for deciding tool formats are:

- Give the model enough tokens to "think" so it doesn't paint itself into a corner.
- Keep formats close to what the model naturally sees in internet text.
- Ensure there's no format "overhead," such as having to accurately count thousands of lines of code or string-escape any code it writes.

A rule of thumb is to consider how much effort you'd put into human-computer interfaces (HCI) and plan to put the same amount of effort into creating good Agent-Computer Interfaces (ACI). Here are some ideas for how to do this:

- Think from the model's perspective. Is using this tool obvious given the description and parameters, or do you need to think carefully about it? If the latter, it's probably the same for the model. A good tool definition typically includes example usage, edge cases, input format requirements, and clear boundaries with other tools.
- How could you change parameter names or descriptions to make things more obvious? Treat it as writing an excellent docstring for a junior developer on your team. This is especially important when using many similar tools.
- Test how the model uses your tools: run many example inputs in our playground to see what mistakes the model makes and iterate.
- Make your tools foolproof. Change parameters to make it harder to make mistakes.

When building our SWE-bench agent, we actually spent more time optimizing our tools than the overall prompt. For example, we found that the model made mistakes with tools using relative file paths after the agent moved out of the root directory. To solve this, we changed the tool to always require absolute file paths—we found the model used this approach flawlessly.
