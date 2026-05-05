# MemAgent Reshaping Long-Context LLM with Multi-Conv RL-based Memory Agent

5202
luJ
3
]LC.sc[
1v95220.7052:viXra
MemAgent: Reshaping Long-Context LLM with
Multi-Conv RL-based Memory Agent
HongliYu1,2,3, TinghongChen2, JiangtaoFeng2, JiangjieChen1,3, WeinanDai1,2,3,
QiyingYu1,2,3, Ya-QinZhang2,3, Wei-YingMa2,3, JingjingLiu2,3, MingxuanWang1,3, HaoZhou2,3
1ByteDanceSeed 2InstituteforAIIndustryResearch(AIR),TsinghuaUniversity
3SIA-LabofTsinghuaAIRandByteDanceSeed
Abstract
Despite improvements by length extrapolation, efficient attention and memory modules, handling
infinitely long documents with linear complexity without performance degradation during extrapo-
lation remains the ultimate challenge in long-text processing. We directly optimize for long-text
tasksinanend-to-endfashionandintroduceanovelagentworkflow,MemAgent,whichreadstext
in segments and updates the memory using an overwrite strategy. We extend the DAPO algorithm
to facilitate training via independent-context multi-conversation generation. MemAgent has
demonstrated superb long-context capabilities, being able to extrapolate from an 8K context
trained on 32K text to a 3.5M QA task with performance loss < 5% and achieves 95%+ in 512K
RULER test.
Date: July 4, 2025
Correspondence: zhouhao@air.tsinghua.edu.cn, wangmingxuan.89@bytedance.com
ProjectPage: https://memagent-sialab.github.io/
80
60
40
20
0
7K 112K 224K 448K 896K 1.75M 3.5M
Context Length in Tokens
erocS
RL-MemAgent-14B
RL-MemAgent-7B
QwenLong-L1-32B
Qwen2.5-Instruct-14B-1M
Qwen2.5-Instruct-7B-1M
DS-Distill-Qwen-32B
DS-Distill-Qwen-14B
DS-Distill-Qwen-7B
Truncation
Figure1 Accuracy scores of RULER-HotpotQA [1, 2] . Even models that employ long-context continual pretraining
and extrapolation techniques fail to maintain consistent performance. In contrast, MemAgent with RL demonstrates
nearly lossless performance extrapolation.
1
1 Introduction
While having demonstrated impressive capabilities [3–7], industry-level Large Language Model (LLM) sys-
tems [8–10] still face a critical challenge: how to handle long contexts effectively - processing an entire book,
executing a complex chain of reasoning over many steps, or managing the long-term memory of an agent
system - all these complex tasks can generate overflowing text that quickly explodes the typical-size context
window of current LLMs.
Existing approaches to long-context tasks are three-pronged. The first involves length extrapolation methods
by shifting the positional embeddings in order to extend the context window of the model [11–15], plus
continued pre-training [16–18]. Despite promising potential, these methods often suffer from performance
degradationandslowprocessingspeedduetoO(n2)computationalcomplexitywhenappliedtoextremelylong
text. Thesecondschoolofmethodsleveragessparseattention[19–21]andlinearattentionmechanisms[22,23]
to reduce the complexity of attention for more efficient processing of longer sequences. However, this typically
requires training from scratch, with inherent adversities such as linear attention facing difficulties in parallel
trainingorsparseattentiondependingonhuman-definedpatterns. Thelastlineofinquiryinvestigatescontext
compression [24–27], which aims to condense information in token-level or external-memory-plugin modules.
Such approaches often struggle with extrapolation, and require the integration of additional modules or
context operations, which ineluctably disrupts the standard generation process and hinders compatibility as
well as parallelization.
Hence, a successful LLM with strong long-context capabilities requires the trinity of: 1) processing infinite
length of text; 2) scaling without performance drop; and 3) efficient decoding with linear complexity. To
pursue this quest, we return to the basic intuition behind long-context modeling [28–31]. When humans
process long-context information, we tend to abstract out the main revealing conceptions to capture the
essence of the whole text, often by making notes of critical details or using short-handed stenograph to record
the key points, while discarding redundant and irrelevant data. We do not attempt to memorize every single
fact or each small piece of information; instead, we focus our intellectual energy on more important aspects of
the task at hand. This selective attention not only simplifies the process but also aids in tackling complex
problems more efficiently.
Following this anthropocentric intuition, we propose a novel use of Reinforcement Learning (RL) to equip
LLMs with a dynamically updated fixed-length ‘memory’, as illustrated in Figure 2. During inference, the
LLM processes the input text segment-by-segment. As it reads each segment, the model proactively and
selectively updates the memory, which then contributes to the generation of the final output after all relevant
messages are aggregated and synergized in the memory. This clever mechanism allows the LLM to flexibly
handle arbitrary text lengths while maintaining a linear time complexity during processing, since the length
of the memory is fixed, which leads to a fixed context window size for the model. This segment-based
approach generates multiple outputs from a single long-text input, requiring multiple rounds of memory
updates and a final round for the generation of the final response. Training this type of agent workflow, which
enables dialogues across multiple independent contexts, is still an unexplored territory in current LLM study.
Existing systems typically handle workflow trajectories via alternating tool calls or environment feedback by
either simply concatenating [32, 33] them or using a sliding window [34] approach, which lacks flexibility and
scalability in practice. Our MemAgent approach, instead, proposes that treats each context-independent
conversation as an optimization objective. Based on the DAPO[35] algorithm, we implement the Multi-Conv
DAPO to optimize an arbitrary agent workflow by verifiable outcome reward.
In our experiments, an RL-trained model with a modest 8K context window (with a 1024-token memory
and a 5000-token document chunk) trained on 32K documents exhibits consistently superb capabilities for
Question Answering (QA) tasks on documents of up to 4 million tokens, without performance drop and with
linear computation cost. This demonstratively showcases the efficiency and scalability of our long-context
memory approach.
Our major contributions are threefold:
• We introduce a novel approach that enables LLMs to process arbitrarily long inputs within limited
context window under linear time complexity during inference, overcoming a significant bottleneck in
2
Solving Long-Context Task with Long-Context LLM A
Long-Context LLM
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 … N-2 N-1 N Q Text Chunk
Q Question
3 Memory
1 2 3 A
A Answer
…
LLM LLM LLM LLM
1 Q 1 2 Q 2 3 Q K N Q
Solving Long-Context Task with Memory Agent via RL
Figure2 MemAgent is inspired by the way humans process long documents. It divides the document into multiple
chunksandallowsLLMstoprocessthemiteratively,recordingrelevantinformationinmemory. Finally,LLMsgenerate
answers based on the information stored in the memory.
long-context processing.
• Wedesignanagentworkflowtoimplementthismechanismandproposeanend-to-endtrainingapproach
using the multi-conversation DAPO algorithm.
• We empirically demonstrate that our RL-trained method allows models to extrapolate to vastly long
documentswithminimalperformancedegradation,pushingtheboundariesofwhatiscurrentlyachievable
in long-context LLM systems.
2 Related Work
Extrapolation methods for RoPE-based LLMs [11], such as NTK [12], PI [13], YaRN [14]
LongContextLLMs
and DCA [15], modify the base frequency, position index and other components of positional embeddings,
enabling the model to capture long-range semantic dependencies. On the other hand, Linear attention
mechanisms [22, 23], Recurrent Neural Networks (RNNs) and State Space Models (SSMs) [36–40] leverage
different architectures to achieve O(N) computation complexity, aiming to process extremely long context.
Sparse attention [19–21] shifts the attention mask matrix to apply patterns such as sliding windows, thereby
eliminating irrelevant attention calculations. However, these patterns are typically based on predefined
heuristics. The possibility of dynamic sparse attention [41, 42] has been explored recently. The Long Short-
Term Memory (LSTM) mechanism [29] achieved significant success in early NLP tasks, while Neural Turing
Machines [30] and Memory Networks [31] demonstrated how to equip neural networks with memory. Existing
memory mechanisms integrated to Transformer models are typically realized by adding external memory
modules [26, 43–45] or external database [46–48]. In contrast, we use reinforcement learning (RL) to enable
LLM itself the ability to memorize.
In recent RL studies, the reward signals have gradually shifted from human
ReinforcementLearningforLLMs
preferences [49] or reward models distilled from them [50] to rule-based feedback, which has demonstrated
great potential in enhancing model reasoning capabilities [3, 4, 51–53]. Key contributions include PPO [54]
based on GAE [55], the Actor-Critic framework, as well as GRPO [56] that utilizes Group Normalization.
Algorithmic enhancements [35, 57, 58] have mostly focused on improving training sustainability and sample
efficiency of these algorithms. To further release the potential of RL, recent works such as Search-R1 [33],
Agent-R1 [32] and RAGEN [59] have explored the training of tool-using agents based on multi-turn chat.
However, these multi-turn chats are constructed by alternately concatenating tool responses and model
replies, with the ultimate optimization goal being a single conversation with tool masking. GiGPO [34]
further investigates the use of multiple independent contexts in agent training with environment feedback
3
with sliding window trajectories. However, these approaches are limited to optimizing interleaved trajectories
of observation and generation, making them difficult to apply to more general agent workflows.
3 The Proposed MemAgent
In this section, we describe the details of MemAgent approach for solving long-context tasks, including the
overall workflow (§ 3.1), Multi-conv RL algorithm for training MemAgent (§ A), reward modeling design
(§ 3.3), and architecture implementation design (§ 3.4).
3.1 The MemAgent Workflow: RL-shaped Memory for Unbounded Contexts
As illustrated in Figure 2, MemAgent views an arbitrarily long document not as a monolithic block but as a
controlled stream of evidence. At every step, the model sees exactly two things: the next chunk of text and a
compact, fixed-length memory that summarizes everything deemed important so far. Crucially, the memory
is just a sequence of ordinary tokens inside the context window, so the core generation process of the base
LLM remains unchanged.
After reading a new chunk, the model overwrites the previous memory with an updated one. This
overwrite
strategy seems almost too simple, yet it is precisely what enables the system to scale: because memory length
never grows, the total compute per chunk stays O(1) and end-to-end complexity is strictly linear to the
number of chunks. We formulate the overwrite decision as a reinforcement learning problem: the agent is
rewarded for retaining information that will later prove useful and for discarding distractors that would waste
precious tokens. By optimizing this objective with our newly introduced multi-conversation DAPO algorithm
(detailed in § A), the model learns to compress aggressively while preserving answer-critical facts.
The workflow naturally decomposes inference into two modules. Within the module the
Context-Processing
model iterates over chunks, updating memory with a prompt template (Table 1, top). Once the stream is
exhausted, a final module is invoked (Table 1, bottom) where the model consults only
Answer-Generation
the problem statement and the memory to produce its boxed answer. Because positional embeddings are
never re-scaled or patched, the same tokenization and attention layout apply in both modules, unlocking the
model’s latent length-extrapolation capability without any architectural modifications.
MemAgent therefore enjoys three benefits from this design: (1) : the document can be
Unlimited length
millions of tokens because it is processed as a stream; (2) : RL encourages the memory
Noperformancecliff
to retain exactly the information needed, yielding near-lossless extrapolation (Figure 1); (3) : a
Linearcost
constant window size implies decoding time and memory consumption grow linearly with input length (O(N))
(detailedin§A.)Thisrendersapracticalrecipeforturninganymoderatelycontext-sizedLLMintoanefficient
long-context reasoner with minimal engineering overhead.
3.2 Training MemAgent with Multi-conv RL
By viewing memory update in context processing for answer-generation tasks as part of the policy to be
optimized by RL, we adopt the RLVR recipe [3, 51, 60] to train MemAgent.
For the base algorithm, we adopt Group Relative Policy Optimization (GRPO) [56] for its simplicity and
effectiveness in RLVR. In the rollout phase of GRPO, the policy model π samples a group of G individual
θold
responses {o }G for an input x. Let {R }G refer to the sequence-level rewards, then the group normalizing
i i=1 i i=1
advantage of the i-th response is calculated by the following function:
r −mean({R }G )
Aˆ = i i i=1 . (1)
i,t std({R }G )
i i=1
GRPO adopts a clipped objective with a KL penalty term:
4
You are presented with a , a of an article that may contain the answer, and a
problem section previous
. Please read the section carefully and update the memory with new information that helps to
memory
answer the problem, while retaining all relevant details from the previous memory.
<problem> {prompt} </problem>
<memory> {memory} </memory>
<section> {chunk} </section>
Updatedmemory:
You are presented with a and a . Please answer the problem based on the
problem previousmemory
previous memory and put the answer in \boxed {}.
<problem> {prompt} </problem>
<memory> {memory} </memory>
Youranswer:
Table1 Templateof MemAgentforcontextprocessing(toppart)andfinalanswergeneration(bottom). Curly-brace
placeholders {} will be replaced with actual content.
J (θ)=E
GRPO (q,a)∼D,{oi}G
i=1
∼πθold (·|q)
(cid:34)
1 (cid:88)
G
1 (cid:88)
|oi|(cid:32)
min (cid:16) r (θ)Aˆ , clip (cid:16) r (θ),1−ε,1+ε (cid:17) Aˆ (cid:17) −βD (π ||π )
(cid:33)(cid:35)
,
(2)
G |o | i,t i,t i,t i,t KL θ ref
i
i=1 t=1
where r (θ) refers to the importance sampling weight:
i,t
π (o |q,o )
r (θ)= θ i,t i,<t . (3)
i,t π (o |q,o )
θold i,t i,<t
However, due to the nature of the MemAgent approach, it generates multiple context-independent conversa-
tions for a single query, as illustrated in Figure 2. Therefore, policy optimization cannot be implemented by
simply applying the attention mask as is done in multi-turn tool-calling optimization.
To address this issue, we treat each conversation as an independent optimization target, as demonstrated in
Figure 3. Let n denote the number of generated conversations (o ,o ,...,o ) for a given sample (q ,a ) in
i i,1 i,2 i,ni i i
a group. o further decomposes into token-level outputs (o ,o ,...,o ). We compute an outcome
i,j i,j,1 i,j,2 i,j,|oi,j|
rewardR persamplebythefinalconversationthatcontainsthefinalanswer,anddistributegroup-normalized
i
advantages across all associated conversations.
Equations 4 and 5 illustrate how the advantage and loss are computed within our MemAgent algorithm for
context-independent multi-conversation rollouts. The advantage value is derived from the conversation that
contains the final answer, then uniformly applied across all conversations originating from the same sample.
Our loss function is analogous to that used in DAPO [35], which incorporates a token-level averaging loss.
Furthermore, we extend the dimensionality of the loss computation from the conventional (group, token)
structure to (group, conversation, token). Following DrGRPO [58], we do not normalize the advantage
by the standard deviation of rewards.
Aˆ =r −mean({R }G ) (4)
i,j,t i i i=1
5
KL 𝒥clip
o Reference r A
1 Model 1 1
q Policy o Rule-Based r Group A
Model 2 Verifier 2 Normalization 2
… … …
o r A Frozen
GRPO G G G Model
Trainable
Model
Group of Conversations KL 𝒥clip Take part in
Adv. Compute
Context-Independent Conversations
o 1,1 o 1,2 … o 1,c 1 Re M fe o r d e e n l c e r 1 A 1
q Policy Rule-Based r Group A
Model o 2,1 o 2,2 … o 2,c 2 Verifier 2 Normalization 2
… …
…
Multi-conv r A
G G
DAPO o G,1 o G,2 … o G,cG
Figure3 Comparison between vanilla GRPO and Multi-Conv DAPO. During the rollout phase of Multi-conv DAPO,
each sample generates multiple conversations. The answer contained in the final conversation is used to compute the
reward and advantage, which are then employed to optimize all preceding conversations.
J (θ)= E
DAPO (q,a)∼D,{oi,j}G
i=1
∼πθold (·|q, oi,j−1)
(cid:34)
1 (cid:88)
G
(cid:88)
ni |
(cid:88)
oi,j|
(cid:16) (cid:17)
(cid:35)
C −βD (π ||π (5)
(cid:80)G (cid:80)ni
|o |
i,j,t KL θ ref
i=1 j=1 i,j i=1j=1 t=1
(cid:16) (cid:16) (cid:17) (cid:17)
where C =min r (θ)Aˆ , clip r (θ),1−ε ,1+ε Aˆ
i,j,t i,j,t i,j,t i,j,t low high i,j,t
3.3 Reward Modeling
Following the RLVR recipe [33, 35, 51], we train the model with a final outcome reward computed by a
rule-based verifier. In RULER [1] and other datasets, questions may have multiple ground-truth answers. For
some tasks, such as question answering, these ground truths are considered equivalent. Given a set of multiple
ground-truth answers Y ={y ,y ,...,y }, the reward score is defined as:
1 2 n
R(yˆ,Y)=max (cid:0)I(is_equiv(y,yˆ) (cid:1) (6)
y∈Y
where yˆis the predicted answer, and I(·) denotes the indicator function.
For other tasks, all ground-truth answers are expected to be included in the final output. An example is
the task of Multi-Value Needle in a Haystack, where the question might be: “What are all the special magic
numbers for XXX?” In such cases, the reward function is defined as:
|y ∈Y |I(y ∈yˆ)|
R(yˆ,Y)= (7)
|Y|
where |·| denotes the cardinality of a set.
3.4 Rethinking MemAgent from Autoregressive Modeling Perspectives
Finally, to get a deeper sense of the MemAgent design, we propose to re-think language-model factorization
in the following fashion. A standard autoregressive LLM factorizes the joint likelihood of a sequence x as
1:N
6
External Input External Output External Input External Output
Controller
p(c k ∣m k−1) p(m k ∣c k ,m k−1) c1 c2 … cK cK+1
Read Head Write Head
∅ m1 m2 … mK
Memory
t=0 t=1 t=2 t=K t=K+1
Architecture of MemAgent Graphical Model of MemAgent
Figure4 The architecture and graphic model of MemAgent. The memory is modeled as a latent memory variable,
thereby enabling the decomposition of the autoregressive language model into multiple steps of reading from and
writing to the memory.
p(x )= (cid:81)N p(x |x ), implicitly assuming that every past token (or at least its hidden state) must
1:N n=1 n 1:n−1
stay in the active context. This is what turns quadratic attention into the long-context bottleneck.
MemAgent replaces the unbounded history with a fixed-length memory m∈VM, as shown in Figure 4. The
input text is streamed through the model in K contiguous chunks c1,...,cK (each of length ≤ C). After
chunk k is read, the model overwrites the panel with a new vector mk that summarizes all evidence seen so
far. Because |mk|=M is constant, both compute and memory per step are O(C+M), yielding an overall
linear complexity O(N).
Introducing the latent sequence m1:K−1 decomposes the original likelihood as
K
(cid:88) (cid:89)
p(x )= p(ck |mk−1) p(mk |ck,mk−1), (8)
1:N
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
m1:K−1k=1
read write
with base case m0 =∅. Inside each chunk, we still run an ordinary transformer decoder, but conditioned
on a constant context window (ck,mk−1). The read path factorizes token-by-token, p(ck | mk−1) =
(cid:81)kC p(x |x ,mk−1), while the write path generates the next memory in the same autoregressive
i=(k−1)C+1 i 1:i−1
fashion.
MemAgent enjoys token-level compression of context, yet local-global or linear-attention models compress
long context in the feature space; their summaries are implicit and opaque. MemAgent’s summaries reside
in token space, so every intermediate memory is human-readable and can be inspected or even edited — a
property we exploit when designing the RL reward (§3.3). Conceptually, Equation 8 turns the transformer
into a recurrent network whose state size is user-controllable.
Because memory tokens are latent and updated via a discrete overwrite rule, back-
Why is RL Essential?
propagation alone cannot teach the model what to keep and what to discard. Our multi-conversation GRPO
algorithm (§A) treats each read–write–read loop as an RL transition, directly rewarding memories that lead
to a correct final answer. This bridges the gap between explicit supervision (answers) and implicit structure
(good memories), completing the training pipeline introduced earlier.
7
The resulting MemAgent architecture preserves the vanilla decoder’s training recipe, requires no exotic
attention kernels, and satisfies the long-context trilemma of arbitrary length, lossless extrapolation, and linear
cost.
4 Experiments
For our training and primary evaluation, we utilize multi-hop long-text question answering (QA) tasks, and
furtherconductevaluationsonothervariouslong-texttasks. Weselectpriorlong-contextmethodsasbaselines
to evaluate the long-text extrapolation capabilities of the models by comparing performance changes as the
length of the test set data increases.
4.1 Datasets
RULER [1] comprises various synthetic tasks with controllable context lengths, making it an ideal benchmark
for investigating how model performance varies with increasing context length.
The Question Answering subset of RULER adapts existing short-context QA datasets for long-context
evaluation by embedding golden paragraphs (containing correct answers) within extensive distractor content
sampled from the same dataset. This configuration represents a real-world adaptation of the Needle in a
Haystack (NIAH) paradigm, where questions serve as queries, golden paragraphs function as needles, and
distractor paragraphs constitute the haystack. This task bridges the gap between synthetic evaluation and
practical long-context applications, well poised for assessing a model’s ability to locate and extract relevant
information from realistic document collections.
We synthesized training samples from the HotpotQA dataset using this methodology. Our synthetic data
comprises a total of 200 articles, with an approximate token length of 28K.
We thoroughly cleaned our dataset by filtering out questions where the Best-Of-2 score is 100% without
requiring any context for Qwen2.5-7B-Base or Qwen2.5-7B-Instruct. These questions likely represent common
knowledge already internalized within the models’ memories. Using this method, we processed 80,000 samples
fromtheHotpotQA[2]trainingsplit. Approximately50%ofthedatawerefilteredout,andfromtheremaining
samples we selected the frist 32,768 samples for further use.
We then applied a similar approach to synthesize 128 samples from the HotpotQA validation set. To further
investigate how model performance varies with length, we synthesized test sets with different context lengths
using the same questions. The number of articles ranges from 50, 100, up to 6400, corresponding to context
lengths of approximately 7K, 14K, and up to 3.5M tokens, respectively.
4.2 Experimental Setup
To maintain comparability with previous work, we choose Qwen2.5-7B-Instruct and Qwen2.5-
TrainingDetails
14B-Instruct as base models for experiments. We implement the framework for multi-conversation with
independent contexts based on verl [61]. During training, we intentionally limit the model to an 8K context
window to highlight its extrapolation capabilities. This 8K-window was allocated as follows: 1024 tokens for
the query, 5000 tokens for the context chunk, 1024 tokens for the memory, and 1024 tokens for the output,
with remaining tokens reserved for the chat template. Consequently, the model typically requires 5 to 7
conversational turns to process the entire context.
We use the GRPO algorithm for training, applying a KL factor of 1e-3 and disabling the
Hyperparameters
entropyloss. WeemploytheAdamWoptimizerwithalearningrateof1e-6,scheduledwithaconstantlearning
rate with linear warm-up. We use a rollout batch size of 128 and 256 for 7B and 14B models, respectively,
and a group size of 16. The ratio of the sample batch size to the backpropagation batch size is set to 16.
WeuseDeepSeek-R1-Distill-Qwen[51],Qwen-2.5-Instruct-1M[62]andQwenLong-L1[63]
ModelConfiguration
as baselines. We follow the official configurations of these baseline models to set context lengths. Specifically,
for the Qwen2.5-Instruct-1M series, we further extrapolate the context length to 1M tokens using DCA. For
the DeepSeek-R1-Distill-Qwen series and QwenLong, the context length is set to 128K tokens. For the model
8
with 128K context length, the input consists of 120,000 tokens, with an output of 10,000 tokens. For the
model with 1M context length, the input is 990,000 tokens, with an output of 10,000 tokens.
4.3 Main Results
The main experimental results are reported in Table 2. We conduct a comparative analysis of all model
performances within the context length ranging from 7K to 896K. Specifically, for the MemAgent model,
we extend our evaluation to explore its extrapolation capabilities on ultra-long contexts of 1.75M and 3.5M,
assessing how the model generalizes beyond the standard context range.
From these results, we observe that MemAgent exhibits remarkable length extrapolation capabilities with
only marginal performance decay as the input context length increases. This demonstrates the effectiveness
of the proposed memory mechanism combined with reinforcement learning for handling ultra-long context
scenarios.
In contrast, baseline models demonstrate distinct failure patterns even within the context window. The
reasoningmodels(DS-Distill-Qwenseries)showrapidperformancedegradation,whileQwenLong-L1maintains
reasonable performance within its training length 60K but experiences substantial degradation afterward. The
Qwen2.5-Instruct-1M series models maintains an acceptable performance within 112K tokens. However, their
performancesdeterioratetozeroat896Ktokens,wellbeforereachingtheirtheoretical1Mtokencapacity. This
suggests that despite extended context windows, these models struggle with effective information utilization
in ultra-long contexts.
Table2 Main experimental results comparing model performance across various context lengths. All values represent
accuracy (%).
Length
Model
7K 14K 28K 56K 112K 224K 448K 896K 1.75M 3.5M
QwenLong-L1-32B 72.66 75.00 72.66 60.94 31.25 17.19 13.28 11.72 N/A N/A
Qwen2.5-Instruct-14B-1M 60.16 60.94 50.00 57.03 50.00 37.50 8.59 0.00 N/A N/A
Qwen2.5-Instruct-7B-1M 61.72 56.25 53.91 55.47 51.56 33.59 12.50 0.00 N/A N/A
DS-Distill-Qwen-32B 70.31 66.41 65.62 46.88 23.44 13.28 7.81 7.03 N/A N/A
DS-Distill-Qwen-14B 64.06 64.84 57.03 40.62 14.84 8.59 3.12 6.25 N/A N/A
DS-Distill-Qwen-7B 30.47 12.50 3.12 0.00 0.00 0.78 0.00 0.00 N/A N/A
RL-MemAgent-14B 83.59 82.03 84.38 80.47 76.56 81.25 75.00 77.34 76.56 78.12
RL-MemAgent-7B 82.03 79.69 78.91 77.34 79.69 72.66 74.22 76.56 75.78 71.09
4.4 Ablation Study
Toinvestigatetheimpactofreinforcementlearningonthememorymechanism,weconductfurther
RLTraining
ablation experiments. Our baselines are Qwen2.5-Instruct [64] series and Qwen2.5-Instruct models which are
equipped with memory mechanism without RL training.
As shown in Figure 5, vanilla models exhibit severe performance degradation as context length increases,
especially after 112K where the inputs are truncated because of the context window. While the model
equipped with a memory, without RL training, demonstrates better performance and maintains reasonable
performance on tasks exceeding the context length, it still experiences an overall decline in performance as
the input length increases.
Incontrast,RL-trainedmodelsmaintainconsistentlyhighperformanceacrossallcontextlengthswithminimal
degradation. This demonstrates that while the memory mechanism provides structural support for long
contexts, reinforcement learning is essential for teaching models to properly leverage the memory.
To evaluate the generalization capabilities of our approach, we conduct comprehen-
Out-of-DistributionTasks
sive experiments on the OOD task in RULER benchmark, including ,
needle-in-a-haystackvariants variable
, , and synthesized from SQuAD [65]. We synthesize
tracking frequentwordsextraction questionanswering
9
80
70
60
50
40
30
20
10
0
7K 28K 112K 224K 448K 896K
Context Length in Tokens
erocS
RL-MemAgent-14B
RL-MemAgent-7B
MemAgent-32B w/o RL
MemAgent-14B w/o RL
MemAgent-7B w/o RL
Qwen2.5-Instruct-32B
Qwen2.5-Instruct-14B
Qwen2.5-Instruct-7B
Truncation
Figure 5 Ablation study on RULER-HotpotQA comparing models with and without RL training across context
lengths from 28K to 896K tokens.
context lengths ranging from 8K to 512K tokens for these tasks, except that SQuAD extends only to 256K
tokens due to limited document length.
Figure 6 presents the performance comparison across different task categories. The results demonstrate that
MemAgent maintains consistently superior performance across diverse task types. Particularly, MemAgent-
14B achieves over 95% accuracy on the average RULER tasks in context ranging from 8K to 512K, while
MemAgent-7B achieves the best performance, surpassing 32B model without RL training and long-context
post-trained models. MemAgent-7B/14B both maintain stable performance on the SQuAD-based QA task,
indicating that memorizing ability can generalize beyond training data. In contrast, baseline models show
significant degradation beyond 128K tokens across all task categories.
The consistent performance strength across heterogeneous tasks validates that the memory mechanism
effectively generalizes to various long-context scenarios rather than overfitting to specific formats. Complete
results for all individual RULER tasks are provided in Appendix B.
4.5 Case Study
To further illustrate the proposed memory mechanism in detail, we conduct a case study on a generation
trajectory of MemAgent-14B. The input question is: The director of the romantic comedy ‘Big Stone Gap’
is based in what New York city? This a 2-hop question with the following relevant Wikipedia entries:
1) is a 2014 American drama romantic comedy film written and directed by Adriana Trigiani.
BigStoneGap
2) is an Italian American best-selling author of sixteen books, television writer, film director,
AdrianaTrigiani
and entrepreneur based in Greenwich Village, New York City.
In the first round, the model is presented with the entry Ghost, which refers to a production team also based
in New York. The model chooses to retain this potentially useful information for future use. In the second
round, no relevant context is provided; nevertheless, the model maintains its agent state, demonstrating
robustness against distraction. In the third round, both relevant entries are presented. The model correctly
identifies critical information and updates its memory accordingly, leading to the correct answer: Greenwich
Village, New York City. At this point, the reasoning process is complete. In the remaining rounds, the model’s
memory remains unchanged and is used to produce the final response.
10
100 100
RL-MemAgent-14B 97.45 96.97 97.46 97.85 96.08 96.24 95.40 RL-MemAgent-14B 77.34 76.56 79.69 77.34 78.12 77.34
RL-MemAgent-7B 93.03 92.03 91.33 88.83 86.92 83.70 81.91 RL-MemAgent-7B 81.25 81.25 82.03 76.56 79.69 81.25
MemAgent-32B w/o RL 99.04 96.59 94.61 91.85 86.56 83.57 81.51 MemAgent-32B w/o RL 78.12 75.00 71.09 75.00 73.44 71.09
80 80
MemAgent-14B w/o RL 97.95 90.22 87.43 80.30 67.97 58.88 46.18 MemAgent-14B w/o RL 70.31 68.75 70.31 66.41 64.84 53.91
MemAgent-7B w/o RL 92.56 92.47 90.52 88.36 84.46 80.05 73.48 MemAgent-7B w/o RL 60.16 66.41 58.59 55.47 66.02 57.03
QwenLong-L1-32B 92.00 91.23 91.40 77.39 41.66 23.22 14.78 60 QwenLong-L1-32B 82.81 78.91 73.44 67.19 36.72 33.59 60
Qwen2.5-Instruct-14B-1M 98.34 97.31 93.47 90.50 89.95 83.91 62.34 Qwen2.5-Instruct-14B-1M 85.16 82.81 79.69 77.34 68.75 51.56
Qwen2.5-Instruct-7B-1M 90.28 89.57 88.56 87.37 85.11 78.14 39.21 Qwen2.5-Instruct-7B-1M 76.56 74.22 71.88 63.28 61.72 50.00
DS-Distill-Qwen-32B 97.28 97.54 95.21 76.63 40.11 24.09 15.73 40 DS-Distill-Qwen-32B 78.91 71.09 67.97 46.88 28.91 28.91 40
DS-Distill-Qwen-14B 95.33 95.06 89.89 64.50 28.65 17.59 12.40 DS-Distill-Qwen-14B 71.09 67.97 58.59 39.84 22.66 23.44
DS-Distill-Qwen-7B 53.96 14.77 1.45 0.03 0.00 0.00 0.00 DS-Distill-Qwen-7B 31.25 11.72 8.59 2.34 0.78 0.78
Qwen2.5-Instruct-32B 97.23 94.42 91.59 91.34 79.95 44.74 27.01 20 Qwen2.5-Instruct-32B 86.72 76.56 71.09 65.62 55.47 45.31 20
Qwen2.5-Instruct-14B 90.91 86.65 83.05 79.16 69.39 39.22 24.87 Qwen2.5-Instruct-14B 83.59 73.44 66.41 58.59 48.44 42.19
Qwen2.5-Instruct-7B 58.53 48.10 45.48 54.37 38.01 25.69 17.05 Qwen2.5-Instruct-7B 71.09 67.19 71.09 57.03 49.22 39.84
0 0
8K 16K 32K 64K 128K 256K 512K 8K 16K 32K 64K 128K 256K
RL-MemAgent Long Context Model Backbone RL-MemAgent Long Context Model Backbone
MemAgent w/o RL Reasoning Model MemAgent w/o RL Reasoning Model
(a) RULER average across 10 tasks (b) RULER-QA task from SQuAD
Figure6 Performance heatmaps on RULER benchmark tasks showing accuracy scores across different context lengths
(greener indicates better performance). Models are grouped by type on the vertical axis. (a) Average performance
across 10 synthetic tasks including needle-in-a-haystack variants, variable tracking, and word extraction. (b) Question
answering task synthesized from SQuAD dataset with context lengths up to 256K tokens.
Chunk1
...
Document 20: Ghost (production team)
Ghost is a Swedish record producing and songwriting team, composed of Ulf Lindström and Johan
Ekhé, based in New York City.
...
Memory1
The provided section does not contain any information about the director of the romantic comedy
"Big Stone Gap" or their base in New York City.
However,itdoesmentionaproductionteamcalled
Since the problem is specifically asking about the director of
GhostwhichisbasedinNewYorkCity.
"Big Stone Gap," and there is no direct information about the director in the given section, we cannot
infer anything directly related to the problem from the provided text.
Updated memory:
• Ghost is a Swedish record producing and songwriting team, composed of Ulf Lindström and
Johan Ekhé, based in New York City. They are perhaps best known for writing and producing
Swedish singer Robyn’s three first studio albums.
The problem remains unanswered based on the provided section. Additional information would be
needed to determine the director of "Big Stone Gap" and their base in New York City.
11
Chunk2
...(No relevant document)
Memory2
Theprovidedsectiondoesnotcontainanyinformationaboutthedirectoroftheromanticcomedy
BigStoneGaportheirbaseinNewYorkCity.Therefore,theupdatedmemoryremainsunchanged
The memory still notes that the Ghost record producing and
withrespecttotheproblemathand.
songwritingteamisbasedinNewYorkCity,butitdoesnotprovideanyinformationaboutthedirector
of "Big Stone Gap."
Updated memory:
• Ghost is a Swedish record producing and songwriting team, composed of Ulf Lindström and
Johan Ekhé, based in New York City. They are perhaps best known for writing and producing
Swedish singer Robyn’s three first studio albums.
• The problem remains unanswered based on the provided section. Additional information would
be needed to determine the director of "Big Stone Gap" and their base in New York City.
Chunk3
...
Document 81: Big Stone Gap (film)
is a 2014 American drama romantic comedy film written and directed by
Big Stone Gap Adriana
and produced by Donna Gigliotti for Altar Identity Studios, a subsidiary of Media Society.
Trigiani
...
Document 96: Adriana Trigiani
is an Italian American best-selling author of sixteen books, television writer, film
AdrianaTrigiani
director, and entrepreneur based in .
GreenwichVillage,NewYorkCity
...
Memory3
Updated memory:
• Ghost is a Swedish record producing and songwriting team, composed of Ulf Lindström and
Johan Ekhé, based in New York City. They are perhaps best known for writing and producing
Swedish singer Robyn’s three first studio albums.
• isanItalianAmericanbest-sellingauthorofsixteenbooks,televisionwriter,film
AdrianaTrigiani
director, and entrepreneur based in Greenwich Village, New York City. Trigiani has published a
novel a year since 2000.
• is a 2014 American drama romantic comedy film written and directed by Adriana
BigStoneGap
Trigiani and produced by Donna Gigliotti for Altar Identity Studios, a subsidiary of Media
Society. Based on Trigiani’s 2000 best-selling novel of the same name, the story is set in the
actual Virginia town of Big Stone Gap circa 1970s. The film had its world premiere at the
Virginia Film Festival on November 6, 2014.
The director of the romantic comedy "Big Stone Gap" is Adriana Trigiani, who is based in
.
GreenwichVillage,NewYorkCity
Thistrajectoryhighlightsseveralcorecapabilitieslearnedbythememoryagent: estimatingpotentiallyrelevant
content from query keywords and storing it preemptively, immediately updating memory upon encountering
context that matches the query, and remaining unaffected by irrelevant information. Notably, these memory
behaviors are not the result of architectural attention mechanisms, but emerge as text generation abilities
reinforced through RL.
5 Conclusion
We propose a novel approach to modeling long-context tasks by introducing a latent variable memory. This
enablesthedecompositionofcontinuousautoregressivegenerationprocessintoaseriesofstepsthatsequentially
12
generate context from memory. Our method can handle infinitely long input text with O(N) computational
complexity, based on existing Dense-Attention Transformers, without altering the generation paradigm or
introducing additional model architectures. We introduce MemAgent to implement this modeling approach,
equipping LLMs with an RL-trained memory, allowing the model to learn the ability to record relevant
information and ignore irrelevant details. Experiments show that when trained on 32K-length data with
8K context (including a 1024-token memory and processing 5000 tokens of input per step), the model can
extrapolate to 3.5M with almost lossless performance during testing. Ablation studies demonstrate the
effectiveness of using the memory itself as a long-context processing mechanism, as well as the benefits
of further RL training on top of it. The results on both in-domain and out-of-domain tasks show that
MemAgent surpasses long-context post-trained models, reasoning models and other baselines, achieving
state-of-the-art performance on long-context tasks.
13
References
[1] Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia, Yang Zhang, and
Boris Ginsburg. Ruler: What’s the real context size of your long-context language models? arXiv preprint
arXiv:2404.06654, 2024.
[2] Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William W Cohen, Ruslan Salakhutdinov, and Christo-
pher D Manning. Hotpotqa: A dataset for diverse, explainable multi-hop question answering. arXiv preprint
arXiv:1809.09600, 2018.
[3] OpenAI. Learning to reason with llms, 2024.
[4] Google DeepMind. Gemini 2.0 flash thinking, 2024.
[5] XAI. Grok 3 beta — the age of reasoning agents, 2024.
[6] Anthropic. Claude 3.5 sonnet, 2024.
[7] OpenAI. GPT4 technical report. arXiv preprint arXiv:2303.08774, 2023.
[8] Anthropic. Introducing claude 4, 2025.
[9] AonianLi,BangweiGong,BoYang,BojiShan,ChangLiu,ChengZhu,ChunhaoZhang,CongchaoGuo,DaChen,
DongLi,etal. Minimax-01: Scalingfoundationmodelswithlightningattention. arXivpreprintarXiv:2501.08313,
2025.
[10] Aixin Liu, Bei Feng, Bin Wang, Bingxuan Wang, Bo Liu, Chenggang Zhao, Chengqi Dengr, Chong Ruan, Damai
Dai, Daya Guo, et al. Deepseek-v2: A strong, economical, and efficient mixture-of-experts language model. arXiv
preprint arXiv:2405.04434, 2024.
[11] JianlinSu,MurtadhaAhmed,YuLu,ShengfengPan,WenBo,andYunfengLiu. Roformer: Enhancedtransformer
with rotary position embedding. Neurocomputing, 568:127063, 2024.
[12] bloc97. NTK-Aware Scaled RoPE allows LLaMA models to have extended (8k+) context size without any
fine-tuning and minimal perplexity degradation., 2023.
[13] Shouyuan Chen, Sherman Wong, Liangjian Chen, and Yuandong Tian. Extending context window of large
language models via positional interpolation. arXiv preprint arXiv:2306.15595, 2023.
[14] Bowen Peng, Jeffrey Quesnelle, Honglu Fan, and Enrico Shippole. Yarn: Efficient context window extension of
large language models. arXiv preprint arXiv:2309.00071, 2023.
[15] Chenxin An, Fei Huang, Jun Zhang, Shansan Gong, Xipeng Qiu, Chang Zhou, and Lingpeng Kong. Training-free
long-context scaling of large language models. arXiv preprint arXiv:2402.17463, 2024.
[16] Xiaoran Liu, Hang Yan, Shuo Zhang, Chenxin An, Xipeng Qiu, and Dahua Lin. Scaling laws of rope-based
extrapolation. arXiv preprint arXiv:2310.05209, 2023.
[17] WenhanXiong,JingyuLiu,IgorMolybog,HejiaZhang,PrajjwalBhargava,RuiHou,LouisMartin,RashiRungta,
Karthik Abinav Sankararaman, Barlas Oguz, et al. Effective long-context scaling of foundation models. arXiv
preprint arXiv:2309.16039, 2023.
[18] Chaochen Gao, Xing Wu, Zijia Lin, Debing Zhang, and Songlin Hu. Nextlong: Toward effective long-context
training without long documents. arXiv preprint arXiv:2501.12766, 2025.
[19] Iz Beltagy, Matthew E Peters, and Arman Cohan. Longformer: The long-document transformer. arXiv preprint
arXiv:2004.05150, 2020.
[20] GuangxiangZhao,JunyangLin,ZhiyuanZhang,XuanchengRen,QiSu,andXuSun. Explicitsparsetransformer:
Concentrated attention through explicit selection. arXiv preprint arXiv:1912.11637, 2019.
[21] Guangxuan Xiao, Yuandong Tian, Beidi Chen, Song Han, and Mike Lewis. Efficient streaming language models
with attention sinks. arXiv preprint arXiv:2309.17453, 2023.
[22] Rewon Child, Scott Gray, Alec Radford, and Ilya Sutskever. Generating long sequences with sparse transformers.
arXiv preprint arXiv:1904.10509, 2019.
14
[23] Angelos Katharopoulos, Apoorv Vyas, Nikolaos Pappas, and François Fleuret. Transformers are rnns: Fast
autoregressive transformers with linear attention. In International conference on machine learning, pages 5156–
5165. PMLR, 2020.
[24] Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, and Lili Qiu. Llmlingua: Compressing prompts for
accelerated inference of large language models. arXiv preprint arXiv:2310.05736, 2023.
[25] Yucheng Li, Bo Dong, Chenghua Lin, and Frank Guerin. Compressing context to enhance inference efficiency of
large language models. arXiv preprint arXiv:2310.06201, 2023.
[26] Ali Behrouz, Peilin Zhong, and Vahab Mirrokni. Titans: Learning to memorize at test time. arXiv preprint
arXiv:2501.00663, 2024.
[27] Jiaxin Zhang, Yiqi Wang, Xihong Yang, Siwei Wang, Yu Feng, Yu Shi, Ruichao Ren, En Zhu, and Xinwang Liu.
Test-time training on graphs with large language models (llms). In Proceedings of the 32nd ACM International
Conference on Multimedia, pages 2089–2098, 2024.
[28] George A Miller et al. The magical number seven, plus or minus two. Psychological review, 63(2):81–97, 1956.
[29] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural computation, 9(8):1735–1780, 1997.
[30] Alex Graves, Greg Wayne, and Ivo Danihelka. Neural turing machines. arXiv preprint arXiv:1410.5401, 2014.
[31] Jason Weston, Sumit Chopra, and Antoine Bordes. Memory networks. arXiv preprint arXiv:1410.3916, 2014.
[32] Jie Ouyang, Ruiran Yan, Yucong Luo, Mingyue Cheng, Qi Liu, Zirui Liu, Shuo Yu, and Daoyu Wang. Training
powerful llm agents with end-to-end reinforcement learning, 2025.
[33] Bowen Jin, Hansi Zeng, Zhenrui Yue, Jinsung Yoon, Sercan Arik, Dong Wang, Hamed Zamani, and Jiawei
Han. Search-r1: Training llms to reason and leverage search engines with reinforcement learning. arXiv preprint
arXiv:2503.09516, 2025.
[34] Lang Feng, Zhenghai Xue, Tingcong Liu, and Bo An. Group-in-group policy optimization for llm agent training.
arXiv preprint arXiv:2505.10978, 2025.
[35] Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Tiantian Fan, Gaohong Liu,
Lingjun Liu, Xin Liu, et al. Dapo: An open-source llm reinforcement learning system at scale. arXiv preprint
arXiv:2503.14476, 2025.
[36] Albert Gu, Karan Goel, and Christopher Ré. Efficiently modeling long sequences with structured state spaces.
arXiv preprint arXiv:2111.00396, 2021.
[37] Albert Gu and Tri Dao. Mamba: Linear-time sequence modeling with selective state spaces. arXiv preprint
arXiv:2312.00752, 2023.
[38] Bo Peng, Eric Alcaide, Quentin Anthony, Alon Albalak, Samuel Arcadinho, Stella Biderman, Huanqi Cao, Xin
Cheng, Michael Chung, Matteo Grella, et al. Rwkv: Reinventing rnns for the transformer era. arXiv preprint
arXiv:2305.13048, 2023.
[39] Soham De, Samuel L Smith, Anushan Fernando, Aleksandar Botev, George Cristian-Muraru, Albert Gu, Ruba
Haroun, Leonard Berrada, Yutian Chen, Srivatsan Srinivasan, et al. Griffin: Mixing gated linear recurrences with
local attention for efficient language models. arXiv preprint arXiv:2402.19427, 2024.
[40] Leo Feng, Frederick Tung, Hossein Hajimirsadeghi, Mohamed Osama Ahmed, Yoshua Bengio, and Greg Mori.
Attention as an rnn. arXiv preprint arXiv:2405.13956, 2024.
[41] Jingyang Yuan, Huazuo Gao, Damai Dai, Junyu Luo, Liang Zhao, Zhengyan Zhang, Zhenda Xie, YX Wei, Lean
Wang, Zhiping Xiao, et al. Native sparse attention: Hardware-aligned and natively trainable sparse attention.
arXiv preprint arXiv:2502.11089, 2025.
[42] EnzheLu,ZhejunJiang,JingyuanLiu,YulunDu,TaoJiang,ChaoHong,ShaoweiLiu,WeiranHe,EnmingYuan,
Yuzhi Wang, et al. Moba: Mixture of block attention for long-context llms. arXiv preprint arXiv:2502.13189,
2025.
[43] Pedro Henrique Martins, Zita Marinho, and André FT Martins. ∞-former: Infinite memory transformer. arXiv
preprint arXiv:2109.00301, 2021.
15
[44] Qingyang Wu, Zhenzhong Lan, Kun Qian, Jing Gu, Alborz Geramifard, and Zhou Yu. Memformer: A memory-
augmented transformer for sequence modeling. arXiv preprint arXiv:2010.06891, 2020.
[45] Aydar Bulatov, Yuri Kuratov, Yermek Kapushev, and Mikhail S Burtsev. Scaling transformer to 1m tokens and
beyond with rmt. arXiv preprint arXiv:2304.11062, 2023.
[46] Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, and Yanlin Wang. Memorybank: Enhancing large language
models with long-term memory. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 38,
pages 19724–19731, 2024.
[47] Junru Lu, Siyu An, Mingbao Lin, Gabriele Pergola, Yulan He, Di Yin, Xing Sun, and Yunsheng Wu. Memochat:
Tuning llms to use memos for consistent long-range open-domain conversation. arXiv preprint arXiv:2308.08239,
2023.
[48] Ali Modarressi, Ayyoob Imani, Mohsen Fayyaz, and Hinrich Schütze. Ret-llm: Towards a general read-write
memory for large language models. arXiv preprint arXiv:2305.14322, 2023.
[49] LongOuyang,JeffreyWu,XuJiang,DiogoAlmeida,CarrollWainwright,PamelaMishkin,ChongZhang,Sandhini
Agarwal, Katarina Slama, Alex Ray, John Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens,
Amanda Askell, Peter Welinder, Paul F Christiano, Jan Leike, and Ryan Lowe. Training language models to
followinstructionswithhumanfeedback. InS.Koyejo,S.Mohamed,A.Agarwal,D.Belgrave,K.Cho,andA.Oh,
editors, Advances in Neural Information Processing Systems, volume 35, pages 27730–27744. Curran Associates,
Inc., 2022.
[50] Yuntao Bai, Saurav Kadavath, Sandipan Kundu, Amanda Askell, Jackson Kernion, Andy Jones, Anna Chen,
Anna Goldie, Azalia Mirhoseini, Cameron McKinnon, et al. Constitutional ai: Harmlessness from ai feedback.
arXiv preprint arXiv:2212.08073, 2022.
[51] Daya Guo, Dejian Yang, Haowei Zhang, Junxiao Song, Ruoyu Zhang, Runxin Xu, Qihao Zhu, Shirong Ma, Peiyi
Wang, Xiao Bi, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning. arXiv
preprint arXiv:2501.12948, 2025.
[52] Qwen. Qwq-32b: Embracing the power of reinforcement learning, 2024.
[53] Kimi Team, Angang Du, Bofei Gao, Bowei Xing, Changjiu Jiang, Cheng Chen, Cheng Li, Chenjun Xiao,
Chenzhuang Du, Chonghua Liao, et al. Kimi k1. 5: Scaling reinforcement learning with llms. arXiv preprint
arXiv:2501.12599, 2025.
[54] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization
algorithms. arXiv preprint arXiv:1707.06347, 2017.
[55] John Schulman, Philipp Moritz, Sergey Levine, Michael Jordan, and Pieter Abbeel. High-dimensional continuous
control using generalized advantage estimation, 2018.
[56] Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Mingchuan Zhang, YK Li, Y Wu, and Daya
Guo. Deepseekmath: Pushing the limits of mathematical reasoning in open language models. arXiv preprint
arXiv:2402.03300, 2024.
[57] Jian Hu. Reinforce++: A simple and efficient approach for aligning large language models. arXiv preprint
arXiv:2501.03262, 2025.
[58] Zichen Liu, Changyu Chen, Wenjun Li, Penghui Qi, Tianyu Pang, Chao Du, Wee Sun Lee, and Min Lin.
Understanding r1-zero-like training: A critical perspective. arXiv preprint arXiv:2503.20783, 2025.
[59] Zihan Wang, Kangrui Wang, Qineng Wang, Pingyue Zhang, Linjie Li, Zhengyuan Yang, Xing Jin, Kefan Yu,
Minh Nhat Nguyen, Licheng Liu, Eli Gottlieb, Yiping Lu, Kyunghyun Cho, Jiajun Wu, Li Fei-Fei, Lijuan Wang,
Yejin Choi, and Manling Li. Ragen: Understanding self-evolution in llm agents via multi-turn reinforcement
learning, 2025.
[60] ByteDance Seed, Jiaze Chen, Tiantian Fan, Xin Liu, Lingjun Liu, Zhiqi Lin, Mingxuan Wang, Chengyi Wang,
Xiangpeng Wei, Wenyuan Xu, et al. Seed1. 5-thinking: Advancing superb reasoning models with reinforcement
learning. arXiv preprint arXiv:2504.13914, 2025.
[61] GuangmingSheng,ChiZhang,ZilingfengYe,XibinWu,WangZhang,RuZhang,YanghuaPeng,HaibinLin,and
Chuan Wu. Hybridflow: A flexible and efficient rlhf framework. arXiv preprint arXiv:2409.19256, 2024.
16
[62] An Yang, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei Huang, Haoyan Huang, Jiandong Jiang, Jianhong Tu,
Jianwei Zhang, Jingren Zhou, Junyang Lin, Kai Dang, Kexin Yang, Le Yu, Mei Li, Minmin Sun, Qin Zhu, Rui
Men,TaoHe,WeijiaXu,WenbiaoYin,WenyuanYu,XiafeiQiu,XingzhangRen,XinlongYang,YongLi,Zhiying
Xu, and Zipeng Zhang. Qwen2.5-1m technical report. arXiv preprint arXiv:2501.15383, 2025.
[63] Fanqi Wan, Weizhou Shen, Shengyi Liao, Yingcheng Shi, Chenliang Li, Ziyi Yang, Ji Zhang, Fei Huang, Jingren
Zhou, and Ming Yan. Qwenlong-l1: Towards long-context large reasoning models with reinforcement learning.
arXiv preprint arXiv:2505.17667, 2025.
[64] An Yang, Baosong Yang, Beichen Zhang, Binyuan Hui, Bo Zheng, Bowen Yu, Chengyuan Li, Dayiheng Liu, Fei
Huang, Haoran Wei, et al. Qwen2. 5 technical report. arXiv preprint arXiv:2412.15115, 2024.
[65] Pranav Rajpurkar, Jian Zhang, Konstantin Lopyrev, and Percy Liang. Squad: 100,000+ questions for machine
comprehension of text. arXiv preprint arXiv:1606.05250, 2016.
17
Appendix
A Computation Complexity
We adopt the floating-point operations (FLOP) estimator for the Qwen2Model from verl [61] to compute the
FLOP cost of both the baseline model and our proposed method. The results are shown in Figure 7. The
baseline model exhibits an O(n2) complexity, while MemAgent achieves an O(n) complexity.
2.0
1.5
1.0
0.5
0.0
8K 16K 32K 64K 128K 256K 512K 1M 2M 4M
Context Length
etupmoC
1e19
Baseline
Memory Agent
Figure7 Floating point operations across context lengths from 8K to 4M
For the baseline model, the number of tokens required to process is q+c+o, where q represents the length
for the problem, c is the context length and o represents the output length.
For MemAgent, total FLOP cost is the sum of the FLOPs from all stages. The detailed stages involved are
as follows:
• Initializing: Inthefirststage,themodelprocessesaninputconsistingofq+200+o,where200represents
a constant added to prompt the model to follow the MemAgent workflow.
• Memory Updating: The number of repetitions is determined by k = ⌈c⌉, where c is the variable
N
component of the input. Each repetition requires an input of length q+200+N +o.
• FinalAnswering: Thefinalstageprocessesaninputoflengthq+100+o,whichincludestheaccumulated
output from the previous steps.
We set q =1024,o=1024,N =5000 and c is ranging from 8K to 4M to calculate the final result.
B Complete Out-Of-Domain Task Results
The RULER benchmark comprises tasks across four primary categories: retrieval, multi-hop tracing, aggre-
gation, and question answering. Each task is designed to evaluate specific aspects of long-context modeling
capability through automatically generated examples based on configurable input parameters that define
sequence length and complexity. Within this constrained evaluation framework, task complexity can be
conceptualized as a function of the number of target output tokens and the signal-to-noise ratio within the
context.
The Needle-in-a-Haystack (NIAH) paradigm evaluates retrieval performance in long-context scenarios by
inserting key-value pairs ("needles") into large distractor content ("haystack"). It includes four variants:
18
Single NIAH, which requires retrieving a single needle; Multi-keys NIAH, which involves retrieving one needle
amidst multiple distractors; Multi-values NIAH, where all values associated with a key must be extracted;
and Multi-queries NIAH, which necessitates retrieving multiple needles with distinct keys. Variable Tracking
(VT) tests multi-hop reasoning by tracking entity chains across extended sequences, while Frequent Words
Extraction (FWE) challenges models to identify frequent words in power-law distributions, evaluating their
ability to analyze word frequencies in linguistic data.
B.1 Needle-in-a-Haystack (NIAH)
100 100 100
RL-MemAgent-14B 100.00 100.00 100.00 100.00 100.00 100.00 100.00 RL-MemAgent-14B 100.00 99.22 100.00 100.00 99.22 99.22 100.00 RL-MemAgent-14B 99.22 96.09 99.22 100.00 99.22 97.66 98.44
RL-MemAgent-7B 100.00 100.00 100.00 100.00 98.44 100.00 98.44 RL-MemAgent-7B 100.00 97.66 96.09 94.53 92.19 91.41 85.94 RL-MemAgent-7B 99.22 96.09 99.22 98.44 98.44 97.66 90.62
MemAgent-32B w/o RL 100.00 100.00 100.00 97.66 96.09 96.09 96.88 80 MemAgent-32B w/o RL 100.00 96.09 91.41 81.25 75.00 78.91 60.16 80 MemAgent-32B w/o RL 100.00 92.19 92.19 88.28 72.66 60.16 58.59 80
MemAgent-14B w/o RL 100.00 96.09 98.44 96.88 95.31 95.31 88.28 MemAgent-14B w/o RL 100.00 85.94 75.78 64.06 46.88 41.41 17.19 MemAgent-14B w/o RL 99.22 78.12 75.78 67.19 39.06 31.25 14.84
MemAgent-7B w/o RL 98.44 97.66 96.09 98.44 95.31 95.31 92.19 MemAgent-7B w/o RL 100.00 100.00 98.44 99.22 96.88 97.66 89.06 MemAgent-7B w/o RL 99.22 90.62 92.97 97.66 89.84 86.72 84.38
QwenLong-L1-32B 100.00 100.00 100.00 100.00 88.28 42.97 21.88 60 QwenLong-L1-32B 100.00 100.00 100.00 88.28 28.12 19.53 14.84 60 QwenLong-L1-32B 96.09 96.88 97.66 93.75 40.62 21.88 15.62 60
Qwen2.5-Instruct-14B-1M 100.00 100.00 100.00 100.00 100.00 100.00 100.00 Qwen2.5-Instruct-14B-1M 99.22 100.00 100.00 100.00 100.00 100.00 86.72 Qwen2.5-Instruct-14B-1M 99.22 100.00 100.00 100.00 100.00 100.00 92.97
Qwen2.5-Instruct-7B-1M 100.00 100.00 100.00 100.00 100.00 100.00 100.00 Qwen2.5-Instruct-7B-1M 100.00 100.00 100.00 99.22 98.44 94.53 61.72 Qwen2.5-Instruct-7B-1M 100.00 100.00 99.22 100.00 100.00 100.00 58.59
DS-Distill-Qwen-32B 100.00 100.00 100.00 100.00 89.06 42.97 21.88 40 DS-Distill-Qwen-32B 100.00 100.00 98.44 85.16 29.69 18.75 14.06 40 DS-Distill-Qwen-32B 99.22 100.00 97.66 89.06 31.25 17.19 11.72 40
DS-Distill-Qwen-14B 100.00 100.00 100.00 98.44 84.38 40.62 21.09 DS-Distill-Qwen-14B 99.22 100.00 100.00 60.16 18.75 8.59 11.72 DS-Distill-Qwen-14B 99.22 100.00 100.00 71.88 23.44 10.94 8.59
DS-Distill-Qwen-7B 73.44 27.34 8.59 0.00 0.00 0.00 0.00 DS-Distill-Qwen-7B 57.81 18.75 0.00 0.00 0.00 0.00 0.00 DS-Distill-Qwen-7B 57.03 10.94 0.00 0.00 0.00 0.00 0.00
Qwen2.5-Instruct-32B 100.00 100.00 100.00 100.00 89.06 42.97 21.88 20 Qwen2.5-Instruct-32B 100.00 100.00 100.00 100.00 89.06 45.31 23.44 20 Qwen2.5-Instruct-32B 100.00 100.00 100.00 100.00 95.31 40.62 25.00 20
Qwen2.5-Instruct-14B 100.00 100.00 100.00 100.00 89.06 42.97 21.88 Qwen2.5-Instruct-14B 100.00 100.00 100.00 100.00 89.06 46.09 23.44 Qwen2.5-Instruct-14B 100.00 99.22 100.00 100.00 95.31 40.62 25.00
Qwen2.5-Instruct-7B 85.16 38.28 21.09 25.00 11.72 9.38 3.12 Qwen2.5-Instruct-7B 92.97 68.75 64.06 88.28 50.78 25.00 17.97 Qwen2.5-Instruct-7B 84.38 85.94 88.28 96.88 78.91 38.28 24.22
8K 16K 32K 64K 128K 256K 512K 0 8K 16K 32K 64K 128K 256K 512K 0 8K 16K 32K 64K 128K 256K 512K 0
RL-MemAgent Long Context Model Backbone RL-MemAgent Long Context Model Backbone RL-MemAgent Long Context Model Backbone
MemAgent w/o RL Reasoning Model MemAgent w/o RL Reasoning Model MemAgent w/o RL Reasoning Model
(a) NIAH Single-key 1 (b) NIAH Single-key 2 (c) NIAH Single-key 3
Figure8 Performance on Single-keys NIAH tasks with increasing numbers of distractor needles. Tasks 1-3 represent
different levels of difficulty with varying distractor densities.
100 100 100
RL-MemAgent-14B 100.00 100.00 99.22 99.22 98.44 99.22 98.44 RL-MemAgent-14B 100.00 96.88 98.44 100.00 92.97 92.19 85.94 RL-MemAgent-14B 92.97 93.75 89.06 90.62 82.81 83.59 78.91
RL-MemAgent-7B 99.22 100.00 100.00 97.66 93.75 91.41 95.31 RL-MemAgent-7B 99.22 95.31 93.75 73.44 73.44 57.81 49.22 RL-MemAgent-7B 99.22 96.09 94.53 95.31 96.88 96.88 94.53
MemAgent-32B w/o RL 100.00 96.88 90.62 85.94 63.28 63.28 61.72 80 MemAgent-32B w/o RL 100.00 96.88 95.31 92.19 89.06 86.72 89.06 80 MemAgent-32B w/o RL 99.22 98.44 97.66 94.53 92.97 84.38 81.25 80
MemAgent-14B w/o RL 100.00 86.72 83.59 72.66 48.44 34.38 17.97 MemAgent-14B w/o RL 99.22 95.31 87.50 86.72 84.38 62.50 53.91 MemAgent-14B w/o RL 97.66 85.94 84.38 71.09 57.81 45.31 35.94
MemAgent-7B w/o RL 96.09 96.09 96.09 91.41 88.28 87.50 86.72 MemAgent-7B w/o RL 96.88 87.50 80.47 73.44 65.62 50.78 32.03 MemAgent-7B w/o RL 96.09 96.09 92.19 85.16 78.12 66.41 53.12
QwenLong-L1-32B 100.00 100.00 100.00 77.34 40.62 21.09 4.69 60 QwenLong-L1-32B 100.00 100.00 97.66 57.81 17.19 6.25 3.12 60 QwenLong-L1-32B 100.00 100.00 96.09 53.12 6.25 3.91 2.34 60
Qwen2.5-Instruct-14B-1M 100.00 100.00 100.00 99.22 99.22 96.88 67.97 Qwen2.5-Instruct-14B-1M 100.00 100.00 100.00 98.44 98.44 86.72 13.28 Qwen2.5-Instruct-14B-1M 100.00 98.44 100.00 96.09 99.22 57.03 7.81
Qwen2.5-Instruct-7B-1M 100.00 99.22 96.88 98.44 100.00 96.09 42.97 Qwen2.5-Instruct-7B-1M 99.22 100.00 100.00 100.00 98.44 78.91 3.94 Qwen2.5-Instruct-7B-1M 96.88 93.75 93.75 92.19 78.91 57.81 0.00
DS-Distill-Qwen-32B 100.00 98.44 97.66 68.75 32.81 16.41 5.47 40 DS-Distill-Qwen-32B 100.00 96.88 97.66 47.66 10.94 7.03 0.78 40 DS-Distill-Qwen-32B 100.00 100.00 97.66 46.09 0.78 0.78 0.78 40
DS-Distill-Qwen-14B 100.00 93.75 86.72 57.81 18.75 11.72 3.91 DS-Distill-Qwen-14B 98.44 97.66 86.72 39.06 4.69 1.56 0.00 DS-Distill-Qwen-14B 100.00 96.09 81.25 18.75 0.78 0.00 0.00
DS-Distill-Qwen-7B 56.25 10.94 1.56 0.00 0.00 0.00 0.00 DS-Distill-Qwen-7B 38.28 9.38 0.00 0.00 0.00 0.00 0.00 DS-Distill-Qwen-7B 28.12 1.56 0.00 0.00 0.00 0.00 0.00
Qwen2.5-Instruct-32B 96.88 95.31 92.97 97.66 80.47 46.88 18.75 20 Qwen2.5-Instruct-32B 92.97 83.59 75.78 67.97 60.16 32.03 10.16 20 Qwen2.5-Instruct-32B 94.53 85.94 73.44 80.47 55.47 23.44 15.62 20
Qwen2.5-Instruct-14B 82.81 85.16 91.41 87.50 86.72 46.09 17.97 Qwen2.5-Instruct-14B 84.38 76.56 68.75 67.19 45.31 22.66 10.94 Qwen2.5-Instruct-14B 84.38 71.09 61.72 50.78 21.88 8.59 7.03
Qwen2.5-Instruct-7B 67.19 64.06 67.19 84.38 47.66 31.25 14.84 Qwen2.5-Instruct-7B 83.59 50.00 51.56 72.66 28.91 16.41 3.12 Qwen2.5-Instruct-7B 58.59 57.81 38.28 28.91 13.28 7.03 1.56
8K 16K 32K 64K 128K 256K 512K 0 8K 16K 32K 64K 128K 256K 512K 0 8K 16K 32K 64K 128K 256K 512K 0
RL-MemAgent Long Context Model Backbone RL-MemAgent Long Context Model Backbone RL-MemAgent Long Context Model Backbone
MemAgent w/o RL Reasoning Model MemAgent w/o RL Reasoning Model MemAgent w/o RL Reasoning Model
(a) NIAH Multi-key 1 (b) NIAH Multi-key 2 (c) NIAH Multi-key 3
Figure9 Performance on Multi-keys NIAH tasks with increasing numbers of distractor needles. Tasks 1-3 represent
different levels of difficulty with varying distractor densities.
19
100 100
RL-MemAgent-14B 99.80 98.24 100.00 99.41 99.61 98.24 99.61 RL-MemAgent-14B 95.12 93.95 97.07 96.68 97.46 97.85 98.63
RL-MemAgent-7B 99.22 98.05 96.09 89.45 80.66 71.88 75.39 RL-MemAgent-7B 93.16 84.77 81.25 82.62 77.15 69.73 73.83
MemAgent-32B w/o RL 99.80 97.66 94.73 91.99 91.60 83.98 90.62 MemAgent-32B w/o RL 99.02 94.92 91.21 95.12 92.77 87.89 86.13
80 80
MemAgent-14B w/o RL 99.02 95.51 94.53 89.26 71.68 57.62 41.21 MemAgent-14B w/o RL 95.70 89.84 87.30 74.61 65.43 61.13 46.09
MemAgent-7B w/o RL 77.73 91.41 93.16 89.84 91.41 89.26 87.79 MemAgent-7B w/o RL 89.26 83.98 85.74 89.45 86.33 85.94 78.12
QwenLong-L1-32B 100.00 99.02 98.05 90.04 46.68 22.66 12.11 60 QwenLong-L1-32B 98.63 96.88 92.19 77.15 42.77 22.85 9.57 60
Qwen2.5-Instruct-14B-1M 100.00 100.00 99.80 100.00 99.61 98.63 79.88 Qwen2.5-Instruct-14B-1M 99.22 98.44 98.24 98.44 95.31 93.55 66.41
Qwen2.5-Instruct-7B-1M 98.63 99.61 99.61 99.41 98.24 93.16 52.34 Qwen2.5-Instruct-7B-1M 95.12 87.11 84.38 75.59 71.68 63.09 30.08
DS-Distill-Qwen-32B 99.22 99.61 96.09 86.33 33.01 15.62 7.62 40 DS-Distill-Qwen-32B 97.66 95.90 89.26 75.59 31.64 18.55 7.42 40
DS-Distill-Qwen-14B 97.07 94.92 89.84 71.88 16.80 6.45 2.93 DS-Distill-Qwen-14B 92.58 91.02 78.91 63.48 15.04 7.62 3.71
DS-Distill-Qwen-7B 66.80 12.70 0.20 0.00 0.00 0.00 0.00 DS-Distill-Qwen-7B 74.22 16.80 0.59 0.00 0.00 0.00 0.00
Qwen2.5-Instruct-32B 99.80 99.22 98.44 98.05 90.23 46.29 24.22 20 Qwen2.5-Instruct-32B 95.51 92.58 90.23 88.87 83.01 47.07 22.66 20
Qwen2.5-Instruct-14B 96.29 93.36 91.21 92.77 86.52 43.95 23.24 Qwen2.5-Instruct-14B 91.41 86.52 80.47 78.52 70.31 41.02 22.07
Qwen2.5-Instruct-7B 4.49 4.88 19.34 49.80 45.70 24.80 12.50 Qwen2.5-Instruct-7B 1.76 0.00 0.00 0.39 11.72 14.45 9.77
0 0
8K 16K 32K 64K 128K 256K 512K 8K 16K 32K 64K 128K 256K 512K
RL-MemAgent Long Context Model Backbone RL-MemAgent Long Context Model Backbone
MemAgent w/o RL Reasoning Model MemAgent w/o RL Reasoning Model
(a) NIAH Multi-query (b) NIAH Multi-value
Figure 10 Performance on advanced NIAH variants. (a) Multi-query task requiring retrieval of multiple distinct
needles. (b) Multi-value task requiring extraction of all values sharing identical keys.
B.2 Variable Tracking (VT) and Frequent Words Extraction (FWE)
100 100
RL-MemAgent-14B 90.72 94.84 91.75 92.78 92.00 95.09 94.84 RL-MemAgent-14B 96.72 96.72 99.84 99.84 99.06 99.38 99.22
RL-MemAgent-7B 67.65 77.91 68.32 70.93 69.63 72.77 69.84 RL-MemAgent-7B 73.44 74.38 84.06 85.94 88.59 87.50 85.94
MemAgent-32B w/o RL 92.52 93.01 93.55 93.30 94.33 97.42 94.59 MemAgent-32B w/o RL 99.84 99.84 99.38 98.28 97.81 96.88 96.09
80 80
MemAgent-14B w/o RL 89.94 94.33 91.49 94.07 93.55 95.36 95.61 MemAgent-14B w/o RL 98.75 94.38 95.47 86.41 77.19 64.53 50.78
MemAgent-7B w/o RL 81.69 91.98 84.47 77.42 72.98 68.77 63.39 MemAgent-7B w/o RL 90.16 89.38 85.62 81.56 79.84 72.19 68.05
QwenLong-L1-32B 29.70 30.74 43.58 54.55 42.00 48.26 50.36 60 QwenLong-L1-32B 95.62 88.75 88.75 81.88 64.06 22.81 13.28 60
Qwen2.5-Instruct-14B-1M 93.29 90.46 84.79 89.69 87.09 86.30 84.77 Qwen2.5-Instruct-14B-1M 92.50 85.78 51.88 23.12 20.62 20.00 23.59
Qwen2.5-Instruct-7B-1M 83.75 88.65 85.82 83.23 80.88 72.80 23.09 Qwen2.5-Instruct-7B-1M 29.22 27.34 25.94 25.62 24.53 25.00 19.37
DS-Distill-Qwen-32B 77.98 87.04 79.84 77.50 77.73 75.37 71.75 40 DS-Distill-Qwen-32B 98.75 97.50 97.81 90.16 64.22 28.28 15.78 40
DS-Distill-Qwen-14B 72.27 79.00 79.07 82.17 65.45 69.91 63.14 DS-Distill-Qwen-14B 94.53 98.12 96.41 81.41 38.44 18.44 8.91
DS-Distill-Qwen-7B 44.55 37.26 2.34 0.26 0.00 0.00 0.00 DS-Distill-Qwen-7B 43.13 2.03 1.25 0.00 0.00 0.00 0.00
Qwen2.5-Instruct-32B 93.04 89.95 87.37 85.56 84.52 90.72 89.43 20 Qwen2.5-Instruct-32B 99.53 97.66 97.66 94.84 72.19 32.03 18.91 20
Qwen2.5-Instruct-14B 89.95 86.59 84.27 78.31 78.80 82.67 86.05 Qwen2.5-Instruct-14B 79.84 67.97 52.66 36.56 30.94 17.50 11.09
Qwen2.5-Instruct-7B 78.57 83.48 81.39 76.75 69.97 75.44 72.80 Qwen2.5-Instruct-7B 28.59 27.81 23.59 20.62 21.41 14.84 10.62
0 0
8K 16K 32K 64K 128K 256K 512K 8K 16K 32K 64K 128K 256K 512K
RL-MemAgent Long Context Model Backbone RL-MemAgent Long Context Model Backbone
MemAgent w/o RL Reasoning Model MemAgent w/o RL Reasoning Model
(a) Frequent Words Extraction (b) Variable Tracking
Figure11 Performance on frequent words extraction and variable tracking tasks.
20