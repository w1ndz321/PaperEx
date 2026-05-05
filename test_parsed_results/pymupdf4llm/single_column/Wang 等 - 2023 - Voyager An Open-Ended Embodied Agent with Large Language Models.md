# **VOYAGER: An Open-Ended Embodied Agent with Large Language Models** 

**Guanzhi Wang**[1 2][ �] **, Yuqi Xie**[3] **, Yunfan Jiang**[4] _[∗]_ **, Ajay Mandlekar**[1] _[∗]_ **, Chaowei Xiao**[1 5] **, Yuke Zhu**[1 3] **, Linxi “Jim” Fan**[1] _[†]_[ �] **, Anima Anandkumar**[1 2] _[†]_ 

1NVIDIA, 2Caltech, 3UT Austin, 4Stanford, 5UW Madison 

> _∗_ Equal contribution _†_ Equal advising � Corresponding authors `https://voyager.minedojo.org` 

## **Abstract** 

We introduce VOYAGER, the first LLM-powered embodied lifelong learning agent in Minecraft that continuously explores the world, acquires diverse skills, and makes novel discoveries without human intervention. VOYAGER consists of three key components: 1) an automatic curriculum that maximizes exploration, 2) an ever-growing skill library of executable code for storing and retrieving complex behaviors, and 3) a new iterative prompting mechanism that incorporates environment feedback, execution errors, and self-verification for program improvement. VOYAGER interacts with GPT-4 via blackbox queries, which bypasses the need for model parameter fine-tuning. The skills developed by VOYAGER are temporally extended, interpretable, and compositional, which compounds the agent’s abilities rapidly and alleviates catastrophic forgetting. Empirically, VOYAGER shows strong in-context lifelong learning capability and exhibits exceptional proficiency in playing Minecraft. It obtains 3 _._ 3 _×_ more unique items, travels 2 _._ 3 _×_ longer distances, and unlocks key tech tree milestones up to 15 _._ 3 _×_ faster than prior SOTA. VOYAGER is able to utilize the learned skill library in a new Minecraft world to solve novel tasks from scratch, while other techniques struggle to generalize. 

**==> picture [378 x 221] intentionally omitted <==**

Figure 1: VOYAGER discovers new Minecraft items and skills continually by self-driven exploration, significantly outperforming the baselines. X-axis denotes the number of prompting iterations. 

1 

**==> picture [389 x 168] intentionally omitted <==**

**----- Start of picture text -----**<br>
Automatic Curriculum Iterative Prompting Mechanism Skill Library<br>Mine Wood  Log<br>Make Crafting Table<br>Make Crafting Table Craft Stone Sword<br>New 
 Skill 
 Make Furnace<br>Combat 
 Task Retrieval<br>Zombie Craft Shield<br>Cook Steak<br>     Mine Wood Log Combat Zombie<br>Env Feedback
 Code as  Refine Program<br>Execution Errors Actions<br>Mine Diamond Update 
 Add New Skill<br>Exploration<br>Progress<br>Environment Self-Verification<br>**----- End of picture text -----**<br>


Figure 2: VOYAGER consists of three key components: an automatic curriculum for open-ended exploration, a skill library for increasingly complex behaviors, and an iterative prompting mechanism that uses code as action space. 

## **1 Introduction** 

Building generally capable embodied agents that continuously explore, plan, and develop new skills in open-ended worlds is a grand challenge for the AI community [1–5]. Classical approaches employ reinforcement learning (RL) [6, 7] and imitation learning [8–10] that operate on primitive actions, which could be challenging for systematic exploration [11–15], interpretability [16–18], and generalization [19–21]. Recent advances in large language model (LLM) based agents harness the world knowledge encapsulated in pre-trained LLMs to generate consistent action plans or executable policies [16, 22, 19]. They are applied to embodied tasks like games and robotics [23–27], as well as NLP tasks without embodiment [28–30]. However, these agents are not lifelong learners that can progressively acquire, update, accumulate, and transfer knowledge over extended time spans [31, 32]. 

Let us consider Minecraft as an example. Unlike most other games studied in AI [33, 34, 10], Minecraft does not impose a predefined end goal or a fixed storyline but rather provides a unique playground with endless possibilities [23]. Minecraft requires players to explore vast, procedurally generated 3D terrains and unlock a tech tree using gathered resources. Human players typically start by learning the basics, such as mining wood and cooking food, before advancing to more complex tasks like combating monsters and crafting diamond tools. We argue that an effective lifelong learning agent should have similar capabilities as human players: (1) **propose suitable tasks** based on its current skill level and world state, e.g., learn to harvest sand and cactus before iron if it finds itself in a desert rather than a forest; (2) **refine skills** based on environmental feedback and **commit mastered skills to memory** for future reuse in similar situations (e.g. fighting zombies is similar to fighting spiders); (3) **continually explore the world** and seek out new tasks in a self-driven manner. 

Towards these goals, we introduce VOYAGER, the first _LLM-powered embodied lifelong learning agent_ to drive exploration, master a wide range of skills, and make new discoveries continually without human intervention in Minecraft. VOYAGER is made possible through three key modules (Fig. 2): 1) an **automatic curriculum** that maximizes exploration; 2) a **skill library** for storing and retrieving complex behaviors; and 3) a new **iterative prompting mechanism** that generates executable code for embodied control. We opt to use code as the action space instead of low-level motor commands because programs can naturally represent temporally extended and compositional actions [16, 22], which are essential for many long-horizon tasks in Minecraft. VOYAGER interacts with a blackbox LLM (GPT-4 [35]) through prompting and in-context learning [36–38]. Our approach bypasses the need for model parameter access and explicit gradient-based training or finetuning. 

More specifically, VOYAGER attempts to solve progressively harder tasks proposed by the **automatic curriculum** , which takes into account the exploration progress and the agent’s state. The curriculum is generated by GPT-4 based on the overarching goal of “discovering as many diverse things as possible”. This approach can be perceived as an in-context form of _novelty search_ [39, 40]. VOYAGER incrementally builds a **skill library** by storing the action programs that help solve a task successfully. 

2 

**==> picture [50 x 30] intentionally omitted <==**

**==> picture [51 x 29] intentionally omitted <==**

**==> picture [51 x 29] intentionally omitted <==**

**==> picture [51 x 29] intentionally omitted <==**

**==> picture [51 x 29] intentionally omitted <==**

