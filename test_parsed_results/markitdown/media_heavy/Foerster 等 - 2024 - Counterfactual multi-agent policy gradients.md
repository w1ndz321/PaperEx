|     |                       |     |                            | Counterfactual |     |     | Multi-Agent     | Policy |                              | Gradients |                 |     |     |     |     |
| --- | --------------------- | --- | -------------------------- | -------------- | --- | --- | --------------- | ------ | ---------------------------- | --------- | --------------- | --- | --- | --- | --- |
|     |                       |     | JakobN.Foerster1,†         |                |     |     |                 |        | GregoryFarquhar1,†           |           |                 |     |     |     |     |
|     |                       |     | jakob.foerster@cs.ox.ac.uk |                |     |     |                 |        | gregory.farquhar@cs.ox.ac.uk |           |                 |     |     |     |     |
|     | TriantafyllosAfouras1 |     |                            |                |     |     | NantasNardelli1 |        |                              |           | ShimonWhiteson1 |     |     |     |     |
afourast@robots.ox.ac.uk nantas@robots.ox.ac.uk shimon.whiteson@cs.ox.ac.uk
|     |     |     |     | 1UniversityofOxford,UnitedKingdom |     |     |     |     | †Equalcontribution |     |     |     |     |     |     |
| --- | --- | --- | --- | --------------------------------- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- |
4202 ceD 11  ]IA.sc[  3v62980.5071:viXra
Abstract or a laboratory in which extra state information is avail-
|      |            |     |           |      |            |        |         | able and | agents | can communicate |     | freely. | This | centralised |     |
| ---- | ---------- | --- | --------- | ---- | ---------- | ------ | ------- | -------- | ------ | --------------- | --- | ------- | ---- | ----------- | --- |
| Many | real-world |     | problems, | such | as network | packet | routing |          |        |                 |     |         |      |             |     |
trainingofdecentralisedpoliciesisastandardparadigmfor
| and | the coordination |     | of  | autonomous | vehicles, | are | naturally |             |          |            |     |        |     |         |       |
| --- | ---------------- | --- | --- | ---------- | --------- | --- | --------- | ----------- | -------- | ---------- | --- | ------ | --- | ------- | ----- |
|     |                  |     |     |            |           |     |           | multi-agent | planning | (Oliehoek, |     | Spaan, | and | Vlassis | 2008; |
modelledascooperativemulti-agentsystems.Thereisagreat
|      |     |                   |     |          |         |     |              | Kraemer | and Banerjee | 2016) | and | has | recently | been | picked |
| ---- | --- | ----------------- | --- | -------- | ------- | --- | ------------ | ------- | ------------ | ----- | --- | --- | -------- | ---- | ------ |
| need | for | new reinforcement |     | learning | methods |     | that can ef- |         |              |       |     |     |          |      |        |
ficiently learn decentralised policies for such systems. To up by the deep RL community (Foerster et al. 2016; Jorge,
this end, we propose a new multi-agent actor-critic method Ka˚geba¨ck,andGustavsson2016).However,thequestionof
calledcounterfactualmulti-agent(COMA)policygradients. how best to exploit the opportunity for centralised learning
| COMA      | uses          | a centralised |        | critic      | to estimate    | the     | Q-function   | remainsopen. |         |               |     |             |                |        |         |
| --------- | ------------- | ------------- | ------ | ----------- | -------------- | ------- | ------------ | ------------ | ------- | ------------- | --- | ----------- | -------------- | ------ | ------- |
| and       | decentralised |               | actors | to optimise | the            | agents’ | policies. In |              |         |               |     |             |                |        |         |
|           |               |               |        |             |                |         |              | Another      | crucial | challenge     | is  | multi-agent |                | credit | assign- |
| addition, |               | to address    | the    | challenges  | of multi-agent |         | credit as-   |              |         |               |     |             |                |        |         |
|           |               |               |        |             |                |         |              | ment (Chang, | Ho,     | and Kaelbling |     | 2003):      | in cooperative |        | set-    |
signment,itusesacounterfactualbaselinethatmarginalises
|     |          |         |         |       |         |           |         | tings, joint | actions      | typically | generate |     | only global | rewards, |      |
| --- | -------- | ------- | ------- | ----- | ------- | --------- | ------- | ------------ | ------------ | --------- | -------- | --- | ----------- | -------- | ---- |
| out | a single | agent’s | action, | while | keeping | the other | agents’ |              |              |           |          |     |             |          |      |
|     |          |         |         |       |         |           |         | making       | it difficult | for each  | agent    | to  | deduce      | its own  | con- |
actionsfixed.COMAalsousesacriticrepresentationthatal-
|     |     |     |     |     |     |     |     | tribution | to the | team’s success. |     | Sometimes | it  | is possible | to  |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------ | --------------- | --- | --------- | --- | ----------- | --- |
lowsthecounterfactualbaselinetobecomputedefficientlyin
asingleforwardpass.WeevaluateCOMAinthetestbedof designindividualrewardfunctionsforeachagent.However,
StarCraftunitmicromanagement,usingadecentralisedvari- theserewardsarenotgenerallyavailableincooperativeset-
antwithsignificantpartialobservability.COMAsignificantly tingsandoftenfailtoencourageindividualagentstosacri-
improvesaverageperformanceoverothermulti-agentactor- fice for the greater good. This often substantially impedes
criticmethodsinthissetting,andthebestperformingagents multi-agent learning in challenging tasks, even with rela-
| are | competitive |     | with state-of-the-art |     | centralised |     | controllers |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --------------------- | --- | ----------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
tivelysmallnumbersofagents.
thatgetaccesstothefullstate.
|     |     |     |     |     |     |     |     | In this | paper, | we propose | a   | new multi-agent |     | RL  | method |
| --- | --- | --- | --- | --- | --- | --- | --- | ------- | ------ | ---------- | --- | --------------- | --- | --- | ------ |
calledcounterfactualmulti-agent(COMA)policygradients,
1 Introduction
inordertoaddresstheseissues.COMAtakesanactor-critic
| Manycomplexreinforcementlearning(RL)problemssuch |                  |     |     |            |     |          |             |                  |                |           |             |     |           |           | actor, |
| ------------------------------------------------ | ---------------- | --- | --- | ---------- | --- | -------- | ----------- | ---------------- | -------------- | --------- | ----------- | --- | --------- | --------- | ------ |
|                                                  |                  |     |     |            |     |          |             | (Konda           | and Tsitsiklis | 2000)     | approach,   |     | in which  | the       |        |
| as                                               | the coordination |     | of  | autonomous |     | vehicles | (Cao et al. |                  |                |           |             |     |           |           |        |
|                                                  |                  |     |     |            |     |          |             | i.e., thepolicy, |                | istrained | byfollowing |     | agradient | estimated |        |
2013),networkpacketdelivery(Ye,Zhang,andYang2015), byacritic.COMAisbasedonthreemainideas.
and distributed logistics (Ying and Dayong 2005) are nat- First, COMA uses a centralised critic. The critic is only
| urally | modelled | as  | cooperative |     | multi-agent | systems. | How- |     |     |     |     |     |     |     |     |
| ------ | -------- | --- | ----------- | --- | ----------- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
usedduringlearning,whileonlytheactorisneededduring
| ever, | RL methods |     | designed | for | single | agents | typically fare |     |     |     |     |     |     |     |     |
| ----- | ---------- | --- | -------- | --- | ------ | ------ | -------------- | --- | --- | --- | --- | --- | --- | --- | --- |
execution.Sincelearningiscentralised,wecanthereforeuse
| poorly | on  | such tasks, | since | the | joint | action | space of the |     |     |     |     |     |     |     |     |
| ------ | --- | ----------- | ----- | --- | ----- | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
acentralisedcriticthatconditionsonthejointactionandall
agentsgrowsexponentiallywiththenumberofagents. availablestateinformation,whileeachagent’spolicycondi-
Tocopewithsuchcomplexity,itisoftennecessarytore- tionsonlyonitsownaction-observationhistory.
sorttodecentralisedpolicies,inwhicheachagentselectsits
Second,COMAusesacounterfactualbaseline.Theidea
ownactionconditionedonlyonitslocalaction-observation
isinspiredbydifferencerewards(WolpertandTumer2002;
| history. | Furthermore, |     | partial | observability |     | and | communica- |     |     |     |     |     |     |     |     |
| -------- | ------------ | --- | ------- | ------------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
TumerandAgogino2007),inwhicheachagentlearnsfrom
tionconstraintsduringexecutionmaynecessitatetheuseof a shaped reward that compares the global reward to the re-
decentralisedpoliciesevenwhenthejointactionspaceisnot ward received when that agent’s action is replaced with a
prohibitivelylarge.
defaultaction.Whiledifferencerewardsareapowerfulway
| Hence, | there | is  | a great | need | for new | RL  | methods that |            |             |        |             |     |      |         |     |
| ------ | ----- | --- | ------- | ---- | ------- | --- | ------------ | ---------- | ----------- | ------ | ----------- | --- | ---- | ------- | --- |
|        |       |     |         |      |         |     |              | to perform | multi-agent | credit | assignment, |     | they | require | ac- |
canefficientlylearndecentralisedpolicies.Insomesettings,
cesstoasimulatororestimatedrewardfunction,andingen-
the learning itself may also need to be decentralised. How- eral it is unclear how to choose the default action. COMA
ever, in many cases, learning can take place in a simulator addresses this by using the centralised critic to compute an
Copyright©2018,AssociationfortheAdvancementofArtificial agent-specific advantage function that compares the esti-
Intelligence(www.aaai.org).Allrightsreserved. matedreturnforthecurrentjointactiontoacounterfactual

baselinethatmarginalisesoutasingleagent’saction,while ever,thesemethodsdonotallowforextrastateinformation
keepingtheotheragents’actionsfixed.Thisissimilartocal- tobeusedduringlearninganddonotaddressthemulti-agent
culatinganaristocratutility(WolpertandTumer2002),but creditassignmentproblem.
avoidstheproblemofarecursiveinterdependencebetween Gupta, Egorov, and Kochenderfer (2017) investigate
the policy and utility function because the expected contri- actor-critic methods for decentralised execution with cen-
bution of the counterfactual baseline to the policy gradient tralised training. However, in their methods both the actors
| is zero. | Hence, instead | of  | relying | on extra | simulations, | ap- |     |     |     |     |     |     |     |     |
| -------- | -------------- | --- | ------- | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
andthecriticconditiononlocal,per-agent,observationsand
proximations,orassumptionsregardingappropriatedefault actions,andmulti-agentcreditassignmentisaddressedonly
actions,COMAcomputesaseparatebaselineforeachagent withhand-craftedlocalrewards.
that relies on the centralised critic to reason about counter- MostpreviousapplicationsofRLtoStarCraftmicroman-
factualsinwhichonlythatagent’sactionchanges. agementuseacentralisedcontroller,withaccesstothefull
Third,COMAusesacriticrepresentationthatallowsthe
|     |     |     |     |     |     |     | state, and | control | of  | all units, | although | the | architecture | of  |
| --- | --- | --- | --- | --- | --- | --- | ---------- | ------- | --- | ---------- | -------- | --- | ------------ | --- |
counterfactualbaselinetobecomputedefficiently.Inasin- the controllers exploits the multi-agent nature of the prob-
gleforwardpass,itcomputestheQ-valuesforallthediffer- lem.Usunieretal.(2016)useagreedyMDP,whichateach
entactionsofagivenagent,conditionedontheactionsofall timestep sequentially chooses actions for agents given all
the other agents. Because a single centralised critic is used previous actions, in combination with zero-order optimisa-
forallagents,allQ-valuesforallagentscanbecomputedin
tion,whilePengetal.(2017)useanactor-criticmethodthat
asinglebatchedforwardpass. reliesonRNNstoexchangeinformationbetweentheagents.
We evaluate COMA in the testbed of StarCraft unit mi- The closest to our problem setting is that of Foerster et
cromanagement1,whichhasrecentlyemergedasachalleng- al.(2017),whoalsouseamulti-agentrepresentationandde-
ingRLbenchmarktaskwithhighstochasticity,alargestate-
|     |     |     |     |     |     |     | centralised | policies. | However, |     | they focus | on  | stabilising | ex- |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --------- | -------- | --- | ---------- | --- | ----------- | --- |
actionspace,anddelayedrewards.Previousworks(Usunier
periencereplaywhileusingDQNanddonotmakefulluse
etal.2016;Pengetal.2017)havemadeuseofacentralised ofthecentralisedtrainingregime.Astheydonotreporton
controlpolicythatconditionsontheentirestateandcanuse absolutewin-rateswedonotcompareperformancedirectly.
powerful macro-actions, using StarCraft’s built-in planner, However, Usunier et al. (2016) address similar scenarios
that combine movement and attack actions. To produce a to our experiments and implement a DQN baseline in a
meaningfullydecentralisedbenchmarkthatproveschalleng-
fullyobservablesetting.InSection6wethereforereportour
ingforscenarioswithevenrelativelyfewagents,wepropose
competitiveperformanceagainstthesestate-of-the-artbase-
a variant that massively reduces each agent’s field-of-view lines, while maintaining decentralised control. Omidshafiei
andremovesaccesstothesemacro-actions. etal.(2017)alsoaddressthestabilityofexperiencereplayin
Our empirical results on this new benchmark show that multi-agentsettings,butassumeafullydecentralisedtrain-
| COMA | can significantly |     | improve | performance |     | over other |     |     |     |     |     |     |     |     |
| ---- | ----------------- | --- | ------- | ----------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
ingregime.
multi-agentactor-criticmethods,aswellasablatedversions
|     |     |     |     |     |     |     | (Lowe | et al. | 2017) | concurrently |     | propose | a multi-agent |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | ------ | ----- | ------------ | --- | ------- | ------------- | --- |
ofCOMAitself.Inaddition,COMA’sbestagentsarecom- policy-gradientalgorithmusingcentralisedcritics.Theirap-
petitive with state-of-the-art centralised controllers that are proachdoesnotaddressmulti-agentcreditassignment.Un-
givenaccesstofullstateinformationandmacro-actions.
likeourwork,itlearnsaseparatecentralisedcriticforeach
agentandisappliedtocompetitiveenvironmentswithcon-
|     |     | 2 RelatedWork |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tinuousactionspaces.
|          |             |     |          |         |      |            | Our work | builds   |     | directly | off of | the idea | of difference |     |
| -------- | ----------- | --- | -------- | ------- | ---- | ---------- | -------- | -------- | --- | -------- | ------ | -------- | ------------- | --- |
| Although | multi-agent | RL  | has been | applied | in a | variety of |          |          |     |          |        |          |               |     |
|          |             |     |          |         |      |            | rewards  | (Wolpert | and | Tumer    | 2002). | The      | relationship  | of  |
settings(Busoniu,Babuska,andDeSchutter2008;Yangand
Gu 2004), it has often been restricted to tabular methods COMAtothislineofworkisdiscussedinSection4.
| and simple | environments. |     | One | exception | is recent | work in |     |     |     |     |     |     |     |     |
| ---------- | ------------- | --- | --- | --------- | --------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
deep multi-agent RL, which can scale to high dimensional 3 Background
| input and | action spaces. |                  | Tampuu | et al.     | (2015) use | a com- |              |     |              |             |             |            |           |         |
| --------- | -------------- | ---------------- | ------ | ---------- | ---------- | ------ | ------------ | --- | ------------ | ----------- | ----------- | ---------- | --------- | ------- |
|           |                |                  |        |            |            |        | We consider  | a   | fully        | cooperative | multi-agent |            | task that | can     |
| bination  | of DQN         | with independent |        | Q-learning | (Tan       | 1993;  |              |     |              |             |             |            |           |         |
|           |                |                  |        |            |            |        | be described | as  | a stochastic |             | game        | G, defined | by        | a tuple |
ShohamandLeyton-Brown2009)tolearnhowtoplaytwo-
|     |     |     |     |     |     |     | G = ⟨S,U,P,r,Z,O,n,γ⟩, |     |     |     | in which | n agents | identified |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | -------- | -------- | ---------- | --- |
playerpong.Morerecentlythesamemethodhasbeenused
byLeiboetal.(2017)tostudytheemergenceofcollabora- by a ∈ A ≡ {1,...,n} choose sequential actions. The en-
|     |     |     |     |     |     |     | vironment | has | a true | state s | ∈ S. At | each | time step, | each |
| --- | --- | --- | --- | --- | --- | --- | --------- | --- | ------ | ------- | ------- | ---- | ---------- | ---- |
tionanddefectioninsequentialsocialdilemmas.
|     |     |     |     |     |     |     | agent simultaneously |     |     | chooses | an action | ua  | ∈ U, | forming |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | ------- | --------- | --- | ---- | ------- |
Alsorelatedisworkontheemergenceofcommunication
|     |     |     |     |     |     |     | a joint action |     | u ∈ U | ≡ Un | which | induces | a transition | in  |
| --- | --- | --- | --- | --- | --- | --- | -------------- | --- | ----- | ---- | ----- | ------- | ------------ | --- |
betweenagents,learnedbygradientdescent(Dasetal.2017;
|          |            |       |            |     |               |     | the environment |     | according | to  | the state | transition | function |     |
| -------- | ---------- | ----- | ---------- | --- | ------------- | --- | --------------- | --- | --------- | --- | --------- | ---------- | -------- | --- |
| Mordatch | and Abbeel | 2017; | Lazaridou, |     | Peysakhovich, | and |                 |     |           |     |           |            |          |     |
|          |            |       |            |     |               |     | P(s′|s,u)       | : S | ×U×S      | →   | [0,1].    |            |          |     |
Baroni 2016; Foerster et al. 2016; Sukhbaatar, Fergus, and The agents all share the
Randγ
|     |     |     |     |     |     |     | samerewardfunctionr(s,u) |     |     |     | : S ×U | →   |     | ∈ [0,1) |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | ------ | --- | --- | ------- |
others2016).Inthislineofwork,passinggradientsbetween
isadiscountfactor.
agentsduringtrainingandsharingparametersaretwocom-
|          |         |           |     |             |           |      | We consider |              | a partially |     | observable    | setting, | in     | which  |
| -------- | ------- | --------- | --- | ----------- | --------- | ---- | ----------- | ------------ | ----------- | --- | ------------- | -------- | ------ | ------ |
| mon ways | to take | advantage | of  | centralised | training. | How- |             |              |             |     |               |          |        |        |
|          |         |           |     |             |           |      | agents draw | observations |             | z   | ∈ Z according |          | to the | obser- |
1StarCraft and its expansion StarCraft: Brood War are trade- vation function O(s,a) : S ×A → Z. Each agent has an
marksofBlizzardEntertainment™. action-observationhistoryτa ∈T ≡(Z×U)∗,onwhichit

conditionsastochasticpolicyπa(ua|τa) : T ×U → [0,1]. where y(λ) = (1 − λ) (cid:80)∞ λn−1G(n), and the n-step
n=1 t
We denote joint quantities over agents in bold, and joint returns G(n) are calculated with bootstrapped values esti-
quantities over agents other than a given agent a with the t
matedbyatargetnetwork (Mnihetal.2015)withparame-
superscript−a. terscopiedperiodicallyfromθc.
ThediscountedreturnisR = (cid:80)∞ γlr .Theagents’
t l=0 t+l
joint policy induces a value function, i.e., an expectation
4 Methods
over R , Vπ(s ) = E [R |s ], and an action-
value f t unction t Qπ(s ,u st+ ) 1:∞ = ,ut:E∞ t t [R |s ,u ]. Inthissection,wedescribeapproachesforextendingpolicy
The advantage func t tion t is give st n +1: b ∞ y ,ut A +1 π :∞ (s ,u t ) t t = gradientstoourmulti-agentsetting.
t t
Qπ(s ,u )−Vπ(s ).
t t t
IndependentActor-Critic
Following previous work (Oliehoek, Spaan, and Vlassis
2008; Kraemer and Banerjee 2016; Foerster et al. 2016; The simplest way to apply policy gradients to multiple
Jorge,Ka˚geba¨ck,andGustavsson2016),ourproblemsetting agents is to have each agent learn independently, with its
allowscentralisedtrainingbutrequiresdecentralisedexecu- own actor and critic, from its own action-observation his-
tion.Thisisanaturalparadigmforalargesetofmulti-agent tory. This is essentially the idea behind independent Q-
problemswheretrainingiscarriedoutusingasimulatorwith learning (Tan 1993), which is perhaps the most popular
additionalstateinformation,buttheagentsmustrelyonlo- multi-agentlearningalgorithm,butwithactor-criticinplace
calaction-observationhistoriesduringexecution.Tocondi- of Q-learning. Hence, we call this approach independent
tiononthisfullhistory,adeepRLagentmaymakeuseofa actor-critic(IAC).
recurrentneuralnetwork(HausknechtandStone2015),typ- InourimplementationofIAC,wespeedlearningbyshar-
ically with a gated model such as LSTM (Hochreiter and ingparametersamongtheagents,i.e.,welearnonlyoneac-
Schmidhuber1997)orGRU(Choetal.2014). torandonecritic,whichareusedbyallagents.Theagents
In Section 4, we develop a new multi-agent policy gra- canstillbehavedifferentlybecausetheyreceivedifferentob-
dient method for tackling this setting. In the remainder of servations, including an agent-specific ID, and thus evolve
this section, we provide some background on single-agent differenthiddenstates.Learningremainsindependentinthe
policygradientmethods(Suttonetal.1999).Suchmethods sense that each agent’s critic estimates only a local value
optimise a single agent’s policy, parameterised by θπ, by function, i.e., one that conditions on ua, not u. Though we
performing gradient ascent on an estimate of the expected arenotawareofpreviousapplicationsofthisspecificalgo-
discountedtotalrewardJ = E [R ].Perhapsthesimplest rithm, we do not consider it a significant contribution but
π 0
formofpolicygradientisREINFORCE(Williams1992),in insteadmerelyabaselinealgorithm.
whichthegradientis: WeconsidertwovariantsofIAC.Inthefirst,eachagent’s
(cid:34) T (cid:35) critic estimates V(τa) and follows a gradient based on
(cid:88) the TD error, as described in Section 3. In the second,
g =E R ∇ logπ(u |s ) . (1)
s0:∞,u0:∞ t θπ t t each agent’s critic estimates Q(τa,ua) and follows a gra-
t=0 dient based on the advantage: A(τa,ua) = Q(τa,ua) −
In actor-critic approaches (Sutton et al. 1999; Konda and V(τa),whereV(τa) = (cid:80) π(ua|τa)Q(τa,ua).Indepen-
ua
Tsitsiklis 2000; Schulman et al. 2015), the actor, i.e., the dentlearningisstraightforward,butthelackofinformation
policy, is trained by following a gradient that depends on sharing at training time makes it difficult to learn coordi-
a critic, which usually estimates a value function. In par- nated strategies that depend on interactions between multi-
ticular, R t is replaced by any expression equivalent to pleagents,orforanindividualagenttoestimatethecontri-
Q(s t ,u t )−b(s t ),whereb(s t )isabaselinedesignedtore- butionofitsactionstotheteam’sreward.
ducevariance(WeaverandTao2001).Acommonchoiceis
b(s ) = V(s ), in which case R is replaced by A(s ,u ). CounterfactualMulti-AgentPolicyGradients
t t t t t
AnotheroptionistoreplaceR withthetemporaldifference
t The difficulties discussed above arise because, beyond pa-
(TD)errorr +γV(s )−V(s),whichisanunbiasedes-
t t+1 rameter sharing, IAC fails to exploit the fact that learning
timate of A(s ,u ). In practice, the gradient must be esti-
t t is centralised in our setting. In this section, we propose
matedfromtrajectoriessampledfromtheenvironment,and
counterfactualmulti-agent(COMA)policygradients,which
the(action-)valuefunctionsmustbeestimatedwithfunction
overcomethislimitation.ThreemainideasunderlyCOMA:
approximators. Consequently, the bias and variance of the
1)centralisationofthecritic,2)useofacounterfactualbase-
gradient estimate depends strongly on the exact choice of
line,and3)useofacriticrepresentationthatallowsefficient
estimator(KondaandTsitsiklis2000).
evaluationofthebaseline.Theremainderofthissectionde-
In this paper, we train critics fc(·,θc) on-policy to es-
scribestheseideas.
timate either Q or V, using a variant of TD(λ) (Sutton
First, COMA uses a centralised critic. Note that in IAC,
1988) adapted for use with deep neural networks. TD(λ) each actor π(ua|τa) and each critic Q(τa,ua) or V(τa)
uses a mixture of n-step returns G( t n) = (cid:80)n l=1 γl−1r t+l + conditions only on the agent’s own action-observation his-
γnfc(· t+n ,θc).Inparticular,thecriticparametersθcareup- tory τa. However, the critic is used only during learning
datedbyminibatchgradientdescenttominimisethefollow- and only the actor is needed during execution. Since learn-
ingloss: ing is centralised, we can therefore use a centralised critic
L (θc)=(y(λ)−fc(· ,θc))2, (2) thatconditionsonthetrueglobalstates,ifitisavailable,as
t t

