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

| From |     | Missteps    | to      | Mastery: | Enhancing |       | Low-Resource |            |           | Dense |
| ---- | --- | ----------- | ------- | -------- | --------- | ----- | ------------ | ---------- | --------- | ----- |
|      |     | Retrieval   | through |          | Adaptive  | Query |              | Generation |           |       |
|      |     | ZhenyuTong∗ |         |          | ChuanQin∗ |       |              |            | ChuyuFang |       |
UniversityoftheChineseAcademyof ComputerNetworkInformation BaiduInc.
|     |                         | Sciences      |     | Center,ChineseAcademyofSciences |                        |     |     |                         | Beijing,China  |     |
| --- | ----------------------- | ------------- | --- | ------------------------------- | ---------------------- | --- | --- | ----------------------- | -------------- | --- |
|     |                         | Beijing,China |     |                                 | Beijing,China          |     |     | fangchuyu2022@gmail.com |                |     |
|     | tongzhenyu123@gmail.com |               |     |                                 | chuanqin0426@gmail.com |     |     |                         |                |     |
|     |                         | KaichunYao    |     |                                 | XiChen                 |     |     |                         | JingshuaiZhang |     |
InstituteofSoftware,Chinese UniversityofScienceandTechnology BaiduInc.
|     | AcademyofSciences      |               |     |                             | ofChina     |     |     |                           | Beijing,China |     |
| --- | ---------------------- | ------------- | --- | --------------------------- | ----------- | --- | --- | ------------------------- | ------------- | --- |
|     |                        | Beijing,China |     |                             | Hefei,China |     |     | zhangjingshuai0@gmail.com |               |     |
|     | yaokaichun@outlook.com |               |     | chenxi0401@mail.ustc.edu.cn |             |     |     |                           |               |     |
HengshuZhu†
ChenZhu
|     |     | UniversityofScienceandTechnology |                     |     | ComputerNetworkInformation      |                      |               |     |     |     |
| --- | --- | -------------------------------- | ------------------- | --- | ------------------------------- | -------------------- | ------------- | --- | --- | --- |
|     |     |                                  | ofChina             |     | Center,ChineseAcademyofSciences |                      |               |     |     |     |
|     |     |                                  | Hefei,China         |     |                                 |                      | Beijing,China |     |     |     |
|     |     |                                  | zc3930155@gmail.com |     |                                 | zhuhengshu@gmail.com |               |     |     |     |
Abstract
fine-tuningprocess.Furthermore,wedesignanoveliterativeopti-
Documentretrieval,designedtorecallquery-relevantdocuments mizationstrategythatdynamicallyoptimizesthequerygenerator
forproducingmoreinformativequeries,therebyenhancingthe
fromexpansivecollections,isessentialforinformation-seeking
efficacyoftheentireframework.Finally,extensiveexperiments
tasks,suchaswebsearchandopen-domainquestion-answering.
conductedonaseriesofpubliclyavailableretrievalbenchmark
Advancesinrepresentationlearningandpretrainedlanguagemod-
els(PLMs)havedrivenaparadigmshiftfromtraditionalsparse datasetshavedemonstratedtheeffectivenessoftheproposediGFT.
| retrieval | methods | to more effective | dense | retrieval | approaches, |     |     |     |     |     |
| --------- | ------- | ----------------- | ----- | --------- | ----------- | --- | --- | --- | --- | --- |
CCSConcepts
forgingenhancedsemanticconnectionsbetweenqueriesanddocu-
mentsandestablishingnewperformancebenchmarks.However, •Informationsystems→Informationretrieval;•Computing
relianceonextensiveannotateddocument-querypairslimitstheir methodologies→Naturallanguagegeneration.
competitivenessinlow-resourcescenarios.Recentresearchefforts
| employingthefew-shotcapabilitiesoflargelanguagemodels(LLMs) |     |     |     |     | Keywords |     |     |     |     |     |
| ----------------------------------------------------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
andpromptengineeringforsyntheticdatagenerationhaveemerged
Denseretrieval;querygeneration;largelanguagemodel
asapromisingsolution.Nonetheless,theseapproachesarehindered
bythegenerationoflower-qualitydatawithintheconventional ACMReferenceFormat:
denseretrievaltrainingprocess.Tothisend,inthispaper,weintro- ZhenyuTong,ChuanQin,ChuyuFang,KaichunYao,XiChen,Jingshuai
duceiGFT,aframeworkaimedatenhancinglow-resourcedensere- Zhang,ChenZhu,andHengshuZhu.2025.FromMisstepstoMastery:En-
trievalbyintegratingathree-phaseprocess—Generation,Filtering, hancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration.
InProceedingsofthe31stACMSIGKDDConferenceonKnowledgeDiscovery
andTuning—coupledwithaniterativeoptimizationstrategy.Specif-
andDataMiningV.1(KDD’25),August3–7,2025,Toronto,ON,Canada.ACM,
ically,wefirstemploysupervisedfine-tuningonlimitedground
NewYork,NY,USA,12pages.https://doi.org/10.1145/3690624.3709225
truthdata,enablinganLLMtofunctionasthegeneratorcapableof
producingpotentialqueriesfromgivendocuments.Subsequently,
wepresentamulti-stagefilteringmoduletominimizenoiseinthe 1 Introduction
generateddatawhileretainingsamplespoisedtosignificantlyim- Documentretrievalhasplayedasignificantrolewithinmodern
provethedenseretrievalmodel’sperformanceinthefollow-up
information-seekingsystems,aimingtoidentifythemostrelevant
∗Bothareco-firstauthorsandcontributeequallytothiswork. documentsfromvastcorporainresponsetouserqueries[12,38,
†Correspondingauthor 58].Thisfoundationalprocessunderpinsawiderangeofapplica-
tions,fromestablishedsearchengines[25]tothelatestretrieval-
augmentedgeneration(RAG)frameworks[28].
ThisworkislicensedunderaCreativeCommons4.0InternationalLicense. Thefieldofdocumentretrievalhasarichresearchhistory,with
KDD’25,August3–7,2025,Toronto,ON,Canada
traditionalapproachespredominantlyutilizingsparseretrievers,
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
Document: Many
| ofquerieswhenretrievingphrase-basedanswers[46,47]. |     |     |     |     | s e r v ic e s   c h a r g e    |                       |                  |                      |            |
| -------------------------------------------------- | --- | --- | --- | --- | ------------------------------- | --------------------- | ---------------- | -------------------- | ---------- |
|                                                    |     |     |     |     | p r i c e s   t h a t   d o   n | o t  L L M -b a s e d | L L M -b a s e d | Ad a p ti v e  L L M | - b a s ed |
Researchhasalsoexploredeffectivenegativesamplingmethods s c a l e  l i n e a r l y   w i th   Qu e ry  G e n e ra tor Qu e ry  G e n e ra tor Q u e r y  G e n e ra t o r
|     |     |     |     |     | u s ag e .   T h i s  i s   b e | -   |     |     |     |
| --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- |
fortrainingretrievalmodels.Forinstance,Xiongetal.employed ca u se   t h e   s e r v i c e   Pseudo Document- Pseudo Document- Pseudo Document-
|     |     |     |     |     | provider has ...	 | Query Pairs | Query Pairs | Query Pairs |     |
| --- | --- | --- | --- | --- | ----------------- | ----------- | ----------- | ----------- | --- |
theretrievalmodeltrainedintheprecedingiterationtoidentify
newnegativeinstancesforthesubsequenttrainingiteration[54]. L im it e d   an n o t a t e d Dens e  R e tr ieval D a t a   F i l t e r i n g M u lt i- S t a g e
|     |     |     |     |     | docu m en t - q u er y   p | a i r s M o d e l | (                    . . . ) | D a ta  F il t e r | in g |
| --- | --- | --- | --- | --- | -------------------------- | ----------------- | ---------------------------- | ------------------ | ---- |
Additionally,RocketQA[39]enhanceddenseretrievalperformance D o c u m e n t :   D u r- Document Query
|     |     |     |     |     | in g  t h e 1 2   p l u s   |     | Filtered Pseudo | Scored, Filtered |     |
| --- | --- | --- | --- | --- | --------------------------- | --- | --------------- | ---------------- | --- |
byusingknowledgedistillationtodenoisenegativesamples.Be- hours the market  Document- Pseudo Document-
|                                                          |     |     |     |     | was closed news   | Encoder Encoder | Query Pairs | Query Pairs |     |
| -------------------------------------------------------- | --- | --- | --- | --- | ----------------- | --------------- | ----------- | ----------- | --- |
| sides,Contriever[18]employedcontrastivelearningtoachieve |     |     |     |     | can change inve-	 |                 |             |             |     |
stors opinion of ...
unsupervisedtrainingindenseretrieval. Query: What cau- Dense Retrieval Dense Retrieval
|                                                          |     |     |     |     | ses discontinuities  | Score | Model | Model |     |
| -------------------------------------------------------- | --- | --- | --- | --- | -------------------- | ----- | ----- | ----- | --- |
| Whiledenseretrievaldemonstratessuperiorperformance,prior |     |     |     |     | with stock prices    |       |       |       |     |
researchhasprimarilyconcentratedonlearningfromexistingquery
Figure2:EnhancingdenseretrievalwithLLM-basedquery
labels.Inlow-resourcescenarios,denseretrievalexhibitsdiscernible
limitations[59].Toaddressthisissue,weproposeanovelframe- generation:acomparisonofparadigms.
workcomprisingathree-phaseprocess:Generation,Filtering,and
Tuning,aimedatenhancinglow-resourcedenseretrieval.
3 Preliminary
𝑁
|     |     |     |     |     | GivenalargecorpusD | ={𝑑 | 𝑖} composedof𝑁 | documents,and |     |
| --- | --- | --- | --- | --- | ------------------ | --- | -------------- | ------------- | --- |
𝑖 =1
2.2 DataAugmentationforDenseRetrieval anaturallanguagequery𝑞,theobjectiveofdocumentretrievalis
tolearnamodelRcapableofreturningarankedlistofthe𝑛most
| L e v er a g in | g d at a a u g m en | t at i o n t e c hn i q | u e s t o a u gm e n | t t h e a va i la b i l- |                     |     |                                   |     |     |
| --------------- | ------------------- | ----------------------- | -------------------- | ------------------------ | ------------------- | --- | --------------------------------- | --- | --- |
|                 |                     |                         |                      |                          | relevantdocumentsD𝑞 |     | [𝑑 𝑞 ,𝑑 𝑞 ,...,𝑑 𝑞 ]forthequery𝑞. |     |     |
it y o f p s eu d o d a t a c an e ff e c t iv e l y e n h a n c e t h e ro b u s t n es s o f t h e = 𝑛
1 2
UnliketraditionalsparseretrievalmethodslikeBM25,which
model[2,42].Inthefieldofdenseretrieval,severalstudiesrelied
dependonlexicalmatching,denseretrievalmodelsemploytwo
onhandcraftedtemplatesandfeaturestoextractmorerelevant
learnablefunctionsthatmapqueriesanddocumentstodensevec-
paireddata[36,40].Additionally,someresearchersproposedusing
|     |     |     |     |     | tors.Formally,let𝐸 | 𝑄(·)denotethequeryencoder,whichproduces |     |     |     |
| --- | --- | --- | --- | --- | ------------------ | --------------------------------------- | --- | --- | --- |
extractiontoselectportionsofdocumentcontentasqueriesor
∈R𝑘
answerstoachievedataenhancement[26,45]. arepresentation𝐸 𝑄(𝑞) 1 foreachquery𝑞.Similarly,thedoc-
|     |     |     |     |     | umentencoder𝐸 | 𝐷(·)isdefinedtomapadocument𝑑toitsrepre- |     |     |     |
| --- | --- | --- | --- | --- | ------------- | --------------------------------------- | --- | --- | --- |
Inrecentyears,researchershaveutilizedlargelanguagemodels
|     |     |     |     |     | sentation𝐸 | 𝐷(𝑑) ∈R𝑘 2.Alongthisline,thedenseretrievalmodel |     |     |     |
| --- | --- | --- | --- | --- | ---------- | ----------------------------------------------- | --- | --- | --- |
togeneratequeriesforunlabeledcorpora,achievingfavorableout-
Rcanbedenotedby
comesininformationretrievaltasks[4,8,11,33,34,44,52].InPars
utilizedpromptswithalimitednumberofexamplestogenerate
|     |     |     |     |     |     | R(𝑞,𝑑;𝜃)=𝑓 | (cid:0)𝐸 𝑄(𝑞),𝐸 𝐷(𝑑)(cid:1), |     |     |
| --- | --- | --- | --- | --- | --- | ---------- | ---------------------------- | --- | --- |
paragraph-levelqueriesbasedonGPT-3[4].Similarly,TQGen[31] 𝑠𝑖𝑚 (1)
exploredqueryextractionandquerygenerationtocreatepseudo
where𝜃 denotestheparametersofRandthesimilaritymeasure-
| document-querypairsforaugmentingretrievertraining.Incontrast |     |     |     |     | mentfunction𝑓 |     |     |     |     |
| ------------------------------------------------------------ | --- | --- | --- | --- | ------------- | --- | --- | --- | --- |
𝑠𝑖𝑚(·)canbeimplementedusinganinnerproduct,
tousingthehardpromptforgeneration,SPTAR[37]introduced
amultilayerperceptronnetwork(MLP),orotherneuralnetwork
softprompttuningtooptimizethequalityofthegeneratedquery.
architectures.Typically,therepresentationdimensionsofdocu-
Furthermore,toaddresstheinconsistencyofgeneratedqueriesby
|                                                        |     |     |     |     | ments and | queries are identical, | i.e.,𝑘 = | 𝑘 2. However, | this is |
| ------------------------------------------------------ | --- | --- | --- | --- | --------- | ---------------------- | -------- | ------------- | ------- |
| LLMs,somestudieshaveconcentratedondesigningvariousdata |     |     |     |     |           |                        | 1        |               |         |
notalwaysthecase.Forinstance,inColBERT[24],awell-known
selectionmethodstofilteroutqualifieddatafortraining[8,44].
denseretrievalmodel,queriesanddocumentsarerepresentedas
Beyondtrainingageneratorusinglabeleddocument-querypairs, ∈R|𝑞|×𝑘 ∈R|𝑑|×𝑘
|     |     |     |     |     | 𝐸 𝑄(𝑞) | and𝐸 𝐷(𝑑) | ,respectively,where𝑘repre- |     |     |
| --- | --- | --- | --- | --- | ------ | --------- | -------------------------- | --- | --- |
someresearchershaveexploredthedirectgenerationofpseudo
sentsthetokenrepresentationdimension.Subsequently,therele-
databasedonpretrainedmodelsinzero-shotscenarios[15,30,48].
vancescoreiscalculatedasfollows,
Additionally,SPAR[7]employedknowledgedistillationfromsparse
retrievalmodelstotrainthedatageneratorinzero-shotsettings. |𝑞|
∑︁
Withouttrainingthedatagenerator,methodslikeHyDE[10]and R(𝑞,𝑑;𝜃)= max 𝐸 𝑄(𝑞) ⊤𝐸 𝐷(𝑑)𝑗 , (2)
|                                                         |     |     |     |     |     |     | 𝑗=1,...,|𝑑| | 𝑖   |     |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- |
| CSQE[27]achievedsuperiorzero-shotinformationretrievalby |     |     |     |     |     | 𝑖=1 |             |     |     |
supplementingqueriesordocumentswithgeneratedinformation.
where|𝑞|and|𝑑|denotethenumberoftokensin𝑞and𝑑,respec-
However,currentLLM-baseddatageneratorsprimarilyrelyon
|     |     |     |     |     | tively.𝐸 𝑄(𝑞)𝑖 | and𝐸 𝐷(𝑑)𝑗 |     |     |     |
| --- | --- | --- | --- | --- | -------------- | ---------- | --- | --- | --- |
correspondtotheembeddingvectorsfor
existinglabeleddataandpowerfulpretrainedmodels,lackingthe
the𝑖-thtokenin𝑞andthe𝑗-thtokenin𝑑,respectively.
abilitytoimproveautonomouslyinlow-resourcescenarios.More-
Asmentionedbefore,denseretrievalpredominantlyemploys
over,thereisasignificantdeficiencyineffectivemethodsforas-
asupervisedtrainingsetting.GivenatrainingsetT𝑡𝑟𝑎𝑖𝑛,where
sessingandselectinggeneratedresults.Inthispaper,wepropose
|     |     |     |     |     | (𝑞,𝑑) | ∈ T𝑡𝑟𝑎𝑖𝑛 |     |     |     |
| --- | --- | --- | --- | --- | ----- | -------- | --- | --- | --- |
amulti-stagefilteringmoduledesignedtominimizenoiseinthe each representsarelevantdocument-querypair,
R(𝑞,𝑑;𝜃)
|     |     |     |     |     | the optimization | of the dense | retrieval model |     | can be |
| --- | --- | --- | --- | --- | ---------------- | ------------ | --------------- | --- | ------ |
generateddataandretainsamplesmostlikelytosignificantlyim-
formalizedas:
provetheperformanceofdenseretrievalmodels.Additionally,we
introduceadifficulty-guidediterativeoptimizationstrategytocon- 𝜃∗=argmaxE L(R,𝑞,𝑑+,𝑑−),
|                                                  |     |     |     |     |     | (𝑞,𝑑+,𝑑−)∼T′ |       |     | (3) |
| ------------------------------------------------ | --- | --- | --- | --- | --- | ------------ | ----- | --- | --- |
| tinuouslyenhancethecapabilitiesofdatagenerators. |     |     |     |     |     |              | 𝑡𝑟𝑎𝑖𝑛 |     |     |
𝜃
1375

