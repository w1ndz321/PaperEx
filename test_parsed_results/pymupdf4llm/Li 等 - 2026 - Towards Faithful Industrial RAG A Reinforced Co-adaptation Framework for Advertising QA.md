# **Towards Faithful Industrial RAG: A Reinforced Co-adaptation Framework for Advertising QA** 

**Wenwei Li** _[∗]_ **, Ming Xu** _[∗]_ **, Tianle Xia, Lingxiang Hu, Yiding Sun, Linfang Shang Liqun Liu** _[†]_ , **Peng Shu** , **Huan Yu** , **Jie Jiang** 

Tencent 

{wenweiwwli,flemingxu,tianlexia,lingxianghu,emanuelsun,faelynshang}@tencent.com {liqunliu,archershu,huanyu,zeus}@tencent.com 

> _∗_ Equal contribution. 

> _†_ Corresponding author. 

## **Abstract** 

Industrial advertising question answering (QA) is a high-stakes task in which hallucinated content, particularly fabricated URLs, can lead to financial loss, compliance violations, and legal risk. Although Retrieval-Augmented Generation (RAG) is widely adopted, deploying it in production remains challenging because industrial knowledge is inherently relational, frequently updated, and insufficiently aligned with generation objectives. We propose a reinforced co-adaptation framework that jointly optimizes retrieval and generation through two components: (1) Graph-aware Retrieval (GraphRAG), which models entity-relation structure over a high-citation knowledge subgraph for multihop, domain-specific evidence selection; and (2) evidence-constrained reinforcement learning via Group Relative Policy Optimization (GRPO) with multi-dimensional rewards covering faithfulness, style compliance, safety, and URL validity. Experiments on an internal advertising QA dataset show consistent gains across expert-judged dimensions including accuracy, completeness, and safety, while reducing the hallucination rate by 72%. A two-week online A/B test demonstrates a 28.6% increase in like rate, a 46.2% decrease in dislike rate, and a 92.7% reduction in URL hallucination. The system has been running in production for over half a year and has served millions of QA interactions. 

## **1 Introduction** 

Online advertising platforms are complex, fastevolving ecosystems where intelligent customer service (ICS) systems are critical for operational efficiency and user satisfaction (Gao et al., 2025). These systems must handle diverse intents, from pre-sales consultations to post-sales compliance appeals, under frequently updated internal policies (e.g., ad review guidelines, account systems, reimbursement protocols) that are often behind private knowledge barriers (Sharma et al., 2024). 

**==> picture [219 x 103] intentionally omitted <==**

Figure 1: Traditional QA vs. our approach over a shared knowledge base. Given the same user query and knowledge items A, B, C, D, traditional methods often yield **incomplete** , **hallucinated** , **over-generated** , or **verbose** answers. Our method produces an **exact** answer that remains complete, faithful, and concise. 

In this high-stakes setting, even minor factual errors can trigger compliance risks, user harm, and direct financial losses, and fabricated structured items such as URLs are particularly costly (Ji et al., 2023; Ming et al., 2025). As illustrated in Figure 1, conventional pipelines may produce incomplete, hallucinated, over-generated, or verbose answers, whereas our framework targets concise and evidence-grounded responses. 

Retrieval-Augmented Generation (RAG) is a standard paradigm for grounding LLMs in external evidence (Lewis et al., 2020; Gao et al., 2024), yet production advertising question answering (QA) reveals three key gaps. First, industrial knowledge is relational and process-driven (e.g., products, rules, procedures), where single-shot hybrid retrieval can miss multi-hop dependencies; graphbased retrieval such as GraphRAG addresses this by explicitly modeling entities and relations for crossdocument reasoning (Edge et al., 2024). Second, simply expanding context length is insufficient: under the “lost in the middle” effect, models may fail to reliably use evidence in long inputs, motivating targeted evidence selection (Liu et al., 2023). Third, generation must satisfy strict style and compliance 

1 

constraints, yet even strong models may deviate from provided context under unanswerable or counterfactual inputs (Ming et al., 2025; Rakin et al., 2024); while reinforcement learning (Schulman et al., 2017a; Rafailov et al., 2023) can align generation with task constraints, and post-hoc methods such as SelfCheckGPT (Manakul et al., 2023) can detect unsupported content, treating retrieval and generation as isolated stages leaves a coordination gap. 

To address these gaps, we propose an end-toend reinforced co-adaptation framework that jointly optimizes retrieval and evidence-grounded generation. It has two key components: (1) **Graphaware Retrieval** via GraphRAG, which models relationships between products, rules, and processes to support multi-hop reasoning and terminology alignment (Edge et al., 2024); and (2) **Evidence-constrained Reinforcement Learning (RL)** , which aligns the generator with retrieved evidence using multi-dimensional rewards that encourage faithfulness while enforcing style, safety, and URL validity. 

Our contributions are as follows: 

- We propose a co-adaptation framework that jointly optimizes GraphRAG-based retrieval and an RL-tuned generator, achieving superior alignment between retrieved domain knowledge and generated responses. 

- We design a multi-dimensional RL objective covering faithfulness, style compliance, safety, and URL validity, explicitly penalizing unsupported content and hallucinated links. 

- We deploy the system on a large-scale advertising platform, serving millions of QA interactions over half a year. A two-week A/B test shows a 28.6% like-rate increase, a 46.2% dislike-rate reduction, and a 92.7% reduction in URL hallucination. 

## **2 Methodology** 

## **2.1 Problem Formulation** 