|     |      | AA11               |      |              | AA22               |      |        |                |                                         |     |      |     |     |     |
| --- | ---- | ------------------ | ---- | ------------ | ------------------ | ---- | ------ | -------------- | --------------------------------------- | --- | ---- | --- | --- | --- |
|     |      |                    |      |              |                    |      |        | 𝜋a =𝜋(ha , 𝜀)  |                                         |     | Aa   |     |     |     |
|     |      | tt                 |      | CCrriittiicc | tt                 |      |        | t  t           |                                         |     | t    |     |     |     |
|     |      | 𝜋𝜋((hh11,,  𝜀𝜀))   |      |              | 𝜋𝜋((hh22,,  𝜀𝜀))   |      |        |                |                                         |     |      |     |     |     |
|     |      |                    |      |              |                    |      | (𝜀)    |                | (ua, 𝜋a)                                |     | COMA |     |     |     |
|     |      |                    |      |              |                    |      |        |                |                                         | t t |      |     |     |     |
|     | hh11 |                    | uu11 | uu22         |                    | hh22 |        |                |                                         |     |      |     |     |     |
|     |      |                    | tt   | tt           |                    |      |        | ha             | {Q(ua=1, u-a,..),. .,Q(ua=|U|, u-a,..)} |     |      |     |     |     |
|     |      |                    |      |              |                    |      |        | t              |                                         |     | t    |     | t   |     |
|     |      | AAccttoorr  11     |      |              | AAccttoorr  22     |      |        |                |                                         |     |      |     |     |     |
|     |      |                    |      |              |                    |      | ((hhaa | ))             | (ha)                                    |     |      |     |     |     |
GRU
|     |     |             | o, s |     r ,h       |             |     | tt--11 |     | t   |     |     |     |     |     |
| --- | --- | ----------- | ---- | -------------- | ----------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
|     |     |             |      | t t   t    t-1 |             |     |        |     |     |     |     |     |     |     |
|     |     | oo11   uu11 |      |                | uu22 oo22   |     |        |     |     |     |     |     |     |     |
|     |     | tt          | tt   |                | tt          | tt  |        |     |     |     |     |     |     |     |
EEnnvviirroonnmmeenntt
|     |     |     |     |     |     |     |     | (oa, a, ua | )   | (u-a, s, oa, a, u |       | ,h)    |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ----------------- | ----- | ------ | --- | --- |
|     |     |     |     |     |     |     |     | t t-1      |     |                   | t t t | t-1  t |     |     |
|     |     |     |     | (a) |     |     |     | (b)        |     |                   | (c)   |        |     |     |
Figure 1: In (a), information flow between the decentralised actors, the environment and the centralised critic in COMA; red
arrowsandcomponentsareonlyrequiredduringcentralisedlearning.In(b)and(c),architecturesoftheactorandcritic.
Actor 2
well as the joint action-observation histories τ. Each actor waythatavoidstheseproblems.COMAlearnsacentralised
conditions on its own action-observation histories τa, with critic, Q(s,τ,u) that estimates Q-values for the joint ac-
parametersharing,asinIAC.Figure1aillustratesthissetup. tionuconditionedonthecentralstatesandthejointaction-
A naive way to use this centralised critic would be for observation history.For each agent a we canthen compute
each actor to follow a gradient based on the TD error esti- anadvantagefunctionthatcomparestheQ-valueforthecur-
matedfromthiscritic: rentactionua toacounterfactualbaselinethatmarginalises
outua,whilekeepingtheotheragents’actionsu−afixed:
logπ(ua|τa)(r+γV(s
g =∇ θπ t+1 )−V(s t )). (3) Aa(s,τ,u)=Q(s,τ,u)− (cid:88) πa(u′a|τa)Q(s,τ,(u−a,u′a)).
t t
| However,   |     | such an  | approach | fails to | address         | a key credit |     |     |     |     | u′a |     |     |     |
| ---------- | --- | -------- | -------- | -------- | --------------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
| assignment |     | problem. | Because  | the TD   | error considers | only         |     |     |     |     |     |     |     | (4) |
global rewards, the gradient computed for each actor does Hence, Aa(s,τ,ua) computes a separate baseline for each
not explicitly reason about how that particular agent’s ac- agentthatusesthecentralisedcritictoreasonaboutcounter-
|     |     |     |     |     |     |     |     | factuals in | which only | a’s | action changes, | learned |     | directly |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------- | ---------- | --- | --------------- | ------- | --- | -------- |
tionscontributetothatglobalreward.Sincetheotheragents
maybeexploring,thegradientforthatagentbecomesvery fromagents’experiencesinsteadofrelyingonextrasimula-
noisy,particularlywhentherearemanyagents. tions,arewardmodel,orauser-designeddefaultaction.
Therefore, COMA uses a counterfactual baseline. The This advantage has the same form as the aristocrat util-
idea is inspired by difference rewards (Wolpert and Tumer ity (Wolpert and Tumer 2002). However, optimising for an
2002), in which each agent learns from a shaped reward aristocrat utility using value-based methods creates a self-
Da = r(s,u) − r(s,(u−a,ca)) that compares the global consistencyproblembecausethepolicyandutilityfunction
rewardtotherewardreceivedwhentheactionofagentais depend recursively on each other. As a result, prior work
replacedwithadefaultactionca.Anyactionbyagentathat focused on difference evaluations using default states and
improves Da also improves the true global reward r(s,u), actions.COMAisdifferentbecausethecounterfactualbase-
r(s,(u−a,ca)) line’s expected contribution to the gradient, as with other
| because |     |     | does | not depend | on agent | a’s | ac- |     |     |     |     |     |     |     |
| ------- | --- | --- | ---- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tions. policy gradient baselines, is zero. Thus, while the baseline
Differencerewardsareapowerfulwaytoperformmulti- doesdependonthepolicy,itsexpectationdoesnot.Conse-
agent credit assignment. However, they typically require quently,COMAcanusethisformoftheadvantagewithout
access to a simulator in order to estimate r(s,(u−a,ca)). creatingaself-consistencyproblem.
When a simulator is already being used for learning, dif- WhileCOMA’sadvantagefunctionreplacespotentialex-
ference rewards increase the number of simulations that tra simulations with evaluations of the critic, those evalu-
must be conducted, since each agent’s difference reward ations may themselves be expensive if the critic is a deep
requires a separate counterfactual simulation. Proper and neuralnetwork.Furthermore,inatypicalrepresentation,the
Tumer (2012) and Colby, Curran, and Tumer (2015) pro- numberofoutputnodesofsuchanetworkwouldequal|U|n,
pose estimating difference rewards using function approxi- the size of the joint action space, making it impractical to
mationratherthanasimulator.However,thisstillrequiresa train.Toaddressboththeseissues,COMAusesacriticrep-
user-specifieddefaultactioncathatcanbedifficulttochoose resentation that allows for efficient evaluation of the base-
inmanyapplications.Inanactor-criticarchitecture,thisap- line. In particular, the actions of the other agents, u−a, are
t
proachwouldalsointroduceanadditionalsourceofapprox- part of the input to the network, which outputs a Q-value
imationerror. foreachofagenta’sactions,asshowninFigure1c.Conse-
A key insight underlying COMA is that a centralised quently,thecounterfactualadvantagecanbecalculatedeffi-
critic can be used to implement difference rewards in a ciently by a single forward pass of the actor and critic, for