| KDD’25,August3–7,2025,Toronto,ON,Canada |     |     |     |     |     |     | ZhenyuTongetal. |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --------------- | --- |
whereT ′ 𝑎𝑖𝑛isconstructedbasedonthetrainingsetT𝑡𝑟𝑎𝑖𝑛.Specif- isdefinedasfollows:
𝑡𝑟
| ically,∀(𝑞,𝑑+,𝑑−) | ∈T ′ 𝑎𝑖𝑛,𝑑+denotesapositive(relevant)docu- |     |     |     |       |          |             |     |
| ----------------- | ------------------------------------------ | --- | --- | --- | ----- | -------- | ----------- | --- |
|                   | 𝑡𝑟                                         |     |     |     | |𝑞|   |          |             |     |
|                   | (𝑞 , 𝑑 +                                   | 𝑑 − |     |     | ∑︁ ∑︁ | (cid:0)𝑝 | <𝑡)(cid:1), |     |
m e n t , i. e ., ) ∈ T 𝑡 𝑟 𝑎 𝑖 𝑛 , a nd r e p r e se n ts a s a m p l e d n e g a t i v e L𝑙𝑙𝑚 =m a x log Θ+Θ𝐿 (𝑞 𝑡|𝑑,𝑞 (5)
|     |     | − − |     | Θ   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
( ir r el e v a n t) d o c u m en t , i . e ., 𝑑 ∈ D , ( 𝑞 , 𝑑 ) ∉ T 𝑡𝑟 𝑎 𝑖𝑛 . T h e o b j e c t i v e 𝐿 (𝑞,𝑑) 𝑡=1
∈T𝑡𝑟𝑎𝑖𝑛
functionLiscrucialformodeloptimization,withthecontrastive
|                                                         |     |     | whereΘ | representstheLoRAparameters,weexclusivelyupdate |     |     |     |     |
| ------------------------------------------------------- | --- | --- | ------ | ----------------------------------------------- | --- | --- | --- | --- |
| objectivebeingaprevalentchoice.Formally,thisisdefinedas |     |     |        | 𝐿                                               |     |     |     |     |
theseLoRAparametersthroughoutthetrainingprocess.Thenota-
tion𝑞 referstothe𝑡-thtokenin𝑞,and𝑞
|                  |     | 𝑒𝑥𝑝(R(𝑞,𝑑+)) | 𝑡   |     |     | <𝑡 representsthesequence |     |     |
| ---------------- | --- | ------------ | --- | --- | --- | ------------------------ | --- | --- |
| L(R,𝑞,𝑑+,𝑑−)=log |     | . (4)        |     |     |     |                          |     |     |
𝑒𝑥𝑝(R(𝑞,𝑑+))+(cid:205)𝑙 oftokens{𝑞 1 ,𝑞 1 ,...,𝑞 𝑡−1 }.Finally,thefine-tunedLLMGempowers
𝑒𝑥𝑝(R(𝑞,𝑑−))
𝑗=1 𝑗 ustogeneratequeriesforanygivendocument,asrepresentedby:
Inpractice,foreachquery𝑞,wesample𝑙 documentsasnegative 𝑞 =G(𝑑;Θ+Θ 𝐿). (6)
(cid:101)
examplestoefficientlytrainthedenseretrievalmodelR,andwe
|      |                                        |     | T h i s c a p | a b ili ty f a c | i lit a t e st h e c r e a | ti o n o f a sy n th | e t i cd atasetT𝐺 | to  |
| ---- | -------------------------------------- | --- | ------------- | ---------------- | -------------------------- | -------------------- | ----------------- | --- |
| use𝑑 | − 𝑗-thnegativedocuments.Uponcompleting |     |               |                  |                            |                      |                   |     |
𝑗 todenotethe
|     |     |     | e n h a n c e | t h e p er f o r | m a n c e o f d e n s | e r e tr ie v al m o d | e l R . |     |
| --- | --- | --- | ------------- | ---------------- | --------------------- | ---------------------- | ------- | --- |
thetrainingofR,nearestneighborsearchtoolssuchasFAISS[21]
canbeemployedtoretrievethetop-𝑛mostrelevantdocumentsfor
4.2 Multi-StageDataFiltering
anygivenquery𝑞withsublinearcomplexity.
DespitethegeneratorG,trainedonannotateddata,iscapableof
Ashighlightedintheintroduction,collectingasufficientnumber
generatinghigh-qualityqueriesforconstructingsyntheticdataset
ofdocument-querypairsfortraininginlow-resourcescenarioscan
|     |     |     | T𝐺,ashighlightedinourintroduction,T𝐺 |     |     | unavoidablyincludes |     |     |
| --- | --- | --- | ------------------------------------ | --- | --- | ------------------- | --- | --- |
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
strategy,whichsignificantlyenhancestheperformanceofdense pair(𝑞 ,𝑑 ∈T𝐺,werandomlyselectother𝑚
|     |     |     | 𝑖   | 𝑗)  |     | 1documentsD𝑚 |     | =   |
| --- | --- | --- | --- | --- | --- | ------------ | --- | --- |
{𝑑𝑚} 𝑚
retrievalmodelsinlow-resourcescenarios. 1 from the corpus D as negative samples. This process
𝑘 𝑘=1
|     |     |     | formsacandidatesetD𝑚 |     | ′ ={𝑑 𝑗}∪D𝑚.Inourexperiments,𝑚 |     |     | 1is |
| --- | --- | --- | -------------------- | --- | ------------------------------ | --- | --- | --- |
4 Methodology setto100.Subsequently,foreach𝑑 ∈D𝑚 ′ ,(𝑞 ,𝑑 𝑘)isscoredusing
|                                                          |     |     |                      |     |                | 𝑘 𝑖                   |     |     |
| -------------------------------------------------------- | --- | --- | -------------------- | --- | -------------- | --------------------- | --- | --- |
|                                                          |     |     | BM25,denotedasBM25(𝑞 |     | ,𝑑 𝑘).IfBM25(𝑞 | ,𝑑 𝑗)yieldsthehighest |     |     |
| Inthissection,weelaborateonthedetailsoftheiGFTframework, |     |     |                      |     | 𝑖              | 𝑖                     |     |     |
incorporatingthreeprocesses:LLM-basedquerygeneration,multi- score,weretainthispseudo-pairinT𝐺;otherwise,itisexcluded.
|     |     |     | ByapplyingthiscriterionacrossT𝐺,werefineittoT |     |     |     | 1.  |     |
| --- | --- | --- | --------------------------------------------- | --- | --- | --- | --- | --- |
stagedatafiltering,andfine-tuningofthedenseretrievalmodel.Ad- 𝐺
ditionally,weintroduceadynamiciterativeoptimizationstrategy, 4.2.2 FilteringwithDenseRetrieval. Followingtheinitialfiltration
specificallydesignedtorefinethequerygenerator.Theframework
withBM25,whicheliminatessomelower-qualitydocument-query
overviewisdepictedinFigure3.
pairs,werecognizethelimitationofBM25toprimarilylexical-level
relevance.Consequently,wefurtheremployapretraineddense
4.1 LLM-basedQueryGeneration retrievalmodelR𝑝𝑟𝑒 forasecondroundoffiltering.Thissubse-
ToenhancetheperformanceofdenseretrievalmodelR quentstepseekstocapturenuancedsemanticrelationshipsthat
inlow-
resourcesettings,recentstudies[4,44]haveleveragedLLMsto BM25mightmiss,ensuringamorediscerningselectionoftraining
generateappropriatequeriesfordocumentswithincorporathat instancesforourdenseretrievalmodelR.
lack sufficient annotations. However, the effectiveness of these Specifically,wefirstleveragetheannotateddataT𝑡𝑟𝑎𝑖𝑛 totrain
methodsreliesheavilyonthedesignofprompts,especiallythe the pretrained dense retrieval model R𝑝𝑟𝑒. In our experiments,
R𝑝𝑟𝑒 isbasedontheColbertmodel.Subsequently,mirroringthe
qualityofdocument-queryexamplesusedinin-contextlearning,
whichdonotguaranteetheconsistentgenerationofhigh-quality processoffilteringwithBM25,weconstructcorrespondingnegative
|                             |     |     | samplesforeachquery-documentpair(𝑞      |     |     | ,𝑑   | 1.Onlythose |     |
| --------------------------- | --- | --- | --------------------------------------- | --- | --- | ---- | ----------- | --- |
| queriesacrossvariedcorpora. |     |     |                                         |     |     | 𝑖 𝑗) | ∈ T 𝐺       |     |
|                             |     |     | pairsrankedastop-1basedonthescoreR𝑝𝑟𝑒(𝑞 |     |     |      | ,𝑑          |     |
Toaddressthischallenge,weutilizeLlama-2[51],anopen-source 𝑖 𝑗)areselected
LLM,andapplySupervisedFine-Tuning(SFT)onaconstrained toformthefilteredsetT 2.Additionally,tofurtherenhancethe
𝐺
datasetofannotateddocument-querypairs,T𝑡𝑟𝑎𝑖𝑛,todevelopa 2,wesortallquery-documentpairsindescendingorder
qualityofT 𝐺
querygenerationmodel,G.Specifically,asillustratedinthetop basedonthescores{R𝑝𝑟𝑒(𝑞 𝑖 ,𝑑 𝑗),∀(𝑞 𝑖 ,𝑑 𝑗) ∈T 2}.Weretainonly
𝐺
leftcornerofFigure3,wefirstconstructtheSFTdatabasedon thetop𝑚 2%ofthesepairstoformthenewfiltereddatasetT 3.In
𝐺
T𝑡𝑟𝑎𝑖𝑛.Subsequently,giventhesubstantialcomputationalresources
ourexperiments,throughparameteranalysis,weretain40%ofT2
| requiredforfull-parameterfine-tuning,weoptforLoRA[16],a |     |     |     |     |     |     |     | 𝐺   |
| ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
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
T3thatexhibitinghigherlossvalues:
| 𝐺   |     |     |     |     |     | rapidlyreachesaperformanceplateau.Toaddressthischallenge, |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- |
L(R,𝑞 ,𝑑 𝑗)=−E L(R,𝑞 ,𝑑 ,𝑑−), w e d e v el o p ed a n i t e r a tiv e o p ti m iz a ti o n st r at e g y th at dy n a m i c a l l y
|     | 𝑖   | 𝑑−∼D,(𝑞𝑖,𝑑−)∉T |     | 3 𝑖 𝑗 | (7) |     |     |     |     |     |
| --- | --- | -------------- | --- | ----- | --- | --- | --- | --- | --- | --- |
𝐺 up d a t es o u r ge n e r a t o r G . T h i ss tr a t e gy e n a b le s G to a d a pt i v e l y
(𝑞 ,𝑑 3 L(R,𝑞 ,𝑑 ,𝑑−) producequeriesthatsignificantlyenhancetheiterativeupdatesof
| where | 𝑖 𝑗) ∈ | T 𝐺 and | 𝑖 𝑗 | canbedeterminedby |     |     |     |     |     |     |
| ----- | ------ | ------- | --- | ----------------- | --- | --- | --- | --- | --- | --- |
R,ensuringcontinuousimprovementinretrievalperformance.
Equation4.However,duetothehighcomputationalcostofsam-
plingnegativeinstances𝑑−,weemployamuti-headcross-attention Toclarifyourmethodology,webeginwiththefollowingdefini-
mechanismtoestimateEquation7.Formally,wehave tions:R𝑖𝑛𝑖𝑡 representstheinitialdenseretrievalmodeltrainedon
|     |                 |     |                   |                         |     | T 𝑡𝑟 𝑎 𝑖𝑛 ; G 1 | , d e r i v ed fr o m | tr a i n i n g o n t | h e S F T d ata , is | id e nt i fi e d a s |
| --- | --------------- | --- | ----------------- | ----------------------- | --- | --------------- | --------------------- | -------------------- | -------------------- | -------------------- |
|     | ℎ =𝑀𝑢𝑙𝑡𝑖𝐻𝑒𝑎𝑑𝐴𝑡𝑡 |     | (cid:0)𝐸 𝑄(𝑞 𝑖),𝐸 | 𝐷(𝑑 𝑗),𝐸 𝐷(𝑑 𝑗)(cid:1), |     |                 |                       |                      |                      |                      |
1 t h e fi r st i t e ra t i o n of t h eu p d a t e d g e n e ra t o r; T 4 d e no te s t h e s y n -
|     |        |                      |     |     | (8) |     |     |     | 𝐺,1 |     |
| --- | ------ | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | ℎ =𝑓(ℎ | ), 𝑦 =𝑚𝑒𝑎𝑛_𝑝𝑜𝑜𝑙𝑖𝑛𝑔(ℎ |     | ),  |     |     |     |     |     | 4   |
2 1 𝑞𝑖,𝑑𝑗 2 theticdataaftermulti-stagefiltering;andR 1,fine-tunedusingT 𝐺 ,1
∈R|𝑞𝑖|×𝑘 ∈R|𝑞𝑖|×1,𝑀𝑢𝑙𝑡𝑖𝐻𝑒𝑎𝑑𝐴𝑡𝑡(·,·,·)represents fromR𝑖𝑛𝑖𝑡,isrecognizedasthefirstiterationoftheupdateddense
| whereℎ |     | 3,ℎ |     |     |     |     |     |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 2 retrievalmodel.Alongthisline,wedenotethegenerator,synthetic
| themulti-headattentionnetwork, |     |     | 𝑓(·) | isalearnablemultilayer |     |     |     |     |     |     |
| ------------------------------ | --- | --- | ---- | ---------------------- | --- | --- | --- | --- | --- | --- |
data,andretrieverupdatedinthe𝑡-thiterationthroughouritera-
| perceptron | network, | and 𝐸 | and 𝐸 | denote the document | and |     |     |     |     |     |
| ---------- | -------- | ----- | ----- | ------------------- | --- | --- | --- | --- | --- | --- |
|            |          | 𝑄     | 𝐷     |                     |     |     |     | 4   |     |     |
queryencodersofR,respectively.Byuniformlysamplingasetof tiveoptimizationstrategyasG𝑡,T 𝐺 ,𝑡 ,andR𝑡,respectively.Indeed,
′ o ur p r im a r y m o t i v a t i on f o r i t e ra tiv e ly u p d at i n g t h e g e n e r a to r is
| ( 𝑞 𝑖 ,𝑑 | 𝑗 ) ∈ T 3 , d e | n o te d a s T 3 | , w e c an e | s tim a te t h e p | a r am e te rsin |     |     |     |     |     |
| -------- | --------------- | ---------------- | ------------ | ------------------ | ---------------- | --- | --- | --- | --- | --- |
𝐺 𝐺 to en a b le t h e sy n t h e t i c da t a T 4 to in c lu d e m o r e ( 𝑞 𝑖 , 𝑑 𝑗 ) p a i rs t ha t
t h e lo s s pr e d i c ti o n m o d u le b y m i ni m izi n g th e fo l lo w i n g lo ss : 𝐺 ,𝑡
|     |     |     |     |     |     | challengeR𝑡−1,specificallythosewithahighL(R𝑡−1 |     |     |     | ,𝑞 ,𝑑 𝑗).To |
| --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | ----------- |
𝑖
|     |     | ∑︁  | (cid:16) | (cid:17)2 |     |     |     |     |     |     |
| --- | --- | --- | -------- | --------- | --- | --- | --- | --- | --- | --- |
L𝑙𝑝 = 𝑦 −L(R,𝑞 𝑖 ,𝑑 𝑗) . (9) thisend,wedeveloparewardmodelandemployproximalpolicy
𝑞𝑖,𝑑𝑗
|     |     | 3′  |     |     |     | optimization(PPO)-basedreinforcementlearning(RL)toenhance |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --------------------------------------------------------- | --- | --- | --- | --- |
(𝑞𝑖,𝑑𝑗)∈T
|     |     | 𝐺   |     |     |     | thequerygenerator. |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- |
Subsequently,wecalculateandsortall𝑦 ,where(𝑞 𝑖 ,𝑑 𝑗) ∈T 3, Reward Model Learning Phase: The objective of the reward
|     |     |     |     | 𝑞𝑖,𝑑𝑗 | 𝐺   |     |     |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
indescendingorder.Weretainthetop𝑚 modelV𝑡at𝑡-thiterationistoassignscorestoany(𝑞 ,𝑑 𝑗),ensuring
|     |     |     |     | 3ofthesepairs,whichwe |     |     |     |     | 𝑖   |     |
| --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- |
,𝑞 ,𝑑
identifyasthemostinformativeinstancesforoptimizingthedense thatthepairswithahigherL(R𝑡−1 𝑖 𝑗)achievehigherscores.
retrievalmodel,tocomposethefinalfiltereddatasetT 4. ThearchitectureofV𝑡 issimilartothatofthegeneratorG,but
𝐺
replacesthefinaloutputlayerwithalinearpredictionheadthat
4.3 TuningandIterativeOptimization outputsscalarrewardvalues.Additionally,therewardmodelis
initializedwiththeparametersofthegeneratorG.Weleverage
| 4.3.1 | Fine-TuningDenseRetrievalModel. |     |     | AsintroducedinSection |     |     |     |     |     |     |
| ----- | ------------------------------- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- |
4
3,thedenseretrievalmodelcanbetrainedusingEquations3and4. T 𝐺 ,𝑡−1 to construct a dataset comprised of paired comparisons
Giventheannotatedtrainingdataset T𝑡𝑟𝑎𝑖𝑛,weinitiallytraina betweentworesponsesfromG𝑡−1andemployapairwiseranking
denseretrievalR𝑖𝑛𝑖𝑡.Subsequently,leveragingthesyntheticdata losstotrainV𝑡 inthefollowingmanner:
T4generatedbyourquerygenerationmodelGandrefinedthrough
𝐺
| a m u   | l ti -s t a g e fi lt e | ri n g p r o c e s s   | , we fu r t he | rfine-tuneR𝑖𝑛𝑖𝑡toproduce |     |         |                  |           |                |              |
| ------- | ----------------------- | ---------------------- | -------------- | ------------------------ | --- | ------- | ---------------- | --------- | -------------- | ------------ |
|         |                         |                        |                |                          |     | L𝑟𝑚 =−E | (𝑞𝑖,𝑞𝑘,𝑑𝑗)∼T𝑟𝑚,𝑡 | log𝜎(V𝑡(𝑞 | 𝑖 ,𝑑 𝑗)−V𝑡(𝑞 𝑘 | ,𝑑 𝑗)). (10) |
| o u r e | n h a n c e d d e       | n s e r et r i e v a l | m od e l R .   |                          |     |         |                  |           |                |              |
1377

| KDD’25,August3–7,2025,Toronto,ON,Canada |     |     |     |     |     |     |     |     |     |     |     |     | ZhenyuTongetal. |     |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------- | --- |
𝜎 denotestheactivationsigmoidfunction.T𝑟𝑚,𝑡 = {(𝑞 ,𝑞 ,𝑑 𝑗)}, 5 Experiments
|     |     |     |     |       |     |      | 𝑖   | 𝑘   |     |     |     |     |     |     |
| --- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | (𝑞  | ,𝑑  | 4   | (𝑞 ,𝑑 | 4   | and𝑦 | >   | 𝑦   |     |     |     |     |     |     |
where 𝑖 𝑗) ∈ T 𝐺 ,𝑡−1 , 𝑘 𝑗) ∈ T 𝐺 ,𝑡−1 , 𝑞𝑖,𝑑𝑗 𝑞𝑘,𝑑𝑗 . 5.1 ExperimentalSetting
𝑦 𝑞𝑖,𝑑𝑗 iscalculatedbythelosspredictionmoduleinSection4.2.3.
|     |     |     |     |     |     |     |     |     | 5.1.1 | Datasets. TovalidatetheeffectivenessoftheproposediGFT |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----------------------------------------------------- | --- | --- | --- | --- |
PPO-basedRLFine-TuningPhase:Wefirstusequerygener-
|     |       |            |          |        |                 |                |        |           | i n l o | w - re s o u rc e se t ti n | g s ,w e s e l e | c t ed a s e | ri e s o fd at a | s e t s f r o m t h e |
| --- | ----- | ---------- | -------- | ------ | --------------- | -------------- | ------ | --------- | ------- | --------------------------- | ---------------- | ------------ | ---------------- | --------------------- |
| a t | o r G | an d r e w | a rd m o | d e lV | to in it ia l i | z e t h e a ct | or m o | d e l G 𝑎 |         |                             |                  |              |                  |                       |
|     | 𝑡 −   | 1          |          | 𝑡      |                 |                |        |           |         |                             |                  |              |                  |                       |
𝑐 B E I R b e n c h m a rk [ 5 0 ] t o co n s t r u c t ou r e x p e r im en t s . S p e c i fi ca l ly ,
| a n | d c r it ic | m o d e l V | .D u r | in g th e | RL fi n e - | t u n i n g, w | e sa m | p l e t h e |     |     |     |     |     |     |
| --- | ----------- | ----------- | ------ | --------- | ----------- | -------------- | ------ | ----------- | --- | --- | --- | --- | --- | --- |
𝑑 4 𝑑 , 𝑠 .𝑡. 𝑞 ,𝑑 4 wefirstselecteddatasetsfromBEIRthatincludedocument-query
| d o | cu m e n | t 𝑗 ∈ D | =   | { ∀ 𝑗 | ∃ ( 𝑖 𝑗 | ) ∈ T | } a n d | l e ve r - |     |     |     |     |     |     |
| --- | -------- | ------- | --- | ----- | ------- | ----- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
𝐺 ,𝑡 − 1 𝐺 ,𝑡 − 1 t r a in in g d a t a , s u c h a s F i Q A , M S M A R C O , a n d N Q . W e fo ll o w e d th e
| ag  | e G 𝑎 t o | g e n era te | q u e ry ,d | e n o t e | d a s 𝑞 (cid:101)𝑖 . T | h en , th e | r e w a r d | c a n b e |          |                            |                  |             |                |                     |
| --- | --------- | ------------ | ----------- | --------- | ---------------------- | ----------- | ----------- | --------- | -------- | -------------------------- | ---------------- | ----------- | -------------- | ------------------- |
|     |           |              |             |           |                        |             |             |           | e x p er | im e n t a l s e t u p o f | S P T A R [ 3 7] | ,u s in g o | n l y 50 0 d o | cu m e n t- q ue ry |
formulatedasfollows:
pairsasthetrainingsettosimulatethelow-resourceconditions.In
additiontothestandardlow-resourcescenariosmentionedabove,
|     | 𝑟   | =V𝑡(𝑑 ,𝑞 | (cid:101)𝑖)−𝜆log | (cid:0)𝑝(𝑞 (cid:101)𝑖|𝑑 | ,G 𝑎 )/𝑝(𝑞 | (cid:101)𝑖|𝑑 ,G𝑡−1 | )(cid:1), | (11) |     |     |     |     |     |     |
| --- | --- | -------- | ---------------- | ----------------------- | ---------- | ------------------ | --------- | ---- | --- | --- | --- | --- | --- | --- |
𝑞 (cid:101)𝑖,𝑑𝑗 𝑗 𝑗 𝑗 wefollowedtheBEIRbenchmarktovalidatethemodel’szero-shot
performance.DetaileddescriptionsofeachdatasetinBEIRcanbe
where𝜆isthecoefficientfortheKL-divergencetermthatisused foundinAppendixA.1.
tolimittherangeofchangesinthepolicyduringeachupdate[35].
|     |     |     |     |     |     |     |     |     | 5.1.2 | EvaluationMetrics. | Theevaluationofdocumentretrievalper- |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------------------ | ------------------------------------ | --- | --- | --- |
Meanwhile,theadvantagevalueisthedifferencebetweenreward
formancereliesonassessingtherankingquality,measuredthrough
| 𝑟 andthevalueoftheinput𝑑 |     |     |     | 𝑗 estimatedbythecriticmodelas: |     |     |     |     |     |     |     |     |     |     |
| ------------------------ | --- | --- | --- | ------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑐 m e t r ic s i n c l u d i n g M e a n A v e r a g e P re ci s i o n ( M A P ) [ 2 9 ] , R e c a l l [ 2 9 ],
| 𝑎   | =   | 𝑟 − V | ( 𝑑 𝑗 , 𝑞 | ),  | w h e re 𝑞 | d e n ot e s | t h e 𝑘 -t htoken |     |     |     |     |     |     |     |
| --- | --- | ----- | --------- | --- | ---------- | ------------ | ----------------- | --- | --- | --- | --- | --- | --- | --- |
𝑞 (cid:101)𝑖 ,𝑘 ,𝑑 𝑗 𝑞 (cid:101) 𝑖 ,𝑑𝑗 (cid:101)𝑖 , < 𝑘 + 1 (cid:101) 𝑖, 𝑘 N o r m a li z e d D i s c o u n t e d C u m u la te d G a i n s ( N D C G ) [ 2 9 ], a n d M e a n
|     | 𝑞   |     |     |     |     | G 𝑎 |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
in (cid:101) 𝑖 .T h e n , w e ca n o p t i m i z e t h e a ct o r m o d e l b a s e d o n : Re c i p r o c a l R a n k ( M R R ) [2 9 ] . I n th i s p a p e r , w e r e p o r t t h e t o p - 1 0
retrievalperformanceemployingtheabovemetrics—specifically,
𝑎
|     |     |     | ∑︁  | (cid:18) | 𝑝 (𝑞 |𝑑 | 𝑗 ,𝑞 , G | )   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | -------- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
L𝑝𝑝𝑜 =E (cid:101) 𝑖 ,𝑘 (cid:101) 𝑖 ,< 𝑘 𝑎 , M A P@ 1 0 ,R e ca ll @ 1 0, N D C G @ 1 0 , a n d M R R @ 1 0 .
|     |     | 𝑞 ∼ G 𝑎 (   | 𝑑 ) | min | 𝑝 (𝑞 |𝑑 ,        | 𝑞 ,                   | 𝑞 (cid:101)𝑖,𝑘,𝑑𝑗 |     |     |     |     |     |     |     |
| --- | --- | ----------- | --- | --- | ---------------- | --------------------- | ----------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     | (cid:101) 𝑖 | 𝑗   |     | (cid:101) 𝑖, 𝑘 𝑗 | (cid:101) 𝑖, < 𝑘 G 𝑡− | 1 )               |     |     |     |     |     |     |     |
𝑑 𝑗 ∼ D 4 𝑞 (cid:101)𝑖 ,𝑘∈𝑞 (cid:101)𝑖 5.1 .3 I m p le m en t at io n D e ta il s. I n t h e q u er y g e n erationphaseof
|     |     | 𝐺 , | 𝑡− 1 |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:18) 𝑝 (𝑞 |𝑑 ,𝑞 , R 𝑎 ) (cid:19) (cid:19) i G FT , w e u tili z ed Ll a m a- 2 a st he g e n e ra ti v e m o d e l. In th e S F T s t a g e,
|     |     |     | (cid:101) 𝑖 ,𝑘 𝑗 | (cid:101) 𝑖 ,< 𝑘 |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ---------------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
clip ,1−𝜀,1+𝜀 𝑎 𝑞 (cid:101)𝑖,𝑘,𝑑𝑗 , t he A d a m W o p tim i z er w i th a le a r n in g r a te o f 5 𝑒 − 5 w a s u ti l iz e d .
|     |     | 𝑝 (𝑞 | |𝑑 𝑗 , 𝑞                 | , G    | 𝑡− ) |     |     |      |                                                       |     |     |     |     |     |
| --- | --- | ---- | ------------------------ | ------ | ---- | --- | --- | ---- | ----------------------------------------------------- | --- | --- | --- | --- | --- |
|     |     |      | (cid:101) 𝑖, 𝑘 (cid:101) | 𝑖, < 𝑘 | 1    |     |     |      |                                                       |     |     |     |     |     |
|     |     |      |                          |        |      |     |     | (12) | Thetrainingspannedacross3epochs,withabatchsizesetto4, |     |     |     |     |     |
incorporatingtheLoRA[16]techniquetoachieveparametereffi-
ciency.Pleasenotethatinzero-shotscenarios,suchasArguana,
| wherefunctionclip(𝑥,1−𝜀,1+𝜀)limitsthevalueof𝑥 |     |     |     |     |     |     | between |     |     |     |     |     |     |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
duetothelackofdocument-querytrainingdata,weskippedthe
| (1−𝜀,1+𝜀).Finally,thecriticmodelV𝑐 |     |     |                                |       |                   | isoptimizedwithloss |     |     |         |                             |               |             |                 |                       |
| ---------------------------------- | --- | --- | ------------------------------ | ----- | ----------------- | ------------------- | --- | --- | ------- | --------------------------- | ------------- | ----------- | --------------- | --------------------- |
|                                    |     |     |                                |       |                   |                     |     |     | S F T p | r oc e ss f o r t h e L L M | -b as ed q u  | er y g en e | ra t io n m o d | el a n d i ns t e a d |
| function:L𝑐                        |     | =E  | (𝑟                             | −V𝑐(𝑑 | ,𝑞 (cid:101)𝑖))2. |                     |     |     |         |                             |               |             |                 |                       |
|                                    |     | (𝑞  | (cid:101)𝑖,𝑑𝑗) 𝑞 (cid:101)𝑖,𝑑𝑗 |       | 𝑗                 |                     |     |     |         |                             |               | G           |                 |                       |
|                                    |     |     |                                |       |                   |                     |     |     | u se d  | t h e o ri g i n a l L la m | a -2 m o d el | a s .       | M e a n w hi le | , d u r in g e a c h  |
Difficulty-GuidedLearningStrategy:Byleveragingthereward
iterationoftheoptimizationprocess,wesetthelearningrateas
modelandPPO-basedRLalgorithm,wecanupdatethequerygener-
|     |     |     |     |     |     |     |     |     | 1𝑒 −7totraintherewardmodelandupdatethegenerator.The |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------------------------------------------------- | --- | --- | --- | --- | --- |
atorfromG𝑡−1toG𝑡.Additionally,toimprovetheeffectivenessof
batchsizeduringthisphasewasestablishedat8,andthe𝜆inthe
theRLalgorithm,weintroduceadifficulty-guidedlearningstrategy, PPO-basedRLfine-tuningstagewasfixedat0.95.Intheprocessof
sothatG𝑡 canexhibitbetterperformance.
filteringwithsparseretrieval,weemployedtheBM25algorithm,
ConsideringthevaryingcapabilitiesofgeneratorG𝑡−1topro- adjustingtheparametersto𝑏 =0.75and𝑘 =1.5,setting𝑚
1 =100
| duce | informative |     | queries | for different | documents, |     | the difficulty |     |     |     |     |     |     |     |
| ---- | ----------- | --- | ------- | ------------- | ---------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
tosievethroughthesyntheticdataforquality.Concurrently,for
facedbytheRLprocesstofurtherenhanceG𝑡−1togeneratemore
thedenseretrieval-basedfilteringphase,weselectedthehighest-
| i n | f o r m a t iv | e q u e r i e  | s v a rie s | a c r os s do | cu m e n ts   | . S pe c ifi  | ca l ly , g iv | e n t h e |          |                     |                |               |            |                       |
| --- | -------------- | -------------- | ----------- | ------------- | ------------- | ------------- | -------------- | --------- | -------- | ------------------- | -------------- | ------------- | ---------- | --------------------- |
|     |                |                |             |               |               |               |                |           | s c o ri | n g 𝑚 = 4 0 % o f T | 1 a s d e te r | m i n e d b y | R , d e si | g n a ti n g t h es e |
|     |                | 4              |             |               |               |               |                | 𝑑         |          | 2 𝐺                 |                |               | 𝑝 𝑟𝑒       |                       |
| s y | n t h et i c   | d at a T 𝐺 , 𝑡 | , w e e     | s ti m a te   | th e di ffi c | u l ty o f do | c u m e n      | t 𝑗 f o r |          |                     |                |               |            |                       |
− 1 a s m e e ti ng th e fi lt e r’ s c u t -o ff . F u rt h e r m o re , w it h i n t h e p r o ce s s o f
| PPOby |     |     |     |     |     |     |     |     | filteringwiththelosspredictionmodule,weset𝑚 |     |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------------------- | --- | --- | --- | --- | --- |
3 =40%toobtain
thefinalfiltereddataT4.Inaligningwiththeexperimentalsetup
|     |     |     |     |     |     | 𝑟𝑎𝑛𝑘 |     |     |     |     | 𝐺   |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
1 ∑︁ 𝑞 𝑖, 𝑑 o fS P T A R ,t h e C o lB E R T in i G F T w a s tr ain edusingabatchsizeof
|     | diff(𝑑 𝑗)= |     |     |     |     |     | 𝑗   | , (13) |     |     |     |     |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
|{(𝑞 ,𝑑 4 R𝑡−1 (𝑞 , 𝑑 𝑗) 32 a n d a dh e re d t o a le a rn in g r a te o f 2𝑒 − 5.
|     |     | 𝑖                                       | 𝑗) ∈T | 𝐺 ,𝑡−1 }| |              |        | 𝑖   |     |     |                                     |     |     |     |     |
| --- | --- | --------------------------------------- | ----- | --------- | ------------ | ------ | --- | --- | --- | ----------------------------------- | --- | --- | --- | --- |
|     |     |                                         |       |           | (𝑞𝑖,𝑑𝑗 )∈T 𝐺 | 4 ,𝑡−1 |     |     |     |                                     |     |     |     |     |
|     |     |                                         |       |           |              |        |     |     | 5.2 | PerformanceintheLow-ResourceSetting |     |     |     |     |
|     |     | (𝑞 ,𝑑 𝑗)representstherelevancescoreof(𝑞 |       |           |              |        | ,𝑑  |     |     |                                     |     |     |     |     |
whereR𝑡−1 𝑖 𝑖 𝑗)calcu- 5.2.1 BaselineApproaches. ToevaluatetheeffectivenessofiGFTin
latedbythe(𝑡−1)-thiterationdenseretrievalmodeland𝑟𝑎𝑛𝑘
𝑞𝑖,𝑑𝑗
thelow-resourcesetting,wemeticulouslyselectedarangeofcom-
| denotestherankingof𝑑 |     |     | 𝑗 withinallthedocumentsinthecorpusD, |     |     |     |     |     |     |     |     |     |     |     |
| -------------------- | --- | --- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
petitivebaselinemodelsforcomparison.Theseinclude:(1)Sparse
| determinedbydescendingorderofR𝑡−1 |     |     |     |     | (𝑞  | ,𝑑 𝑗).Indeed,diff(𝑑 |     | 𝑗)  |                                                         |     |     |     |     |     |
| --------------------------------- | --- | --- | --- | --- | --- | ------------------- | --- | --- | ------------------------------------------------------- | --- | --- | --- | --- | --- |
|                                   |     |     |     |     |     | 𝑖                   |     |     | retrievalmethods:BM25[43]anditsvariantBM25-tuned[3],em- |     |     |     |     |     |
effectivelyestimatesthecurrentgeneratorcapacitytogeneratein- ployingaLuceneindexforenhancedretrievalefficiency;(2)Dense
| formativefor𝑑 |     | 𝑗.Thus,ahigherdiff(𝑑 |     |     |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | -------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝑗)suggeststhatthegenerator retrievalmodelviasupervisedlearningwithlowresourcedata:Col-
G𝑡−1facesgreaterchallengesinfurtherimprovement.Alongthis
BERT[24];and(3)Denseretrievalmodeltrainedviaunsupervised
line,duringthePPO-basedRLfine-tuningprocess,insteadofusing
learning:ICT[26],MSS[45],andContriever[18].Moreover,wein-
| randomdatashufflingonD |     |     |     | 4   | ,wesequencethedatabasedon |     |     |     |     |     |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
𝐺 ,𝑡−1 corporatedcutting-edgeLLM-basedquerygenerationmethodsthat
thedifficultyleveldifffromlowertohigherforallthe𝑑 𝑗 ∈D 4 . aimtoenhancedenseretrievalmodels,includingDoc2Query[34],
𝐺 ,𝑡−1
1378

