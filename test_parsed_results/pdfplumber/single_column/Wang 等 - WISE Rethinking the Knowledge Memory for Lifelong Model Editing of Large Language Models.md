# Wang 等 - WISE Rethinking the Knowledge Memory for Lifelong Model Editing of Large Language Models

WISE: Rethinking the Knowledge Memory for
Lifelong Model Editing of Large Language Models
PengWang1∗ ZexiLi1∗ NingyuZhang1† ZiwenXu1 YunzhiYao1
YongJiang2 PengjunXie2 FeiHuang2 HuajunChen1,3†
1ZhejiangUniversity 2AlibabaGroup
3ZhejiangKeyLaboratoryofBigDataIntelligentComputing
{peng2001,zexi.li,zhangningyu}@zju.edu.cn
Abstract
Largelanguagemodels(LLMs)needknowledgeupdatestomeettheever-growing
world facts and correct the hallucinated responses, facilitating the methods of
lifelong model editing. Where the updated knowledge resides in memories is
a fundamental question for model editing. In this paper, we find that editing
either long-term memory (direct model parameters) or working memory (non-
parametricknowledgeofneuralnetworkactivations/representationsbyretrieval)
willresultinanimpossibletriangle—reliability,generalization,andlocalitycannot
berealizedtogetherinthelifelongeditingsettings. Forlong-termmemory,directly
editingtheparameterswillcauseconflictswithirrelevantpretrainedknowledgeor
previousedits(poorreliabilityandlocality). Forworkingmemory,retrieval-based
activationscanhardlymakethemodelunderstandtheeditsandgeneralize(poor
generalization). Therefore,weproposeWISEtobridgethegapbetweenmemories.
In WISE, we design a dual parametric memory scheme, which consists of the
main memory for the pretrained knowledge and a side memory for the edited
knowledge. Weonlyedittheknowledgeinthesidememoryandtrainarouterto
decidewhichmemorytogothroughwhengivenaquery. Forcontinualediting,
wedeviseaknowledge-shardingmechanismwheredifferentsetsofeditsresidein
distinctsubspacesofparametersandaresubsequentlymergedintoasharedmemory
withoutconflicts. ExtensiveexperimentsshowthatWISEcanoutperformprevious
modeleditingmethodsandovercometheimpossibletriangleunderlifelongmodel
editingofquestionanswering,hallucination,andout-of-distributionsettingsacross
trendingLLMarchitectures,e.g.,GPT,LLaMA,andMistral‡.
1 Introduction
Largelanguagemodels(LLMs)showemergentintelligencewhenscalingthenumberofparameters
and data [1–4], which reveals the sparks of artificial general intelligence [5]. However, when
deployed,LLMsstillmakemistakes[6],generatingresponseswithhallucinations[7],bias[8],and
factual decays [9]. On the other hand, the world’s knowledge is ever-growing, so the up-to-date
knowledgeisusuallydifferentfromtheoneduringLLMs’pretraining[10]. Manysucherrorsand
emergingfactswillarisesequentiallyindeployment,someofwhichhavetobeaddressedtimelyand
efficientlywithoutwaitingforretrainingorfinetuning[11,12]. Also,retrainingorfinetuningisoften
toocomputationallyexpensive[13,10],whichisnotsustainableforlifelonggrowingknowledge.
Therefore,lifelongmodelediting[10]wasproposedtoremedythecontinualknowledgeupdatesand
injectionsforLLMsinacheapandtimelymanner.
∗ Equalcontribution.
† CorrespondingAuthor.
‡Codeisavailableathttps://github.com/zjunlp/EasyEdit.
38thConferenceonNeuralInformationProcessingSystems(NeurIPS2024).
Aneffectivelifelongmodeleditingapproachshouldsatisfythefollowingproperties[14,15,11,16,
17]: i)reliability,themodelcanrememberbothcurrentandpreviouseditsaftersequentialediting;
ii)locality,modeleditingwillnotinfluenceinherentpretrainedknowledgewhichisirrelevanttothe
editedknowledge;iii)generalization,themodelisnotjustmerelymemorizingthequery-targetpairs;
instead,itshouldunderstandandgeneralizewhengiven
otherformsofquerieswiththesameknowledge. Wecom-
Continual Editing T=100 WISE (Our Method)
pareexistingmodeleditingandcontinuallearningmeth- Reliability FT-EWC
odsonthethreemetricsinFigure1andfindthatitseemsto DEFER
GRACE
beanimpossibletriangle—reliability,generalization,and ROME
localitycannotberealizedatthesametimeinthecontin- 1.0 0.8
0.6
ualeditingsettings. Wefindthatwheretheupdatedknowl- 0.4
0.2
edgeresidesinmemoriesaffectseditingperformances,and
previous methods can be generally divided into editing
eitherlong-termmemory,e.g.,ROME[18],MEMIT[19],
Locality
andFT-EWC(FinetuningwithElasticWeightConsolida- Generalization
tion[20],acontinuallearningmethod),orworkingmem-
ory, e.g., GRACE [10]. Note that the categorization of
Figure 1: Metric triangle among re-
long-termandworkingmemoriesisderivedfromhuman
liability, generalization, and locality.
recognition[21,22]andneuroscience[23]whichhasre-
ZsREdataset,numberofcontinualedits
centlybeenadoptedinthestudyofLLMs[24–27]. Model
T = 100,LLaMA-2-7B.Editingmeth-
editingoflong-termmemoryreferstodirectlyeditingthe
odsbasedonlong-termmemory(ROME
modelparameters,whichcontaingeneralizableparametric
and FT-EWC) and working memory
knowledge[28,24]. However,editinglong-termmemory
(DEFERandGRACE)showtheimpos-
willcauseconflictswithpreviouspretrainedknowledge,
sibletriangleinmetrics,whileourWISE
resulting in poor locality (e.g., ROME and FT-EWC in
isleadinginallthreemetrics.
Figure1). Workingmemoryreferstothenon-parametric
knowledge of neural network activations/representations by retrieval, and it does not change the
networkparameters[24];instead,itreplacestherepresentationsbyretrievalatworking(inference)
time,likeGRACE.GRACE’sworkingmemoryshowspromisingresultsinreliabilityandlocality,but
inourexperiments,itshowspoorgeneralizationsinceretrieval-basedrepresentationscanhardlymake
themodelunderstandtheeditsandgeneralizetodifferentqueries. Itrevealsthatlong-termmemory
andworkingmemorybothhavedrawbacksforlifelongmodelediting,thoughthereweresomespecial
memorydesignsforLLMarchitectures,likeMemorryLLM[28],SPALM[27],andMemoria[25],
theychangethearchitecturesandcannotbedirectlyappliedfordifferentLLMs. Intuitively,there
isagapbetweeneditingworkingandlong-termmemories,thus,inthispaper,westudy:
Whatisthebettermemorymechanismforlifelongmodeleditingtobreaktheimpossibletriangle?
Humanbrainscontaintheleftandrighthemispheres,whichhavedifferentdivisionsasstudiedin
recognitionscience[29,30],e.g.,theleftbrainistypicallyassociatedwithlogicaltaskswhilethe
rightbrainismoreinvolvedinintuitiveprocesses. ThisinspiresustodesignWISE,whichmakes
modeleditorWISERinmemories. WISEcontainsadualparametricmemorymechanismforLLMs’
editing: themainmemoryforthepretrainedknowledgeandasidememoryfortheeditedknowledge,
realizingbothlong-termmemory’sgeneralizationandretrieval-basedworkingmemory’sreliability
andlocality. Thesidememoryisaformofmid-termmemory. Weonlyedittheknowledgeintheside
memoryandtrainaroutertodecidewhichmemorytogothroughwhengivenaquery. Forcontinual
editing,wedesignaknowledge-shardingmechanismwheredifferentsetsofeditsresideindistinct
andorthogonalsubspacesofparameters. Thesearethenmergedintoacommonsidememorywithout
conflicts. Ourcontributionsareasfollows:
• Weidentifythepitfallsofcurrentmodeleditingmethodsinlifelongsettings,thatis,theimpossible
triangleamong—reliability,generalization,andlocality. Behindtheimpossibletriangle,wefind
thereisagapbetweeneditinglong-termmemoryandworkingmemory.
• We propose WISE, with a side parametric memory as the mid-term memory, realizing the ad-
vantagesofbothparametriclong-termmemoryandretrieval-basedworkingmemory. Wedesign
memoryrouting,sharding,andmergingmodulesinWISE,makingWISEleadincontinualknowl-
edgeediting,reachingthethreemetricsbettersimultaneously.
• Extensive experiments on GPT, LLaMA, and Mistral across QA, Hallucination, and out-of-
distributiondatasetsvalidatetheeffectivenessofWISEforlifelongmodelediting.
2
2 Methodology
2.1 Preliminaries: LifelongModelEditing
Wefocusonlifelongmodeleditingproblem[10,11],whichcanensurehundredsoreventhousands
ofsequentialeditsonLLMstomaketheoutputsoftargetqueriesalignwithhumanexpectations
while maintaining LLMs’ previous knowledge and capability. Let f : X (cid:55)→ Y, parameterized
Θ
by Θ, denote a model function mapping an input x to the prediction f (x). The initial model
Θ
beforeeditingisΘ ,whichistrainedonalargecorpusD . WhentheLLMmakesmistakesor
0 train
requiresinjectionsofnewknowledge,itneedsmodeleditingwithatime-evolvingeditingdatasetas
D = {(X ,Y )|(x ,y ),...,(x ,y )}. AtthetimestepT,amodeleditor(ME)takestheT-th
edit e e 1 1 T T
editandtheLLMoftheT −1timestepf asinputsandproducetherevisedLLMmodelf
ΘT−1 ΘT
followingtheequationbelow:
(cid:26)
y ifx∈X ,
f =ME(f ,x ,y ), s.t.f (x)= e e (1)
ΘT ΘT−1 T T ΘT f (x) ifx∈/ X .
Θ0 e
Equation 1 describes that after model editing, the LLM should make the correct prediction on
the currentedit as f (x ) = y , while also preservingknowledgefrom past editinginstances
ΘT T T
(x ,y ) ∈ D aswellasmaintainingcapabilityoff ontheirrelevantdatawhenx ∈/ X ,
<T <T edit Θ0 e
especiallyforgeneraltrainingcorpusD .
train
2.2 RethinkingtheMemoryDesignofLifelongModelEditing
Table1: Comparisonofcurrentmodeleditingmethods. “(cid:33)” refersto“yes”and“well-supported”,
(cid:37)refersto“no”or“badly-supported”, and“ ”refersto“less-supported”. Thethreemetricsof
Reliability,Generalization,andLocalitydenotetheperformancesonlifelong(continual)editing.
(cid:35)
Methods Long-termMemory WorkingMemory ParametricKnowledge RetrievalKnowledge WhetherLifelong Reliability Generalization Locality
FT-EWC (cid:33) (cid:37) (cid:33) (cid:37) (cid:33) (cid:33) (cid:33) (cid:37)
ROME/MEMIT (cid:33) (cid:37) (cid:33) (cid:37) (cid:37) (cid:37) (cid:37) (cid:37)
MEND (cid:33) (cid:37) (cid:33) (cid:37) (cid:37) (cid:37) (cid:37) (cid:37)
SERAC/DEFER (cid:37) (cid:33) (cid:33) (cid:33) (cid:33) (cid:37)
GRACE (cid:37) (cid:33) (cid:37) (cid:33) (cid:33) (cid:33)(cid:35) (cid:37) (cid:33)(cid:35)
WISE (cid:33) (cid:33) (cid:33) (cid:33) (cid:33) (cid:33) (cid:33) (cid:33)
In Table 1, we compare current model editing methods in terms of memory types and lifelong
editing abilities. FT-EWC [20], ROME [18], MEMIT [19], and MEND [31] edit the long-term
memorystoredintheLLMs’modelparameters,buttheyeitherdonotsupportcontinualeditingor
havenegativeeffectsonirrelevantknowledge(poorlocality). GRACE[10]isdesignedforlifelong
editing via retrieval-based working memory. The retrieval codebook can avoid the conflicts of
irrelevantknowledge,butGRACEfailstogeneralizeduetoitscodebookbeinganon-parametric
knowledgerepresentationthatsolelymemorizesquerieswithoutcomprehension. Itisworthnoting
thatSERAC[32]/DEFER[10]usesworkingmemorythatisstoredinadditionalsmallmodels: a
scopeclassifierandacounterfactualmodel,whoseknowledgeisparametric. However,thesmall
counterfactualmodelcannotmatchtheexpressivenessandgeneralizationcapabilitiesofLLMitself,
makingitchallengingfortheeditedknowledgetogeneralizeeffectively.
Toenableeffectivelifelongmodelediting,themethodshouldtakeadvantageofbothLLMparameters’
long-termmemoryandretrieval-basedworkingmemory. Therefore,weproposeWISEasfollows.
2.3 WISE:SideMemorywithKnowledgeSharding,Merging,andRouting
AsillustratedinFigure2,WISEcomprisestwokeycomponents: 1)SideMemoryDesign: i)side
memory: sidememoryisamemorycontainerthatisinitializedasacopyofLLM’scertainFFNlayer,
storingthestreamofedits;ii)memoryroutingmechanism: similartoretrieval,aroutingactivation
componentisadoptedtoidentifythescopeofedits,routingthemain(original)orsidememories
duringinference;2)KnowledgeShardingandMerging:i)knowledgeinrandommemorysubspaces:
tomaketheeditsinappropriateknowledgedensityandavoidforgetting,weshardthesidememory
into several random subspaces for editing; ii) knowledge merging: we leverage model merging
techniquestomergedifferentmemoryshardsintoonesidememorywithoutlossofknowledge.
3
Layers before editing Editing layer Layers after editing ① Initialize Wv' with Wv
e.g., 0-25 Layers for LLaMA-2-7B e.g., 26-th Layer for LLaMA-2-7B e.g., 27-31 Layers for LLaMA-2-7B
② Generate k random masks with
mask ratio ρ for edit streams {xt}
Attn xt-2xt-1 xt xt+1 xt+2xt+3...T
Main (time)
Memory
If ∆act(x) < ε FFN
Wv ③ Edit in side memory subspaces
Data x L I a n y p e u r t s ... L I a n y p e u r t s ... W FF k N A R c o t u iv ti a n t g ion ... O La u y tp er u s t
④ Merge subspaces into one
FFN side memory via Ties-Merge
If ∆act(x) > ε
S
m
e
a
l
x
e c
o
t
n
t
e
he Wv'
Editing Side
Layer Memories
(a) Workflow Overview with Knowledge Routing (b) Knowledge Sharding and Merging
Figure2: OverviewofWISE.Sidememory(inblue)andmainmemory(ingreen)storeeditedand
pretrainedknowledge,respectively. Note: duringinference,ifWISE-Retrieve,theactivationrouting
willretrieveandselectonesidememorywithmaximalactivationscore.
2.3.1 SideMemoryDesign
Side memory in FFN’s value matrix. Each layer in a Transformer contains a multi-head
self-attention(MHA)mechanismand afeed-forwardnetwork (FFN),wheretheFFNconstitutes
two-thirdsofthemodelparameters[33]. ThequestionofhowTransformersretrieveandutilizestored
knowledgeremainsunresolved[18,34],yetpastworks[31,33]havedemonstratedthateditingthe
weightsoftheFFNisconsistentlymoreeffectiveforLLMs. TheFFNtypicallyconsistsofkey-value
linearmatrices: W ,W ,i.e.,twomulti-layerperceptron(MLP)layers. Fortheoutputofattention
k v
featuref,thecomputationofthefeed-forwardnetwork,omittingthebiasterms,canberepresentedas:
FFN(f)=a·W =σ(f⊤·W )·W , (2)
v k v
whereσ isanonlinearactivationfunction(e.g. SwiGLU,GeLU),andarepresentstheactivation
valuesofthefirstMLPlayer. Followingpreviousworks[18,33],weeditthevaluematrixW of
v
thechosenFFNlayer.
However,directlyeditingthevaluematrixmaycauseforgettingandsideeffectsinalifelongsetting.
Thus,wecopyavaluematrixassidememoryandeditthesidememoryinsteadoftheoriginal
matrix(mainmemory). Specifically,thesidememoryisinitializedwiththecopyofmainmemory
asW ← W . Giventhesidememory,thenewoutputisexpressedasFFN (f) = a·W . We
v′ v s v′
willintroducehowtoupdatethesidememoryinSection2.3.2.
Locatingsidememory’sFFNlayer. TransformerLLMshavebeenwidelydemonstratedtoencode
“lower-level”information(e.g.,partsofspeech)inearlierlayerswhileprocessingmoreadvanced
linguisticphenomenalikeanaphoraandcoreferenceinlaterlayers[35–37]. Representationsinlater
hidden layers propagate through residual connections without drastic changes [38, 18], enabling
effectiveearlyexitinLLMs[39,40]. Therefore,tominimizethesideeffectsofeditingandadjust
advanced linguistic phenomena, we target mid-to-late layers (e.g. 27) for side memory. Further
analysisoflayerselectionisprovidedinSection3.3.
Routingbetweensidememoriesandmainmemory. Similartotheretrieval-basedmethods[10,
32],duringinference,itisneededtodecidewhetherthemainmemoryorthesidememoryisused.Ifa
givenqueryiswithinthescopeofpreviousedits,thesidememoryisused;otherwise,themainmemory.
Inspiredby[11],weintroducearoutingactivationindicator,givenaninputx,itisformulated:
∆ (x)=∥A(x)·(W −W )∥ , (3)
act v′ v 2
whereA(·)=aistheactivationofthesidememory’scorrespondingFFNlayerinEquation2. We
wanttheactivationindicatorsofeditingqueriestobelargerthantheonesofirrelevantqueriesby
alargemargin,whichis:
min{∆ (x )|x ∈D }≫max{∆ (x )|x ∈D }, (4)
act e e edit act i i irr
whereD istheirrelevantdatasetwhichincludesD .
irr train
4
To achieve the above objective, we design a margin-based loss function during editing training,
similartocontrastive[41]ortripletloss[42]. Themargin-basedlossfunctionforroutingactivationis:
L =min{max(0,∆ (x )−α)+max(0,β−∆ (x ))+max(0,γ−(∆ (x )−∆ (x )))}, (5)
a act i act e act e act i
Wv′
s.t.x ∈D ,x ∈D .
e edit i irr
Equation5aimsthatforallqueriesofirrelevantexamplesx ,theactivationindicatorsshouldbe
i
lessthanthresholdα,andfortheeditsamplesx ,theactivationsshouldbelargerthanthreshold
e
β,withacertaindistanceγ between∆ (x )and∆ (x ).
act e act i
Inthecontinualstreamofincomingedits,thesmallestactivationindicatorwithintheeditsisupdated
andsaved: ϵ=min{∆ (x )|x ∈D }. Weaimtorecognizethelocalscopeofeditsinthisform.
act e e edit
Duringinference,iftheactivationindicatorofanewinputisgreaterthanϵ,WISEwillusetheside
memoryW ;otherwise,usingthemainmemoryW . Thus,giventhequeryx,theoutputofthe
v′ v
targetedFFNinEquation2isreplacedby:
(cid:26)
A(x)·W if∥A(x)·(W −W )∥ >ϵ,
FFN (x)= v′ v′ v 2 (6)
out A(x)·W otherwise.
v
2.3.2 KnowledgeShardingandMerging
Howtoeffectivelyandefficientlystorecontinualknowledgeinmodelparametersisimportantfor
lifelongediting. Weintroducethenotionof“knowledgedensity”(similartoknowledgecapacity[43])
thatdescribeshowmanypiecesofknowledgearestoredperparameteronaverage. Thereisanediting
dilemmaw.r.t. knowledgedensity: i)Ifonlyafeweditsaremadeforfullfine-tuningoreditingthe
entirememory,theknowledgedensityislow,whichmayleadtooverfitting. ii)Ifnumerousedits
aremadewithinacommonandlimitedparameterspace,theknowledgedensityishigh,resultingin
conflictswithintheeditedknowledgeandpotentiallycausingcatastrophicforgetting. Toremedythis
dilemma,weproposeaknowledgeshardingandmergingmechanismtodividetheeditsintoseveral
shards,storethemindifferentparametersubspaces,andmergethemintoacommonsidememory.
Knowledgeinrandommemorysubspaces. WeeditthesidememoryW . Wedivideneditsinto
v′
kshards,copythesidememoryforktimes,andgeneratekrandomgradientmaskwithmaskratioρ
foreachcopyofsidememory. ArandomgradientmaskM
i
∈{0,1}|W v′|,i∈[k]isabinarymask
whoseproportionof1isρ[44]. Foreditshardi,i∈[k],weedittheknowledgeintothesubspace
M asfollows:
i
Wi ←Wi −η(M ⊙g (Wi )), (7)
v′ v′ i i v′
whereWi isthei-thcopyofthesidememory,ηisthelearningrate,g (·)isthegradientofthei-th
v′ i
shardofedits,andthegradientistheautoregressivelossplustheroutingactivationlossL (Equation
a
5): L =−logP (y |x )+L .
edit W v′ e e a
Therandommaskofgradientsfreezestheparametersintactwhentheelementsare0andupdates
theweightswhentheelementsare1. Itissuperiortopruningbecauseitdoesnotharmthenetwork
performancewhileregularizingoptimizationinasubspace[44]. Inaddition,theρsubspacewillhave
higherknowledgedensitywhenk·ρ<1,resultinginhighergeneralization(e.g.,Figure5). Also,
differentshardsofeditshavedifferentrandommasks,andduetothe(sub)orthogonalityofrandom
masks,differentshardswillnotconflictwitheachother. Therefore,wecannon-destructivelymerge
thekcopiesofsidememoryintoone.
Knowledge merging. We merge the k subspace pieces of side memory into one. Because we
randomlygeneratethesubspacemasks,differentrandommaskswillhavesomeoverlappingelements
andsomedisjointelements,followingthetheorembelow:
Theorem2.1 SubspaceOverlap. GeneratekmemorysubspacesWi ,i∈[k]byrandommaskwith
v′
1’sratioρ,soeachmemoryhasρ·|W |activetrainedparameters. ForanytwosubspacesWi
v′ v′
andWj i ̸= j;i,j ∈ [k], thereareρ2 ·|W |activeparametersthatareoverlapped. Forallk
v′ v′
subspaces,thereareρk·|W |overlappedactiveparameters.
v′
Thetheoremshowsthatlargerρwillcausemoreoverlapofsubspaceparameters,andtheproofis
inAppendixC.Wefindthatthisoverlapishelpfulinplayingtheroleof“anchors”forknowledge
merging(SeeFigure5andAppendixB.5). However,knowledgeconflictsalsoexistintheoverlapped
parameters,soweleveragetherecenttaskarithmeticmodelmergingtechniqueTies-Merge[45]to
5
Table2: MaineditingresultsforQAsetting(ZsREdataset). T: NumEdits.
QA
Method
T=1 T=10 T=100 T=1000
Rel. Gen. Loc. Avg. Rel. Gen. Loc. Avg. Rel. Gen. Loc. Avg. Rel. Gen. Loc. Avg.
LLaMA-2-7B
FT-L 0.57 0.52 0.96 0.68 0.48 0.48 0.76 0.57 0.30 0.27 0.23 0.27 0.19 0.16 0.03 0.13
FT-EWC 0.96 0.95 0.02 0.64 0.82 0.76 0.01 0.53 0.83 0.74 0.08 0.55 0.76 0.69 0.08 0.51
MEND 0.95 0.93 0.98 0.95 0.26 0.28 0.28 0.27 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
ROME 0.85 0.80 0.99 0.88 0.64 0.62 0.75 0.67 0.23 0.22 0.04 0.16 0.01 0.01 0.00 0.01
MEMIT 0.84 0.81 0.99 0.88 0.58 0.58 0.85 0.67 0.02 0.02 0.02 0.02 0.04 0.04 0.02 0.03
MEMIT-MASS 0.84 0.81 0.99 0.88 0.75 0.72 0.97 0.81 0.76 0.68 0.85 0.76 0.69 0.65 0.62 0.65
DEFER 0.68 0.58 0.56 0.61 0.65 0.47 0.36 0.49 0.20 0.12 0.27 0.20 0.03 0.03 0.74 0.27
GRACE 0.99 0.36 1.00 0.78 0.96 0.16 1.00 0.71 0.96 0.15 1.00 0.70 0.93 0.08 1.00 0.67
WISE 0.98 0.92 1.00 0.97 0.94 0.88 1.00 0.94 0.90 0.81 1.00 0.90 0.77 0.72 1.00 0.83
Mistral-7B
FT-L 0.58 0.54 0.91 0.68 0.39 0.39 0.50 0.43 0.11 0.10 0.02 0.08 0.16 0.13 0.01 0.10
FT-EWC 1.00 0.99 0.01 0.67 0.84 0.78 0.02 0.55 0.82 0.72 0.09 0.54 0.76 0.69 0.09 0.51
MEND 0.94 0.93 0.98 0.95 0.01 0.01 0.02 0.01 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00
ROME 0.79 0.77 0.98 0.85 0.58 0.57 0.75 0.63 0.05 0.05 0.02 0.04 0.04 0.04 0.02 0.03
MEMIT 0.81 0.79 0.99 0.86 0.46 0.45 0.61 0.51 0.00 0.00 0.01 0.00 0.04 0.04 0.02 0.03
MEMIT-MASS 0.81 0.79 0.99 0.86 0.74 0.71 0.97 0.81 0.73 0.71 0.88 0.77 0.73 0.70 0.62 0.68
DEFER 0.64 0.54 0.79 0.66 0.53 0.43 0.29 0.42 0.28 0.17 0.26 0.24 0.02 0.02 0.67 0.24
GRACE 1.00 0.36 1.00 0.79 1.00 0.15 1.00 0.72 1.00 0.15 1.00 0.72 1.00 0.02 1.00 0.67
WISE 0.98 0.97 1.00 0.98 0.92 0.89 1.00 0.94 0.87 0.80 1.00 0.89 0.70 0.67 1.00 0.79
relievetheconflicts. First,wecomputetheeditweightshiftvectorsT ={τi =Wi −W |i∈[k]}.
e e v′ v
Then,weuseTies-Mergetomergetheeditvectorsintoone:
W ←W +Ties(T ;W ). (8)
v′ v e v
Ties-Mergeconsistsofthreesteps: i)trim: trimtheredundantparametersforeachtaskvector;ii)
electthesign: electthesignsofeachparameter;ii)disjointmerge: computethedisjointmeanfor
eachparameterwhichhasthesameandcorrectsigns[45]. ByTies-Merge,differentsubspacesof
knowledgeareintegratedintoonewithfewerconflicts. Westudytheeffectsofdifferentmerging
techniquesinTable11ofAppendixB.2.
Routingandretrievingamongseveralsidememories. Onesinglesidememoryhasitslimited
knowledgecapacity[43]. Forthelifelongeditingstream,wecanproduceseveralsidememories
andretrievethemviaactivationscorerouting. Wecomputedifferentactivationindicatorscoresof
sidememoriesandretrievethetop-1duringinference. ThisdesignisnamedWISE-Retrieve,which
enablesamorechallenginglifelongeditingscenario. ForWISEwithonlyonesidememory,itis
notated as WISE-Merge. For most of the experiments, we use WISE-Merge by default, and we
compareWISE-RetrieveinTable6andFigure6.
Thepseudo-codeofourmethodcanbefoundinAlgorithms1and2.
3 Experiments
3.1 ExperimentalSettingsandEvaluationMetrics
Intheexperiments,wecomparetheperformanceofdifferentbaselinesandWISEinsequentially
editing LLM models hundreds to thousands of times. In practice, we augment x by generating
e
10randomtokensequencesoflength10usingf ,enhancingeditinggeneralization/adaptationto
Θ
diversecontexts. Weensurethatthisaugmentationwithrandomtokensisappliedacrossallbaselines
(SeeAppendixB.6,weablatethecontributionofRandomToken).
DatasetsandModels. Wechoosetrendingau- Table3:Datasetstatisticsformainresults.Locality
toregressiveLLMmodelsLLaMA-2-7B[13], Dataistheirrelevantdataoftheeditingprocess. T
Mistral-7B [52], and GPT-J-6B [53, 54] for isthenumberofsamples. Pre-editistheunedited
evaluation. The dataset details are in Table model’sperformanceoneachdataset.
3. Following [10], we evaluate WISE on the
SETTING EDITINGDATA T Pre-edit(LLaMA/Mistral) LOCALITYDATA
closed-book question-answering (QA) dataset
QA ZsRE[46] 1,000 0.36/0.39ACC NQ[47]
ZsRE[46],andalsoevaluateitsabilitytocor- Halluc. SelfCheckGPT[48] 600 27.4/19.4PPL RedPajama[49]
OODGen. Temporal[50] 100 0.56δ-ACC(GPT-J) Pile[51]
rectHallucinationinSelfCheckGPT[48]. The
Temporaldataset[50]isemployedtotesttheout-of-distribution(OOD)generalizationofediting.
SinceTemporalcomprisesemergingentitiespost-2019,weavoidusingthelatestLLMsinOOD
experiments. Instead,wefollowtheoriginalliteratureoftheTemporaldataset[50]andadoptGPT-J-
6Basthebasemodel,whichispretrainedonthePile[51]withacutoffin2020. Implementation
detailsandeditingexamplesforeachdatasetandcanbefoundinAppendixA.
6
Table4: MaineditingresultsforHallucinationsetting(SelfCheckGPTdataset). T: NumEdits.
Hallucination
LLaMA-2-7B Mistral-7B
T=1 T=10 T=100 T=600 T=1 T=10 T=100 T=600
Method Rel.(PPL↓) Loc.(↑) Rel.(↓) Loc.(↑) Rel.(↓) Loc.(↑) Rel.(↓) Loc.(↑) Rel.(↓) Loc.(↑) Rel.(↓) Loc.(↑) Rel.(↓) Loc.(↑) Rel.(↓) Loc.(↑)
FT-L 4.41 0.96 12.57 0.71 33.06 0.41 69.22 0.26 25.03 0.38 100.00 0.03 1594.93 0.00 - -
FT-EWC 2.56 0.24 3.63 0.09 2.10 0.16 4.56 0.24 1.75 0.04 3.05 0.09 4.73 0.17 5.46 0.25
MEND 5.65 0.87 11.01 0.86 10.04 0.88 1847.90 0.00 7.64 0.96 83.74 0.05 23114.94 0.01 - -
ROME 1.68 0.99 2.04 0.94 94.15 0.05 104.93 0.02 2.04 0.99 3.45 0.92 103.75 0.03 241.17 0.01
MEMIT 1.66 1.00 2.36 0.97 76.65 0.05 107.61 0.02 1.64 1.00 15.89 0.89 97.23 0.04 132.30 0.02
MEMIT-MASS 1.66 1.00 1.61 0.99 7.18 0.96 13.47 0.94 1.64 1.00 2.78 0.99 3.22 0.97 7.28 0.95
DEFER 1.29 0.23 3.64 0.28 8.91 0.19 19.16 0.12 4.76 0.45 7.30 0.25 9.54 0.43 24.16 0.13
GRACE 2.21 1.00 8.67 1.00 9.67 1.00 9.34 1.00 1.39 1.00 5.97 1.00 9.53 1.00 9.57 1.00
WISE 1.91 1.00 1.04 1.00 1.14 1.00 3.12 0.99 1.40 1.00 2.56 0.94 1.31 0.99 5.21 0.93
Baselines. Thebaselinesincludemethodsofcontinuallearningandmodelediting. Wecompare
WISE against direct fine-tuning FT-L with an additional KL divergence loss [18], and continual
learning fine-tuning based on Elastic Weight Consolidation (FT-EWC) [20]. We also compare
WISEtoothermodeleditors,including1)GPT-styleeditorsbasedoncausaltracing: ROME[18],
MEMIT[19],andMEMIT-MASS(abatch-editingversionofMEMIT);2)hypernetwork-based
editors: MEND[31];and3)thelatestmemory-basededitors: DEFER(inspiredbySERAC[32]for
inferencerouting)andGRACE[10]. DetailsonallcomparisonsarefoundinAppendixA.2.
Metrics. Eacheditexampleincludesaneditdescriptor(i.e.,query)x ,itsparaphrasepromptsx
e e′
(ifavailable)fortestinggeneralization,andanunrelatedstatementx fortestinglocality. Forthe
loc
editingdatasetD ={(X ,Y )}withT edits,weevaluatethefinalpost-editmodelf afterthe
edit e e ΘT
T-theditexample(x ,y ). Weevaluatethemodeleditor’sreliabilityandgeneralizationusingthe
T T
metricsRel. (a.k.aEditSuccessRate[10])andGen. (GeneralizationSuccessRate[55]),whileLoc.
(LocalizationSuccessRate[55]),definedasthepost-editmodelshouldnotchangetheoutputofthe
irrelevantexamplesx ,assessesspecificity. Wereportthesemetricsandtheirmeanscores,which
loc
areformallydefinedas:
Rel.=
T
1 (cid:88) T 1(fΘT (xt
e
)=y
e
t), Gen.=
T
1 (cid:88) T 1(fΘT (xt e′)=y
e
t), Loc.=
T
1 (cid:88) T 1(fΘT (xt
loc
)=fΘ0 (xt
loc
)), (9)
t=1 t=1 t=1
where1(·)istheindicatorfunction. Notably,fortheHallucinationdataset,following[10],weuse
theperplexity(PPL)toverifythelocality,andthereisnopropermetricforgeneralization.
3.2 MainResults
CompetitivePerformanceofWISE. ThecompetitiveperformanceofWISEisevidentinTable
2 and 4, which compare its results with eight baselines on the QA (ZsRE) and Hallucination
(SelfCheckGPT) settings. In general, we observe the followings: ❶ WISE outperforms existing
methods on multiple tasks after long editing sequences; ❷ direct editing of long-term memory
(ROME,MEMIT,etc.) createsconflictswithpriorpretrainingknowledge,resultinginpoorlocality;
and❸retrievingworkingmemoryandmodifyingactivations(GRACE,DEFER,etc)struggleto
generalizetodiversequeries.
IntheQAsetting,withT =1000,WISEachievesaverage Table 5: OOD results for Temporal
scoresof0.83and0.79onLLaMAandMistral,respec- dataset. GPT-J-6Bisused.
tively,reflectingimprovementsof18%and11%overthe
T=10 T=75
nearestcompetitor. ThisdemonstratesWISE’soutstand- Method Rel. OODGen.Loc. Avg. Rel. OODGen.Loc. Avg.
ingstabilityandeffectivemanagementoflong-sequential w/oEditing 0.56 0.21 - 0.39 0.56 0.21 - 0.39
FT-EWC 0.87 0.17 0.13 0.39 0.81 0.22 0.18 0.40
edits. WhilemethodslikeMENDandROMEarecompet- ROME 0.09 0.00 0.06 0.05 0.05 0.00 0.03 0.03
MEMIT-MASS 0.73 0.22 0.99 0.65 0.78 0.27 0.97 0.67
itiveearlyinediting,theyshowclearshortcomingsasthe DEFER 0.68 0.33 0.08 0.36 0.52 0.26 0.08 0.29
GRACE 0.97 0.28 1.00 0.75 0.97 0.28 1.00 0.75
editsequenceextends. Directlyeditinglong-termmemory
WISE 0.99 0.36 0.98 0.78 0.96 0.37 1.00 0.78
(e.g.,MEMIT,FT-EWC,MEND)resultsinasignificant
declineinLoc. WhenT ∈ {100,1000},thisindicatesthatthesemethodscannotpreserveLLMs’
knowledgestructureandsignificantlyimpairthemodel’sgeneralizationability.GRACEexcelsinLoc.
andRel. (closeto1.00),however,itsacrificesgeneralizationincontinualediting. Apossiblereason
isthattokenrepresentationmaynotbesuitableformeasuringsemanticsimilarityinautoregressive
LMs,leadingtoparaphrasex failingtoachievesimilaritymatchingwithanyCodeBookKeyin
e′
GRACE(detailedinAppendixB.1). Overemphasisonpreservingandpreciselyadaptingtraining
data(workingmemory)hampersadaptabilitytonewcontexts. Inanutshell,mostpreviousmethods
struggletobalanceRel., Gen., andLoc., particularlyinlong-formeditingtasks. Inaddition, the
resultsofGPT-J-6BcanbefoundinFigure9intheAppendix.
WISEalsosurpassesthebaselinesontheHallucinationdataset,maintainingthelowestperplexity
scores of 3.12 and 5.21 at T = 600, with Loc. remaining above 0.93. We similarly observe
7
1.0 Reliability
Generalization
0.8 Locality
0.6 GRACE Avg
0.4
0.2
0.0
l
=0
l
=1
l
=13
l
=14
l
=25
l
=26
l
=27
l
=31
0.03 0.1 0.2 0.3 0.4 0.5 0.6
Figure 4: Analysis of locating
FFN layer of side memory for
WISE.ZsRE,LLaMA-2-7B.
k
0.2
0.3
0.4
0.5
0.6
Performance (Avg.)
0.85
0.780 0.833 0.850 0.840 0.843 0.830 0.790 2.0
0.80
0.717 0.813 0.807 0.820 0.813 0.803 0.750 3.0
0.75
0.660 0.790 0.810 0.817 0.820 0.813 0.813 4.0
0.70
0.577 0.773 0.803 0.803 0.797 0.803 0.750 0.65 5.0
0.637 0.723 0.740 0.790 0.797 0.803 0.797 0.60 6.0
0.03 0.1 0.2 0.3 0.4 0.5 0.6
k
Subspace Overlap
0.00 0.01 0.04 0.09 0.16 0.25 0.36
102
0.00 0.00 0.01 0.03 0.06 0.12 0.22
104
0.00 0.00 0.00 0.01 0.03 0.06 0.13
106
0.00 0.00 0.00 0.00 0.01 0.03 0.08
0.00 0.00 0.00 0.00 0.00 0.02 0.05 108
k
Figure5: Analysisofdifferentmaskratiosρandsubspaceskfor
WISE. Left: Avg. performance of Rel., Gen., and Loc.; Right: the
subspaceoverlapprobabilityinTheorem2.1.ZsRE,LLaMA-2-7B.
significantPPLincreasesforFT-L,MEND,andROMEinlong-contexteditingtasks,whileGRACE’s
performanceislacklusterinLLMlongtexts(possiblyduetothelimitedfittingcapacityofthevery
smallactivetrainedparameters|hl|ofGRACE).
Out-of-DistributionEvaluation. Ideally,modeleditingneedstogeneralizedistributionallyfrom
formulaiceditingexamplestonaturaltexts[50],wherethedistributionalshiftinvolvescomplexity
ratherthanconventionaldomainshift[56]. Following[50], weevaluatetheOODgeneralization
ofeditingmethodsonemergingentitiesusingthetemporalupdatingdataset,Temporal. Editing
examples and evaluation metrics are provided in Appendix A.1. As shown in Table 5, WISE
effectivelyhandlesout-of-distributiongeneralizationtasks(achievingthebestOODGen. andoverall
performance).DEFERdeliversmediocreperformanceonOODGen.duetothelimitedcapacityofthe
auxiliarymodel[14]. Duringthefine-tuningphase,GRACEandMEMITfocusontherepresentation
v∗ofasingleinputtokenafterW (GRACE:lasttoken, MEMIT:lastsubjecttoken). However,
v
regardingv∗theeditingcarrierencounterstwoproblems: 1)thetrainingobjectiveisnotalignedwith
thepretrainingphase,and2)thesinglerepresentationlimitsthesearchscopeofgradientdescent,
makingitdifficulttohandleOODgeneralization. WISE,ontheotherhand,avoidsthesechallenges.
3.3 FurtherAnalysis
40
20
0 200 400 600 800 1000
erocS
noitavitcA
QA (zsre)
Edit prompt
Rephrase prompt
Irrelevant prompt
60
40
20
0 100 200 300 400 500 600
erocS
noitavitcA
Visualization of WISE’s Routing Activation. To
demonstrate the effectiveness of memory routing, we
record the activation values ∆ (x) of 1000 (QA, act
ZsRE)/600(Halluc.)queriesduringtheinferencestagevia
knowledgemergingintoasinglesidememory. Asshown
inFigure3,thepurplehorizontallinerepresentstheactiva-
tionthresholdϵrecordedduringtheeditingphase. Almost Hallucination (selfcheckgpt)
allunrelatedqueriesshowlowactivationswithvaluesless Edit prompt
Irrelevant prompt
than10inZsREandlessthan20inHalluc.;meanwhile,
WISE accurately routes the editing prompt and unseen
paraphrasesintothesidememory. Thisensuresediting
localityandpreventsexcessiveshiftsfromthepre-training
distributionduringlifelongediting. Figure 3: Activations of the memory
routingmoduleofWISEwhenvary-
Localization Analysis of WISE’s Side Memory. To
ingT. X-axis: Numedits. LLaMA-7B.
validate the benefits of editing mid-to-late layers, we
select decoder layers from early, intermediate, mid-to-late, and late stages. As shown in Figure
4, theablationresultsrevealthateditingcriticallayersliketheearlyandfinallayers(0, 1, 31)is
ineffective,evenresultinginaverylowLoc. valueof0.096,whichindicatesafailuretorecognize
the editing scope. This may occur because the early layers represent fundamental grammatical
information, andthefinallayerdirectlycontrolsthedecodingprocedure, leadingtopoorediting
of advanced language functions. Editing in the intermediate layers is suboptimal but still shows
a markable improvement compared to early layers, possibly because intermediate layers start to
integratebasicgrammaticalinformationwithmorecomplexsemanticdata. Notably,themid-to-late
layersdemonstrateexceptionaleditingperformance; forinstance,selectinglayer26resultsinan
80%successrateandgeneralizationwhilemaintaining100%locality. Thisempiricallysupports
ourclaiminSection2.3.1thattheredundantmid-to-latelayers[39]areidealsidememorylayers
andconfirmsthehierarchicalnatureofinformationprocessinginTransformerLLMs[57,58].
Analysisofρandk forWISE. WeanalyzetheimportanthyperparametersofWISE:themask
ratioρandthenumberofsubspacesk inFigure5. Ontheleftfigure,fork = 2,thebestρis0.2,
8
satisfying k ∗ρ = 0.4 < 1, which implies the effectiveness of our subspace design that higher
knowledge density will cause better generalization. When scaling k, we observe an increasing
demandofρ. FromTheorem2.1,theprobabilityofsubspaceoverlapisρk,andwehypothesizethat
thisoverlapisimportantasananchorformodelmerging. Interestingly,fromtherightfigure,itcan
beobservedthattheoptimalcasesalwayshavetheρk closestto0.03. Thisshowsaninherenttradeoff
betweenmergeanchorandmergeconflicts,andthesubspaceoverlapsaround0.03areoptimalfor
the best performances. Such experiments indicate that 20% FFN parameters can accommodate
atleast500editedsamples. When"maskmemoryexhaustion"occurs,wecanallocatenewmask
parameterstostorenewknowledge. Usingretrievewhenknowledgeisn’tfullandmergingasneeded
tosavememory,achievestruelifelongmodelediting.
ScaleUpto3KofEdits. Wescalethenum-
Table6: Scalingto3KeditsofZsRE.LLaMA-2-7B.
ber of continual edits to 3K in Table 6. We
compareWISE-Merge,keepingonesidemem- T=2000 T=3000
Method
orybymulti-timemerging,andWISE-Retrieve, Rel. Gen. Loc. Avg. Rel. Gen. Loc. Avg.
keepingseveralsidememoriesbyroutingand GRACE 0.96 0.03 1.00 0.66 0.96 0.03 1.00 0.66
MEMIT-MASS 0.64 0.58 0.55 0.59 0.58 0.53 0.47 0.53
retrievingamongdifferentsidememories. For
WISE-Merge 0.66 0.63 1.00 0.76 0.58 0.56 1.00 0.71
WISE-Retrieve,weshowanupperbound“ora- WISE-Retrieve 0.68 0.64 1.00 0.77 0.61 0.58 1.00 0.73
cle”,whichalwaysidentifiesthecorrectrouting WISE-Retrieveoracle 0.77 0.72 1.00 0.83 0.75 0.70 1.00 0.82
path. WeobservethattheWISEseriesmaintainshighscalability,consistentlyoutperformingthe
strongestbaselinesincludingMEMIT-MASSandGRACE.WISE-Retrievebasedontop-1activa-
tionretrievaldemonstratesthebestresultsin3Kedits,showingtheeffectivenessofwell-organized
memorysubspacesandroutingstrategiesduringediting. Wenotethatthe“oracle”exhibitsmarginal
performancedeclinewhenscalingtheeditsfrom2Kto3K,yetitdemonstratesremarkableperfor-
manceacrossallmetrics. ThisunderscoresthepotentialofWISEtohandleextremelylongcontinual
edits,contingentuponsubstantialimprovementintheretrievalofsidememories. Additionally,an
appropriatereplayofeditscanfurtherimproveretrievalaccuracy,asdetailedinAppendixB.3.
Contribution of Router designs in WISE. Without the Table7: AblationstudyofRouter
routerstrategy,allinputseitherpasssolelythroughthemainor (comparedwithTable2). LlaMA.
sidememory. Tofurthervalidateitseffectiveness,weconduct
additionalablationswithL
a
. WISE’sperformanceonZsRE WISEw.o.La Rel. Gen. Loc. Avg.
isshowninTable7. WeobservetheexpecteddecreaseinLoc. T=1 1.00 0.96 0.93-0.07 0.96-0.01
T=10 0.93 0.90 0.88-0.12 0.90-0.04
w.o. L , such as dropping from 1.00 to 0.72 at T=1000, re-
a T=100 0.92 0.85 0.81-0.19 0.86-0.04
veals the router’s effectiveness in identifying editing scopes, T=1000 0.84 0.79 0.72-0.28 0.78-0.05
minimizingsideeffects,andretainingasubstantialamountofpre-trainingknowledge.
1.30
1.25
1.20
1.15
1.10
1.05
1.00
0.95
0 500 1000 1500 2000 2500 3000
)x0.1(
emiT
ecnerefnI
Inference Time Analysis of WISE. Figure 6
shows the inference time of a single instance for w/o Editing
WISE Merge
LLaMAaftert ∈ [0,3000]editingsteps,measured WISE Retrieve
across10trialsofeachsetting. Consistentwithour
expectations,wefindthatWISE-Mergeincursacon-
stantinferencedelay(about3%)astheeditingstream
expands. WISE-Retrieve,duetotheintroductionof
retrievalrouting,showsanincreaseininferencetime
Figure 6: Inference time of WISE when
as the number of edits increases, with a time cost
varyingT. ZsRE,LLaMA-2-7B.
increment of about 7% after 3K edits. Knowledge
mergingensuresthatWISE-Mergeonlybringsconstantadditionalcosts(0.64%extraparametersand
4%extraGPUVRAM,asdetailedinAppendixB.7),contrastingwithpastmemory-basedworksthat
continuouslydemandmoreavailablememory[10,32].
4 RelatedWorks
MemoryandKnowledgeInjectionofLLMs. LLMshavelong-term(episodic)andworkingmem-
ory[24,25,27]. Long-termmemoryisstoredinmodelparameters,updatablevia(re)pretraining[53],
finetuning[59], andmodelediting[14]. Workingmemoryresidesinneuronactivations, utilized
duringinference[24].In-contextlearningandretrieval-basededitingmethodslikeGRACEcontribute
toworkingmemory[60,10]. However,whetherfinetuningorretrievalisdebated[61,62]. Also,
currentknowledgeinjectionmethodsoftensufferfromcomputationaloverhead[13,10],catastrophic
forgetting [63], and overfitting [64]. Methods like MemorryLLM [28], SPALM [27], NKB [65],
andMemoria[25]areproposedtoimprovethememoriesfromthearchitecturedesignperspective.
9
ModelEditingofLLMs. Modeleditingencompassesconstrainedfinetuning,locating-and-editing,
meta-learning,andretrieval-basedmethods. ROMEidentifiesfactualassociationsandeditsefficiently
usingMLP-basedmemories[18],extendedbyMEMITformass-editing[19]. T-Patcheraddsneurons
foreditsinLLMs’feed-forwardlayers[11]. Meta-learningmethodslikeMENDdecouplefinetuning
gradientstogeneralizeedits[31],complementedbyMALMENaddressingcancellationeffects[15].
Retrieval-basedmethodslikeSERACandGRACEimproveworkingmemoryforediting[32,10].
Fromsingletomasseditingandstatictolifelongediting,modeleditingevolvestomeetrealistic
demands. ThelatesteffortsinlifelongeditingsuchasLTE[66],MALMEN[15],andRECIPE[67]
requireextensivetrainingwithdomain-specificeditsbeforespecificediting,yetwecannotpredict
thedomainofupcomingeditsintheeditingflowandaccessingthesedataisoftenimpracticalor
unrealistic. Itpotentiallyincreasestherisksassociatedwithretraining.
ModelMerging Modelmerging[68],alsoknownasmodelfusion[69,70],studieshowtoaggregate
different models’ knowledge into one by parameter merging. However, in the research of linear
modeconnectivity,itisfoundthatdifferentminimaofneuralnetworkscanhardlybemergedintoa
generalizedoneeveniftrainedonthesamedatasetsfromthesameinitialization(butwithdifferent
randomseeds)[71,72]. Themainreasonisconsideredtobethepermutationinvariancepropertyof
deepneuralnetworks,whichmeansthatthepositionsofneuronscanbepermutedwithoutaffecting
thenetworkfunction[71];asaresult,differentminimaresideindifferentlossbasins[72].Toimprove
linearmodeconnectivityandmodelmerging,methodslikeoptimaltransport[70,73],re-basin[72],
andtraining-timealignment[44]aredeveloped. Fortheapplications,modelmergingtechniquescan
helptoimprovethegeneralizationoffederatedlearning[74,75]andenableknowledgeaggregation
ofdifferent-taskmodelsinataskarithmeticway[76,77]. Recently,methodsliketaskarithmeticin
tangentspace[77],TIES-Merging[45],ZipIt![78],andColDfusion[79]havebeenproposedfor
deepmodelfusionofpretrainedfoundationmodels,suchasCLIP,ViT,andlargelanguagemodels.
Specifically,TIES-Merging[45]consistsoftrim,electsign&mergepipeline,whichinspiresthe
mergeprocessofsidememoriesinourpaper.
Fordetailedrelatedworks,pleaserefertoAppendixD.
5 LimitationsandBroaderImpacts
Although WISE shows promising results in lifelong editing, it also has some limitations. One
limitationisaddressedinTable6thatthesidememoryretrievalhasroomforimprovementtoreach
the oracle. Also, in Figure 6, the inference time of WISE-Retrieve increases with ever-growing
editing streams. However, the current limitations cannot outweigh the merits of WISE in that it
currentlyreachesbetterperformanceingeneralforlifelongmodelediting.Webridgethegapbetween
long-termandworkingmemory,itmayinspirefurtherworkonmemorydesignformodeleditingor
evenLLMarchitecture. However,theapplicationofsuchtechnologiesshouldbeguidedbyethical
considerations. MalicioususersmayattempttoeditLLMstopropagatehate,highlightingtheneed
forsafeguardstopreventabuseandmitigateharmfuloutcomes. Somecurrentmodeleditorsupdate
themodel’sweightsdirectly,makingeditshardtotraceandwithdraw. WISEusesamodularand
non-destructivesidememory,allowinguserstodiscarditifeditsareunnecessaryorharmful,without
modificationstothemainLLMs.
6 Conclusion
Inthispaper,wepointouttheimpossibletriangleofcurrentlifelongmodelingeditingapproaches
that reliability, generalization, and locality can hardly be achieved simultaneously. We find the
reasonbehindthisisthegapbetweenworkingandlong-termmemory. Therefore,weproposeWISE,
consistingofsidememoryandmodelmerging,toremedythegap.
Acknowledgements
We would like to express gratitude to the anonymous reviewers for their kind comments. This
workwassupportedbytheNationalNaturalScienceFoundationofChina(No. 62206246,No. NS-
FCU23B2055,No. NSFCU19B2027),theFundamentalResearchFundsfortheCentralUniversities
(226-2023-00138),ZhejiangProvincialNaturalScienceFoundationofChina(No. LGG22F030011),
Yongjiang Talent Introduction Programme (2021A-156-G), SMP-Zhipu.AI Large Model Cross-
DisciplinaryFund,NingboScienceandTechnologySpecialProjectsunderGrantNo. 2023Z212,
InformationTechnologyCenterandStateKeyLabofCAD&CG,ZhejiangUniversity. Wegratefully
acknowledgethesupportofZhejiangUniversityEducationFoundationQizhenScholarFoundation.
10
References
[1] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon
Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural
languagemodels. arXivpreprintarXiv:2001.08361,2020.
[2] Ben Sorscher, Robert Geirhos, Shashank Shekhar, Surya Ganguli, and Ari Morcos. Be-
yondneuralscalinglaws: beatingpowerlawscalingviadatapruning. AdvancesinNeural
InformationProcessingSystems,35:19523–19536,2022.
[3] IbrahimMAlabdulmohsin,BehnamNeyshabur,andXiaohuaZhai. Revisitingneuralscaling
lawsinlanguageandvision. AdvancesinNeuralInformationProcessingSystems,35:22300–
22312,2022.
[4] WayneXinZhao,KunZhou,JunyiLi,TianyiTang,XiaoleiWang,YupengHou,Yingqian
Min,BeichenZhang,JunjieZhang,ZicanDong,YifanDu,ChenYang,YushuoChen,Zhipeng
Chen,JinhaoJiang,RuiyangRen,YifanLi,XinyuTang,ZikangLiu,PeiyuLiu,Jian-YunNie,
andJi-RongWen. Asurveyoflargelanguagemodels. CoRR,abs/2303.18223,2023.
[5] SébastienBubeck,VarunChandrasekaran,RonenEldan,JohannesGehrke,EricHorvitz,Ece
Kamar,PeterLee,YinTatLee,YuanzhiLi,ScottLundberg,etal. Sparksofartificialgeneral
intelligence: Earlyexperimentswithgpt-4. arXivpreprintarXiv:2303.12712,2023.
[6] VidhishaBalachandran,HannanehHajishirzi,WilliamCohen,andYuliaTsvetkov. Correcting
diverse factual errors in abstractive summarization via post-editing and language model
infilling. InProceedingsofthe2022ConferenceonEmpiricalMethodsinNaturalLanguage
Processing,pages9818–9830,2022.
[7] ZiweiJi,NayeonLee,RitaFrieske,TiezhengYu,DanSu,YanXu,EtsukoIshii,YeJinBang,
AndreaMadotto,andPascaleFung. Surveyofhallucinationinnaturallanguagegeneration.
ACMComputingSurveys,55(12):1–38,2023.
[8] Emilio Ferrara. Should chatgpt be biased? challenges and risks of bias in large language
models. ChallengesandRisksofBiasinLargeLanguageModels(October26,2023),2023.
[9] NicolaDeCao,WilkerAziz,andIvanTitov. Editingfactualknowledgeinlanguagemodels. In
Proceedingsofthe2021ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,
pages6491–6506,2021.
[10] TomHartvigsen,SwamiSankaranarayanan,HamidPalangi,YoonKim,andMarzyehGhas-
semi. Agingwithgrace: Lifelongmodeleditingwithdiscretekey-valueadaptors. Advancesin
NeuralInformationProcessingSystems,36,2023.
[11] Zeyu Huang, Yikang Shen, Xiaofeng Zhang, Jie Zhou, Wenge Rong, and Zhang Xiong.
Transformer-patcher:Onemistakeworthoneneuron.InTheEleventhInternationalConference
onLearningRepresentations,2023.
[12] AngelikiLazaridou,AdhiKuncoro,ElenaGribovskaya,DevangAgrawal,AdamLiska,Tayfun
Terzi,MaiGimenez,CypriendeMassond’Autume,TomasKocisky,SebastianRuder,etal.
Mindthegap: Assessingtemporalgeneralizationinneurallanguagemodels. Advancesin
NeuralInformationProcessingSystems,34:29348–29363,2021.
[13] HugoTouvron,LouisMartin,KevinStone,PeterAlbert,AmjadAlmahairi,YasmineBabaei,
NikolayBashlykov,SoumyaBatra,PrajjwalBhargava,ShrutiBhosale,etal. Llama2: Open
foundationandfine-tunedchatmodels. arXivpreprintarXiv:2307.09288,2023.
[14] YunzhiYao,PengWang,BozhongTian,SiyuanCheng,ZhouboLi,ShuminDeng,Huajun
Chen,andNingyuZhang. Editinglargelanguagemodels: Problems,methods,andopportu-
nities. InProceedingsofthe2023ConferenceonEmpiricalMethodsinNaturalLanguage
Processing,pages10222–10240,2023.
[15] ChenmienTan,GeZhang,andJieFu. Massiveeditingforlargelanguagemodelviameta
learning. InTheTwelfthInternationalConferenceonLearningRepresentations,2023.
11
[16] AntonSinitsin,VsevolodPlokhotnyuk,DmitriyV.Pyrkin,SergeiPopov,andArtemBabenko.
Editableneuralnetworks. CoRR,abs/2004.00345,2020.
[17] NicolaDeCao,WilkerAziz,andIvanTitov. Editingfactualknowledgeinlanguagemodels.
InMarie-FrancineMoens,XuanjingHuang,LuciaSpecia,andScottWen-tauYih,editors,
Proceedingsofthe2021ConferenceonEmpiricalMethodsinNaturalLanguageProcessing,
pages6491–6506,OnlineandPuntaCana,DominicanRepublic,November2021.Association
forComputationalLinguistics.
[18] KevinMeng,DavidBau,AlexAndonian,andYonatanBelinkov. Locatingandeditingfactual
associationsingpt. AdvancesinNeuralInformationProcessingSystems,35:17359–17372,
2022.
[19] KevinMeng,ArnabSenSharma,AlexJAndonian,YonatanBelinkov,andDavidBau. Mass-
editing memory in a transformer. In The Eleventh International Conference on Learning
Representations,2023.
[20] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins,
AndreiARusu,KieranMilan,JohnQuan,TiagoRamalho,AgnieszkaGrabska-Barwinska,
etal. Overcomingcatastrophicforgettinginneuralnetworks. Proceedingsofthenational
academyofsciences,114(13):3521–3526,2017.
[21] GeorgeAMiller,GalanterEugene,andKarlHPribram. Plansandthestructureofbehaviour.
InSystemsResearchforBehavioralScience,pages369–382.Routledge,2017.
[22] AlanBaddeley. Workingmemoryandlanguage: Anoverview. Journalofcommunication
disorders,36(3):189–208,2003.
[23] Keisuke Fukuda and Geoffrey F Woodman. Visual working memory buffers information
retrievedfromvisuallong-termmemory. ProceedingsoftheNationalAcademyofSciences,
114(20):5306–5311,2017.
[24] DaliangLi,AnkitSinghRawat,ManzilZaheer,XinWang,MichalLukasik,AndreasVeit,
FelixYu,andSanjivKumar. Largelanguagemodelswithcontrollableworkingmemory. In
Findings of the Association for Computational Linguistics: ACL 2023, pages 1774–1793,
2023.
[25] SangjunParkandJinYeongBak. Memoria: Hebbianmemoryarchitectureforhuman-like
sequentialprocessing. arXivpreprintarXiv:2310.03052,2023.
[26] Charles Packer, Vivian Fang, Shishir G Patil, Kevin Lin, Sarah Wooders, and Joseph E
Gonzalez. Memgpt: Towardsllmsasoperatingsystems. arXivpreprintarXiv:2310.08560,
2023.
[27] DaniYogatama,CypriendeMassond’Autume,andLingpengKong. Adaptivesemiparametric
languagemodels. TransactionsoftheAssociationforComputationalLinguistics,9:362–373,
2021.
[28] YuWang,XiusiChen,JingboShang,andJulianMcAuley.Memoryllm:Towardsself-updatable
largelanguagemodels. arXivpreprintarXiv:2402.04624,2024.
[29] JosephBHellige. Hemisphericasymmetry: What’srightandwhat’sleft,volume6. Harvard
UniversityPress,2001.
[30] RichardBIvryandLynnCRobertson. Thetwosidesofperception. MITpress,1998.
[31] EricMitchell,CharlesLin,AntoineBosselut,ChelseaFinn,andChristopherDManning. Fast
modeleditingatscale. InInternationalConferenceonLearningRepresentations,2022.
[32] Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D Manning, and Chelsea Finn.
Memory-basedmodeleditingatscale. InInternationalConferenceonMachineLearning,
pages15817–15831.PMLR,2022.
12
[33] MorGeva,RoeiSchuster,JonathanBerant,andOmerLevy. Transformerfeed-forwardlayers
are key-value memories. In Marie-Francine Moens, Xuanjing Huang, Lucia Specia, and
ScottWen-tauYih, editors, Proceedingsofthe2021ConferenceonEmpiricalMethodsin
NaturalLanguageProcessing,pages5484–5495,OnlineandPuntaCana,DominicanRepublic,
November2021.AssociationforComputationalLinguistics.
[34] JingchengNiu,AndrewLiu,ZiningZhu,andGeraldPenn. Whatdoestheknowledgeneuron
thesis have to do with knowledge? In The Twelfth International Conference on Learning
Representations,2024.
[35] GaneshJawahar,BenoîtSagot,andDjaméSeddah. WhatdoesBERTlearnaboutthestructure
oflanguage? InAnnaKorhonen,DavidTraum,andLluísMàrquez,editors,Proceedingsof
the57thAnnualMeetingoftheAssociationforComputationalLinguistics,pages3651–3657,
Florence,Italy,July2019.AssociationforComputationalLinguistics.
[36] YuliaOtmakhova,KarinVerspoor,andJeyHanLau. Cross-linguisticcomparisonoflinguistic
feature encoding in BERT models for typologically different languages. In Ekaterina Vy-
lomova, Edoardo Ponti, and Ryan Cotterell, editors, Proceedings of the 4th Workshop on
ResearchinComputationalLinguisticTypologyandMultilingualNLP,pages27–35,Seattle,
Washington,July2022.AssociationforComputationalLinguistics.
[37] IanTenney,DipanjanDas,andElliePavlick. BERTrediscoverstheclassicalNLPpipeline. In
AnnaKorhonen,DavidTraum,andLluísMàrquez,editors,Proceedingsofthe57thAnnual
MeetingoftheAssociationforComputationalLinguistics,pages4593–4601,Florence,Italy,
July2019.AssociationforComputationalLinguistics.
[38] Yung-SungChuang,YujiaXie,HongyinLuo,YoonKim,JamesR.Glass,andPengchengHe.
Dola: Decodingbycontrastinglayersimprovesfactualityinlargelanguagemodels. InThe
TwelfthInternationalConferenceonLearningRepresentations,2024.
[39] XinMen,MingyuXu,QingyuZhang,BingningWang,HongyuLin,YaojieLu,XianpeiHan,
andWeipengChen. Shortgpt: Layersinlargelanguagemodelsaremoreredundantthanyou
expect. arXivpreprintarXiv:2403.03853,2024.
[40] Tal Schuster, Adam Fisch, Jai Gupta, Mostafa Dehghani, Dara Bahri, Vinh Tran, Yi Tay,
and Donald Metzler. Confident adaptive language modeling. In S. Koyejo, S. Mohamed,
A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, Advances in Neural Information
ProcessingSystems,volume35,pages17456–17472.CurranAssociates,Inc.,2022.
[41] TingChen,SimonKornblith,MohammadNorouzi,andGeoffreyHinton. Asimpleframework
for contrastive learning of visual representations. In International conference on machine
learning,pages1597–1607.PMLR,2020.
[42] FlorianSchroff,DmitryKalenichenko,andJamesPhilbin. Facenet: Aunifiedembeddingfor
facerecognitionandclustering. InProceedingsoftheIEEEconferenceoncomputervision
andpatternrecognition,pages815–823,2015.
[43] ZeyuanAllen-ZhuandYuanzhiLi. Physicsoflanguagemodels: Part3.3,knowledgecapacity
scalinglaws. 2024.
[44] ZexiLi,ZhiqiLi,JieLin,TaoShen,TaoLin,andChaoWu. Training-timeneuronalignment
throughpermutationsubspaceforimprovinglinearmodeconnectivityandmodelfusion. arXiv
preprintarXiv:2402.01342,2024.
[45] PrateekYadav,DerekTam,LeshemChoshen,ColinARaffel,andMohitBansal.Ties-merging:
Resolvinginterferencewhenmergingmodels. AdvancesinNeuralInformationProcessing
Systems,36,2023.
[46] OmerLevy,MinjoonSeo,EunsolChoi,andLukeZettlemoyer. Zero-shotrelationextraction
viareadingcomprehension. InRogerLevyandLuciaSpecia,editors,Proceedingsofthe21st
ConferenceonComputationalNaturalLanguageLearning(CoNLL2017),pages333–342,
Vancouver,Canada,August2017.AssociationforComputationalLinguistics.
13
[47] Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh,
ChrisAlberti,DanielleEpstein,IlliaPolosukhin,JacobDevlin,KentonLee,KristinaToutanova,
Llion Jones, Matthew Kelcey, Ming-Wei Chang, Andrew M. Dai, Jakob Uszkoreit, Quoc
Le, and Slav Petrov. Natural questions: A benchmark for question answering research.
TransactionsoftheAssociationforComputationalLinguistics,7:452–466,2019.
[48] Potsawee Manakul, Adian Liusie, and Mark Gales. SelfCheckGPT: Zero-resource black-
boxhallucinationdetectionforgenerativelargelanguagemodels. InHoudaBouamor,Juan
Pino,andKalikaBali,editors,Proceedingsofthe2023ConferenceonEmpiricalMethodsin
NaturalLanguageProcessing,pages9004–9017,Singapore,December2023.Associationfor
ComputationalLinguistics.
[49] TogetherComputer. Redpajama: anopendatasetfortraininglargelanguagemodels. 2023.
[50] JohnHewitt,SarahChen,LanruoLoraXie,EdwardAdams,PercyLiang,andChristopherD.
Manning. Modeleditingwithcanonicalexamples,2024.
[51] LeoGao,StellaBiderman,SidBlack,LaurenceGolding,TravisHoppe,CharlesFoster,Jason
Phang,HoraceHe,AnishThite,NoaNabeshima,ShawnPresser,andConnorLeahy. Thepile:
An800gbdatasetofdiversetextforlanguagemodeling,2020.
[52] AlbertQ.Jiang,AlexandreSablayrolles,ArthurMensch,ChrisBamford,DevendraSingh
Chaplot,DiegodelasCasas,FlorianBressand,GiannaLengyel,GuillaumeLample,Lucile
Saulnier,LélioRenardLavaud,Marie-AnneLachaux,PierreStock,TevenLeScao,Thibaut
Lavril,ThomasWang,TimothéeLacroix,andWilliamElSayed. Mistral7b,2023.
[53] AlecRadford,KarthikNarasimhan,TimSalimans,andIlyaSutskever. Improvinglanguage
understandingbygenerativepre-training.
[54] BenWangandAranKomatsuzaki. GPT-J-6B:A6BillionParameterAutoregressiveLanguage
Model. https://github.com/kingoflolz/mesh-transformer-jax,May2021.
[55] NingyuZhang,YunzhiYao,BozhongTian,PengWang,ShuminDeng,MengruWang,Zekun
Xi,ShengyuMao,JintianZhang,YuanshengNi,etal. Acomprehensivestudyofknowledge
editingforlargelanguagemodels. arXivpreprintarXiv:2401.01286,2024.
[56] YonatanOren, ShioriSagawa, TatsunoriB.Hashimoto, andPercyLiang. Distributionally
robust language modeling. In Kentaro Inui, Jing Jiang, Vincent Ng, and Xiaojun Wan,
editors, Proceedings of the 2019 Conference on Empirical Methods in Natural Language
Processing and the 9th International Joint Conference on Natural Language Processing
(EMNLP-IJCNLP),pages4227–4237,HongKong,China,November2019.Associationfor
ComputationalLinguistics.
[57] AaronMueller,RobertFrank,TalLinzen,LuhengWang,andSebastianSchuster. Coloring
theblankslate: Pre-trainingimpartsahierarchicalinductivebiastosequence-to-sequence
models. InSmarandaMuresan,PreslavNakov,andAlineVillavicencio,editors,Findingsof
theAssociationforComputationalLinguistics: ACL2022,pages1352–1368,Dublin,Ireland,
May2022.AssociationforComputationalLinguistics.
[58] ShikharMurty,PratyushaSharma,JacobAndreas,andChristopherManning. Grokkingof
hierarchical structure in vanilla transformers. In Anna Rogers, Jordan Boyd-Graber, and
Naoaki Okazaki, editors, Proceedings of the 61st Annual Meeting of the Association for
ComputationalLinguistics(Volume2: ShortPapers),pages439–448,Toronto,Canada,July
2023.AssociationforComputationalLinguistics.
[59] EdwardJHu,PhillipWallis,ZeyuanAllen-Zhu,YuanzhiLi,SheanWang,LuWang,Weizhu
Chen,etal. Lora: Low-rankadaptationoflargelanguagemodels. InInternationalConference
onLearningRepresentations,2021.
[60] JasonWei,XuezhiWang,DaleSchuurmans,MaartenBosma,FeiXia,EdChi,QuocVLe,
DennyZhou,etal. Chain-of-thoughtpromptingelicitsreasoninginlargelanguagemodels.
Advancesinneuralinformationprocessingsystems,35:24824–24837,2022.
14
[61] OdedOvadia,MenachemBrief,MoshikMishaeli,andOrenElisha. Fine-tuningorretrieval?
comparingknowledgeinjectioninllms. arXivpreprintarXiv:2312.05934,2023.
[62] MariusMosbach,TiagoPimentel,ShauliRavfogel,DietrichKlakow,andYanaiElazar. Few-
shotfine-tuningvs.in-contextlearning: Afaircomparisonandevaluation. InFindingsofthe
AssociationforComputationalLinguistics: ACL2023,pages12284–12314,2023.
[63] YunLuo,ZhenYang,FandongMeng,YafuLi,JieZhou,andYueZhang. Anempiricalstudy
ofcatastrophicforgettinginlargelanguagemodelsduringcontinualfine-tuning.arXivpreprint
arXiv:2308.08747,2023.
[64] KushalTirumala,AramMarkosyan,LukeZettlemoyer,andArmenAghajanyan.Memorization
withoutoverfitting: Analyzingthetrainingdynamicsoflargelanguagemodels. Advancesin
NeuralInformationProcessingSystems,35:38274–38290,2022.
[65] DamaiDai,WenbinJiang,QingxiuDong,YajuanLyu,andZhifangSui. Neuralknowledge
bank for pretrained transformers. In Natural Language Processing and Chinese Comput-
ing: 12thNationalCCFConference, NLPCC2023, Foshan, China, October12–15, 2023,
Proceedings,PartII,page772–783,Berlin,Heidelberg,2023.Springer-Verlag.
[66] YuxinJiang,YufeiWang,ChuhanWu,WanjunZhong,XingshanZeng,JiahuiGao,Liangyou
Li, Xin Jiang, Lifeng Shang, Ruiming Tang, Qun Liu, and Wei Wang. Learning to edit:
Aligningllmswithknowledgeediting,2024.
[67] QizhouChen,TaolinZhang,XiaofengHe,DongyangLi,ChengyuWang,LongtaoHuang,and
HuiXue. Lifelongknowledgeeditingforllmswithretrieval-augmentedcontinuousprompt
learning,2024.
[68] CharlesGoddard,ShamaneSiriwardhana,MalikehEhghaghi,LukeMeyers,VladKarpukhin,
BrianBenedict,MarkMcQuade,andJacobSolawetz. Arcee’smergekit: Atoolkitformerging
largelanguagemodels. arXivpreprintarXiv:2403.13257,2024.
[69] WeishiLi,YongPeng,MiaoZhang,LiangDing,HanHu,andLiShen. Deepmodelfusion: A
survey. arXivpreprintarXiv:2309.15698,2023.
[70] SidakPalSinghandMartinJaggi. Modelfusionviaoptimaltransport. AdvancesinNeural
InformationProcessingSystems,33:22045–22055,2020.
[71] RahimEntezari,HanieSedghi,OlgaSaukh,andBehnamNeyshabur. Theroleofpermutation
invarianceinlinearmodeconnectivityofneuralnetworks. InInternationalConferenceon
LearningRepresentations,2022.
[72] SamuelAinsworth,JonathanHayase,andSiddharthaSrinivasa. Gitre-basin: Mergingmodels
modulo permutation symmetries. In The Eleventh International Conference on Learning
Representations,2023.
[73] MoritzImfeld,JacopoGraldi,MarcoGiordano,ThomasHofmann,SotirisAnagnostidis,and
SidakPalSingh. Transformerfusionwithoptimaltransport. InTheTwelfthInternational
ConferenceonLearningRepresentations,2024.
[74] ZexiLi,TaoLin,XinyiShang,andChaoWu. Revisitingweightedaggregationinfederated
learning with neural networks. In International Conference on Machine Learning, pages
19767–19788.PMLR,2023.
[75] HongyiWang,MikhailYurochkin,YuekaiSun,DimitrisPapailiopoulos,andYasamanKhaza-
eni. Federatedlearningwithmatchedaveraging. InInternationalConferenceonLearning
Representations,2020.
[76] GabrielIlharco,MarcoTulioRibeiro,MitchellWortsman,LudwigSchmidt,HannanehHa-
jishirzi,andAliFarhadi. Editingmodelswithtaskarithmetic. InTheEleventhInternational
ConferenceonLearningRepresentations,2023.
[77] Guillermo Ortiz-Jimenez, Alessandro Favero, and Pascal Frossard. Task arithmetic in the
tangent space: Improved editing of pre-trained models. Advances in Neural Information
ProcessingSystems,36,2024.
15
[78] GeorgeStoica,DanielBolya,JakobBrandtBjorner,PratikRamesh,TaylorHearn,andJudy
Hoffman. Zipit! merging models from different tasks without training. In The Twelfth
InternationalConferenceonLearningRepresentations,2024.
[79] ShacharDon-Yehiya,EladVenezian,ColinRaffel,NoamSlonim,andLeshemChoshen. Cold
fusion: Collaborativedescentfordistributedmultitaskfinetuning. InProceedingsofthe61st
AnnualMeetingoftheAssociationforComputationalLinguistics(Volume1: LongPapers),
pages788–806,2023.
[80] TomBrown,BenjaminMann,NickRyder,MelanieSubbiah,JaredDKaplan,PrafullaDhari-
wal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. Language
modelsarefew-shotlearners. Advancesinneuralinformationprocessingsystems,33:1877–
1901,2020.
[81] AlecRadford,JeffreyWu,RewonChild,DavidLuan,DarioAmodei,IlyaSutskever,etal.
Languagemodelsareunsupervisedmultitasklearners. OpenAIblog,1(8):9,2019.
[82] OpenAIandtheCo-authors. Gpt-4technicalreport,2024.
[83] DiederikKingmaandJimmyBa.Adam:Amethodforstochasticoptimization.InInternational
ConferenceonLearningRepresentations(ICLR),SanDiega,CA,USA,2015.
[84] OhadShamirandTongZhang. Stochasticgradientdescentfornon-smoothoptimization: Con-
vergenceresultsandoptimalaveragingschemes. InSanjoyDasguptaandDavidMcAllester,
editors,Proceedingsofthe30thInternationalConferenceonMachineLearning,volume28of
ProceedingsofMachineLearningResearch,pages71–79,Atlanta,Georgia,USA,17–19Jun
2013.PMLR.
[85] JacobDevlin,Ming-WeiChang,KentonLee,andKristinaToutanova. BERT:Pre-trainingof
deepbidirectionaltransformersforlanguageunderstanding. InJillBurstein,ChristyDoran,
and Thamar Solorio, editors, Proceedings of the 2019 Conference of the North American
ChapteroftheAssociationforComputationalLinguistics: HumanLanguageTechnologies,
Volume1(LongandShortPapers),pages4171–4186,Minneapolis,Minnesota,June2019.
AssociationforComputationalLinguistics.
[86] Nils Reimers and Iryna Gurevych. Sentence-BERT: Sentence embeddings using Siamese
BERT-networks. InKentaroInui,JingJiang,VincentNg,andXiaojunWan,editors,Proceed-
ingsofthe2019ConferenceonEmpiricalMethodsinNaturalLanguageProcessingandthe
9thInternationalJointConferenceonNaturalLanguageProcessing(EMNLP-IJCNLP),pages
3982–3992,HongKong,China,November2019.AssociationforComputationalLinguistics.
[87] Tianyu Gao, Xingcheng Yao, and Danqi Chen. SimCSE: Simple contrastive learning of
sentenceembeddings. InMarie-FrancineMoens,XuanjingHuang,LuciaSpecia,andScott
Wen-tauYih, editors, Proceedingsofthe2021ConferenceonEmpiricalMethodsinNatu-
ralLanguageProcessing,pages6894–6910,OnlineandPuntaCana,DominicanRepublic,
November2021.AssociationforComputationalLinguistics.
[88] ColinRaffel,NoamShazeer,AdamRoberts,KatherineLee,SharanNarang,MichaelMatena,
YanqiZhou,WeiLi,andPeterJ.Liu. Exploringthelimitsoftransferlearningwithaunified
text-to-texttransformer. JournalofMachineLearningResearch,21(140):1–67,2020.
[89] Tian Yu Liu, Matthew Trager, Alessandro Achille, Pramuditha Perera, Luca Zancato, and
StefanoSoatto. Meaningrepresentationsfromtrajectoriesinautoregressivemodels. InThe
TwelfthInternationalConferenceonLearningRepresentations,2024.
[90] Afra Feyza Akyürek, Ekin Akyürek, Derry Wijaya, and Jacob Andreas. Subspace regu-
larizers for few-shot class incremental learning. In International Conference on Learning
Representations,2022.
[91] Amirkeivan Mohtashami and Martin Jaggi. Landmark attention: Random-access infinite
contextlengthfortransformers. InWorkshoponEfficientSystemsforFoundationModels@
ICML2023,2023.
16
[92] TsendsurenMunkhdalai, ManaalFaruqui, andSiddharthGopal. Leavenocontextbehind:
Efficientinfinitecontexttransformerswithinfini-attention. arXivpreprintarXiv:2404.07143,
2024.
[93] MatthewSotoudehandAThakur. Correctingdeepneuralnetworkswithsmall,generalizing
patches. InWorkshoponsafetyandrobustnessindecisionmaking,2019.
[94] AnkitSinghRawat,ChenZhu,DaliangLi,FelixYu,ManzilZaheer,SanjivKumar,andSrinadh
Bhojanapalli. Modifyingmemoriesintransformermodels. InInternationalConferenceon
MachineLearning(ICML),volume2020,2021.
[95] ShuaiyiLi,YangDeng,DengCai,HongyuanLu,LiangChen,andWaiLam. Consecutive
modeleditingwithbatchalongsidehooklayers,2024.
[96] Ce Zheng, Lei Li, Qingxiu Dong, Yuxuan Fan, Zhiyong Wu, Jingjing Xu, and Baobao
Chang. Canweeditfactualknowledgebyin-contextlearning? InHoudaBouamor, Juan
Pino,andKalikaBali,editors,Proceedingsofthe2023ConferenceonEmpiricalMethodsin
NaturalLanguageProcessing,pages4862–4876,Singapore,December2023.Associationfor
ComputationalLinguistics.
[97] Baolong Bi, Shenghua Liu, Lingrui Mei, Yiwei Wang, Pengliang Ji, and Xueqi Cheng.
Decodingbycontrastingknowledge: Enhancingllms’confidenceoneditedfacts,2024.
[98] HaizhouShi,ZihaoXu,HengyiWang, WeiyiQin, WenyuanWang,YibinWang,andHao
Wang. Continuallearningoflargelanguagemodels: Acomprehensivesurvey,2024.
[99] Tongtong Wu, Linhao Luo, Yuan-Fang Li, Shirui Pan, Thuy-Trang Vu, and Gholamreza
Haffari. Continuallearningforlargelanguagemodels: Asurvey,2024.
[100] Matthias De Lange, Rahaf Aljundi, Marc Masana, Sarah Parisot, Xu Jia, Aleš Leonardis,
GregorySlabaugh,andTinneTuytelaars. Acontinuallearningsurvey: Defyingforgetting
in classification tasks. IEEE transactions on pattern analysis and machine intelligence,
44(7):3366–3385,2021.
[101] BillYuchenLin,SidaIWang,XiLin,RobinJia,LinXiao,XiangRen,andScottYih. On
continualmodelrefinementinout-of-distributiondatastreams. InProceedingsofthe60th
AnnualMeetingoftheAssociationforComputationalLinguistics(Volume1: LongPapers),
pages3128–3139,2022.
[102] David Rolnick, Arun Ahuja, Jonathan Schwarz, Timothy Lillicrap, and Gregory Wayne.
Experiencereplayforcontinuallearning. Advancesinneuralinformationprocessingsystems,
32,2019.
[103] RahafAljundi,EugeneBelilovsky,TinneTuytelaars,LaurentCharlin,MassimoCaccia,Min
Lin, and Lucas Page-Caccia. Online continual learning with maximal interfered retrieval.
Advancesinneuralinformationprocessingsystems,32,2019.
[104] Thomas Henn, Yasukazu Sakamoto, Clément Jacquet, Shunsuke Yoshizawa, Masamichi
Andou,StephenTchen,RyosukeSaga,HiroyukiIshihara,KatsuhikoShimizu,YingzhenLi,
et al. A principled approach to failure analysis and model repairment: Demonstration in
medicalimaging. InMedicalImageComputingandComputerAssistedIntervention–MICCAI
2021: 24thInternationalConference,Strasbourg,France,September27–October1,2021,
Proceedings,PartIII24,pages509–518.Springer,2021.
[105] Zhenhua Liu, Yunhe Wang, Kai Han, Wei Zhang, Siwei Ma, and Wen Gao. Post-training
quantization for vision transformer. Advances in Neural Information Processing Systems,
34:28092–28103,2021.
[106] AaronVanDenOord,OriolVinyals,etal. Neuraldiscreterepresentationlearning. Advances
inneuralinformationprocessingsystems,30,2017.
[107] ZifengWang,ZizhaoZhang,SaynaEbrahimi,RuoxiSun,HanZhang,Chen-YuLee,Xiaoqi
Ren,GuolongSu,VincentPerot,JenniferDy,etal. Dualprompt: Complementaryprompting
forrehearsal-freecontinuallearning. InEuropeanConferenceonComputerVision, pages
631–648.Springer,2022.
17
[108] ZifengWang,ZizhaoZhang,Chen-YuLee,HanZhang,RuoxiSun,XiaoqiRen,GuolongSu,
VincentPerot,JenniferDy,andTomasPfister. Learningtopromptforcontinuallearning. In
ProceedingsoftheIEEE/CVFConferenceonComputerVisionandPatternRecognition,pages
139–149,2022.
[109] LeeXiong,ChenyanXiong,YeLi,Kwok-FungTang,JialinLiu,PaulBennett,JunaidAhmed,
andArnoldOverwijk. Approximatenearestneighbornegativecontrastivelearningfordense
textretrieval. arXivpreprintarXiv:2007.00808,2020.
[110] FrederikTräuble,AnirudhGoyal,NasimRahaman,MichaelCurtisMozer,KenjiKawaguchi,
YoshuaBengio, andBernhardSchölkopf. Discretekey-valuebottleneck. InInternational
ConferenceonMachineLearning,pages34431–34455.PMLR,2023.
[111] YiDai,HaoLang,YinheZheng,FeiHuang,LuoSi,andYongbinLi. Lifelonglearningfor
questionansweringwithhierarchicalprompts. arXive-prints,pagesarXiv–2208,2022.
18
Appendix
IntheAppendix,weintroducemoredetailsalongwithadditionalexperimentalresults,discussions,
andrelatedworks:
• AppendixA:Experimentalsetups(cf. Section3).
• AppendixB:Moreexperimentalresults(cf. Section2and3).
• AppendixC:ProofoftheTheorem2.1(cf. Section2).
• AppendixD:Additionaldiscussionsandmorerelatedworks(cf. Section4).
A ImplementationDetails
A.1 DescriptionofDatasets
Table8: Boldedtextreferstotheeditlabelsy . Localityexamplex isanunrelatedquery.
e loc
(a) ZsRE, question-answering (b)Hallucinationeditingdatasetexample.Intheoriginaldata[10],there
editingdatasetexample. isnoparaphrasex e′ sothemeasurementofGen.metricisignoredhere.
x ,y Which continent x ,y ThisisaWikipediapassageaboutheinzchristianpander.
e e e e
is Berkner Island Heinz Christian Pander (1794 - 1865) was a German
in?SouthAmerica anatomistandembryologistwhowasborninRiga,Latvia.
HestudiedmedicineattheUniversityofDorpatandlater
x who gets the
loc attheUniversityofBerlin.In1820,hetookpartina
golden boot if its a
scientificexpeditiontoBokharaasanaturalist.
tie? shared
x Tiredandrestlessly,driftinginandoutofsleep. Hearing
x′,y Onwhichcontinent loc
e e crashingandbanging,thinkingtheroofwillcavein. Not
isBerknerIslandlo-
alertenoughtoquiteknowwhat itwas,Iyelledloudly
cated?SouthAmer-
forwhoeverwasmakingthosenoisesatsuchanhourto
ica
stop. Theyheardandlistened,I’mguessing
ZsRE The ZsRE question-answering task [46] is extensively studied within the model editing
literature [18, 19, 31, 15, 11], where each record contains an editing statement x , a paraphrase
e
prompt x′, and a locality prompt x . We use the same train/test split as [31] (163196/19086).
e loc
Notably,onlyMENDrequiresfittingahypernetworkonthetrainingset;othermethodsdiscardthe
trainingsetandperformeditsandevaluationsonthetestset. Inpractice,werandomlysample1K
and3KrecordsfromthetestsettoformtheeditsetsinSection3.2and3.3.
140
120
100
80
60
40
20
0
0 50 100 150 200 250 300 350 400
Halluc. Length Ranges
ycneuqerF
Hallucination WeutilizethesamedatasetasGRACE,
SelfCheckGPT[48],toassesstheabilityofModelEditors
tomitigatehallucinationsinautoregressiveLMs. Thisset-
tinginvolveseditinghighlyinaccuratesentences(sourced
from GPT-3 [80]) and replacing them with correspond-
ingsentencesfromactualWikipediaentries. Thisdataset
aligns moreclosely with real-world deployment scenar-
ioswheremodelstrigger"unexpectedbehaviors,"andthe
token length of edits is significantly longer than in past
datasets,makingitamorechallengingeditingsetting. Un-
likeGRACE,whichusedGPT2-XL(1.5B)[81],ourmain
experiments deploy larger LLMs, LLaMA and Mistral, Figure7: Hallucinationlengthstatistics.
bothwith7Bparameters,wemeasureretentionofpretrainingdata(x )fromthebasemodel: Red-
loc
Pajama[49],apublicversionofLLaMA’spretrainingdata. Someoftheexceptionallylongediting
samplescannotevenbeaccommodatedonanNVIDIAA800(80GB)duetoresourcelimitations.
AsshowninFigure7,theoriginaldatasetprovidedbyGRACE,aftertokenizationwithLLAMATO-
KENIZER,haslengthdistributionsrangingfrom[17,390]. ThedimensionofasingleMLPlayerin
llama-2-7b-hfis(11008,4096)§. Theoretically,fine-tuninganinputoflength390withdefault
§https://huggingface.co/meta-llama/Llama-2-7b-hf
19
Table9: TemporalOODdatasetexample. Boldedtextreferstotheeditlabelsy andy .
e ood
x ,y Self-drivingcars,alsoknownasautonomousvehicles,arevehiclesthatarecapable
e e
ofnavigatingandoperatingwithouthumanintervention. Theseinnovativevehicles
rely on a combination of advanced sensors, artificial intelligence, and computer
algorithmstointerprettheirenvironmentandmakereal-timedecisions. Withthe
potentialtosignificantlyimpactnumerousindustriesandsectors,self-drivingcars
havetheabilitytorevolutionizetransportationbyenhancingsafety,improvingtraffic
flow,andincreasingenergyefficiency. However,challengesrelatedtoregulatory
frameworks,ethicalconsiderations,andpublicacceptancestillneedtobeaddressed
beforewidespreadadoptionbecomesareality.
x Applehasanewpeachwiththereleaseofits3.0GHz,8-coreIntelXeon-basedMacPro.
loc
The 8-core Mac Pro is powered bu two quad-core Intel Xeon C¨lov ertownp¨rocessors
runningat3.0GHz. Applealsoreleasedaquad-coreMacProfeaturingtwoDual-Core
IntelXeonW¨ oodcrestp¨rocessors.
x ,y Self-driving cars, also known as autonomous cars or driverless cars, are vehicles
e ood
capableoftravelingwithouthumaninput. Thesecarsutilizearangeofsensors,
includingopticalandthermographiccameras,radar,lidar,ultrasound/sonar,GPS,
odometry, and inertial measurement units, to perceive their surroundings. By
interpreting sensory information, control systems in the car are able to create a
three-dimensional model of its environment. Using this model, the car can then
identifythebestnavigationpathanddevelopstrategiesformanagingtrafficcontrols
andobstacles. Asself-drivingcartechnologycontinuestoadvance,itisexpectedto
haveasignificantimpactonvariousfieldssuchastheautomotiveindustry,health,
welfare,urbanplanning,traffic,insurance,andthelabormarket. Theregulationof
autonomousvehiclesisalsobecominganincreasinglyimportanttopicofdiscussion.
fullprecisionandtheAdamoptimizerwouldrequire(390+4+4+4)*(11008*4096*4)+4*7B=
100.36GBofVRAM(foractivations,gradients,first-order,andsecond-orderoptimizers),exceeding
thememorycapacityoftheNVIDIAA800. Consequently,weexcludedexcessivelylongsamples
(limitingtokenizedlengthsto254)andultimatelyretained906editinginstances(comparedto1392
inGRACE).TofacilitateafaircomparisonwithMEND,wespecificallyallocatedatrainingsetfor
MEND,withafinaltrain/testsplitof306/600. Allmethodswereeditedandevaluatedonthetestset.
Temporal [50]sourcestheprefixx fromthefirstparagraphofanentity’sWikipediapageand
e
samplesaparagraphy discussedbyGPT-4[82]abouttheemergingentityx ,whichisusuallynoisy
e e
butmaycontainhelpfulinformation. ThesearepresentedaseditingpromptstoModelEditors. For
out-of-distribution(OOD)generalizationtocomplexnaturalcontexts(notfitted),y istakenfrom
ood
theactualWikipediasuffixofx . ThissetupisutilizedtoevaluatetheOODgeneralizationofModel
e
Editorscenteredaroundasinglecanonicalexample. Consistentwithpreviouswork[10],theout-of-
scopedatax isderivedfromthePile[51],thepretrainingcorpusofGPT-J-6B.Examplesfromthe
loc
datasetcanbeseeninTable9. TomeasuretheOODgeneralizationofeditingmethodsforemerging
entities,weperformmodeleditingusingstandardizedsimpleexamplesandthenevaluatethisbehavior
onmorecomplexinstances. Following[50],inanaturalsetting,nosinglecorrectcontinuationexists.
Thus,wealsouseprobabilitythreshold-basedevaluations,suchas80%,wheretheeditingsuccessrate
evaluateswhetherthelossL foranexamplefallsbelowδ =−log(0.8),asindicatedinthefor-
xe,yood
mulabelow. Theintuitionbehindthisisthatmanyotherplausiblealternativecontinuationsmayexist.
T
1 (cid:88)
OODGen.= 1{(L (x ,y )<δ)}. (10)
T ΘT e ood
t=1
A.2 DescriptionsofComparedModelEditors
FT-L. AllotherlayersoftheLLMsremainfrozen,andonlyasingleMLPlayerisfine-tunedthrough
autoregressiveloss[18]. Additionally,weimposeanL normconstrainttopreventtheparameters
∞
fromdeviatingtoofarfromthepretraineddistribution.
FT-EWC. ElasticWeightConsolidation(EWC)hasbeendemonstratedtomitigatecatastrophic
forgettingbyupdatingweightsusingaFisherinformationmatrix,whichiscomputedfrompastedits,
20
multipliedbyascalingfactorλ[20]. Following[10],weomittheconstraintsoftheL norminthis
∞
implementation.
MEND. MEND[31]transformsthegradientsobtainedfromstandardfine-tuningusingahyper-
networkthatconvertsgradientsdecomposedintolowrank(rank=1)intonewgradients,whichare
thenappliedtothetargetlayerforparameterupdates. Duringthetrainingphase,asmallauxiliary
hypernetwork receives editing examples (x ,y ), and x . MEND’s training loss comprises the
e e loc
standardautoregressivelosscombinedwiththeKLdivergencelossofthemodel’soutputonx
loc
beforeandafterediting. Thishypernetworkplaysacrucialroleduringtheeditingprocedure.
ROME. ROME [18] uses causal analysis to pinpoint knowledge within specific MLP layers
and modifiesthe entirematrix throughleast squares approximation. Itoperates under thestrong
assumptionthattheMLPistheprimarymoduleforstoringknowledge[33],anditinjectsasingle
pieceofknowledgeintotheMLPateachiterationusingaLagrangianremainder.
MEMIT. Similarly,basedontheassumptionthattheFFNservesasaknowledgekey-valuestore,
MEMIT[19]manipulatesparametersofspecificlayersdirectlythroughleastsquaresapproximation.
Unlike ROME, which updates a single layer, MEMIT is a multi-layer updating algorithm that
supports simultaneous updates of hundreds or thousands of facts. For sequential model editing
tasks, MEMITrequiresimmediateon-the-flyrepairswhenthemodelmakeserrors, expressedas
f =MEMIT(f ,x ,y ),involvingmultipleoperationsontheoriginalmodel.
ΘT ΘT−1 T T
MEMIT-MASS. Unlikesequentialediting,MEMITsupportsmodificationofmultipleknowledge
fragmentsinabatchmode,namedMEMIT-MASS.Supposewecollectstreamingerrorsas(X,Y)=
{(x ,y ),(x ,y ),...,(x ,y )}andinjectthemcollectivelyintotheMLP,itonlyinvolvesasingle
0 0 1 1 T T
editing operation on the original model as f = MEMIT(f ,X,Y). Although this approach
ΘT Θ0
losesthecapabilityforon-the-flyrepairs,westillincludethisbaselineinourexperiments.
DEFER. In GRACE, a reimplementation of SERAC [32] is utilized, denoted as DEFER. For
new inputs, DEFER includes a network g (corresponding to the scope classifier in SERAC) that
predictswhetherto: 1)trustthepredictionoftheLLMs,or2)trustthepredictionofthenewmodel.
Here, the new model is configured as a single-layer linear network o with a sigmoid activation
function,correspondingtothecounterfactualmodelinSERAC.Duringtheeditingprocess,gando
arefine-tunedjointly.
GRACE. GRACE [10] utilizes a discrete KEY-VALUE codebook and maintains the codebook
throughouttheeditingflowbyadding,expanding,andsplittingKEYs. Duringtheinferencephase,it
retrievesthenearestKEYanddetermineswhethertoreplacetheactivationofthehiddenlayeroutput.
A.3 TrainingDetailsandHyperparameters
Except for MEMIT-MASS, the batch size for all methods is consistently 1 in sequential editing
scenarios. Allexperimentsareconductedusing3NVIDIAA800GPUs,withalltasksreproducible
onasingleA800. EditingZsREtakesapproximately4hours,whileHallucinationrequiresaround6
hours. Toensurefaircomparisons,unlessotherwisespecified(forsomemethodslikeMEND,ROME,
andMEMIT,wefollowtheoriginalliteraturebyselectingthelastfewlayersorusingcausalanalysis
toidentifythetargetlayers),thedefaulttargetlayersforeditingonLLaMA,Mistral,andGPT-Jare
model.layers[27].mlp.down_proj.weight, model.layers[27].mlp.down_proj.weight,
andtransformer.h[21].mlp.c_fc,respectively.
ForFT-L,weutilizeareimplementationfromROME¶,employingtheAdam[83]optimizerwith
consideration of learning rates at 1e-5, 1e-4, and 5e-4, and conducting gradient descents for 50
iterations,ultimatelyreportingthebestresultsatalearningrateof5e-4.
ForFT-EWC,wefollowthereimplementationinGRACEanditsdefaultsettings,settingthelearning
rateat1e-2,theλ penaltyfactorat0.1,andthenumberofreplayinstancesat10.
ewc
ForthetrainingphaseofMEND,weadheretotheoriginalpaper,settingthelearningrateat1e-4,
iterating100Ktimes,andemployingearlystoppingat30K,ultimatelyachievinganaccuracyof0.95
onthetrainingset. Notably,wetargetthelastfewMLPlayersaspertheoriginalliterature,such
as model.layers[i].mlp.down_proj.weight, model.layers[i].mlp.gate_proj.weight,
model.layers[i].mlp.up_proj.weightinLLaMA,wherei∈[29,30,31].
ForROMEandMEMIT,wefollowtheoriginalliteratureonGPT-Jusingthedefaultconfigurations,
specificallythefifthlayerandlayers[3,4,5,6,7,8]. InLLaMAandMistral,additionalcausalanalysis
isconductedtopinpointthelayersstoringknowledge. AsshowninFigure8,anincreasingtrendin
¶https://github.com/kmeng01/rome
21
40%
20%
0%
0 5 10 15 20 25 30
LlaMA-2-7B Layer at which the single hidden state is restored
tceffE
tceridnI
egarevA
Causal effect of states at the early site with Attn or MLP modules severed
40.0%
Effect of single state on P
Effect with Attn severed 30.0% Effect with MLP severed
20.0%
10.0%
0.0%
0 5 10 15 20 25 30
Mistral-7B Layer at which the single hidden state is restored
tceffE
tceridnI
egarevA
Causal effect of states at the early site with Attn or MLP modules severed
Effect of single state on P
Effect with Attn severed Effect with MLP severed
Figure8: Mid-layerMLPsplayacrucialmediatingroleinLLaMA-2-7BandMistral-7B.
1.0
0.8
0.6
0.4
0.2
0.0
1 10 100 1000
Number of Continual Edits
ytilibaileR
1.0
0.8
0.6
0.4
0.2
0.0
1 10 100 1000
Number of Continual Edits
noitazilareneG
1.0
0.8
0.6
0.4
0.2
0.0
1 10 100 1000
Number of Continual Edits
ytilacoL
1.0
0.8
0.6
0.4
0.2
0.0
1 10 100 1000
Number of Continual Edits
egarevA
FT-EWC
MEND
ROME
MEMIT-MASS
DEFER
GRACE
WISE (ours)
Figure9: GPT-J-6B,ZsRE,continualediting.
theAverageIndirectEffectoftheMLPisobservedacrosslayers[4,5,6,7,8],suggestingthatthemodel
recallsfactualknowledgehereandpassesthematuredtokendistributionviaresidualconnectionsto
thelastMLP.Thus,inLLaMAandMistral,ROMEeditsthefifthlayer,whileMEMITeditslayers
[4,5,6,7,8].
ForDEFER,theoriginalliteratureusesalearningrateof1.0; Table10: WISEhyper-parameters
however,wefounditunfitforLLaMAandMistral,withsevere duringeditingandmerging.
fluctuations in model loss. Therefore, we experiment with
learning rates of 7e-5, 7e-4, and 1e-3, and ultimately report
Hyper-Parameters Values
using7e-5(optimal).
ForGRACE,westrictlyfollowtheoriginalliterature,setting Optimizer SGD
thelearningrateat1.0,andusingreplace_lasttoonlyre- LRη 1.0
placetheactivationofthelasttokeninautoregressivescenarios.
MaskRatioρ 0.2
After observing failures in generalization, we adjust various
α 5.0
ϵ valuesanddiscussthismoreinAppendixB.1.
init β 20.0
ForWISE,thehyperparametersfortheQAandHallucination
γ 10.0
tasks are identical. We find that a learning rate of 1.0 with
the SGD [84] optimizer is a good approach for stable train- MergeWeightsλ 0.5
ing. Thehyperparametersdesignedintheknowledgeediting
Knowledgeshardsk 2
phaseincludetherandommaskingprobabilityρandtherouting
thresholdguidanceα,β,γ. Intheknowledgemergingphase,hyperparametersincludethenumberof
mergeskandthemergingweightsλforeachMLP(wediscusstheimpactofρandkinSection3.3).
Theoretically,astheimportanceofknowledgeinanyMLPisconsiderable,wealwaysaveragewith
λ=1/kacrossallexperiments. TheseareshowninTable10.
A.4 PseudoCodeofWISE
Thepseudo-codeoftheWISEeditingstageisinAlgorithm1,andtheoneoftheWISEinference
stageisAlgorithm2.
B MoreExperimentalResultsandAnalyses
B.1 OnthePitfallofGRACE:GeneralizationCollapsesinDecoder-onlyLLMs
Here,wediscusswhyGRACEexhibitspoorgeneralizationwheneditingdecoder-onlyLMs.
AsshowninFigure10,wecontinuouslyedit15samples(x ,y )usingGRACEandobservethe
e e
nearestcodebookKeyfortheirparaphrasesx andunrelatedqueriesx ,aswellasthegoverned
e′ loc
DeferralradiiϵofthoseKeys. WhenoverlappingKeysexist,GRACEreducestheDeferralradiito
splitthisKeysandthenaddsanewcodebookentry,resultinginexponentiallydecayingofradiiϵ
duringtheeditingprocess. Thoughϵisinitializedfromahighϵ ,itwillbesmallandineffective
init
aftercontinuousedits. FromFigure10,weobservethatGRACEismorelikelytohaveaconservative
22
Algorithm1:WISEEditingStage
Input: TheinitialLLMmodelf ,thetargetedFFNlayer,theeditdatasetD whose
Θ0 edit
lengthisT,theirrelevantdatasetD ,thesubspacemaskratioρ,thenumberofsubspacesk,
irr
whetherWISE-Retrieve.
Output: ThefinalLLMmodelf afterT edits.
ΘT
1: GeneratekrandommasksM i ,i∈[k]ofratioρ;ifWISE-Retrieve,copythesidememory
severaltimes;
2: foreachedit(x t ,y t )∈D edit ,t∈[T]do
3: Edit(x t ,y t )inthecorrespondingmemorysubspacebyL edit =−logP W v′ (y t |x t )+L a ;
4: Updatetheactivationthreshold: ϵ=min(ϵ,∆ act (x t ));
5: ifAlltheksubspacesofasidememoryarefullthen
6: UseTies-MergeinEquation8toupdatethefinalsidememory;
7: ifWISE-Retrievethen
8: MovetoanothercopyofsidememoryW v′ ;
9: endif
10: else
11: ifCurrentsubspaceM i isfullthen
12: MovetoanothersubspaceofsidememoryM i+1 ;
13: endif
14: endif
15: endfor
16: returnObtainthefinalLLMmodelf ΘT .
Algorithm2:WISEInferenceStage
Input: TheeditedLLMmodelf ,theactivationthresholdϵ,thetestdatasetD ,whether
ΘT test
WISE-Retrieve.
Output: Themodel’soutput.
1: foreachqueryx i ∈D test do
2: ifWISE-Retrievethen
3: Getthevalueofactivation∆ act =∥A(x i )·(W v′ −W v )∥ 2 foreachsidememoryand
selecttheonewiththemaximalvalueof∆ ;
act
4: else
5: Getthevalueofactivation∆ act =∥A(x i )·(W v′ −W v )∥ 2 ;
6: endif
7: if∆ >ϵthen
act
8: UsethesidememoryW v′ togeneratetheoutputasinEquation6;
9: else
10: UsethemainmemoryW v togeneratetheoutputasinEquation6.
11: endif
12: endfor
strategythatsetssmallerDeferralradiiduringediting. SmallerDeferralradiiwillcausex tofail
e′
to hit the codebook (the distance to the nearest Key is farther than its Deferral radii) but let x
loc
successfullyfarawayfromtheradii,resultinglowgeneralizationandhighlocality. Also,weobserve
thattheDeferralradiimethodisnoteffectiveunderanyϵ ;foralltestedϵ valuesof1.0,3.0,10.0,
init init
and500.0,theyallhavelowgeneralizationandhighlocality.
ThissuggeststhatinautoregressiveLMs,thedistributionofthelasttokencannoteffectivelyrepresent
semantics; whereasinencoder-onlyandencoder-decoderarchitectures,capturingsemanticinfor-
mationthroughvectorrepresentationhasbeenextensivelystudied[85–87]. Thisisconsistentwith
thedegreeofgeneralizationshownbyGRACEwhenanchoringtheT5[88]Encoderlayer. Some
relatedworks[89]alsoindicatethatinautoregressivemodels,semanticsimilaritymeasuresbased
onaveragesofoutputtokensunderperform,recommendingtheuseofscoredistributionsovertext
continuationstorepresentsemanticdistances.
B.2 ImpactofKnowledgeMergingStrategiesforWISE
23
20
10
0
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
ecnatsiD
2L
init = 1.
Dist(xe0, Its Nearest Key k1) Dist(xloc, Its Nearest Key k2)
k1 : defferal radius of k1 k2 : defferal radius of k2
20
10
0
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
ecnatsiD
2L
init = 3.
Dist(xe0, Its Nearest Key k1) Dist(xloc, Its Nearest Key k2)
k1 : defferal radius of k1 k2 : defferal radius of k2
20
10
0
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
ecnatsiD
2L
init = 10.
Dist(xe0, Its Nearest Key k1) Dist(xloc, Its Nearest Key k2)
k1 : defferal radius of k1 k2 : defferal radius of k2
20
10
0
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14
ecnatsiD
2L
init = 500.
Dist(xe0, Its Nearest Key k1) Dist(xloc, Its Nearest Key k2)
k1 : defferal radius of k1 k2 : defferal radius of k2
Figure 10: Investigation on the query x and its distance to the nearest Key k, as well as the
deferralradiusϵofthatKey. RedandBluerespectivelyrepresenttheparaphrasequeryx andthe
e′
unrelatedqueryx ,withthehatchrepresentingtheradiusofthenearestKey. Weobservethatwhen
loc
conflictsoccur(hitthecodebookKeybutwithdifferentEditTargety ),thedeferralradiusϵdecays
e
exponentially. ThisresultsinGRACEbeingunabletoencompasstheparaphrasex andmaintain
e′
highlocality,regardlessofhowϵ isadjusted. ZsRE,LLaMA-2-7B.
init
Here,weconductamorein-depthstudyoftheknowledgemerging Table11:VaryingMergingStrat-
strategiesforWISE,exploringvariousmergingapproachesincluding egy.ZsRE.LLaMA-2-7B.
(i)Linear,whichusesasimpleweightedaverage;(ii)Slerp,which
sphericallyinterpolatestheparametersoftwomodels;(iii)Ties,a Methods Rel. Gen. Loc. Avg.
componentusedinthemainexperimentsofthispaperthatresolves Linear .63 .61 .93 .72
merging disturbances through TRIM ELECT SIGN; (iv) Dare: Slerp .62 .64 .91 .72
whichfollowsaBernoullidistributiontodeleteredundantparame- Dare .68 .63 .92 .74
Dare_Ties .67 .63 .83 .71
tersandrescaletheremainingones;(v)Dare_Ties,whichcombines
Ties .85 .81 .94 .87
dareandthesignconsensusalgorithmofTIES;and(vi)Sign, an Sign .80 .76 .97 .84
ablationcomponentofTiesthataddressesdirectionalconflicts—all
utilizing the official implementation from MergeKit [68] ||. We randomly sample 100 edits from
ZsRE, retaining a fine-tuned MLP every 50 edits (merging 2 MLPs). As shown in Table 11, we
||https://github.com/arcee-ai/mergekit
24
observethatignoringthedirectionofparameterupdates(Linear,Slerp,Dare)leadstoasignificant
declineineditingperformance,underscoringtheimportanceofaddressingknowledgeconflictsin
overlappingparameters. ThesuccessofSignalsoreaffirmsthispoint. Meanwhile,therandomly
maskedknowledgeshardsexhibitanon-redundancy, indivisiblenature. Thisisdemonstratedby
thesignificantlyweakerperformanceofDare_TiescomparedtoTies/Sign,indicatingthatremoving
parameterupdatescanleadtothelossofeditedknowledgeorevenpotential"anchors".
B.3 AnalysisofRetrievingTop-1Activation
Edit Success (ES.) % Routing Success (prec@1) %
80 100
60 80
60
40
40
WISE Retrieve
20
WISE Retrieveoracle 20 WISE Retrieve
WISE Retrieve w. Lmemo WISE Retrieve w. Lmemo
0 0
1000 2000 3000 1000 2000 3000
(a) AverageofRel.andGen. (b) RetrievalAcc.byTop-1Activation
Figure 11: Comparing editing results of WISE-{Retrieve, Retrieve , Retrieve w.
oracle
L } when varying T. (a) shows the simple average of Rel. and Gen. (ES.), while (b) shows
memo
retrievalaccuracy,i.e.,whethertheTop-1ActivationroutestothecorrectMLP(prec@1). X-axis:
Numedits. ZsRE.LlaMA-2-7B.
WISE-Retrieveretainseachknowledge-shardingmemoryandretrievesthroughTop-1Activation.
However,asshowninTable6andFigure11b,theretrievalaccuracystillhassignificantroomfor
improvement;specifically,whenT reaches3K,theaccuracyofroutingtothecorrectMLPdropsto
around60%,indicatingthespecificitybetweensidememoriesisinsufficient. Onepossiblereasonis
thatwhensamplingtheeditsfromasingledataset(ZsRE),theeditinginstances(x ,y )allbelong
e e
tothesamedomain. Thisleadstosomeverysimilarinstancesbeingcapturedbymultipleexpertside
memories(resultinginhighactivationsforallsidememories),introducingmoreretrievalfailures.
Therefore,toimprovethespecificityofsidememoryandreducetheprobabilityofroutingerrors,
weattempttoaddanewconstraintL toEquation5. Forknowledge-shardingmemoryW ,we
memo i
randomlyreplayinstances(x ,y )fromtheeditsetD ofpastshardW ,ensuringthat
m m Wj j,j∈[0,i−1]
W remainsinactiveforx :
i m
L′ =L +max(0,∆ (x )−α), s.t.x ∈D .
a a act m m Wj
(cid:124) (cid:123)(cid:122) (cid:125)
Lmemo
AsshowninFigure11b,thisreplaybehaviorincreasesthespecificitybetweensidememories,main-
tainingnearly88%retrievalaccuracyatT =3K. Figure11aalsoshowsthatWISE-Retrievew.
L improvesEditSuccess(ES.)by8.39%comparedtoWISE-Retrieve,providingapromising
memo
directionforfuturework. Withfiner-grainedactivationmanagement,wemightbeabletobridgethe
performancegapbetweenRetrieveandOracle.
B.4 CaseStudy
InTable12,wepresentbadcasesofusingWISEtoedittheLLaMA-2-7BontheZsREdatasetand
mitigatingthesefailuresiscriticalforfutureworkinmodelediting. Weobservethatini)errorsoccur
onlyinpartofthetokens,andtheseerrorsconstitutealargeproportionofthebadcases,indicating
thattheeditshavenotbeensufficientlyfitted. ii)displayscaseswheretheentireoutputisincorrect,
andfactualfailuresindicatedifficultiesinretainingmemoryofparametersforsomerareentities
(suchasPersianiia,iib). iv)presentscasesofgeneralizationfailure,forexampleinivd),where
themodelanswered“English”butdidnotfullyfollowthegroundtruth,indicatingsignificantroom
forimprovementintheaccuracyofgeneralizededits. Meanwhile,iniii)wesurprisinglyfindthat
evenwhenWISEerrsontheEditPrompt, itcancorrectlyansweritsparaphraseiiib)“Thekind
25
Table12:
FailurecasesofusingWISEtoeditLLaMA-2-7B.✔✗
representserrorsinpartofthetokens,
✗representscompleteoutputerrors(i.e.,factualfailures),and✓indicatestheexpectedexactmatch.
Prompt EditTarget Post-EditOutput
ia) BywhichpersonLahtiTownHallhasbeendesigned? AkiKaurismäki WimeKaurismäki✔✗
ib) WhichisthearchitectofLahtiTownHall? - WimeKaurismäki✔✗
ic) WhichcorporationwasUSSLeedstown(APA-56) Lockheed LeezShipbuilding✔✗
createdby? Shipbuilding
id) WhichcompanymanufacturestheUSSLeedstown - LeezShipbuilding✔✗
(APA-56)?
iia) WhichlanguageisGarowePrincipleswrittenin? Persian Dutchian✗
iib) Inwhatlanguagedoesthemonthlyfootballmagazine - Somian✗
GarowePrinciplesreport?
iic) WhatyearwastheserviceentrydateforPanzer58? 1957 1953✗
iid) WhatwastheyearPanzer58wascommissioned? - 1953✗
iiia)WhatwasGemmaBosini’srange? mezzo-srano Wzo-srano✗
iiib)ThekindofvoiceofGemmaBosiniiswhat? - mezzo-srano✓
iva) InwhichstateisQalehLanlocated? GolestanProvince GolestanProvince✓
ivb) WhatstateisQalehLanin? - LestanProvince✗
ivc) InwhichlanguageGarowePrinciplesmonthly AmericanEnglish AmericanEnglish✓
footballmagazinereporting?
ivd) WhatlanguageareGarowePrincipleswrittenin? - EnglishEnglish✗
ofvoiceofGemmaBosiniiswhat?”. ThisindicatesthatWISEcanhandlecontextualinformation
correctlyinsomecasesbutfallsshortinspecificeditinginstructions, suggestingthatoptimizing
editinginstructions(modifyingtheeditingcontext)maybeadirectionforimprovement.
B.5 ImportanceofKnowledgeAnchorWhenMergingModels
Table13: AnalysisofMergingw.o. andw. Here,wediscusstheeffectsofindependent(ensuredby
"knowledgeanchor"(KA).T =1000.ZsRE. non-overlappingmasks)vspartiallyoverlappingparam-
LLaMA-2-7B. eterswithinMLPsubspacesoneditingperformance,as
shown in Table 13. It is observable that, despite vary-
w.o.KA w.KA
ρ/k ingmaskratiosρandthenumberofsubspacesk,partial
Rel. Gen. Loc. Avg. Rel. Gen. Loc. Avg.
overlap (w. KA) consistently outperforms independent
2/0.30 0.76 0.72 1.00 0.83 0.79 0.73 1.00 0.84
configurations (w.o. KA) in terms of Reliability (Rel.)
2/0.50 0.74 0.73 1.00 0.82 0.77 0.72 1.00 0.83
3/0.33 0.72 0.68 1.00 0.80 0.75 0.71 1.00 0.82 andGeneralization(Gen.). Forexample,atρ/kof5/0.20,
5/0.20 0.64 0.61 1.00 0.75 0.73 0.68 1.00 0.80 thereisarelativeimprovementof9%and7%respectively.
Thisdemonstratesthattheoverlappingregionscontributeas“anchors”forknowledgefusion,facilitat-
inginformationtransferacrossdifferentsubspaces.Moreover,thesharedparametersprovideanatural
regularization[90]mechanism,helpingsynchronizemodelbehavioracrossdifferentsubspaces.
B.6 AblationStudyofRandomPrefixToken
1.0
0.8
0.6
0.4
0.2
0.0
1 10 100 1000
T: Num Edits
ssecuS
gnitidE
Effect of Random Prefix Token (PT)
Rel (w.o. PT) Gen (w.o. PT) Rel (w. PT) Gen (w. PT)
Figure12: AblationstudiesonRandomPrefixToken(PT)ofWISE.Light/Darkcolorsindicate
theEditingSucessw.o./w. PTaddition. ZsRE.LlaMA-2-7B
26
As described in Section 3.1, we employ random prefix token augmentation to enable the editing
knowledgetocopewithvariouscontexts. Thatis,forasinglex ,itexpandsinto(prefix ,x ). The
e i e
prefix is derived from tokens that are randomly generated by the original LM f , serving as an
Θ
economicaldataaugmentationmethod. Weobservethattheeditingsuccessrateiscompromised
(Figure 12). Specifically, for instance, at T=1000, Rel. and Gen. decreased by 0.15 and 0.17,
respectively. Byutilizingrandomlygeneratedprefixtokens,themodelisabletolearnabroaderrange
oflinguisticfeatures,therebyexhibitinggreaterrobustnessinpracticalapplications. Webelievethat
accesstothe"datagenerator"candeepenthemodel’smemoryofeditingsamples.
B.7 ParameterEfficiency
1.30
1.25
1.20
1.15
1.10
1.05
1.00
0.95
0 500 1000 1500 2000 2500 3000
)x0.1(
noitpmusnoC
UPG
The key to lifelong model editing is maintaining con- w/o Editing
WISE Merge stantorslowlyincreasingcomputationalcostsasthenum- WISE Retrieve
ber of edits expands. Here, we provide a quantitative
analysisusingLLaMA-2-7Basanexample. Supposewe
selectmodel.layers[27].mlp.down_proj.weightas
sidememory. Inthatcase,thetheoreticallyaddedparame-
tersare11008×4096×4=0.18GB,whichaccountsfor Figure13: Computationalcosts.
0.64%oftheoriginalLLaMA’s7B×4=28GB(ignoringtheVRAMrequiredforinputactivations).
AsshowninFigure13,inpractice,WISE-MergeincreasesVRAMby4%comparedtotheoriginal
LLaMAandremainsconstantovertime. WISE-Retrieve,insteadofmerging,usesretrievalrouting,
meaning the computational cost increases over time, but this increase is gradual and can easily
handle thousands or tens of thousands of inputs. Additionally, if we partially merge side MLPs
(combiningWISE-RetrieveandWISE-Merge),wecanfurtherreducethecomputationaldemandsof
WISE-Retrieve.
C ProofofTheorem2.1
TheoremC.1 Subspace Overlap. Generate k memory subspaces Wi ,i ∈ [k] by random mask
v′
with1’sratioρ,soeachmemoryhasρ·|W |activetrainedparameters. Foranytwosubspaces
v′
Wi andWj i̸=j;i,j ∈[k],thereareρ2·|W |activeparametersthatareoverlapped. Forallk
v′ v′ v′
subspaces,thereareρk·|W |overlappedactiveparameters.
v′
Proof: WeaimtoprovetheSubspaceOverlaptheorembyinduction.
LetWi representthei-thmemorysubspacegeneratedbyarandommaskwithasparsityratioofρ,
v′
wherei∈[k]. EachmemorysubspaceWi containsρ·|W |activetrainedparameters.
v′ v′
Westartbyconsideringthecaseoftwomemorysubspaces,Wi andWj ,wherei̸=jandi,j ∈[k].
v′ v′
LetP(parametersampled)=ρbetheprobabilitythataparameterissampledinonemaskgeneration
event.
1. Forasinglemaskgeneration,theprobabilitythataspecificparameterissampledisρ. We
denotethisprobabilityasP(sampled)=ρ.
2. Consideringtwoindependentmaskgenerationevents,theprobabilitythatthesameparameter
issampledinbothmasksistheproductoftheirindividualprobabilities,i.e.,ρ2. Thisis
derivedfromtheindependenceoftheevents. Mathematically:
P(sampledinbothmasks)=P(sampled)×P(sampled)=ρ×ρ=ρ2.
3. Extendingthislogic,forkindependentmaskgenerationevents,theprobabilitythataspecific
parameterissampledinallkmasksisρk. Mathematically:
P(sampledinallkmasks)=P(sampled)×P(sampled)×···×P(sampled)=ρk.
(cid:124) (cid:123)(cid:122) (cid:125)
ktimes
Now,let’scalculatethenumberofparametersoverlappedintworandommasks:
ThetotalnumberofparametersinW is|W |.
v′ v′
Thus,thenumberofparametersoverlappedintworandommasks,Wi andWj ,isρ2·|W |.
v′ v′ v′
Extendingthistokrandommasks,thenumberofparametersoverlappedinallkmasksisρk·|W |.
v′
Thisconcludestheproof.
□
27
D DetailedRelatedWorks
MemoryandKnowledgeInjectionofLLMs ThememoriesofLLMscanbedividedintolong-
term(episodic)memoryandworkingmemory(short-term)[24,25,27]. Long-termmemoryrefersto
theknowledgestoredinthemodel’sparameters,whichcanbeupdatedby(re)pretraining[53],finetun-
ing[59],andmodelediting[14]. Workingmemoryisstoredinsustainedactivations/representations
ofneurons,whichwillbeawakenedduringinferencetime[24]. In-contextlearning(ICL)isakind
ofworkingmemory[60],alsoalongwithretrieval-basededitingmethodslikeGRACE[10]. How
toreinforcememoryandinject/updateknowledgeforLLMsisafundamentalquestion[28,61,62].
ICLorfinetuning? Differentworksshowdifferentconclusions. In[62],theauthorsfindthatfew-shot
finetuningismoregeneralizablethanICL,especiallyforout-of-distributiondata. In[61],theauthors
contrastfinetuningwithretrieval-augmentedgeneration(RAG)intermsofknowledgeinjectionand
findthatRAGisbetterinmostcases,andcombiningbothwillproducethebestresults. However,
finetuningandpretrainingarecomputation-expensive[13,10]andusuallysufferfromcatastrophic
forgetting [63] and overfitting [64]. For ICL and RAG, the working memory is sometimes not
controllable,themodelmaynotfollowtheinformationofthecontexts[24],andthecontextwindow
islimited[91,92],andthereareworksaddressingtheseissuesbytrainingcontrollableICL[24],
long-context [91,92],andrecurrentmemoryarchitecturedesign[28]. SPALMisproposedtoadd
languagemodelswithstoragemodulesthatresemblebothworkingandlong-termmemories[27].
Model Editing of LLMs Model editing can be summarized as the following lines of research.
Constrainedfinetuning: Preliminarymodeleditingusesconstrainedfinetuningtoupdateparameters
basedonnewexamples[93,94]. Locate-and-edit: ROME[18]locatesthefactualassociationsin
autoregressiveLLMsandconductsaccurateandefficienteditsbytakingMLPsaskey-valuememories.
Then,MEMIT[19]extendsROMEfromsingle-editingtomass-editing.COMEBA-HK[95]identifies
the Local Editing Scope and extends MEMIT for sequential editing. In addition, T-Patcher [11]
targets the last feed-forward layer of LLMs, adding an additional neuron for each edit. Meta
learning: Recentmeta-learningmethodsusehypernetworksforaidingediting. MEND[31]learnsa
hypernetworkthatcandecouplethefinetuninggradientsintothegradientupdatesthatgeneralizethe
editsandwon’tdamagetheperformancesonunrelatedinputs. Toremedythecancellationeffectof
MEND,MALMEN[15]useshypernetworktoproducetheweightshiftsofeditingandformulatesthe
weightshiftaggregationastheleastsquareproblem. Retrieval-basedmethods: Insteadofdirectly
editingthemodelparameters,retrieval-basedmethodsaimtoimprovetheworkingmemoryofLLMs
toenablemodelediting. IKE[96]usescontext-editfactstoguidethemodelwhengeneratingedited
facts. DeCK [97] employs contrasting knowledge decoding, which enhances the confidence of
in-context-basededitorsintheeditedfacts. SERAC[32](amodifiedversiondubbedasDEFER[10])
recordsedititemsinafileandtrainsadditionalscopeclassifierandcounterfactualmodeltodetect,
retrieve,andgeneratetheedit-relatedresults. Thoughtheeditingretrieverandgeneratorareneural
networks,theyaretoosmalltohavethepowerofLLMs. GRACE[10]adoptsadiscretecodebook
ofeditsforretrievingandreplacingtheedits’layerrepresentationsduringinference. Fromsingle
editing[18]tomassediting[15,19],andfromstaticeditingtosequential[11](continual)orlifelong
editing[10],modeleditingisdevelopingtomeetmorerealisticdemands.
ContinualLearning Continuallearning[98,99]tacklesthecatastrophicforgettingproblemin
deeplearningmodelswithnewknowledge[100],andrecentresearchhasfocusedonvariousmethods
inthisarea. Onesuchmethodiscontinualfinetuning,whereLLMsarerefinedovertimewiththe
arrivalofnewinstances. Forinstance,acomprehensivestudyby[101]explorescontinualfinetuning
extensively. However, it has been observed that regularizing finetuning with continual learning
techniques such as Elastic Weight Consolidation [20], Experience Replay [102], and Maximally
InterferedReplay[103]canleadtoarapiddecayinperformanceonprevioustasks,althoughitaids
inretainingsomememoryofpastinputs. Thissuggeststhatediting,asopposedtovanillacontinual
finetuning,presentsuniquechallenges,especiallyconsideringthateditsareunlikelytobeevenly
distributed[104]. Onepromisingdirectionwithintherealmofcontinuallearningistheadoption
of key-value methods, inspired by advancements in computer vision [105, 106]. Recent studies
haveshowcasedtheeffectivenessofcontinualprompt-learningforNLP[107,108],particularlyin
applicationsliketextretrieval[109].Notably,discretekey-valuemethodshavebeenshowntoexcelin
handlingshiftingdistributions[110],withsomerecenteffortsextendingtheirapplicationtoquestion
answering[111]. Thesemethodscachevaluestoensurethatinputsremainwithinthedistributionfor
downstreamencoders,thusfacilitatingtheincorporationoflonger-termmemory,providedthereare
adequatecomputationalresources.
28
NeurIPSPaperChecklist
1. Claims
Question: Dothemainclaimsmadeintheabstractandintroductionaccuratelyreflectthe
paper’scontributionsandscope?
Answer: [Yes]
Justification: AbstractandSection1Introduction
Guidelines:
• The answer NA means that the abstract and introduction do not include the claims
madeinthepaper.
• Theabstractand/orintroductionshouldclearlystatetheclaimsmade,includingthe
contributionsmadeinthepaperandimportantassumptionsandlimitations. ANoor
NAanswertothisquestionwillnotbeperceivedwellbythereviewers.
• Theclaimsmadeshouldmatchtheoreticalandexperimentalresults,andreflecthow
muchtheresultscanbeexpectedtogeneralizetoothersettings.
• Itisfinetoincludeaspirationalgoalsasmotivationaslongasitisclearthatthesegoals
arenotattainedbythepaper.
2. Limitations
Question: Doesthepaperdiscussthelimitationsoftheworkperformedbytheauthors?
Answer: [Yes]
Justification: Section5Limitations
Guidelines:
• TheanswerNAmeansthatthepaperhasnolimitationwhiletheanswerNomeansthat
thepaperhaslimitations,butthosearenotdiscussedinthepaper.
• Theauthorsareencouragedtocreateaseparate"Limitations"sectionintheirpaper.
• Thepapershouldpointoutanystrongassumptionsandhowrobusttheresultsareto
violationsoftheseassumptions(e.g.,independenceassumptions,noiselesssettings,
modelwell-specification,asymptoticapproximationsonlyholdinglocally).Theauthors
shouldreflectonhowtheseassumptionsmightbeviolatedinpracticeandwhatthe
implicationswouldbe.
• Theauthorsshouldreflectonthescopeoftheclaimsmade,e.g.,iftheapproachwas
onlytestedonafewdatasetsorwithafewruns. Ingeneral,empiricalresultsoften
dependonimplicitassumptions,whichshouldbearticulated.
• Theauthorsshouldreflectonthefactorsthatinfluencetheperformanceoftheapproach.
Forexample,afacialrecognitionalgorithmmayperformpoorlywhenimageresolution
isloworimagesaretakeninlowlighting. Oraspeech-to-textsystemmightnotbe
usedreliablytoprovideclosedcaptionsforonlinelecturesbecauseitfailstohandle
technicaljargon.
• Theauthorsshoulddiscussthecomputationalefficiencyoftheproposedalgorithms
andhowtheyscalewithdatasetsize.
• If applicable, the authors should discuss possible limitations of their approach to
addressproblemsofprivacyandfairness.
• Whiletheauthorsmightfearthatcompletehonestyaboutlimitationsmightbeusedby
reviewersasgroundsforrejection,aworseoutcomemightbethatreviewersdiscover
limitationsthataren’tacknowledgedinthepaper. Theauthorsshouldusetheirbest
judgmentandrecognizethatindividualactionsinfavoroftransparencyplayanimpor-
tantroleindevelopingnormsthatpreservetheintegrityofthecommunity. Reviewers
willbespecificallyinstructedtonotpenalizehonestyconcerninglimitations.
3. TheoryAssumptionsandProofs
Question: Foreachtheoreticalresult,doesthepaperprovidethefullsetofassumptionsand
acomplete(andcorrect)proof?
Answer: [Yes]
29
Justification: AssumptionsinSection2.3.2andProofsinAppendixC
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotincludetheoreticalresults.
• Allthetheorems, formulas, andproofsinthepapershouldbenumberedandcross-
referenced.
• Allassumptionsshouldbeclearlystatedorreferencedinthestatementofanytheorems.
• Theproofscaneitherappearinthemainpaperorthesupplementalmaterial, butif
theyappearinthesupplementalmaterial,theauthorsareencouragedtoprovideashort
proofsketchtoprovideintuition.
• Inversely,anyinformalproofprovidedinthecoreofthepapershouldbecomplemented
byformalproofsprovidedinappendixorsupplementalmaterial.
• TheoremsandLemmasthattheproofreliesuponshouldbeproperlyreferenced.
4. ExperimentalResultReproducibility
Question: Doesthepaperfullydisclosealltheinformationneededtoreproducethemainex-
perimentalresultsofthepapertotheextentthatitaffectsthemainclaimsand/orconclusions
ofthepaper(regardlessofwhetherthecodeanddataareprovidedornot)?
Answer: [Yes]
Justification: WereportthesetupthroughoutthepaperaswellasintheSection3.1and
AppendixA
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotincludeexperiments.
• Ifthepaperincludesexperiments,aNoanswertothisquestionwillnotbeperceived
well by the reviewers: Making the paper reproducible is important, regardless of
whetherthecodeanddataareprovidedornot.
• Ifthecontributionisadatasetand/ormodel,theauthorsshoulddescribethestepstaken
tomaketheirresultsreproducibleorverifiable.
• Dependingonthecontribution,reproducibilitycanbeaccomplishedinvariousways.
Forexample,ifthecontributionisanovelarchitecture,describingthearchitecturefully
mightsuffice,orifthecontributionisaspecificmodelandempiricalevaluation,itmay
benecessarytoeithermakeitpossibleforotherstoreplicatethemodelwiththesame
dataset,orprovideaccesstothemodel. Ingeneral. releasingcodeanddataisoften
onegoodwaytoaccomplishthis,butreproducibilitycanalsobeprovidedviadetailed
instructionsforhowtoreplicatetheresults,accesstoahostedmodel(e.g.,inthecase
ofalargelanguagemodel),releasingofamodelcheckpoint,orothermeansthatare
appropriatetotheresearchperformed.
• WhileNeurIPSdoesnotrequirereleasingcode,theconferencedoesrequireallsubmis-
sionstoprovidesomereasonableavenueforreproducibility,whichmaydependonthe
natureofthecontribution. Forexample
(a) Ifthecontributionisprimarilyanewalgorithm,thepapershouldmakeitclearhow
toreproducethatalgorithm.
(b) Ifthecontributionisprimarilyanewmodelarchitecture,thepapershoulddescribe
thearchitectureclearlyandfully.
(c) Ifthecontributionisanewmodel(e.g.,alargelanguagemodel),thenthereshould
eitherbeawaytoaccessthismodelforreproducingtheresultsorawaytoreproduce
themodel(e.g.,withanopen-sourcedatasetorinstructionsforhowtoconstruct
thedataset).
(d) We recognize that reproducibility may be tricky in some cases, in which case
authorsarewelcometodescribetheparticularwaytheyprovideforreproducibility.
Inthecaseofclosed-sourcemodels,itmaybethataccesstothemodelislimitedin
someway(e.g.,toregisteredusers),butitshouldbepossibleforotherresearchers
tohavesomepathtoreproducingorverifyingtheresults.
5. Openaccesstodataandcode
Question: Doesthepaperprovideopenaccesstothedataandcode,withsufficientinstruc-
tionstofaithfullyreproducethemainexperimentalresults,asdescribedinsupplemental
material?
30
Answer: [Yes]
Justification: We use publicly available datasets (Appendix A), Code and Data are also
providedinsupplementalmaterial.
Guidelines:
• TheanswerNAmeansthatpaperdoesnotincludeexperimentsrequiringcode.
• Please see the NeurIPS code and data submission guidelines (https://nips.cc/
public/guides/CodeSubmissionPolicy)formoredetails.
• Whileweencouragethereleaseofcodeanddata,weunderstandthatthismightnotbe
possible,so“No”isanacceptableanswer. Paperscannotberejectedsimplyfornot
includingcode,unlessthisiscentraltothecontribution(e.g.,foranewopen-source
benchmark).
• Theinstructionsshouldcontaintheexactcommandandenvironmentneededtorunto
reproducetheresults. SeetheNeurIPScodeanddatasubmissionguidelines(https:
//nips.cc/public/guides/CodeSubmissionPolicy)formoredetails.
• Theauthorsshouldprovideinstructionsondataaccessandpreparation,includinghow
toaccesstherawdata,preprocesseddata,intermediatedata,andgenerateddata,etc.
• Theauthorsshouldprovidescriptstoreproduceallexperimentalresultsforthenew
proposedmethodandbaselines. Ifonlyasubsetofexperimentsarereproducible,they
shouldstatewhichonesareomittedfromthescriptandwhy.
• Atsubmissiontime, topreserveanonymity, theauthorsshouldreleaseanonymized
versions(ifapplicable).
• Providingasmuchinformationaspossibleinsupplementalmaterial(appendedtothe
paper)isrecommended,butincludingURLstodataandcodeispermitted.
6. ExperimentalSetting/Details
Question: Doesthepaperspecifyallthetrainingandtestdetails(e.g.,datasplits,hyper-
parameters, how they were chosen, type of optimizer, etc.) necessary to understand the
results?
Answer: [Yes]
Justification:InAppendixA,weprovidedetaileddescriptionsofdatasplitsandtheproposed
method’shyperparametersandbaselines’hyperparameters. Additionally,inSection3.3,we
discusshowtoselectthemfortheproposedmethod.
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotincludeexperiments.
• Theexperimentalsettingshouldbepresentedinthecoreofthepapertoalevelofdetail
thatisnecessarytoappreciatetheresultsandmakesenseofthem.
• Thefulldetailscanbeprovidedeitherwiththecode,inappendix,orassupplemental
material.
7. ExperimentStatisticalSignificance
Question:Doesthepaperreporterrorbarssuitablyandcorrectlydefinedorotherappropriate
informationaboutthestatisticalsignificanceoftheexperiments?
Answer: [Yes]
Justification: The LLMs only have one checkpoint of the corresponding size, e.g.,
LLaMA-2-7B, so we only edit once for each setting. But we test our method and base-
linesundervariousmodels,settings,anddatasets,therefore,thestatisticalsignificanceof
theexperimentscanbeverifiedandsupported.
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotincludeexperiments.
• Theauthorsshouldanswer"Yes"iftheresultsareaccompaniedbyerrorbars,confi-
denceintervals,orstatisticalsignificancetests,atleastfortheexperimentsthatsupport
themainclaimsofthepaper.
• Thefactorsofvariabilitythattheerrorbarsarecapturingshouldbeclearlystated(for
example,train/testsplit,initialization,randomdrawingofsomeparameter,oroverall
runwithgivenexperimentalconditions).
31
• Themethodforcalculatingtheerrorbarsshouldbeexplained(closedformformula,
calltoalibraryfunction,bootstrap,etc.)
• Theassumptionsmadeshouldbegiven(e.g.,Normallydistributederrors).
• Itshouldbeclearwhethertheerrorbaristhestandarddeviationorthestandarderror
ofthemean.
• It is OK to report 1-sigma error bars, but one should state it. The authors should
preferablyreporta2-sigmaerrorbarthanstatethattheyhavea96%CI,ifthehypothesis
ofNormalityoferrorsisnotverified.
• Forasymmetricdistributions,theauthorsshouldbecarefulnottoshowintablesor
figuressymmetricerrorbarsthatwouldyieldresultsthatareoutofrange(e.g. negative
errorrates).
• Iferrorbarsarereportedintablesorplots,Theauthorsshouldexplaininthetexthow
theywerecalculatedandreferencethecorrespondingfiguresortablesinthetext.
8. ExperimentsComputeResources
Question: Foreachexperiment,doesthepaperprovidesufficientinformationonthecom-
puterresources(typeofcomputeworkers,memory,timeofexecution)neededtoreproduce
theexperiments?
Answer: [Yes]
Justification: InAppendixA.3,B.7andSection3.3
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotincludeexperiments.
• ThepapershouldindicatethetypeofcomputeworkersCPUorGPU,internalcluster,
orcloudprovider,includingrelevantmemoryandstorage.
• Thepapershouldprovidetheamountofcomputerequiredforeachoftheindividual
experimentalrunsaswellasestimatethetotalcompute.
• Thepapershoulddisclosewhetherthefullresearchprojectrequiredmorecompute
thantheexperimentsreportedinthepaper(e.g.,preliminaryorfailedexperimentsthat
didn’tmakeitintothepaper).
9. CodeOfEthics
Question: Doestheresearchconductedinthepaperconform, ineveryrespect, withthe
NeurIPSCodeofEthicshttps://neurips.cc/public/EthicsGuidelines?
Answer: [Yes]
Justification: We use publicly standard datasets that do not contain information about
individualpeopleoroffensivecontexttoourknowledge.Ethicalconsiderationsarediscussed
inSection5.
Guidelines:
• TheanswerNAmeansthattheauthorshavenotreviewedtheNeurIPSCodeofEthics.
• IftheauthorsanswerNo,theyshouldexplainthespecialcircumstancesthatrequirea
deviationfromtheCodeofEthics.
• Theauthorsshouldmakesuretopreserveanonymity(e.g.,ifthereisaspecialconsid-
erationduetolawsorregulationsintheirjurisdiction).
10. BroaderImpacts
Question: Does the paper discuss both potential positive societal impacts and negative
societalimpactsoftheworkperformed?
Answer: [Yes]
Justification: InSection5
Guidelines:
• TheanswerNAmeansthatthereisnosocietalimpactoftheworkperformed.
• IftheauthorsanswerNAorNo,theyshouldexplainwhytheirworkhasnosocietal
impactorwhythepaperdoesnotaddresssocietalimpact.
32
• Examplesofnegativesocietalimpactsincludepotentialmaliciousorunintendeduses
(e.g.,disinformation,generatingfakeprofiles,surveillance),fairnessconsiderations
(e.g.,deploymentoftechnologiesthatcouldmakedecisionsthatunfairlyimpactspecific
groups),privacyconsiderations,andsecurityconsiderations.
• Theconferenceexpectsthatmanypaperswillbefoundationalresearchandnottied
toparticularapplications,letalonedeployments. However,ifthereisadirectpathto
anynegativeapplications,theauthorsshouldpointitout. Forexample,itislegitimate
topointoutthatanimprovementinthequalityofgenerativemodelscouldbeusedto
generatedeepfakesfordisinformation. Ontheotherhand,itisnotneededtopointout
thatagenericalgorithmforoptimizingneuralnetworkscouldenablepeopletotrain
modelsthatgenerateDeepfakesfaster.
• Theauthorsshouldconsiderpossibleharmsthatcouldarisewhenthetechnologyis
being used as intended and functioning correctly, harms that could arise when the
technologyisbeingusedasintendedbutgivesincorrectresults,andharmsfollowing
from(intentionalorunintentional)misuseofthetechnology.
• Iftherearenegativesocietalimpacts,theauthorscouldalsodiscusspossiblemitigation
strategies (e.g., gated release of models, providing defenses in addition to attacks,
mechanismsformonitoringmisuse,mechanismstomonitorhowasystemlearnsfrom
feedbackovertime,improvingtheefficiencyandaccessibilityofML).
11. Safeguards
Question: Doesthepaperdescribesafeguardsthathavebeenputinplaceforresponsible
releaseofdataormodelsthathaveahighriskformisuse(e.g.,pretrainedlanguagemodels,
imagegenerators,orscrapeddatasets)?
Answer: [NA]
Justification: [NA]
Guidelines:
• TheanswerNAmeansthatthepaperposesnosuchrisks.
• Releasedmodelsthathaveahighriskformisuseordual-useshouldbereleasedwith
necessarysafeguardstoallowforcontrolleduseofthemodel,forexamplebyrequiring
thatusersadheretousageguidelinesorrestrictionstoaccessthemodelorimplementing
safetyfilters.
• DatasetsthathavebeenscrapedfromtheInternetcouldposesafetyrisks. Theauthors
shoulddescribehowtheyavoidedreleasingunsafeimages.
• Werecognizethatprovidingeffectivesafeguardsischallenging,andmanypapersdo
notrequirethis,butweencourageauthorstotakethisintoaccountandmakeabest
faitheffort.
12. Licensesforexistingassets
Question: Arethecreatorsororiginalownersofassets(e.g.,code,data,models),usedin
thepaper,properlycreditedandarethelicenseandtermsofuseexplicitlymentionedand
properlyrespected?
Answer: [Yes]
Justification: Section3.1andAppendixA.Weusepubliclyavailableartifacts.
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotuseexistingassets.
• Theauthorsshouldcitetheoriginalpaperthatproducedthecodepackageordataset.
• Theauthorsshouldstatewhichversionoftheassetisusedand,ifpossible,includea
URL.
• Thenameofthelicense(e.g.,CC-BY4.0)shouldbeincludedforeachasset.
• Forscrapeddatafromaparticularsource(e.g.,website),thecopyrightandtermsof
serviceofthatsourceshouldbeprovided.
• If assets are released, the license, copyright information, and terms of use in the
packageshouldbeprovided. Forpopulardatasets,paperswithcode.com/datasets
hascuratedlicensesforsomedatasets. Theirlicensingguidecanhelpdeterminethe
licenseofadataset.
33
• Forexistingdatasetsthatarere-packaged,boththeoriginallicenseandthelicenseof
thederivedasset(ifithaschanged)shouldbeprovided.
• Ifthisinformationisnotavailableonline,theauthorsareencouragedtoreachoutto
theasset’screators.
13. NewAssets
Question:Arenewassetsintroducedinthepaperwelldocumentedandisthedocumentation
providedalongsidetheassets?
Answer: [NA]
Justification: [NA]
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotreleasenewassets.
• Researchersshouldcommunicatethedetailsofthedataset/code/modelaspartoftheir
submissions via structured templates. This includes details about training, license,
limitations,etc.
• Thepapershoulddiscusswhetherandhowconsentwasobtainedfrompeoplewhose
assetisused.
• Atsubmissiontime,remembertoanonymizeyourassets(ifapplicable). Youcaneither
createananonymizedURLorincludeananonymizedzipfile.
14. CrowdsourcingandResearchwithHumanSubjects
Question: Forcrowdsourcingexperimentsandresearchwithhumansubjects,doesthepaper
includethefulltextofinstructionsgiventoparticipantsandscreenshots,ifapplicable,as
wellasdetailsaboutcompensation(ifany)?
Answer: [NA]
Justification: [NA]
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotinvolvecrowdsourcingnorresearchwith
humansubjects.
• Includingthisinformationinthesupplementalmaterialisfine,butifthemaincontribu-
tionofthepaperinvolveshumansubjects,thenasmuchdetailaspossibleshouldbe
includedinthemainpaper.
• AccordingtotheNeurIPSCodeofEthics,workersinvolvedindatacollection,curation,
orotherlaborshouldbepaidatleasttheminimumwageinthecountryofthedata
collector.
15. InstitutionalReviewBoard(IRB)ApprovalsorEquivalentforResearchwithHuman
Subjects
Question: Doesthepaperdescribepotentialrisksincurredbystudyparticipants,whether
suchrisksweredisclosedtothesubjects,andwhetherInstitutionalReviewBoard(IRB)
approvals(oranequivalentapproval/reviewbasedontherequirementsofyourcountryor
institution)wereobtained?
Answer: [NA]
Justification: [NA]
Guidelines:
• TheanswerNAmeansthatthepaperdoesnotinvolvecrowdsourcingnorresearchwith
humansubjects.
• Dependingonthecountryinwhichresearchisconducted,IRBapproval(orequivalent)
mayberequiredforanyhumansubjectsresearch. IfyouobtainedIRBapproval,you
shouldclearlystatethisinthepaper.
• Werecognizethattheproceduresforthismayvarysignificantlybetweeninstitutions
andlocations,andweexpectauthorstoadheretotheNeurIPSCodeofEthicsandthe
guidelinesfortheirinstitution.
• Forinitialsubmissions,donotincludeanyinformationthatwouldbreakanonymity(if
applicable),suchastheinstitutionconductingthereview.
34