eachagent.Furthermore,thenumberofoutputsisonly|U| route.Thesepowerfulattack-movemacro-actionsmakethe
insteadof(|U|n).Whilethenetworkhasalargeinputspace controlproblemconsiderablyeasier.
thatscaleslinearlyinthenumberofagentsandactions,deep To create a more challenging benchmark that is mean-
neuralnetworkscangeneralisewellacrosssuchspaces. ingfully decentralised, we impose a restricted field of view
In this paper, we focus on settings with discrete actions. on the agents, equal to the firing range of ranged units’
However, COMA can be easily extended to continuous ac- weapons, shown in Figure 2. This departure from the stan-
tionsspacesbyestimatingtheexpectationin(4)withMonte
dardsetupforcentralisedStarCraftcontrolhasthreeeffects.
| Carlo samples | or  | using | functional | forms | that render | it ana- |     |     |     |     |     |
| ------------- | --- | ----- | ---------- | ----- | ----------- | ------- | --- | --- | --- | --- | --- |
lytical,e.g.,Gaussianpoliciesandcritic.
| The following                                      |              | lemma       | establishes     | the | convergence  | of          |     |     |     |     |     |
| -------------------------------------------------- | ------------ | ----------- | --------------- | --- | ------------ | ----------- | --- | --- | --- | --- | --- |
| COMA                                               | to a locally | optimal     | policy.         | The | proof        | follows di- |     |     |     |     |     |
| rectly from                                        | the          | convergence | of single-agent |     | actor-critic | al-         |     |     |     |     |     |
| gorithms(Suttonetal.1999),andissubjecttothesameas- |              |             |                 |     |              |             |     | x   |     |     |     |
sumptions.Lyuetal.(2024,AppendixE.2)provearelated
| result, showing |     | that a | family of | cooperative | policy | gradi- |     |     |     |     |     |
| --------------- | --- | ------ | --------- | ----------- | ------ | ------ | --- | --- | --- | --- | --- |
entmethodswithcentralizedcritics,whichincludesCOMA,
convergetolocaloptimaassumingaccesstothecorrectpol-
icyvalues,i.e.,aperfectcritic.
| Lemma1. | Foranactor-criticalgorithmwithacompatible |     |     |     |     |     |     |     |     |     |     |
| ------- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TD(1)criticfollowingaCOMApolicygradient Figure2:Startingpositionwithexamplelocalfieldofview
|     |     | (cid:34) |     |     |     | (cid:35) |          |        |     |     |     |
| --- | --- | -------- | --- | --- | --- | -------- | -------- | ------ | --- | --- | --- |
|     |     |          |     |     |     |          | forthe2d | 3zmap. |     |     |     |
(cid:88)
| g   | =E  | ∇   | logπa(ua|τa)Aa(s,τ,u) |     |     | (5) |     |     |     |     |     |
| --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| k   | π   |     | θk                    |     |     |     |     |     |     |     |     |
a First, it introduces significant partial observability. Sec-
ateachiterationk, ond, it means units can only attack when they are in range
ofenemies,removingaccesstotheStarCraftmacro-actions.
liminf||∇J||=0 w.p.1. (6) Third, agents cannot distinguish between enemies who are
|     |     | k   |     |     |     |     | dead and | those who are | out of range | and so can issue | in- |
| --- | --- | --- | --- | --- | --- | --- | -------- | ------------- | ------------ | ---------------- | --- |
Proof. SeeAppendixA.
validattackcommandsatsuchenemies,whichresultsinno
actionbeingtaken.Thissubstantiallyincreasestheaverage
5 ExperimentalSetup sizeoftheactionspace,whichinturnincreasesthedifficulty
ofbothexplorationandcontrol.
Inthissection,wedescribetheStarCraftproblemtowhich
Underthesedifficultconditions,scenarioswithevenrela-
| we apply | COMA, | as well | as details | of  | the state | features, |     |     |     |     |     |
| -------- | ----- | ------- | ---------- | --- | --------- | --------- | --- | --- | --- | --- | --- |
networkarchitectures,trainingregimes,andablations. tivelysmallnumbersofunitsbecomemuchhardertosolve.
Decentralised StarCraft Micromanagement. StarCraft AsseeninTable1,wecompareagainstasimplehand-coded
is a rich environment with stochastic dynamics that cannot heuristicthatinstructstheagentstorunforwardsintorange
andthenfocustheirfire,attackingeachenemyinturnuntil
beeasilyemulated.Manysimplermulti-agentsettings,such
|     |     |     |     |     |     |     | it dies. This | heuristic achieves | a 98% | win rate on 5m | with |
| --- | --- | --- | --- | --- | --- | --- | ------------- | ------------------ | ----- | -------------- | ---- |
asPredator-Prey(Tan1993)orPacketWorld(Weyns,Helle-
boogh,andHolvoet2005),bycontrast,havefullsimulators afullfieldofview,butonly66%inoursetting.Toperform
withcontrolledrandomnessthatcanbefreelysettoanystate wellinthistask,theagentsmustlearntocooperatebyposi-
inordertoperfectlyreplayexperiences.Thismakesitpos- tioningproperlyandfocussingtheirfire,whileremembering
whichenemyandallyunitsarealiveoroutofview.
sible,thoughcomputationallyexpensive,tocomputediffer-
ence rewards via extra simulations. In StarCraft, as in the All agents receive the same global reward at each time
realworld,thisisnotpossible. step, equal to the sum of damage inflicted on the opponent
In this paper, we focus on the problem of microman- unitsminushalfthedamagetaken.Killinganopponentgen-
agement in StarCraft, which refers to the low-level con- eratesarewardof10points,andwinningthegamegenerates
arewardequaltotheteam’sremainingtotalhealthplus200.
| trol of individual |     | units’ | positioning | and | attack | commands |     |     |     |     |     |
| ------------------ | --- | ------ | ----------- | --- | ------ | -------- | --- | --- | --- | --- | --- |
Thisdamage-basedrewardsignaliscomparabletothatused
| as they fight | enemies. | This | task | is naturally | represented | as  |     |     |     |     |     |
| ------------- | -------- | ---- | ---- | ------------ | ----------- | --- | --- | --- | --- | --- | --- |
amulti-agentsystem,whereeachStarCraftunitisreplaced byUsunieretal.(2016).Unlike(Pengetal.2017),ourap-
byadecentralisedcontroller.Weconsiderseveralscenarios proachdoesnotrequireestimatinglocalrewards.
withsymmetricteamsformedof:3marines(3m),5marines State Features. The actor and critic receive different in-
(5m),5wraiths(5w),or2dragoonswith3zealots(2d 3z). putfeatures,correspondingtolocalobservationsandglobal
The enemy team is controlled by the StarCraft AI, which state,respectively.Bothincludefeaturesforalliesandene-
usesreasonablebutsuboptimalhand-craftedheuristics. mies.Unitscanbeeitheralliesorenemies,whileagentsare
We allow the agents to choose from a set of discrete thedecentralisedcontrollersthatcommandallyunits.
actions: move[direction], attack[enemy id], The local observations for every agent are drawn only
stop,andnoop.IntheStarCraftgame,whenaunitselects from a circular subset of the map centred on the unit it
an attack action, it first moves into attack range before controlsandincludeforeachunitwithinthisfieldofview:
firing, using the game’s built-in pathfinding to choose a distance, relative x, relative y, unit type

