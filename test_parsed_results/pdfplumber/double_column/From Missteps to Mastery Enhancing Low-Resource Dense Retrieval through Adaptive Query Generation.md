# From Missteps to Mastery Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation

PDF Download
3690624.3709225.pdf
26 March 2026
Total Citations: 5
. Total Downloads: 393
.
Latest updates: hps://dl.acm.org/doi/10.1145/3690624.3709225 .
.
Published: 20 July 2025
.
. .
RESEARCH-ARTICLE .
Citation in BibTeX format
From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval
.
.
through Adaptive ery Generation KDD '25: The 31st ACM SIGKDD
Conference on Knowledge Discovery and
Data Mining
ZHENYU TONG, University of Chinese Academy of Sciences, Beijing, China August 3 - 7, 2025
Toronto ON, Canada
.
CHUAN QIN, Chinese Academy of Sciences, Beijing, Beijing, China .
.
Conference Sponsors:
. CHUYU FANG, Baidu, Inc., Beijing, China SIGMOD
SIGKDD
.
KAICHUN YAO, Institute of Soware Chinese Academy of Sciences, Beijing, Beijing, China
.
XI CHEN, University of Science and Technology of China, Hefei, Anhui, China
.
JINGSHUAI ZHANG, Baidu, Inc., Beijing, China
.
View all
.
.
Open Access Support provided by:
.
University of Science and Technology of China
.
Baidu, Inc.
.
Chinese Academy of Sciences
.
University of Chinese Academy of Sciences
.
Institute of Soware Chinese Academy of Sciences
.
KDD '25: Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.1 (July 2025)
hps://doi.org/10.1145/3690624.3709225
ISBN: 9798400712456
.
From Missteps to Mastery: Enhancing Low-Resource Dense
Retrieval through Adaptive Query Generation
ZhenyuTong∗ ChuanQin∗ ChuyuFang
UniversityoftheChineseAcademyof ComputerNetworkInformation BaiduInc.
Sciences Center,ChineseAcademyofSciences Beijing,China
Beijing,China Beijing,China fangchuyu2022@gmail.com
tongzhenyu123@gmail.com chuanqin0426@gmail.com
KaichunYao XiChen JingshuaiZhang
InstituteofSoftware,Chinese UniversityofScienceandTechnology BaiduInc.
AcademyofSciences ofChina Beijing,China
Beijing,China Hefei,China zhangjingshuai0@gmail.com
yaokaichun@outlook.com chenxi0401@mail.ustc.edu.cn
ChenZhu HengshuZhu†
UniversityofScienceandTechnology ComputerNetworkInformation
ofChina Center,ChineseAcademyofSciences
Hefei,China Beijing,China
zc3930155@gmail.com zhuhengshu@gmail.com
Abstract fine-tuningprocess.Furthermore,wedesignanoveliterativeopti-
Documentretrieval,designedtorecallquery-relevantdocuments mizationstrategythatdynamicallyoptimizesthequerygenerator
fromexpansivecollections,isessentialforinformation-seeking forproducingmoreinformativequeries,therebyenhancingthe
tasks,suchaswebsearchandopen-domainquestion-answering. efficacyoftheentireframework.Finally,extensiveexperiments
Advancesinrepresentationlearningandpretrainedlanguagemod- conductedonaseriesofpubliclyavailableretrievalbenchmark
els(PLMs)havedrivenaparadigmshiftfromtraditionalsparse datasetshavedemonstratedtheeffectivenessoftheproposediGFT.
retrieval methods to more effective dense retrieval approaches,
CCSConcepts
forgingenhancedsemanticconnectionsbetweenqueriesanddocu-
mentsandestablishingnewperformancebenchmarks.However, •Informationsystems→Informationretrieval;•Computing
relianceonextensiveannotateddocument-querypairslimitstheir methodologies→Naturallanguagegeneration.
competitivenessinlow-resourcescenarios.Recentresearchefforts
employingthefew-shotcapabilitiesoflargelanguagemodels(LLMs) Keywords
andpromptengineeringforsyntheticdatagenerationhaveemerged
Denseretrieval;querygeneration;largelanguagemodel
asapromisingsolution.Nonetheless,theseapproachesarehindered
bythegenerationoflower-qualitydatawithintheconventional ACMReferenceFormat:
denseretrievaltrainingprocess.Tothisend,inthispaper,weintro- ZhenyuTong,ChuanQin,ChuyuFang,KaichunYao,XiChen,Jingshuai
duceiGFT,aframeworkaimedatenhancinglow-resourcedensere- Zhang,ChenZhu,andHengshuZhu.2025.FromMisstepstoMastery:En-
trievalbyintegratingathree-phaseprocess—Generation,Filtering, hancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration.
andTuning—coupledwithaniterativeoptimizationstrategy.Specif- InProceedingsofthe31stACMSIGKDDConferenceonKnowledgeDiscovery
andDataMiningV.1(KDD’25),August3–7,2025,Toronto,ON,Canada.ACM,
ically,wefirstemploysupervisedfine-tuningonlimitedground
NewYork,NY,USA,12pages.https://doi.org/10.1145/3690624.3709225
truthdata,enablinganLLMtofunctionasthegeneratorcapableof
producingpotentialqueriesfromgivendocuments.Subsequently,
wepresentamulti-stagefilteringmoduletominimizenoiseinthe 1 Introduction
generateddatawhileretainingsamplespoisedtosignificantlyim-
Documentretrievalhasplayedasignificantrolewithinmodern
provethedenseretrievalmodel’sperformanceinthefollow-up
information-seekingsystems,aimingtoidentifythemostrelevant
∗Bothareco-firstauthorsandcontributeequallytothiswork. documentsfromvastcorporainresponsetouserqueries[12,38,
†Correspondingauthor 58].Thisfoundationalprocessunderpinsawiderangeofapplica-
tions,fromestablishedsearchengines[25]tothelatestretrieval-
augmentedgeneration(RAG)frameworks[28].
ThisworkislicensedunderaCreativeCommons4.0InternationalLicense. Thefieldofdocumentretrievalhasarichresearchhistory,with
KDD’25,August3–7,2025,Toronto,ON,Canada traditionalapproachespredominantlyutilizingsparseretrievers,
©2025Copyrightheldbytheowner/author(s).
suchasTF-IDFandBM25[43],tomatchqueriesanddocuments
ACMISBN979-8-4007-1245-6/25/08
https://doi.org/10.1145/3690624.3709225 throughlexicaloverlap.Withtheadvancementofdeeplearning,
1373
KDD’25,August3–7,2025,Toronto,ON,Canada ZhenyuTongetal.
0.30
0.25
0.20
0.15
0.10
0.05
0.00
300020001000500 486 250 100 50 10
01@GCDN
0.30 LLM-basedquerygeneratorbyfine-tuningLLMswithannotated
ColBERT
BM25 0.25 document-query pairs. (2) How can generated queries be filtered
0.20
toimprovetheperformanceofdenseretrievalmodels?SinceLLMs
0.15
0.10 ColBERT + QG donotalwaysgeneratehigh-qualityqueries,incorporatingadata
0.05 C iG o F lB T ERT + QG + Denoisy filteringmodulebeforetrainingdenseretrievalmodelsbecomes
0.00 essential.Previousstudieshavetypicallyreliedonusingthegen-
250 500 750 1000 1250 1500 1750
eration probability of queries [4] to weed out low-quality data.
Figure1:Left:DecliningperformanceofColBERTonthe However,thesemethodsoverlookacriticalperspective:theidenti-
FiQAdatasetwithreducingtrainingdata(hollowcircleindi- ficationandselectionofthemostinformativedocument-querypairs
catestrainingsetusedintheSPTAR[37]experimentalsetup. forimprovingretrievaleffectiveness.(3)Howcanthegeneratorbe
Right:Impactoffine-tuningtheColBERTmodel(pretrained optimizedtomoreconsistentlyproducehigh-qualitydocument-query
usingthesametrainingsetofSPTAR)withsyntheticdata pairs?AlthoughLLM-basedgeneratorscancontinuouslygenerate
generatedbyLLM-basedquerygenerator(QG),QGenhanced newdata,itisimportanttorecognizethatnotallgenerateddata
withdatadenoising,andourproposediGFTacrossvarious contributespositivelytotheperformanceofdenseretrievalmodels.
augmenteddatavolumes. AsillustratedinFigure1,themarginalutilityofdatafromastatic
generatorinenhancingretrievalmodelperformancediminishes
throughoutthetrainingprocess.Therefore,continuouslyoptimiz-
recentmethodsleveragingadual-encoderarchitecturehavetrans- inggeneratorstomorereliablyproducehigh-qualitysyntheticdata,
formeddocumentretrievalbyembeddingqueriesanddocuments particularlytoimprovetheperformanceofdenseretrievalmodels,
intolow-dimensionaldensevectorsforrelevancecalculation,mark- hasbecomeacriticalchallenge.
ingtheemergenceofdenseretrieval[17,58].Duetotheirprofound Toaddresstheabovechallenges,inthispaper,weintroducea
capabilitytocaptureintrinsicsemantics,pretrainedlanguagemod- novelframeworknamediGFT,designedtoenhancedenseretrieval
els(PLMs)likeBERT[9,23]haveemergedasthede-factoimple- throughathree-phase,iterativelyoptimizedprocess—Generation,
mentationforencodersindenseretrieval,consequentlyredefining Filtering,andTuning.Specifically,webeginbyleveragingsuper-
performancebenchmarksinthefield[24]. visedfine-tuningonlimitedgroundtruthdata,enablinganLLMto
Despiteitssuperiorperformanceoversparseretrievalmethods serveasageneratorcapableofproducingpotentialqueriesfrom
acrossabroadrangeofbenchmarkdatasets,denseretrievalheavily givendocuments.Followingthis,weintroduceamulti-stagefilter-
reliesonawealthofannotateddocument-querypairsforeffective ingmoduledesignedtoreducenoiseinthegenerateddatawhilepre-
trainingandoftenexhibitspoorgeneralizationacrossdomains[49]. servingthemostinformativesamplesthatcansignificantlyenhance
Thisdependencyisespeciallypronouncedinlow-resourcescenar- theperformanceofthedenseretrievalmodelduringsubsequent
ios,wherethescarcityofannotateddataandthelabor-intensive fine-tuning.Additionally,wedesignanoveliterativeoptimization
processofcollectingwell-labeleddocument-querypairs[41]ex- strategyaimedataugmentingthedenseretrievalmodel’straining
acerbatethechallengeofimprovingdenseretrievalperformance. efficacy.Inparticular,wepresentadifficulty-guidedreinforcement
Inresponse,severalresearchershavebegunconstructingpseudo learningmethod,dynamicallyadaptingthequerygeneratortopro-
document-querypairsandleveragingcontrastivelearningtech- duce more informative synthetic data at each iteration. Finally,
niquestotraindenseretrievalmodels,aimingtoovercomethis extensiveexperimentsconductedonseveralpubliclyavailablere-
obstacle[26].Recently,largelanguagemodels(LLMs),including trievalbenchmarkdatasetshavedemonstratedtheeffectivenessof
ChatGPTandGPT-4,havedemonstratedremarkablecapabilitiesin theproposedframework.
languageunderstanding,generation,andfew-shotlearningacross
variousNLPtasks[5,6,20].Thisadvancementintroducesadata
augmentationperspectiveforresearcherstoboosttheperformance 2 RelatedWorks
oflow-resourcedenseretrievalbygeneratingpotentialqueriesfrom
2.1 DenseRetrieval
givendocuments[4,19,37,44].Forinstance,InParscapitalizeson
GPT-3’sincontextlearningtogeneratequeriesforunlabeleddocu- Compared with traditional bag-of-words-based sparse retrieval
ments[4],whileSPTARemployssoftprompttuningtooptimize models[1,43,56],neuralnetwork-baseddenseretrieval[22,24,39]
promptsbasedonlimitedgroundtruthdata[37]. hasthepotentialtocapturedeepersemanticinformation.Early
However,employingLLMsasquerygeneratorstoenhancedense explorationsindenseretrievalfocusedondirectlycapturinglatent
retrievalperformancestillpresentsseveraltechnicalchallenges. semanticcharacteristicsformatchingthroughneuralnetworktrain-
(1)HowcanLLMsbeenabledtogeneratehigh-qualityqueries?Cur- ing[13,14].Recently,theadventofpretrainedmodelshassignifi-
rentmethods,suchasInPars[4],InPars-v2[19],andPROMPTA- cantlyenhancedthelanguageunderstandingabilityofthemodel.A
GATOR[8],primarilyrelyonpromptengineeringtoguideLLMs notableexampleisDPR[22]whichemploysaBERT-basedencoder
ingeneratingqueries,usingasmallsetofpositivedocument-query toindependentlyencodequeriesanddocuments,calculatingrele-
pairsasexamples.Theseapproachesdependheavilyontheprompt vanceviadotproductsimilarity.Furthermore,MVR[57]introduced
qualityandtheLLMs’few-shotlearningcapabilities,whichoften thestrategyofinsertingmultipletokensatthebeginningofthetext
resultininconsistentqueryquality,therebycompromisingtheeffec- toobtaindiverserepresentations.Formorefine-grainedvectorin-
tivenessofsubsequentdenseretrievalmodeltraining.Furthermore, teraction,ColBERT[24]innovativelygeneratedindependentvector
thesemethodsoverlookthepotentialbenefitsofenhancingthe representationsforeachwordinqueriesanddocuments.Inaddition,
1374
FromMisstepstoMastery:EnhancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration KDD’25,August3–7,2025,Toronto,ON,Canada
severalstudieshaveproposedlearningphrase-levelrepresentations Unlabeled documents LLM-QG+DR LLM-QG+DF+DR iGFT
ofquerieswhenretrievingphrase-basedanswers[46,47]. Document: Many
Researchhasalsoexploredeffectivenegativesamplingmethods s p s e c r a i r c v l e e ic s l e i t n s h e c a a h t r a l d y r o g w e n i o th t Qu L e L ry M G -b e a n s e e ra d tor Qu L e L ry M G -b e a n s e e ra d tor Ad Q a u p e ti r v y e G L e L n M e - ra b t a o s r ed
fortrainingretrievalmodels.Forinstance,Xiongetal.employed u ca s u ag se e . t h T e h i s s e i r s v i b c e e - Pseudo Document- Pseudo Document- Pseudo Document-
provider has ... Query Pairs Query Pairs Query Pairs
theretrievalmodeltrainedintheprecedingiterationtoidentify
newnegativeinstancesforthesubsequenttrainingiteration[54]. docu L m im en it t e - d q u an er n y o t p a a t i e r d s Dens M e o R d e e tr l ieval D ( a t a F i l t e . r . i . n ) g D M a u ta lt F i- il S t t e a r g in e g
Additionally,RocketQA[39]enhanceddenseretrievalperformance D in o g c t u h m e 1 e 2 n t p : l u D s u r- Document Query Filtered Pseudo Scored, Filtered
byusingknowledgedistillationtodenoisenegativesamples.Be- hours the market Document- Pseudo Document-
was closed news Encoder Encoder Query Pairs Query Pairs
sides,Contriever[18]employedcontrastivelearningtoachieve can change inve-
stors opinion of ...
unsupervisedtrainingindenseretrieval. Query: What cau- Dense Retrieval Dense Retrieval
ses discontinuities Score Model Model
Whiledenseretrievaldemonstratessuperiorperformance,prior with stock prices
researchhasprimarilyconcentratedonlearningfromexistingquery
labels.Inlow-resourcescenarios,denseretrievalexhibitsdiscernible Figure2:EnhancingdenseretrievalwithLLM-basedquery
limitations[59].Toaddressthisissue,weproposeanovelframe- generation:acomparisonofparadigms.
workcomprisingathree-phaseprocess:Generation,Filtering,and
Tuning,aimedatenhancinglow-resourcedenseretrieval.
3 Preliminary
GivenalargecorpusD ={𝑑 𝑖} 𝑖 𝑁 =1 composedof𝑁 documents,and
2.2 DataAugmentationforDenseRetrieval anaturallanguagequery𝑞,theobjectiveofdocumentretrievalis
tolearnamodelRcapableofreturningarankedlistofthe𝑛most
L it e y v o er f a p g s in eu g d d o at d a a a t u a g c m an en e t ff at e i c o t n iv t e e l c y hn e i n q h u a e n s c t e o t a h u e gm ro e b n u t s t t h n e es a s va o i f la t b h i e l- relevantdocumentsD𝑞 = [𝑑 1 𝑞 ,𝑑 2 𝑞 ,...,𝑑 𝑛 𝑞 ]forthequery𝑞.
UnliketraditionalsparseretrievalmethodslikeBM25,which
model[2,42].Inthefieldofdenseretrieval,severalstudiesrelied
dependonlexicalmatching,denseretrievalmodelsemploytwo
onhandcraftedtemplatesandfeaturestoextractmorerelevant
learnablefunctionsthatmapqueriesanddocumentstodensevec-
paireddata[36,40].Additionally,someresearchersproposedusing
extractiontoselectportionsofdocumentcontentasqueriesor
tors.Formally,let𝐸 𝑄(·)denotethequeryencoder,whichproduces
answerstoachievedataenhancement[26,45]. arepresentation𝐸 𝑄(𝑞) ∈R𝑘 1 foreachquery𝑞.Similarly,thedoc-
Inrecentyears,researchershaveutilizedlargelanguagemodels
umentencoder𝐸 𝐷(·)isdefinedtomapadocument𝑑toitsrepre-
togeneratequeriesforunlabeledcorpora,achievingfavorableout- sentation𝐸 𝐷(𝑑) ∈R𝑘 2.Alongthisline,thedenseretrievalmodel
comesininformationretrievaltasks[4,8,11,33,34,44,52].InPars Rcanbedenotedby
utilizedpromptswithalimitednumberofexamplestogenerate
paragraph-levelqueriesbasedonGPT-3[4].Similarly,TQGen[31] R(𝑞,𝑑;𝜃)=𝑓 𝑠𝑖𝑚 (cid:0)𝐸 𝑄(𝑞),𝐸 𝐷(𝑑)(cid:1), (1)
exploredqueryextractionandquerygenerationtocreatepseudo
where𝜃 denotestheparametersofRandthesimilaritymeasure-
document-querypairsforaugmentingretrievertraining.Incontrast
mentfunction𝑓 𝑠𝑖𝑚(·)canbeimplementedusinganinnerproduct,
tousingthehardpromptforgeneration,SPTAR[37]introduced
amultilayerperceptronnetwork(MLP),orotherneuralnetwork
softprompttuningtooptimizethequalityofthegeneratedquery.
architectures.Typically,therepresentationdimensionsofdocu-
Furthermore,toaddresstheinconsistencyofgeneratedqueriesby
ments and queries are identical, i.e.,𝑘 1 = 𝑘 2. However, this is
LLMs,somestudieshaveconcentratedondesigningvariousdata
notalwaysthecase.Forinstance,inColBERT[24],awell-known
selectionmethodstofilteroutqualifieddatafortraining[8,44].
denseretrievalmodel,queriesanddocumentsarerepresentedas
Beyondtrainingageneratorusinglabeleddocument-querypairs, 𝐸 𝑄(𝑞) ∈R|𝑞|×𝑘 and𝐸 𝐷(𝑑) ∈R|𝑑|×𝑘 ,respectively,where𝑘repre-
someresearchershaveexploredthedirectgenerationofpseudo
sentsthetokenrepresentationdimension.Subsequently,therele-
databasedonpretrainedmodelsinzero-shotscenarios[15,30,48].
vancescoreiscalculatedasfollows,
Additionally,SPAR[7]employedknowledgedistillationfromsparse
retrievalmodelstotrainthedatageneratorinzero-shotsettings. |𝑞|
Withouttrainingthedatagenerator,methodslikeHyDE[10]and R(𝑞,𝑑;𝜃)= ∑︁ max 𝐸 𝑄(𝑞) 𝑖 ⊤𝐸 𝐷(𝑑)𝑗 , (2)
CSQE[27]achievedsuperiorzero-shotinformationretrievalby 𝑖=1 𝑗=1,...,|𝑑|
supplementingqueriesordocumentswithgeneratedinformation.
where|𝑞|and|𝑑|denotethenumberoftokensin𝑞and𝑑,respec-
However,currentLLM-baseddatageneratorsprimarilyrelyon
existinglabeleddataandpowerfulpretrainedmodels,lackingthe
tively.𝐸 𝑄(𝑞)𝑖 and𝐸 𝐷(𝑑)𝑗 correspondtotheembeddingvectorsfor
the𝑖-thtokenin𝑞andthe𝑗-thtokenin𝑑,respectively.
abilitytoimproveautonomouslyinlow-resourcescenarios.More-
Asmentionedbefore,denseretrievalpredominantlyemploys
over,thereisasignificantdeficiencyineffectivemethodsforas-
sessingandselectinggeneratedresults.Inthispaper,wepropose
asupervisedtrainingsetting.GivenatrainingsetT𝑡𝑟𝑎𝑖𝑛,where
amulti-stagefilteringmoduledesignedtominimizenoiseinthe
each (𝑞,𝑑) ∈ T𝑡𝑟𝑎𝑖𝑛 representsarelevantdocument-querypair,
the optimization of the dense retrieval model R(𝑞,𝑑;𝜃) can be
generateddataandretainsamplesmostlikelytosignificantlyim-
formalizedas:
provetheperformanceofdenseretrievalmodels.Additionally,we
introduceadifficulty-guidediterativeoptimizationstrategytocon- 𝜃∗=argmaxE (𝑞,𝑑+,𝑑−)∼T′ L(R,𝑞,𝑑+,𝑑−), (3)
tinuouslyenhancethecapabilitiesofdatagenerators. 𝜃 𝑡𝑟𝑎𝑖𝑛
1375
KDD’25,August3–7,2025,Toronto,ON,Canada ZhenyuTongetal.
whereT 𝑡𝑟 ′ 𝑎𝑖𝑛isconstructedbasedonthetrainingsetT𝑡𝑟𝑎𝑖𝑛.Specif- isdefinedasfollows:
ically,∀(𝑞,𝑑+,𝑑−) ∈T 𝑡𝑟 ′ 𝑎𝑖𝑛,𝑑+denotesapositive(relevant)docu- |𝑞|
(
m
ir
e
r
n
el
t
e
,
v
i.
a
e
n
.,
t)
(𝑞
d
,
o
𝑑
c
+
u
)
m
∈
en
T
t
𝑡
,
𝑟
i
𝑎
.
𝑖
e
𝑛
.,
,
𝑑
a
−
nd
∈
𝑑
D
−
,
r
(
e
𝑞
p
,
r
𝑑
e
−
se
)
n
∉
ts
T
a
𝑡𝑟
s
𝑎
a
𝑖𝑛
m
.
p
T
l
h
e
e
d
o
n
b
e
j
g
e
a
c
t
t
i
i
v
v
e
e
L𝑙𝑙𝑚 =m
Θ
a
𝐿
x
(𝑞,𝑑)
∑︁
∈T𝑡𝑟𝑎𝑖𝑛
∑︁
𝑡=1
log (cid:0)𝑝 Θ+Θ𝐿 (𝑞 𝑡|𝑑,𝑞 <𝑡)(cid:1), (5)
functionLiscrucialformodeloptimization,withthecontrastive
whereΘ 𝐿 representstheLoRAparameters,weexclusivelyupdate
objectivebeingaprevalentchoice.Formally,thisisdefinedas
theseLoRAparametersthroughoutthetrainingprocess.Thenota-
𝑒𝑥𝑝(R(𝑞,𝑑+)) tion𝑞 𝑡 referstothe𝑡-thtokenin𝑞,and𝑞 <𝑡 representsthesequence
L(R,𝑞,𝑑+,𝑑−)=log 𝑒𝑥𝑝(R(𝑞,𝑑+))+(cid:205)𝑙 𝑒𝑥𝑝(R(𝑞,𝑑−)) . (4) oftokens{𝑞 1 ,𝑞 1 ,...,𝑞 𝑡−1 }.Finally,thefine-tunedLLMGempowers
𝑗=1 𝑗 ustogeneratequeriesforanygivendocument,asrepresentedby:
Inpractice,foreachquery𝑞,wesample𝑙 documentsasnegative 𝑞
(cid:101)
=G(𝑑;Θ+Θ 𝐿). (6)
examplestoefficientlytrainthedenseretrievalmodelR,andwe
use𝑑 𝑗 − todenotethe 𝑗-thnegativedocuments.Uponcompleting e
T
n
h
h
i
a
s
n
c
c
a
e
p
t
a
h
b
e
ili
p
ty
er
f
f
a
o
c
r
i
m
lit
a
a
n
t
c
e
e
st
o
h
f
e
d
c
e
r
n
e
s
a
e
ti
r
o
e
n
tr
o
ie
f
v
a
al
sy
m
n
o
th
d
e
e
t
l
i
R
cd
.
atasetT𝐺 to
thetrainingofR,nearestneighborsearchtoolssuchasFAISS[21]
canbeemployedtoretrievethetop-𝑛mostrelevantdocumentsfor
4.2 Multi-StageDataFiltering
anygivenquery𝑞withsublinearcomplexity.
DespitethegeneratorG,trainedonannotateddata,iscapableof
Ashighlightedintheintroduction,collectingasufficientnumber
generatinghigh-qualityqueriesforconstructingsyntheticdataset
ofdocument-querypairsfortraininginlow-resourcescenarioscan
T𝐺,ashighlightedinourintroduction,T𝐺 unavoidablyincludes
bechallenging,leadingtosuboptimalretrievalperformance.More-
noisethatmayunderminethetrainingefficacyofthedenseretrieval
over,mostretrievaldatasetscontainavastnumberofunlabeled
modelR.Tomitigatethisconcern,wedevelopamulti-stagedata
documents(i.e.,documentsnotappearinginT𝑡𝑟𝑎𝑖𝑛).Whiledense
filteringmodulethatfocusesonboththequalityofpseudodata
retrievalmodelsperformwellonannotateddocuments,theymay
anditsutilityintrainingR.
struggletoeffectivelyrecalltheseunlabeledones.Toaddressthis
issue,ourstudyintroducesathree-phaseapproach—Generation, 4.2.1 FilteringwithSparseRetrieval. Initially,weemployBM25
Filtering,andTuning—integratedwithaniterativeoptimization forfilteringtheT𝐺.Specifically,foreachpseudodocument-query
strategy,whichsignificantlyenhancestheperformanceofdense pair(𝑞 𝑖 ,𝑑 𝑗) ∈T𝐺,werandomlyselectother𝑚 1documentsD𝑚 =
retrievalmodelsinlow-resourcescenarios. {𝑑𝑚} 𝑚 1 from the corpus D as negative samples. This process
𝑘 𝑘=1
formsacandidatesetD𝑚 ′ ={𝑑 𝑗}∪D𝑚.Inourexperiments,𝑚 1is
4 Methodology setto100.Subsequently,foreach𝑑 𝑘 ∈D𝑚 ′ ,(𝑞 𝑖 ,𝑑 𝑘)isscoredusing
Inthissection,weelaborateonthedetailsoftheiGFTframework, BM25,denotedasBM25(𝑞 𝑖 ,𝑑 𝑘).IfBM25(𝑞 𝑖 ,𝑑 𝑗)yieldsthehighest
incorporatingthreeprocesses:LLM-basedquerygeneration,multi-
score,weretainthispseudo-pairinT𝐺;otherwise,itisexcluded.
stagedatafiltering,andfine-tuningofthedenseretrievalmodel.Ad-
ByapplyingthiscriterionacrossT𝐺,werefineittoT
𝐺
1.
ditionally,weintroduceadynamiciterativeoptimizationstrategy,
4.2.2 FilteringwithDenseRetrieval. Followingtheinitialfiltration
specificallydesignedtorefinethequerygenerator.Theframework
withBM25,whicheliminatessomelower-qualitydocument-query
overviewisdepictedinFigure3.
pairs,werecognizethelimitationofBM25toprimarilylexical-level
relevance.Consequently,wefurtheremployapretraineddense
4.1 LLM-basedQueryGeneration retrievalmodelR𝑝𝑟𝑒 forasecondroundoffiltering.Thissubse-
ToenhancetheperformanceofdenseretrievalmodelR inlow- quentstepseekstocapturenuancedsemanticrelationshipsthat
resourcesettings,recentstudies[4,44]haveleveragedLLMsto BM25mightmiss,ensuringamorediscerningselectionoftraining
generateappropriatequeriesfordocumentswithincorporathat instancesforourdenseretrievalmodelR.
lack sufficient annotations. However, the effectiveness of these Specifically,wefirstleveragetheannotateddataT𝑡𝑟𝑎𝑖𝑛 totrain
methodsreliesheavilyonthedesignofprompts,especiallythe the pretrained dense retrieval model R𝑝𝑟𝑒. In our experiments,
qualityofdocument-queryexamplesusedinin-contextlearning, R𝑝𝑟𝑒 isbasedontheColbertmodel.Subsequently,mirroringthe
whichdonotguaranteetheconsistentgenerationofhigh-quality processoffilteringwithBM25,weconstructcorrespondingnegative
queriesacrossvariedcorpora. samplesforeachquery-documentpair(𝑞 𝑖 ,𝑑 𝑗) ∈ T 𝐺 1.Onlythose
Toaddressthischallenge,weutilizeLlama-2[51],anopen-source pairsrankedastop-1basedonthescoreR𝑝𝑟𝑒(𝑞 𝑖 ,𝑑 𝑗)areselected
LLM,andapplySupervisedFine-Tuning(SFT)onaconstrained toformthefilteredsetT 𝐺 2.Additionally,tofurtherenhancethe
datasetofannotateddocument-querypairs,T𝑡𝑟𝑎𝑖𝑛,todevelopa qualityofT
𝐺
2,wesortallquery-documentpairsindescendingorder
querygenerationmodel,G.Specifically,asillustratedinthetop basedonthescores{R𝑝𝑟𝑒(𝑞 𝑖 ,𝑑 𝑗),∀(𝑞 𝑖 ,𝑑 𝑗) ∈T 𝐺 2}.Weretainonly
leftcornerofFigure3,wefirstconstructtheSFTdatabasedon thetop𝑚 2%ofthesepairstoformthenewfiltereddatasetT
𝐺
3.In
T𝑡𝑟𝑎𝑖𝑛.Subsequently,giventhesubstantialcomputationalresources
ourexperiments,throughparameteranalysis,weretain40%ofT2
requiredforfull-parameterfine-tuning,weoptforLoRA[16],a 𝐺
toensureoptimalperformance.
parameter-efficientfine-tuningtechnique,whichretainsthecore
parametersoftheLLMunchangedandfocusesontrainingrank 4.2.3 FilteringwithLossPredictionModule. Inthepreviousstages,
decompositionmatricesspecifictoeachlayeroftheTransformer ourfocuswasonremovingthenoisydata.Indeed,selectingsamples
architecture.Alongthisline,thelearningobjectiveforthegenerator thatoffermoreinformativevaluetothedenseretrievalmodelR
1376
FromMisstepstoMastery:EnhancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration KDD’25,August3–7,2025,Toronto,ON,Canada
Figure3:TheoverviewarchitectureofourproposediGFTframework.
cansignificantlyenhancethetrainingprocess’seffectiveness.To 4.3.2 IterativeOptimizationStrategy. WhileGcancontinuously
realizethisimprovement,weintroducealosspredictionmodule producenewdatafortrainingthedenseretrievalmodelR,there
aimedatcreatingthefinalfiltereddataset. isnoassurancethatGwillconsistentlygeneratehigh-qualityand
Specifically,giventhefiltereddataT3,totraindenseretrieval informativedatathroughoutthetrainingprocessofR.Figure1
𝐺
modelRmoreeffectively,intuitively,wecanselectinstancesfrom alsoillustratesthatevenfilteringoutlow-qualitytrainingdata,R
T3thatexhibitinghigherlossvalues: rapidlyreachesaperformanceplateau.Toaddressthischallenge,
𝐺
L(R,𝑞 𝑖 ,𝑑 𝑗)=−E 𝑑−∼D,(𝑞𝑖,𝑑−)∉T 𝐺 3 L(R,𝑞 𝑖 ,𝑑 𝑗 ,𝑑−), (7) w up e d d a e t v es el o o u p r ed ge a n n e i r t a e t r o a r tiv G e . o T p h ti i m ss iz tr a a ti t o e n gy st e r n at a e b g le y s th G at to dy a n d a a m pt i i c v a e l l l y y
where (𝑞 𝑖 ,𝑑 𝑗) ∈ T 𝐺 3 and L(R,𝑞 𝑖 ,𝑑 𝑗 ,𝑑−) canbedeterminedby producequeriesthatsignificantlyenhancetheiterativeupdatesof
Equation4.However,duetothehighcomputationalcostofsam-
R,ensuringcontinuousimprovementinretrievalperformance.
plingnegativeinstances𝑑−,weemployamuti-headcross-attention Toclarifyourmethodology,webeginwiththefollowingdefini-
mechanismtoestimateEquation7.Formally,wehave tions:R𝑖𝑛𝑖𝑡 representstheinitialdenseretrievalmodeltrainedon
ℎ
1
=𝑀𝑢𝑙𝑡𝑖𝐻𝑒𝑎𝑑𝐴𝑡𝑡 (cid:0)𝐸 𝑄(𝑞 𝑖),𝐸 𝐷(𝑑 𝑗),𝐸 𝐷(𝑑 𝑗)(cid:1),
t
T
h
𝑡𝑟
e
𝑎
fi
𝑖𝑛
r
;
st
G
i
1
t
,
e
d
ra
e
t
r
i
i
o
v
n
ed
of
fr
t
o
h
m
eu
tr
p
a
d
i
a
n
t
i
e
n
d
g
g
o
e
n
n
t
e
h
ra
e
t
S
o
F
r;
T
T
d
4
ata
d
,
e
is
no
id
te
e
s
nt
t
i
h
fi
e
e
s
d
y
a
n
s
-
(8) 𝐺,1
ℎ 2 =𝑓(ℎ 1 ), 𝑦 𝑞𝑖,𝑑𝑗 =𝑚𝑒𝑎𝑛_𝑝𝑜𝑜𝑙𝑖𝑛𝑔(ℎ 2 ), theticdataaftermulti-stagefiltering;andR 1,fine-tunedusingT
𝐺
4
,1
whereℎ
1
∈R|𝑞𝑖|×𝑘 3,ℎ
2
∈R|𝑞𝑖|×1,𝑀𝑢𝑙𝑡𝑖𝐻𝑒𝑎𝑑𝐴𝑡𝑡(·,·,·)represents fromR𝑖𝑛𝑖𝑡,isrecognizedasthefirstiterationoftheupdateddense
themulti-headattentionnetwork, 𝑓(·) isalearnablemultilayer retrievalmodel.Alongthisline,wedenotethegenerator,synthetic
perceptron network, and 𝐸 𝑄 and 𝐸 𝐷 denote the document and
data,andretrieverupdatedinthe𝑡-thiterationthroughouritera-
queryencodersofR,respectively.Byuniformlysamplingasetof
tiveoptimizationstrategyasG𝑡,T
𝐺
4
,𝑡
,andR𝑡,respectively.Indeed,
t ( h 𝑞 e 𝑖 ,𝑑 lo 𝑗 s ) s ∈ pr T e 𝐺 d 3 i , c d ti e o n n o m te o d d a u s le T 𝐺 b 3 y ′ , m w i e ni c m an izi e n s g tim th a e te fo t l h lo e w p i a n r g am lo e ss te : rsin o to ur en p a r b im le a t r h y e m sy o n t t i h v e a t t i i c on da f t o a r T i 𝐺 t 4 e ,𝑡 ra to tiv in e c ly lu u d p e d m at o i r n e g ( t 𝑞 h 𝑖 , e 𝑑 g 𝑗 e ) n p e a r i a rs to t r ha is t
challengeR𝑡−1,specificallythosewithahighL(R𝑡−1 ,𝑞 𝑖 ,𝑑 𝑗).To
∑︁ (cid:16) (cid:17)2
L𝑙𝑝 = 𝑦 𝑞𝑖,𝑑𝑗 −L(R,𝑞 𝑖 ,𝑑 𝑗) . (9) thisend,wedeveloparewardmodelandemployproximalpolicy
(𝑞𝑖,𝑑𝑗)∈T
𝐺
3′ optimization(PPO)-basedreinforcementlearning(RL)toenhance
thequerygenerator.
Subsequently,wecalculateandsortall𝑦 𝑞𝑖,𝑑𝑗 ,where(𝑞 𝑖 ,𝑑 𝑗) ∈T 𝐺 3, Reward Model Learning Phase: The objective of the reward
indescendingorder.Weretainthetop𝑚 3ofthesepairs,whichwe modelV𝑡at𝑡-thiterationistoassignscorestoany(𝑞 𝑖 ,𝑑 𝑗),ensuring
identifyasthemostinformativeinstancesforoptimizingthedense thatthepairswithahigherL(R𝑡−1 ,𝑞 𝑖 ,𝑑 𝑗)achievehigherscores.
retrievalmodel,tocomposethefinalfiltereddatasetT
𝐺
4. ThearchitectureofV𝑡 issimilartothatofthegeneratorG,but
replacesthefinaloutputlayerwithalinearpredictionheadthat
4.3 TuningandIterativeOptimization outputsscalarrewardvalues.Additionally,therewardmodelis
4.3.1 Fine-TuningDenseRetrievalModel. AsintroducedinSection
initializedwiththeparametersofthegeneratorG.Weleverage
3,thedenseretrievalmodelcanbetrainedusingEquations3and4. T 𝐺 4 ,𝑡−1 to construct a dataset comprised of paired comparisons
Giventheannotatedtrainingdataset T𝑡𝑟𝑎𝑖𝑛,weinitiallytraina betweentworesponsesfromG𝑡−1andemployapairwiseranking
denseretrievalR𝑖𝑛𝑖𝑡.Subsequently,leveragingthesyntheticdata losstotrainV𝑡 inthefollowingmanner:
T4generatedbyourquerygenerationmodelGandrefinedthrough
𝐺
o
a
u
m
r
u
e
l
n
ti
h
-s
a
t
n
a
c
g
e
e
d
fi
d
lt
e
e
n
ri
s
n
e
g
r
p
et
r
r
o
i
c
e
e
v
s
a
s
l
,
m
we
od
fu
e
r
l
t
R
he
.
rfine-tuneR𝑖𝑛𝑖𝑡toproduce
L𝑟𝑚 =−E (𝑞𝑖,𝑞𝑘,𝑑𝑗)∼T𝑟𝑚,𝑡 log𝜎(V𝑡(𝑞 𝑖 ,𝑑 𝑗)−V𝑡(𝑞 𝑘 ,𝑑 𝑗)). (10)
1377
KDD’25,August3–7,2025,Toronto,ON,Canada ZhenyuTongetal.
𝜎 denotestheactivationsigmoidfunction.T𝑟𝑚,𝑡 = {(𝑞 𝑖 ,𝑞 𝑘 ,𝑑 𝑗)}, 5 Experiments
where (𝑞 𝑖 ,𝑑 𝑗) ∈ T 𝐺 4 ,𝑡−1 , (𝑞 𝑘 ,𝑑 𝑗) ∈ T 𝐺 4 ,𝑡−1 , and𝑦 𝑞𝑖,𝑑𝑗 > 𝑦 𝑞𝑘,𝑑𝑗 . 5.1 ExperimentalSetting
𝑦 𝑞𝑖,𝑑𝑗 iscalculatedbythelosspredictionmoduleinSection4.2.3.
5.1.1 Datasets. TovalidatetheeffectivenessoftheproposediGFT
PPO-basedRLFine-TuningPhase:Wefirstusequerygener-
a a t n o d r c G r 𝑡 it − ic 1 m an o d d r e e l w V a 𝑐 rd .D m u o r d in e g lV th 𝑡 e to RL in fi it n ia e l - i t z u e n t i h n e g, a w ct e or sa m m o p d l e e l t G h 𝑎 e i B n E l I o R w b - e re n s c o h u m rc a e rk se [ t 5 ti 0 n ] g t s o ,w co e n s s e t l r e u c c t t ed ou a r s e e x ri p e e s r o im fd en at t a s s . e S t p s e f c r i o fi m ca t l h ly e ,
wefirstselecteddatasetsfromBEIRthatincludedocument-query
d ag o e cu G m 𝑎 e t n o t g 𝑑 e 𝑗 n ∈ era D te 𝐺 4 q ,𝑡 u − e 1 ry = ,d { e ∀ n 𝑑 o 𝑗 t , e 𝑠 d .𝑡. a ∃ s ( 𝑞 𝑞 (cid:101)𝑖 𝑖 . ,𝑑 T 𝑗 h ) en ∈ , T th 𝐺 4 e ,𝑡 r − e 1 w } a a r n d d c l a e n ve b r e - t
e
r
x
a
p
in
er
in
im
g
e
d
n
a
t
t
a
a
l
,
s
s
e
u
t
c
u
h
p
a
o
s
f
F
S
i
P
Q
T
A
A
,
R
M
[
S
3
M
7]
A
,u
R
s
C
in
O
g
,
o
a
n
n
l
d
y
N
50
Q
0
.
d
W
o
e
cu
fo
m
ll
e
o
n
w
t-
e
q
d
ue
th
ry
e
formulatedasfollows:
pairsasthetrainingsettosimulatethelow-resourceconditions.In
additiontothestandardlow-resourcescenariosmentionedabove,
𝑟 𝑞 (cid:101)𝑖,𝑑𝑗 =V𝑡(𝑑 𝑗 ,𝑞 (cid:101)𝑖)−𝜆log (cid:0)𝑝(𝑞 (cid:101)𝑖|𝑑 𝑗 ,G 𝑎 )/𝑝(𝑞 (cid:101)𝑖|𝑑 𝑗 ,G𝑡−1 )(cid:1), (11) wefollowedtheBEIRbenchmarktovalidatethemodel’szero-shot
performance.DetaileddescriptionsofeachdatasetinBEIRcanbe
where𝜆isthecoefficientfortheKL-divergencetermthatisused foundinAppendixA.1.
tolimittherangeofchangesinthepolicyduringeachupdate[35].
5.1.2 EvaluationMetrics. Theevaluationofdocumentretrievalper-
Meanwhile,theadvantagevalueisthedifferencebetweenreward
formancereliesonassessingtherankingquality,measuredthrough
𝑟 andthevalueoftheinput𝑑 𝑗 estimatedbythecriticmodelas:
𝑎 in 𝑞 (cid:101)𝑖 𝑞 (cid:101) ,𝑘 𝑖 ,𝑑 .T 𝑗 h = e 𝑟 n 𝑞 (cid:101) , 𝑖 w ,𝑑𝑗 e − ca V n 𝑐 o ( p 𝑑 t 𝑗 i , m 𝑞 (cid:101)𝑖 i , z < e 𝑘 t + h 1 e ), a w ct h o e r re m 𝑞 (cid:101) o 𝑖, d 𝑘 e d l e G n 𝑎 ot b e a s s t e h d e o 𝑘 n -t : htoken m N Re o e c r t i r m p ic r a s o li c i z n a e c l d l R u D d a i n i s n k c g o ( u M M n e R t a e R n d ) C A [2 v u 9 e m ] r . a u g I la n e te P th d re i G s ci a p s i a i n o p s n e ( r ( N , M D w A C e P G r ) e ) [ p 2 [ o 2 9 9 r ] t , ], R t a h e n e c d a t l o M l p [ e 2 - a 1 9 n 0 ],
retrievalperformanceemployingtheabovemetrics—specifically,
L𝑝𝑝𝑜 =E 𝑞 (cid:101) 𝑑 𝑖 𝑗 ∼ ∼ G D 𝑎 𝐺 4 ( , 𝑑 𝑡− 𝑗 1 ) 𝑞 (cid:101)𝑖 ∑︁ ,𝑘∈𝑞 (cid:101)𝑖 min (cid:18) 𝑝 𝑝 (𝑞 (cid:101) (𝑞 (cid:101) 𝑖, 𝑖 𝑘 ,𝑘 |𝑑 |𝑑 𝑗 , 𝑗 𝑞 (cid:101) ,𝑞 (cid:101) 𝑖, 𝑖 < ,< 𝑘 𝑘 , , G G 𝑡− 𝑎 1 ) ) 𝑎 𝑞 (cid:101)𝑖,𝑘,𝑑𝑗 , M 5.1 A .3 P@ I 1 m 0 p ,R le e m ca en ll t @ at 1 io 0, n N D D e C ta G il @ s. 1 I 0 n , t a h n e d q M u R er R y @ g 1 e 0 n . erationphaseof
clip (cid:18) 𝑝 𝑝 (𝑞 (cid:101) (𝑞 (cid:101) 𝑖, 𝑖 𝑘 ,𝑘 |𝑑 |𝑑 𝑗 , 𝑗 𝑞 (cid:101) ,𝑞 (cid:101) 𝑖, 𝑖 < ,< 𝑘 𝑘 , , G R 𝑡− 𝑎 1 ) ) ,1−𝜀,1+𝜀 (cid:19) 𝑎 𝑞 (cid:101)𝑖,𝑘,𝑑𝑗 (cid:19) , i t G he FT A , d w a e m u W tili o z p ed tim Ll i a z m er a- w 2 i a th st a he le g a e r n n e in ra g ti r v a e te m o o f d 5 e 𝑒 l. − In 5 th w e a S s F u T ti s l t iz a e g d e, .
Thetrainingspannedacross3epochs,withabatchsizesetto4,
(12)
incorporatingtheLoRA[16]techniquetoachieveparametereffi-
ciency.Pleasenotethatinzero-shotscenarios,suchasArguana,
wherefunctionclip(𝑥,1−𝜀,1+𝜀)limitsthevalueof𝑥 between
(1−𝜀,1+𝜀).Finally,thecriticmodelV𝑐
isoptimizedwithloss
duetothelackofdocument-querytrainingdata,weskippedthe
function:L𝑐 =E (𝑞 (cid:101)𝑖,𝑑𝑗) (𝑟 𝑞 (cid:101)𝑖,𝑑𝑗 −V𝑐(𝑑 𝑗 ,𝑞 (cid:101)𝑖))2. S u F se T d p t r h oc e e o ss ri f g o i r n t a h l e L L la L m M a -b -2 as m ed o q d u el er a y s g G en . e M ra e t a io n n w m hi o le d , el d a u n r d in i g ns e t a e c a h d
Difficulty-GuidedLearningStrategy:Byleveragingthereward
iterationoftheoptimizationprocess,wesetthelearningrateas
modelandPPO-basedRLalgorithm,wecanupdatethequerygener- 1𝑒 −7totraintherewardmodelandupdatethegenerator.The
atorfromG𝑡−1toG𝑡.Additionally,toimprovetheeffectivenessof batchsizeduringthisphasewasestablishedat8,andthe𝜆inthe
theRLalgorithm,weintroduceadifficulty-guidedlearningstrategy, PPO-basedRLfine-tuningstagewasfixedat0.95.Intheprocessof
sothatG𝑡 canexhibitbetterperformance.
filteringwithsparseretrieval,weemployedtheBM25algorithm,
ConsideringthevaryingcapabilitiesofgeneratorG𝑡−1topro- adjustingtheparametersto𝑏 =0.75and𝑘 =1.5,setting𝑚
1
=100
duce informative queries for different documents, the difficulty
tosievethroughthesyntheticdataforquality.Concurrently,for
facedbytheRLprocesstofurtherenhanceG𝑡−1togeneratemore
thedenseretrieval-basedfilteringphase,weselectedthehighest-
i s n y f n o t r h m et a i t c iv d e at q a u T e 𝐺 r 4 i , e 𝑡 s − v 1 , a w rie e s e a s c ti r m os a s te do th cu e m di e ffi n c ts u . l S ty pe o c f ifi do ca c l u ly m , e g n iv t e 𝑑 n 𝑗 t f h o e r s a c s o m ri e n e g ti 𝑚 ng 2 = th 4 e 0 fi % lt o e f r’ T s 𝐺 c 1 u a t s -o d ff e . te F r u m rt i h n e e r d m b o y re R , 𝑝 w 𝑟𝑒 it , h d i e n si t g h n e a p ti r n o g ce t s h s es o e f
PPOby filteringwiththelosspredictionmodule,weset𝑚
3
=40%toobtain
thefinalfiltereddataT4.Inaligningwiththeexperimentalsetup
𝐺
𝑟𝑎𝑛𝑘
diff(𝑑 𝑗)=
|{(𝑞 𝑖 ,𝑑 𝑗)
1
∈T 𝐺 4 ,𝑡−1 }| (𝑞𝑖,𝑑𝑗
∑︁
)∈T
𝐺
4
,𝑡−1
R𝑡−1 (𝑞
𝑞
𝑖
𝑖,
,
𝑑
𝑑
𝑗
𝑗)
, (13) o
32
fS
a
P
n
T
d
A
a
R
dh
,t
e
h
re
e
d
C
t
o
o
lB
a
E
le
R
a
T
rn
in
in
i
g
G
r
F
a
T
te
w
o
a
f
s
2𝑒
tr
−
ain
5.
edusingabatchsizeof
5.2 PerformanceintheLow-ResourceSetting
whereR𝑡−1 (𝑞 𝑖 ,𝑑 𝑗)representstherelevancescoreof(𝑞 𝑖 ,𝑑 𝑗)calcu- 5.2.1 BaselineApproaches. ToevaluatetheeffectivenessofiGFTin
latedbythe(𝑡−1)-thiterationdenseretrievalmodeland𝑟𝑎𝑛𝑘
𝑞𝑖,𝑑𝑗 thelow-resourcesetting,wemeticulouslyselectedarangeofcom-
denotestherankingof𝑑 𝑗 withinallthedocumentsinthecorpusD, petitivebaselinemodelsforcomparison.Theseinclude:(1)Sparse
determinedbydescendingorderofR𝑡−1 (𝑞 𝑖 ,𝑑 𝑗).Indeed,diff(𝑑 𝑗) retrievalmethods:BM25[43]anditsvariantBM25-tuned[3],em-
effectivelyestimatesthecurrentgeneratorcapacitytogeneratein- ployingaLuceneindexforenhancedretrievalefficiency;(2)Dense
formativefor𝑑 𝑗.Thus,ahigherdiff(𝑑 𝑗)suggeststhatthegenerator
retrievalmodelviasupervisedlearningwithlowresourcedata:Col-
G𝑡−1facesgreaterchallengesinfurtherimprovement.Alongthis
BERT[24];and(3)Denseretrievalmodeltrainedviaunsupervised
line,duringthePPO-basedRLfine-tuningprocess,insteadofusing learning:ICT[26],MSS[45],andContriever[18].Moreover,wein-
randomdatashufflingonD 𝐺 4 ,𝑡−1 ,wesequencethedatabasedon corporatedcutting-edgeLLM-basedquerygenerationmethodsthat
thedifficultyleveldifffromlowertohigherforallthe𝑑 𝑗 ∈D 𝐺 4 ,𝑡−1 . aimtoenhancedenseretrievalmodels,includingDoc2Query[34],
1378
FromMisstepstoMastery:EnhancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration KDD’25,August3–7,2025,Toronto,ON,Canada
Table1:Theperformancesinthelow-resourcesettingofourmodelandbaselines.Theorderofthetop10predictionswas
consideredinNDCG,MAP,Recall,andMRR.Thebestresultsareinbold,andthesecond-bestresultsareinunderscored.
Datasets FiQA MSMARCO NQ
Metrics NDCG MAP Recall MRR NDCG MAP Recall MRR NDCG MAP Recall MRR
BM25 0.1113 0.0697 0.1913 0.1103 0.0343 0.0151 0.1009 0.0158 0.0789 0.0721 0.0914 0.0800
BM25-tuned 0.2361 0.1784 0.2951 0.2889 0.2084 0.1712 0.3787 0.1733 0.2855 0.2454 0.4555 0.2634
ColBERT 0.1149 0.0820 0.1547 0.1675 0.0786 0.0619 0.1301 0.0639 0.2560 0.2029 0.4015 0.2225
ICT 0.1955 0.1515 0.2278 0.2585 0.1389 0.1095 0.2112 0.0980 0.2601 0.1917 0.4012 0.2077
MSS 0.1660 0.1219 0.2167 0.2067 0.1465 0.1180 0.2344 0.1212 0.2414 0.1892 0.3875 0.2047
Contriever 0.2536 0.2002 0.2994 0.3259 0.2056 0.1578 0.3568 0.1611 0.2538 0.1970 0.4128 0.2155
Doc2Query 0.1884 0.1392 0.2362 0.2327 0.1827 0.1503 0.3671 0.1702 0.2648 0.2060 0.4673 0.2216
Doc2Query-- 0.2173 0.1676 0.2712 0.2416 0.2044 0.1758 0.3955 0.1818 0.2829 0.2359 0.4938 0.2529
DocT5Query 0.2046 0.1586 0.2385 0.2530 0.2026 0.1717 0.3914 0.1848 0.2767 0.2110 0.4661 0.2264
GPL 0.2019 0.1513 0.2335 0.2431 0.2009 0.1751 0.3917 0.1837 0.2641 0.2017 0.4721 0.2134
UDAPDR 0.1732 0.1333 0.2185 0.2240 0.2012 0.1392 0.2208 0.1377 0.2620 0.2091 0.4503 0.2170
InPars 0.2574 0.2024 0.3051 0.3179 0.1821 0.1444 0.2991 0.1480 0.3097 0.2531 0.4624 0.2701
InPars-v2 0.2714 0.2158 0.3283 0.3565 0.1890 0.1532 0.2999 0.1566 0.3412 0.2963 0.4892 0.3515
SPTAR 0.2688 0.2103 0.3083 0.3039 0.2185 0.1872 0.3662 0.1704 0.3007 0.2517 0.4613 0.2607
Promptagator 0.2351 0.1752 0.2737 0.2725 0.2007 0.1725 0.3927 0.1867 0.2814 0.2315 0.4894 0.2460
ChatGPT 0.2697 0.2076 0.2512 0.2507 0.2131 0.1828 0.3987 0.1974 0.2977 0.2417 0.5023 0.2567
Ours 0.3042 0.2415 0.3666 0.3731 0.2550 0.2044 0.4108 0.2085 0.4252 0.3898 0.5796 0.4222
𝐼𝑚𝑝𝑟𝑜𝑣𝑒. +12.09% +11.91% +11.67% +4.66% +16.70% +9.19% +3.03% +5.62% 24.62% +31.56% +15.39% +20.11%
0.30 0.25
0.20
100%80%60%40%20%
01@GCDN
FiQA
0.20
0.15
100%80%60%40%20%
01@PAM
FiQA
0.35 0.30
0.25
100%80%60%40%20%
01@llaceR
FiQA
0.35 0.30
0.25
100%80%60%40%20%
01@RRM
FiQA
0.24 0.22
0.20
100%80%60%40%20%
01@GCDN
MSMARCO 0.20
0.18
0.16
100%80%60%40%20%
01@PAM
MSMARCO 0.400
0.375
0.350
0.325
100%80%60%40%20%
01@llaceR
MSMARCO 0.20
0.18
0.16
0.14
100%80%60%40%20%
01@RRM
 L * ) 7 w/o  6 5  	  ' 5  L * ) 7 w/o  / 3 iGFT