FromMisstepstoMastery:EnhancingLow-ResourceDenseRetrievalthroughAdaptiveQueryGeneration KDD’25,August3–7,2025,Toronto,ON,Canada
Table1:Theperformancesinthelow-resourcesettingofourmodelandbaselines.Theorderofthetop10predictionswas
consideredinNDCG,MAP,Recall,andMRR.Thebestresultsareinbold,andthesecond-bestresultsareinunderscored.
| Datasets |     | FiQA |     | MSMARCO |     | NQ  |     |
| -------- | --- | ---- | --- | ------- | --- | --- | --- |
Metrics NDCG MAP Recall MRR NDCG MAP Recall MRR NDCG MAP Recall MRR
BM25 0.1113 0.0697 0.1913 0.1103 0.0343 0.0151 0.1009 0.0158 0.0789 0.0721 0.0914 0.0800
BM25-tuned 0.2361 0.1784 0.2951 0.2889 0.2084 0.1712 0.3787 0.1733 0.2855 0.2454 0.4555 0.2634
ColBERT 0.1149 0.0820 0.1547 0.1675 0.0786 0.0619 0.1301 0.0639 0.2560 0.2029 0.4015 0.2225
ICT 0.1955 0.1515 0.2278 0.2585 0.1389 0.1095 0.2112 0.0980 0.2601 0.1917 0.4012 0.2077
MSS 0.1660 0.1219 0.2167 0.2067 0.1465 0.1180 0.2344 0.1212 0.2414 0.1892 0.3875 0.2047
Contriever 0.2536 0.2002 0.2994 0.3259 0.2056 0.1578 0.3568 0.1611 0.2538 0.1970 0.4128 0.2155
Doc2Query 0.1884 0.1392 0.2362 0.2327 0.1827 0.1503 0.3671 0.1702 0.2648 0.2060 0.4673 0.2216
Doc2Query--
0.2173 0.1676 0.2712 0.2416 0.2044 0.1758 0.3955 0.1818 0.2829 0.2359 0.4938 0.2529
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
|     |     |     |  L * ) 7 w/o  6 5  	  ' 5 |  L * ) 7 w/o  / 3 | iGFT |     |     |
| --- | --- | --- | ----------------------------- | ------------------- | ---- | --- | --- |
FiQA FiQA FiQA FiQA MSMARCO 0.20 MSMARCO 0.400 MSMARCO 0.20 MSMARCO
| 0.30 |     |     | 0.35 |     |     |     |     |
| ---- | --- | --- | ---- | --- | --- | --- | --- |
01@GCDN 01@PAM 01@llaceR 0.35 01@RRM 01@GCDN 0.24 01@PAM 01@llaceR 0.375 01@RRM
| 0.25 | 0.20 |      |      |      | 0.18 |       | 0.18 |
| ---- | ---- | ---- | ---- | ---- | ---- | ----- | ---- |
|      |      | 0.30 | 0.30 | 0.22 |      |       |      |
|      |      |      |      |      |      | 0.350 | 0.16 |
| 0.20 | 0.15 | 0.25 | 0.25 | 0.20 | 0.16 |       |      |
|      |      |      |      |      |      | 0.325 | 0.14 |
100%80%60%40%20% 100%80%60%40%20% 100%80%60%40%20% 100%80%60%40%20% 100%80%60%40%20% 100%80%60%40%20% 100%80%60%40%20% 100%80%60%40%20%
Figure4:ComparisonofiGFT,iGFTw/oLP,andiGFTw/oSR&DRundervariousparametersettings.
|     |     |     |  L * ) 7 w 1 |  L * ) 7 w  5 ' 6 iGFT |     |     |     |
| --- | --- | --- | -------------- | ------------------------ | --- | --- | --- |
0.32 FiQA FiQA 0.375 FiQA FiQA 0.26 MSMARCO MSMARCO 0.42 MSMARCO MSMARCO
|     | 0.24 |     |     |     |     |     | 0.22 |
| --- | ---- | --- | --- | --- | --- | --- | ---- |
01@GCDN 0.30 01@PAM 01@llaceR 0.350 01@RRM 0.35 01@GCDN 01@PAM 0.20 01@llaceR 0.41 01@RRM
| 0.28 | 0.22 | 0.325 |      | 0.24 |      | 0.40 | 0.20 |
| ---- | ---- | ----- | ---- | ---- | ---- | ---- | ---- |
|      |      |       | 0.30 |      | 0.18 |      |      |
| 0.26 | 0.20 | 0.300 |      |      |      | 0.39 | 0.18 |
|      |      |       | 0.25 | 0.22 |      | 0.38 |      |
1 2 3 4 5 1 2 3 4 5 1 2 3 4 5 1 2 3 4 5 1 2 3 4 5 1 2 3 4 5 1 2 3 4 5 1 2 3 4 5
|     | Figure5:ComparisonofiGFT,iGFTwG |     |     | 1,andiGFTwRDSatdifferentiterations. |     |     |     |
| --- | ------------------------------- | --- | --- | ----------------------------------- | --- | --- | --- |
Doc2Query--[11],DocT5Query[33],GPL[52],InPars[4],InPars- observations:(1)OuriGPTconsistentlyoutperformsallbaseline
v2[19],UDAPDR[44],Promptagator[8],andSPTAR[37].Further- modelsacrosseverydataset,markingsignificantadvancements.
more,weutilizedChatGPTforthequerygenerationprocessfor Specifically,comparedtothebestperformancesofallbaselines
comparativeanalysis.Inourexperimentalsetup,weappliedboth acrossvariousmetrics,ouriGFTachievesanaverageimprovement
ouriGFTandaboveLLM-basedmethodstoapre-trainedColBERT, of17.80%,17.55%,10.03%,and10.13%ontheNDCG@10,MAP@10,
whichensuredafairanddirectcomparisonofperformance. Recall@10,andMRR@10,respectively,acrossthethreedatasets.
(2)WecanobservethatColBERT,relyingonsupervisedlearning,
5.2.2 ExperimentalResults. Table1showcasesthecomparative doesnotoutperformallsparseretrievalmethods.Thisindicatesthat
denseretrievalmodelstrainedsolelyonannotateddatastruggleto
| performance | analysis of | the proposed iGFT | framework against |     |     |     |     |
| ----------- | ----------- | ----------------- | ----------------- | --- | --- | --- | --- |
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