|     |     |     | COMA      |     | central-QV |     |     | IAC-V |     |     | IAC-Q |     |
| --- | --- | --- | --------- | --- | ---------- | --- | --- | ----- | --- | --- | ----- | --- |
|     |     |     | central-V |     | heuristic  |     |     |       |     |     |       |     |
|     | 90  |     |           |     |            |     | 90  |       |     |     |       |     |
|     | 80  |     |           |     |            |     | 80  |       |     |     |       |     |
% niW egarevA
|     | % niW egarevA 70 |     |     |            |                  |     | 70  |         |            |         |     |     |
| --- | ---------------- | --- | --- | ---------- | ---------------- | --- | --- | ------- | ---------- | ------- | --- | --- |
|     | 60               |     |     |            |                  |     | 60  |         |            |         |     |     |
|     | 50               |     |     |            |                  |     | 50  |         |            |         |     |     |
|     | 40               |     |     |            |                  |     | 40  |         |            |         |     |     |
|     | 30               |     |     |            |                  |     | 30  |         |            |         |     |     |
|     | 20               |     |     |            |                  |     | 20  |         |            |         |     |     |
|     | 10               |     |     |            |                  |     | 10  |         |            |         |     |     |
|     | 0                |     |     |            |                  |     | 0   |         |            |         |     |     |
|     |                  | 20k | 40k | 60k        | 80k 100k120k140k |     |     | 10k 20k | 30k 40k    | 50k 60k | 70k |     |
|     |                  |     |     | # Episodes |                  |     |     |         | # Episodes |         |     |     |
|     |                  |     |     | (a)3m      |                  |     |     |         | (b)5m      |         |     |     |
|     | 90               |     |     |            |                  |     | 70  |         |            |         |     |     |
80
60
|     | % niW egarevA |     |     |     |     |     | % niW egarevA |     |     |     |     |     |
| --- | ------------- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- |
70
50
60
|     | 50  |     |     |     |     |     | 40  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
40
30
|     | 30  |     |     |     |     |     | 20  |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
20
10
10
|     | 0   |     |     |            |         |     | 0   |        |             |         |     |     |
| --- | --- | --- | --- | ---------- | ------- | --- | --- | ------ | ----------- | ------- | --- | --- |
|     |     | 5k  | 10k | 15k 20k    | 25k 30k | 35k |     | 5k 10k | 15k 20k 25k | 30k 35k | 40k |     |
|     |     |     |     | # Episodes |         |     |     |        | # Episodes  |         |     |     |
|     |     |     |     | (c)5w      |         |     |     |        | (d)2d 3z    |         |     |     |
Figure3:WinratesforCOMAandcompetingalgorithmsonfourdifferentscenarios.COMAoutperformsallbaselinemethods.
Centralisedcriticsalsoclearlyoutperformtheirdecentralisedcounterparts.Thelegendatthetopappliesacrossallplots.
and shield.2 All features are normalised by their maxi- critics use extra output heads appended to the last layer of
mum values. We do not include any information about the the actor network. Action probabilities are produced from
units’currenttarget. the final layer, z, via a bounded softmax distribution that
The global state representation consists of similar fea- lower-bounds the probability of any given action by ϵ/|U|:
tures, but for all units on the map regardless of fields of P(u) = (1 − ϵ)softmax(z) + ϵ/|U|). We anneal ϵ lin-
u
view. Absolute distance is not included, and x-y locations earlyfrom0.5to0.02across750trainingepisodes.Thecen-
are given relative to the centre of the map rather than to tralisedcriticisafeedforwardnetworkwithmultipleReLU
a particular agent. The global state also includes health layerscombinedwithfullyconnectedlayers.Hyperparame-
points and cooldown for all agents. The representa- ters were coarsely tuned on the 5m scenario and then used
tion fed to the centralised Q-function critic is the concate- forallothermaps.Wefoundthatthemostsensitiveparam-
nation of the global state representation with the local ob- eterwasTD(λ),butsettledonλ = 0.8,whichworkedbest
forbothCOMAandourbaselines.Ourimplementationuses
| servation | of the agent | whose |     | actions are | being evaluated. |     |     |     |     |     |     |     |
| --------- | ------------ | ----- | --- | ----------- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
Our centralised critic that estimates V(s), and is therefore TorchCraft (Synnaeve et al. 2016) and Torch7 (Collobert,
agent-agnostic, receives the global state concatenated with Kavukcuoglu, and Farabet 2011). Pseudocode and further
all agents’ observations. The observations contain no new details on the training procedure are in the supplementary
| information | but include |     | the egocentric |     | distances relative | to  | material. |     |     |     |     |     |
| ----------- | ----------- | --- | -------------- | --- | ------------------ | --- | --------- | --- | --- | --- | --- | --- |
thatagent. We experimented with critic architectures that are fac-
| Architecture | &   | Training. | The | actor | consists of | 128-bit |     |     |     |     |     |     |
| ------------ | --- | --------- | --- | ----- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
toredattheagentlevelandfurtherexploitinternalparameter
| gated recurrent | units | (GRUs) |     | (Cho et | al. 2014) | that use |     |     |     |     |     |     |
| --------------- | ----- | ------ | --- | ------- | --------- | -------- | --- | --- | --- | --- | --- | --- |
sharing.However,wefoundthatthebottleneckforscalabil-
fullyconnectedlayersbothtoprocesstheinputandtopro-
itywasnotthecentralisationofthecritic,butratherthedif-
| duce the | output values | from | the | hidden | state, ha. | The IAC |         |                |              |        |     |               |
| -------- | ------------- | ---- | --- | ------ | ---------- | ------- | ------- | -------------- | ------------ | ------ | --- | ------------- |
|          |               |      |     |        | t          |         | ficulty | of multi-agent | exploration. | Hence, | we  | defer further |
investigationoffactoredCOMAcriticstofuturework.
| 2After | firing, a | unit’s cooldown |     | is reset, | and it | must drop |     |            |                     |             |     |             |
| ------ | --------- | --------------- | --- | --------- | ------ | --------- | --- | ---------- | ------------------- | ----------- | --- | ----------- |
|        |           |                 |     |           |        |           |     | Ablations. | We perform ablation | experiments |     | to validate |
beforefiringagain.Shieldsabsorbdamageuntiltheybreak,after
whichunitsstartlosinghealth.Dragoonsandzealotshaveshields threekeyelementsofCOMA.First,wetesttheimportance
butmarinesdonot. ofcentralisingthecriticbycomparingagainsttwoIACvari-

