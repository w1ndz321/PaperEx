Towards Faithful Industrial RAG: A Reinforced Co-adaptation Framework
|     |     |     | for Advertising | QA  |     |     |     |     |     |
| --- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- |
WenweiLi∗,MingXu∗,TianleXia,LingxiangHu,YidingSun,LinfangShang
LiqunLiu†,PengShu,HuanYu,JieJiang
Tencent
{wenweiwwli,flemingxu,tianlexia,lingxianghu,emanuelsun,faelynshang}@tencent.com
{liqunliu,archershu,huanyu,zeus}@tencent.com
|     |     |     | ∗Equalcontribution. | †Correspondingauthor. |     |     |     |     |     |
| --- | --- | --- | ------------------- | --------------------- | --- | --- | --- | --- | --- |
Abstract
Industrialadvertisingquestionanswering(QA)
6202 beF 62  ]LC.sc[  1v48522.2062:viXra
isahigh-stakestaskinwhichhallucinatedcon-
tent,particularlyfabricatedURLs,canleadto
financialloss,complianceviolations,andlegal
| risk. Although | Retrieval-Augmented |          | Gener-       |     |     |     |     |     |     |
| -------------- | ------------------- | -------- | ------------ | --- | --- | --- | --- | --- | --- |
| ation (RAG)    | is widely           | adopted, | deploying it |     |     |     |     |     |     |
inproductionremainschallengingbecausein-
dustrialknowledgeisinherentlyrelational,fre-
Figure1:TraditionalQAvs.ourapproachoverashared
quentlyupdated,andinsufficientlyalignedwith
|                       |     |                      |     | knowledgebase. |     | Giventhesameuserqueryandknowl- |     |     |     |
| --------------------- | --- | -------------------- | --- | -------------- | --- | ------------------------------ | --- | --- | --- |
| generationobjectives. |     | Weproposeareinforced |     |                |     |                                |     |     |     |
edgeitemsA,B,C,D,traditionalmethodsoftenyield
co-adaptationframeworkthatjointlyoptimizes
incomplete,hallucinated,over-generated,orverbose
| retrieval | and generation | through | two compo- |          |            |     |                   |        |      |
| --------- | -------------- | ------- | ---------- | -------- | ---------- | --- | ----------------- | ------ | ---- |
|           |                |         |            | answers. | Our method |     | produces an exact | answer | that |
nents: (1)Graph-awareRetrieval(GraphRAG),
remainscomplete,faithful,andconcise.
| whichmodels                            | entity-relationstructure |          | over a     |     |     |     |     |     |     |
| -------------------------------------- | ------------------------ | -------- | ---------- | --- | --- | --- | --- | --- | --- |
| high-citation                          | knowledge                | subgraph | for multi- |     |     |     |     |     |     |
| hop, domain-specificevidenceselection; |                          |          | and        |     |     |     |     |     |     |
(2)evidence-constrainedreinforcementlearn- In this high-stakes setting, even minor factual er-
| ing via | Group Relative | Policy | Optimization |     |     |     |     |     |     |
| ------- | -------------- | ------ | ------------ | --- | --- | --- | --- | --- | --- |
rorscantriggercompliancerisks,userharm,and
(GRPO)withmulti-dimensionalrewardscover- direct financial losses, and fabricated structured
ingfaithfulness,stylecompliance,safety,and
itemssuchasURLsareparticularlycostly(Jietal.,
| URLvalidity. | Experimentsonaninternalad- |      |                  |            |     |             |                |     |         |
| ------------ | -------------------------- | ---- | ---------------- | ---------- | --- | ----------- | -------------- | --- | ------- |
|              |                            |      |                  | 2023; Ming | et  | al., 2025). | As illustrated |     | in Fig- |
| vertising    | QA dataset                 | show | consistent gains |            |     |             |                |     |         |
ure1,conventionalpipelinesmayproduceincom-
acrossexpert-judgeddimensionsincludingac-
curacy,completeness,andsafety,whilereduc- plete,hallucinated,over-generated,orverbosean-
ingthehallucinationrateby72%. Atwo-week swers,whereasourframeworktargetsconciseand
onlineA/Btestdemonstratesa28.6%increase
evidence-groundedresponses.
| in like rate, | a 46.2%   | decrease | in dislike rate, |                     |     |     |            |       |      |
| ------------- | --------- | -------- | ---------------- | ------------------- | --- | --- | ---------- | ----- | ---- |
|               |           |          |                  | Retrieval-Augmented |     |     | Generation | (RAG) | is a |
| and a 92.7%   | reduction | in URL   | hallucination.   |                     |     |     |            |       |      |
Thesystemhasbeenrunninginproductionfor standardparadigmforgroundingLLMsinexternal
overhalfayearandhasservedmillionsofQA evidence(Lewisetal.,2020;Gaoetal.,2024),yet
| interactions. |     |     |     | production | advertising |           | question          | answering | (QA)   |
| ------------- | --- | --- | --- | ---------- | ----------- | --------- | ----------------- | --------- | ------ |
|               |     |     |     | reveals    | three       | key gaps. | First, industrial |           | knowl- |
1 Introduction
|     |     |     |     | edge is | relational | and | process-driven | (e.g., | prod- |
| --- | --- | --- | --- | ------- | ---------- | --- | -------------- | ------ | ----- |
Online advertising platforms are complex, fast- ucts,rules,procedures),wheresingle-shothybrid
evolving ecosystems where intelligent customer retrievalcanmissmulti-hopdependencies;graph-
service (ICS) systems are critical for operational basedretrievalsuchasGraphRAGaddressesthisby
efficiencyandusersatisfaction(Gaoetal.,2025). explicitlymodelingentitiesandrelationsforcross-
These systems must handle diverse intents, from document reasoning (Edge et al., 2024). Second,
pre-sales consultations to post-sales compliance simplyexpandingcontextlengthisinsufficient: un-
appeals, under frequently updated internal poli- derthe“lostinthemiddle”effect,modelsmayfail
cies (e.g., ad review guidelines, account systems, toreliablyuseevidenceinlonginputs,motivating
reimbursement protocols) that are often behind targetedevidenceselection(Liuetal.,2023). Third,
private knowledge barriers (Sharma et al., 2024). generationmustsatisfystrictstyleandcompliance
1

constraints, yet even strong models may deviate subjecttoconstraintsC,includingzeroURLhal-
fromprovidedcontextunderunanswerableorcoun- lucinations,domain-specificstylecompliance,and
| terfactual   | inputs (Ming  | et  | al., 2025; | Rakin     | et al., | safetyrequirements. |     |     |     |     |     |
| ------------ | ------------- | --- | ---------- | --------- | ------- | ------------------- | --- | --- | --- | --- | --- |
| 2024); while | reinforcement |     | learning   | (Schulman |         |                     |     |     |     |     |     |
etal.,2017a;Rafailovetal.,2023)canaligngener-
2.2 Graph-awareRetrieval
ationwithtaskconstraints,andpost-hocmethods
|     |     |     |     |     |     | To address | the | limitations | of  | traditional | hybrid |
| --- | --- | --- | --- | --- | --- | ---------- | --- | ----------- | --- | ----------- | ------ |
suchasSelfCheckGPT(Manakuletal.,2023)can
|     |     |     |     |     |     | retrieval | methods | (e.g., | BGE | + BM25) | in han- |
| --- | --- | --- | --- | --- | --- | --------- | ------- | ------ | --- | ------- | ------- |
detectunsupportedcontent,treatingretrievaland
generationasisolatedstagesleavesacoordination dlingcomplexmulti-hopdependenciesanddomain-
|     |     |     |     |     |     | specific | terminology, | we  | propose | a Graph-aware |     |
| --- | --- | --- | --- | --- | --- | -------- | ------------ | --- | ------- | ------------- | --- |
gap.
RetrievalmodulethatintegratesGraphRAGwith
| To address | these | gaps, | we propose | an  | end-to- |     |     |     |     |     |     |
| ---------- | ----- | ----- | ---------- | --- | ------- | --- | --- | --- | --- | --- | --- |
acarefullycurated,high-citationknowledgebase,
endreinforcedco-adaptationframeworkthatjointly
optimizesretrievalandevidence-groundedgener- complementedbyaparallelretrievalarchitecture
forindustrial-scaledeployment.
| ation. It       | has two key | components: |     | (1)   | Graph- |     |     |     |     |     |     |
| --------------- | ----------- | ----------- | --- | ----- | ------ | --- | --- | --- | --- | --- | --- |
| aware Retrieval | via         | GraphRAG,   |     | which | models |     |     |     |     |     |     |
relationships between products, rules, and pro- High-CitationKnowledgeBase. GraphRAGen-
cesses to support multi-hop reasoning and termi- hancesretrievalbutintroducessubstantialcompu-
|                  |       |     |         |        |         | tational | overhead. | To  | balance | effectiveness | and |
| ---------------- | ----- | --- | ------- | ------ | ------- | -------- | --------- | --- | ------- | ------------- | --- |
| nology alignment | (Edge |     | et al., | 2024); | and (2) |          |           |     |         |               |     |
efficiency,wemaintainahigh-citationknowledge
Evidence-constrainedReinforcementLearning
(RL), which aligns the generator with retrieved baseK ⊂ K throughtraffic-drivenfeedback. We
h
|     |     |     |     |     |     | accumulate | recall | frequency | for | each | knowledge |
| --- | --- | --- | --- | --- | --- | ---------- | ------ | --------- | --- | ---- | --------- |
evidenceusingmulti-dimensionalrewardsthaten-
|     |     |     |     |     |     | chunk from | production |     | query | logs as | a “citation |
| --- | --- | --- | --- | --- | --- | ---------- | ---------- | --- | ----- | ------- | ----------- |
couragefaithfulnesswhileenforcingstyle,safety,
andURLvalidity. heat”indicator,andperiodicallyselectthetop-N%
Ourcontributionsareasfollows: most frequently cited items to form K h . This cu-
ratedsubsetservesasthesubgraphforGraphRAG,
reducingtraversalcomplexitywhilepreservingef-
| • We propose | a co-adaptation |     |     | framework | that |     |     |     |     |     |     |
| ------------ | --------------- | --- | --- | --------- | ---- | --- | --- | --- | --- | --- | --- |
jointlyoptimizesGraphRAG-basedretrieval fectivenessthroughautomaticrollingupdates.
andanRL-tunedgenerator,achievingsuperior
|           |         |           |     |        |        | GraphRAG |     | Architecture. |     | We construct | a   |
| --------- | ------- | --------- | --- | ------ | ------ | -------- | --- | ------------- | --- | ------------ | --- |
| alignment | between | retrieved |     | domain | knowl- |          |     |               |     |              |     |
edgeandgeneratedresponses. knowledge graph G = (V,E) over K via entity
h
extractionandrelationidentification,withcommu-
|     |     |     |     |     |     | nity detection |     | partitioning | the | graph into | hierar- |
| --- | --- | --- | --- | --- | --- | -------------- | --- | ------------ | --- | ---------- | ------- |
• Wedesignamulti-dimensionalRLobjective
coveringfaithfulness,stylecompliance,safety, chical subgraphs for semantic aggregation. The
andURLvalidity,explicitlypenalizingunsup- retrievallayersupportsdynamicroutingbetween
portedcontentandhallucinatedlinks. hybridretrievalandgraph-basedtraversal,balanc-
ingefficiencyforsimplequerieswithmulti-hoprea-
• Wedeploythesystemonalarge-scaleadver- soningforcomplexones. High-citationsubgraph
tisingplatform,servingmillionsofQAinter- pruningconstrainsretrievalscope,andincremental
actions over half a year. A two-week A/B updates maintain temporal currency without full
| testshowsa28.6%like-rateincrease,a46.2% |     |     |     |     |     | reconstruction. |     |     |     |     |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --------------- | --- | --- | --- | --- | --- |
dislike-ratereduction,anda92.7%reduction
inURLhallucination.
|               |     |     |     |     |     | Parallel                                 | Retrieval | Architecture. |            | To      | mitigate   |
| ------------- | --- | --- | --- | --- | --- | ---------------------------------------- | --------- | ------------- | ---------- | ------- | ---------- |
|               |     |     |     |     |     | GraphRAG                                 | latency   | while         | maximizing |         | recall, we |
| 2 Methodology |     |     |     |     |     | executeGraphRAGandtraditionalRAGchannels |           |               |            |         |            |
|               |     |     |     |     |     | concurrently.                            |           | The GraphRAG  |            | channel | performs   |
2.1 ProblemFormulation
|     |     |     |     |     |     | asynchronous |     | graph traversal |     | over K h | for multi- |
| --- | --- | --- | --- | --- | --- | ------------ | --- | --------------- | --- | -------- | ---------- |
WeformulateadvertisingQAasaconstrainedcon- hopreasoning,whilethetraditionalRAGchannel
ditional generation task (Figure 2). Given a user usesBGE+BM25hybridretrievalwithmulti-path
queryq andadynamicallyupdatedprivateknowl- queryrewritingthatdecomposescomplexqueries
edge base K, the system retrieves a relevant ev- intoparallelsub-queries. Resultsfrombothchan-
idence set D = {d ,...,d }. The generator π nelsaremergedanddeduplicatedtoformthefinal
|     | 1   |     | k   |     | θ   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
producesaresponseAthatmaximizesP(A | q,D) evidencesetD = {d ,...,d }.
|     |     |     |     |     |     |     |     | 1   | k   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2

Graph-aware Retrieval Module Evidence-constrained Generation & RL-tuned
GraphRAG Channel Traditional RAG Channel Query
RL-tuned Generator
High-Citation Sources Query Rewriting (Qwen3-32B-RL)
ssusuubb-bq--ququeueryreyry
Evidence Set
Citation Self-iterative
Heat Updates Reward Models
VVeeccttoorr BM25
Faithfulness Safety GRPO
Graph Traversal & Update
Multi-hop Reasoning (Groundtruth (Policy violation
comparison) check)
Style Compliance Link
(Domain (Valid/hallucinated
Merge & formatting) URLs)
Deduplication
Multi-dimensional Reward
Evidence Set
Zero-URL Hallucination
Private Retrieval Module
Knowledge （GraphRAG + Vector + RL-tuned Generator Domain-specific Style
Query Base BM25） Satety
Evidence Set Answer
Figure2: Systemoverview. GivenauserqueryqandaprivateknowledgebaseK,theretrievalsystemconstructs
anevidencesetDviatwoparallelchannels: aGraphRAGchanneloverahigh-citationknowledgebaseK and
h
a traditional RAG channel with query rewriting and BGE + BM25 hybrid retrieval. Results are merged and
deduplicated. The RL-tuned generator then produces a response optimized by GRPO with multi-dimensional
rewardsforfaithfulness,stylecompliance,safety,andURLvalidity.
2.3 Evidence-constrainedGeneration LLM-as-judgecomparison.
The generation module centers on an RL-tuned • StyleCompliance(R s ): Evaluatesadherenceto
generator(Qwen3-32B-RL).Whilesupervisedfine- advertisingdomainconventions,includingtone,
tuning establishes foundational formatting, re- professionalism,andformatting.
inforcement learning is critical for steering the • Safety(R ): Detectsplatformpolicyviolations
a
model toward stable, safe, and hallucination-free andensuresregulatorycompliance.
responsesunderstrictindustrialconstraints. • URL Validity (R ): Rewards valid URLs and
h
We optimize the generator using GRPO (Shao penalizeshallucinatedones. AURLisvalidifit
etal.,2024),whosegroup-basedmechanismstabi- appearsintheevidenceD,orifitsprefixbelongs
lizes training under noisy reward signals. Unlike toanapprovedpoolanditsHTTPstatuscodeis
PPO(Schulman et al., 2017b), which requires a in{200,301,302}.
separate critic model, GRPO estimates the base-
Thefullrewardcomputationprocedure,including
line from group rewards, reducing memory over-
URLextractionandvalidationdetails,isprovided
head and training instability. This is particularly
inAlgorithm1intheAppendix.
valuableforindustrialapplicationswherereward
signals are inherently noisy due to the subjective 3 Experiments
natureofstyleandsafetyassessments.
Wedesignamulti-dimensionalrewardfunction: We evaluate our approach using both offline and
onlinemetrics.
R = λ R +λ R +λ R +λ R (1)
1 f 2 s 3 a 4 h
where λ are weighting coefficients. Following 3.1 ExperimentalSetting
i
preliminary experiments, we set λ 3 = 2.0 and Dataset. We evaluate on the Advertising QA
λ 4 = 2.0toprioritizesafetyandhallucinationre- Dataset,aninternalChineseadvertisingcustomer-
duction,withλ 1 = λ 2 = 1.0. Therewardcompo- service dataset with 3,000 expert-annotated
nentsare: question–answerpairs. Forout-of-domaingener-
• Evidence Faithfulness (R ): Measures align- alization, we use FaithEval (Ming et al., 2025),
f
mentwiththeground-truthanswerviapairwise whichtestsfaithfulnessunderunanswerableques-
3

tions,counterfactualcontexts,andinconsistentin- (Ours) improves ROUGE-L from 33.82 to 35.49
| formation. |     |     |     |     |     |     | overQwen3-32B-SFT(+1.67),andlowersHalluci- |     |     |     |     |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | --- | --- | --- | --- |
nationRatefrom0.0047to0.0013(72%relativere-
| Evaluation |           | Protocol.   | We         | compare |          | systems |           |                               |               |     |       |            |     |
| ---------- | --------- | ----------- | ---------- | ------- | -------- | ------- | --------- | ----------------------------- | ------------- | --- | ----- | ---------- | --- |
|            |           |             |            |         |          |         | duction). | EvenunderBaseRAG,Qwen3-32B-RL |               |     |       |            |     |
| along      | two axes: | (i)         | retrieval, | where   |          | we con- |           |                               |               |     |       |            |     |
|            |           |             |            |         |          |         | achieves  | a 0.0017                      | Hallucination |     | Rate, | indicating |     |
| trast Base | RAG       | (a standard |            | RAG     | pipeline | with    |           |                               |               |     |       |            |     |
thatevidence-constrainedRLtargetshallucination
| a reranker) | with | GraphRAG, |     | and (ii) | generation |     |     |     |     |     |     |     |     |
| ----------- | ---- | --------- | --- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
behaviorsthatsupervisedfine-tuningalonecannot
| backbones, |     | where we | evaluate | open-source |     | and |     |     |     |     |     |     |     |
| ---------- | --- | -------- | -------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
eliminate.
proprietarymodelsaswellasourRL-tunedmodel.
ThecomplementaryeffectbetweenGraphRAG
| Weuseahybridevaluationprotocol. |             |     |                |     | ROUGE-L |       |           |            |                  |              |     |          |         |
| ------------------------------- | ----------- | --- | -------------- | --- | ------- | ----- | --------- | ---------- | ---------------- | ------------ | --- | -------- | ------- |
|                                 |             |     |                |     |         |       | and RL    | is evident | across           | all metrics. |     | GraphRAG |         |
| (0–100)                         | is computed |     | automatically, |     | while   | Accu- |           |            |                  |              |     |          |         |
|                                 |             |     |                |     |         |       | primarily | improves   | coverage-related |              |     |          | metrics |
racy,Completeness,Clarity,Style,andSafetyare
(ROUGE-L,Completeness),whileRLenhancesre-
| ratedbyhumanexpertsona0–10scale. |     |     |     |     |     | Halluci- |     |     |     |     |     |     |     |
| -------------------------------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
liabilityandcompliancemetrics(Style,Safety,Hal-
| nation        | Rate is | also assessed                   |     | by human | experts | at  |                  |     |                             |     |     |     |     |
| ------------- | ------- | ------------------------------- | --- | -------- | ------- | --- | ---------------- | --- | --------------------------- | --- | --- | --- | --- |
|               |         |                                 |     |          |         |     | lucinationRate). |     | Theircombinationachievesthe |     |     |     |     |
| thecaselevel: |         | foreachcase,iftheanswercontains |     |          |         |     |                  |     |                             |     |     |     |     |
bestoverallperformance,withourfinalsystemout-
anyfabricatedorunsupportedcontent,wecountit
performingthestrongestbaseline(DeepSeek-V3.2
| asonehallucinatedcase. |     |     | Formally,givenN |     |     | cases |                |     |                  |     |     |              |     |
| ---------------------- | --- | --- | --------------- | --- | --- | ----- | -------------- | --- | ---------------- | --- | --- | ------------ | --- |
|                        |     |     |                 |     |     |       | with GraphRAG) |     | on Hallucination |     |     | Rate (0.0030 |     |
andanindicatorI[·],wereport
|     |     |     |     |     |     |     | vs. 0.0013)whilemaintainingcompetitivequality |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- | --- |
scores.
N
|      | 1 (cid:88) |          |                         |     |     |     |     |     |     |     |     |     |     |
| ---- | ---------- | -------- | ----------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| HR = |            | I[answer | containshallucination]. |     |     |     |     |     |     |     |     |     |     |
i
|     | N   |     |     |     |     |     | 3.3 GraphRAGEffectiveness |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- |
i=1
Weevaluategraph-awareretrievalbothofflineand
ROUGE-Lmeasureslexicaloverlapwiththerefer-
online.
ence;lowerHRindicatesfewerhallucinatedcases.
|         |     |          |      |                |     |       | OfflineEvaluation. |        | Weassessretrievalviaside- |     |           |     |        |
| ------- | --- | -------- | ---- | -------------- | --- | ----- | ------------------ | ------ | ------------------------- | --- | --------- | --- | ------ |
| Models. | We  | evaluate | five | representative |     | back- |                    |        |                           |     |           |     |        |
|         |     |          |      |                |     |       | by-side            | expert | comparison                | and | knowledge |     | recall |
bones: DeepSeek-V3.2(DeepSeek-AIetal.,2025),
analysis.
| GPT-5.2 | (OpenAI, |     | 2025), | Qwen3-32B |     | (Qwen |                             |     |     |     |              |     |     |
| ------- | -------- | --- | ------ | --------- | --- | ----- | --------------------------- | --- | --- | --- | ------------ | --- | --- |
|         |          |     |        |           |     |       | KnowledgeRecallEnhancement. |     |     |     | Figure3shows |     |     |
Team,2025),Qwen3-32B-SFT,andQwen3-32B-
|            |     |           |        |         |     |         | progressiveimprovementsinknowledgerecall. |     |     |     |     |     | Ef- |
| ---------- | --- | --------- | ------ | ------- | --- | ------- | ----------------------------------------- | --- | --- | --- | --- | --- | --- |
| RL (ours). | All | evaluated | models | support |     | reason- |                                           |     |     |     |     |     |     |
fectiveknowledgechunksperqueryincreasefrom
ingcapabilities;tomatchproductionlatencycon-
3.9(BaseRAG)to4.5(GraphRAG)to6.3(paral-
| straints, | we evaluate |     | all models | in  | non-thinking |     |                 |     |                 |     |              |     |     |
| --------- | ----------- | --- | ---------- | --- | ------------ | --- | --------------- | --- | --------------- | --- | ------------ | --- | --- |
|           |             |     |            |     |              |     | lel retrieval), |     | a 61.5% overall |     | improvement. |     | Re- |
modeforafaircomparison.
calleffectivenessimprovesfrom73.6%to90.5%,
| This | model | set covers | strong | open-source |     | and |     |     |     |     |     |     |     |
| ---- | ----- | ---------- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
demonstratingthatGraphRAGcombinedwithpar-
commercialbaselines,isolatestheimpactofRL(vs.
allelretrievalsubstantiallyenrichescontextualin-
SFT)onthesamebackbone,andtestsrobustness
formation.
acrossmodelfamilies.
|     |     |     |     |     |     |     | Retrieval   | Quality | Optimization. |     |     | In    | expert  |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | ------------- | --- | --- | ----- | ------- |
|     |     |     |     |     |     |     | evaluation, | the     | Good:Same:Bad |     |     | ratio | reaches |
3.2 MainResults
|                                     |     |     |     |     |           |     | 32.4%:64.9%:2.7% |     | at  | retrieval. | The | Good | ratio |
| ----------------------------------- | --- | --- | --- | --- | --------- | --- | ---------------- | --- | --- | ---------- | --- | ---- | ----- |
| Table1reportsthemainofflineresults. |     |     |     |     | Replacing |     |                  |     |     |            |     |      |       |
is12×higherthanBad,indicatingeffectivenoise
BaseRAGwithGraphRAGconsistentlyimproves
filtering.
| qualityandreduceshallucinations. |     |     |     | DeepSeek-V3.2 |     |     |            |     |              |     |     |            |     |
| -------------------------------- | --- | --- | --- | ------------- | --- | --- | ---------- | --- | ------------ | --- | --- | ---------- | --- |
|                                  |     |     |     |               |     |     | End-to-End |     | Performance. |     | The | end-to-end |     |
improvesROUGE-Lfrom33.27to37.00(+3.73)
Good:Same:Badratioreaches24.3%:71.6%:4.1%,
| and reduces |     | Hallucination | Rate | from | 0.0077 | to  |     |     |     |     |     |     |     |
| ----------- | --- | ------------- | ---- | ---- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
withpositivegainsoutweighingnegativeimpacts
| 0.0030 | (61% | relative | reduction). |     | Similar | pat- |     |     |     |     |     |     |     |
| ------ | ---- | -------- | ----------- | --- | ------- | ---- | --- | --- | --- | --- | --- | --- | --- |
by6×.
ternsholdforGPT-5.2(ROUGE-L:32.82→35.88;
Hallucination Rate: 0.0057→0.0023, 60%) and OnlineA/BTesting. Wedeployedat50%traffic.
Qwen3-32B (ROUGE-L: 29.39→32.96; Halluci- Table2showsconsistentimprovements: likerate
nationRate: 0.0117→0.0060). Graph-awaremulti- increasesfrom0.21%to0.27%(+28.6%),dislike
hopevidenceaggregationstrengthensbothcover- ratedecreasesfrom0.26%to0.18%(−30.8%),and
ageandgroundingbeyondhybridretrievalalone. average conversation turns increase from 1.54 to
RL provides additional gains beyond retrieval 1.81 (+17.5%), indicating improved user engage-
| improvements. |     | UnderGraphRAG,Qwen3-32B-RL |     |     |     |     | ment. |     |     |     |     |     |     |
| ------------- | --- | -------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
4

Metric DeepSeek-V3.2 GPT-5.2 Qwen3-32B Qwen3-32B-SFT Qwen3-32B-RL
BaseRAG GraphRAG BaseRAG GraphRAG BaseRAG GraphRAG BaseRAG GraphRAG BaseRAG Ours
ROUGE-L↑ 33.27 37.00 32.82 35.88 29.39 32.96 30.79 33.82 31.40 35.49
| Accuracy↑ |     | 7.82 | 8.37 | 7.94 | 8.39 | 7.25 | 7.82 | 7.50 | 8.10 |     | 7.85 8.26 |
| --------- | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | --- | --------- |
Completeness↑ 6.78 7.10 6.70 7.08 6.20 6.66 6.43 6.91 6.46 6.99
| Clarity↑ |     | 8.96 | 8.99 | 8.92 | 8.97 | 8.52 | 8.74 | 8.82 | 8.94 |     | 8.83 8.95 |
| -------- | --- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | ---- | --- | --------- |
| Style↑   |     | 8.19 | 8.25 | 8.14 | 8.25 | 7.82 | 8.03 | 8.07 | 8.19 |     | 8.27 8.33 |
| Safety↑  |     | 9.94 | 9.93 | 9.95 | 9.96 | 9.88 | 9.91 | 9.95 | 9.94 |     | 9.97 9.99 |
HallucinationRate↓ 0.0077 0.0030 0.0057 0.0023 0.0117 0.0060 0.0117 0.0047 0.0017 0.0013
Table1: Mainexperimentalresults. OursreferstoQwen3-32B-RLwithGraphRAG.Bestresultsinbold,second
bestunderlined.
|     | Knowledge Recall Enhancement |     |     |     |       | Metric         |     | BaseRAG |     | Ours | ∆      |
| --- | ---------------------------- | --- | --- | --- | ----- | -------------- | --- | ------- | --- | ---- | ------ |
|     | Chunks/Query                 |     |     |     |       | LikeRate(%)    |     | 0.21    |     | 0.27 | +28.6% |
|     | 8                            |     |     |     | 100   |                |     |         |     |      |        |
|     | Recall Eff. (%)              |     |     |     | 90.5% | DislikeRate(%) |     | 0.26    |     | 0.18 | −30.8% |
84.2%
|     |       |     |     | 6.3 |                    | Avg.Conv.Turns |     | 1.54 |     | 1.81 | +17.5% |
| --- | ----- | --- | --- | --- | ------------------ | -------------- | --- | ---- | --- | ---- | ------ |
|     | 73.6% |     |     |     | 80 )%( .ffE llaceR |                |     |      |     |      |        |
yreuQ/sknuhC 6
4.5
|     |     |     |     |     | 60  | Table2: | OnlineA/Btestingat50%traffic. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | ----------------------------- | --- | --- | --- | --- |
3.9
4
40
|     | 2   |     |     |     |     | the nuanced | nature | of domain-specific |     |     | tone and |
| --- | --- | --- | --- | --- | --- | ----------- | ------ | ------------------ | --- | --- | -------- |
20
|     |          |          |     |          |     | compliancerequirements. |             |             | Theoverallrewardcon- |     |          |
| --- | -------- | -------- | --- | -------- | --- | ----------------------- | ----------- | ----------- | -------------------- | --- | -------- |
|     | 0        |          |     |          | 0   |                         |             |             |                      |     |          |
|     |          |          |     |          |     | verges                  | to a stable | high value, | suggesting           |     | that the |
|     | Base RAG | GraphRAG |     | Parallel |     |                         |             |             |                      |     |          |
multi-objectiveoptimizationachievesbalancedim-
| Figure3: | KnowledgerecallenhancementacrossBase |     |          |            |           |            |        |                |     |         |        |
| -------- | ------------------------------------ | --- | -------- | ---------- | --------- | ---------- | ------ | -------------- | --- | ------- | ------ |
|          |                                      |     |          |            |           | provements | across | all dimensions |     | without | detri- |
| RAG,     | GraphRAG,                            | and | Parallel | retrieval. | Effective |            |        |                |     |         |        |
mentaltrade-offs.
chunksprequeryandrecalleffectivenessinpercent.
3.5 GeneralizationonFaithEval
|     | 1.0 |     |     |     |     | To assess | whether | our RL-tuned |     | model | general- |
| --- | --- | --- | --- | --- | --- | --------- | ------- | ------------ | --- | ----- | -------- |
ecnamrofreP dezilamroN
izesbeyondthein-domainsetting,weevaluateon
0.8
|     |     |     |     |     |     | FaithEval. | Figure5showstheresults. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------- | ----------------------- | --- | --- | --- | --- |
0.6
|     |     |     |     |     |     | Our       | RL-tuned | model         |     | improves | over  |
| --- | --- | --- | --- | --- | --- | --------- | -------- | ------------- | --- | -------- | ----- |
|     |     |     |     |     |     | Qwen3-32B | on       | all FaithEval |     | subsets: | Unan- |
0.4
|     |     |     |       |     |        | swerable | 44.60%→53.40%, |     |     | Counterfactual |     |
| --- | --- | --- | ----- | --- | ------ | -------- | -------------- | --- | --- | -------------- | --- |
|     |     |     | Style |     | Safety |          |                |     |     |                |     |
0.2 Faithfulness Overall 57.90%→64.40%(outperformingDeepSeek-V3.2
|     |     |     | Link |     |     | at 56.40%), | and | Inconsistent |     | 63.80%→84.60%. |     |
| --- | --- | --- | ---- | --- | --- | ----------- | --- | ------------ | --- | -------------- | --- |
0.0
|     | 20  | 40  | 60  | 80  | 100 | The gains | on Unanswerable |     | and | Counterfactual |     |
| --- | --- | --- | --- | --- | --- | --------- | --------------- | --- | --- | -------------- | --- |
Training Steps
suggeststrongerrefusalbehaviorwhencontextis
Figure4: Trainingdynamicsofmulti-dimensionalre- missingormisleading. OnInconsistent,itreaches
84.60%,substantiallyaboveQwen3-32B(63.80%)
wardcomponentsduringRL.
|     |                       |     |     |     |     | and closer                      | to DeepSeek-V3.2 |          |            | (94.80%). | These        |
| --- | --------------------- | --- | --- | --- | --- | ------------------------------- | ---------------- | -------- | ---------- | --------- | ------------ |
|     |                       |     |     |     |     | results                         | indicate         | improved | contextual |           | faithfulness |
| 3.4 | RLRewardEffectiveness |     |     |     |     | withoutdegradinggeneralization. |                  |          |            |           |              |
Figure4showsconsistentimprovementacrossall
3.6 ProductionDeployment
| reward | components | during | RL  | fine-tuning. | With |     |     |     |     |     |     |
| ------ | ---------- | ------ | --- | ------------ | ---- | --- | --- | --- | --- | --- | --- |
only 1,000 training samples, all metrics rapidly 3.6.1 OfflineEvaluation
improve within 100 steps and converge, demon- We compare against a Base RAG + DeepSeek-
stratingefficientrewarddesign.
V3(Liuetal.,2024)baselineviaexpertassessment
The reward components exhibit distinct opti- oncompleteness,professionalism,compliance,and
mizationpatterns. FaithfulnessandURLvalidity hallucination. AsshowninFigure6, ourmethod
rewardsshowthesteepestinitialascent,indicating wins substantially more often than it loses, with
thatthemodelquicklylearnstoalignwithretrieved the largest gains in professionalism (45.2% win)
evidence and avoid hallucinated links. Style and and compliance (41.9% win) and a low loss rate
safetyrewardsimprovemoregradually,reflecting (1.1%). It also improves hallucination outcomes
5

100
75
50
25
0
Incons. Unans. Cfact. Overall
)%(
ycaruccA
Metric Baseline Ours ∆
DeepSeek-V3.2
94.8
Qwen3-32B LikeRate(%) 0.21 0.27 +28.6%
84.6
Qwen3-32B-RL (Ours) DislikeRate(%) 0.26 0.14 −46.2%
68.5 67.5 URLHallu.(%) 0.0041 0.0003 −92.7%
63.8 64.4
54.2 53.4 56.457.9 55.4 Latency(s) 2.5 3.1 +24.0%
44.6
Table 3: Online A/B testing results (two weeks, 50%
traffic).
Module Latency(ms)
QueryRewriting 690
Figure5: FaithEvalgeneralization: accuracy(%)onIn- GraphRAGRetrieval 852
BGE+BM25Retrieval 167
consistent,Unanswerable,Counterfactual,andOverall.
Reranking 557
Generation 801
SafetyGuardrails 230
Completeness 29.0% 64.5% 6.5%
Total 3130
Professionalism 45.2% 53.8% 1.1%
Table4: Latencybreakdownbymodule.
Compliance 41.9% 57.0% 1.1%
Hallucination 11.7% 88.1% 0.1%
0 20 40 60 80 100 thelargestsinglelatencycost(852ms),whichmo-
Percentage (%) tivates our high-citation knowledge base design
Ours Win Tie Baseline Win
to constrain graph traversal and reduce overhead.
ExecutingGraphRAGinparallelwiththeBGE+
Figure6: Offlineevaluationcomparison: win/tie/lose
BM25pipelineensuresthattheslowergraph-based
distributionacrossfourdimensions.
retrievaldoesnotblockthefasterhybridchannel.
Generation latency (801ms) is on par with stan-
(7.7%winvs. 0.1%loss),supportingthebenefitof
dard large language model inference, suggesting
co-adaptingGraphRAGandRL-tunedgeneration.
thatRLfine-tuningdoesnotintroducenoticeable
computationaloverheadrelativetothebasemodel.
3.6.2 OnlineA/BTesting
Safetyguardrailsincuranadditional230msaspost-
Atwo-weekonlineA/Btestcomparesourdeployed
processing, without affecting time-to-first-token,
systemagainsttheBaseRAG+DeepSeek-V3base-
therebypreservingsystemresponsiveness.
line, with a 50%/50% traffic split (Table 3). Our
method increases like rate from 0.21% to 0.27%
4 Conclusion
(+28.6%), decreases dislike rate from 0.26% to
0.14%(−46.2%),andreducesURLhallucination
Wepresentareinforcedco-adaptationframework
from 0.0041% to 0.0003% (−92.7%). Average
tomitigatehallucinationsinindustrialadvertising
first-tokenlatencyrisesfrom2.5sto3.1s(+24.0%),
Q&AbyjointlyoptimizingGraphRAGandanRL-
whichremainsacceptableinpractice. Overall,the
tuned generator guided by multi-dimensional re-
A/Bresultssuggestthatreinforcedco-adaptation
wards,therebynarrowingtheretrieval–generation
improvesbothusersatisfactionandreliabilityun-
gapandreducingunsupportedcontentandhalluci-
derrealtraffic,withamanageablelatencytrade-off.
natedorinvalidlinks. Ourresultsshowthatgraph-
3.6.3 LatencyAnalysis awareretrievalwithahigh-citationknowledgebase
Table 4 details the latency distribution. Query balancesmulti-hopevidenceaggregationwithcom-
rewriting takes 690ms, parallel retrieval takes putational efficiency, while evidence-constrained
852ms (GraphRAG) and 167ms (BGE + BM25), RLfurthersuppresseshallucinationswithoutsac-
reranking takes 557ms, generation takes 801ms, rificing domain style compliance or safety. Ex-
and safety guardrails take 230ms. Total latency tensiveofflineevaluations,atwo-weekproduction
is3130ms,meetingacceptablethresholdsforuser A/Btest,andoversixmonthsofdeploymentcollec-
experienceandindustrialdeployment. tivelyvalidatethattheapproachimprovesanswer
The latency breakdown highlights several av- reliability and user-facing quality at scale under
enuesforoptimization. GraphRAGretrievalincurs practicallatencyconstraints.
6

EthicsStatement
PatrickLewis,EthanPerez,AleksandraPiktus,Fabio
Petroni,VladimirKarpukhin,NamanGoyal,Hein-
Our research targets high-stakes industrial adver- richKüttler, MikeLewis, Wen-tauYih, TimRock-
|                                     |           |     |             |            | täschel,   | and | 1 others.           | 2020. | Retrieval-augmented |        |     |
| ----------------------------------- | --------- | --- | ----------- | ---------- | ---------- | --- | ------------------- | ----- | ------------------- | ------ | --- |
| tising question                     | answering |     | and adheres | to ethical |            |     |                     |       |                     |        |     |
|                                     |           |     |             |            | generation | for | knowledge-intensive |       | NLP                 | tasks. | In  |
| principlesthatprioritizeuserrights. |           |     | Weaimtoim-  |            |            |     |                     |       |                     |        |     |
AdvancesinNeuralInformationProcessingSystems,
provesystemreliabilityandsafetybyreducingun-
volume33,pages9459–9474.
supportedclaimsandhallucinatedorinvalidURLs
|     |     |     |     |     | Aixin Liu, | Bei | Feng, | Bing Xue, | Bingxuan |     | Wang, |
| --- | --- | --- | --- | --- | ---------- | --- | ----- | --------- | -------- | --- | ----- |
thatcouldmisleadusersorintroducecompliance
BochaoWu,ChengdaLu,ChenggangZhao,Chengqi
risks. Any dataset examples are used solely for Deng, Chenyu Zhang, Chong Ruan, and 1 others.
scientificanalysisanddonotnecessarilyreflectthe arXivpreprint
2024. Deepseek-v3technicalreport.
| viewsoftheauthors. |          | Allresourcesareintendedfor |                    |     | arXiv:2412.19437. |         |       |           |         |        |     |
| ------------------ | -------- | -------------------------- | ------------------ | --- | ----------------- | ------- | ----- | --------- | ------- | ------ | --- |
| scientific         | research | purposes                   | only, contributing | to  |                   |         |       |           |         |        |     |
|                    |          |                            |                    |     | Nelson            | F. Liu, | Kevin | Lin, John | Hewitt, | Ashwin |     |
thedevelopmentofmoresecureandreliabledigital
Paranjape,MicheleBevilacqua,FabioPetroni,and
| platforms.   |       |      |                    |      | Percy             | Liang.        | 2023. Lost          | in            | the middle: | How      | lan-   |
| ------------ | ----- | ---- | ------------------ | ---- | ----------------- | ------------- | ------------------- | ------------- | ----------- | -------- | ------ |
|              |       |      |                    |      | guage             | models        | use long            | contexts.     | arXiv       | preprint |        |
|              |       |      |                    |      | arXiv:2307.03172. |               | AcceptedtoTACL2023. |               |             |          |        |
| References   |       |      |                    |      | Potsawee          | Manakul,      | Adian               | Liusie,       | and         | Mark     | Gales. |
|              |       |      |                    |      | 2023.             | Selfcheckgpt: |                     | Zero-resource | black-box   |          | hal-   |
| DeepSeek-AI, | Aixin | Liu, | Aoxue Mei, Bangcai | Lin, |                   |               |                     |               |             |          |        |
|              |       |      |                    |      | lucination        | detection     | for                 | generative    | large       | language |        |
BingXue,BingxuanWang,BingzhengXu,Bochao
|           |        |         |           |           | models. | InProceedingsofthe2023Conferenceon |     |     |     |     |     |
| --------- | ------ | ------- | --------- | --------- | ------- | ---------------------------------- | --- | --- | --- | --- | --- |
| Wu, Bowei | Zhang, | Chaofan | Lin, Chen | Dong, and |         |                                    |     |     |     |     |     |
EmpiricalMethodsinNaturalLanguageProcessing,
1 others. 2025. Deepseek-v3.2: Pushing the fron- pages9004–9017,Singapore.AssociationforCom-
| tierofopenlargelanguagemodels. |     |     | arXivpreprint |     |     |     |     |     |     |     |     |
| ------------------------------ | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- |
putationalLinguistics.
arXiv:2512.02556.
YifeiMing,SenthilPurushwalkam,ShreyPandit,Zix-
Darren Edge, Ha Trinh, Newman Cheng, Joshua uan Ke, Xuan-Phi Nguyen, Caiming Xiong, and
Bradley, Alex Chao, Apurva Mody, Steven Truitt, Shafiq Joty. 2025. Faitheval: Can your language
DashaMetropolitansky,RobertOsazuwaNess,and modelstayfaithfultocontext,evenif“themoonis
Jonathan Larson. 2024. From local to global: A made of marshmallows”. In International Confer-
graphRAGapproachtoquery-focusedsummariza- enceonLearningRepresentations.
tion. arXivpreprintarXiv:2404.16130.
|                                             |              |            |          |         | OpenAI.2025.   |     | Introducinggpt-5.2. |     | Accessed:         |     | 2026- |
| ------------------------------------------- | ------------ | ---------- | -------- | ------- | -------------- | --- | ------------------- | --- | ----------------- | --- | ----- |
| TianhongGao,JundongShen,JiapengWang,BeiShi, |              |            |          |         | 02-08.         |     |                     |     |                   |     |       |
| YingJu,JunfengYao,andHuiyuYu.2025.          |              |            |          | Bench-  |                |     |                     |     |                   |     |       |
|                                             |              |            |          |         | QwenTeam.2025. |     | Qwen3-32b.          |     | HuggingFacemodel, |     |       |
| marking                                     | and learning | real-world | customer | service |                |     |                     |     |                   |     |       |
accessed2026-02-08.
| dialogue. | arXivpreprintarXiv:2510.22143. |     |     |     |     |     |     |     |     |     |     |
| --------- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
RafaelRafailov,ArchitSharma,EricMitchell,Stefano
Yunfan Gao, Yun Xiong, Xinyu Gao, Kangxiang Jia, Ermon,ChristopherD.Manning,andChelseaFinn.
JinliuPan,YuxiBi,YiDai,JiaweiSun,MengWang, 2023. Directpreferenceoptimization:Yourlanguage
| andHaofenWang.2024.            |     |     | Retrieval-augmentedgen- |       |       |             |          |        |     | Advances | in  |
| ------------------------------ | --- | --- | ----------------------- | ----- | ----- | ----------- | -------- | ------ | --- | -------- | --- |
|                                |     |     |                         |       | model | is secretly | a reward | model. | In  |          |     |
| erationforlargelanguagemodels: |     |     | Asurvey.                | arXiv |       |             |          |        |     |          |     |
NeuralInformationProcessingSystems.
preprintarXiv:2312.10997.
|     |     |     |     |     | Salman | Rakin, | Md. A. R. | Shibly, | Zahin | M. Hossain, |     |
| --- | --- | --- | --- | --- | ------ | ------ | --------- | ------- | ----- | ----------- | --- |
Gemini Team, Google. 2025. Gemini 2.5: Pushing ZeeshanKhan,andMd.MostofaAkbar.2024. Lever-
thefrontierwithadvancedreasoning,multimodality, agingthedomainadaptationofretrievalaugmented
generationmodelsforquestionansweringandreduc-
longcontext,andnextgenerationagenticcapabilities.
|     |     |     |     |     | inghallucination. |     | arXivpreprintarXiv:2410.17783. |     |     |     |     |
| --- | --- | --- | --- | --- | ----------------- | --- | ------------------------------ | --- | --- | --- | --- |
Technicalreport,accessed2026-02-08.
JohnSchulman,FilipWolski,PrafullaDhariwal,Alec
ZiweiJi,NayeonLee,RitaFrieske,TiezhengYu,Dan
|                              |            |        |                  |        | Radford, | and          | Oleg | Klimov.     | 2017a. | Proximal |     |
| ---------------------------- | ---------- | ------ | ---------------- | ------ | -------- | ------------ | ---- | ----------- | ------ | -------- | --- |
| Su, Yan                      | Xu, Etsuko | Ishii, | Ye Jin Bang,     | Andrea |          |              |      |             |        |          |     |
|                              |            |        |                  |        | policy   | optimization |      | algorithms. | arXiv  | preprint |     |
| Madotto,andPascaleFung.2023. |            |        | Surveyofhalluci- |        |          |              |      |             |        |          |     |
arXiv:1707.06347.
| nationinnaturallanguagegeneration. |     |     | ACMComput- |     |     |     |     |     |     |     |     |
| ---------------------------------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
ingSurveys,55(12):1–38.
JohnSchulman,FilipWolski,PrafullaDhariwal,Alec
|     |     |     |     |     | Radford, | and | Oleg | Klimov. | 2017b. | Proximal |     |
| --- | --- | --- | --- | --- | -------- | --- | ---- | ------- | ------ | -------- | --- |
Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying policy optimization algorithms. arXiv preprint
| Sheng, | Lianmin | Zheng, | Cody Hao Yu, | Joseph E. |     |     |     |     |     |     |     |
| ------ | ------- | ------ | ------------ | --------- | --- | --- | --- | --- | --- | --- | --- |
arXiv:1707.06347.
| Gonzalez, | Hao | Zhang, | and Ion Stoica. | 2023. Ef- |     |     |     |     |     |     |     |
| --------- | --- | ------ | --------------- | --------- | --- | --- | --- | --- | --- | --- | --- |
ficient memory management for large language Zhihong Shao, Peiyi Wang, Qihao Zhu, Runxin Xu,
modelservingwithPagedAttention. arXivpreprint JunxiaoSong,XiaoBi,HaoweiZhang,Mingchuan
arXiv:2309.06180. Zhang, Y. K. Li, Y. Wu, and Daya Guo. 2024.
7

| Deepseekmath:                  |     | Pushingthelimitsofmathematical |     |               |     |
| ------------------------------ | --- | ------------------------------ | --- | ------------- | --- |
| reasoninginopenlanguagemodels. |     |                                |     | arXivpreprint |     |
arXiv:2402.03300.
SanatSharma,DavidSeunghyunYoon,FranckDernon-
court,DewangSultania,KarishmaBagga,Mengjiao
| Zhang,TrungBui,andVarunKotte.2024. |     |     |     |     | Retrieval |
| ---------------------------------- | --- | --- | --- | --- | --------- |
augmentedgenerationfordomain-specificquestion
| answering. | arXivpreprintarXiv:2404.14760. |            |            |     |           |
| ---------- | ------------------------------ | ---------- | ---------- | --- | --------- |
| Guangming  | Sheng,                         | Chi Zhang, | Zilingfeng |     | Ye, Xibin |
Wu,WangZhang,RuZhang,YanghuaPeng,Haibin
| Lin,                          | and Chuan | Wu. 2024. | HybridFlow: |               | A flexi- |
| ----------------------------- | --------- | --------- | ----------- | ------------- | -------- |
| bleandefficientRLHFframework. |           |           |             | arXivpreprint |          |
arXiv:2409.19256.
| TencentHunyuanTeam.2025. |       |          | Hunyuan-TurboS:Ad- |         |        |
| ------------------------ | ----- | -------- | ------------------ | ------- | ------ |
| vancing                  | large | language | models             | through | mamba- |
transformersynergyandadaptivechain-of-thought.
Preprint,arXiv:2505.15431.
| Qiying   | Yu, Zheng | Zhang, Ruofei |        | Zhu, Yufeng   | Yuan,  |
| -------- | --------- | ------------- | ------ | ------------- | ------ |
| Xiaochen | Zuo,      | Yu Yue,       | Weinan | Dai, Tiantian | Fan,   |
| Gaohong  | Liu,      | Lingjun Liu,  | Xin    | Liu, Haibin   | Lin,   |
| Zhiqi    | Lin, Bole | Ma, Guangming |        | Sheng,        | Yuxuan |
Tong,ChiZhang,MofanZhang,WangZhang,and
| 16others.2025.                  |     | DAPO:Anopen-sourceLLMrein- |     |               |     |
| ------------------------------- | --- | -------------------------- | --- | ------------- | --- |
| forcementlearningsystematscale. |     |                            |     | arXivpreprint |     |
arXiv:2503.14476.
YanzhaoZhang,MingxinLi,DingkunLong,XinZhang,
| Huan                              | Lin, Baosong | Yang,                     | Pengjun  | Xie,          | An Yang, |
| --------------------------------- | ------------ | ------------------------- | -------- | ------------- | -------- |
| Dayiheng                          | Liu,         | Junyang                   | Lin, and | 1 others.     | 2025.    |
| Qwen3embedding:                   |              | Advancingtextembeddingand |          |               |          |
| rerankingthroughfoundationmodels. |              |                           |          | arXivpreprint |          |
arXiv:2506.05176.
YuzeZhao,JintaoHuang,JinghanHu,XingjunWang,
YunlinMao,DaozeZhang,ZeyinziJiang,ZhikaiWu,
BaoleAi,AngWang,WenmengZhou,andYingda
| Chen.2025.          |     | Swift: Ascalablelightweightinfrastruc- |     |     |     |
| ------------------- | --- | -------------------------------------- | --- | --- | --- |
| tureforfine-tuning. |     | InProceedingsoftheAAAICon-             |     |     |     |
ferenceonArtificialIntelligence,volume39,pages
29733–29735.
8

A ImplementationDetails before serving, enforcing zero-hallucination and
strictsafetyconstraintsinthefinalresponse.
Thissectiondetailstheparametersettings,end-to-
endpipelineimplementation,andtrainingspecifics B RewardComputationAlgorithm
that instantiate the method described in the main
paper.
Algorithm1Multi-dimensionalRewardComputa-
tion
Query rewriting and retrieval. Multi-route
Require: GeneratedanswerA,retrievedevidence
query rewriting produces three rewritten variants
D = {d ,...,d }, ground truth answer A ,
inparallelwhileretainingtheoriginaluserquery, 1 k gt
URLprefixcandidatepoolC
yielding four queries in total for retrieval. The p
Ensure: TotalrewardR
GraphRAG component follows the standard Mi-
1: Extract URLs via regex: U ←
crosoft GraphRAG design (Edge et al., 2024),
ExtractURLs (A)
with local search used for graph traversal. The re
high-citation knowledge subgraph is built from 2: Extract evidence URLs via regex: U D ←
ExtractURLs (D)
the top-N% most frequently cited items, with re
3: HTTPstatusset: S ← {200,301,302}
N = 10. ThetraditionalRAGchanneluseshybrid
retrieval with BGE + BM25 (run jointly); results 4: URLsinevidence: U evi ← U ∩U D
frombothchannelsaremergedanddeduplicated, 5: URLsnotinevidence: U out ← U \U D
thenrerankedbyalightweightQwen3-4Breranker 6: Prefix-approvedURLs: U pref ← {u ∈ U out |
Prefix(u) ∈ C }
(Zhangetal.,2025). Finally,tofitthemodelcon- p
textwindow,wetruncatethererankedevidenceto 7: HTTP-valid URLs: U http ← {u ∈ U pref |
code(u) ∈ S}
8Ktokens.
8: ValidURLs: U valid ← U evi ∪U http
SFT stage. The first stage is supervised fine- 9: R f ← f faithful (A,A gt ){Pairwisecomparison
withgroundtruthusingLLM-as-judge}
tuningwithLoRAonthebasemodelQwen3-32B,
implementedwiththeSWIFTinfrastructure(Zhao 10: R s ← f style (A){StyleevaluationusingLLM-
et al., 2025). We use a learning rate of 1×10−4, as-judge}
trainfor5epochson8×NVIDIAH20GPUs,and 11: R a ← f safety (A){SafetycheckusingLLM-as-
judge}
use1khuman-annotateddialoguesamples.
12: R h + ← Reward(U valid ) {Positive reward for
RLstage. Thesecondstageusesreinforcement validlinks}
learning via the VERL framework (Sheng et al., 13: R h − ← Penalty(U \U valid ){Negativepenalty
2024)andtheGRPOalgorithm. Trainingisagain forinvalidlinks}
LoRA-basedon16×H20GPUs,with1kprompts 14: R h ← R h +−R h −
and responses labeled by Gemini 2.5 Pro (Gem- 15: R ← λ 1 R f +λ 2 R s +λ 3 R a +λ 4 R h
iniTeam,Google,2025)forrewardlearning. The 16: return R
judger used to compute rewards is Hunyuan Tur-
boS(TencentHunyuanTeam,2025). Wetrainfor C Prompt
120stepswithbatchsize16,setgenerationtemper-
LLMJudgerPrompt
ature to 1.0, set the maximum response length to
2K tokens, and use 8 rollouts per prompt. All re-
You are an expert evaluator for advertising
wardtermsarenormalizedbeforecombination. For
customer service answer quality.
reward weights, we set higher weights for safety Evaluate Answer B on the three
andhallucination-relatedterms. Wesetλ = 2.0 dimensions below.
3
- Evidence Faithfulness: compare Answer A and
forsafetyandλ = 2.0forhallucinationandlink
4 Answer B; judge whether Answer B
penalty,whileotherweightsaresetto1. Following is G, meaning better, S, meaning tie, or B,
meaning worse, than Answer A and give
aDAPO-stylesetup(Yuetal.,2025),thereference-
a brief reason.
modelKLtermisremoved. - Style Compliance and Safety: score Answer B
only, for example on a 0-10 scale, and
Safetyguardrails. Duringstreaminggeneration, do not use G, S, or B.
safetyguardrailspost-processtheoutputtodetect
Dimensions:
andfilterpolicyviolationsandhallucinatedURLs
9

|     |             |               |           |          |          |          |     | "Style    | Compliance": |     | 8,  |     |     |
| --- | ----------- | ------------- | --------- | -------- | -------- | -------- | --- | --------- | ------------ | --- | --- | --- | --- |
| 1.  | Evidence    | Faithfulness: |           |          |          |          |     | "Safety": | 9            |     |     |     |     |
|     | - How well  | does          | the       | answer   | align    | with the | }   |           |              |     |     |     |     |
|     | provided    |               | materials | through  |          |          | }   |           |              |     |     |     |     |
|     | pairwise    | comparison?   |           | Consider |          | semantic |     |           |              |     |     |     |     |
|     | consistency |               | and       | factual  | accuracy |          |     |           |              |     |     |     |     |
|     | given       | the user      | query     | and      | dialogue |          |     |           |              |     |     |     |     |
D FactualQAunderDistractingContext
|     | history;          |              | penalize | unsupported |             | or  |                                   |     |      |                       |           |           |      |
| --- | ----------------- | ------------ | -------- | ----------- | ----------- | --- | --------------------------------- | --- | ---- | --------------------- | --------- | --------- | ---- |
|     | contradictory     |              | claims.  |             |             |     |                                   |     |      |                       |           |           |      |
|     |                   |              |          |             |             |     | Settingandresults.                |     |      | WeconstructafactualQA |           |           |      |
| 2.  | Style Compliance, |              | score    | 0-10:       |             |     |                                   |     |      |                       |           |           |      |
|     |                   |              |          |             |             |     | evaluation                        | set | from | 1,000                 | knowledge | items     | sam- |
|     | - Does the        | answer       | adhere   | to          | advertising |     |                                   |     |      |                       |           |           |      |
|     |                   |              |          |             |             |     | pledfromtheproductionenvironment. |     |      |                       |           | Retrieved |      |
|     | domain            | conventions, |          | including   |             |     |                                   |     |      |                       |           |           |      |
tone, professionalism, and domain- contextisobtainedfromtheactualrecallpipeline
|     | specific   |     | formatting |      | requirements? |     |                                        |     |     |     |     |     |         |
| --- | ---------- | --- | ---------- | ---- | ------------- | --- | -------------------------------------- | --- | --- | --- | --- | --- | ------- |
|     |            |     |            |      |               |     | sothatallmodelsreceiveidenticalinputs. |     |     |     |     |     | Allmod- |
|     | - Scoring: | 0-2 | poor.      | This | includes      |     |                                        |     |     |     |     |     |         |
informal style, off-tone responses, or els are evaluated in non-thinking mode. Figure 7
|     | wrong     | format.  |     |      |           |     | reportsaccuracyforouronlinedeployedmodeland |     |     |     |     |     |     |
| --- | --------- | -------- | --- | ---- | --------- | --- | ------------------------------------------- | --- | --- | --- | --- | --- | --- |
|     | 3-4 below | average. |     | This | indicates |     |                                             |     |     |     |     |     |     |
leadingcommercialflagshipmodels.
|     | partial         |     | compliance. |           |       |         |     |     |     |     |     |     |     |
| --- | --------------- | --- | ----------- | --------- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- |
|     | 5-6 acceptable. |     | This        | indicates |       | general |     |     |     |     |     |     |     |
|     | compliance      |     | with        | minor     | gaps. |         |     |     |     |     |     |     |     |
99.3%
|     | 7-8 good. | This | indicates |            | professional |          | 100 |     |       |     |       |       | 96.5% |
| --- | --------- | ---- | --------- | ---------- | ------------ | -------- | --- | --- | ----- | --- | ----- | ----- | ----- |
|     |           |      |           |            |              |          |     |     | 93.6% |     | 95.0% |       |       |
|     | responses |      | with      | consistent |              | tone and |     |     |       |     |       | 92.2% |       |
)%( ycaruccA
format.
|     | 9-10 excellent. |     | This | indicates |     | full |     |     |     |     |     |     |     |
| --- | --------------- | --- | ---- | --------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
80
|     | alignment  |             | with  | domain   | conventions. |        |     |      |             |             |            |     |        |
| --- | ---------- | ----------- | ----- | -------- | ------------ | ------ | --- | ---- | ----------- | ----------- | ---------- | --- | ------ |
| 3.  | Safety,    | score       | 0-10: |          |              |        |     |      |             |             |            |     |        |
|     | - Does the | answer      | avoid | platform |              | policy | 60  |      |             |             |            |     |        |
|     | violations |             | and   | comply   | with         |        |     |      |             |             |            |     |        |
|     | regulatory | standards   |       | and      | safety       |        |     |      |             |             |            |     |        |
|     |            |             |       |          |              |        |     | Ours |             | .2 imi K2.5 | Doubao 1.8 |     | HY 2.0 |
|     | g u        | i de l i ne | s ?   |          |              |        |     |      | DeepSeek-V3 |             |            |     |        |
K
|     | - Scori n     | g : 0 - 2 | s e vere | violations. |            | This |        |             |     |             |     |            |      |
| --- | ------------- | --------- | -------- | ----------- | ---------- | ---- | ------ | ----------- | --- | ----------- | --- | ---------- | ---- |
|     | indicates     |           | policy   | breach      | or harmful | or   |        |             |     |             |     |            |      |
|     | non-compliant |           | content. |             |            |      |        |             |     |             |     |            |      |
|     |               |           |          |             |            |      | Figure | 7: Accuracy | on  | the factual | QA  | evaluation | set. |
|     | 3-4 notable   |           | issues.  | This        | indicates  |      |        |             |     |             |     |            |      |
Theinputcontextincludesallrelevantknowledgeand
|     | multiple |     | issues | or serious |     |     |     |     |     |     |     |     |     |
| --- | -------- | --- | ------ | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
distractingretrievedpassages.
|     | compliance      |      | gaps.     |           |           |          |     |     |     |     |     |     |     |
| --- | --------------- | ---- | --------- | --------- | --------- | -------- | --- | --- | --- | --- | --- | --- | --- |
|     | 5-6 acceptable. |      | This      | indicates |           | minor or |     |     |     |     |     |     |     |
|     | ambiguous       |      | issues.   |           |           |          |     |     |     |     |     |     |     |
|     | 7-8 good.       | This | indicates |           | compliant |          |     |     |     |     |     |     |     |
E ExampleDialogueComparison
|     | responses |     | with | isolated |     |     |     |     |     |     |     |     |     |
| --- | --------- | --- | ---- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
imperfections.
|     |                 |     |      |           |     |      | Setting. | Thisexamplecomparesresponsestoan |     |     |     |     |     |
| --- | --------------- | --- | ---- | --------- | --- | ---- | -------- | -------------------------------- | --- | --- | --- | --- | --- |
|     | 9-10 excellent. |     | This | indicates |     | full |          |                                  |     |     |     |     |     |
compliance with no risk. accountIDquery. Thepreviousonlineanswercon-
tainshallucinatedlinksmarkedinred,whileouran-
---
|     |        |     |     |     |     |     | swerusesvalidatedlinks.                    |     |     | Sensitiveplatformnames |     |     |     |
| --- | ------ | --- | --- | --- | --- | --- | ------------------------------------------ | --- | --- | ---------------------- | --- | --- | --- |
| ### | Input: |     |     |     |     |     | anddomainsinouranswerarereplacedwithplace- |     |     |                        |     |     |     |
holders: [PlatformName]representstheadvertis-
| [Query]: | {query} |     |     |     |     |     |              |     |       |                           |     |     |     |
| -------- | ------- | --- | --- | --- | --- | --- | ------------ | --- | ----- | ------------------------- | --- | --- | --- |
|          |         |     |     |     |     |     | ing platform |     | name, | and [platform-domain.com] |     |     |     |
[Dialogue History]: {dialogue_history} representstheplatformdomain.
| [Materials]: |     | {file} |     |     |     |     |              |     |     |       |           |     |           |
| ------------ | --- | ------ | --- | --- | --- | --- | ------------ | --- | --- | ----- | --------- | --- | --------- |
|              |     |        |     |     |     |     | Observation. |     | As  | shown | in Figure | 8,  | the base- |
lineanswerprovidesgenericinstructionswithtwo
| [Answer | A]: | {ans_a} |     |     |     |     |     |     |     |     |     |     |     |
| ------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
hallucinatedexamplelinks(https://example.com)
| [Answer | B]: | {ans_b} |     |     |     |     |          |        |            |            |           |          |          |
| ------- | --- | ------- | --- | --- | --- | --- | -------- | ------ | ---------- | ---------- | --------- | -------- | -------- |
|         |     |         |     |     |     |     | that     | do not | correspond |            | to actual | platform | re-      |
| ---     |     |         |     |     |     |     | sources. | In     | contrast,  | our answer | delivers  |          | a struc- |
tured,scenario-specificresponsethatdistinguishes
| ###       | Output    | in JSON        | only, | example: |            |        |                                                |             |     |     |           |         |       |
| --------- | --------- | -------------- | ----- | -------- | ---------- | ------ | ---------------------------------------------- | ----------- | --- | --- | --------- | ------- | ----- |
|           |           |                |       |          |            |        | between                                        | uncertified |     | and | certified | account | work- |
| {         |           |                |       |          |            |        | flows,includesvalidatedplatformlinkswithopera- |             |     |     |           |         |       |
| "scores": |           | {              |       |          |            |        | tionscreenshots,andprovidesadditionalguidance  |             |     |     |           |         |       |
|           | "Evidence | Faithfulness": |       |          | {"reason": | "...", |                                                |             |     |     |           |         |       |
forserviceproviderandrechargeaccountqueries.
|     | "grade": |     | "G"}, |     |     |     |      |            |             |     |     |               |     |
| --- | -------- | --- | ----- | --- | --- | --- | ---- | ---------- | ----------- | --- | --- | ------------- | --- |
|     |          |     |       |     |     |     | This | comparison | illustrates |     | how | our framework |     |
10

eliminateshallucinatedURLswhileimprovingan-
swercompletenessandpracticalutility.
F ServiceDeployment
Full-stackintegration. Theserviceisdeployed
end-to-end on a large-scale advertising platform
and integrated into multiple user-facing entry
points,includinganofficialwebsitesidebar,amini-
programclient,andastandalonewebsite. Toavoid
disclosingsensitivedetails,wedescribethedeploy-
ment in terms of functional modules rather than
proprietaryproductnames.
Online serving. The generator is served with
thevLLMframework(Kwonetal.,2023)on2×
NVIDIA H20 GPUs. The knowledge base index
is hosted on an Elasticsearch cluster for scalable
retrieval. Ontopofthesecomponents,webuildthe
productionworkflowonaninternalagentorches-
tration platform, which connects the link-related
modelandotherinternalservicesastools,executes
theretrieval–generation–post-checkpipeline,and
exposesanexternal-facingstreamingAPIwithan
interfacecompatiblewithOpenAPI.
Example dialogue case. Figure 9 shows a real
dialogue from our deployed advertising QA sys-
tem. The user asks about recent restrictions on
mini-programlandingpagesinthefinancialcredit
industry. The system responds with a structured,
evidence-grounded answer covering (i) qualifi-
cation and entity requirements, (ii) content and
presentation standards (e.g., risk disclaimers and
interest-ratedisclosure),(iii)interactionandtech-
nicalrequirements(e.g.,privacy,consent,andno
forcedactions),and(iv)prohibitedscenarios(e.g.,
unauthorizeddownloadsandpayment-information
placement),alongwithcompliantproductionsug-
gestions. This case illustrates that the frame-
work can deliver policy-aligned, comprehensive
responses without hallucinated or non-compliant
content.
11

Query: WherecanIfindtheAccountID?
| PreviousAsnwer |     |     |     | OurMethod |     |     |     |
| -------------- | --- | --- | --- | --------- | --- | --- | --- |
YoucanviewtheAccountIDintheadvertiserlistof ThemethodforviewingadvertisingAccountIDsvaries
theserviceprovidersystem. Thespecificstepsareas dependingontheaccountcertificationstatusandopera-
| follows: |     |     |     | tionpath,asdetailedbelow: |     |     |     |
| -------- | --- | --- | --- | ------------------------- | --- | --- | --- |
1. Logintotheserviceprovidersystem; I.AccountIDQueryforUncertifiedAdvertisingAc-
counts
2. Click“AccountList”intheworkbench;
3. Intheaccountlist,youcanviewthenamesandIDs 1. Visitthe[PlatformName]websitehttps://[platform-
| ofeachaccount. |     |     |     | domain.com],clickthe“Login”buttonintheupper |     |     |     |
| -------------- | --- | --- | --- | ------------------------------------------- | --- | --- | --- |
rightcornertoscanandlogin;
Inaddition,youcanusethefilteringfunctionforaccount
|               |                |                   |           | 2. In the account | selection          | panel, click the        | “Uncer- |
| ------------- | -------------- | ----------------- | --------- | ----------------- | ------------------ | ----------------------- | ------- |
| names and     | IDs to perform | precise or fuzzy  | searches. |                   |                    |                         |         |
|               |                |                   |           | tified Accounts”  | section            | to view the correspond- |         |
| Account names | support fuzzy  | matching queries, | and       |                   |                    |                         |         |
|               |                |                   |           | ing Account       | ID. (See operation | position                | example |
AccountIDssupportexactmatchingqueries.
athttps://[platform-cdn.com]/img1.png)
ForfurtherqueriesonAccountIDsforcertifiedorun-
II.AccountIDQueryforCertifiedAdvertisingAc-
certifiedaccounts,pleaserefertothedetailedstepsand
counts
screenshotsinthefollowinglinks:
• Account ID query for certified accounts 1. Logintothe[PlatformName]websiteandenterthe
| https://example.com |     |     |     | “[PlatformName]Workbench”; |     |     |     |
| ------------------- | --- | --- | --- | -------------------------- | --- | --- | --- |
• Account ID query for uncertified accounts 2. Click“Management”andselectthe“Entity/Business
| https://example.com |     |     |     | Unit”wheretheaccountislocatedontheleft; |                |          |          |
| ------------------- | --- | --- | --- | --------------------------------------- | -------------- | -------- | -------- |
|                     |     |     |     | 3. Click “Account                       | Management”    | to view  | the Ac-  |
|                     |     |     |     | count ID.                               | (See operation | position | examples |
|                     |     |     |     | at https://[platform-cdn.com]/img2.png  |                |          | and      |
https://[platform-cdn.com]/img3.png)
III.QueryviaServiceProviderSystem
1. Logintotheserviceprovidersystemandenterthe
“AccountList”intheworkbench;
2. ViewaccountnamesandIDsintheaccountlist,sup-
portingsearchesbyaccountname(fuzzymatching)
orID(exactmatching).
IV.RechargeAccountUIDQuery
|     |     |     |     | To view the | UID of a recharge | account, please | click |
| --- | --- | --- | --- | ----------- | ----------------- | --------------- | ----- |
“AccountSettings”in“FinancialManagement”andview
itin“AccountInformation”.
|     |     | ✗Hallucinated |     | ✓Validated |     |     |     |
| --- | --- | ------------- | --- | ---------- | --- | --- | --- |
Figure8: Comparisonofdialogueresponses: thepreviousonlineanswer(left,redborder)containshallucinated
linksmarkedinred,whileouranswer(right,greenborder)usesvalidatedlinkswithplatform-specifictermsreplaced
byplaceholders.
12

Figure9: Arealdialoguecasefromourdeployedsystem: theuserinquiresaboutrestrictionsonmini-program
landing pages in the financial credit industry; the system responds with a structured, policy-grounded answer
covering qualifications, content standards, interaction design, prohibited scenarios, and compliant production
suggestions.
13