MSMARCO
Figure4:ComparisonofiGFT,iGFTw/oLP,andiGFTw/oSR&DRundervariousparametersettings.
0.32
0.30
0.28
0.26
1 2 3 4 5
01@GCDN
FiQA
0.24
0.22
0.20
1 2 3 4 5
01@PAM
FiQA 0.375
0.350
0.325
0.300
1 2 3 4 5
01@llaceR
FiQA
0.35
0.30
0.25
1 2 3 4 5
01@RRM
FiQA 0.26
0.24
0.22
1 2 3 4 5
01@GCDN
MSMARCO
0.20
0.18
1 2 3 4 5
01@PAM
MSMARCO 0.42
0.41
0.40
0.39
0.38
1 2 3 4 5
01@llaceR
MSMARCO
0.22
0.20
0.18
1 2 3 4 5
01@RRM
 L * ) 7 w 1  L * ) 7 w  5 ' 6 iGFT
MSMARCO
Figure5:ComparisonofiGFT,iGFTwG 1,andiGFTwRDSatdifferentiterations.
Doc2Query--[11],DocT5Query[33],GPL[52],InPars[4],InPars- observations:(1)OuriGPTconsistentlyoutperformsallbaseline
v2[19],UDAPDR[44],Promptagator[8],andSPTAR[37].Further- modelsacrosseverydataset,markingsignificantadvancements.
more,weutilizedChatGPTforthequerygenerationprocessfor Specifically,comparedtothebestperformancesofallbaselines
comparativeanalysis.Inourexperimentalsetup,weappliedboth acrossvariousmetrics,ouriGFTachievesanaverageimprovement
ouriGFTandaboveLLM-basedmethodstoapre-trainedColBERT, of17.80%,17.55%,10.03%,and10.13%ontheNDCG@10,MAP@10,
whichensuredafairanddirectcomparisonofperformance. Recall@10,andMRR@10,respectively,acrossthethreedatasets.
(2)WecanobservethatColBERT,relyingonsupervisedlearning,
doesnotoutperformallsparseretrievalmethods.Thisindicatesthat
5.2.2 ExperimentalResults. Table1showcasesthecomparative
denseretrievalmodelstrainedsolelyonannotateddatastruggleto
performance analysis of the proposed iGFT framework against
effectivelyhandledocumentretrievaltasksinlow-resourcesettings.
baselinemodelsontheFiQA,MSMARCO,andNQdatasets.We
(3)Theunsuperviseddenseretrievalapproaches,includingICT,
highlightedthebestresultsinboldfaceandunderlinedthesub-
MSS,andContriever,whichtrainmodelsbyconstructingpseudo
optimalresults.Accordingtotheresults,therearethefollowing
1379
KDD’25,August3–7,2025,Toronto,ON,Canada ZhenyuTongetal.
Table2:TheperformancecomparisonofourmodelandbaselinesonNDCG@10inthezero-shotsetting.InPars-v2*,LaPraDoR*,
andOurs*respectivelyrepresenttheperformancesafteraddingarerankertothecorrespondingoriginaldenseretrievalmodel.
Models QGen LameR DRAD InPars-v2 Query2Doc HyDE CSQE SPAR LaPraDoR Ours InPars-v2* LaPraDoR* Ours*
ArguAna 0.4934 0.4021 0.4975 0.4725 0.4146 0.4662 0.4034 0.4591 0.5072 0.5105 0.4690 0.5274 0.5883
DBPedia-Entity 0.3281 0.3957 0.4180 0.4192 0.4247 0.3682 0.4137 0.4275 0.4189 0.4624 0.4982 0.4904 0.5123
TREC-Covid 0.6083 0.7481 0.7372 0.7184 0.7384 0.5933 0.7422 0.7326 0.7389 0.7712 0.8462 0.8518 0.8794
FiQA 0.3082 0.2580 0.3382 0.3243 0.2912 0.2768 0.2794 0.3258 0.3290 0.3628 0.5092 0.4973 0.5202
SciFact 0.6429 0.7251 0.6928 0.6825 0.7172 0.6916 0.6978 0.6962 0.6882 0.7430 0.7742 0.7523 0.7962
Table3:Theperformancesinthefully-supervisedsettingofourmodelandColBERT.
Datasets FiQA MSMARCO NQ
Metrics NDCG MAP Recall MRR NDCG MAP Recall MRR NDCG MAP Recall MRR
ColBERT 0.3312 0.2578 0.3782 0.4193 0.3837 0.3381 0.5127 0.3454 0.5280 0.4169 0.6591 0.4382
Ours 0.3572 0.2872 0.3968 0.4312 0.4016 0.3505 0.5680 0.3589 0.5412 0.4557 0.7094 0.4862
(𝑞,𝑑) pairs, utilizing strategies that include segment extraction 5.4 AnalysisofIterativeOptimization
fromdocuments,haveeffectivelyenhancedmodelperformance. Wefurtherinvestigatedtheeffectivenessoftheproposediterative
Contriever,inparticular,outperformssparseretrievalmodelsacross optimizationstrategy.Specifically,weintroducedtwovariantsof
amajorityofmetricsontheFiQAdatasetandachievescompetitive ourapproach:(1)iGFTwG 1,whichmaintainsastaticgenerator,
performanceontheMSMARCO.(4)Allenhanceddenseretrieval i.e.,G 1(trainedontheSFTdata),throughouttheiterativelearning
approachesleveragingLLM-basedquerygeneration,includingour processofiGFT;(2)iGFTw RDS,whichadoptsarandomdata
iGFTframework,achievesuperiorperformancecomparedtoprevi- shufflemethodinsteadoftheproposeddifficulty-guidedlearning
ousbaselinemodels.ThisverifiesthecapabilityofLLMstoboost strategyforimplementingPPOalgorithmtoupdatethegenerator.
denseretrievalinlow-resourcescenariosthroughadataaugmen- Figure5presentstheperformanceofouriGFTanditsvariantsat
tationperspective.Furthermore,ourapproachoutperformsthese differentiterations.Westandardizedthequantityofdatagenerated
state-of-the-artLLM-basedapproaches,therebydemonstratingthe periterationby G𝑡,ensuringthat |G𝑡| remainsconstant.Thex-
effectivenessofouriGFTframework.Furthermore,ourexperimen- axisdenotestheiterationnumber,withthegeneratorsettoG 1at
talresultsonNFCorpusandSciFactalsodemonstratethatouriGFT thefirstiteration.ResultsillustratedinFigure5revealthatiGFT
canachievebetterperformance.Duetospaceconstraints,these significantlyimprovesretrievalperformanceviaadaptiveupdates
resultsarepresentedinAppendixA.3. tothegeneratorthroughouttheiterativeprocess.Furthermore,the
implementationoftheproposeddifficulty-guidedlearningstrategy
inthePPOalgorithmsubstantiallyelevatesiGFT’sperformance.
5.3 AnalysisofFilteringStrategies
Furthermore,thetimecostanalysisoftheiterativeoptimizationis
Toevaluatetheimpactofdifferentcomponentswithinourmulti- presentedinAppendixA.2.
stagefilteringphase,weintroducedtwovariantsofouriGFT:(1)
iGFTw/oLP,whichexcludesthelosspredictionmoduleforselect-
5.5 PerformanceintheZero-ShotSetting
ingsyntheticdatathatoffermoreinformativevaluefortraining
thedenseretrievalmodel,asdetailedinSection4.2.3;(2)iGFT Weselectedseveralcompetitivebaselinemodelsknownfortheir
w/oSR&DR,whichremovestheprocessesdescribedinSections effectivenessinzero-shotscenarios,including(1)query-generation
4.2.1-4.2.2forfilteringoutlow-qualitydataviaBM25andR𝑝𝑟𝑒. methods:QGen[30],LameR[48]andDRAD[15],whichfocuson
Wereportedtheperformanceofourapproachanditstwovari- generatingdomain-specificdatausingpre-trainedmodelswithout
antsFiQAandMSMARCOinFigure4,withthesettingof𝑚
2
=𝑚
3
anytrainingdata;(2)queryexpansionmethods:Query2Doc[53],
rangingfrom100%to20%.As𝑚 2and𝑚 3valuesincrease,thefiltered HyDE[10]andCSQE[27],whichenhancequerycontentbygen-
databecomemoreclosertotheoriginalsyntheticdata.Notably, eratingadditionalinformationtoexpandtheoriginalquery;and
when𝑚
2
=𝑚
3
=100%,symbolizingascenariodevoidofanyfil- (3)knowledgedistillationmethods:SPAR[7]andLaPraDoR[55].
teringprocesses,BM25filteringisnotimplemented.Asillustrated Additionally,wecomparedtheperformanceofdifferentmodels
in Figure 1, we observed a decline in model performance upon after incorporating a reranker. Specifically, we followed InPars-
theremovalofanycomponent,underscoringtheimportanceof v2[19],utilizingapre-trainedmonoT5-3Bmodel[32]forreranking.
consideringboththequalityofthegenerateddataanditsinfluence
onthedenseretrievalmodel’strainingwithinthefilteringprocess. 5.5.1 ExperimentalResults. InTable2,wepresentacomparative
Furthermore,wedeterminedthataconfigurationof𝑚 2 =𝑚 3 =40% performanceanalysisoftheproposediGFTmethodandbaseline
yieldsoptimalresults.Consequently,weadoptedthissettingfor modelsontheArguAna,DBPedia-Entity,TREC-Covid,FiQA,and
ouriGFTintheexperiments. SciFactdatasets.Theexperimentalresultsshowthatourmethod
1380
FromMisstepstoMastery:EnhancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration KDD’25,August3–7,2025,Toronto,ON,Canada
Table4:CasestudyofquerygenerationbasedonFiQAdataset.
Document𝑑(ID:527311) Sohere’sthethingthateveryoneseemstoforget:IboughtNetflixtowatchMOVIES.Originalcontentisgreatandall
buttheystartedofftryingtoprovideaserviceandthenjustabandonedthatservicetoessentiallybecometheirownTV
network.IfI’mboredathomeandwanttowatchAFewGoodMen,forexample,Ican’tfireupmyNetflixsubscription
soI’mofftothevideostoreinstead,whichisexactlythethingIwastryingtoavoidbysubscribingtoNetflix.
Generatedquery𝑞(associatedwithhigh𝑦𝑞,𝑑) IsNetflixworthitifIneverwatchstreamingmovies?
Generatedquery𝑞(associatedwithlow𝑦𝑞,𝑑) What’stheproblemonNetflixifIwanttowatchAFewGoodMen?
Document𝑑(ID:77792) Andthat’sfine,it’sTHEIRnetworkthatmayormaynotprovideInternetaccess,theycandowhattheywantwith
yourdata(redirectrequestsorblockcertainaccess)whileyou’reusingitjustaslandownerscantellyouwhereyou
cangoandwhatyoucandoontheirland.Sure,it’sshitty,butit’stheirrighttobeshittyaboutit.Ifyoudon’twantto
besubjecttothat,don’tconnecttotheirWiFinetwork.
Generatedquery𝑞(associatedwithhigh𝑦𝑞,𝑑) Whatarethedangersofconnectingtoanetwork?
Generatedquery𝑞(associatedwithlow𝑦𝑞,𝑑) Whatcananetworkadministratordotomelikealandowner?
consistentlyachievesthebestperformance.Additionally,themod-
els’performanceimprovestovaryingdegreeswiththeadditionof Figure 6: Distribution of diff(𝑑) cal-
areranker.Duetospaceconstraints,theresultsfortheremaining culated from different synthetic data
datasetsintheBEIRbenchmarkareprovidedinAppendixA.3. T(cid:102)4𝐺,1andT(cid:102)4𝐺,2,whichcraftedbygen-
eratorsG 1 andG 2,respectively.Itcan
5.6 PerformanceintheFully-SupervisedSetting beobservedthatouriterativelyupdated
generatorismorelikelytoproducesam-
To further demonstrate the effectiveness of iGFT, we evaluated
pleswithhigherdiff(𝑑).
itsperformanceusingfullysuperviseddata.Unliketheprevious
low-resourceexperiments,wherewesampledtrainingdatafrom
FiQA,MSMARCO,andNQ,weusedthecompletetrainingdatato derivedT(cid:102)4𝐺,1andT(cid:102)4𝐺,2.Figure6presentsthedistributionofdiff𝑑,
construct|T𝑡𝑟𝑎𝑖𝑛|.TheexperimentalresultsinTable3showthat
foreach𝑑 ∈D,computedfromT(cid:102)4𝐺,1andT(cid:102)4𝐺,2,respectively.The
evenwithsufficienttrainingdata,ourframeworkstillenhancesthe
resultsindicatethattheiterativetrainingofourgeneratorsignifi-
performanceofthedenseretrievalmodel.
cantlyimprovesthelikelihoodofgeneratinghigh-qualityandinfor-
mativesyntheticqueries,therebyvalidatingtheeffectivenessofthe
5.7 CaseStudy
iterativeoptimizationstrategyinenhancingtheoverallframework.
Toenableamoreintuitiveanalysisofthedataqualityproducedby
ourquerygeneratorG𝑡 forfine-tuningthedenseretrievalmodel, 6 Conclusion
thiscasestudypresentsexamplesofthegeneratedqueriesforthe Inthispaper,weintroducediGFT,anovelframeworkaimedaten-
FiQAdataset.AsillustratedinTable4,ourquerygeneratorG𝑡 is hancinglow-resourcedenseretrievalbyintegratingathree-phase
capableofproducingqueriestailoredtodifferentdocuments.For process—Generation,Filtering,andTuning—coupledwithanitera-
instance,document#527311outlinesreasonsausermightchoose tiveoptimizationstrategy.Tobemorespecific,wefirstemployed
nottorenewtheirNetflixsubscription,primarilyduetotheinabil- anLLMtogenerateappropriatequeriesfordocumentswithsu-
itytowatchnon-NetflixOriginalcontent,suchas“AFewGood pervisedfine-tuningonlimitedgroundtruthdata.Subsequently,
Men”.Thegeneratedqueriesdemonstratesubstantialrelevance amulti-stagefilteringmodulewaspresenttomitigatenoisydata
tothedocument𝑑,furthervalidatingtheeffectivenessofthesyn-
whileselectingsamplesthatnotablyenhancetheperformanceof
theticdatainenhancingthetrainingprocessofthedenseretrieval denseretrievalmodels.Toproducemoreinformativequeries,wede-
model.Notably,thefirstgeneratedqueryexhibitsahigher𝑦
𝑑,𝑞 visedanoveliterativeoptimizationstrategycapableofdynamically
valuecomparedtothesecond.Thesecondquerydirectlytargets refiningtheLLM-basedquerygenerator.Thisstrategyfacilitated
thekeyword“AFewGoodMen"fromthedocument,whilethefirst thegradualenhancementoftheinformationretrievalcapabilities
requiresadegreeofinferencetoformulateananswerbasedonthe oftheentireframework.Finally,extensiveexperimentsconducted
document’scontent,posingagreaterchallengefortheretrieval onseveralpubliclyavailableretrievalbenchmarkdatasetshave
model.Consequently,inouriGFTframework,weimplementan demonstratedtheeffectivenessoftheproposediGFT.
iterativeoptimizationstrategytoupdatethegenerator,encourag-
ingittoproducesuchchallenginginstances,therebysignificantly Acknowledgments
improvingtheperformanceofthedenseretrievalmodel.
ThisworkwaspartiallysupportedbytheNationalNaturalScience
Subsequently,wedemonstratedthatouriterativelyoptimized
Foundation of China (No.92470204), the Fundamental Research
generatormoreeasilyproducesinformativesyntheticdatafordense
ProjectofCNIC(No.E4552304),thePostdoctoralFellowshipPro-
retrievalmodelscomparedtoastaticgenerator.Specifically,we
gramofCPSF(No.GZC20232811),andtheChinaPostdoctoralSci-
usedboththeinitialgeneratorG 1anditsiterativelyupdatedversion,
enceFoundation(No.2024M753357).
G 2(afteroneiteration),togenerate10queriesforeachdocument
𝑑 ∈D.Thisprocessproducedtwocorrespondingsyntheticdatasets
T(cid:101)𝐺,1andT(cid:101)𝐺,2.Afterapplyingourmulti-stagefilteringprocess,we
1381
KDD’25,August3–7,2025,Toronto,ON,Canada ZhenyuTongetal.
References
MethodsinNaturalLanguageProcessing(EMNLP).AssociationforComputational
[1] AkikoAizawa.2003.Aninformation-theoreticperspectiveoftf–idfmeasures. Linguistics.
InformationProcessing&Management39,1(2003),45–65. [23] JacobDevlinMing-WeiChangKentonandLeeKristinaToutanova.2019.BERT:
[2] MarkusBayer,Marc-AndréKaufhold,andChristianReuter.2022.ASurveyon Pre-trainingofDeepBidirectionalTransformersforLanguageUnderstanding.In
DataAugmentationforTextClassification.ACMComput.Surv.55,7,Article146 ProceedingsofNAACL-HLT.4171–4186.
(dec2022),39pages. https://doi.org/10.1145/3544558 [24] OmarKhattabandMateiZaharia.2020.Colbert:Efficientandeffectivepassage
[3] AndrzejBiałecki,RobertMuir,GrantIngersoll,andLucidImagination.2012. searchviacontextualizedlateinteractionoverbert.InProceedingsofthe43rd
Apachelucene4.InSIGIR2012workshoponopensourceinformationretrieval.17. InternationalACMSIGIRconferenceonresearchanddevelopmentinInformation
[4] LuizBonifacio,HugoAbonizio,MarziehFadaee,RodrigoNogueira,etal.2022. Retrieval.39–48.
InPars:UnsupervisedDatasetGenerationforInformationRetrieval.InPROCEED- [25] MeiKobayashiandKoichiTakeda.2000.Informationretrievalontheweb.ACM
INGSOFTHE45THINTERNATIONALACMSIGIRCONFERENCEONRESEARCH computingsurveys(CSUR)32,2(2000),144–173.
ANDDEVELOPMENTININFORMATIONRETRIEVAL(SIGIR’22).6. [26] KentonLee,Ming-WeiChang,andKristinaToutanova.2019.LatentRetrieval
[5] TomBrown,BenjaminMann,NickRyder,MelanieSubbiah,JaredDKaplan, forWeaklySupervisedOpenDomainQuestionAnswering.InProceedingsofthe
PrafullaDhariwal,ArvindNeelakantan,PranavShyam,GirishSastry,Amanda 57thAnnualMeetingoftheAssociationforComputationalLinguistics.6086–6096.
Askell,etal.2020.Languagemodelsarefew-shotlearners.Advancesinneural [27] YibinLei,YuCao,TianyiZhou,TaoShen,andAndrewYates.2024. Corpus-
informationprocessingsystems33(2020),1877–1901. SteeredQueryExpansionwithLargeLanguageModels.InProceedingsofthe
[6] YupengChang,XuWang,JindongWang,YuanWu,LinyiYang,KaijieZhu,Hao 18thConferenceoftheEuropeanChapteroftheAssociationforComputational
Chen,XiaoyuanYi,CunxiangWang,YidongWang,etal.2023. Asurveyon Linguistics(Volume2:ShortPapers).393–401.
evaluationoflargelanguagemodels.ACMTransactionsonIntelligentSystems [28] PatrickLewis,EthanPerez,AleksandraPiktus,FabioPetroni,VladimirKarpukhin,
andTechnology(2023). NamanGoyal,HeinrichKüttler,MikeLewis,Wen-tauYih,TimRocktäschel,
[7] XilunChen,KushalLakhotia,BarlasOguz,AnchitGupta,PatrickLewis,Stan etal.2020.Retrieval-augmentedgenerationforknowledge-intensivenlptasks.
Peshterliev,YasharMehdad,SonalGupta,andWen-tauYih.2022.SalientPhrase AdvancesinNeuralInformationProcessingSystems33(2020),9459–9474.
AwareDenseRetrieval:CanaDenseRetrieverImitateaSparseOne?.InFindings [29] FangyuanLuo,JunWu,andTaoWang.2023.DiscreteListwiseContent-aware
oftheAssociationforComputationalLinguistics:EMNLP2022.250–262. Recommendation. ACMTrans.Knowl.Discov.Data18,1,Article7(aug2023),
[8] ZhuyunDai,VincentYZhao,JiMa,YiLuan,JianmoNi,JingLu,AntonBakalov, 20pages. https://doi.org/10.1145/3609334
KelvinGuu,KeithHall,andMing-WeiChang.2022. Promptagator:Few-shot [30] JiMa,IvanKorotkov,YinfeiYang,KeithHall,andRyanMcDonald.2021.Zero-shot
DenseRetrievalFrom8Examples.InTheEleventhInternationalConferenceon NeuralPassageRetrievalviaDomain-targetedSyntheticQuestionGeneration.
LearningRepresentations. InProceedingsofthe16thConferenceoftheEuropeanChapteroftheAssociation
[9] ChuyuFang,ChuanQin,QiZhang,KaichunYao,JingshuaiZhang,HengshuZhu, forComputationalLinguistics:MainVolume.
FuzhenZhuang,andHuiXiong.2023.Recruitpro:Apretrainedlanguagemodel [31] RuiMeng,YeLiu,SemihYavuz,DivyanshAgarwal,LifuTu,NingYu,Jianguo
withskill-awarepromptlearningforintelligentrecruitment.InProceedingsof Zhang,MeghanaBhat,andYingboZhou.2022.UnsupervisedDenseRetrieval
the29thACMSIGKDDConferenceonKnowledgeDiscoveryandDataMining. DeservesBetterPositivePairs:ScalableAugmentationwithQueryExtraction
3991–4002. andGeneration.arXivpreprintarXiv:2212.08841(2022).
[10] LuyuGao,XueguangMa,JimmyLin,andJamieCallan.2023.PreciseZero-Shot [32] RodrigoNogueira,ZhiyingJiang,RonakPradeep,andJimmyLin.2020.Docu-
DenseRetrievalwithoutRelevanceLabels.InProceedingsofthe61stAnnual mentRankingwithaPretrainedSequence-to-SequenceModel.InFindingsofthe
MeetingoftheAssociationforComputationalLinguistics(Volume1:LongPapers). AssociationforComputationalLinguistics:EMNLP2020.708–718.
1762–1777. [33] RodrigoNogueira,JimmyLin,andAIEpistemic.2019. Fromdoc2queryto
[11] MitkoGospodinov,SeanMacAvaney,andCraigMacdonald.2023.Doc2Query–: docTTTTTquery.Onlinepreprint6,2(2019).
whenlessismore.InEuropeanConferenceonInformationRetrieval.Springer, [34] RodrigoNogueira,WeiYang,JimmyLin,andKyunghyunCho.2019.Document
414–422. expansionbyqueryprediction.arXivpreprintarXiv:1904.08375(2019).
[12] JiafengGuo,YinqiongCai,YixingFan,FeiSun,RuqingZhang,andXueqiCheng. [35] LongOuyang,JeffreyWu,XuJiang,DiogoAlmeida,CarrollWainwright,Pamela
2022. Semanticmodelsforthefirst-stageretrieval:Acomprehensivereview. Mishkin,ChongZhang,SandhiniAgarwal,KatarinaSlama,AlexRay,etal.2022.
ACMTransactionsonInformationSystems(TOIS)40,4(2022),1–42. Traininglanguagemodelstofollowinstructionswithhumanfeedback.Advances
[13] JiafengGuo,YixingFan,QingyaoAi,andWBruceCroft.2016.Adeeprelevance inNeuralInformationProcessingSystems35(2022),27730–27744.
matchingmodelforad-hocretrieval.InProceedingsofthe25thACMinternational [36] ShivankPandeyandKCRajeswari.2013.Automaticquestiongenerationusing
onconferenceoninformationandknowledgemanagement.55–64. softwareagentsfortechnicalinstitutions. InternationalJournalofAdvanced
[14] JiafengGuo,YixingFan,LiangPang,LiuYang,QingyaoAi,HamedZamani,Chen ComputerResearch3,4(2013),307.
Wu,WBruceCroft,andXueqiCheng.2020.Adeeplookintoneuralranking [37] ZhiyuanPeng,XuyangWu,andYiFang.2023.Softprompttuningforaugmenting
modelsforinformationretrieval. InformationProcessing&Management57,6 denseretrievalwithlargelanguagemodels. arXivpreprintarXiv:2307.08303
(2020),102067. (2023).
[15] HeliaHashemi,YongZhuang,SachithSriRamKothur,SrivasPrasad,Edgar [38] ChuanQin,LeZhang,YihangCheng,RuiZha,DazhongShen,QiZhang,XiChen,
Meij,andWBruceCroft.2023.Denseretrievaladaptationusingtargetdomain YingSun,ChenZhu,HengshuZhu,etal.2023.Acomprehensivesurveyofartifi-
description.InProceedingsofthe2023ACMSIGIRInternationalConferenceon cialintelligencetechniquesfortalentanalytics.arXivpreprintarXiv:2307.03195
TheoryofInformationRetrieval. (2023).
[16] EdwardJHu,PhillipWallis,ZeyuanAllen-Zhu,YuanzhiLi,SheanWang,Lu [39] YingqiQu,YuchenDing,JingLiu,KaiLiu,RuiyangRen,WayneXinZhao,Daxi-
Wang,WeizhuChen,etal.2021.LoRA:Low-RankAdaptationofLargeLanguage angDong,HuaWu,andHaifengWang.2021.RocketQA:AnOptimizedTraining
Models.InInternationalConferenceonLearningRepresentations. ApproachtoDensePassageRetrievalforOpen-DomainQuestionAnswering.In
[17] Po-SenHuang,XiaodongHe,JianfengGao,LiDeng,AlexAcero,andLarry Proceedingsofthe2021ConferenceoftheNorthAmericanChapteroftheAssociation
Heck.2013. Learningdeepstructuredsemanticmodelsforwebsearchusing forComputationalLinguistics:HumanLanguageTechnologies.5835–5847.
clickthroughdata.InProceedingsofthe22ndACMinternationalconferenceon [40] SheetalRakangorandYRGhodasara.2015. Literaturereviewofautomatic
Information&KnowledgeManagement.2333–2338. questiongenerationsystems. Internationaljournalofscientificandresearch
[18] GautierIzacard,MathildeCaron,LucasHosseini,SebastianRiedel,PiotrBo- publications5,1(2015),1–5.
janowski,ArmandJoulin,andEdouardGrave.2022.UnsupervisedDenseInfor- [41] OriRam,GalShachaf,OmerLevy,JonathanBerant,andAmirGloberson.2022.
mationRetrievalwithContrastiveLearning.TransactionsonMachineLearning LearningtoRetrievePassageswithoutSupervision.InProceedingsofthe2022
Research(2022). ConferenceoftheNorthAmericanChapteroftheAssociationforComputational
[19] VitorJeronymo,LuizBonifacio,HugoAbonizio,MarziehFadaee,RobertoLotufo, Linguistics:HumanLanguageTechnologies.2687–2700.
JakubZavrel,andRodrigoNogueira.2023. InPars-v2:LargeLanguageMod- [42] Sylvestre-AlviseRebuffi,SvenGowal,DanAndreiCalian,FlorianStimberg,Olivia
elsasEfficientDatasetGeneratorsforInformationRetrieval. arXivpreprint Wiles,andTimothyAMann.2021.DataAugmentationCanImproveRobustness.
arXiv:2301.01820(2023). InAdvancesinNeuralInformationProcessingSystems,M.Ranzato,A.Beygelzimer,
[20] FeihuJiang,ChuanQin,KaichunYao,ChuyuFang,FuzhenZhuang,Hengshu Y.Dauphin,P.S.Liang,andJ.WortmanVaughan(Eds.),Vol.34.CurranAssociates,
Zhu,andHuiXiong.2024.Enhancingquestionansweringforenterpriseknowl- Inc.,29935–29948. https://proceedings.neurips.cc/paper_files/paper/2021/file/
edgebasesusinglargelanguagemodels.InInternationalConferenceonDatabase fb4c48608ce8825b558ccf07169a3421-Paper.pdf
SystemsforAdvancedApplications.Springer,273–290. [43] StephenERobertson,SteveWalker,SusanJones,MichelineMHancock-Beaulieu,
[21] JeffJohnson,MatthijsDouze,andHervéJégou.2019. Billion-scalesimilarity MikeGatford,etal.1995.OkapiatTREC-3.NistSpecialPublicationSp109(1995),
searchwithgpus.IEEETransactionsonBigData7,3(2019),535–547. 109.
[22] VladimirKarpukhin,BarlasOguz,SewonMin,PatrickLewis,LedellWu,Sergey [44] Jon Saad-Falcon, Omar Khattab, Keshav Santhanam, Radu Florian, Martin
Edunov,DanqiChen,andWen-tauYih.2020.DensePassageRetrievalforOpen- Franz,SalimRoukos,AvirupSil,MdArafatSultan,andChristopherPotts.2023.
DomainQuestionAnswering.InProceedingsofthe2020ConferenceonEmpirical UDAPDR:UnsupervisedDomainAdaptationviaLLMPromptingandDistillation
1382
FromMisstepstoMastery:EnhancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration KDD’25,August3–7,2025,Toronto,ON,Canada
ofRerankers.arXivpreprintarXiv:2303.00807(2023). • HotpotQA:HotpotQAisaspecializeddatasetforstudyingmulti-
[45] DevendraSachan,MostofaPatwary,MohammadShoeybi,NeelKant,WeiPing, hopquestionsinnaturallanguagequestionanswering,featuring
WilliamLHamilton,andBryanCatanzaro.2021.End-to-EndTrainingofNeural
comprehensivesupervisionofsupportingfacts.
RetrieversforOpen-DomainQuestionAnswering.InProceedingsofthe59th
AnnualMeetingoftheAssociationforComputationalLinguisticsandthe11th • Quora:QuoraissourcedfromtheQuoraQ&Aplatform,with
InternationalJointConferenceonNaturalLanguageProcessing(Volume1:Long questions and answers created by its users. It covers a wide
Papers).6648–6662.
[46] MinjoonSeo,TomKwiatkowski,AnkurParikh,AliFarhadi,andHannaneh rangeoftopicsandincludesannotationsindicatingwhethereach
Hajishirzi.2018. Phrase-IndexedQuestionAnswering:ANewChallengefor questionissemanticallysimilartoexistingquestions.
ScalableDocumentComprehension.InProceedingsofthe2018Conferenceon • CQADupstack:CQADupStackisacommunityquestion-answering
EmpiricalMethodsinNaturalLanguageProcessing.559–564.
[47] MinjoonSeo,JinhyukLee,TomKwiatkowski,AnkurParikh,AliFarhadi,and dataset sourced from StackExchange, comprising Q&A posts
HannanehHajishirzi.2019.Real-TimeOpen-DomainQuestionAnsweringwith across12subdomains,includingprogramming(StackOverflow),
Dense-SparsePhraseIndex.InProceedingsofthe57thAnnualMeetingofthe
mathematics(MathStackExchange),andphysics(PhysicsStack
AssociationforComputationalLinguistics.4430–4441.
[48] TaoShen,GuodongLong,XiuboGeng,ChongyangTao,TianyiZhou,andDaxin Exchange).
Jiang.2023.Largelanguagemodelsarestrongzero-shotretriever.arXivpreprint • TREC-COVID: The TREC-COVID dataset is specifically de-
arXiv:2304.14233(2023).
[49] XiaoyuShen,SvitlanaVakulenko,MarcoDelTredici,GianniBarlacchi,Bill signedfortheretrievalofinformationrelatedtotheCOVID-19
Byrne,andAdriàdeGispert.2022.Low-resourcedenseretrievalforopen-domain pandemic.Itaimstoassistresearchersinaccessingreliabledata
questionanswering:Acomprehensivesurvey.arXivpreprintarXiv:2208.03197
aboutthevirusanditsimpacts.
(2022).
[50] NandanThakur,NilsReimers,AndreasRücklé,AbhishekSrivastava,andIryna • NFCorpus:NFCorpusisdesignedformedicalinformationre-
Gurevych.2021.BEIR:AHeterogeneousBenchmarkforZero-shotEvaluationof trieval.Itcomprisesnon-technicalnaturallanguagequeriesand
InformationRetrievalModels.InThirty-fifthConferenceonNeuralInformation
correspondingcomplex,terminology-heavydocuments.
ProcessingSystemsDatasetsandBenchmarksTrack(Round2).
[51] HugoTouvron,LouisMartin,KevinStone,PeterAlbert,AmjadAlmahairi,Yas- • Trec-News:TREC-Newsisadatasetfornewsinformationre-
mineBabaei,NikolayBashlykov,SoumyaBatra,PrajjwalBhargava,ShrutiBhos- trieval,aimedatenhancingtheunderstandingofcontentrele-
ale,etal.2023. Llama2:Openfoundationandfine-tunedchatmodels. arXiv
preprintarXiv:2307.09288(2023). vanceinnewsretrieval.
[52] KexinWang,NandanThakur,NilsReimers,andIrynaGurevych.2022. GPL: • Robust04:Robust04consistsofnewsarticlesandothertexts,
GenerativePseudoLabelingforUnsupervisedDomainAdaptationofDense
focusingonpoorlyperformingtopicstoadvanceretrievaltech-
Retrieval.InProceedingsofthe2022ConferenceoftheNorthAmericanChapterof
theAssociationforComputationalLinguistics:HumanLanguageTechnologies. niques.
[53] LiangWang,NanYang,andFuruWei.2023.Query2doc:QueryExpansionwith • ArguAna:ArguAnadatasetissourcedfromdebatewebsitesand
LargeLanguageModels.InThe2023ConferenceonEmpiricalMethodsinNatural
forums,comprisingalargenumberofspeculativequestionsand
LanguageProcessing.
[54] LeeXiong,ChenyanXiong,YeLi,Kwok-FungTang,JialinLiu,PaulBennett, responseswithsupportingandopposingarguments.
JunaidAhmed,andArnoldOverwijk.2020.Approximatenearestneighbornega- • Touche-2020:TheTouche-2020datasetcomprisescontentious
tivecontrastivelearningfordensetextretrieval.arXivpreprintarXiv:2007.00808
(2020). question-answerpairsin2020,whereeachqueryincludesmulti-
[55] CanwenXu,DayaGuo,NanDuan,andJulianMcAuley.2022.LaPraDoR:Unsu- pleresponseswithsupportingoropposingpositionsandargu-
pervisedPretrainedDenseRetrieverforZero-ShotTextRetrieval.InFindingsof
ments.
theAssociationforComputationalLinguistics:ACL2022.3557–3569.
[56] PeilinYang,HuiFang,andJimmyLin.2017.Anserini:Enablingtheuseoflucene • DBPedia-Entity:DBPediaisextractedfromWikipediainastruc-
forinformationretrievalresearch.InProceedingsofthe40thinternationalACM turedmanner,containingalargenumberofentitiesalongwith
SIGIRconferenceonresearchanddevelopmentininformationretrieval.1253–1256.
theircorrespondingattributesandrelationships.
[57] ShunyuZhang,YaoboLiang,MingGong,DaxinJiang,andNanDuan.2022.Multi-
ViewDocumentRepresentationLearningforOpen-DomainDenseRetrieval.In • SciDocs:SciDocsiscomposedofresearchpapersfromawide
Proceedingsofthe60thAnnualMeetingoftheAssociationforComputational rangeofacademicfields,includingstructuredinformationsuch
Linguistics(Volume1:LongPapers).5990–6000.
[58] Wayne Xin Zhao, Jing Liu, Ruiyang Ren, and Ji-Rong Wen. 2022. Dense asauthors,titles,andabstracts.Itaimstocontributetoadvance-
textretrievalbasedonpretrainedlanguagemodels:Asurvey. arXivpreprint mentsinpaperinformationretrieval.
arXiv:2211.14876(2022). • Fever:FeverisafactverificationdatasetsourcedfromWikipedia.
[59] YutaoZhu,HuayingYuan,ShutingWang,JiongnanLiu,WenhanLiu,Chen-
longDeng,ZhichengDou,andJi-RongWen.2023.Largelanguagemodelsfor It consists of queries requiring validation, corresponding evi-
informationretrieval:Asurvey.arXivpreprintarXiv:2308.07107(2023). dence,andlabelsindicatingthetruthfulnessoftheclaims.Inthe
fieldofinformationretrieval,itistreatedasataskofretrieving
A Appendix
evidencecorrespondingtothequeries.
A.1 DatasetDescriptions • Climate-Fever:Climate-Feverisafactverificationdatasetin
theclimatedomain,sourcedfromscientificpapers,newsarti-
Weconductedourexperimentsusingaseriesofdatasetsincludedin
cles,governmentreports,andmore.SimilartoFever,itincludes
theBEIRbenchmark.Thedetaileddescriptionsareprovidedbelow:
climate-relatedqueries,correspondingevidence,andtruthfulness
• FiQA:FiQAdatasetconcentratesonquestion-and-answerses-
labels.
sionsrelatedtofinancialmatters,encompassingadiverserange
• SciFact:SciFactisafactverificationdatasetsourcedfrompeer-
ofinquiriesandresponsessourcedfromfinancialforums.
reviewedscientificpapers.Itincludesscience-relatedqueries,
• MSMARCO:MSMARCOisasubstantialquestion-answerand
correspondingevidence,andtruthfulnesslabels.
informationretrievaldataset.Itaimstofosteradvancementsin
Pleasenotethatinourexperiments,theBioASQandSignaldatasets
machinereadingcomprehensionandsearchenginealgorithms.
fromBEIRwerenotincluded.Thisisbecausethesetwodatasetsare
• NQ:NQcentersprimarilyonquestion-answeringtasks.Each
notpubliclyavailable,andwehavenotyetsucceededinobtaining
questionisgroundedinreal-worldinformationrequirementsand
accesstothem.
correlatedwithanswersextractedfromcompletewebpages.
1383
KDD’25,August3–7,2025,Toronto,ON,Canada ZhenyuTongetal.
TableS1:Theperformancesinthezero-shotsettingofourmodelandrepresentativebaselinesonallaccessibledatasetsinthe
BEIRbenchmark.
Models QGen InPars-v2 LaPraDoR Ours InPars-v2* LaPraDoR* Ours*
FiQA 0.3082 0.3243 0.3290 0.3628 0.5085 0.4973 0.5202
NQ 0.3583 0.4532 0.4872 0.5221 0.6382 0.7072 0.7119
HotPotQA 0.5245 0.5406 0.6241 0.6665 0.7912 0.7832 0.8215
Quora 0.8129 0.8080 0.8692 0.8468 0.8451 0.8946 0.8889
CQADupstack 0.3589 0.3019 0.2427 0.3792 0.4483 0.4672 0.4925
TREC-COVID 0.6083 0.7184 0.7389 0.7712 0.8462 0.8518 0.8792
NFCorpus 0.3032 0.3341 0.3246 0.3815 0.3845 0.4409 0.4252
Trec-News 0.3872 0.3825 0.4481 0.4323 0.4902 0.5241 0.5135
Robust04 0.3567 0.4285 0.4901 0.4805 0.6322 0.6018 0.6312
ArguAna 0.4934 0.4725 0.5072 0.5105 0.4690 0.5273 0.5583
Touche-2020 0.1822 0.2845 0.3241 0.3107 0.2905 0.3305 0.3175
DBPedia-Entity 0.3281 0.4192 0.4189 0.4624 0.4979 0.4902 0.5123
SciDocs 0.1429 0.1129 0.1829 0.1675 0.2083 0.2472 0.2238
Fever 0.6693 0.6671 0.6821 0.7894 0.8715 0.7894 0.8714
Climate-Fever 0.1755 0.1725 0.2267 0.1947 0.3234 0.3371 0.3451
SciFact 0.6429 0.6825 0.6882 0.7430 0.7743 0.7523 0.7962
Avg. 0.3913 0.4178 0.4461 0.4718 0.5637 0.5776 0.5943
TableS2:Theefficiencyofstaticgeneratoranditerativeup- data,ourproposedmethodisdemonstratedtobemoreefficient.
datedgenerator. Moreover,wehaveconductedanadditionalexperimenttoillustrate
theperformancedifferencesbetweenthemodelswhenallocated
Models NDCG MAP Recall MRR Time FLOPS
thesametimebudgetperiterationinTableS3.Thishighlightsthat
Staticgenerator 0.3262 0.2568 0.5225 0.2826 1.6h 24.32PFLOP
Iterativeupdatedgenerator 0.3312 0.2583 0.5273 0.2925 2.1h 34.13PFLOP ouriterativeoptimizationprogressivelyunlocksthelatentpoten-
tialofthegenerator,enablingmoreefficientimprovementsinthe
TableS3:Theperformanceofstaticgeneratoranditerative
performanceofthedenseretrievalmodelwhilemaintainingthe
updatedgeneratoroveriterations.
samecomputationalresourceconstraints.Incontrast,thestatic
Models Staticgenerator generatorfacesaperformancebottleneck,limitingitseffectiveness.
Comparedtootherquerygenerationmodels,whichdonotuse
#Iteration NDCG MAP Recall MRR
iterativecomputations,ourmodelismorecomputationallyefficient
1 0.3281 0.2402 0.4817 0.3491 inthenon-iterativesetting,withInPars[4],Promptagator[8],and
2 0.3581 0.2517 0.4991 0.3518 UDAPDR[44]taking2.03h,2.5h,and1.92h,respectively,whileour
3 0.3579 0.2502 0.4969 0.3512 modelrequiresonly1.6h.Withiterativecomputations,ourmodel
takes2.1h,9.38%morethanthenon-iterativeapproach.However,
Models Iterativeupdatedgenerator
asshowninpreviousexperiments,thisadditionalcostisjustified
#Iteration NDCG MAP Recall MRR bythesignificantperformancegainsindenseretrievalachieved
1 0.3672 0.2549 0.5117 0.3682 throughiteration.
2 0.4002 0.3434 0.5310 0.3940
A.3 AddtionalEvaluationintheZero-Shot
3 0.4218 0.3842 0.5720 0.4182
Setting
Following the experimental setup in Section 5.5, we compared
A.2 TheTimeCostoftheIterativeOptimization
ourmethodwithseveralrepresentativebaselinesonallaccessi-
Weconductedadetailedanalysisoftheiterativeefficiencyduring bledatasetsintheBEIRbenchmark.Theresultsarepresentedin
thetrainingprocessontheFiQAdataset.AsillustratedinTableS2, Table S1. Specifically, we found that our approach achieved an
whilemaintaininganequivalenttotaloutputofpseudoqueries,we averageimprovementof20.57%,12.92%,and5.76%inNDCG@10
comparedthetrainingdurationforthereinforcementlearning(RL) acrossallaccessibledatasetsintheBEIRBenchmark,comparedto
processwiththetimeandflops(floatingpointoperations)required QGen,Inpars-v2,andLaPraDoR,respectively.Afterincorporating
foreachroundofdirectgeneration.Ourfindingsrevealthatgener- areranker,ourapproachcontinuestoachieveimprovementsof
atinganequivalentnumberofqueriesusingtheiterativemethod 5.43%and2.89%forInPars-v2andLaPraDoR,respectively.These
requires31.25%moretimeand40.33%moreflops.Consideringthe experimentalresultsprovidestrongevidencethatourproposed
additionaltrainingoverheadofRL,coupledwiththefactthatthe iGFTmethoddeliverssuperiorperformanceinthevastmajorityof
iterativeupdatedgeneratorismoreadeptatproducinghigh-quality zero-shotscenarios.
1384