|     |     |     |     | Local | Field | of View | (FoV) |     |     | Full | FoV, | Central | Control |     |
| --- | --- | --- | --- | ----- | ----- | ------- | ----- | --- | --- | ---- | ---- | ------- | ------- | --- |
COMA
| map | heur. | IAC-V |     | IAC-Q |     | cnt-V | cnt-QV |     |     | heur. |     | DQN | GMEZO |     |
| --- | ----- | ----- | --- | ----- | --- | ----- | ------ | --- | --- | ----- | --- | --- | ----- | --- |
mean best
| 3m    | 35  | 47  | (3) | 56  | (6)  | 83 (3) | 83 (5) | 87 (3) | 98  | 74  |     | -   |     | -   |
| ----- | --- | --- | --- | --- | ---- | ------ | ------ | ------ | --- | --- | --- | --- | --- | --- |
| 5m    | 66  | 63  | (2) | 58  | (3)  | 67 (5) | 71 (9) | 81 (5) | 95  | 98  |     | 99  |     | 100 |
| 5w    | 70  | 18  | (5) | 57  | (5)  | 65 (3) | 76 (1) | 82 (3) | 98  | 82  |     | 70  |     | 743 |
| 2d 3z | 63  | 27  | (9) | 19  | (21) | 36 (6) | 39 (5) | 47 (5) | 65  | 68  |     | 61  |     | 90  |
Table1:Meanwinpercentageaveragedacrossfinal1000evaluationepisodesforthedifferentmaps,forallmethodsandthe
hand-codedheuristicinthedecentralisedsettingwithalimitedfieldofview.Thehighestmeanperformancesareinbold,while
valuesinparenthesesdenotethe95%confidenceinterval,forexample87(3)=87±3.Alsoshown,maximumwinpercentages
forCOMA(decentralised),incomparisontotheheuristicandpublishedresults(evaluatedinthecentralisedsetting).
| ants,IAC-QandIAC-V.Thesecriticstakethesamedecen- |     |     |     |     |     |     | policies. |     |     |     |     |     |     |     |
| ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
tralisedinputastheactor,andshareparameterswiththeac- Learningastate-valuefunctionhastheobviousadvantage
tor network up to the final layer. IAC-Q then outputs |U| of not conditioning on the joint action. Still, we find that
Q-values, one for each action, while IAC-V outputs a sin- COMA outperforms the central-V baseline in final perfor-
glestate-value.Notethatwestillshareparametersbetween mance. Furthermore, COMA typically achieves good poli-
agents,usingtheegocentricobservationsandID’saspartof cies faster, which is expected as COMA provides a shaped
theinputtoallowdifferentbehaviourstoemerge.Thecoop- trainingsignal.Trainingisalsomorestablethancentral-V,
erativerewardfunctionisstillsharedbyallagents. which is a consequence of the COMA gradient tending to
Second,wetestthesignificanceoflearningQinsteadof zero as the policy becomes greedy. Overall, COMA is the
| V.         | central-V |     |       |        |         |           | bestperformingandmostconsistentmethod. |     |     |     |     |     |     |     |
| ---------- | --------- | --- | ----- | ------ | ------- | --------- | -------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| The method |           |     | still | uses a | central | state for | the                                    |     |     |     |     |     |     |     |
critic,butlearnsV(s),andusestheTDerrortoestimatethe Usunieretal.(2016)reporttheperformanceoftheirbest
advantageforpolicygradientupdates. agents trained with their state-of-the-art centralised con-
Third, we test the utility of our counterfactual baseline. troller labelled GMEZO (greedy-MDP with episodic zero-
The method central-QV learns both Q and V simultane- order optimisation), and for a centralised DQN controller,
|           |           |     |           |     |     |              | both | given a | full field | of view | and | access | to attack-move |     |
| --------- | --------- | --- | --------- | --- | --- | ------------ | ---- | ------- | ---------- | ------- | --- | ------ | -------------- | --- |
| ously and | estimates | the | advantage | as  | Q − | V, replacing |      |         |            |         |     |        |                |     |
COMA’s counterfactual baseline with V. All methods use macro-actions.TheseresultsarecomparedinTable1against
thesamearchitectureandtrainingschemefortheactors,and the best agents trained with COMA for each map. Clearly,
allcriticsaretrainedwithTD(λ). inmostsettingstheseagentsachieveperformancecompara-
bletothebestpublishedwinratesdespitebeingrestrictedto
decentralisedpoliciesandlocalfieldsofview.
|     |     | 6   | Results |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure3showsaveragewinratesasafunctionofepisodefor 7 Conclusions&FutureWork
eachmethodandeachStarCraftscenario.Foreachmethod,
|                  |     |             |             |     |             |          | This       | paper presented |     | COMA              | policy   | gradients, |          | a method  |
| ---------------- | --- | ----------- | ----------- | --- | ----------- | -------- | ---------- | --------------- | --- | ----------------- | -------- | ---------- | -------- | --------- |
| we conducted     | 35  | independent | trials      | and | froze       | learning | ev-        |                 |     |                   |          |            |          |           |
|                  |     |             |             |     |             |          | that uses  | a centralised   |     | critic            | in order | to         | estimate | a coun-   |
| ery 100 training |     | episodes    | to evaluate |     | the learned | policies |            |                 |     |                   |          |            |          |           |
|                  |     |             |             |     |             |          | terfactual | advantage       |     | for decentralised |          | policies   |          | in mutli- |
across200episodespermethod,plottingtheaverageacross
|     |     |     |     |     |     |     | agent | RL. COMA | addresses |     | the challenges |     | of multi-agent |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | -------- | --------- | --- | -------------- | --- | -------------- | --- |
episodesandtrials.Alsoshownisonestandarddeviationin
|     |     |     |     |     |     |     | credit | assignment | by  | using | a counterfactual |     | baseline | that |
| --- | --- | --- | --- | --- | --- | --- | ------ | ---------- | --- | ----- | ---------------- | --- | -------- | ---- |
performance.
|     |     |     |     |     |     |     | marginalises |     | out a | single agent’s |     | action, | while | keeping |
| --- | --- | --- | --- | --- | --- | --- | ------------ | --- | ----- | -------------- | --- | ------- | ----- | ------- |
TheresultsshowthatCOMAissuperiortotheIACbase-
|              |            |                |     |     |     |         | the other | agents’   | actions | fixed.          | Our | results | in        | a decen- |
| ------------ | ---------- | -------------- | --- | --- | --- | ------- | --------- | --------- | ------- | --------------- | --- | ------- | --------- | -------- |
| lines in all | scenarios. | Interestingly, |     | the | IAC | methods | also      |           |         |                 |     |         |           |          |
|              |            |                |     |     |     |         | tralised  | StarCraft | unit    | micromanagement |     |         | benchmark | show     |
eventually learn reasonable policies in 5m, although they that COMA significantly improves final performance and
| need substantially |       | more episodes |         | to do    | so. This | may seem  |             |         |                  |                   |                  |              |             |         |
| ------------------ | ----- | ------------- | ------- | -------- | -------- | --------- | ----------- | ------- | ---------------- | ----------------- | ---------------- | ------------ | ----------- | ------- |
|                    |       |               |         |          |          |           | training    | speed   | over             | other multi-agent |                  | actor-critic |             | methods |
| counterintuitive   | since | in            | the IAC | methods, |          | the actor | and         |         |                  |                   |                  |              |             |         |
|                    |       |               |         |          |          |           | and         | remains | competitive      | with              | state-of-the-art |              | centralised |         |
| critic networks    | share | parameters    |         | in their | early    | layers    | (see        |         |                  |                   |                  |              |             |         |
|                    |       |               |         |          |          |           | controllers | under   | best-performance |                   |                  | reporting.   | Future      | work    |
Section5),whichcouldbeexpectedtospeedlearning.How-
|     |     |     |     |     |     |     | will extend | COMA | to  | tackle | scenarios | with | large | numbers |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---- | --- | ------ | --------- | ---- | ----- | ------- |
ever,theseresultssuggestthattheimprovedaccuracyofpol- ofagents,wherecentralisedcriticsaremoredifficulttotrain
icyevaluationmadepossiblebyconditioningontheglobal
|     |     |     |     |     |     |     | andexplorationisharder |     |     | tocoordinate.Wealsoaimto |     |     |     | de- |
| --- | --- | --- | --- | --- | --- | --- | ---------------------- | --- | --- | ------------------------ | --- | --- | --- | --- |
stateoutweighstheoverheadoftrainingaseparatenetwork.
|     |     |     |     |     |     |     | velop | more sample-efficient |     |     | variants | that | are practical | for |
| --- | --- | --- | --- | --- | --- | --- | ----- | --------------------- | --- | --- | -------- | ---- | ------------- | --- |
Furthermore,COMAstrictlydominatescentral-QV,both
real-worldapplicationssuchasself-drivingcars.
intrainingspeedandinfinalperformanceacrossallsettings.
Thisisastrongindicatorthatourcounterfactualbaselineis 35wDQNandGMEZObenchmarkperformancesareofapol-
crucial when using a central Q-critic to train decentralised icytrainedonalargermapandtestedon5w