**==> picture [344 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
Inventory (5/36): {'oak_planks': 3, 'stick':  Reasoning: Since you have a wooden pickaxe and some stones, it would be<br>4, 'crafting_table': 1, 'stone': 3,  GPT-4 beneficial to upgrade your pickaxe to a stone pickaxe for better efficiency.<br>'wooden_pickaxe': 1} Task: Craft 1 stone pickaxe.<br>Biome: river
 Reasoning: Since you have a fishing rod in your inventory and you are near a river<br>Inventory (4/36): {'sugar_cane': 3, 'paper':  GPT-4 biome, it would be a good opportunity to catch some fish for food and experience.<br>3, 'fishing_rod': 1, 'wooden_pickaxe': 1} Task: Catch 1 fish.<br>Nearby entities: pig, cat, villager
 Reasoning: Your hunger is at 0, which means you need to find food to replenish<br>Health: 12/20
 GPT-4 your hunger. Since there are pigs nearby, you can kill one to obtain raw porkchops.<br>Hunger: 0/20 Task: Kill 1 pig.<br>Inventory (6/36): {'furnace': 1,  Reasoning: You have raw iron and coal, and you have a furnace. It's time to smelt<br>'stone_pickaxe': 1, 'oak_planks': 7,  GPT-4 the iron to make iron ingots, which can be used to craft better tools and armor.<br>'crafting_table': 1, 'raw_iron': 4, 'coal': 1}  Task: Smelt 4 raw iron.<br>Time: night
 Reasoning: Since it's night and there's a zombie nearby, it's a good opportunity to<br>Nearby entities: zombie
 GPT-4 try killing the zombie now that you have a stone sword and a shield equipped.<br>Equipment: 'stone_sword', 'shield' Task: Kill 1 zombie.<br>**----- End of picture text -----**<br>


Figure 3: Tasks proposed by the automatic curriculum. We only display the partial prompt for brevity. See Appendix, Sec. A.3 for the full prompt structure. 

Each program is indexed by the embedding of its description, which can be retrieved in similar situations in the future. Complex skills can be synthesized by _composing_ simpler programs, which compounds VOYAGER’s capabilities rapidly over time and alleviates catastrophic forgetting in other continual learning methods [31, 32]. 

However, LLMs struggle to produce the correct action code consistently in one shot [41]. To address this challenge, we propose an **iterative prompting mechanism** that: (1) executes the generated program to obtain observations from the Minecraft simulation (such as inventory listing and nearby creatures) and error trace from the code interpreter (if any); (2) incorporates the feedback into GPT-4’s prompt for another round of code refinement; and (3) repeats the process until a self-verification module confirms the task completion, at which point we commit the program to the skill library (e.g., `craftStoneShovel()` and `combatZombieWithSword()` ) and query the automatic curriculum for the next milestone (Fig. 2). 

Empirically, VOYAGER demonstrates strong **in-context lifelong learning** capabilities. It can construct an ever-growing skill library of action programs that are reusable, interpretable, and generalizable to novel tasks. We evaluate VOYAGER systematically against other LLM-based agent techniques (e.g., ReAct [29], Reflexion [30], AutoGPT [28]) in MineDojo [23], an open-source Minecraft AI framework. VOYAGER outperforms prior SOTA by obtaining 3 _._ 3 _×_ more unique items, unlocking key tech tree milestones up to 15 _._ 3 _×_ faster, and traversing 2 _._ 3 _×_ longer distances. We further demonstrate that VOYAGER is able to utilize the learned skill library in a new Minecraft world to solve novel tasks from scratch, while other methods struggle to generalize. 

## **2 Method** 

VOYAGER consists of three novel components: (1) an automatic curriculum (Sec. 2.1) that suggests objectives for open-ended exploration, (2) a skill library (Sec. 2.2) for developing increasingly complex behaviors, and (3) an iterative prompting mechanism (Sec. 2.3) that generates executable code for embodied control. Full prompts are presented in Appendix, Sec. A. 

## **2.1 Automatic Curriculum** 

Embodied agents encounter a variety of objectives with different complexity levels in open-ended environments. An automatic curriculum offers numerous benefits for open-ended exploration, ensuring a challenging but manageable learning process, fostering curiosity-driven intrinsic motivation for agents to learn and explore, and encouraging the development of general and flexible problemsolving strategies [42–44]. Our automatic curriculum capitalizes on the internet-scale knowledge contained within GPT-4 by prompting it to provide a steady stream of new tasks or challenges. The curriculum unfolds in a bottom-up fashion, allowing for considerable adaptability and responsiveness to the exploration progress and the agent’s current state (Fig. 3). As VOYAGER progresses to harder self-driven goals, it naturally learns a variety of skills, such as “mining a diamond”. 

3 

**==> picture [396 x 185] intentionally omitted <==**

**----- Start of picture text -----**<br>
Program Generated by GPT-4 Program Description Skill Library<br>Mine Wood  Log<br>Make Crafting Table<br>Craft Wooden Pickaxe<br>GPT-3.5 Embedding Key Craft Stone Sword<br>Make Furnace<br>Add ...<br>Combat Cow<br>Cook Steak<br>Value Craft Iron Axe<br>Combat Zombie<br>Task: Craft Iron Pickaxe Top-5 Relevant Skills<br>To craft an iron pickaxe, you  Smelt Iron Ingot<br>How to craft an iron pickaxe in Minecraft? GPT-3.5 need to 3 iron ingots and 2 sticks. Once you have gathered the materials, ....
 Embedding Query Skill Library Retrieve Craft Stick
Make Crafting Table<br>----------------------------------
 Make Furnace<br>         Environment Feedback Craft Wooden Pickaxe<br>**----- End of picture text -----**<br>


Figure 4: Skill library. **Top: Adding a new skill.** Each time GPT-4 generates and verifies a new skill, we add it to the skill library, represented by a vector database. The key is the embedding vector of the program description (generated by GPT-3.5), while the value is the program itself. **Bottom: Skill retrieval.** When faced with a new task proposed by the automatic curriculum, we first leverage GPT-3.5 to generate a general suggestion for solving the task, which is combined with environment feedback as the query context. Subsequently, we perform querying to identify the top-5 relevant skills. 

The input prompt to GPT-4 consists of several components: 

- (1) **Directives encouraging diverse behaviors and imposing constraints** , such as “ `My ultimate goal is to discover as many diverse things as possible ... The next task should not be too hard since I may not have the necessary resources or have learned enough skills to complete it yet.` ”; 

- (2) **The agent’s current state** , including inventory, equipment, nearby blocks and entities, biome, time, health and hunger bars, and position; 

- (3) **Previously completed and failed tasks** , reflecting the agent’s current exploration progress and capabilities frontier; 

- (4) **Additional context** : We also leverage GPT-3.5 to self-ask questions based on the agent’s current state and exploration progress and self-answer questions. We opt to use GPT-3.5 instead of GPT-4 for standard NLP tasks due to budgetary considerations. 

## **2.2 Skill Library** 

With the automatic curriculum consistently proposing increasingly complex tasks, it is essential to have a skill library that serves as a basis for learning and evolution. Inspired by the generality, interpretability, and universality of programs [45], we represent each skill with executable code that scaffolds temporally extended actions for completing a specific task proposed by the automatic curriculum. 

The input prompt to GPT-4 consists of the following components: 

- (1) **Guidelines for code generation** , such as “ `Your function will be reused for building more complex functions. Therefore, you should make it generic and reusable.` ”; 

- (2) **Control primitive APIs, and relevant skills** retrieved from the skill library, which are crucial for in-context learning [36–38] to work well; 

- (3) **The generated code from the last round, environment feedback, execution errors, and critique** , based on which GPT-4 can self-improve (Sec. 2.3); 

- (4) **The agent’s current state** , including inventory, equipment, nearby blocks and entities, biome, time, health and hunger bars, and position; 

4 

**==> picture [396 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>
Environment Feedback Execution Error<br>throw new Error(`No item named ${name}`);<br>I cannot make stick because I need:  2 more planks<br>No item named acacia_axe<br>I cannot make stone_shovel because I need:  2 more stick<br>at line 18:await craftItem(bot, "acacia_axe", 1);<br>GPT-4 GPT-4<br>**----- End of picture text -----**<br>


Figure 5: **Left: Environment feedback.** GPT-4 realizes it needs 2 more planks before crafting sticks. **Right: Execution error.** GPT-4 realizes it should craft a wooden axe instead of an acacia axe since there is no acacia axe in Minecraft. We only display the partial prompt for brevity. The full prompt structure for code generation is in Appendix, Sec. A.4. 

## (5) **Chain-of-thought prompting** [46] to do reasoning before code generation. 

We iteratively refine the program through a novel iterative prompting mechanism (Sec. 2.3), incorporate it into the skill library as a new skill, and index it by the embedding of its description (Fig. 4, top). For skill retrieval, we query the skill library with the embedding of self-generated task plans and environment feedback (Fig. 4, bottom). By continuously expanding and refining the skill library, VOYAGER can learn, adapt, and excel in a wide spectrum of tasks, consistently pushing the boundaries of its capabilities in the open world. 

## **2.3 Iterative Prompting Mechanism** 

We introduce an iterative prompting mechanism for self-improvement through three types of feedback: 

- (1) **Environment feedback** , which illustrates the intermediate progress of program execution (Fig. 5, left). For example, “ `I cannot make an iron chestplate because I need: 7 more iron ingots` ” highlights the cause of failure in crafting an iron chestplate. We use `bot.chat()` inside control primitive APIs to generate environment feedback and prompt GPT-4 to use this function as well during code generation; 

- (2) **Execution errors** from the program interpreter that reveal any invalid operations or syntax errors in programs, which are valuable for bug fixing (Fig. 5, right); 

- (3) **Self-verification for checking task success.** Instead of manually coding success checkers for each new task proposed by the automatic curriculum, we instantiate another GPT-4 agent for self-verification. By providing VOYAGER’s current state and the task to GPT-4, we ask it to act as a critic [47–49] and inform us whether the program achieves the task. In addition, if the task fails, it provides a critique by suggesting how to complete the task (Fig. 6). Hence, our self-verification is more comprehensive than self-reflection [30] by both checking success and reflecting on mistakes. 

During each round of code generation, we execute the generated program to obtain environment feedback and execution errors from the code interpreter, which are incorporated into GPT-4’s prompt for the next round of code refinement. This iterative process repeats until self-verification validates 

5 

**==> picture [396 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
Inventory (8/36): {'oak_planks': 5, 'cobblestone': 2,<br>Reasoning: Mining coal_ore in Minecraft will get coal. You have 5 coal in your<br>'porkchop': 2, 'wooden_sword': 1, 'coal': 5, 'wooden_pickaxe':  GPT-4 inventory.<br>1, 'oak_log': 3, 'dirt': 9}
 Success: True<br>Task: Mine 5 coal ores<br>Inventory (10/36): {'raw_copper': 9, 'copper_ingot': 3,  Reasoning: To craft a spyglass, you need 2 copper ingots and 1 amethyst shard.<br>'acacia_planks': 1, 'raw_iron': 1, 'stick': 1, 'iron_sword': 1,  GPT-4 You have 3 copper ingots, but you don't have any amethyst shards.<br>'iron_pickaxe': 1, 'iron_ingot': 3, 'crafting_table': 1, 'furnace': 1}
 Success: False<br>Task: Craft a spyglass Critique: Find and mine an amethyst shard underground.<br>Inventory (7/36): {'oak_log': 5, 'oak_planks': 1,  Reasoning: You have 2 white_wool and 6 mutton in your inventory, which indicates<br>'wooden_pickaxe': 1, 'wooden_sword': 1, 'porkchop': 2,  GPT-4 that you killed 2 sheep. You needed to kill 3 sheep.<br>'white_wool': 2, 'mutton': 6}
 Success: False<br>Task: Kill 3 sheep Critique: Find and kill one more sheep to complete the task.<br>Inventory (9/36): {'string': 4, 'coal': 1, 'rotten_flesh': 1,<br>'iron_sword': 1, 'furnace': 1, 'dirt': 6, 'stone_shovel': 1,  GPT-4 Reasoning: You have 1 rotten_flesh in your inventory, which means you have killed at least 1 zombie.<br>'wooden_pickaxe': 1, 'granite': 5}<br>Success: True<br>Task: Kill 1 zombie<br>**----- End of picture text -----**<br>


Figure 6: Self-verification examples. We only display the partial prompt for brevity. See Appendix, Sec. A.5 for the full prompt structure. 

the task’s completion, at which point we add this new skill to the skill library and ask the automatic curriculum for a new objective (Fig. 2). If the agent gets stuck after 4 rounds of code generation, then we query the curriculum for another task. This iterative prompting approach significantly improves program synthesis for embodied control, enabling VOYAGER to continuously acquire diverse skills without human intervention. 

## **3 Experiments** 

## **3.1 Experimental Setup** 

We leverage OpenAI’s `gpt-4-0314` [35] and `gpt-3.5-turbo-0301` [50] APIs for text completion, along with `text-embedding-ada-002` [51] API for text embedding. We set all temperatures to 0 except for the automatic curriculum, which uses temperature = 0.1 to encourage task diversity. Our simulation environment is built on top of MineDojo [23] and leverages Mineflayer [52] JavaScript APIs for motor controls. See Appendix, Sec. B.1 for more details. 

## **3.2 Baselines** 

Because there is no LLM-based agents that work out of the box for Minecraft, we make our best effort to select a number of representative algorithms as baselines. These methods are originally designed only for NLP tasks without embodiment, therefore we have to re-interpret them to be executable in MineDojo and compatible with our experimental setting: 

**ReAct** [29] uses chain-of-thought prompting [46] by generating both reasoning traces and action plans with LLMs. We provide it with our environment feedback and the agent states as observations. 

**Reflexion** [30] is built on top of ReAct [29] with self-reflection to infer more intuitive future actions. We provide it with execution errors and our self-verification module. 

**AutoGPT** [28] is a popular software tool that automates NLP tasks by decomposing a high-level goal into multiple subgoals and executing them in a ReAct-style loop. We re-implement AutoGPT by using GPT-4 to do task decomposition and provide it with the agent states, environment feedback, and execution errors as observations for subgoal execution. Compared with VOYAGER, AutoGPT lacks the skill library for accumulating knowledge, self-verification for assessing task success, and automatic curriculum for open-ended exploration. 

Note that we do not directly compare with prior methods that take Minecraft screen pixels as input and output low-level controls [53–55]. It would not be an apple-to-apple comparison, because we rely on the high-level Mineflayer [52] API to control the agent. Our work’s focus is on pushing the limits of GPT-4 for lifelong embodied agent learning, rather than solving the 3D perception or sensorimotor control problems. VOYAGER is orthogonal and can be combined with gradient-based approaches like 

6 

Table 1: Tech tree mastery. Fractions indicate the number of successful trials out of three total runs. 0/3 means the method fails to unlock a level of the tech tree within the maximal prompting iterations (160). Numbers are prompting iterations averaged over three trials. The fewer the iterations, the more efficient the method. 

|Method|Wooden Tool<br>Stone Tool<br>Iron Tool<br>Diamond Tool|
|---|---|
|ReAct [29]<br>Refexion [30]<br>AutoGPT [28]<br>VOYAGERw/o Skill Library<br>VOYAGER(Ours)|N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>92_±_72(**3**_/_**3**)<br>94_±_72(**3**_/_**3**)<br>135_±_103(**3**_/_**3**)<br>N/A(0_/_3)<br>**7**_±_**2**(**3**_/_**3**)<br>**9**_±_**4**(**3**_/_**3**)<br>29_±_11(**3**_/_**3**)<br>N/A(0_/_3)<br>**6**_±_**2**(**3**_/_**3**)<br>**11**_±_**2**(**3**_/_**3**)<br>**21**_±_**7**(**3**_/_**3**)<br>**102**(**1**_/_**3**)|



**==> picture [318 x 171] intentionally omitted <==**

Figure 7: Map coverage: bird’s eye views of Minecraft maps. VOYAGER is able to traverse 2 _._ 3 _×_ longer distances compared to baselines while crossing diverse terrains. 

VPT [8] as long as the controller provides a code API. We make a system-level comparison between VOYAGER and prior Minecraft agents in Table. A.2. 

## **3.3 Evaluation Results** 

We systematically evaluate VOYAGER and baselines on their exploration performance, tech tree mastery, map coverage, and zero-shot generalization capability to novel tasks in a new world. 

**Significantly better exploration.** Results of exploration performance are shown in Fig. 1. VOYAGER’s superiority is evident in its ability to consistently make new strides, discovering 63 unique items within 160 prompting iterations, 3 _._ 3 _×_ many novel items compared to its counterparts. On the other hand, AutoGPT lags considerably in discovering new items, while ReAct and Reflexion struggle to make significant progress, given the abstract nature of the open-ended exploration goal that is challenging to execute without an appropriate curriculum. 

**Consistent tech tree mastery.** The Minecraft tech tree tests the agent’s ability to craft and use a hierarchy of tools. Progressing through this tree (wooden tool _→_ stone tool _→_ iron tool _→_ diamond tool) requires the agent to master systematic and compositional skills. Compared with baselines, VOYAGER unlocks the wooden level 15 _._ 3 _×_ faster (in terms of the prompting iterations), the stone level 8 _._ 5 _×_ faster, the iron level 6 _._ 4 _×_ faster, and VOYAGER is the only one to unlock the diamond level of the tech tree (Fig. 2 and Table. 1). This underscores the effectiveness of the automatic curriculum, which consistently presents challenges of suitable complexity to facilitate the agent’s progress. 

**Extensive map traversal.** VOYAGER is able to navigate distances 2 _._ 3 _×_ longer compared to baselines by traversing a variety of terrains, while the baseline agents often find themselves confined to local areas, which significantly hampers their capacity to discover new knowledge (Fig. 7). 

7 

Table 2: Zero-shot generalization to unseen tasks. Fractions indicate the number of successful trials out of three total attempts. 0/3 means the method fails to solve the task within the maximal prompting iterations (50). Numbers are prompting iterations averaged over three trials. The fewer the iterations, the more efficient the method. 

|Method|Diamond Pickaxe<br>Golden Sword<br>Lava Bucket<br>Compass|
|---|---|
|ReAct [29]<br>Refexion [30]<br>AutoGPT [28]<br>AutoGPT [28] w/ Our Skill Library<br>VOYAGERw/o Skill Library<br>VOYAGER(Ours)|N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>N/A(0_/_3)<br>39(1_/_3)<br>30(1_/_3)<br>N/A(0_/_3)<br>30(2_/_3)<br>36(2_/_3)<br>30_±_9(**3**_/_**3**)<br>27_±_9(**3**_/_**3**)<br>26_±_3(**3**_/_**3**)<br>**19**_±_**3**(**3**_/_**3**)<br>**18**_±_**7**(**3**_/_**3**)<br>**21**_±_**5**(**3**_/_**3**)<br>**18**_±_**2**(**3**_/_**3**)|



**==> picture [396 x 143] intentionally omitted <==**

Figure 8: Zero-shot generalization to unseen tasks. We visualize the intermediate progress of each method on two tasks. See Appendix, Sec. B.4.3 for the other two tasks. We do not plot ReAct and Reflexion since they do not make any meaningful progress. 

**Efficient zero-shot generalization to unseen tasks.** To evaluate zero-shot generalization, we clear the agent’s inventory, reset it to a newly instantiated world, and test it with unseen tasks. For both VOYAGER and AutoGPT, we utilize GPT-4 to break down the task into a series of subgoals. Table. 2 and Fig. 8 show VOYAGER can consistently solve all the tasks, while baselines cannot solve any task within 50 prompting iterations. What’s interesting to note is that our skill library constructed from lifelong learning not only enhances VOYAGER’s performance but also gives a boost to AutoGPT. This demonstrates that the skill library serves as a versatile tool that can be readily employed by other methods, effectively acting as a plug-and-play asset to enhance performance. 

## **3.4 Ablation Studies** 

We ablate 6 design choices (automatic curriculum, skill library, environment feedback, execution errors, self-verification, and GPT-4 for code generation) in VOYAGER and study their impact on exploration performance (see Appendix, Sec. B.3 for details of each ablated variant). Results are shown in Fig. 9. We highlight the key findings below: 

- **Automatic curriculum is crucial for the agent’s consistent progress.** The discovered item count drops by 93% if the curriculum is replaced with a random one, because certain tasks may be too challenging if attempted out of order. On the other hand, a manually designed curriculum requires significant Minecraft-specific expertise, and does not take into account the agent’s live situation. It falls short in the experimental results compared to our automatic curriculum. 

- **VOYAGER w/o skill library exhibits a tendency to plateau in the later stages.** This underscores the pivotal role that the skill library plays in VOYAGER. It helps create more complex actions and steadily pushes the agent’s boundaries by encouraging new skills to be built upon older ones. 

8 

**==> picture [318 x 142] intentionally omitted <==**

Figure 9: **Left: Ablation studies for the automatic curriculum, skill library, and GPT-4.** GPT-3.5 means replacing GPT-4 with GPT-3.5 for code generation. VOYAGER outperforms all the alternatives, demonstrating the critical role of each component. **Right: Ablation studies for the iterative prompting mechanism.** VOYAGER surpasses all the other options, thereby highlighting the essential significance of each type of feedback in the iterative prompting mechanism. 

**==> picture [397 x 97] intentionally omitted <==**

Figure 10: VOYAGER builds 3D structures with human feedback. The progress of building designs that integrate human input is demonstrated from left to right. 

- **Self-verification is the most important among all the feedback types** . Removing the module leads to a significant drop ( _−_ 73%) in the discovered item count. Self-verification serves as a critical mechanism to decide when to move on to a new task or reattempt a previously unsuccessful task. 

- **GPT-4 significantly outperforms GPT-3.5 in code generation** and obtains 5 _._ 7 _×_ more unique items, as GPT-4 exhibits a quantum leap in coding abilities. This finding corroborates recent studies in the literature [56, 57]. 

## **3.5 Multimodal Feedback from Humans** 

VOYAGER does not currently support visual perception, because the available version of GPT-4 API is text-only at the time of this writing. However, VOYAGER has the potential to be augmented by multimodal perception models [58, 59] to achieve more impressive tasks. We demonstrate that given human feedback, VOYAGER is able to construct complex 3D structures in Minecraft, such as a Nether Portal and a house (Fig. 10). There are two ways to integrate human feedback: 

- (1) Human as a critic (equivalent to VOYAGER’s self-verification module): humans provide visual critique to VOYAGER, allowing it to modify the code from the previous round. This feedback is essential for correcting certain errors in the spatial details of a 3D structure that VOYAGER cannot perceive directly. 

- (2) Human as a curriculum (equivalent to VOYAGER’s automatic curriculum module): humans break down a complex building task into smaller steps, guiding VOYAGER to complete them incrementally. This approach improves VOYAGER’s ability to handle more sophisticated 3D construction tasks. 

9 

## **4 Limitations and Future Work** 

**Cost.** The GPT-4 API incurs significant costs. It is 15 _×_ more expensive than GPT-3.5. Nevertheless, VOYAGER requires the quantum leap in code generation quality from GPT-4 (Fig. 9), which GPT-3.5 and open-source LLMs cannot provide [60]. 

**Inaccuracies.** Despite the iterative prompting mechanism, there are still cases where the agent gets stuck and fails to generate the correct skill. The automatic curriculum has the flexibility to reattempt this task at a later time. Occasionally, self-verification module may also fail, such as not recognizing spider string as a success signal of beating a spider. 

**Hallucinations.** The automatic curriculum occasionally proposes unachievable tasks. For example, it may ask the agent to craft a “copper sword" or “copper chestplate", which are items that do not exist within the game. Hallucinations also occur during the code generation process. For instance, GPT-4 tends to use cobblestone as a fuel input, despite being an invalid fuel source in the game. Additionally, it may call functions absent in the provided control primitive APIs, leading to code execution errors. 

We are confident that improvements in the GPT API models as well as novel techniques for finetuning open-source LLMs will overcome these limitations in the future. 

## **5 Related work** 

**Decision-making Agents in Minecraft.** Minecraft is an open-ended 3D world with incredibly flexible game mechanics supporting a broad spectrum of activities. Built upon notable Minecraft benchmarks [23, 61–65], Minecraft learning algorithms can be divided into two categories: 1) Low-level controller: Many prior efforts leverage hierarchical reinforcement learning to learn from human demonstrations [66–68]. Kanitscheider et al. [14] design a curriculum based on success rates, but its objectives are limited to curated items. MineDojo [23] and VPT [8] utilize YouTube videos for large-scale pre-training. DreamerV3 [69], on the other hand, learns a world model to explore the environment and collect diamonds. 2) High-level planner: Volum et al. [70] leverage few-shot prompting with Codex [41] to generate executable policies, but they require additional human interaction. Recent works leverage LLMs as a high-level planner in Minecraft by decomposing a high-level task into several subgoals following Minecraft recipes [55, 53, 71], thus lacking full exploration flexibility. Like these latter works, VOYAGER also uses LLMs as a high-level planner by prompting GPT-4 and utilizes Mineflayer [52] as a low-level controller following Volum et al. [70]. Unlike prior works, VOYAGER employs an automatic curriculum that unfolds in a bottom-up manner, driven by curiosity, and therefore enables open-ended exploration. 

**Large Language Models for Agent Planning.** Inspired by the strong emergent capabilities of LLMs, such as zero-shot prompting and complex reasoning [72, 37, 38, 36, 73, 74], embodied agent research [75–78] has witnessed a significant increase in the utilization of LLMs for planning purposes. Recent efforts can be roughly classified into two groups. 1) Large language models for robot learning: Many prior works apply LLMs to generate subgoals for robot planning [27, 27, 25, 79, 80]. Inner Monologue [26] incorporates environment feedback for robot planning with LLMs. Code as Policies [16] and ProgPrompt [22] directly leverage LLMs to generate executable robot policies. VIMA [19] and PaLM-E [59] fine-tune pre-trained LLMs to support multimodal prompts. 2) Large language models for text agents: ReAct [29] leverages chain-of-thought prompting [46] and generates both reasoning traces and task-specific actions with LLMs. Reflexion [30] is built upon ReAct [29] with self-reflection to enhance reasoning. AutoGPT [28] is a popular tool that automates NLP tasks by crafting a curriculum of multiple subgoals for completing a high-level goal while incorporating ReAct [29]’s reasoning and acting loops. DERA [81] frames a task as a dialogue between two GPT-4 [35] agents. Generative Agents [82] leverages ChatGPT [50] to simulate human behaviors by storing agents’ experiences as memories and retrieving those for planning, but its agent actions are not executable. SPRING [83] is a concurrent work that uses GPT-4 to extract game mechanics from game manuals, based on which it answers questions arranged in a directed acyclic graph and predicts the next action. All these works lack a skill library for developing more complex behaviors, which are crucial components for the success of VOYAGER in lifelong learning. 

**Code Generation with Execution.** Code generation has been a longstanding challenge in NLP [41, 84, 85, 73, 37], with various works leveraging execution results to improve program 

10 

synthesis. Execution-guided approaches leverage intermediate execution outcomes to guide program search [86–88]. Another line of research utilizes majority voting to choose candidates based on their execution performance [89, 90]. Additionally, LEVER [91] trains a verifier to distinguish and reject incorrect programs based on execution results. CLAIRIFY [92], on the other hand, generates code for planning chemistry experiments and makes use of a rule-based verifier to iteratively provide error feedback to LLMs. VOYAGER distinguishes itself from these works by integrating environment feedback, execution errors, and self-verification (to assess task success) into an iterative prompting mechanism for embodied control. 

## **6 Conclusion** 

In this work, we introduce VOYAGER, the first LLM-powered embodied lifelong learning agent, which leverages GPT-4 to explore the world continuously, develop increasingly sophisticated skills, and make new discoveries consistently without human intervention. VOYAGER exhibits superior performance in discovering novel items, unlocking the Minecraft tech tree, traversing diverse terrains, and applying its learned skill library to unseen tasks in a newly instantiated world. VOYAGER serves as a starting point to develop powerful generalist agents without tuning the model parameters. 

## **7 Broader Impacts** 

Our research is conducted within Minecraft, a safe and harmless 3D video game environment. While VOYAGER is designed to be generally applicable to other domains, such as robotics, its application to physical robots would require additional attention and the implementation of safety constraints by humans to ensure responsible and secure deployment. 

## **8 Acknowledgements** 

We are extremely grateful to Ziming Zhu, Kaiyu Yang, Rafał Kocielnik, Colin White, Or Sharir, Sahin Lale, De-An Huang, Jean Kossaifi, Yuncong Yang, Charles Zhang, Minchao Huang, and many other colleagues and friends for their helpful feedback and insightful discussions. This work is done during Guanzhi Wang’s internship at NVIDIA. Guanzhi Wang is supported by the Kortschak fellowship in Computing and Mathematical Sciences at Caltech. 

## **References** 

- [1] Eric Kolve, Roozbeh Mottaghi, Winson Han, Eli VanderBilt, Luca Weihs, Alvaro Herrasti, Daniel Gordon, Yuke Zhu, Abhinav Gupta, and Ali Farhadi. Ai2-thor: An interactive 3d environment for visual ai. _arXiv preprint arXiv: Arxiv-1712.05474_ , 2017. 

- [2] Manolis Savva, Jitendra Malik, Devi Parikh, Dhruv Batra, Abhishek Kadian, Oleksandr Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, and Vladlen Koltun. Habitat: A platform for embodied AI research. In _2019 IEEE/CVF International Conference on Computer Vision, ICCV 2019, Seoul, Korea (South), October 27 - November 2, 2019_ , pages 9338–9346. IEEE, 2019. 

- [3] Yuke Zhu, Josiah Wong, Ajay Mandlekar, and Roberto Martín-Martín. robosuite: A modular simulation framework and benchmark for robot learning. _arXiv preprint arXiv: Arxiv2009.12293_ , 2020. 

- [4] Fei Xia, William B. Shen, Chengshu Li, Priya Kasimbeg, Micael Tchapmi, Alexander Toshev, Li Fei-Fei, Roberto Martín-Martín, and Silvio Savarese. Interactive gibson benchmark (igibson 0.5): A benchmark for interactive navigation in cluttered environments. _arXiv preprint arXiv: Arxiv-1910.14442_ , 2019. 

- [5] Bokui Shen, Fei Xia, Chengshu Li, Roberto Martín-Martín, Linxi Fan, Guanzhi Wang, Claudia Pérez-D’Arpino, Shyamal Buch, Sanjana Srivastava, Lyne P. Tchapmi, Micael E. Tchapmi, Kent Vainio, Josiah Wong, Li Fei-Fei, and Silvio Savarese. igibson 1.0: a simulation environment for interactive tasks in large realistic scenes. _arXiv preprint arXiv: Arxiv-2012.02924_ , 2020. 

11 

- [6] Jens Kober, J Andrew Bagnell, and Jan Peters. Reinforcement learning in robotics: A survey. _The International Journal of Robotics Research_ , 32(11):1238–1274, 2013. 

- [7] Kai Arulkumaran, Marc Peter Deisenroth, Miles Brundage, and Anil Anthony Bharath. Deep reinforcement learning: A brief survey. _IEEE Signal Processing Magazine_ , 34(6):26–38, 2017. 

- [8] Bowen Baker, Ilge Akkaya, Peter Zhokhov, Joost Huizinga, Jie Tang, Adrien Ecoffet, Brandon Houghton, Raul Sampedro, and Jeff Clune. Video pretraining (vpt): Learning to act by watching unlabeled online videos. _arXiv preprint arXiv: Arxiv-2206.11795_ , 2022. 

- [9] DeepMind Interactive Agents Team, Josh Abramson, Arun Ahuja, Arthur Brussee, Federico Carnevale, Mary Cassin, Felix Fischer, Petko Georgiev, Alex Goldin, Mansi Gupta, Tim Harley, Felix Hill, Peter C Humphreys, Alden Hung, Jessica Landon, Timothy Lillicrap, Hamza Merzic, Alistair Muldal, Adam Santoro, Guy Scully, Tamara von Glehn, Greg Wayne, Nathaniel Wong, Chen Yan, and Rui Zhu. Creating multimodal interactive agents with imitation and self-supervised learning. _arXiv preprint arXiv: Arxiv-2112.03763_ , 2021. 

- [10] Oriol Vinyals, Igor Babuschkin, Junyoung Chung, Michael Mathieu, Max Jaderberg, Wojciech M Czarnecki, Andrew Dudzik, Aja Huang, Petko Georgiev, Richard Powell, et al. Alphastar: Mastering the real-time strategy game starcraft ii. _DeepMind blog_ , 2, 2019. 

- [11] Adrien Ecoffet, Joost Huizinga, Joel Lehman, Kenneth O. Stanley, and Jeff Clune. Go-explore: a new approach for hard-exploration problems. _arXiv preprint arXiv: Arxiv-1901.10995_ , 2019. 

- [12] Joost Huizinga and Jeff Clune. Evolving multimodal robot behavior via many stepping stones with the combinatorial multiobjective evolutionary algorithm. _Evolutionary computation_ , 30(2):131–164, 2022. 

- [13] Rui Wang, Joel Lehman, Aditya Rawal, Jiale Zhi, Yulun Li, Jeffrey Clune, and Kenneth O. Stanley. Enhanced POET: open-ended reinforcement learning through unbounded invention of learning challenges and their solutions. In _Proceedings of the 37th International Conference on Machine Learning, ICML 2020, 13-18 July 2020, Virtual Event_ , volume 119 of _Proceedings of Machine Learning Research_ , pages 9940–9951. PMLR, 2020. 

- [14] Ingmar Kanitscheider, Joost Huizinga, David Farhi, William Hebgen Guss, Brandon Houghton, Raul Sampedro, Peter Zhokhov, Bowen Baker, Adrien Ecoffet, Jie Tang, Oleg Klimov, and Jeff Clune. Multi-task curriculum learning in a complex, visual, hard-exploration domain: Minecraft. _arXiv preprint arXiv: Arxiv-2106.14876_ , 2021. 

- [15] Michael Dennis, Natasha Jaques, Eugene Vinitsky, Alexandre M. Bayen, Stuart Russell, Andrew Critch, and Sergey Levine. Emergent complexity and zero-shot transfer via unsupervised environment design. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, _Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual_ , 2020. 

- [16] Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. Code as policies: Language model programs for embodied control. _arXiv preprint arXiv: Arxiv-2209.07753_ , 2022. 

- [17] Shao-Hua Sun, Te-Lin Wu, and Joseph J. Lim. Program guided agent. In _8th International Conference on Learning Representations, ICLR 2020, Addis Ababa, Ethiopia, April 26-30, 2020_ . OpenReview.net, 2020. 

- [18] Zelin Zhao, Karan Samel, Binghong Chen, and Le Song. Proto: Program-guided transformer for program-guided tasks. In Marc’Aurelio Ranzato, Alina Beygelzimer, Yann N. Dauphin, Percy Liang, and Jennifer Wortman Vaughan, editors, _Advances in Neural Information Processing Systems 34: Annual Conference on Neural Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual_ , pages 17021–17036, 2021. 

- [19] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen, Li Fei-Fei, Anima Anandkumar, Yuke Zhu, and Linxi (Jim) Fan. Vima: General robot manipulation with multimodal prompts. _ARXIV.ORG_ , 2022. 

12 

- [20] Mohit Shridhar, Lucas Manuelli, and Dieter Fox. Cliport: What and where pathways for robotic manipulation. _arXiv preprint arXiv: Arxiv-2109.12098_ , 2021. 

- [21] Linxi Fan, Guanzhi Wang, De-An Huang, Zhiding Yu, Li Fei-Fei, Yuke Zhu, and Animashree Anandkumar. SECANT: self-expert cloning for zero-shot generalization of visual policies. In Marina Meila and Tong Zhang, editors, _Proceedings of the 38th International Conference on Machine Learning, ICML 2021, 18-24 July 2021, Virtual Event_ , volume 139 of _Proceedings of Machine Learning Research_ , pages 3088–3099. PMLR, 2021. 

- [22] Ishika Singh, Valts Blukis, Arsalan Mousavian, Ankit Goyal, Danfei Xu, Jonathan Tremblay, Dieter Fox, Jesse Thomason, and Animesh Garg. Progprompt: Generating situated robot task plans using large language models. _arXiv preprint arXiv: Arxiv-2209.11302_ , 2022. 

- [23] Linxi Fan, Guanzhi Wang, Yunfan Jiang, Ajay Mandlekar, Yuncong Yang, Haoyi Zhu, Andrew Tang, De-An Huang, Yuke Zhu, and Anima Anandkumar. Minedojo: Building open-ended embodied agents with internet-scale knowledge. _arXiv preprint arXiv: Arxiv-2206.08853_ , 2022. 

- [24] Andy Zeng, Adrian Wong, Stefan Welker, Krzysztof Choromanski, Federico Tombari, Aveek Purohit, Michael Ryoo, Vikas Sindhwani, Johnny Lee, Vincent Vanhoucke, and Pete Florence. Socratic models: Composing zero-shot multimodal reasoning with language. _arXiv preprint arXiv: Arxiv-2204.00598_ , 2022. 

- [25] Michael Ahn, Anthony Brohan, Noah Brown, Yevgen Chebotar, Omar Cortes, Byron David, Chelsea Finn, Keerthana Gopalakrishnan, Karol Hausman, Alex Herzog, Daniel Ho, Jasmine Hsu, Julian Ibarz, Brian Ichter, Alex Irpan, Eric Jang, Rosario Jauregui Ruano, Kyle Jeffrey, Sally Jesmonth, Nikhil J Joshi, Ryan Julian, Dmitry Kalashnikov, Yuheng Kuang, Kuang-Huei Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao, Kanishka Rao, Jarek Rettinghouse, Diego Reyes, Pierre Sermanet, Nicolas Sievers, Clayton Tan, Alexander Toshev, Vincent Vanhoucke, Fei Xia, Ted Xiao, Peng Xu, Sichun Xu, and Mengyuan Yan. Do as i can, not as i say: Grounding language in robotic affordances. _arXiv preprint arXiv: Arxiv-2204.01691_ , 2022. 

- [26] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng, Jonathan Tompson, Igor Mordatch, Yevgen Chebotar, Pierre Sermanet, Noah Brown, Tomas Jackson, Linda Luu, Sergey Levine, Karol Hausman, and Brian Ichter. Inner monologue: Embodied reasoning through planning with language models. _arXiv preprint arXiv: Arxiv2207.05608_ , 2022. 

- [27] Wenlong Huang, Pieter Abbeel, Deepak Pathak, and Igor Mordatch. Language models as zeroshot planners: Extracting actionable knowledge for embodied agents. In Kamalika Chaudhuri, Stefanie Jegelka, Le Song, Csaba Szepesvári, Gang Niu, and Sivan Sabato, editors, _International Conference on Machine Learning, ICML 2022, 17-23 July 2022, Baltimore, Maryland, USA_ , volume 162 of _Proceedings of Machine Learning Research_ , pages 9118–9147. PMLR, 2022. 

- [28] Significant-gravitas/auto-gpt: An experimental open-source attempt to make gpt-4 fully autonomous., 2023. 

- [29] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan, and Yuan Cao. React: Synergizing reasoning and acting in language models. _arXiv preprint arXiv: Arxiv-2210.03629_ , 2022. 

- [30] Noah Shinn, Beck Labash, and Ashwin Gopinath. Reflexion: an autonomous agent with dynamic memory and self-reflection. _arXiv preprint arXiv: Arxiv-2303.11366_ , 2023. 

- [31] German Ignacio Parisi, Ronald Kemker, Jose L. Part, Christopher Kanan, and Stefan Wermter. Continual lifelong learning with neural networks: A review. _Neural Networks_ , 113:54–71, 2019. 

- [32] Liyuan Wang, Xingxing Zhang, Hang Su, and Jun Zhu. A comprehensive survey of continual learning: Theory, method and application. _arXiv preprint arXiv: Arxiv-2302.00487_ , 2023. 

- [33] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Alex Graves, Ioannis Antonoglou, Daan Wierstra, and Martin Riedmiller. Playing atari with deep reinforcement learning. _arXiv preprint arXiv: Arxiv-1312.5602_ , 2013. 

13 

- [34] OpenAI, :, Christopher Berner, Greg Brockman, Brooke Chan, Vicki Cheung, Przemysław D˛ebiak, Christy Dennison, David Farhi, Quirin Fischer, Shariq Hashme, Chris Hesse, Rafal Józefowicz, Scott Gray, Catherine Olsson, Jakub Pachocki, Michael Petrov, Henrique P. d. O. Pinto, Jonathan Raiman, Tim Salimans, Jeremy Schlatter, Jonas Schneider, Szymon Sidor, Ilya Sutskever, Jie Tang, Filip Wolski, and Susan Zhang. Dota 2 with large scale deep reinforcement learning. _arXiv preprint arXiv: Arxiv-1912.06680_ , 2019. 

- [35] OpenAI. Gpt-4 technical report. _arXiv preprint arXiv: Arxiv-2303.08774_ , 2023. 

- [36] Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, Ed H. Chi, Tatsunori Hashimoto, Oriol Vinyals, Percy Liang, Jeff Dean, and William Fedus. Emergent abilities of large language models. _arXiv preprint arXiv: Arxiv-2206.07682_ , 2022. 

- [37] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In Hugo Larochelle, Marc’Aurelio Ranzato, Raia Hadsell, Maria-Florina Balcan, and Hsuan-Tien Lin, editors, _Advances in Neural Information Processing Systems 33: Annual Conference on Neural Information Processing Systems 2020, NeurIPS 2020, December 6-12, 2020, virtual_ , 2020. 

- [38] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. _J. Mach. Learn. Res._ , 21:140:1–140:67, 2020. 

- [39] Benjamin Eysenbach, Abhishek Gupta, Julian Ibarz, and Sergey Levine. Diversity is all you need: Learning skills without a reward function. In _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net, 2019. 

- [40] Edoardo Conti, Vashisht Madhavan, Felipe Petroski Such, Joel Lehman, Kenneth O. Stanley, and Jeff Clune. Improving exploration in evolution strategies for deep reinforcement learning via a population of novelty-seeking agents. In Samy Bengio, Hanna M. Wallach, Hugo Larochelle, Kristen Grauman, Nicolò Cesa-Bianchi, and Roman Garnett, editors, _Advances in Neural Information Processing Systems 31: Annual Conference on Neural Information Processing Systems 2018, NeurIPS 2018, December 3-8, 2018, Montréal, Canada_ , pages 5032–5043, 2018. 

- [41] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating large language models trained on code. _arXiv preprint arXiv: Arxiv2107.03374_ , 2021. 

- [42] Rui Wang, Joel Lehman, Jeff Clune, and Kenneth O. Stanley. Paired open-ended trailblazer (poet): Endlessly generating increasingly complex and diverse learning environments and their solutions. _arXiv preprint arXiv: Arxiv-1901.01753_ , 2019. 

- [43] Rémy Portelas, Cédric Colas, Lilian Weng, Katja Hofmann, and Pierre-Yves Oudeyer. Automatic curriculum learning for deep RL: A short survey. In Christian Bessiere, editor, _Proceedings of the Twenty-Ninth International Joint Conference on Artificial Intelligence, IJCAI 2020_ , pages 4819–4825. ijcai.org, 2020. 

14 

- [44] Sébastien Forestier, Rémy Portelas, Yoan Mollard, and Pierre-Yves Oudeyer. Intrinsically motivated goal exploration processes with automatic curriculum learning. _The Journal of Machine Learning Research_ , 23(1):6818–6858, 2022. 

- [45] Kevin Ellis, Catherine Wong, Maxwell Nye, Mathias Sable-Meyer, Luc Cary, Lucas Morales, Luke Hewitt, Armando Solar-Lezama, and Joshua B. Tenenbaum. Dreamcoder: Growing generalizable, interpretable knowledge with wake-sleep bayesian program learning. _arXiv preprint arXiv: Arxiv-2006.08381_ , 2020. 

- [46] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and Denny Zhou. Chain of thought prompting elicits reasoning in large language models. _arXiv preprint arXiv: Arxiv-2201.11903_ , 2022. 

- [47] Volodymyr Mnih, Adrià Puigdomènech Badia, Mehdi Mirza, Alex Graves, Timothy P. Lillicrap, Tim Harley, David Silver, and Koray Kavukcuoglu. Asynchronous methods for deep reinforcement learning. In Maria-Florina Balcan and Kilian Q. Weinberger, editors, _Proceedings of the 33nd International Conference on Machine Learning, ICML 2016, New York City, NY, USA, June 19-24, 2016_ , volume 48 of _JMLR Workshop and Conference Proceedings_ , pages 1928–1937. JMLR.org, 2016. 

- [48] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. Proximal policy optimization algorithms. _arXiv preprint arXiv: Arxiv-1707.06347_ , 2017. 

- [49] Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval Tassa, David Silver, and Daan Wierstra. Continuous control with deep reinforcement learning. In Yoshua Bengio and Yann LeCun, editors, _4th International Conference on Learning Representations, ICLR 2016, San Juan, Puerto Rico, May 2-4, 2016, Conference Track Proceedings_ , 2016. 

- [50] Introducing chatgpt, 2022. 

- [51] New and improved embedding model, 2022. 

- [52] PrismarineJS. Prismarinejs/mineflayer: Create minecraft bots with a powerful, stable, and high level javascript api., 2013. 

- [53] Kolby Nottingham, Prithviraj Ammanabrolu, Alane Suhr, Yejin Choi, Hanna Hajishirzi, Sameer Singh, and Roy Fox. Do embodied agents dream of pixelated sheep?: Embodied decision making using language guided world modelling. _ARXIV.ORG_ , 2023. 

- [54] Shaofei Cai, Zihao Wang, Xiaojian Ma, Anji Liu, and Yitao Liang. Open-world multi-task control through goal-aware representation learning and adaptive horizon prediction. _arXiv preprint arXiv: Arxiv-2301.10034_ , 2023. 

- [55] Zihao Wang, Shaofei Cai, Anji Liu, Xiaojian Ma, and Yitao Liang. Describe, explain, plan and select: Interactive planning with large language models enables open-world multi-task agents. _arXiv preprint arXiv: Arxiv-2302.01560_ , 2023. 

- [56] Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid Palangi, Marco Tulio Ribeiro, and Yi Zhang. Sparks of artificial general intelligence: Early experiments with gpt-4. _arXiv preprint arXiv: Arxiv-2303.12712_ , 2023. 

- [57] Yiheng Liu, Tianle Han, Siyuan Ma, Jiayue Zhang, Yuanyuan Yang, Jiaming Tian, Hao He, Antong Li, Mengshen He, Zhengliang Liu, Zihao Wu, Dajiang Zhu, Xiang Li, Ning Qiang, Dingang Shen, Tianming Liu, and Bao Ge. Summary of chatgpt/gpt-4 research and perspective towards the future of large language models. _arXiv preprint arXiv: Arxiv-2304.01852_ , 2023. 

- [58] Shikun Liu, Linxi Fan, Edward Johns, Zhiding Yu, Chaowei Xiao, and Anima Anandkumar. Prismer: A vision-language model with an ensemble of experts. _arXiv preprint arXiv: Arxiv2303.02506_ , 2023. 

15 

- [59] Danny Driess, Fei Xia, Mehdi S. M. Sajjadi, Corey Lynch, Aakanksha Chowdhery, Brian Ichter, Ayzaan Wahid, Jonathan Tompson, Quan Vuong, Tianhe Yu, Wenlong Huang, Yevgen Chebotar, Pierre Sermanet, Daniel Duckworth, Sergey Levine, Vincent Vanhoucke, Karol Hausman, Marc Toussaint, Klaus Greff, Andy Zeng, Igor Mordatch, and Pete Florence. Palm-e: An embodied multimodal language model. _arXiv preprint arXiv: Arxiv-2303.03378_ , 2023. 

- [60] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, Aurelien Rodriguez, Armand Joulin, Edouard Grave, and Guillaume Lample. Llama: Open and efficient foundation language models. _arXiv preprint arXiv: Arxiv-2302.13971_ , 2023. 

- [61] William H. Guss, Brandon Houghton, Nicholay Topin, Phillip Wang, Cayden Codel, Manuela Veloso, and Ruslan Salakhutdinov. Minerl: A large-scale dataset of minecraft demonstrations. In Sarit Kraus, editor, _Proceedings of the Twenty-Eighth International Joint Conference on Artificial Intelligence, IJCAI 2019, Macao, China, August 10-16, 2019_ , pages 2442–2448. ijcai.org, 2019. 

- [62] William H. Guss, Cayden Codel, Katja Hofmann, Brandon Houghton, Noboru Kuno, Stephanie Milani, Sharada Mohanty, Diego Perez Liebana, Ruslan Salakhutdinov, Nicholay Topin, Manuela Veloso, and Phillip Wang. The minerl 2019 competition on sample efficient reinforcement learning using human priors. _arXiv preprint arXiv: Arxiv-1904.10079_ , 2019. 

- [63] William H. Guss, Mario Ynocente Castro, Sam Devlin, Brandon Houghton, Noboru Sean Kuno, Crissman Loomis, Stephanie Milani, Sharada Mohanty, Keisuke Nakata, Ruslan Salakhutdinov, John Schulman, Shinya Shiroshita, Nicholay Topin, Avinash Ummadisingu, and Oriol Vinyals. The minerl 2020 competition on sample efficient reinforcement learning using human priors. _arXiv preprint arXiv: Arxiv-2101.11071_ , 2021. 

- [64] Anssi Kanervisto, Stephanie Milani, Karolis Ramanauskas, Nicholay Topin, Zichuan Lin, Junyou Li, Jianing Shi, Deheng Ye, Qiang Fu, Wei Yang, Weijun Hong, Zhongyue Huang, Haicheng Chen, Guangjun Zeng, Yue Lin, Vincent Micheli, Eloi Alonso, François Fleuret, Alexander Nikulin, Yury Belousov, Oleg Svidchenko, and Aleksei Shpilman. Minerl diamond 2021 competition: Overview, results, and lessons learned. _arXiv preprint arXiv: Arxiv-2202.10583_ , 2022. 

- [65] Matthew Johnson, Katja Hofmann, Tim Hutton, and David Bignell. The malmo platform for artificial intelligence experimentation. In Subbarao Kambhampati, editor, _Proceedings of the Twenty-Fifth International Joint Conference on Artificial Intelligence, IJCAI 2016, New York, NY, USA, 9-15 July 2016_ , pages 4246–4247. IJCAI/AAAI Press, 2016. 

- [66] Zichuan Lin, Junyou Li, Jianing Shi, Deheng Ye, Qiang Fu, and Wei Yang. Juewu-mc: Playing minecraft with sample-efficient hierarchical reinforcement learning. _arXiv preprint arXiv: Arxiv-2112.04907_ , 2021. 

- [67] Hangyu Mao, Chao Wang, Xiaotian Hao, Yihuan Mao, Yiming Lu, Chengjie Wu, Jianye Hao, Dong Li, and Pingzhong Tang. Seihai: A sample-efficient hierarchical ai for the minerl competition. _arXiv preprint arXiv: Arxiv-2111.08857_ , 2021. 

- [68] Alexey Skrynnik, Aleksey Staroverov, Ermek Aitygulov, Kirill Aksenov, Vasilii Davydov, and Aleksandr I. Panov. Hierarchical deep q-network from imperfect demonstrations in minecraft. _Cogn. Syst. Res._ , 65:74–78, 2021. 

- [69] Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timothy Lillicrap. Mastering diverse domains through world models. _arXiv preprint arXiv: Arxiv-2301.04104_ , 2023. 

- [70] Ryan Volum, Sudha Rao, Michael Xu, Gabriel DesGarennes, Chris Brockett, Benjamin Van Durme, Olivia Deng, Akanksha Malhotra, and Bill Dolan. Craft an iron sword: Dynamically generating interactive game characters by prompting large language models tuned on code. In _Proceedings of the 3rd Wordplay: When Language Meets Games Workshop (Wordplay 2022)_ , pages 25–43, Seattle, United States, 2022. Association for Computational Linguistics. 

- [71] Haoqi Yuan, Chi Zhang, Hongcheng Wang, Feiyang Xie, Penglin Cai, Hao Dong, and Zongqing Lu. Plan4mc: Skill reinforcement learning and planning for open-world minecraft tasks. _arXiv preprint arXiv: 2303.16563_ , 2023. 

16 

- [72] Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von Arx, Michael S. Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card, Rodrigo Castellon, Niladri Chatterji, Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora Demszky, Chris Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John Etchemendy, Kawin Ethayarajh, Li Fei-Fei, Chelsea Finn, Trevor Gale, Lauren Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha, Tatsunori Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling, Fereshte Khani, Omar Khattab, Pang Wei Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal Ladhak, Mina Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li, Xuechen Li, Tengyu Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani, Eric Mitchell, Zanele Munyikwa, Suraj Nair, Avanika Narayan, Deepak Narayanan, Ben Newman, Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan, Julian Nyarko, Giray Ogut, Laurel Orr, Isabel Papadimitriou, Joon Sung Park, Chris Piech, Eva Portelance, Christopher Potts, Aditi Raghunathan, Rob Reich, Hongyu Ren, Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher Ré, Dorsa Sadigh, Shiori Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, Alex Tamkin, Rohan Taori, Armin W. Thomas, Florian Tramèr, Rose E. Wang, William Wang, Bohan Wu, Jiajun Wu, Yuhuai Wu, Sang Michael Xie, Michihiro Yasunaga, Jiaxuan You, Matei Zaharia, Michael Zhang, Tianyi Zhang, Xikun Zhang, Yuhui Zhang, Lucia Zheng, Kaitlyn Zhou, and Percy Liang. On the opportunities and risks of foundation models. _arXiv preprint arXiv: Arxiv-2108.07258_ , 2021. 

- [73] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel. Palm: Scaling language modeling with pathways. _arXiv preprint arXiv: Arxiv-2204.02311_ , 2022. 

- [74] Hyung Won Chung, Le Hou, Shayne Longpre, Barret Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi Wang, Mostafa Dehghani, Siddhartha Brahma, Albert Webson, Shixiang Shane Gu, Zhuyun Dai, Mirac Suzgun, Xinyun Chen, Aakanksha Chowdhery, Sharan Narang, Gaurav Mishra, Adams Yu, Vincent Zhao, Yanping Huang, Andrew Dai, Hongkun Yu, Slav Petrov, Ed H. Chi, Jeff Dean, Jacob Devlin, Adam Roberts, Denny Zhou, Quoc V. Le, and Jason Wei. Scaling instruction-finetuned language models. _arXiv preprint arXiv: Arxiv-2210.11416_ , 2022. 

- [75] Jiafei Duan, Samson Yu, Hui Li Tan, Hongyuan Zhu, and Cheston Tan. A survey of embodied AI: from simulators to research tasks. _IEEE Trans. Emerg. Top. Comput. Intell._ , 6(2):230–244, 2022. 

- [76] Dhruv Batra, Angel X. Chang, Sonia Chernova, Andrew J. Davison, Jia Deng, Vladlen Koltun, Sergey Levine, Jitendra Malik, Igor Mordatch, Roozbeh Mottaghi, Manolis Savva, and Hao Su. Rearrangement: A challenge for embodied ai. _arXiv preprint arXiv: Arxiv-2011.01975_ , 2020. 

- [77] Harish Ravichandar, Athanasios S Polydoros, Sonia Chernova, and Aude Billard. Recent advances in robot learning from demonstration. _Annual review of control, robotics, and autonomous systems_ , 3:297–330, 2020. 

- [78] Jack Collins, Shelvin Chand, Anthony Vanderkop, and David Howard. A review of physics simulators for robotic applications. _IEEE Access_ , 9:51416–51431, 2021. 

- [79] So Yeon Min, Devendra Singh Chaplot, Pradeep Ravikumar, Yonatan Bisk, and R. Salakhutdinov. Film: Following instructions in language with modular methods. _International Conference on Learning Representations_ , 2021. 

17 

- [80] Valts Blukis, Chris Paxton, Dieter Fox, Animesh Garg, and Yoav Artzi. A persistent spatial semantic representation for high-level natural language instruction execution. In _5th Annual Conference on Robot Learning_ , 2021. 

- [81] Varun Nair, Elliot Schumacher, Geoffrey Tso, and Anitha Kannan. Dera: Enhancing large language model completions with dialog-enabled resolving agents. _arXiv preprint arXiv: Arxiv-2303.17071_ , 2023. 

- [82] Joon Sung Park, Joseph C. O’Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior. _arXiv preprint arXiv: Arxiv-2304.03442_ , 2023. 

- [83] Yue Wu, Shrimai Prabhumoye, So Yeon Min, Yonatan Bisk, Ruslan Salakhutdinov, Amos Azaria, Tom Mitchell, and Yuanzhi Li. Spring: Gpt-4 out-performs rl algorithms by studying papers and reasoning. _arXiv preprint arXiv: 2305.15486_ , 2023. 

- [84] Erik Nijkamp, Bo Pang, Hiroaki Hayashi, Lifu Tu, Huan Wang, Yingbo Zhou, Silvio Savarese, and Caiming Xiong. A conversational paradigm for program synthesis. _arXiv preprint arXiv: Arxiv-2203.13474_ , 2022. 

- [85] Hung Le, Yue Wang, Akhilesh Deepak Gotmare, Silvio Savarese, and Steven C. H. Hoi. Coderl: Mastering code generation through pretrained models and deep reinforcement learning. _arXiv preprint arXiv: Arxiv-2207.01780_ , 2022. 

- [86] Xinyun Chen, Chang Liu, and Dawn Song. Execution-guided neural program synthesis. In _7th International Conference on Learning Representations, ICLR 2019, New Orleans, LA, USA, May 6-9, 2019_ . OpenReview.net, 2019. 

- [87] Xinyun Chen, Dawn Song, and Yuandong Tian. Latent execution for neural program synthesis. _arXiv preprint arXiv: Arxiv-2107.00101_ , 2021. 

- [88] Kevin Ellis, Maxwell I. Nye, Yewen Pu, Felix Sosa, Josh Tenenbaum, and Armando SolarLezama. Write, execute, assess: Program synthesis with a REPL. In Hanna M. Wallach, Hugo Larochelle, Alina Beygelzimer, Florence d’Alché-Buc, Emily B. Fox, and Roman Garnett, editors, _Advances in Neural Information Processing Systems 32: Annual Conference on Neural Information Processing Systems 2019, NeurIPS 2019, December 8-14, 2019, Vancouver, BC, Canada_ , pages 9165–9174, 2019. 

- [89] Yujia Li, David Choi, Junyoung Chung, Nate Kushman, Julian Schrittwieser, Rémi Leblond, Tom Eccles, James Keeling, Felix Gimeno, Agustin Dal Lago, Thomas Hubert, Peter Choy, Cyprien de Masson d’Autume, Igor Babuschkin, Xinyun Chen, Po-Sen Huang, Johannes Welbl, Sven Gowal, Alexey Cherepanov, James Molloy, Daniel J. Mankowitz, Esme Sutherland Robson, Pushmeet Kohli, Nando de Freitas, Koray Kavukcuoglu, and Oriol Vinyals. Competition-level code generation with alphacode. _arXiv preprint arXiv: Arxiv-2203.07814_ , 2022. 

- [90] Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian, Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and John Schulman. Training verifiers to solve math word problems. _arXiv preprint arXiv: Arxiv2110.14168_ , 2021. 

- [91] Ansong Ni, Srini Iyer, Dragomir Radev, Ves Stoyanov, Wen tau Yih, Sida I. Wang, and Xi Victoria Lin. Lever: Learning to verify language-to-code generation with execution. _arXiv preprint arXiv: Arxiv-2302.08468_ , 2023. 

- [92] Marta Skreta, Naruki Yoshikawa, Sebastian Arellano-Rubach, Zhi Ji, Lasse Bjørn Kristensen, Kourosh Darvish, Alán Aspuru-Guzik, Florian Shkurti, and Animesh Garg. Errors are useful prompts: Instruction guided task programming with verifier-assisted iterative prompting. _arXiv preprint arXiv: Arxiv-2303.14100_ , 2023. 

18 

## **A Method** 

## **A.1 VOYAGER Algorithm** 

Pseudocode 1: VOYAGER algorithm. 

```
defvoyager(
environment ,#environmentthatusescodeasactionspace
curriculum_agent ,#curriculumagentforproposingthenexttask
action_agent ,#actionagentforcodegeneration
critic_agent ,#criticagentforself -verification
skill_manager ,#skillmanagerforaddingnewskillsandskill
retrieval
):
agent_state=environment.reset ()
whileTrue:
exploration_progress=(
curriculum_agent . get_exploration_progress (
curriculum_agent . get_completed_tasks (),
curriculum_agent . get_failed_tasks (),
)
)
task=curriculum_agent . propose_next_task (
agent_state ,exploration_progress
)
code=None
environment_feedback=None
execution_errors=None
critique=None
success=False
#tryatmost4roundsbeforemovingontothenexttask
foriinrange (4):
skills=skill_manager . retrieve_skills (
task ,environment_feedback
)
code=action_agent. generate_code (
task ,
code ,
environment_feedback ,
execution_errors ,
critique ,
skills ,
)
(
agent_state ,
environment_feedback ,
execution_errors ,
)=environment.step(code)
success ,critique=critic_agent. check_task_success (
task ,agent_state
)
ifsuccess:
break
ifsuccess:
skill_manager.add_skill(code)
curriculum_agent . add_completed_task (task)
else:
curriculum_agent . add_failed_task (task)
```

## **A.2 Prompting** 

GPT-4 and GPT-3.5 offer users the ability to designate the role of each prompt message among three options: 

19 

- System: A high-level instruction that guides the model behavior throughout the conversation. It sets the overall tone and objective for the interaction. 

- User: A detailed instruction that guides the assistant for the next immediate response. 

- Assistant: A response message generated the model. 

## See `https://platform.openai.com/docs/guides/chat/introduction` for more details. 

To save token usage, instead of engaging in multi-round conversations, we concatenate a system prompt and a user prompt to obtain each assistant’s response. 

## **A.3 Automatic Curriculum** 

## **A.3.1 Components in the Prompt** 

The input prompt to GPT-4 consists of several components: 

- (1) Directives encouraging diverse behaviors and imposing constraints (so that the proposed task is achievable and verifiable): See Sec. A.3.4 for the full prompt; 

- (2) The agent’s current state: 

   - **Inventory** : A dictionary of items with counts, for example, {‘cobblestone’: 4, ‘furnace’: 1, ‘stone_pickaxe’: 1, ‘oak_planks’: 7, ‘dirt’: 6, ‘wooden_pickaxe’: 1, ‘crafting_table’: 1, ‘raw_iron’: 4, ‘coal’: 1}; 

   - **Equipment** : Armors or weapons equipped by the agents; 

   - **Nearby blocks** : A set of block names within a 32-block distance to the agent, for example, ‘dirt’, ‘water’, ‘spruce_planks’, ‘grass_block’, ‘dirt_path’, ‘sugar_cane’, ‘fern’; 

   - **Other blocks that are recently seen** : Blocks that are not nearby or in the inventory; 

   - **Nearby entities** : A set of entity names within a 32-block distance to the agent, for example, ‘pig’, ‘cat’, ‘villager’, ‘zombie’; 

   - **A list of chests that are seen by the agent** : Chests are external containers where the agent can deposit items. If a chest is not opened before, its content is “Unknown”. Otherwise, the items inside each chest are shown to the agent. 

   - **Biome** : For example, ‘plains’, ‘flower_forest’, ‘meadow’, ‘river’, ‘beach’, ‘forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘old_growth_birch_forest’, ‘ocean’, ‘sunflower_plains’, ‘stony_shore’; 

   - **Time** : One of ‘sunrise’, ‘day’, ‘noon’, ‘sunset’, ‘night’, ‘midnight’; 

   - **Health and hunger bars** : The max value is 20; 

   - **Position** : 3D coordinate ( _x, y, z_ ) of the agent’s position in the Minecraft world; 

- (3) Previously completed and failed tasks; 

- (4) Additional context: See Sec. A.3.2; 

- (5) Chain-of-thought prompting [46] in response: We request GPT-4 to first reason about the current progress and then suggest the next task. 

## **A.3.2 Additional Context** 

We leverage GPT-3.5 to self-ask questions to provide additional context. Each question is paired with a concept that is used for retrieving the most relevant document from the wiki knowledge base [23]. We feed the document content to GPT-3.5 for self-answering questions. In practice, using a wiki knowledge base is optional since GPT-3.5 already possesses a good understanding of Minecraft game mechanics. However, the external knowledge base becomes advantageous if GPT-3.5 is not pre-trained in that specific domain. See Sec. A.3.4 for the full prompt. 

## **A.3.3 Warm-up Schedule** 

In practice, we adopt a warm-up schedule to gradually incorporate the agent’s state and the additional context into the prompt based on how many tasks the agent has completed. This ensures that the prompt is exposed to increasing amounts of information over the exploration progress and therefore 

20 

begins with basic skills and progressively advances towards more intricate and diverse ones. The warm-up setting that we use across all the experiments is shown in Table. A.1. 

Table A.1: Warm-up schedule for automatic curriculum. 

|Information in the prompt|After how many tasks are completed|
|---|---|
|||
|core inventory (only including log, planks, stick,<br>crafting table, furnace, dirt, coal, pickaxe, sword,<br>and axe)<br>equipment<br>nearby blocks<br>position<br>nearby entities<br>full inventory<br>other blocks that are recently seen<br>biome<br>health bar<br>hunger bar<br>time<br>additional context|0<br>0<br>0<br>0<br>5<br>7<br>10<br>10<br>15<br>15<br>15<br>15|



## **A.3.4 Full Prompt** 

Prompt 1: Full system prompt for automatic curriculum. The list of question-answer pairs represents the additional context. 

```
Youareahelpfulassistantthattellsmethenextimmediatetaskto
doinMinecraft.Myultimategoalistodiscoverasmanydiverse
thingsaspossible ,accomplishasmanydiversetasksaspossible
andbecomethebestMinecraftplayerintheworld.
Iwillgiveyouthefollowinginformation:
Question1:...
Answer:...
Question2:...
Answer:...
Question3:...
Answer:...
...
Biome:...
Time:...
Nearbyblocks:...
Otherblocksthatarerecentlyseen:...
Nearbyentities(nearesttofarthest):...
Health:Higherthan15meansI’mhealthy.
Hunger:Higherthan15meansI’mnothungry.
Position:...
Equipment:IfIhavebetterarmorinmyinventory ,youshouldaskme
toequipit.
Inventory(xx /36):...
Chests:Youcanaskmetodepositortakeitemsfromthesechests.
Therealsomightbesomeunknownchest ,youshouldaskmetoopen
andcheckitemsinsidetheunknownchest.
Completedtaskssofar:...
Failedtasksthataretoohard:...
Youmustfollowthefollowingcriteria:
1)Youshouldactasamentorandguidemetothenexttaskbasedon
mycurrentlearningprogress.
2)PleasebeveryspecificaboutwhatresourcesIneedtocollect ,
whatIneedtocraft ,orwhatmobsIneedtokill.
```

21 

```
3)Thenexttaskshouldfollowaconciseformat ,suchas"Mine[
quantity][block ]","Craft[quantity][item]","Smelt[quantity][
item]","Kill[quantity][mob]","Cook[quantity][food]","Equip
[item ]"etc.Itshouldbeasinglephrase.Donotproposemultiple
tasksatthesametime.Donotmentionanythingelse.
4)ThenexttaskshouldnotbetoohardsinceImaynothavethe
necessaryresourcesorhavelearnedenoughskillstocompleteit
yet.
5)Thenexttaskshouldbenovelandinteresting.Ishouldlookfor
rareresources ,upgrademyequipmentandtoolsusingbetter
materials ,anddiscovernewthings.Ishouldnotbedoingthesame
thingoverandoveragain.
6)ImaysometimesneedtorepeatsometasksifIneedtocollectmore
resourcestocompletemoredifficulttasks.Onlyrepeattasksif
necessary.
7)Donotaskmetobuildordigshelterevenifit ’satnight.Iwant
toexploretheworldanddiscovernewthings.Idon ’twantto
stayinoneplace.
8)Tasksthatrequireinformationbeyondtheplayer ’sstatustoverify
shouldbeavoided.Forinstance ,"Placing4torches"and"Diga2
x1x2hole"arenotidealsincetheyrequirevisualconfirmation
fromthescreen.Alltheplacing ,building ,planting ,andtrading
tasksshouldbeavoided.Donotproposetaskstartingwiththese
keywords.
Youshouldonlyrespondintheformatasdescribedbelow:
RESPONSEFORMAT:
Reasoning:BasedontheinformationIlistedabove ,doreasoningabout
whatthenexttaskshouldbe.
Task:Thenexttask.
Here ’sanexampleresponse:
Reasoning:Theinventoryisemptynow ,chopdownatreetogetsome
wood.
Task:Obtainawoodlog.
```

Prompt 2: Full system prompt for asking questions. We provide both good and bad examples as few-shot exemplars. 

```
Youareahelpfulassistantthatasksquestionstohelpmedecidethe
nextimmediatetasktodoinMinecraft.Myultimategoalisto
discoverasmanythingsaspossible ,accomplishasmanytasksas
possibleandbecomethebestMinecraftplayerintheworld.
Iwillgiveyouthefollowinginformation:
Biome:...
Time:...
Nearbyblocks:...
Otherblocksthatarerecentlyseen:...
Nearbyentities(nearesttofarthest):...
Health:...
Hunger:...
Position:...
Equipment:...
Inventory(xx /36):...
Chests:...
Completedtaskssofar:...
Failedtasksthataretoohard:...
Youmustfollowthefollowingcriteria:
1)Youshouldaskatleast5questions(butnomorethan10questions)
tohelpmedecidethenextimmediatetasktodo.Eachquestion
shouldbefollowedbytheconceptthatthequestionisabout.
2)YourquestionshouldbespecifictoaconceptinMinecraft.
Badexample(thequestionistoogeneral):
```

22 

```
Question:WhatisthebestwaytoplayMinecraft?
Concept:unknown
Badexample(axeisstillgeneral ,youshouldspecifythetypeof
axesuchaswoodenaxe):
Whatarethebenefitsofusinganaxetogatherresources?
Concept:axe
Goodexample:
Question:Howtomakeawoodenpickaxe?
Concept:woodenpickaxe
3)Yourquestionsshouldbeself -containedandnotrequireanycontext
.
Badexample(thequestionrequiresthecontextofmycurrentbiome):
Question:WhataretheblocksthatIcanfindinmycurrentbiome?
Concept:unknown
Badexample(thequestionrequiresthecontextofmycurrent
inventory):
Question:Whataretheresourcesyouneedthemostcurrently?
Concept:unknown
Badexample(thequestionrequiresthecontextofmycurrent
inventory):
Question:Doyouhaveanygoldoremeraldresources?
Concept:gold
Badexample(thequestionrequiresthecontextofmynearbyentities
):
Question:Canyouseeanyanimalsnearbythatyoucankillfor
food?
Concept:food
Badexample(thequestionrequiresthecontextofmynearbyblocks):
Question:Isthereanywatersourcenearby?
Concept:water
Goodexample:
Question:WhataretheblocksthatIcanfindinthesparsejungle
?
Concept:sparsejungle
4)Donotaskquestionsaboutbuildingtasks(suchasbuildinga
shelter)sincetheyaretoohardformetodo.
Let ’ssayyourcurrentbiomeissparsejungle.Youcanaskquestions
like:
Question:WhataretheitemsthatIcanfindinthesparsejungle?
Concept:sparsejungle
Question:WhatarethemobsthatIcanfindinthesparsejungle?
Concept:sparsejungle
Let ’ssayyouseeacreepernearby ,andyouhavenotdefeateda
creeperbefore.Youcanaskaquestionlike:
Question:Howtodefeatthecreeper?
Concept:creeper
Let ’ssayyoulastcompletedtaskis"Craftawoodenpickaxe ".Youcan
askaquestionlike:
Question:WhatarethesuggestedtasksthatIcandoaftercraftinga
woodenpickaxe?
Concept:woodenpickaxe
Herearesomemorequestionandconceptexamples:
Question:WhataretheoresthatIcanfindinthesparsejungle?
Concept:sparsejungle
(theaboveconceptshouldnotbe"ore"becauseIneedtolookupthe
pageof"sparsejungle"tofindoutwhatoresIcanfindinthe
sparsejungle)
Question:Howcanyouobtainfoodinthesparsejungle?
Concept:sparsejungle
```

23 

```
(theaboveconceptshouldnotbe"food"becauseIneedtolookupthe
pageof"sparsejungle"tofindoutwhatfoodIcanobtaininthe
sparsejungle)
Question:Howcanyouusethefurnacetoupgradeyourequipmentand
makeusefulitems?
Concept:furnace
Question:Howtoobtainadiamondore?
Concept:diamondore
Question:Whatarethebenefitsofusingastonepickaxeoverawooden
pickaxe?
Concept:stonepickaxe
Question:Whatarethetoolsthatyoucancraftusingwoodplanksand
sticks?
Concept:woodplanks
Youshouldonlyrespondintheformatasdescribedbelow:
RESPONSEFORMAT:
Reasoning:...
Question1:...
Concept1:...
Question2:...
Concept2:...
Question3:...
Concept3:...
Question4:...
Concept4:...
Question5:...
Concept5:...
...
```

Prompt 3: Full system prompt for answering questions. Context represents the optional content from a wiki knowledge base. 

```
YouareahelpfulassistantthatanswermyquestionaboutMinecraft.
Iwillgiveyouthefollowinginformation:
Question:...
Youwillanswerthequestionbasedonthecontext(onlyifavailable
andhelpful)andyourownknowledgeofMinecraft.
1)Startyouranswerwith"Answer:".
2)Answer"Answer:Unknown"ifyoudon ’tknowtheanswer.
```

## **A.4 Skill Library** 

## **A.4.1 Components in the Prompt** 

The input prompt to GPT-4 consists of the following components: 

- (1) Guidelines for code generation: See Sec A.4.2 for the full prompt; 

- (2) Control primitive APIs implemented by us: These APIs serve a dual purpose: they demonstrate the usage of Mineflayer APIs, and they can be directly called by GPT-4. 

   - `exploreUntil(bot, direction, maxTime = 60, callback)` : Allow the agent to explore in a fixed direction for `maxTime` . The `callback` is the stopping condition implemented by the agent to determine when to stop exploring; 

   - `mineBlock(bot, name, count = 1)` : Mine and collect the specified number of blocks within a 32-block distance; 

   - `craftItem(bot, name, count = 1)` : Craft the item with a crafting table nearby; 

   - `placeItem(bot, name, position)` : Place the block at the specified position; 

   - `smeltItem(bot, itemName, fuelName, count = 1)` : Smelt the item with the specified fuel. There must be a furnace nearby; 

24 

   - `killMob(bot, mobName, timeout = 300)` : Attack the mob and collect its dropped item; 

   - `getItemFromChest(bot, chestPosition, itemsToGet)` : Move to the chest at the specified position and get items from the chest; 

   - `depositItemIntoChest(bot, chestPosition, itemsToDeposit)` : Move to the chest at the specified position and deposit items into the chest; 

- (3) Control primitive APIs provided by Mineflayer: 

   - `await bot.pathfinder.goto(goal)` : Go to a specific position. See below for how to set the goal; 

   - `new GoalNear(x, y, z, range)` : Move the bot to a block within the specified range of the specified block; 

   - `new GoalXZ(x, z)` : For long-range goals that don’t have a specific Y level; 

   - `new GoalGetToBlock(x, y, z)` : Not get into the block, but get directly adjacent to it. Useful for fishing, farming, filling a bucket, and using a bed.; 

   - `new GoalFollow(entity, range)` : Follow the specified entity within the specified range; 

   - `new GoalPlaceBlock(position, bot.world, {})` : Position the bot in order to place a block; 

   - `new GoalLookAtBlock(position, bot.world, {})` : Path towards a position where a face of the block at `position` is visible; 

   - `bot.isABed(bedBlock)` : Return true if `bedBlock` is a bed; 

   - `bot.blockAt(position)` : Return the block at `position` ; 

   - `await bot.equip(item, destination)` : Equip the item in the specified destination. `destination` must be one of “hand”, “head”, “torso”, “legs”, “feet”, “off-hand”; 

   - `await bot.consume()` : Consume the item in the bot’s hand. You must equip the item to consume first. Useful for eating food, drinking potions, etc.; 

   - `await bot.fish()` : Let bot fish. Before calling this function, you must first get to a water block and then equip a fishing rod. The bot will automatically stop fishing when it catches a fish; 

   - `await bot.sleep(bedBlock)` : Sleep until sunrise. You must get to a bed block first; 

   - `await bot.activateBlock(block)` : This is the same as right-clicking a block in the game. Useful for buttons, doors, etc. You must get to the block first; 

   - `await bot.lookAt(position)` : Look at the specified position. You must go near the position before you look at it. To fill a bucket with water, you must look at it first; 

   - `await bot.activateItem()` : This is the same as right-clicking to use the item in the bot’s hand. Useful for using a bucket, etc. You must equip the item to activate first; 

   - `await bot.useOn(entity)` : This is the same as right-clicking an entity in the game. Useful for shearing a sheep. You must get to the entity first; 

- (4) Retrieved skills from the skill library; 

- (5) Generated code from the last round; 

- (6) Environment feedback: The chat log in the prompt; 

- (7) Execution errors; 

- (8) Critique from the self-verification module; 

- (9) The agent’s current state: See Sec. A.3.1 for each element of the agent’s state; 

- (10) Task proposed by the automatic curriculum; 

- (11) Task context: We prompt GPT-3.5 to ask for general suggestions about how to solve the task. In practice, this part is handled by the automatic curriculum since it has a systematic mechanism for question-answering (Sec. A.3.2); 

- (12) Chain-of-thought prompting [46] in response: We ask GPT-4 to first explain the reason why the code from the last round fails, then give step-by-step plans to finish the task, and finally generate code. See Sec. A.4.2 for the full prompt. 

25 

## **A.4.2 Full Prompt** 

Prompt 4: Full system prompt for code generation. 

```
YouareahelpfulassistantthatwritesMineflayerjavascriptcodeto
completeanyMinecrafttaskspecifiedbyme.
HerearesomeusefulprogramswrittenwithMineflayerAPIs.
/*
Exploreuntilfindaniron_ore ,useVec3(0,-1,0)becauseironores
areusuallyunderground
awaitexploreUntil(bot ,newVec3(0,-1,0),60,()=>{
constiron_ore=bot.findBlock ({
matching:mcData.blocksByName [" iron_ore "].id ,
maxDistance:32,
});
returniron_ore;
});
Exploreuntilfindapig ,useVec3(1,0,1)becausepigsareusually
onthesurface
letpig=awaitexploreUntil(bot ,newVec3(1,0,1),60,()=>{
constpig=bot.nearestEntity (( entity)=>{
return(
entity.name==="pig"&&
entity.position.distanceTo(bot.entity.position)<32
);
});
returnpig;
});
*/
asyncfunctionexploreUntil (bot ,direction ,maxTime=60,callback){
/*
Implementationofthisfunctionisomitted.
direction:Vec3 ,canonlycontainvalueof-1,0or1
maxTime:number ,themaxtimeforexploration
callback:function ,earlystopcondition ,willbecalledeach
second ,explorationwillstopifreturnvalueisnotnull
Return:nullifexploretimeout ,otherwisereturnthereturnvalue
ofcallback
*/
}
//Mine3cobblestone:mineBlock(bot ,"stone",3);
asyncfunctionmineBlock(bot ,name ,count=1){
constblocks=bot.findBlocks ({
matching:(block)=>{
returnblock.name===name;
},
maxDistance:32,
count:count ,
});
consttargets=[];
for(leti=0;i<Math.min(blocks.length ,count);i++){
targets.push(bot.blockAt(blocks[i]));
}
awaitbot.collectBlock.collect(targets ,{ignoreNoPath:true});
}
//Craft8oak_planksfrom2oak_log(dotherecipe2times):
craftItem(bot ,"oak_planks",2);
```

26 

```
//Youmustplaceacraftingtablebeforecallingthisfunction
asyncfunctioncraftItem(bot ,name ,count=1){
constitem=mcData.itemsByName[name ];
constcraftingTable=bot.findBlock ({
matching:mcData.blocksByName . crafting_table .id ,
maxDistance:32,
});
awaitbot.pathfinder.goto(
newGoalLookAtBlock ( craftingTable .position ,bot.world)
);
constrecipe=bot.recipesFor(item.id ,null ,1,craftingTable)[0];
awaitbot.craft(recipe ,count ,craftingTable );
}
//Placeacrafting_tableneartheplayer ,Vec3(1,0,0)isjustan
example ,youshouldn ’talwaysusethat:placeItem(bot ,"
crafting_table ",bot.entity.position.offset (1,0,0));
asyncfunctionplaceItem(bot ,name ,position){
constitem=bot.inventory. findInventoryItem (mcData.itemsByName[
name ].id);
//findareferenceblock
constfaceVectors=[
newVec3(0,1,0),
newVec3(0,-1,0),
newVec3(1,0,0),
newVec3(-1,0,0),
newVec3(0,0,1),
newVec3(0,0,-1),
];
letreferenceBlock=null;
letfaceVector=null;
for(constvectoroffaceVectors){
constblock=bot.blockAt(position.minus(vector));
if(block ?. name!=="air"){
referenceBlock=block;
faceVector=vector;
break;
}
}
//Youmustfirstgototheblockpositionyouwanttoplace
awaitbot.pathfinder.goto(newGoalPlaceBlock (position ,bot.world ,
{}));
//YoumustequiptheitemrightbeforecallingplaceBlock
awaitbot.equip(item ,"hand ");
awaitbot.placeBlock(referenceBlock ,faceVector);
}
//Smelt1raw_ironinto1iron_ingotusing1oak_planksasfuel:
smeltItem(bot ,"raw_iron","oak_planks ");
//Youmustplaceafurnacebeforecallingthisfunction
asyncfunctionsmeltItem(bot ,itemName ,fuelName ,count=1){
constitem=mcData.itemsByName[itemName ];
constfuel=mcData.itemsByName[fuelName ];
constfurnaceBlock=bot.findBlock ({
matching:mcData.blocksByName .furnace.id ,
maxDistance:32,
});
awaitbot.pathfinder.goto(
newGoalLookAtBlock (furnaceBlock.position ,bot.world)
);
constfurnace=awaitbot.openFurnace(furnaceBlock);
for(leti=0;i<count;i++){
awaitfurnace.putFuel(fuel.id ,null ,1);
```

27 

```
awaitfurnace.putInput(item.id ,null ,1);
//Wait12secondsforthefurnacetosmelttheitem
awaitbot.waitForTicks (12*20);
awaitfurnace.takeOutput ();
}
awaitfurnace.close ();
}
//Killapigandcollectthedroppeditem:killMob(bot ,"pig",300);
asyncfunctionkillMob(bot ,mobName ,timeout=300){
constentity=bot.nearestEntity (
(entity)=>
entity.name===mobName&&
entity.position.distanceTo(bot.entity.position)<32
);
awaitbot.pvp.attack(entity);
awaitbot.pathfinder.goto(
newGoalBlock(entity.position.x,entity.position.y,entity.
position.z)
);
}
//Getatorchfromchestat(30,65,100):getItemFromChest (bot ,new
Vec3 (30,65,100) ,{" torch ":1});
//Thisfunctionwillworknomatterhowfarthebotisfromthechest
.
asyncfunctiongetItemFromChest (bot ,chestPosition ,itemsToGet){
awaitmoveToChest(bot ,chestPosition );
constchestBlock=bot.blockAt( chestPosition );
constchest=awaitbot.openContainer (chestBlock);
for(constnameinitemsToGet){
constitemByName=mcData.itemsByName[name ];
constitem=chest. findContainerItem (itemByName.id);
awaitchest.withdraw(item.type ,null ,itemsToGet[name ]);
}
awaitcloseChest(bot ,chestBlock);
}
//Depositatorchintochestat(30,65,100):depositItemIntoChest (
bot ,newVec3 (30,65,100) ,{" torch ":1});
//Thisfunctionwillworknomatterhowfarthebotisfromthechest
.
asyncfunctiondepositItemIntoChest (bot ,chestPosition ,itemsToDeposit
){
awaitmoveToChest(bot ,chestPosition );
constchestBlock=bot.blockAt( chestPosition );
constchest=awaitbot.openContainer (chestBlock);
for(constnameinitemsToDeposit ){
constitemByName=mcData.itemsByName[name ];
constitem=bot.inventory. findInventoryItem (itemByName.id);
awaitchest.deposit(item.type ,null ,itemsToDeposit [name ]);
}
awaitcloseChest(bot ,chestBlock);
}
//Checktheitemsinsidethechestat(30,65,100):
checkItemInsideChest (bot ,newVec3 (30,65,100));
//Youonlyneedtocallthisfunctiononcewithoutanyactionto
finishtaskofcheckingitemsinsidethechest.
asyncfunctioncheckItemInsideChest (bot ,chestPosition ){
awaitmoveToChest(bot ,chestPosition );
constchestBlock=bot.blockAt( chestPosition );
awaitbot.openContainer (chestBlock);
//Youmustclosethechestafteropeningitifyouareaskedto
openachest
```

28 

```
awaitcloseChest(bot ,chestBlock);
}
awaitbot.pathfinder.goto(goal);//Averyusefulfunction.This
functionmaychangeyourmain -handequipment.
//FollowingaresomeGoalsyoucanuse:
newGoalNear(x,y,z,range);//Movethebottoablockwithinthe
specifiedrangeofthespecifiedblock.‘x‘,‘y‘,‘z‘,and‘range ‘
are‘number ‘
newGoalXZ(x,z);//Usefulforlong -rangegoalsthatdon ’thavea
specificYlevel.‘x‘and‘z‘are‘number ‘
newGoalGetToBlock (x,y,z);//Notgetintotheblock ,butget
directlyadjacenttoit.Usefulforfishing ,farming ,filling
bucket ,andbeds.‘x‘,‘y‘,and‘z‘are‘number ‘
newGoalFollow(entity ,range);//Followthespecifiedentitywithin
thespecifiedrange.‘entity ‘is‘Entity ‘,‘range ‘is‘number ‘
newGoalPlaceBlock (position ,bot.world ,{});//Positionthebotin
ordertoplaceablock.‘position ‘is‘Vec3 ‘
newGoalLookAtBlock (position ,bot.world ,{});//Pathintoaposition
whereablockfaceoftheblockatpositionisvisible.‘position ‘
is‘Vec3 ‘
//TheseareotherMineflayerfunctionsyoucanuse:
bot.isABed(bedBlock);//Returntrueif‘bedBlock ‘isabed
bot.blockAt(position);//Returntheblockat‘position ‘.‘position ‘
is‘Vec3 ‘
//TheseareotherMineflayerasyncfunctionsyoucanuse:
awaitbot.equip(item ,destination);//Equiptheiteminthespecified
destination.‘item ‘is‘Item ‘,‘destination ‘canonlybe"hand",
"head","torso","legs","feet","off -hand"
awaitbot.consume ();//Consumetheiteminthebot ’shand.Youmust
equiptheitemtoconsumefirst.Usefulforeatingfood ,drinking
potions ,etc.
awaitbot.fish ();//Letbotfish.Beforecallingthisfunction ,you
mustfirstgettoawaterblockandthenequipafishingrod.The
botwillautomaticallystopfishingwhenitcatchesafish
awaitbot.sleep(bedBlock);//Sleepuntilsunrise.Youmustgettoa
bedblockfirst
awaitbot.activateBlock(block);//Thisisthesameasright -clicking
ablockinthegame.Usefulforbuttons ,doors ,usinghoes ,etc.
Youmustgettotheblockfirst
awaitbot.lookAt(position);//Lookatthespecifiedposition.You
mustgonearthepositionbeforeyoulookatit.Tofillbucket
withwater ,youmustlookAtfirst.‘position ‘is‘Vec3 ‘
awaitbot.activateItem ();//Thisisthesameasright -clickingtouse
theiteminthebot ’shand.Usefulforusingbuckets ,etc.You
mustequiptheitemtoactivatefirst
awaitbot.useOn(entity);//Thisisthesameasright -clickingan
entityinthegame.Usefulforshearingsheep ,equippingharnesses
,etc.Youmustgettotheentityfirst
{ retrieved_skills }
Ateachroundofconversation ,Iwillgiveyou
Codefromthelastround:...
Executionerror:...
Chatlog:...
Biome:...
Time:...
Nearbyblocks:...
Nearbyentities(nearesttofarthest):
Health:...
```

29 

```
Hunger:...
Position:...
Equipment:...
Inventory(xx /36):...
Chests:...
Task:...
Context:...
Critique:...
```

```
Youshouldthenrespondtomewith
Explain(ifapplicable):Arethereanystepsmissinginyourplan?Why
doesthecodenotcompletethetask?Whatdoesthechatlogand
executionerrorimply?
Plan:Howtocompletethetaskstepbystep.Youshouldpayattention
toInventorysinceittellswhatyouhave.Thetaskcompleteness
checkisalsobasedonyourfinalinventory.
Code:
1)Writeanasyncfunctiontakingthebotastheonlyargument.
2)Reusetheaboveusefulprogramsasmuchaspossible.
-Use‘mineBlock(bot ,name ,count)‘tocollectblocks.Donot
use‘bot.dig ‘directly.
-Use‘craftItem(bot ,name ,count)‘tocraftitems.Donotuse
‘bot.craft ‘directly.
-Use‘smeltItem(bot ,namecount)‘tosmeltitems.Donotuse
‘bot.openFurnace ‘directly.
-Use‘placeItem(bot ,name ,position)‘toplaceblocks.Donot
use‘bot.placeBlock ‘directly.
-Use‘killMob(bot ,name ,timeout)‘tokillmobs.Donotuse‘
bot.attack ‘directly.
3)Yourfunctionwillbereusedforbuildingmorecomplex
functions.Therefore ,youshouldmakeitgenericandreusable.You
shouldnotmakestrongassumptionabouttheinventory(asitmay
bechangedatalatertime),andthereforeyoushouldalwayscheck
whetheryouhavetherequireditemsbeforeusingthem.Ifnot ,
youshouldfirstcollecttherequireditemsandreusetheabove
usefulprograms.
4)Functionsinthe"Codefromthelastround"sectionwillnotbe
savedorexecuted.Donotreusefunctionslistedthere.
5)Anythingdefinedoutsideafunctionwillbeignored ,defineall
yourvariablesinsideyourfunctions.
6)Call‘bot.chat ‘toshowtheintermediateprogress.
7)Use‘exploreUntil(bot ,direction ,maxDistance ,callback)‘when
youcannotfindsomething.Youshouldfrequentlycallthisbefore
miningblocksorkillingmobs.Youshouldselectadirectionat
randomeverytimeinsteadofconstantlyusing(1,0,1).
8)‘maxDistance ‘shouldalwaysbe32for‘bot.findBlocks ‘and‘bot
.findBlock ‘.Donotcheat.
9)Donotwriteinfiniteloopsorrecursivefunctions.
10)Donotuse‘bot.on ‘or‘bot.once ‘toregistereventlisteners.
Youdefinitelydonotneedthem.
11)Nameyourfunctioninameaningfulway(caninferthetask
fromthename).
```

```
Youshouldonlyrespondintheformatasdescribedbelow:
RESPONSEFORMAT:
Explain:...
Plan:
1)...
2)...
3)...
...
Code:
‘‘‘javascript
//helperfunctions(onlyifneeded ,trytoavoidthem)
...
```

30 

```
//mainfunctionafterthehelperfunctions
asyncfunctionyourMainFunctionName (bot){
//...
}
‘‘‘
```

Prompt 5: Full system prompt for generating function descriptions. This is used when adding a new skill to the skill library. We give a one-shot example in the prompt. 

```
Youareahelpfulassistantthatwritesadescriptionofthegiven
functionwritteninMineflayerjavascriptcode.
1)Donotmentionthefunctionname.
2)Donotmentionanythingabout‘bot.chat ‘orhelperfunctions.
3)Theremightbesomehelperfunctionsbeforethemainfunction ,but
youonlyneedtodescribethemainfunction.
4)Trytosummarizethefunctioninnomorethan6sentences.
5)Yourresponseshouldbeasinglelineoftext.
Forexample ,ifthefunctionis:
asyncfunctionmineCobblestone (bot){
//Checkifthewoodenpickaxeisintheinventory ,ifnot ,craft
one
letwoodenPickaxe=bot.inventory. findInventoryItem (mcData.
itemsByName [" wooden_pickaxe "].id);
if(! woodenPickaxe){
bot.chat (" Craftingawoodenpickaxe .");
awaitcraftWoodenPickaxe (bot);
woodenPickaxe=bot.inventory. findInventoryItem (mcData.itemsByName
[" wooden_pickaxe "].id);
}
//Equipthewoodenpickaxeifitexists
if(woodenPickaxe){
awaitbot.equip(woodenPickaxe ,"hand ");
//Exploreuntilwefindastoneblock
awaitexploreUntil(bot ,newVec3(1,-1,1),60,()=>{
conststone=bot.findBlock ({
matching:mcData.blocksByName [" stone "].id ,
maxDistance:32
});
if(stone){
returntrue;
}
});
//Mine8cobblestoneblocksusingthewoodenpickaxe
bot.chat (" Foundastoneblock.Mining8cobblestoneblocks .");
awaitmineBlock(bot ,"stone",8);
bot.chat (" Successfullymined8cobblestoneblocks .");
//Savetheeventofmining8cobblestone
bot.save (" cobblestone_mined ");
}else{
bot.chat (" Failedtocraftawoodenpickaxe.Cannotmine
cobblestone .");
}
}
Themainfunctionis‘mineCobblestone ‘.
Thenyouwouldwrite:
```

31 

```
Thefunctionisaboutmining8cobblestonesusingawoodenpickaxe.
Firstcheckifawoodenpickaxeisintheinventory.Ifnot ,craft
one.Ifthewoodenpickaxeisavailable ,equipthewoodenpickaxe
inthehand.Next ,exploretheenvironmentuntilfindingastone
block.Onceastoneblockisfound ,mineatotalof8cobblestone
blocksusingthewoodenpickaxe.
```

## **A.4.3 Examples** 

Skill library example 1: craftWoodenPlanks. 

```
asyncfunctioncraftWoodenPlanks (bot){
constlogNames=["oak_log","birch_log","spruce_log","jungle_log"
,"acacia_log","dark_oak_log ","mangrove_log"];
constplankNames=["oak_planks","birch_planks"," spruce_planks ","
"
jungle_planks","acacia_planks"," dark_oak_planks ",
mangrove_planks "];
constlogInInventory=logNames.find(logName=>bot.inventory.count(
mcData.itemsByName[logName ].id)>0);
if(! logInInventory){
bot.chat("Nowoodenlogininventory.Miningawoodenlog ...");
awaitmineWoodLog(bot);
}
constlogIndex=logNames.indexOf( logInInventory );
constplankName=plankNames[logIndex ];
bot.chat(‘Crafting4${plankName }... ‘);
awaitcraftItem(bot ,plankName ,1);
bot.chat(‘4${plankName}crafted .‘);
}
```

Skill library example 2: mineTenCobbledDeepslateBelowY0. 

```
asyncfunctionmineTenCobbledDeepslateBelowY0 (bot){
//Equiptheironpickaxe
constironPickaxe=bot.inventory. findInventoryItem (mcData.
itemsByName["iron_pickaxe"].id);
awaitbot.equip(ironPickaxe ,"hand");
//Findcobbled_deepslateblocksbelowY=0
constcobbledDeepslateBlocks=awaitexploreUntil(bot ,newVec3(1,
-1,1),60,()=>{
constcobbledDeepslate=bot.findBlock ({
matching:mcData.blocksByName [" cobbled_deepslate "].id ,
maxDistance:32,
position:pos=>pos.y<0
});
returncobbledDeepslate ;
});
//Mine10cobbled_deepslateblocks
awaitmineBlock(bot ," cobbled_deepslate ",10);
bot.chat("10cobbled_deepslateminedbelowY=0.");
}
```

## Skill library example 3: smeltFiveRawIronV2. 

```
asyncfunctionfindSuitablePosition (bot){
constoffsets=[newVec3(1,0,0),newVec3(-1,0,0),newVec3(0,
0,1),newVec3(0,0,-1)];
for(constoffsetofoffsets){
constposition=bot.entity.position.offset(offset.x,offset.y,
offset.z);
constblock=bot.blockAt(position);
```

32 

```
if(block.name==="air"){
returnposition;
}
}
returnnull;
}
asyncfunctionsmeltFiveRawIron (bot){
//Checkifthereisafurnaceintheinventory
constfurnaceItem=bot.inventory. findInventoryItem (mcData.
itemsByName.furnace.id);
//Ifnot ,craftafurnaceusingtheavailablecobblestone
if(! furnaceItem){
awaitcraftFurnace(bot);
}
//Findasuitablepositiontoplacethefurnace
constfurnacePosition=awaitfindSuitablePosition (bot);
if(! furnacePosition){
bot.chat("Couldnotfindasuitablepositiontoplacethefurnace.
");
return;
}
//Placethefurnaceatthesuitableposition
awaitplaceItem(bot ,"furnace",furnacePosition );
//Smelt5rawironusingtheavailablecoalasfuel
awaitsmeltItem(bot ,"raw_iron","coal",5);
bot.chat("5rawironsmelted.");
}
```

Skill library example 4: fillBucketWithWater. 

```
asyncfunctionfillBucketWithWater (bot){
//Findawaterblocknearby
constwaterBlock=awaitexploreUntil (bot ,newVec3(1,0,1),60,()
=>{
constwater=bot.findBlock ({
matching:mcData.blocksByName .water.id ,
maxDistance:32
});
returnwater;
});
if(! waterBlock){
bot.chat("Couldnotfindwater.");
return;
}
//Gotothewaterblock
constadjacentBlock=waterBlock.position.offset (0,1,0);
awaitbot.pathfinder.goto(
newGoalGetToBlock (adjacentBlock .x,adjacentBlock .y,
adjacentBlock.z)
);
//Lookatthewaterblock
awaitbot.lookAt(waterBlock.position ,true);
//Equipthebucket
constbucket=bot.inventory. findInventoryItem (mcData.itemsByName.
bucket.id);
awaitbot.equip(bucket ,"hand");
```

33 

```
//Activatethebuckettocollectwater
awaitbot.activateItem ();
bot.chat("Filledthebucketwithwater.");
}
```

Skill library example 5: catchFiveFishSafely. 

```
asyncfunctioncatchFiveFishSafely (bot){
//Checkifthebothasafishingrodinitsinventory
letfishingRod=bot.inventory. findInventoryItem (mcData.itemsByName.
fishing_rod.id);
if(! fishingRod){
awaitcraftFishingRod (bot);
fishingRod=bot.inventory. findInventoryItem (mcData.itemsByName.
fishing_rod.id);
}
//Findanearbywaterblock
letwaterBlock;
while(! waterBlock){
waterBlock=awaitexploreUntil(bot ,newVec3(1,0,1),60,()=>
{
constfoundWaterBlock=bot.findBlock ({
matching:mcData.blocksByName .water.id ,
maxDistance:32
});
returnfoundWaterBlock ;
});
if(! waterBlock){
bot.chat("Nopathtothewaterblock.Tryingtofindanother
waterblock ...");
}
}
//Movetoablockadjacenttothewaterblock
constadjacentBlock=waterBlock.position.offset (0,1,0);
awaitbot.pathfinder.goto(newGoalBlock( adjacentBlock .x,
adjacentBlock.y,adjacentBlock.z));
//Lookatthewaterblock
awaitbot.lookAt(waterBlock.position);
//Equipthefishingrod
awaitbot.equip(fishingRod ,"hand");
//Fishinthewater5times
for(leti=0;i<5;i++){
try{
awaitbot.fish ();
bot.chat(‘Fish${i+1}caught .‘);
}catch(error){
if(error.message==="Fishingcancelled"){
bot.chat("Fishingwascancelled.Tryingagain ...");
i--;//Retrythesameiteration
}else{
throwerror;
}
}
}
}
```

34 

## **A.5 Self-Verification** 

## **A.5.1 Components in the Prompt** 

The input prompt to GPT-4 consists of the following components: 

- (1) The agent’s state: We exclude other blocks that are recently seen and nearby entities from the agent’s state since they are not useful for assessing the task’s completeness. See Sec. A.3.1 for each element of the agent’s state; 

- (2) Task proposed by the automatic curriculum; 

- (3) Task context: We prompt GPT-3.5 to ask for general suggestions about how to solve the task. In practice, this part is handled by the automatic curriculum since it has a systematic mechanism for question-answering (Sec. A.3.2); 

- (4) Chain-of-thought prompting [46] in response: We request GPT-4 to initially reason about the task’s success or failure, then output a boolean variable indicating the task’s outcome, and finally provide a critique to the agent if the task fails. 

- (5) Few-shot examples for in-context learning [36–38]. 

## **A.5.2 Full Prompt** 

Prompt 6: Full system prompt for self-verification. 

```
YouareanassistantthatassessesmyprogressofplayingMinecraft
andprovidesusefulguidance.
YouarerequiredtoevaluateifIhavemetthetaskrequirements .
Exceedingthetaskrequirementsisalsoconsideredasuccesswhile
failingtomeetthemrequiresyoutoprovidecritiquetohelpme
improve.
Iwillgiveyouthefollowinginformation:
Biome:Thebiomeafterthetaskexecution.
Time:Thecurrenttime.
Nearbyblocks:Thesurroundingblocks.Theseblocksarenotcollected
yet.However ,thisisusefulforsomeplacingorplantingtasks.
Health:Mycurrenthealth.
Hunger:Mycurrenthungerlevel.Foreatingtask ,ifmyhungerlevel
is20.0,thenIsuccessfullyatethefood.
Position:Mycurrentposition.
Equipment:Myfinalequipment.Forcraftingtasks ,Isometimesequip
thecrafteditem.
Inventory(xx /36):Myfinalinventory.Forminingandsmeltingtasks ,
youonlyneedtocheckinventory.
Chests:Ifthetaskrequiresmetoplaceitemsinachest ,youcan
findchestinformationhere.
Task:TheobjectiveIneedtoaccomplish.
Context:Thecontextofthetask.
YoushouldonlyrespondinJSONformatasdescribedbelow:
{
"reasoning ":"reasoning",
"success ":boolean ,
"critique ":"critique",
}
EnsuretheresponsecanbeparsedbyPython‘json.loads ‘,e.g.:no
trailingcommas ,nosinglequotes ,etc.
Herearesomeexamples:
INPUT:
Inventory(2/36):{’oak_log ’:2,’spruce_log ’:2}
```

35 

```
Task:Mine3woodlogs
RESPONSE:
{
"reasoning ":"Youneedtomine3woodlogs.Youhave2oaklogs
and2sprucelogs ,whichaddupto4woodlogs.",
"success ":true ,
"critique ":""
}
INPUT:
Inventory(3/36):{’crafting_table ’:1,’spruce_planks ’:6,’stick ’:
4}
Task:Craftawoodenpickaxe
RESPONSE:
{
"reasoning ":"Youhaveenoughmaterialstocraftawoodenpickaxe ,
butyoudidn ’tcraftit.",
"success ":false ,
"critique ":"Craftawoodenpickaxewithacraftingtableusing3
spruceplanksand2sticks ."
}
INPUT:
Inventory(2/36):{’raw_iron ’:5,’stone_pickaxe ’:1}
Task:Mine5iron_ore
RESPONSE:
{
"reasoning ":"Miningiron_oreinMinecraftwillgetraw_iron.You
have5raw_ironinyourinventory .",
"success ":true ,
"critique ":""
}
INPUT:
Biome:plains
Nearbyblocks:stone ,dirt ,grass_block ,grass ,farmland ,wheat
Inventory(26/36):...
Task:Plant1wheatseed.
RESPONSE:
{
"reasoning ":"Forplantingtasks ,inventoryinformationisuseless
.Innearbyblocks ,thereisfarmlandandwheat ,whichmeansyou
succeedtoplantthewheatseed.",
"success ":true ,
"critique ":""
}
INPUT:
Inventory(11/36):{...,’rotten_flesh ’:1}
Task:Kill1zombie
Context:...
RESPONSE
{
```

36 

```
"reasoning ":"Youhaverottenfleshinyourinventory ,whichmeans
yousuccessfullykilledonezombie .",
"success ":true ,
"critique ":""
}
INPUT:
Hunger:20.0/20.0
Inventory(11/36):...
Task:Eat1...
Context:...
RESPONSE
{
"reasoning ":"Foralleatingtask ,iftheplayer ’shungeris20.0 ,
thentheplayersuccessfullyatethefood.",
"success ":true ,
"critique ":""
}
INPUT:
Nearbyblocks:chest
Inventory(28/36):{’rail ’:1,’coal ’:2,’oak_planks ’:13,’
copper_block ’:1,’diorite ’:7,’cooked_beef ’:4,’granite ’:22,’
cobbled_deepslate ’:23,’feather ’:4,’leather ’:2,’
cooked_chicken ’:3,’white_wool ’:2,’stick ’:3,’black_wool ’:1,
’stone_sword ’:2,’stone_hoe ’:1,’stone_axe ’:2,’stone_shovel ’:
2,’cooked_mutton ’:4,’cobblestone_wall ’:18,’crafting_table ’:
1,’furnace ’:1,’iron_pickaxe ’:1,’stone_pickaxe ’:1,’
raw_copper ’:12}
Chests:
(81,131,16):{’andesite ’:2,’dirt ’:2,’cobblestone ’:75,’
wooden_pickaxe ’:1,’wooden_sword ’:1}
Task:Deposituselessitemsintothechestat(81,131,16)
Context:...
RESPONSE
{
"reasoning ":"Youhave28itemsinyourinventoryafterdepositing
,whichismorethan20.Youneedtodepositmoreitemsfromyour
inventorytothechest.",
"success ":false ,
"critique ":"Depositmoreuselessitemssuchascopper_block ,
diorite ,granite ,cobbled_deepslate ,feather ,andleathertomeet
therequirementofhavingonly20occupiedslotsinyourinventory
."
}
```

## **A.6 System-level Comparison between VOYAGER and Prior Works** 

We make a system-level comparison in Table. A.2. Voyager stands out as the only method featuring a combination of automatic curriculum, iterative planning, and a skill library. Moreover, it learns to play Minecraft without the need for any gradient update. 

37 

Table A.2: System-level comparison between VOYAGER and prior works. 

||VPT [8]|DreamerV3 [69]|DECKARD [53|]<br>DEPS [55]|Plan4MC [71]|VOYAGER|
|---|---|---|---|---|---|---|
|Demos|Videos|None|Videos|None|None|None|
|Rewards|Sparse|Dense|Sparse|None|Dense|None|
|Observations|Pixels Only|Pixels &<br>Meta|Pixels &<br>Inventory|Feedback &<br>Inventory|Pixels &<br>Meta|Feedback &<br>Meta &<br>Inventory|
|Actions|Keyboard<br>&<br>Mouse|Discrete|Keyboard<br>&<br>Mouse|Keyboard<br>&<br>Mouse|Discrete|Code|
|Automatic<br>Curriculum|||✓|||✓<br>(in-context<br>GPT-4<br>pro-<br>posal)|
|Iterative Plan-<br>ning||||✓||✓<br>(3<br>types<br>of<br>feedback)|
|Skill Library|||||✓<br>(pre-defned)|✓<br>(self-<br>generated)|
|Gradient-Free||||||✓|



## **B Experiments** 

## **B.1 Experimental Setup** 

Our simulation environment is built upon MineDojo [23] and utilizes Mineflayer [52] JavaScript APIs for motor controls (Sec. A.4.2). Additionally, we incorporate many `bot.chat()` into Mineflayer functions to provide abundant environment feedback and implement various condition checks along with try-catch exceptions for continuous execution. If the bot dies, it is resurrected near the closest ground, and its inventory is preserved for uninterrupted exploration. The bot recycles its crafting table and furnace after program execution. For detailed implementations, please refer to our codebase. 

## **B.2 Baselines** 

**ReAct** [29] uses chain-of-thought prompting [46] by generating both reasoning traces and action plans with LLMs. We provide it with our environment feedback and the agent states as observations. ReAct undergoes one round of code generation from scratch, followed by three rounds of code refinement. This process is then repeated until the maximum prompting iteration is reached. 

**Reflexion** [30] is built on top of ReAct [29] with self-reflection to infer more intuitive future actions. We provide it with environment feedback, the agent states, execution errors, and our self-verification module. Similar to ReAct, Reflexion undergoes one round of code generation from scratch, followed by three rounds of code refinement. This process is then repeated until the maximum prompting iteration is reached. 

**AutoGPT** [28] is a popular software tool that automates NLP tasks by decomposing a high-level goal into multiple subgoals and executing them in a ReAct-style loop. We re-implement AutoGPT by using GPT-4 to do task decomposition and provide it with the agent states, environment feedback, and execution errors as observations for subgoal execution. Compared with VOYAGER, AutoGPT lacks the skill library for accumulating knowledge, self-verification for assessing task success, and automatic curriculum for open-ended exploration. During each subgoal execution, if no execution error occurs, we consider the subgoal completed and proceed to the next one. Otherwise, we refine the program until three rounds of code refinement (equivalent to four rounds of code generation) are completed, and then move on to the next subgoal. If three consecutive subgoals do not result in acquiring a new item, we replan by rerunning the task decomposition. 

The task is “explore the world and get as many items as possible” for all baselines. 

38 

Table A.3: Comparison between VOYAGER and baselines. 

||ReAct [29]<br>Refexion [30]<br>AutoGPT [28]<br>VOYAGER|
|---|---|
|||
|Chain-of-Thought [46]<br>Self Verifcation<br>Environment Feedback<br>Execution Errors<br>Agent State<br>Skill Library<br>Automatic Curriculum|✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓<br>✓|



**==> picture [396 x 126] intentionally omitted <==**

Figure A.1: Minecraft item icons with corresponding names. 

## **B.3 Ablations** 

We ablate 6 design choices (automatic curriculum, skill library, environment feedback, execution errors, self-verification, and GPT-4 for code generation) in VOYAGER and study their impact on exploration performance. 

- **Manual Curriculum** : We substitute the automatic curriculum with a manually designed curriculum for mining a diamond: “Mine 3 wood log”, “Craft 1 crafting table”, “Craft 1 wooden pickaxe”, “Mine 11 cobblestone”, “Craft 1 stone pickaxe”, “Craft 1 furnace”, “Mine 3 iron ore”, “Smelt 3 iron ore”, “Craft 1 iron pickaxe”, “Mine 1 diamond”. A manual curriculum requires human effort to design and is not scalable for open-ended exploration. 

- **Random Curriculum** : We curate 101 items obtained by VOYAGER and create a random curriculum by randomly selecting one item as the next task. 

- **w/o Skill Library** : We remove the skill library, eliminating skill retrieval for code generation. 

- **w/o Environment Feedback** : We exclude environment feedback (chat log) from the prompt for code generation. 

- **w/o Execution Errors** : We exclude execution errors from the prompt for code generation. 

- **w/o Self-Verification** : For each task, we generate code without self-verification and iteratively refine the program for 3 rounds (equivalent to 4 rounds of code generation in total). 

- **GPT-3.5** : We replace GPT-4 with GPT-3.5 for code generation. We retain GPT-4 for the automatic curriculum and the self-verification module. 

## **B.4 Evaluation Results** 

## **B.4.1 Significantly Better Exploration** 

The meaning of each icon in Fig. 1 is shown in Fig. A.1. 

We run three trials for each method. The items collected by VOYAGER in each trial is 

39 

- **Trial 1** : ‘iron_ingot’, ‘stone_shovel’, ‘iron_leggings’, ‘fishing_rod’, ‘pufferfish’, ‘oak_log’, ‘cooked_mutton’, ‘green_dye’, ‘flint’, ‘chest’, ‘iron_sword’, ‘string’, ‘ender_pearl’, ‘raw_copper’, ‘crafting_table’, ‘cactus’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘copper_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘scaffolding’, ‘stick’, ‘porkchop’, ‘copper_block’, ‘gravel’, ‘grass_block’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’, ‘oak_sapling’, ‘coal’, ‘bamboo’, ‘wooden_pickaxe’, ‘rotten_flesh’, ‘cooked_porkchop’, ‘cod’, ‘iron_boots’, ‘lightning_rod’, ‘diorite’, ‘water_bucket’, ‘shears’, ‘furnace’, ‘andesite’, ‘granite’, ‘bucket’, ‘wooden_sword’, ‘sandstone’, ‘iron_helmet’, ‘raw_iron’, ‘sand’, ‘acacia_log’, ‘cooked_cod’, ‘oak_planks’, ‘azure_bluet’, ‘iron_shovel’, ‘acacia_planks’, ‘shield’, ‘iron_axe’, ‘iron_chestplate’, ‘cobblestone’; 

- **Trial 2** : ‘iron_ingot’, ‘tuff’, ‘stone_shovel’, ‘iron_leggings’, ‘fishing_rod’, ‘cooked_mutton’, ‘spruce_planks’, ‘gunpowder’, ‘amethyst_shard’, ‘chest’, ‘string’, ‘cooked_salmon’, ‘iron_sword’, ‘raw_copper’, ‘crafting_table’, ‘torch’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘copper_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘stick’, ‘amethyst_block’, ‘salmon’, ‘calcite’, ‘gravel’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’, ‘spyglass’, ‘coal’, ‘wooden_pickaxe’, ‘cod’, ‘iron_boots’, ‘lily_pad’, ‘cobbled_deepslate’, ‘lightning_rod’, ‘snowball’, ‘stone_axe’, ‘smooth_basalt’, ‘diorite’, ‘water_bucket’, ‘furnace’, ‘andesite’, ‘bucket’, ‘granite’, ‘shield’, ‘iron_helmet’, ‘raw_iron’, ‘cobblestone’, ‘spruce_log’, ‘cooked_cod’, ‘tripwire_hook’, ‘stone_hoe’, ‘iron_chestplate’, ‘stone_sword’; 

- **Trial 3** : ‘spruce_planks’, ‘dirt’, ‘shield’, ‘redstone’, ‘clock’, ‘diamond_sword’, ‘iron_chestplate’, ‘stone_pickaxe’, ‘leather’, ‘string’, ‘chicken’, ‘chest’, ‘diorite’, ‘iron_leggings’, ‘black_wool’, ‘cobblestone_wall’, ‘cobblestone’, ‘cooked_chicken’, ‘feather’, ‘stone_sword’, ‘raw_gold’, ‘gravel’, ‘birch_planks’, ‘coal’, ‘cobbled_deepslate’, ‘oak_planks’, ‘iron_pickaxe’, ‘granite’, ‘tuff’, ‘crafting_table’, ‘iron_helmet’, ‘stone_hoe’, ‘iron_ingot’, ‘stone_axe’, ‘birch_boat’, ‘stick’, ‘sand’, ‘bone’, ‘raw_iron’, ‘beef’, ‘rail’, ‘oak_sapling’, ‘kelp’, ‘gold_ingot’, ‘birch_log’, ‘wheat_seeds’, ‘cooked_mutton’, ‘furnace’, ‘arrow’, ‘stone_shovel’, ‘white_wool’, ‘andesite’, ‘jungle_slab’, ‘mutton’, ‘iron_sword’, ‘copper_ingot’, ‘diamond’, ‘torch’, ‘oak_log’, ‘cooked_beef’, ‘copper_block’, ‘flint’, ‘bone_meal’, ‘raw_copper’, ‘wooden_pickaxe’, ‘iron_boots’, ‘wooden_sword’. 

The items collected by ReAct [29] in each trial is 

- **Trial 1** : ‘bamboo’, ‘dirt’, ‘sand’, ‘wheat_seeds’; 

- **Trial 2** : ‘dirt’, ‘rabbit’, ‘spruce_log’, ‘spruce_sapling’; 

- **Trial 3** : ‘dirt’, ‘pointed_dripstone’; 

The items collected by Reflexion [30] in each trial is 

- **Trial 1** : ‘crafting_table’, ‘orange_tulip’, ‘oak_planks’, ‘oak_log’, ‘dirt’; 

- **Trial 2** : ‘spruce_log’, ‘dirt’, ‘clay_ball’, ‘sand’, ‘gravel’; 

- **Trial 3** : ‘wheat_seeds’, ‘oak_log’, ‘dirt’, ‘birch_log’, ‘sand’. 

The items collected by AutoGPT [28] in each trial is 

- **Trial 1** : ‘feather’, ‘oak_log’, ‘leather’, ‘stick’, ‘porkchop’, ‘chicken’, ‘crafting_table’, ‘wheat_seeds’, ‘oak_planks’, ‘dirt’, ‘mutton’; 

- **Trial 2** : ‘wooden_pickaxe’, ‘iron_ingot’, ‘stone’, ‘coal’, ‘spruce_planks’, ‘string’, ‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘andesite’, ‘furnace’, ‘torch’, ‘spruce_sapling’, ‘granite’, ‘iron_pickaxe’, ‘stone_pickaxe’, ‘wooden_axe’, ‘raw_iron’, ‘stick’, ‘spruce_log’, ‘dirt’, ‘cobblestone’; 

- **Trial 3** : ‘wooden_shovel’, ‘wooden_pickaxe’, ‘iron_ingot’, ‘stone’, ‘cod’, ‘coal’, ‘oak_log’, ‘flint’, ‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘furnace’, ‘andesite’, ‘torch’, ‘granite’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘stone_pickaxe’, ‘raw_iron’, ‘stick’, ‘gravel’, ‘oak_planks’, ‘dirt’, ‘iron_axe’, ‘cobblestone’. 

40 

**==> picture [396 x 211] intentionally omitted <==**

Figure A.2: Map coverage: Two bird’s eye views of Minecraft maps. VOYAGER is able to traverse 2 _._ 3 _×_ longer distances compared to baselines while crossing diverse terrains. Trajectories are plotted based on the positions where each agent interacts with GPT-4. 

## **B.4.2 Extensive Map Traversal** 

Agent trajectories for map coverage are displayed in Fig. A.2. Fig. 7 is plotted based on Fig. A.2 by drawing the smallest circle enclosing each trajectory. The terrains traversed by VOYAGER in each trial is 

- **Trial 1** : ‘meadow’, ‘desert’, ‘river’, ‘savanna’, ‘forest’, ‘plains’, ‘bamboo_jungle’, ‘dripstone_caves’; 

- **Trial 2** : ‘snowy_plains’, ‘frozen_river’, ‘dripstone_caves’, ‘snowy_taiga’, ‘beach’; 

- **Trial 3** : ‘flower_forest’, ‘meadow’, ‘old_growth_birch_forest’, ‘snowy_slopes’, ‘frozen_peaks’, ‘forest’, ‘river’, ‘beach’, ‘ocean’, ‘sunflower_plains’, ‘plains’, ‘stony_shore’. 

The terrains traversed by ReAct [29] in each trial is 

- **Trial 1** : ‘plains’, ‘desert’, ‘jungle’; 

- **Trial 2** : ‘snowy_plains’, ‘snowy_taiga’, ‘snowy_slopes’; 

- **Trial 3** : ‘dark_forest’, ‘dripstone_caves’, ‘grove’, ‘jagged_peaks’. 

The terrains traversed by Reflexion [30] in each trial is 

- **Trial 1** : ‘plains’, ‘flower_forest’; 

- **Trial 2** : ‘snowy_taiga’; 

- **Trial 3** : ‘old_growth_birch_forest’, ‘river’, ‘ocean’, ‘beach’, ‘plains’. 

The terrains traversed by AutoGPT [28] in each trial is 

- **Trial 1** : ‘plains’, ‘dripstone_caves’, ‘savanna’, ‘meadow’; 

- **Trial 2** : ‘snowy_taiga’; 

- **Trial 3** : ‘plains’, ‘stony_shore’, ‘forest’, ‘ocean’. 

## **B.4.3 Efficient Zero-Shot Generalization to Unseen Tasks** 

The results of zero-shot generalization to unseen tasks for the other two tasks are presented in Fig. A.3. Similar to Fig. 8, VOYAGER consistently solves all tasks, while the baselines are unable to solve any 

41 

**==> picture [396 x 143] intentionally omitted <==**

Figure A.3: Zero-shot generalization to unseen tasks. We visualize the intermediate progress of each method on the other two tasks. We do not plot ReAct and Reflexion since they do not make any meaningful progress. 

task within 50 prompting iterations. Our skill library, constructed from lifelong learning, not only enhances VOYAGER’s performance but also provides a boost to AutoGPT [28]. 

## **B.4.4 Accurate Skill Retrieval** 

We conduct an evaluation of our skill retrieval (309 samples in total) and the results are in Table. A.4. The top-5 accuracy standing at 96.5% suggests our retrieval process is reliable (note that we include the top-5 relevant skills in the prompt for synthesizing a new skill). 

Table A.4: Skill retrieval accuracy. 

|Top-1 Acc|Top-2 Acc|Top-3 Acc|Top-4 Acc|Top-5 Acc|
|---|---|---|---|---|
|80_._2_±_3_._0|89_._3_±_1_._8|93_._2_±_0_._7|95_._2_±_1_._8|96_._5_±_0_._3|



## **B.4.5 Robust to Model Variations** 

In the main paper, all of Voyager’s experiments are conducted with `gpt-4-0314` . We additionally run new experiments with `gpt-4-0613` and find that the performance is roughly the same (Fig. A.4). It demonstrates that Voyager is robust to model variations. 

**==> picture [278 x 166] intentionally omitted <==**

Figure A.4: VOYAGER’s performance with GPT-4-0314 and GPT-4-0613. 

42 