We formulate advertising QA as a constrained conditional generation task (Figure 2). Given a user query _q_ and a dynamically updated private knowledge base _K_ , the system retrieves a relevant evidence set _D_ = _{d_ 1 _, . . . , dk}_ . The generator _πθ_ produces a response _A_ that maximizes _P_ ( _A | q, D_ ) 

subject to constraints _C_ , including zero URL hallucinations, domain-specific style compliance, and safety requirements. 

## **2.2 Graph-aware Retrieval** 

To address the limitations of traditional hybrid retrieval methods (e.g., BGE + BM25) in handling complex multi-hop dependencies and domainspecific terminology, we propose a Graph-aware Retrieval module that integrates GraphRAG with a carefully curated, high-citation knowledge base, complemented by a parallel retrieval architecture for industrial-scale deployment. 

**High-Citation Knowledge Base.** GraphRAG enhances retrieval but introduces substantial computational overhead. To balance effectiveness and efficiency, we maintain a high-citation knowledge base _Kh ⊂ K_ through traffic-driven feedback. We accumulate recall frequency for each knowledge chunk from production query logs as a “citation heat” indicator, and periodically select the top- _N_ % most frequently cited items to form _Kh_ . This curated subset serves as the subgraph for GraphRAG, reducing traversal complexity while preserving effectiveness through automatic rolling updates. 

**GraphRAG Architecture.** We construct a knowledge graph _G_ = ( _V, E_ ) over _Kh_ via entity extraction and relation identification, with community detection partitioning the graph into hierarchical subgraphs for semantic aggregation. The retrieval layer supports dynamic routing between hybrid retrieval and graph-based traversal, balancing efficiency for simple queries with multi-hop reasoning for complex ones. High-citation subgraph pruning constrains retrieval scope, and incremental updates maintain temporal currency without full reconstruction. 

**Parallel Retrieval Architecture.** To mitigate GraphRAG latency while maximizing recall, we execute GraphRAG and traditional RAG channels concurrently. The GraphRAG channel performs asynchronous graph traversal over _Kh_ for multihop reasoning, while the traditional RAG channel uses BGE + BM25 hybrid retrieval with multi-path query rewriting that decomposes complex queries into parallel sub-queries. Results from both channels are merged and deduplicated to form the final evidence set _D_ = _{d_ 1 _, . . . , dk}_ . 

2 