Acknowledgements Das, A.; Kottur, S.; Moura, J. M.; Lee, S.; and Batra, D.
|                |     |          |         |              |          |          |       | 2017. Learning         |     | cooperative |                                | visual dialog | agents | with | deep |
| -------------- | --- | -------- | ------- | ------------ | -------- | -------- | ----- | ---------------------- | --- | ----------- | ------------------------------ | ------------- | ------ | ---- | ---- |
| This project   | has | received | funding |              | from the | European | Re-   |                        |     |             |                                |               |        |      |      |
|                |     |          |         |              |          |          |       | reinforcementlearning. |     |             | arXivpreprintarXiv:1703.06585. |               |        |      |      |
| search Council |     | (ERC)    | under   | the European |          | Union’s  | Hori- |                        |     |             |                                |               |        |      |      |
zon2020researchandinnovationprogramme(grantagree- Foerster,J.;Assael,Y.M.;deFreitas,N.;andWhiteson,S.
mentnumber637713).ItwasalsosupportedbytheOxford- 2016. Learning to communicate with deep multi-agent re-
Google DeepMind Graduate Scholarship, the UK EPSRC inforcement learning. In Advances in Neural Information
CDTinAutonomousIntelligentMachinesandSystems,and ProcessingSystems,2137–2145.
agenerousgrantfromMicrosoftfortheirAzurecloudcom-
|     |     |     |     |     |     |     |     | Foerster, | J.; Nardelli, |     | N.; Farquhar, |     | G.; Torr, | P.; Kohli, | P.; |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | ------------- | --- | ------------- | --- | --------- | ---------- | --- |
puting services. We would like to thank Nando de Freitas, Whiteson,S.;etal. 2017. Stabilisingexperiencereplayfor
Yannis Assael, and Brendan Shillingford for helpful com- deepmulti-agentreinforcementlearning. InProceedingsof
| ments and | discussion. |     | We  | also thank | Gabriel | Synnaeve, |     |     |     |     |     |     |     |     |     |
| --------- | ----------- | --- | --- | ---------- | ------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The34thInternationalConferenceonMachineLearning.
| Zeming | Lin, and | the | rest of | the TorchCraft |     | team | at FAIR |     |     |     |     |     |     |     |     |
| ------ | -------- | --- | ------- | -------------- | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
Gupta,J.K.;Egorov,M.;andKochenderfer,M.2017.Coop-
fortheirworkontheinterface.
|     |     |     |     |     |     |     |     | erative multi-agent |     | control | using | deep | reinforcement |     | learn- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | --- | ------- | ----- | ---- | ------------- | --- | ------ |
ing.
Errata
|            |         |     |            |           |     |          |        | Hausknecht, | M., | and       | Stone,     | P. 2015. |       | Deep  | recurrent |
| ---------- | ------- | --- | ---------- | --------- | --- | -------- | ------ | ----------- | --- | --------- | ---------- | -------- | ----- | ----- | --------- |
| An earlier | version | of  | this paper | contained |     | an error | in the |             |     |           |            |          |       |       |           |
|            |         |     |            |           |     |          |        | q-learning  | for | partially | observable |          | mdps. | arXiv | preprint  |
proof of Lemma 1 because the critic depended on the state arXiv:1507.06527.
sbutnotthejointhistoryτ.Inthisversion,Equation4and
|     |     |     |     |     |     |     |     | Hochreiter,S.,andSchmidhuber,J. |     |     |     |     | 1997. Longshort-term |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | -------------------- | --- | --- |
Figure1havebeenupdatedtoaddthisdependence.Inaddi-
memory. Neuralcomputation9(8):1735–1780.
tion,theproofofLemma1hasbeenrevisedtoshowexplic-
itlyhowexistingpolicygradientresultsapplytothismodi- Jorge,E.;Ka˚geba¨ck,M.;andGustavsson,E.2016.Learning
toplayguesswho?andinventingagroundedlanguageasa
fiedsetting.TheproofalsoreferstotheSuttonetal.(1999)
result instead of that of Konda and Tsitsiklis (2000) as the consequence. arXivpreprintarXiv:1611.03218.
latter requires that the Markov chain induced by the policy Konda,V.R.,andTsitsiklis,J.N. 2000. Actor-criticalgo-
| be irreducible, |     | which | does not | hold | for history-based |     | state |         |             |     |           |             |     |            |      |
| --------------- | --- | ----- | -------- | ---- | ----------------- | --- | ----- | ------- | ----------- | --- | --------- | ----------- | --- | ---------- | ---- |
|                 |     |       |          |      |                   |     |       | rithms. | In Advances |     | in neural | information |     | processing | sys- |
representations.ThankstoFransOliehoekandChrisAmato
tems,1008–1014.
forpointingouttheseissues.ThanksalsotoFransOliehoek
|            |         |     |          |     |             |        |     | Kraemer,L.,andBanerjee,B. |     |     |     | 2016. | Multi-agentreinforce- |     |     |
| ---------- | ------- | --- | -------- | --- | ----------- | ------ | --- | ------------------------- | --- | --- | --- | ----- | --------------------- | --- | --- |
| and Andrea | Baisero | for | feedback | on  | the revised | proof. | See |                           |     |     |     |       |                       |     |     |
mentlearningasarehearsalfordecentralizedplanning.Neu-
alsoLyuetal.;Lyuetal.;Lyuetal.;Lyuetal.(2021;2022;
rocomputing190:82–94.
2023;2024)formoredetailsonthistopic.
|     |     |     |     |     |     |     |     | Lazaridou, | A.; | Peysakhovich, |     | A.; and | Baroni, | M.  | 2016. |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | --- | ------------- | --- | ------- | ------- | --- | ----- |
Multi-agentcooperationandtheemergenceof(natural)lan-
References
guage. arXivpreprintarXiv:1612.07182.
| Busoniu, | L.; Babuska, |     | R.; and | De  | Schutter, | B.  | 2008. A |           |               |     |     |          |              |     |         |
| -------- | ------------ | --- | ------- | --- | --------- | --- | ------- | --------- | ------------- | --- | --- | -------- | ------------ | --- | ------- |
|          |              |     |         |     |           |     |         | Leibo, J. | Z.; Zambaldi, |     | V.; | Lanctot, | M.; Marecki, |     | J.; and |
comprehensivesurveyofmultiagentreinforcementlearning.
|     |     |     |     |     |     |     |     | Graepel,T. | 2017. | Multi-agentreinforcementlearninginse- |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ----- | ------------------------------------- | --- | --- | --- | --- | --- |
IEEETransactionsonSystemsManandCyberneticsPartC
|     |     |     |     |     |     |     |     | quentialsocialdilemmas. |     |     | arXivpreprintarXiv:1702.03037. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------------- | --- | --- | ------------------------------ | --- | --- | --- | --- |
ApplicationsandReviews38(2):156.
|                                |          |              |           |     |             |             |     | Lowe, R.;               | Wu, | Y.; Tamar, |               | A.; Harb, | J.; Abbeel,  |       | P.; and  |
| ------------------------------ | -------- | ------------ | --------- | --- | ----------- | ----------- | --- | ----------------------- | --- | ---------- | ------------- | --------- | ------------ | ----- | -------- |
| Cao,Y.;Yu,W.;Ren,W.;andChen,G. |          |              |           |     | 2013.       | Anoverview  |     |                         |     |            |               |           |              |       |          |
|                                |          |              |           |     |             |             |     | Mordatch,               | I.  | 2017.      | Multi-agent   |           | actor-critic | for   | mixed    |
| of recent                      | progress | in           | the study | of  | distributed | multi-agent |     |                         |     |            |               |           |              |       |          |
|                                |          |              |           |     |             |             |     | cooperative-competitive |     |            | environments. |           |              | arXiv | preprint |
| coordination.                  | IEEE     | Transactions |           | on  | Industrial  | informatics |     |                         |     |            |               |           |              |       |          |
arXiv:1706.02275.
9(1):427–438.
|     |     |     |     |     |     |     |     | Lyu, X.; | Xiao, | Y.; Daley, | B.; | and Amato, | C.  | 2021. | Con- |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ---------- | --- | ---------- | --- | ----- | ---- |
Chang,Y.-H.;Ho,T.;andKaelbling,L.P.2003.Alllearning
|           |             |     |          |           |        |        |     | trasting               | centralized | and | decentralized    |     | critics | in multi-agent |     |
| --------- | ----------- | --- | -------- | --------- | ------ | ------ | --- | ---------------------- | ----------- | --- | ---------------- | --- | ------- | -------------- | --- |
| is local: | Multi-agent |     | learning | in global | reward | games. | In  |                        |             |     |                  |     |         |                |     |
|           |             |     |          |           |        |        |     | reinforcementlearning. |             |     | arXiv2102.04402. |     |         |                |     |
NIPS,807–814.
|          |     |               |     |               |     |         |      | Lyu, X.; | Baisero, | A.; | Xiao, | Y.; and | Amato, | C.  | 2022. A |
| -------- | --- | ------------- | --- | ------------- | --- | ------- | ---- | -------- | -------- | --- | ----- | ------- | ------ | --- | ------- |
| Cho, K.; | van | Merrie¨nboer, |     | B.; Bahdanau, |     | D.; and | Ben- |          |          |     |       |         |        |     |         |
gio, Y. 2014. On the properties of neural machine deeper understanding of state-based critics in multi-agent
|              |                 |     |     |             |     |       |          | reinforcement |     | learning. | In  | Proceedings | of  | the AAAI | con- |
| ------------ | --------------- | --- | --- | ----------- | --- | ----- | -------- | ------------- | --- | --------- | --- | ----------- | --- | -------- | ---- |
| translation: | Encoder-decoder |     |     | approaches. |     | arXiv | preprint |               |     |           |     |             |     |          |      |
ferenceonartificialintelligence,volume36,9396–9404.
arXiv:1409.1259.
|           |            |             |         |        |       |              |         | Lyu, X.; | Baisero,    | A.; | Xiao,   | Y.; Daley,     | B.; | and Amato,    | C.  |
| --------- | ---------- | ----------- | ------- | ------ | ----- | ------------ | ------- | -------- | ----------- | --- | ------- | -------------- | --- | ------------- | --- |
| Colby, M. | K.;        | Curran,     | W.; and | Tumer, | K.    | 2015.        | Approx- |          |             |     |         |                |     |               |     |
|           |            |             |         |        |       |              |         | 2023. On | centralized |     | critics | in multi-agent |     | reinforcement |     |
| imating   | difference | evaluations |         | with   | local | information. | In      |          |             |     |         |                |     |               |     |
learning.JournalofArtificialIntelligenceResearch77:295–
| Proceedings | of  | the 2015 | International |     | Conference |     | on Au- |     |     |     |     |     |     |     |     |
| ----------- | --- | -------- | ------------- | --- | ---------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
354.
| tonomous | Agents | and | Multiagent | Systems, |     | 1659–1660. | In- |     |     |     |     |     |     |     |     |
| -------- | ------ | --- | ---------- | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ternationalFoundationforAutonomousAgentsandMultia- Lyu, X.; Baisero, A.; Xiao, Y.; Daley, B.; and Amato, C.
gentSystems. 2024. On centralized critics in multi-agent reinforcement
Collobert, R.; Kavukcuoglu, K.; and Farabet, C. 2011. learning. arXiv2408.14597.
Torch7:Amatlab-likeenvironmentformachinelearning. In Mnih, V.; Kavukcuoglu, K.; Silver, D.; Rusu, A. A.; Ve-
BigLearn,NIPSWorkshop. ness, J.; Bellemare, M. G.; Graves, A.; Riedmiller, M.;