| KDD’25,August3–7,2025,Toronto,ON,Canada |     |     |     |     |     |     | ZhenyuTongetal. |
| --------------------------------------- | --- | --- | --- | --- | --- | --- | --------------- |
TableS1:Theperformancesinthezero-shotsettingofourmodelandrepresentativebaselinesonallaccessibledatasetsinthe
BEIRbenchmark.
Models QGen InPars-v2 LaPraDoR Ours InPars-v2* LaPraDoR* Ours*
| FiQA        | 0.3082 | 0.3243 | 0.3290 | 0.3628 | 0.5085 | 0.4973 | 0.5202 |
| ----------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| NQ          | 0.3583 | 0.4532 | 0.4872 | 0.5221 | 0.6382 | 0.7072 | 0.7119 |
| HotPotQA    | 0.5245 | 0.5406 | 0.6241 | 0.6665 | 0.7912 | 0.7832 | 0.8215 |
| Quora       | 0.8129 | 0.8080 | 0.8692 | 0.8468 | 0.8451 | 0.8946 | 0.8889 |
| CQADupstack | 0.3589 | 0.3019 | 0.2427 | 0.3792 | 0.4483 | 0.4672 | 0.4925 |
| TREC-COVID  | 0.6083 | 0.7184 | 0.7389 | 0.7712 | 0.8462 | 0.8518 | 0.8792 |
| NFCorpus    | 0.3032 | 0.3341 | 0.3246 | 0.3815 | 0.3845 | 0.4409 | 0.4252 |
| Trec-News   | 0.3872 | 0.3825 | 0.4481 | 0.4323 | 0.4902 | 0.5241 | 0.5135 |
| Robust04    | 0.3567 | 0.4285 | 0.4901 | 0.4805 | 0.6322 | 0.6018 | 0.6312 |
| ArguAna     | 0.4934 | 0.4725 | 0.5072 | 0.5105 | 0.4690 | 0.5273 | 0.5583 |
| Touche-2020 | 0.1822 | 0.2845 | 0.3241 | 0.3107 | 0.2905 | 0.3305 | 0.3175 |
DBPedia-Entity 0.3281 0.4192 0.4189 0.4624 0.4979 0.4902 0.5123
| SciDocs | 0.1429 | 0.1129 | 0.1829 | 0.1675 | 0.2083 | 0.2472 | 0.2238 |
| ------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Fever   | 0.6693 | 0.6671 | 0.6821 | 0.7894 | 0.8715 | 0.7894 | 0.8714 |
Climate-Fever 0.1755 0.1725 0.2267 0.1947 0.3234 0.3371 0.3451
| SciFact | 0.6429 | 0.6825 | 0.6882 | 0.7430 | 0.7743 | 0.7523 | 0.7962 |
| ------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ |
| Avg.    | 0.3913 | 0.4178 | 0.4461 | 0.4718 | 0.5637 | 0.5776 | 0.5943 |
TableS2:Theefficiencyofstaticgeneratoranditerativeup-
data,ourproposedmethodisdemonstratedtobemoreefficient.
datedgenerator. Moreover,wehaveconductedanadditionalexperimenttoillustrate
theperformancedifferencesbetweenthemodelswhenallocated
| Models | NDCG MAP | Recall MRR Time | FLOPS |     |     |     |     |
| ------ | -------- | --------------- | ----- | --- | --- | --- | --- |
thesametimebudgetperiterationinTableS3.Thishighlightsthat
| Staticgenerator | 0.3262 0.2568 | 0.5225 0.2826 1.6h | 24.32PFLOP |     |     |     |     |
| --------------- | ------------- | ------------------ | ---------- | --- | --- | --- | --- |
Iterativeupdatedgenerator 0.3312 0.2583 0.5273 0.2925 2.1h 34.13PFLOP ouriterativeoptimizationprogressivelyunlocksthelatentpoten-
TableS3:Theperformanceofstaticgeneratoranditerative tialofthegenerator,enablingmoreefficientimprovementsinthe
performanceofthedenseretrievalmodelwhilemaintainingthe
updatedgeneratoroveriterations.
samecomputationalresourceconstraints.Incontrast,thestatic
Models Staticgenerator generatorfacesaperformancebottleneck,limitingitseffectiveness.
#Iteration NDCG MAP Recall MRR Comparedtootherquerygenerationmodels,whichdonotuse
iterativecomputations,ourmodelismorecomputationallyefficient
| 1   | 0.3281 0.2402 | 0.4817 0.3491 |     |     |     |     |     |
| --- | ------------- | ------------- | --- | --- | --- | --- | --- |
inthenon-iterativesetting,withInPars[4],Promptagator[8],and
2 0.3581 0.2517 0.4991 0.3518 UDAPDR[44]taking2.03h,2.5h,and1.92h,respectively,whileour
3 0.3579 0.2502 0.4969 0.3512 modelrequiresonly1.6h.Withiterativecomputations,ourmodel
takes2.1h,9.38%morethanthenon-iterativeapproach.However,
| Models | Iterativeupdatedgenerator |     |     |     |     |     |     |
| ------ | ------------------------- | --- | --- | --- | --- | --- | --- |
asshowninpreviousexperiments,thisadditionalcostisjustified
| #Iteration | NDCG MAP | Recall MRR |     |     |     |     |     |
| ---------- | -------- | ---------- | --- | --- | --- | --- | --- |
bythesignificantperformancegainsindenseretrievalachieved
throughiteration.
| 1   | 0.3672 0.2549 | 0.5117 0.3682 |     |     |     |     |     |
| --- | ------------- | ------------- | --- | --- | --- | --- | --- |
| 2   | 0.4002 0.3434 | 0.5310 0.3940 |     |     |     |     |     |
A.3 AddtionalEvaluationintheZero-Shot
| 3   | 0.4218 0.3842 | 0.5720 0.4182 |     |     |     |     |     |
| --- | ------------- | ------------- | --- | --- | --- | --- | --- |
Setting
|     |     |     |     | Following | the experimental | setup in Section | 5.5, we compared |
| --- | --- | --- | --- | --------- | ---------------- | ---------------- | ---------------- |
A.2 TheTimeCostoftheIterativeOptimization
ourmethodwithseveralrepresentativebaselinesonallaccessi-
Weconductedadetailedanalysisoftheiterativeefficiencyduring
bledatasetsintheBEIRbenchmark.Theresultsarepresentedin
thetrainingprocessontheFiQAdataset.AsillustratedinTableS2, Table S1. Specifically, we found that our approach achieved an
whilemaintaininganequivalenttotaloutputofpseudoqueries,we averageimprovementof20.57%,12.92%,and5.76%inNDCG@10
comparedthetrainingdurationforthereinforcementlearning(RL) acrossallaccessibledatasetsintheBEIRBenchmark,comparedto
processwiththetimeandflops(floatingpointoperations)required QGen,Inpars-v2,andLaPraDoR,respectively.Afterincorporating
foreachroundofdirectgeneration.Ourfindingsrevealthatgener-
areranker,ourapproachcontinuestoachieveimprovementsof
atinganequivalentnumberofqueriesusingtheiterativemethod 5.43%and2.89%forInPars-v2andLaPraDoR,respectively.These
requires31.25%moretimeand40.33%moreflops.Consideringthe experimentalresultsprovidestrongevidencethatourproposed
additionaltrainingoverheadofRL,coupledwiththefactthatthe iGFTmethoddeliverssuperiorperformanceinthevastmajorityof
iterativeupdatedgeneratorismoreadeptatproducinghigh-quality zero-shotscenarios.
1384