**==> picture [432 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
Graph-aware Retrieval Module Evidence-constrained Generation & RL-tuned<br>GraphRAG Channel Traditional RAG Channel Query RL-tuned Generator<br>High-Citation Sources Query Rewriting (Qwen3-32B-RL)<br>sub-querysub-querysub-query<br>Evidence Set<br>Citation Self-iterative<br>Heat Updates Vector BM25 Reward Models<br>Faithfulness Safety GRPO<br>Graph Traversal & Update<br>Multi-hop Reasoning (Groundtruth (Policy violation<br> comparison) check)<br>  Style Compliance Link<br>(Domain  (Valid/hallucinated<br>Merge & formatting) URLs)<br>Deduplication<br>Multi-dimensional Reward<br>Evidence Set<br>Zero-URL Hallucination<br>Private Retrieval Module<br>Knowledge （ GraphRAG + Vector + RL-tuned Generator Domain-specific Style<br>Query Base BM25 ） Satety<br>Evidence Set Answer<br>**----- End of picture text -----**<br>


Figure 2: System overview. Given a user query _q_ and a private knowledge base _K_ , the retrieval system constructs an evidence set _D_ via two parallel channels: a GraphRAG channel over a high-citation knowledge base _Kh_ and a traditional RAG channel with query rewriting and BGE + BM25 hybrid retrieval. Results are merged and deduplicated. The RL-tuned generator then produces a response optimized by GRPO with multi-dimensional rewards for faithfulness, style compliance, safety, and URL validity. 

## **2.3 Evidence-constrained Generation** 

The generation module centers on an RL-tuned generator (Qwen3-32B-RL). While supervised finetuning establishes foundational formatting, reinforcement learning is critical for steering the model toward stable, safe, and hallucination-free responses under strict industrial constraints. 

We optimize the generator using GRPO (Shao et al., 2024), whose group-based mechanism stabilizes training under noisy reward signals. Unlike PPO(Schulman et al., 2017b), which requires a separate critic model, GRPO estimates the baseline from group rewards, reducing memory overhead and training instability. This is particularly valuable for industrial applications where reward signals are inherently noisy due to the subjective nature of style and safety assessments. 

We design a multi-dimensional reward function: 

**==> picture [191 x 12] intentionally omitted <==**

where _λi_ are weighting coefficients. Following preliminary experiments, we set _λ_ 3 = 2 _._ 0 and _λ_ 4 = 2 _._ 0 to prioritize safety and hallucination reduction, with _λ_ 1 = _λ_ 2 = 1 _._ 0. The reward components are: 

- **Evidence Faithfulness (** _Rf_ **)** : Measures alignment with the ground-truth answer via pairwise 

LLM-as-judge comparison. 

- **Style Compliance (** _Rs_ **)** : Evaluates adherence to advertising domain conventions, including tone, professionalism, and formatting. 

- **Safety (** _Ra_ **)** : Detects platform policy violations and ensures regulatory compliance. 

- **URL Validity (** _Rh_ **)** : Rewards valid URLs and penalizes hallucinated ones. A URL is valid if it appears in the evidence _D_ , or if its prefix belongs to an approved pool and its HTTP status code is in _{_ 200 _,_ 301 _,_ 302 _}_ . 

The full reward computation procedure, including URL extraction and validation details, is provided in Algorithm 1 in the Appendix. 

## **3 Experiments** 

We evaluate our approach using both offline and online metrics. 

## **3.1 Experimental Setting** 

**Dataset.** We evaluate on the **Advertising QA Dataset** , an internal Chinese advertising customerservice dataset with 3,000 expert-annotated question–answer pairs. For out-of-domain generalization, we use **FaithEval** (Ming et al., 2025), which tests faithfulness under unanswerable ques- 

3 

tions, counterfactual contexts, and inconsistent information. 

**Evaluation Protocol.** We compare systems along two axes: (i) **retrieval** , where we contrast Base RAG (a standard RAG pipeline with a reranker) with GraphRAG, and (ii) **generation backbones** , where we evaluate open-source and proprietary models as well as our RL-tuned model. 

We use a hybrid evaluation protocol. ROUGE-L (0–100) is computed automatically, while Accuracy, Completeness, Clarity, Style, and Safety are rated by human experts on a 0–10 scale. Hallucination Rate is also assessed by human experts at the case level: for each case, if the answer contains any fabricated or unsupported content, we count it as one hallucinated case. Formally, given _N_ cases and an indicator I[ _·_ ], we report 

**==> picture [210 x 33] intentionally omitted <==**

ROUGE-L measures lexical overlap with the reference; lower HR indicates fewer hallucinated cases. 

**Models.** We evaluate five representative backbones: DeepSeek-V3.2 (DeepSeek-AI et al., 2025), GPT-5.2 (OpenAI, 2025), Qwen3-32B (Qwen Team, 2025), Qwen3-32B-SFT, and Qwen3-32BRL (ours). All evaluated models support reasoning capabilities; to match production latency constraints, we evaluate all models in non-thinking mode for a fair comparison. 

This model set covers strong open-source and commercial baselines, isolates the impact of RL (vs. SFT) on the same backbone, and tests robustness across model families. 

## **3.2 Main Results** 

Table 1 reports the main offline results. Replacing Base RAG with GraphRAG consistently improves quality and reduces hallucinations. DeepSeek-V3.2 improves ROUGE-L from 33.27 to 37.00 (+3.73) and reduces Hallucination Rate from 0.0077 to 0.0030 (61% relative reduction). Similar patterns hold for GPT-5.2 (ROUGE-L: 32.82 _→_ 35.88; Hallucination Rate: 0.0057 _→_ 0.0023, 60%) and Qwen3-32B (ROUGE-L: 29.39 _→_ 32.96; Hallucination Rate: 0.0117 _→_ 0.0060). Graph-aware multihop evidence aggregation strengthens both coverage and grounding beyond hybrid retrieval alone. 

RL provides additional gains beyond retrieval improvements. Under GraphRAG, Qwen3-32B-RL 

( _Ours_ ) improves ROUGE-L from 33.82 to 35.49 over Qwen3-32B-SFT (+1.67), and lowers Hallucination Rate from 0.0047 to 0.0013 (72% relative reduction). Even under Base RAG, Qwen3-32B-RL achieves a 0.0017 Hallucination Rate, indicating that evidence-constrained RL targets hallucination behaviors that supervised fine-tuning alone cannot eliminate. 

The complementary effect between GraphRAG and RL is evident across all metrics. GraphRAG primarily improves coverage-related metrics (ROUGE-L, Completeness), while RL enhances reliability and compliance metrics (Style, Safety, Hallucination Rate). Their combination achieves the best overall performance, with our final system outperforming the strongest baseline (DeepSeek-V3.2 with GraphRAG) on Hallucination Rate (0.0030 vs. 0.0013) while maintaining competitive quality scores. 

## **3.3 GraphRAG Effectiveness** 

We evaluate graph-aware retrieval both offline and online. 

**Offline Evaluation.** We assess retrieval via sideby-side expert comparison and knowledge recall analysis. 

**Knowledge Recall Enhancement.** Figure 3 shows progressive improvements in knowledge recall. Effective knowledge chunks per query increase from 3.9 (Base RAG) to 4.5 (GraphRAG) to 6.3 (parallel retrieval), a 61.5% overall improvement. Recall effectiveness improves from 73.6% to 90.5%, demonstrating that GraphRAG combined with parallel retrieval substantially enriches contextual information. 

**Retrieval Quality Optimization.** In expert evaluation, the Good:Same:Bad ratio reaches 32.4%:64.9%:2.7% at retrieval. The Good ratio is 12 _×_ higher than Bad, indicating effective noise filtering. 

**End-to-End Performance.** The end-to-end Good:Same:Bad ratio reaches 24.3%:71.6%:4.1%, with positive gains outweighing negative impacts by 6 _×_ . 

**Online A/B Testing.** We deployed at 50% traffic. Table 2 shows consistent improvements: like rate increases from 0.21% to 0.27% (+28.6%), dislike _−_ rate decreases from 0.26% to 0.18% ( 30.8%), and average conversation turns increase from 1.54 to 1.81 (+17.5%), indicating improved user engagement. 

4 

|**Metric**|**DeepSeek-V3.2**<br>Base RAG<br>GraphRAG|**GPT-5.2**<br>Base RAG<br>GraphRAG|**Qwen3-32B**<br>Base RAG<br>GraphRAG|**Qwen3-32B-SFT**<br>Base RAG<br>GraphRAG|B|**Qwen3-32B-RL**<br>ase RAG<br>**Ours**|
|---|---|---|---|---|---|---|
|**ROUGE-L**_↑_<br>**Accuracy**_↑_<br>**Completeness**_↑_<br>**Clarity**_↑_<br>**Style**_↑_<br>**Safety**_↑_<br>**Hallucination Rate**_↓_|33.27<br>**37.00**<br>7.82<br>8.37<br>6.78<br>**7.10**<br>8.96<br>**8.99**<br>8.19<br>8.25<br>9.94<br>9.93<br>0.0077<br>0.0030|32.82<br>35.88<br>7.94<br>**8.39**<br>6.70<br>7.08<br>8.92<br>8.97<br>8.14<br>8.25<br>9.95<br>9.96<br>0.0057<br>0.0023|29.39<br>32.96<br>7.25<br>7.82<br>6.20<br>6.66<br>8.52<br>8.74<br>7.82<br>8.03<br>9.88<br>9.91<br>0.0117<br>0.0060|30.79<br>33.82<br>7.50<br>8.10<br>6.43<br>6.91<br>8.82<br>8.94<br>8.07<br>8.19<br>9.95<br>9.94<br>0.0117<br>0.0047||31.40<br>35.49<br>7.85<br>8.26<br>6.46<br>6.99<br>8.83<br>8.95<br>8.27<br>**8.33**<br>9.97<br>**9.99**<br>0.0017<br>**0.0013**|



Table 1: Main experimental results. **Ours** refers to Qwen3-32B-RL with GraphRAG. Best results in **bold** , second best underlined. 

**==> picture [220 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
Knowledge Recall Enhancement<br>8 Chunks/Query 100<br>Recall Eff. (%) 90.5%<br>84.2%<br>6.3<br>6 73.6% 80<br>4.5<br>60<br>3.9<br>4<br>40<br>2<br>20<br>0 0<br>Base RAG GraphRAG Parallel<br>Figure 3: Knowledge recall enhancement across Base<br>RAG, GraphRAG, and Parallel retrieval. Effective<br>chunks pre query and recall effectiveness in percent.<br>1.0<br>0.8<br>0.6<br>0.4<br>Style Safety<br>0.2 Faithfulness Overall<br>Link<br>0.0<br>20 40 60 80 100<br>Training Steps<br>Chunks/Query Recall Eff. (%)<br>Normalized Performance<br>**----- End of picture text -----**<br>


Figure 4: Training dynamics of multi-dimensional reward components during RL. 

## **3.4 RL Reward Effectiveness** 

Figure 4 shows consistent improvement across all reward components during RL fine-tuning. With only 1,000 training samples, all metrics rapidly improve within 100 steps and converge, demonstrating efficient reward design. 

The reward components exhibit distinct optimization patterns. Faithfulness and URL validity rewards show the steepest initial ascent, indicating that the model quickly learns to align with retrieved evidence and avoid hallucinated links. Style and safety rewards improve more gradually, reflecting 

|**Metric**|**Base RAG**|**Ours**|∆|
|---|---|---|---|
|Like Rate (%)|0.21|0.27|+28.6%|
|Dislike Rate (%)|0.26|0.18|_−_30.8%|
|Avg. Conv. Turns|1.54|1.81|+17.5%|



Table 2: Online A/B testing at 50% traffic. 

the nuanced nature of domain-specific tone and compliance requirements. The overall reward converges to a stable high value, suggesting that the multi-objective optimization achieves balanced improvements across all dimensions without detrimental trade-offs. 

## **3.5 Generalization on FaithEval** 

To assess whether our RL-tuned model generalizes beyond the in-domain setting, we evaluate on **FaithEval** . Figure 5 shows the results. 

Our RL-tuned model improves over Qwen3-32B on all FaithEval subsets: Unanswerable 44.60% _→_ 53.40%, Counterfactual 57.90% _→_ 64.40% (outperforming DeepSeek-V3.2 at 56.40%), and Inconsistent 63.80% _→_ 84.60%. The gains on Unanswerable and Counterfactual suggest stronger refusal behavior when context is missing or misleading. On Inconsistent, it reaches 84.60%, substantially above Qwen3-32B (63.80%) and closer to DeepSeek-V3.2 (94.80%). These results indicate improved contextual faithfulness without degrading generalization. 

## **3.6 Production Deployment 3.6.1 Offline Evaluation** 

We compare against a Base RAG + DeepSeekV3(Liu et al., 2024) baseline via expert assessment on completeness, professionalism, compliance, and hallucination. As shown in Figure 6, our method wins substantially more often than it loses, with the largest gains in professionalism (45.2% win) and compliance (41.9% win) and a low loss rate (1.1%). It also improves hallucination outcomes 

5 

**==> picture [220 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
DeepSeek-V3.2<br>100 94.8<br>84.6 Qwen3-32B<br>Qwen3-32B-RL (Ours)<br>75 68.5 67.5<br>63.8 64.4<br>54.2 53.4 56.4 57.9 55.4<br>50 44.6<br>25<br>0<br>Incons. Unans. Cfact. Overall<br>Figure 5: FaithEval generalization: accuracy (%) on In-<br>consistent, Unanswerable, Counterfactual, and Overall.<br>Completeness 29.0% 64.5% 6.5%<br>Professionalism 45.2% 53.8% 1.1%<br>Compliance 41.9% 57.0% 1.1%<br>Hallucination 11.7% 88.1% 0.1%<br>0 20 40 60 80 100<br>Percentage (%)<br>Ours Win Tie Baseline Win<br>Accuracy (%)<br>**----- End of picture text -----**<br>


Figure 5: FaithEval generalization: accuracy (%) on Inconsistent, Unanswerable, Counterfactual, and Overall. 

Figure 6: Offline evaluation comparison: win/tie/lose distribution across four dimensions. 

(7.7% win vs. 0.1% loss), supporting the benefit of co-adapting GraphRAG and RL-tuned generation. 

## **3.6.2 Online A/B Testing** 

A two-week online A/B test compares our deployed system against the Base RAG + DeepSeek-V3 baseline, with a 50%/50% traffic split (Table 3). Our method increases like rate from 0.21% to 0.27% (+28.6%), decreases dislike rate from 0.26% to _−_ 0.14% ( 46.2%), and reduces URL hallucination from 0.0041% to 0.0003% ( _−_ 92.7%). Average first-token latency rises from 2.5s to 3.1s (+24.0%), which remains acceptable in practice. Overall, the A/B results suggest that reinforced co-adaptation improves both user satisfaction and reliability under real traffic, with a manageable latency trade-off. 

## **3.6.3 Latency Analysis** 

Table 4 details the latency distribution. Query rewriting takes 690ms, parallel retrieval takes 852ms (GraphRAG) and 167ms (BGE + BM25), reranking takes 557ms, generation takes 801ms, and safety guardrails take 230ms. Total latency is 3130ms, meeting acceptable thresholds for user experience and industrial deployment. 

The latency breakdown highlights several avenues for optimization. GraphRAG retrieval incurs 

|**Metric**|**Baseline**|**Ours**|∆|
|---|---|---|---|
|Like Rate (%)|0.21|0.27|+28.6%|
|Dislike Rate (%)|0.26|0.14|_−_46.2%|
|URL Hallu. (%)|0.0041|0.0003|_−_92.7%|
|Latency (s)|2.5|3.1|+24.0%|



Table 3: Online A/B testing results (two weeks, 50% traffic). 

|**Module**|**Latency (ms)**|
|---|---|
|Query Rewriting|690|
|GraphRAG Retrieval|852|
|BGE + BM25 Retrieval|167|
|Reranking|557|
|Generation|801|
|Safety Guardrails|230|
|**Total**|**3130**|



Table 4: Latency breakdown by module. 

the largest single latency cost (852ms), which motivates our high-citation knowledge base design to constrain graph traversal and reduce overhead. Executing GraphRAG in parallel with the BGE + BM25 pipeline ensures that the slower graph-based retrieval does not block the faster hybrid channel. Generation latency (801ms) is on par with standard large language model inference, suggesting that RL fine-tuning does not introduce noticeable computational overhead relative to the base model. Safety guardrails incur an additional 230ms as postprocessing, without affecting time-to-first-token, thereby preserving system responsiveness. 

## **4 Conclusion** 

We present a reinforced co-adaptation framework to mitigate hallucinations in industrial advertising Q&A by jointly optimizing GraphRAG and an RLtuned generator guided by multi-dimensional rewards, thereby narrowing the retrieval–generation gap and reducing unsupported content and hallucinated or invalid links. Our results show that graphaware retrieval with a high-citation knowledge base balances multi-hop evidence aggregation with computational efficiency, while evidence-constrained RL further suppresses hallucinations without sacrificing domain style compliance or safety. Extensive offline evaluations, a two-week production A/B test, and over six months of deployment collectively validate that the approach improves answer reliability and user-facing quality at scale under practical latency constraints. 

6 

## **Ethics Statement** 

Our research targets high-stakes industrial advertising question answering and adheres to ethical principles that prioritize user rights. We aim to improve system reliability and safety by reducing unsupported claims and hallucinated or invalid URLs that could mislead users or introduce compliance risks. Any dataset examples are used solely for scientific analysis and do not necessarily reflect the views of the authors. All resources are intended for scientific research purposes only, contributing to the development of more secure and reliable digital platforms. 

## **References** 

- DeepSeek-AI, Aixin Liu, Aoxue Mei, Bangcai Lin, Bing Xue, Bingxuan Wang, Bingzheng Xu, Bochao Wu, Bowei Zhang, Chaofan Lin, Chen Dong, and 1 others. 2025. Deepseek-v3.2: Pushing the frontier of open large language models. _arXiv preprint arXiv:2512.02556_ . 

- Darren Edge, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. 2024. From local to global: A graph RAG approach to query-focused summarization. _arXiv preprint arXiv:2404.16130_ . 

- Tianhong Gao, Jundong Shen, Jiapeng Wang, Bei Shi, Ying Ju, Junfeng Yao, and Huiyu Yu. 2025. Benchmarking and learning real-world customer service dialogue. _arXiv preprint arXiv:2510.22143_ . 

- Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Jinliu Pan, Yuxi Bi, Yi Dai, Jiawei Sun, Meng Wang, and Haofen Wang. 2024. Retrieval-augmented generation for large language models: A survey. _arXiv preprint arXiv:2312.10997_ . 

- Gemini Team, Google. 2025. Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities. Technical report, accessed 2026-02-08. 

- Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of hallucination in natural language generation. _ACM Computing Surveys_ , 55(12):1–38. 

- Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph E. Gonzalez, Hao Zhang, and Ion Stoica. 2023. Efficient memory management for large language model serving with PagedAttention. _arXiv preprint arXiv:2309.06180_ . 

- Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, and 1 others. 2020. Retrieval-augmented generation for knowledge-intensive NLP tasks. In _Advances in Neural Information Processing Systems_ , volume 33, pages 9459–9474. 

- Aixin Liu, Bei Feng, Bing Xue, Bingxuan Wang, Bochao Wu, Chengda Lu, Chenggang Zhao, Chengqi Deng, Chenyu Zhang, Chong Ruan, and 1 others. 2024. Deepseek-v3 technical report. _arXiv preprint arXiv:2412.19437_ . 

- Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, and Percy Liang. 2023. Lost in the middle: How language models use long contexts. _arXiv preprint arXiv:2307.03172_ . Accepted to TACL 2023. 

- Potsawee Manakul, Adian Liusie, and Mark Gales. 2023. Selfcheckgpt: Zero-resource black-box hallucination detection for generative large language models. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pages 9004–9017, Singapore. Association for Computational Linguistics. 

- Yifei Ming, Senthil Purushwalkam, Shrey Pandit, Zixuan Ke, Xuan-Phi Nguyen, Caiming Xiong, and Shafiq Joty. 2025. Faitheval: Can your language model stay faithful to context, even if “the moon is made of marshmallows”. In _International Conference on Learning Representations_ . 

- OpenAI. 2025. Introducing gpt-5.2. Accessed: 202602-08. 

- Qwen Team. 2025. Qwen3-32b. Hugging Face model, accessed 2026-02-08. 

- Rafael Rafailov, Archit Sharma, Eric Mitchell, Stefano Ermon, Christopher D. Manning, and Chelsea Finn. 2023. Direct preference optimization: Your language model is secretly a reward model. In _Advances in Neural Information Processing Systems_ . 

- Salman Rakin, Md. A. R. Shibly, Zahin M. Hossain, Zeeshan Khan, and Md. Mostofa Akbar. 2024. Leveraging the domain adaptation of retrieval augmented generation models for question answering and reducing hallucination. _arXiv preprint arXiv:2410.17783_ . 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. 2017a. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ . 

- John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov. 2017b. Proximal policy optimization algorithms. _arXiv preprint arXiv:1707.06347_ . 

- Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu, Junxiao Song, Xiao Bi, Haowei Zhang, Mingchuan Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024. 

7 

Deepseekmath: Pushing the limits of mathematical reasoning in open language models. _arXiv preprint arXiv:2402.03300_ . 

- Sanat Sharma, David Seunghyun Yoon, Franck Dernoncourt, Dewang Sultania, Karishma Bagga, Mengjiao Zhang, Trung Bui, and Varun Kotte. 2024. Retrieval augmented generation for domain-specific question answering. _arXiv preprint arXiv:2404.14760_ . 

- Guangming Sheng, Chi Zhang, Zilingfeng Ye, Xibin Wu, Wang Zhang, Ru Zhang, Yanghua Peng, Haibin Lin, and Chuan Wu. 2024. HybridFlow: A flexible and efficient RLHF framework. _arXiv preprint arXiv:2409.19256_ . 

- Tencent Hunyuan Team. 2025. Hunyuan-TurboS: Advancing large language models through mambatransformer synergy and adaptive chain-of-thought. _Preprint_ , arXiv:2505.15431. 

- Qiying Yu, Zheng Zhang, Ruofei Zhu, Yufeng Yuan, Xiaochen Zuo, Yu Yue, Weinan Dai, Tiantian Fan, Gaohong Liu, Lingjun Liu, Xin Liu, Haibin Lin, Zhiqi Lin, Bole Ma, Guangming Sheng, Yuxuan Tong, Chi Zhang, Mofan Zhang, Wang Zhang, and 16 others. 2025. DAPO: An open-source LLM reinforcement learning system at scale. _arXiv preprint arXiv:2503.14476_ . 

- Yanzhao Zhang, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, An Yang, Dayiheng Liu, Junyang Lin, and 1 others. 2025. Qwen3 embedding: Advancing text embedding and reranking through foundation models. _arXiv preprint arXiv:2506.05176_ . 

- Yuze Zhao, Jintao Huang, Jinghan Hu, Xingjun Wang, Yunlin Mao, Daoze Zhang, Zeyinzi Jiang, Zhikai Wu, Baole Ai, Ang Wang, Wenmeng Zhou, and Yingda Chen. 2025. Swift: A scalable lightweight infrastructure for fine-tuning. In _Proceedings of the AAAI Conference on Artificial Intelligence_ , volume 39, pages 29733–29735. 

8 

## **A Implementation Details** 

This section details the parameter settings, end-toend pipeline implementation, and training specifics that instantiate the method described in the main paper. 

**Query rewriting and retrieval.** Multi-route query rewriting produces three rewritten variants in parallel while retaining the original user query, yielding four queries in total for retrieval. The GraphRAG component follows the standard Microsoft GraphRAG design (Edge et al., 2024), with local search used for graph traversal. The high-citation knowledge subgraph is built from the top- _N_ % most frequently cited items, with _N_ = 10. The traditional RAG channel uses hybrid retrieval with BGE + BM25 (run jointly); results from both channels are merged and deduplicated, then reranked by a lightweight Qwen3-4B reranker (Zhang et al., 2025). Finally, to fit the model context window, we truncate the reranked evidence to 8K tokens. 

**SFT stage.** The first stage is supervised finetuning with LoRA on the base model Qwen3-32B, implemented with the SWIFT infrastructure (Zhao et al., 2025). We use a learning rate of 1 _×_ 10 _[−]_[4] , train for 5 epochs on 8 _×_ NVIDIA H20 GPUs, and use 1k human-annotated dialogue samples. 

**RL stage.** The second stage uses reinforcement learning via the VERL framework (Sheng et al., 2024) and the GRPO algorithm. Training is again LoRA-based on 16 _×_ H20 GPUs, with 1k prompts and responses labeled by Gemini 2.5 Pro (Gemini Team, Google, 2025) for reward learning. The judger used to compute rewards is Hunyuan TurboS (Tencent Hunyuan Team, 2025). We train for 120 steps with batch size 16, set generation temperature to 1.0, set the maximum response length to 2K tokens, and use 8 rollouts per prompt. All reward terms are normalized before combination. For reward weights, we set higher weights for safety and hallucination-related terms. We set _λ_ 3 = 2 _._ 0 for safety and _λ_ 4 = 2 _._ 0 for hallucination and link penalty, while other weights are set to 1. Following a DAPO-style setup (Yu et al., 2025), the referencemodel KL term is removed. 

**Safety guardrails.** During streaming generation, safety guardrails post-process the output to detect and filter policy violations and hallucinated URLs 

before serving, enforcing zero-hallucination and strict safety constraints in the final response. 

## **B Reward Computation Algorithm** 

**Algorithm 1** Multi-dimensional Reward Computation 

**Require:** Generated answer _A_ , retrieved evidence _D_ = _{d_ 1 _, . . . , dk}_ , ground truth answer _Agt_ , URL prefix candidate pool _Cp_ **Ensure:** Total reward _R_ 

- 1: Extract URLs via regex: _U ←_ ExtractURLs _re_ ( _A_ ) 

- 2: Extract evidence URLs via regex: _UD ←_ ExtractURLs _re_ ( _D_ ) 

- 3: HTTP status set: _S ←{_ 200 _,_ 301 _,_ 302 _}_ 

- 4: URLs in evidence: _Uevi ←U ∩UD_ 

- 5: URLs not in evidence: _Uout ←U \ UD_ 

- 6: Prefix-approved URLs: _Upref ←{u ∈Uout |_ Prefix( _u_ ) _∈Cp}_ 

- 7: HTTP-valid URLs: _Uhttp ←{u ∈Upref |_ code( _u_ ) _∈S}_ 

- 8: Valid URLs: _Uvalid ←Uevi ∪Uhttp_ 

- 9: _Rf ← f_ faithful( _A, Agt_ ) {Pairwise comparison with ground truth using LLM-as-judge} 

- 10: _Rs ← f_ style( _A_ ) {Style evaluation using LLMas-judge} 

- 11: _Ra ← f_ safety( _A_ ) {Safety check using LLM-asjudge} 

- 12: _R_[+][{Positive][reward][for] _h[←]_[Reward][(] _[U][valid]_[)] 

- valid links} 

- 13: _Rh[−][←]_[Penalty][(] _[U][\ U][valid]_[)][ {Negative penalty] for invalid links} 

- 14: _Rh ← Rh_[+] _[−][R] h[−]_ 15: _R ← λ_ 1 _Rf_ + _λ_ 2 _Rs_ + _λ_ 3 _Ra_ + _λ_ 4 _Rh_ 16: **return** _R_ 

## **C Prompt** 

## **LLM Judger Prompt** 

You are an expert evaluator for advertising customer service answer quality. Evaluate Answer B on the three dimensions below. - Evidence Faithfulness: compare Answer A and Answer B; judge whether Answer B is G, meaning better, S, meaning tie, or B, meaning worse, than Answer A and give a brief reason. - Style Compliance and Safety: score Answer B only, for example on a 0-10 scale, and do not use G, S, or B. Dimensions: 

9 

1. Evidence Faithfulness: 

   - How well does the answer align with the provided materials through 

   - pairwise comparison? Consider semantic consistency and factual accuracy 

   - given the user query and dialogue history; penalize unsupported or 

   - contradictory claims. 

2. Style Compliance, score 0-10: 

   - Does the answer adhere to advertising domain conventions, including 

   - tone, professionalism, and domainspecific formatting requirements? 

   - Scoring: 0-2 poor. This includes informal style, off-tone responses, or wrong format. 

   - 3-4 below average. This indicates partial compliance. 

   - 5-6 acceptable. This indicates general compliance with minor gaps. 

   - 7-8 good. This indicates professional responses with consistent tone and format. 

   - 9-10 excellent. This indicates full alignment with domain conventions. 

3. Safety, score 0-10: 

   - Does the answer avoid platform policy violations and comply with 

   - regulatory standards and safety guidelines? 

   - Scoring: 0-2 severe violations. This indicates policy breach or harmful or non-compliant content. 

   - 3-4 notable issues. This indicates multiple issues or serious compliance gaps. 

"Style Compliance": 8, "Safety": 9 } 

} 

## **D Factual QA under Distracting Context** 

**Setting and results.** We construct a factual QA evaluation set from 1,000 knowledge items sampled from the production environment. Retrieved context is obtained from the actual recall pipeline so that all models receive identical inputs. All models are evaluated in non-thinking mode. Figure 7 reports accuracy for our online deployed model and leading commercial flagship models. 

**==> picture [219 x 135] intentionally omitted <==**

**----- Start of picture text -----**<br>
99.3%<br>100 93.6% 95.0% 92.2% 96.5%<br>80<br>60<br>OursDeepSeek-V3.2Kimi K2.5Doubao 1.8 HY 2.0<br>Accuracy (%)<br>**----- End of picture text -----**<br>


Figure 7: Accuracy on the factual QA evaluation set. The input context includes all relevant knowledge and distracting retrieved passages. 

- 5-6 acceptable. This indicates minor or ambiguous issues. 

- 7-8 good. This indicates compliant responses with isolated imperfections. 

- 9-10 excellent. This indicates full compliance with no risk. 

--- 

### Input: 

[Query]: {query} 

[Dialogue History]: {dialogue_history} 

[Materials]: {file} 

[Answer A]: {ans_a} 

[Answer B]: {ans_b} 

--- 

### Output in JSON only, example: 

{ 

"scores": { "Evidence Faithfulness": {"reason": "...", "grade": "G"}, 

## **E Example Dialogue Comparison** 

**Setting.** This example compares responses to an account ID query. The previous online answer contains hallucinated links marked in red, while our answer uses validated links. Sensitive platform names and domains in our answer are replaced with placeholders: [Platform Name] represents the advertising platform name, and [platform-domain.com] represents the platform domain. 

**Observation.** As shown in Figure 8, the baseline answer provides generic instructions with two hallucinated example links ( **https://example.com** ) that do not correspond to actual platform resources. In contrast, our answer delivers a structured, scenario-specific response that distinguishes between uncertified and certified account workflows, includes validated platform links with operation screenshots, and provides additional guidance for service provider and recharge account queries. This comparison illustrates how our framework 

10 

eliminates hallucinated URLs while improving answer completeness and practical utility. 

## **F Service Deployment** 

**Full-stack integration.** The service is deployed end-to-end on a large-scale advertising platform and integrated into multiple user-facing entry points, including an official website sidebar, a miniprogram client, and a standalone website. To avoid disclosing sensitive details, we describe the deployment in terms of functional modules rather than proprietary product names. 

**Online serving.** The generator is served with the vLLM framework (Kwon et al., 2023) on 2 _×_ NVIDIA H20 GPUs. The knowledge base index is hosted on an Elasticsearch cluster for scalable retrieval. On top of these components, we build the production workflow on an internal agent orchestration platform, which connects the link-related model and other internal services as tools, executes the retrieval–generation–post-check pipeline, and exposes an external-facing streaming API with an interface compatible with OpenAPI. 

**Example dialogue case.** Figure 9 shows a real dialogue from our deployed advertising QA system. The user asks about recent restrictions on mini-program landing pages in the financial credit industry. The system responds with a structured, evidence-grounded answer covering (i) qualification and entity requirements, (ii) content and presentation standards (e.g., risk disclaimers and interest-rate disclosure), (iii) interaction and technical requirements (e.g., privacy, consent, and no forced actions), and (iv) prohibited scenarios (e.g., unauthorized downloads and payment-information placement), along with compliant production suggestions. This case illustrates that the framework can deliver policy-aligned, comprehensive responses without hallucinated or non-compliant content. 

11 

## **Query:** Where can I find the Account ID? 

## **Previous Asnwer** 

- You can view the Account ID in the advertiser list of the service provider system. The specific steps are as follows: 

1. Log in to the service provider system; 

2. Click “Account List” in the workbench; 

3. In the account list, you can view the names and IDs of each account. 

- In addition, you can use the filtering function for account names and IDs to perform precise or fuzzy searches. Account names support fuzzy matching queries, and Account IDs support exact matching queries. For further queries on Account IDs for certified or uncertified accounts, please refer to the detailed steps and screenshots in the following links: 

- Account ID query for certified accounts **https://example.com** 

- • Account ID query for uncertified accounts **https://example.com** 

- **Our Method** The method for viewing advertising Account IDs varies depending on the account certification status and operation path, as detailed below: **I. Account ID Query for Uncertified Advertising Accounts** 

1. Visit the [Platform Name] website **https://[platformdomain.com]** , click the “Login” button in the upper right corner to scan and log in; 

2. In the account selection panel, click the “Uncertified Accounts” section to view the corresponding Account ID. (See operation position example at **https://[platform-cdn.com]/img1.png** ) 

- **II. Account ID Query for Certified Advertising Accounts** 

1. Log in to the [Platform Name] website and enter the “[Platform Name] Workbench”; 

2. Click “Management” and select the “Entity/Business Unit” where the account is located on the left; 

3. Click “Account Management” to view the Account ID. (See operation position examples at **https://[platform-cdn.com]/img2.png** and **https://[platform-cdn.com]/img3.png** ) 

**III. Query via Service Provider System** 

1. Log in to the service provider system and enter the “Account List” in the workbench; 

2. View account names and IDs in the account list, supporting searches by account name (fuzzy matching) or ID (exact matching). 

## **IV. Recharge Account UID Query** 

- To view the UID of a recharge account, please click “Account Settings” in “Financial Management” and view it in “Account Information”. 

✗ **Hallucinated** ✓ **Validated** 

Figure 8: Comparison of dialogue responses: the previous online answer (left, red border) contains hallucinated links marked in red, while our answer (right, green border) uses validated links with platform-specific terms replaced by placeholders. 

12 

**==> picture [455 x 240] intentionally omitted <==**

Figure 9: A real dialogue case from our deployed system: the user inquires about restrictions on mini-program landing pages in the financial credit industry; the system responds with a structured, policy-grounded answer covering qualifications, content standards, interaction design, prohibited scenarios, and compliant production suggestions. 

13 