Fidjeland, A. K.; Ostrovski, G.; et al. 2015. Human- Weaver,L.,andTao,N. 2001. Theoptimalrewardbaseline
level control through deep reinforcement learning. Nature for gradient-based reinforcement learning. In Proceedings
518(7540):529–533. oftheSeventeenthconferenceonUncertaintyinartificialin-
Mordatch,I.,andAbbeel,P. 2017. Emergenceofgrounded telligence,538–545. MorganKaufmannPublishersInc.
compositional language in multi-agent populations. arXiv Weyns, D.; Helleboogh, A.; and Holvoet, T. 2005. The
preprintarXiv:1703.04908. packet-world: A test bed for investigating situated multi-
|                                          |             |     |         |           |     |               |     | agentsystems.                     | InSoftwareAgent-BasedApplications,Plat- |     |          |
| ---------------------------------------- | ----------- | --- | ------- | --------- | --- | ------------- | --- | --------------------------------- | --------------------------------------- | --- | -------- |
| Oliehoek,F.A.;Spaan,M.T.J.;andVlassis,N. |             |     |         |           |     | 2008.         | Op- |                                   |                                         |     |          |
|                                          |             |     |         |           |     |               |     | formsandDevelopmentKits.Springer. |                                         |     | 383–408. |
| timal and                                | approximate |     | Q-value | functions | for | decentralized |     |                                   |                                         |     |          |
POMDPs. 32:289–353. Williams,R.J. 1992. Simplestatisticalgradient-following
|     |     |     |     |     |     |     |     | algorithms | for connectionist | reinforcement | learning. Ma- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | ----------------- | ------------- | ------------- |
Omidshafiei,S.;Pazis,J.;Amato,C.;How,J.P.;andVian,
chinelearning8(3-4):229–256.
J. 2017. Deepdecentralizedmulti-taskmulti-agentrlunder
partialobservability. arXivpreprintarXiv:1703.06182. Wolpert,D.H.,andTumer,K. 2002. Optimalpayofffunc-
|            |       |                                       |           |     |       |           |     | tionsformembersofcollectives.             |     | InModelingcomplexityin |          |
| ---------- | ----- | ------------------------------------- | --------- | --- | ----- | --------- | --- | ----------------------------------------- | --- | ---------------------- | -------- |
| Peng, P.;  | Yuan, | Q.; Wen,                              | Y.; Yang, | Y.; | Tang, | Z.; Long, | H.; |                                           |     |                        |          |
|            |       |                                       |           |     |       |           |     | economicandsocialsystems.WorldScientific. |     |                        | 355–369. |
| andWang,J. | 2017. | Multiagentbidirectionally-coordinated |           |     |       |           |     |                                           |     |                        |          |
nets for learning to play starcraft combat games. arXiv Yang,E.,andGu,D. 2004. Multiagentreinforcementlearn-
|     |     |     |     |     |     |     |     | ing for multi-robot | systems: | A survey. | Technical report, |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------- | -------- | --------- | ----------------- |
preprintarXiv:1703.10069.
tech.rep.
| Proper, | S., and | Tumer, | K. 2012. | Modeling |     | difference | re- |     |     |     |     |
| ------- | ------- | ------ | -------- | -------- | --- | ---------- | --- | --- | --- | --- | --- |
Ye,D.;Zhang,M.;andYang,Y.2015.Amulti-agentframe-
| wards for | multiagent | learning. |     | In Proceedings |     | of the | 11th |     |     |     |     |
| --------- | ---------- | --------- | --- | -------------- | --- | ------ | ---- | --- | --- | --- | --- |
workforpacketroutinginwirelesssensornetworks.sensors
InternationalConferenceonAutonomousAgentsandMulti-
agentSystems-Volume3,1397–1398. InternationalFounda- 15(5):10026–10047.
tionforAutonomousAgentsandMultiagentSystems. Ying, W., and Dayong, S. 2005. Multi-agent framework
ExpertSystemswith
Schulman, J.; Moritz, P.; Levine, S.; Jordan, M. I.; and forthirdpartylogisticsine-commerce.
Abbeel,P.2015.High-dimensionalcontinuouscontrolusing Applications29(2):431–436.
| generalizedadvantageestimation. |     |                 |     | CoRRabs/1506.02438. |                |         |     |     |     |     |     |
| ------------------------------- | --- | --------------- | --- | ------------------- | -------------- | ------- | --- | --- | --- | --- | --- |
| Shoham,Y.,andLeyton-Brown,K.    |     |                 |     | 2009.               | MultiagentSys- |         |     |     |     |     |     |
| tems: Algorithmic,              |     | Game-Theoretic, |     |                     | and Logical    | Founda- |     |     |     |     |     |
tions.
NewYork:CambridgeUniversityPress.
| Sukhbaatar, | S.; | Fergus, | R.; et | al. 2016. | Learning |     | multia- |     |     |     |     |
| ----------- | --- | ------- | ------ | --------- | -------- | --- | ------- | --- | --- | --- | --- |
InAdvancesin
gentcommunicationwithbackpropagation.
NeuralInformationProcessingSystems,2244–2252.
Sutton,R.S.;McAllester,D.A.;Singh,S.P.;Mansour,Y.;
| et al. 1999.                       |     | Policy gradient |     | methods | for              | reinforcement |     |     |     |     |     |
| ---------------------------------- | --- | --------------- | --- | ------- | ---------------- | ------------- | --- | --- | --- | --- | --- |
| learningwithfunctionapproximation. |     |                 |     |         | InNIPS,volume99, |               |     |     |     |     |     |
1057–1063.
| Sutton,              | R. S. 1988. | Learning                       |         | to predict | by       | the methods | of    |     |     |     |     |
| -------------------- | ----------- | ------------------------------ | ------- | ---------- | -------- | ----------- | ----- | --- | --- | --- | --- |
| temporaldifferences. |             | Machinelearning3(1):9–44.      |         |            |          |             |       |     |     |     |     |
| Synnaeve,            | G.;         | Nardelli,                      | N.;     | Auvolat,   | A.;      | Chintala,   | S.;   |     |     |     |     |
| Lacroix,             | T.; Lin,    | Z.; Richoux,                   |         | F.; and    | Usunier, | N.          | 2016. |     |     |     |     |
| Torchcraft:          | a library   | for                            | machine | learning   | research | on          | real- |     |     |     |     |
| timestrategygames.   |             | arXivpreprintarXiv:1611.00625. |         |            |          |             |       |     |     |     |     |
Tampuu,A.;Matiisen,T.;Kodelja,D.;Kuzovkin,I.;Korjus,
| K.;Aru,J.;Aru,J.;andVicente,R. |                 |     |      | 2015.              | Multiagentcoop- |           |     |     |     |     |     |
| ------------------------------ | --------------- | --- | ---- | ------------------ | --------------- | --------- | --- | --- | --- | --- | --- |
| eration                        | and competition |     | with | deep reinforcement |                 | learning. |     |     |     |     |     |
arXivpreprintarXiv:1511.08779.
| Tan, M.                      | 1993. | Multi-agent | reinforcement |                         |     | learning: | Inde- |     |     |     |     |
| ---------------------------- | ----- | ----------- | ------------- | ----------------------- | --- | --------- | ----- | --- | --- | --- | --- |
| pendentvs.cooperativeagents. |       |             |               | InProceedingsofthetenth |     |           |       |     |     |     |     |
internationalconferenceonmachinelearning,330–337.
| Tumer,K.,andAgogino,A.    |     |     | 2007.                       | Distributedagent-based |     |     |     |     |     |     |     |
| ------------------------- | --- | --- | --------------------------- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
| airtrafficflowmanagement. |     |     | InProceedingsofthe6thinter- |                        |     |     |     |     |     |     |     |
nationaljointconferenceonAutonomousagentsandmulti-
| agentsystems,255. |               | ACM. |          |         |           |     |       |     |     |     |     |
| ----------------- | ------------- | ---- | -------- | ------- | --------- | --- | ----- | --- | --- | --- | --- |
| Usunier,          | N.; Synnaeve, |      | G.; Lin, | Z.; and | Chintala, | S.  | 2016. |     |     |     |     |
Episodicexplorationfordeepdeterministicpolicies:Anap-
plicationtostarcraftmicromanagementtasks.arXivpreprint
arXiv:1609.02993.

|     |     |     |     |     |     | A   | ProofofLemma1 |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
TheCOMAgradientisgivenby
|     |     |     |     |     |     | (cid:34) |     |     |     |     | (cid:35) |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- | --- |
(cid:88)
|     |     |     |     |     | g =E |     | ∇ logπa(ua|τa)Aa(s,τ,u) |     |     |     | ,   |     |     | (7) |
| --- | --- | --- | --- | --- | ---- | --- | ----------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |      | π   | θ                       |     |     |     |     |     |     |     |
a
|     |     |     |     |     | Aa(s,τ,u)=Q(s,τ,u)−b(s,τ,u−a), |     |     |     |     |     |     |     |     | (8) |
| --- | --- | --- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
whereθaretheparametersofallactorpolicies,e.g.,θ ={θ1,...,θ|A|},andb(s,τ,u−a)isthecounterfactualbaselinedefined
inequation4.
Firstconsidertheexpectedcontributionofthebaseline:
|     |     |      |          |                  | (cid:18) |              |                          |            |                     |     | (cid:19)               |          |          |      |
| --- | --- | ---- | -------- | ---------------- | -------- | ------------ | ------------------------ | ---------- | ------------------- | --- | ---------------------- | -------- | -------- | ---- |
|     |     |      | (cid:88) | (cid:88)         |          | (cid:88)     |                          |            |                     |     |                        |          |          |      |
|     |     | g =− | p(s,τ)   |                  | π(u|τ)   |              | ∇ logπa(ua|τa)b(s,τ,u−a) |            |                     |     | ,                      |          |          | (9)  |
|     |     | b    |          |                  |          |              | θ                        |            |                     |     |                        |          |          |      |
|     |     |      | s,τ      |                  | u        | a            |                          |            |                     |     |                        |          |          |      |
|     |     |      |          |                  | (cid:18) |              |                          |            |                     |     |                        |          | (cid:19) |      |
|     |     |      | (cid:88) | (cid:88)(cid:88) |          |              |                          | (cid:88)   |                     |     |                        |          |          |      |
|     |     | =−   | p(s,τ)   |                  |          | π−a(u−a|τ−a) |                          | πa(ua|τa)∇ |                     |     | logπa(ua|τa)b(s,τ,u−a) |          | ,        |      |
|     |     |      |          |                  |          |              |                          |            |                     | θ   |                        |          |          | (10) |
|     |     |      | s,τ      |                  | a u−a    |              |                          | ua         |                     |     |                        |          |          |      |
|     |     |      |          |                  | (cid:18) |              |                          |            |                     |     |                        | (cid:19) |          |      |
|     |     |      | (cid:88) | (cid:88)(cid:88) |          |              |                          | (cid:88)   |                     |     |                        |          |          |      |
|     |     | =−   | p(s,τ)   |                  |          | π−a(u−a|τ−a) |                          | ∇          | πa(ua|τa)b(s,τ,u−a) |     |                        | ,        |          | (11) |
θ
|     |     |     | s,τ      |                  | a u−a    |                         |     | ua  |     |          |     |     |     |      |
| --- | --- | --- | -------- | ---------------- | -------- | ----------------------- | --- | --- | --- | -------- | --- | --- | --- | ---- |
|     |     |     |          |                  | (cid:18) |                         |     |     |     | (cid:19) |     |     |     |      |
|     |     |     | (cid:88) | (cid:88)(cid:88) |          |                         |     |     |     |          |     |     |     |      |
|     |     | =−  | p(s,τ)   |                  |          | π−a(u−a|τ−a)b(s,τ,u−a)∇ |     |     |     | 1        | ,   |     |     | (12) |
θ
|     |     |     | s,τ |     | a u−a |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
=0,
(13)
where τ−a is the joint action-observation history of all agents except a, and π−a is the joint policy of all agents except a.
Clearly,theper-agentbaseline,althoughitmayreducevariance,doesnotchangetheexpectedgradient,andthereforedoesnot
affecttheconvergenceofCOMA.Thekeyfeatureofthecounterfactualbaselinewhichallowsthispropertyistheindependence
foragentaontheactionua.
Theremainderoftheexpectedpolicygradientisgivenby:
|     |     |     |     |     |     | (cid:34) |     |     |     |     | (cid:35) |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- | --- |
(cid:88)
|     |     |     |     |     | g =E |     | ∇ logπa(ua|τa)Q(s,τ,u) |     |     |     |     |     |     | (14) |
| --- | --- | --- | --- | --- | ---- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | ---- |
|     |     |     |     |     |      | π   | θ                      |     |     |     |     |     |     |      |
a
|     |     |     |     |     |     | (cid:34) |          |                   |     |     | (cid:35) |     |     |      |
| --- | --- | --- | --- | --- | --- | -------- | -------- | ----------------- | --- | --- | -------- | --- | --- | ---- |
|     |     |     |     |     | =E  |          | (cid:89) |                   |     |     |          |     |     |      |
|     |     |     |     |     |     | ∇        | log      | πa(ua|τa)Q(s,τ,u) |     |     | .        |     |     | (15) |
|     |     |     |     |     |     | π        | θ        |                   |     |     |          |     |     |      |
a
Bywritingthejointpolicyastheproductoftheindependentactors,
(cid:89)
|     |     |     |     |     |     | π(u|τ)= |     | πa(ua|τa), |     |     |     |     |     | (16) |
| --- | --- | --- | --- | --- | --- | ------- | --- | ---------- | --- | --- | --- | --- | --- | ---- |
a
wecanrewrite(15)as:
=E
|     |     |     |     |     | g   | π   | [∇ θ logπ(u|τ)Q(s,τ,u)]. |     |     |     |     |     |     | (17) |
| --- | --- | --- | --- | --- | --- | --- | ------------------------ | --- | --- | --- | --- | --- | --- | ---- |
Furthermore,wecanreinterpretπasasingle-agentpolicyinacorrespondingMDPM =⟨S ,U ,P ,r ,γ⟩where,
|     |     |     |     |     |     |     |     |     |     |     |     | m m m | m   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
• S =S×T;
m
• U =U;
m
(s′ P(s′,τ′|s,τ) P(s′|s)1 (z′,z), τ′ z′, [O(s′,1),...,O(s′,n)],
| • P | m |s | m ) = |     | =   |     | =   | where |     | is τ extended |     | with | z = |     | and |
| --- | ---- | ----- | --- | --- | --- | --- | ----- | --- | ------------- | --- | ---- | --- | --- | --- |
1 m
|     | (z′,z)=1iffz′ |     | =z;and |     |     |     |     |     |     |     |     |     |     |     |
| --- | ------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
=
• r ((s,τ),u)=r(s,u).
m
ThegradientginthestochasticgameGcorrespondstothestandardpolicygradientgradientinM:
|     |     |     |     |     | g =E |     | [∇ logπ | (u  | |s )Q(s | ,u  | )], |     |     | (18) |
| --- | --- | --- | --- | --- | ---- | --- | ------- | --- | ------- | --- | --- | --- | --- | ---- |
|     |     |     |     |     | m    | πm  | θ       | m m | m       | m   | m   |     |     |      |
where π (u |s ) = π (u |s,τ) = π(u|τ), i.e., π follows the policy in (16), foregoing the option of depending on s.
|     | m   | m m | m m |     |     |     | m   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Suttonetal.(1999)provethatanactor-criticfollowingthisgradientconvergestoalocalmaximumoftheexpectedreturn,given
severalassumptions,including:

1. theMDPhasboundedrewards;
2. thepolicyisdifferentiable;
3. thecriticistrainedagainstunbiasedtargets,asinTD(1);
4. thecritichasconvergedtoalocaloptimumbeforeeachpolicygradientisestimated;and
5. thecriticusesarepresentationcompatiblewiththepolicy.
Thepolicyparameterisation(i.e.,thesingle-agentjoint-actionlearnerisdecomposedintoindependentactors)isimmaterialto
convergence,aslongasitremainsdifferentiable.
|     |     | B TrainingDetailsandHyperparameters |     |     |
| --- | --- | ----------------------------------- | --- | --- |
Trainingisperformedinbatchmode,withabatchsizeof30.Duetoparametersharing,allagentscanbeprocessedinparallel,
witheachagentforeachepisodeandtimestepoccupyingonebatchentry.Thetrainingcycleprogressesinthreesteps(com-
pletionofallthreestepsconstitutesasoneepisodeinourgraphs):1)collectdata:collect 30 episodes;2)traincritic:foreach
n
timestep,applyagradientsteptothefeed-forwardcritic,startingattheendoftheepisode;and3)trainactor:fullyunrollthe
recurrentpartoftheactor,aggregategradientsinthebackwardpassacrossalltimesteps,andapplyagradientupdate.
We use a target network for the critic, which updates every 150 training steps for the feed-forward centralised critics and
every50stepsfortherecurrentIACcritics.Thefeed-forwardcriticreceivesmorelearningsteps,sinceitperformsaparameter
updateforeachtimestep.BoththeactorandthecriticnetworksaretrainedusingRMS-propwithlearningrate0.0005andalpha
0.99,withoutweightdecay.Wesetgammato0.99forallmaps.
Althoughtuningtheskip-frameinStarCraftcanimproveabsoluteperformance(Pengetal.2017),weuseadefaultvalueof
7,sincethemainfocusisarelativeevaluationbetweenCOMAandthebaselines.
C Algorithm
Algorithm1CounterfactualMulti-Agent(COMA)PolicyGradients
Initialiseθc,θˆc,θπ
1 1
foreachtrainingepisodeedo
Emptybuffer
| fore =1to BatchSize | do  |     |     |     |
| ------------------- | --- | --- | --- | --- |
c n
| s =initialstate,t=0,ha  |     | =0foreachagenta |     |     |
| ----------------------- | --- | --------------- | --- | --- |
| 1                       |     | 0               |     |     |
| whiles ̸=terminalandt<T |     | do              |     |     |
t
t=t+1
foreachagentado
|           | (cid:0) |            | (cid:1) |     |
| --------- | ------- | ---------- | ------- | --- |
| ha =Actor | oa,ha   | ,ua ,a,u;θ |         |     |
| t         | t       | t−1 t−1    | i       |     |
Sampleuafromπ(ha,ϵ(e))
t t
| Getrewardr | andnextstates |     |     |     |
| ---------- | ------------- | --- | --- | --- |
|            | t             | t+1 |     |     |
Addepisodetobuffer
Collateepisodesinbufferintosinglebatch
fort=1toT do//fromnowprocessingallagentsinparallelviasinglebatch
BatchunrollRNNusingstates,actionsandrewards
CalculateTD(λ)targetsyausingθˆc
|     |     | t i |     |     |
| --- | --- | --- | --- | --- |
fort=T downto1do
(cid:0) (cid:1)
| ∆Qa =ya−Q | sa,u |     |     |     |
| --------- | ---- | --- | --- | --- |
| t t       | j    |     |     |     |
∆θc =∇ (∆Qa)2//calculatecriticgradient
| θc  | t   |     |     |     |
| --- | --- | --- | --- | --- |
θc =θc−α∆θc//updatecriticweights
i+1 i
EveryCstepsresetθˆc
=θc
i i
fort=T downto1do
| Aa(sa,u)=Q(sa,u)− |                                              | (cid:80) Q(sa,u,u−a)π(u|ha)//calculateCOMA |     |     |
| ----------------- | -------------------------------------------- | ------------------------------------------ | --- | --- |
| t                 | t                                            | u t                                        |     | t   |
| ∆θπ =∆θπ+∇        | logπ(u|ha)Aa(sa,u)//accumulateactorgradients |                                            |     |     |
|                   | θπ                                           | t                                          | t   |     |
θπ =θπ+α∆θπ
//updateactorweights
i+1 i