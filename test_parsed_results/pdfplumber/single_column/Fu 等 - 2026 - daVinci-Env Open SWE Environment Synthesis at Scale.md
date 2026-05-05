# Fu 等 - 2026 - daVinci-Env Open SWE Environment Synthesis at Scale

SII-GAIR
daVinci-Env: Open SWE Environment Synthesis at Scale
DayuanFu*1,3 ShenyuWu*2,3 YunzeWu*2,3 ZeruiPeng*2,3 YaxingHuang*2,3 JieSun*1 JiZeng2,3
MohanJiang1,2 LinZhang2,3 YukunLi2 JiaruiHu1 LimingLiu1 JinlongHou†1 PengfeiLiu†1,2,3
1SII 2SJTU 3GAIR
Abstract
Training capable software engineering (SWE) agents demands large-scale, executable, and verifiable
environmentsthatprovidedynamicfeedbackloopsforiterativecodeediting,testexecution,andsolution
refinement. However,existingopen-sourcedatasetsremainlimitedinscaleandrepositorydiversity,while
industrial solutions are opaque with unreleased infrastructure, creating a prohibitive barrier for most
academicresearchgroups. WepresentOpenSWE,thelargestfullytransparentframeworkforSWEagent
traininginPython,comprising45,320executableDockerenvironmentsspanningover12.8krepositories,
withallDockerfiles,evaluationscripts,andinfrastructurefullyopen-sourcedforreproducibility.OpenSWE
isbuiltthroughamulti-agentsynthesispipelinedeployedacrossa64-nodedistributedcluster,automating
repositoryexploration,Dockerfileconstruction,evaluationscriptgeneration,anditerativetestanalysis.
Beyondscale,weproposeaquality-centricfilteringpipelinethatcharacterizestheinherentdifficultyofeach
environment,filteringoutinstancesthatareeitherunsolvableorinsufficientlychallengingandretaining
only those that maximize learning efficiency. With $891K spent on environment construction and an
additional$576Kontrajectorysamplinganddifficulty-awarecuration,theentireprojectrepresentsatotal
investmentofapproximately$1.47million,yieldingabout13,000curatedtrajectoriesfromroughly9,000
qualityguaranteedenvironments. ExtensiveexperimentsvalidateOpenSWE’seffectiveness: OpenSWE-
32BandOpenSWE-72Bachieve62.4%and66.0%onSWE-benchVerified,establishingSOTAamong
Qwen2.5series. ModelstrainedonOpenSWEconsistentlyoutperformthosetrainedonSWE-rebench
acrossallsettings,withalog-lineardatascalingtrendshowingnosaturation. Moreover,SWE-focused
training yields substantial out-of-domain improvements, including up to 12 points on mathematical
reasoningand5pointsonsciencebenchmarks,withoutdegradingfactualrecall. Allenvironmentsand
evaluationscriptsarepubliclyavailableathttps://github.com/GAIR-NLP/OpenSWE.
Figure1: ImageconstructionandperformanceoverviewofOpenSWE.
1*Equalcontribution.
2†Correspondingauthors.
1
6202
raM
61
]ES.sc[
2v32031.3062:viXra
SII-GAIR
1.Introduction
1 Introduction
TherapidadvancementofLargeLanguageModels(LLMs)hascatalyzedthedevelopmentofautonomoussoftware
engineering(SWE)agents(Yangetal.,2024;Teametal.,2025a;Jiangetal.,2026). Thesesystemscaninterpret
complexrequirements,navigateextensivecodebases,iterativelyeditcode,runtests,andrefinesolutionswithout
humanintervention(Fuetal.,2025). Unlikestaticcodegeneration,theseagentsrequireverifiableandexecutable
environmentslikeDocker(Jimenezetal.,2023;Xiaetal.,2024)toprovidedynamicfeedbackloops: theymust
compilecode,executetests,andobserveruntimebehaviorstoiterativelyrefinetheirsolutions(Yaoetal.,2023).
However,constructinghigh-qualityanddiverseexecutableenvironmentsatscaleremainsacriticalbottleneck.
Whilerecentopen-sourceeffortssuchasSWE-rebench(Badertdinovetal.,2025),SWE-Universe(Chenetal.,
2026b), and SWE-Factory (Guo et al., 2026) have made progress toward automation, the resource barrier is
prohibitive: the computational and infrastructure costs of generating validated environments at scale remain
extraordinarilyhigh,effectivelyexcludingmostacademicresearchgroupsandcreatingastarkdividebetween
industrialsolutions,whichachievescalebutremainopaquewithunreleasedinfrastructure(Chenetal.,2026b;Liu
etal.,2025a),andopen-sourcealternativesthatremainlimitedinbothscaleandrepositorydiversity.
Beyondthecostofenvironmentconstruction,thequalityanddifficultydistributionoftheseenvironmentsare
equallycriticalforeffectiveagenttraining. Whilescalingthenumberofenvironmentsisanecessarycondition,
itisfarfromsufficientonitsown. AsillustratedinFigure2, environmentssynthesizedfromrealrepositories
frequentlysufferfromPR-Issuemisalignment,wherethesubmittedpatchdoesnotactuallyresolvethedescribed
issue,ortriviality,wheretheissuedescriptiondirectlyrevealsthesolution. Suchenvironmentsareeithereffectively
unsolvableortoosimpletoprovidemeaningfullearningsignal. Morebroadly,thedifficultydistributionacross
environmentsplaysadecisiveroleintrainingeffectiveness,andidentifyingthesubsetatappropriatedifficulty
levelsthatmaximizeslearningefficiencyrequiressystematicevaluationandcarefulcuration.
Inthiswork,weaddressbothchallengesbyintroducingOpenSWE,thelargestfullytransparentframework
forSWEagenttrainingtodate. OpenSWEcomprises45,320executableDockerenvironmentsspanning12.8k
repositories,representingover$891,000inconstructioncosts,withallDockerfiles,evaluationscripts,anddis-
tributedinfrastructurefullyopen-sourced. Unlikepriorwork,wereleasenotonlythefinalenvironmentsbutalso
thecompletesynthesispipeline: amulti-agentsystemdeployedacrossa64-nodeclusterthatautomatesrepository
exploration,Dockerfileconstruction,evaluationscriptgeneration,anditerativetestanalysis. Toensuredataquality
beyond mere scale, we propose a quality-centric filtering pipeline that characterizes the inherent difficulty of
eachenvironment,filteringoutthosethatareeitherunsolvableorinsufficientlychallengingandretainingonly
environmentsatappropriatedifficultylevelsthatprovidethemosteffectivelearningsignal. Thislarge-scaletrajec-
torysamplingandcurationprocessrequiresanadditionalcomputationalinvestmentofapproximately$576,000,
ultimatelyyieldingabout13,000curatedtrajectoriesfromasubsetofroughly9,000high-qualityenvironments.
ExtensiveexperimentsonthesetrajectoriesvalidatetheeffectivenessofOpenSWEandhighlightthecomple-
mentaryrolesofdatascalinganddifficulty-awarecuration. Modelstrainedonourcuratedtrajectoriesachieve
62.4%(32B)and66.0%(72B)onSWE-BenchVerified,establishingstate-of-the-artamongsupervisedfine-tuning
methods and consistently outperforming SWE-rebench-trained models across all configurations. Data scaling
analysisrevealsalog-linearimprovementtrendwithnosaturation,confirmingthatadditionalhigh-qualityenvi-
ronmentscontinuetoyieldmeaningfulgains. Equallyimportant,difficulty-awarefilteringcontributesmeasurably
beyondrawscale: byretainingenvironmentsattheappropriatedifficultyfrontier,trainingefficiencyimproves
significantly compared to using all environments indiscriminately. Furthermore, training on OpenSWE yields
substantialout-of-domainimprovements,includingupto12pointsonmathematicalreasoningandupto5points
onsciencebenchmarks,withoutdegradingfactualrecall.
Thespecificcontributionsofthisworkare:
• Unprecedented Scale with Full Transparency: We release 45,320 executable environments from 12.8k
repositoriesataconstructioncostof$891K,withcompleteinfrastructureincludingallDockerfiles,evaluation
scripts,andthedistributedsynthesispipeline,enablingreproducibilityandcommunity-drivenimprovements.
• Quality-CentricFilteringviaDifficulty-AwareCuration: Weproposeafilteringpipelinethatcharacterizes
environmentdifficultytofilteroutunsolvableandtriviallysimpleinstances.Withanadditional$576Kinvestment
intrajectorysamplingandcuration,weobtainabout13,000curatedtrajectoriesfromroughly9,000high-quality
environments.
• Strong Empirical Validation with Scaling and Curation Insights: OpenSWE-trained models establish
newSOTAresults(62.4%/66.0%)amongSFTmethodsunderQwen2.5series,consistentlyoutperformSWE-
rebenchacrossallscalesandscaffolds,andexhibitlog-linearscalingwithnosaturation. Bothdatascalingand
difficulty-awarefilteringareshowntobeessentialandcomplementarydriversofagentperformance.
2
SII-GAIR
2.RelatedWork
PR-Issue Misalignment Unsolvable Triviality Low Value
📋 Issue Description 🔧 Actual Patch 📋 Issue Description 🔧 Actual Patch
“ ... repo_resolver.py doesn't accept shorthand @@ repo_resolver.py @@ “ mistake in writing @@ src/ZEO/__init__.py @@
commit values. I suggest adding a check else: ZEO/src/ZEO/__init__.py def connection(*args, **kw):
- if repo.head.commit == commit: ...
for a full commit hash value near line 215: + if repo.head.commit == commit line 43 ra should be raise except Exception:
if len(commit) != 40: + or repo.head.commit[:7] == commit: db.close()
logger.critical("Dependency {0} has a m ... - ra
alformed commit hash. Fail.") + raise
...
Instance ID: tianocore__edk2-pytool-extensions-371 Instance ID: zopefoundation__ZEO-103
Figure2: TwospecificrisksinSWEtasks. Left: ThePRisunsolvablebecausethefirstsevencharactersofthe
commithashcanpassthetest,whereastheissuerequirescheckingthefullhash. Right: ThePRistrivial,sincethe
issuehavejusttellthemodifiedfileandthestringthatshouldbechanged.
2 RelatedWork
2.1 EnvironmentSynthesis
The construction of executable environments for agents has become a central infrastructure challenge. SWE-
bench(Jimenezetal.,2023)pioneeredthisdirectionbycuratingabenchmarkofrealGitHubissuespairedwith
pullrequests,whereeachtaskinstanceisembeddedinaDocker-basedrepositorysnapshotwithexecutabletest
suites that serve as evaluation oracles. To overcome this bottleneck, several concurrent efforts have emerged
toautomatelarge-scaleenvironmentgeneration. SWE-rebench(Badertdinovetal.,2025)introducesascalable
pipelinethatreplicatestheSWE-benchconstructionprocessacrossabroadersetofrepositories,aimingtogenerate
thousandsofadditionaltaskinstanceswithexecutabletestenvironments.SWE-Universe(Chenetal.,2026b)takesa
complementaryapproachbysystematicallycrawlingandfilteringGitHubrepositoriestoproduceadiverseuniverse
ofcandidateenvironments. SWE-Factory(Guoetal.,2026)andScale-SWE(Zhaoetal.,2026)furtherautomate
theend-to-endpipelinefromrepositoryselectiontoDockerfilesynthesisandtestharnessgeneration. Scale-SWE
furtherscalesthisparadigmthroughasandboxedmulti-agentworkflow. BeyondSWE(Chenetal.,2026a)expands
theevaluationscopebeyondsingle-repositorybugfixingbyintroducingmorecomplexreal-worldscenariossuchas
cross-repositoryreasoning,dependencymigration,anddomain-specificdevelopmenttasks.SWE-World(Sunetal.,
2026)proposesanorthogonaldirectionbyreplacingphysicalDockerexecutionwithlearnedsurrogatemodels
trainedonagent-environmentinteractiondata,eliminatingtheresource-intensivecostsofDockerenvironment
maintenancewhilepreservingtheagent-environmentfeedbackloop.
2.2 SWEAgentsTraining
Thedevelopmentofautonomoussoftwareengineeringagentshasprogressedrapidlyfromsimplecodecompletion
tocomplex,multi-steptaskresolutioninreal-worldrepositories. ToenableLLMstointeracteffectivelywiththese
repositories,agentscaffoldshaveemergedascriticalinfrastructure. SWE-agent(Yangetal.,2024)servesasa
foundationalexample,establishingabaselinewhereagentscanautonomouslynavigatecodebases,localizebugs,
andgeneratepatches. Buildingonsimilararchitecturalprinciples,OpenHands(Wangetal.,2025b)providesan
extensibleopen-sourceplatformutilizingtheCodeActframework,whichallowsagentstointerleavecodeexecution
andnaturallanguagereasoningwithinaunifiedactionspace.
Onthetraininganddatasynthesisside,SWE-smith(Yangetal.,2025a)constructsalarge-scaletrainingdata
synthesispipelinethatgeneratesdiversetaskinstancesandexecutiontrajectoriesforsupervisedfine-tuningofSWE
agents,enablingthetrainingofopen-weightSWEagentsfromscratch. daVinci-Dev(Zengetal.,2026)takesa
differentapproachbycombiningstructuredplanningwithiterativecodegenerationanddebugging,leveraging
multi-stepreasoningtracestoproducehigh-qualityresolutiontrajectories. SWE-Fixer(Xieetal.,2025)focuses
onscalingsupervisedfine-tuningwithfiltered,high-qualityresolutiontrajectories. TheSWE-Master(Songetal.,
2026)technicalreportsystematicallycomparestheserepresentativeapproaches.
3 Method
3.1 GithubPRCollection
WecollectGitHubPRsfromabroadsetofPythonrepositoriesthroughGitHubREST1andGraphQLAPIs.2 For
eachrepository,weobtainPRmetadataandselectivelyqueryadditionalendpointsfordetailedcontent,including
linkedissuedescriptionswhenavailable,andthefullcommitsequencewithcorrespondingdiffs.
1https://docs.github.com/en/rest
2https://docs.github.com/en/graphql
3
SII-GAIR
3.2 GitHubPRFiltering
GitHub PRs Construction Buffer
Repo
Pull Requests 200 Exploration
Issue Desc …… Master
Issue Unique
C++ Code Materials 200 Dockerfile
Construction
Pull Requests
Issue Desc Eval Script
Construction
Issue ……
Python Code
Node 1 Node 2 Node n Environment
Pull Requests Evaluation
Issue Desc
Python Code Common
Materials Test
Analysis
Pull Requests
Issue Desc
Python Code Local GitHub Repos Pre-definedDockerImages Cloud
Figure3: TheframeworkofOpenSWE.
3.2 GitHubPRFiltering
ThefilteringprocessoperatesontheGitHubPRdatasetobtainedthroughthecollectionpipelinedescribedabove.
Eachentrycomprisesfouressentialfields: repositoryidentifier,PRnumber,associatedissues,andthecompletePR
patchencompassingallcodemodifications.
ToguaranteethequalityandsuitabilityofPRs,weapplyafour-stagefilteringpipeline:
RepositoryViability. Toimprovetherepresentativenessofourdataset,weretainonlyrepositorieswithatleast
fiveGitHubstars,usingstarcountasaproxyforcommunityvalidationandprojectmaturity. Thiscriterionexcludes
nascentorunmaintainedprojectsthatareunlikelytoreflectreal-worldsoftwareengineeringpractice.
LanguageFilter. WeconstrainthedatasettoPRsfromrepositorieswhoseprimaryprogramminglanguageis
Python,asdeterminedbyGitHub’slanguagedetection. Thisalignswiththepredominantlanguagecoveragein
existingcodegenerationbenchmarksandensuresevaluationconsistency.
IssueRequirement. Sinceeverytaskshouldbegroundedinawell-definednaturallanguageproblemstatement,
eachPRisrequiredtohaveatleastoneassociatedissuewithanissuedescription. PRslackinglinkedissuesor
containingonlyemptyissuedescriptionsareexcludedduetotheabsenceofsufficienttaskspecification.
SubstantiveCodeChanges. Inordertoguaranteethateachinstancetestsrealimplementationabilityrather
thanauxiliarytestingeffort,werequirenon-emptypatchestonon-testcodeandexcludePRswhosechangesare
confinedentirelytotestdirectoriesortestfiles(like*tests*,*spec*,or*e2e*initspath).
Afteridentifyinghigh-qualityPRcandidates,weuseamulti-agentsystemtotransformtheselectedPRsintoreal
SWEenvironments. EachenvironmentrequiresareproducibleDockercontainerwiththecorrectdependencies,as
wellasavalidatedevaluationscriptcapableofconfirmingwhetheranagent’ssolutioniscorrect.
3.3 RepositoryExploration
Weintroducealightweightrepositoryexplorationagentthatbridgesrawrepositorystateanddownstreamenvi-
ronmentgeneration. Theagentisinitializedwithrepository-levelmetadata(repositoryname, commit/version,
andpatch-derivedfilecues)andperformsboundedexplorationoverthelocalcheckouttocollectonlysetup-and
test-relevantevidenceforsubsequentagents.
Targeted Retrieval Interface. The agent operates through three constrained repository APIs: (1) browse
forstructuralinspection,(2)searchforlocatingcandidateconfigurationfiles,and(3)digestforextracting
actionablesetupandtestinstructionsfromselectedfiles.Thisinterfaceisintentionallynarrow,encouraginglow-cost
retrievalcenteredonhigh-yieldartifactssuchasREADME.md,CONTRIBUTING.md,dependencymanifests,and
CIworkflows.
Cost-AwareIterativePolicy. Explorationproceedsinmultipleroundsandfollowsaconservativepolicy: in
the absence of explicit failure feedback, the agent performs shallow, document-first inspection; when the test
analysisagentreportsmissingcontext,retrievalisredirectedtoonlytherequestedfilesorconfigurationdimensions.
Thisdesignreducesredundantrepositorytraversalwhilepreservingtheabilitytorecoverfromenvironmentor
test-commandambiguityinlateriterations.
4
SII-GAIR
3.4 DockerfileConstruction
MinorImplementationDetails. Weincludeseveralsmallimplementationdetailsinthisstage: (1)theextraction
scopeexplicitlycapturesPython-specificenvironment-managementframeworks(e.g.,poetry,uv)inaddition
totestframeworks,tohelptheDockerconstructionagentretrieveenoughcontextinadvance;and(2)API-call
parsingandargumentvalidationareenclosedinexception-safehandlingtopreventmalformedinvocationsfrom
terminatingretrievalrounds.
3.4 DockerfileConstruction
The Dockerfile agent is responsible for generating an environment for each task. During the pilot study, we
identifiedtworecurringfailuremodes: (1)networkinstabilityduringenvironmentconstruction,wheregenericbase
imagesrequiredownloadingPythonanddependenciesatbuildtime,leadingtofrequenttimeouts;and(2)redundant
rebuilds, where unchanged base layers are reconstructed from scratch on every iteration. These inefficiencies
becomeparticularlycostlyatscale;therefore,weequiptheDockerfileagentwiththefollowingstrategies.
BaseImageStrategy. RatherthanstartingfromgenericUbuntuimagesthatrequireruntimePythoninstallation,
wepre-buildasuiteofopenswe-pythonbaseimagescoveringPython2.7and3.5–3.14,eachbundledwith
a conda package, a pre-activated testbed environment, and configured package mirrors for reliability. This
eliminatesthemostcommonsourceofbuildfailures—networktimeoutsduringdependencyinstallation—and
enablesimmediatelayerreuseacrosstaskssharingthesamePythonversion.
RepositoryProvisioning. Insteadofcloningrepositoriesinsidethecontaineratbuildtime,wemaintainalocal
barerepositorycacheandinjectthecodebaseviaCOPY,witheachtask’stargetcommitcheckedoutinadvance.
ThisremovesGitHubAPIratelimitsandnetworkfailuresfromtheagentloopentirelyandimprovesreproducibility
by eliminating dependence on external availability. It also reduces the error rate of the agent by avoiding the
repetitionoflongcommithashes.
Layer-AwarePromptingandPython-SpecificOptimizations. Weobservethatintypicalagenticworkflows,
dependencyspecificationsarerevisedfarmorefrequentlythantheDockerfilestructureitself. Leveragingthis
observation,weexplicitlyinstructtheagenttoplacestablebaselayersearlyintheDockerfilesotheyarecachedby
Docker,andtoisolatedependencyinstallationintolaterlayersthatcanbecheaplyrebuiltacrossiterations. This
yieldssignificantspeedupswhentheagentiteratesondependencyfixeswithoutalteringthebaseenvironment.
PromptsalsoenforcePython-specificcorrectnessrequirements,includingpropercondaenvironmentactivation,
development-modepackageinstallation,anddeferredtestexecutiontotheevaluationscript.
TheDockerfileagentwillreceivetherepositoryexplorationagent’sfindings(e.g.,specialdependenciesfrom
README.md)asadditionalinput,allowingtheagenttomakemoreinformedinitialdecisions,anditwilloperate
iterativelytoconstructtheDockerfile. Ifthefinaltestexecutionfails,theDockerfileagentwillalsoreceivethe
feedbackfromthetestanalysisagentandrefineitsoutputinsubsequentattempts.
3.5 EvaluationScriptConstruction
Theevaluationscriptagentgeneratesbashscriptsthatverifyrepaircorrectnessbyexecutingtestsandconfirming
thatfailuresintroducedbytheissuecanberesolvedbythepatchunderevaluation. Thecentralchallengeisprecise
testtargeting: onlythetestcasesdirectlyrelevanttotheissueshouldbeexecuted. Accordingly,theagentidentifies
thespecifictestfilestiedtotheissueand,whennecessary,synthesizesnewtestcasestocoverscenariosnotpresent
intheoriginalPR.
TestDesign. BecausetheagentmayintroducenewtestcasesbeyondthoseintheoriginalPR,thestaticfail2pass
scriptsusedinSWE-Bencharenolongerapplicable. Weinsteadinstructtheagenttoconstructastructuredbash
script from scratch, incorporating: (1) the selected and synthesized test cases with correct exit code capture;
(2) output delimiters marking the start and end of test output for reliable log parsing; and (3) a dedicated exit
codemarker(OPENSWE EXIT CODE)embeddedinthescriptoutput,whosevalueservesasthefinalsignalfor
determiningrepaircorrectness.
Script Design. To support stable iteration, the script is template-based, separating patch injection from test
commandlogicsothattheagentcanrefinetestinvocationsacrossiterationswithoutregeneratingtheentirescript.
Forconda-basedenvironments,explicitactivationsequencesareenforcedtopreventsubtlePATHissuesthatwould
silentlycorrupttestresults.
Like the Dockerfile agent, the evaluation script agent operates within the same iterative feedback loop: the
repository exploration agent and Dockerfile agent supply repository context prior to generation, and after test
execution,thetestanalysisagentinspectsthefinalresultofthetestexecutionanddetermineswhethertherepairis
correct. Ifnot,itwillprovidefeedbacktotheevaluationscriptagenttorefinethescriptforthenextiteration.
5
SII-GAIR
3.6 EnvironmentEvaluation
3.6 EnvironmentEvaluation
With the Dockerfile and evaluation script in place, the pipeline proceeds to rule-based validation. For each
iteration,theDockerimageisbuiltonceandtheevaluationscriptisexecutedundertwoconditions: firstapplying
atest-onlypatchtoverifythatthetestsindeedfailontheunpatchedcodebase,thenapplyingthefullfixpatch
to verify that all tests pass. A sample is accepted only when both conditions are met. The exit code marker
OPENSWE EXIT CODE=Xisparsedfromscriptoutputviaregex;ifthemarkerisabsent,validationismarkedas
failedandtargetedfeedbackisreturnedtotheagent.
Tosupportthisvalidationatscale,weintroducetwoinfrastructureoptimizations. First,toensurereproducible
results and prevent resource contention across concurrent evaluations, each container is bound to 4 dedicated
CPUcores,a24GBmemorycap,anda200GBstoragelimit. Second,ratherthandiscardingimagesafterevery
iteration,weretainimagesuntiltheDockerfilechanges—yieldinga5×speedupinthecommoncasewhereonlythe
evaluationscriptisrevised. Successfullyvalidatedimagesarepushedtoaremoteregistryforreuseinsubsequent
trainingandevaluation.
3.7 TestAnalysis
Oncetherule-basedvalidationcompletes,thetestanalysisagentexaminestheresultsregardlessofwhetherthe
samplepassedorfailed. Onpassingresults,itinspectsthelogstoverifythatthesuccessisgenuine—checking
thattheevaluationscriptdoesnotcontainhardcodedexitcodesorothershortcutsthatbypassrealtestexecution.
Onfailures,itdiagnosestherootcause: aDockerfilemisconfiguration,anevaluationscripterror,oraninherently
unsolvableenvironment(e.g.,conflictingdependencies,unavailablePythonversions).Forfixableerrors,itgenerates
targeted feedback that is routed back to the responsible agent for the next iteration; for inherently unsolvable
cases,itmarksthesampletoenableearlyexit. Thefinaldatasetretainsonlysamplesthatpassboththerule-based
evaluationandtheagent’slegitimacycheck.
3.8 Multi-MachineConstruction
Tofacilitatethelarge-scalesynthesisdescribedinSection1,wedeployedadistributedcomputingclustercomprising
64ElasticComputeService(ECS)instances.Thisinfrastructureenablesthesimultaneousprocessingofanextensive
corpusofapproximately572,114GitHubPRsbyparallelizingtheDocker-basedevaluationpipelineacrossisolated
nodes. WeuseDeepseek-v3.2(Liuetal.,2025a)astheconstructionmodel.
Constructingenvironmentsatthisscalepresentssignificantengineeringchallenges:
• ExecutionInstability: Thepipelinereliesonnon-deterministicexternalfactors,includingLLMAPIlatency,
network-dependentdependencyresolution,andtheexecutionofagent-synthesizedscripts,allofwhichcanlead
tounexpectedprocesscrashes.
• ResourceContention: StandardDockerengineslackthegranularresourceisolationrequiredtopreventmemory
exhaustion(OOM)ordisksaturationduringintensivebuilds,potentiallydestabilizingthehostnode.
Toaddressthese,wedesignedadecoupled,fault-tolerantparallelizationframework:
• Data Parallelism with Minimal Coupling: We adopted a data-parallel approach to minimize inter-node
dependencies. UnliketightlycoupledframeworkssuchasMPIorRay,whereasinglenodefailurecanhaltthe
entirejob,ourarchitectureensuresthatnodesoperateindependently.
• SharedFilesystemMessageQueue: Communicationandtaskdistributionaremanagedthroughafile-based
messagequeuehostedonasharedfilesystem. Thisdesigndecouplesthetaskproducerfromtheconsumers,
ensuringthatindividualnodefailuresdonotresultindatalossorsystem-wideparalysis.
• ResilientProcessManagement:Allsynthesisprocessesaremanagedviasystemdservices.Thisconfiguration
providesautomatedservicerecoveryandrestartsintheeventofunexpectedsoftwaretermination.
• Automated Resource Pruning: To prevent storage and memory exhaustion from “zombie” containers or
orphanedimages—frequentsideeffectsofinterruptedagentscripts—weimplementedanautomatedcleanup
daemonthataggressivelyprunesunusedDockerresources.
• ObservabilityandMonitoring: WedeployedamonitoringstackbasedonPrometheusandGrafanatotrack
performance metrics and task progress in real-time, allowing for rapid diagnosis of hardware or pipeline
anomalies.
Thehardwareandsoftwarespecificationsforeachofthe64computenodesarestandardizedinTable1. Through
empirical experiments in a small scale, we identified this per-node specification as a near-optimal operating
point: it provides sufficient per-task throughput while avoiding the diminishing returns observed with further
resource scaling. With this 64-node cluster, we completed the construction of 45,320 validated environments
in approximately two weeks, reducing what would otherwise be a months-long process and making iterative
refinementofthesynthesispipelinepracticallyfeasible.
6
SII-GAIR
3.9 EnvironmentStatistics
Component Specification
HardwareConfiguration
CPU Intel(R)Xeon(R)6982P-C(32VirtualizedCores)
Memory 128GBRAM
Network 20GbpsIntranetBandwidth
Storage 4TBSSD
SoftwareConfiguration
OperatingSystem Ubuntu24.04LTS
ContainerEngine Docker29.1.3
Table1: HardwareandSoftwareSpecificationsforDistributedSynthesisNodes.
Dataset #Repos #images #Tasks Source
R2E-Gym(Subset)(Jainetal.,2025) 10 2.4k 4.6k Synthetic
SWE-gym(Panetal.,2024) 11 2.4k 2.4k Real
SWE-rebench(Badertdinovetal.,2025) 3.5k 21.3k 21.3k Real
SWE-rebench(filtered) 3.3k 18.8k 18.8k Real
SWE-rebench-v2(Badertdinovetal.,2026) 2.7k 32.7k 32.7k Real
SWE-rebench-v2(Python) 573 7.2k 7.2k Real
Scale-SWE(Zhaoetal.,2026) 5.2k 100k 100k Real
Scale-SWE(open-sourced) 1.2k 20.2k 20.2k Real
OpenSWE(ours) 12.8k 45.3k 45.3k Real
Table2: ComparisonofSWEtrainingenvironment. SWE-rebenchisfilteredbecausesomeenvironmentsfailto
executethegoldpatchunderourinfrastructure.
3.9 EnvironmentStatistics
Table2comparesOpenSWEagainstexistingSWEtrainingdatasetsintermsofscaleandexecutability. Wefiltered
allinstancesthathavebeencreatedinSWE-rebenchandSWE-BenchVerified. OpenSWEprovidesthelargest
numberofexecutablerepositoriesandtasksamongalldatasets,covering12.8kreposand45.3ktasks.
3.10 Training
TrainingDataCollection Toconstructourtrainingdata,weusedtheGLM-4.7modeltosamplethetrajectory
fromtheentireOpenSWEandSWE-rebench(filtered)datasetsfourtimesundertheOpenHandsorSWE-Agent
(temperature1.0,200kcontext,and300steps). Wethencollectedalltrajectoriesthatwerecorrectinoneortwo
of the four attempts under the same instance. To ensure training quality, we masked any steps that contained
formattingerrorsorothermistakes,leadingtoanerrorobservation. Wealsoremovealldatathatcontains’gitpull’
inthebashactiontoavoidrewardhacking.
SFTTraining Wemodifiedtheslimecode3tosupportmultiturntrainingwithcorrectactionmasking. Allmodels
aretrainedwithamaxtokenof128k,5epochs,batchsize128,andalearningratefrom1e-5to1e-6withcosine
annealing. WeuseQwen2.5-32B-BaseandQwen2.5-72B-Baseasourbasemodels.
4 Experiments
4.1 ExperimentalSetup
WeevaluateourmodelonSWE-BenchVerifiedusingOpenHandsorSWE-Agent(temperature0.7,128kcontext,
and300steps)andreportPass@1,averagedacross2runs.
4.2 MainResults
Table3presentsthecomparisonofOpenSWEwithrepresentativeonSWE-BenchVerified.
State-of-the-ArtatBothScales OpenSWE-32Bachievesaresolutionrateof62.4%,surpassingallmethodson
Qwen2.5series. ComparedtothestrongestQwen2.5-Coder-32BbaselineSWE-Master-32BandSWE-Master-
32B-RL.OpenSWE-32Bimprovesby4.6%whileusinganon-Coderbasemodel,demonstratingthathigh-quality
environmentdatacancompensatefordomain-specificpretraining. Atthe72Bscale,OpenSWE-72Breaches66.0%,
outperformingdaVinci-Dev-72Bby7.5%. Boththe32Bresultand72BresultprovetheeffectivenessofOpenSWE.
3https://github.com/THUDM/slime
7
SII-GAIR
4.3 DataScalingAnalysis
Model Backbone Scaffold Score
Qwen2.532BCoderSeries
R2EGym-Agent(Jainetal.,2025) Qwen2.5-32B-Coder-Base R2E-Gym 34.4
Openhands-LM(Wangetal.,2025b) Qwen2.5-Coder-32B-Inst. OpenHands 37.2
SWE-Agent-LM(Yangetal.,2025a) Qwen2.5-Coder-32B-Inst. SWE-Agent 40.2
SWE-Mirror-LM(Wangetal.,2025a) Qwen2.5-Coder-32B-Inst. MOpenHands 52.2
Skywork-SWE(Zengetal.,2025) Qwen2.5-Coder-32B-Inst. OpenHands 38.0
SWE-Compressor(Liuetal.,2025b) Qwen2.5-32B-Base OpenHands 57.6
SWE-Master-32B(Songetal.,2026) Qwen2.5-Coder-32B-Inst. R2E-Gym 57.8
SWE-Master-32B-RL(Songetal.,2026) Qwen2.5-Coder-32B-Inst. R2E-Gym 61.4
Qwen330B-A3BSeries
Qwen3-30B-A3B-Instruct(Zhaoetal.,2026) Qwen3-30B-A3B-Instruct OpenHands 22.0
Scale-SWE(Zhaoetal.,2026) Qwen3-30B-A3B-Instruct OpenHands 64.0
Qwen332BSeries
FrogBoss(Sonwaneetal.,2025) Qwen3-32B SWEAgent 54.6
SWE-Lego-Qwen3-32B(Taoetal.,2026) Qwen3-32B OpenHands 52.6
CoderForge-32B(Ariyaketal.,2026) Qwen3-32B OpenHands 59.4
Qwen2.532BSeries
daVinci-Dev-32B(Zengetal.,2026) Qwen2.5-32B-Base SWE-Agent 56.1
OpenSWE-32B(Ours) Qwen2.5-32B-Base OpenHands 59.8
OpenSWE-32B(Ours) Qwen2.5-32B-Base SWE-Agent 62.4
Qwen2.572BSeries
SWE-Fixer-72B(Xieetal.,2025) Qwen2.5-72B-Base Agentless 32.8
daVinci-Dev-72B(Zengetal.,2026) Qwen2.5-72B-Base SWE-Agent 58.5
Kimi-Dev(Yangetal.,2025b) Qwen2.5-72B-Base Agentless 60.6
OpenSWE-72B(Ours) Qwen2.5-72B-Base OpenHands 65.0
OpenSWE-72B(Ours) Qwen2.5-72B-Base SWE-Agent 66.0
Table3: ComparisonwithrepresentativemethodsonSWE-Bench Verified. Weincluderepresentativeworks
withagenticscaffolds.
ScalingwithModelCapacity OpenSWE-72BimprovesoverOpenSWE-32Bby3.6%. Incontrast,fordaVinci-
Dev, scaling from 32B to 72B yields only a 2.4% gain with the same scaffold, suggesting that higher-quality
trainingenvironmentsenablemodelstobetterleverageincreasedparameters.
Scaffold-AgnosticEffectiveness AsshowninTable3,OpenSWE-32Breaches59.8%withOpenHandsand
62.4% with SWE-Agent; OpenSWE-72B reaches 65.0% with OpenHands and 66.0% with SWE-Agent. This
indicatesthathigh-qualityenvironmentdatabenefitsmultiplescaffolddesignsratherthanbeingtiedtoaspecific
agentframework,enhancingthepracticalapplicabilityofourapproach.
4.3 DataScalingAnalysis
Toinvestigatetheeffectoftrainingdatascaleonagentperformance,weconstructsubsetsofvaryingsizesfromthe
fullOpenSWEtrainingsetandevaluatecheckpointsacrosstwomodelscales(Qwen2.5-32BandQwen2.5-72B)
andtwoagentscaffolds(SWE-AgentandOpenHands). Figure4presentstheresults.
Log-LinearScalingTrend Acrossallfourmodel–scaffoldconfigurations, Pass@1improvesapproximately
log-linearlywithtrainingsteps. Wefitalinearmodelinlog-stepspaceforeachcurveandobserveconsistently
high Pearson correlation coefficients: r=0.972 for 72B CodeAct, r=0.911 for 72B SWE-Agent, r=0.893 for
32BSWE-Agent,andr=0.882for32BCodeAct. Theuniformlyhighrvaluesacrossbothmodelsizesandboth
scaffoldssuggestthatthelog-linearscalingbehaviorisarobustpropertyofthetrainingdataratherthananartifact
ofaspecificarchitectureorevaluationprotocol.
LargerModelsBenefitMorefromScaling The72Bmodelsconsistentlyoutperformtheir32Bcounterparts
acrossalltrainingsteps.Moreover,thegapwidensastrainingprogresses:atearlycheckpoints,the72BSWE-Agent
leadsthe32BSWE-Agentbyapproximately3.1%,whileat∼484stepsthisgapgrowsto3.6%. Morenotably,for
theCodeActscaffold,the72Bmodelimprovesfroma5.2%leadatstep199toa5.2%leadatstep544,indicating
thatlargermodelsextractgreaterbenefitfromadditionaltrainingdata.
8
SII-GAIR
4.4 ImpactofEnvironmentSource
  
  
  
  
  
  
  
  
  
               
 7 U D L Q L Q J  6 W H S V   O R J  V F D O H 
  G H L I L U H 9  K F Q H %  ( : 6    # V V D 3
 2 S H Q 6 : (     %   6 : (  $ J H Q W  r       
 2 S H Q 6 : (     %   2 S H Q + D Q G V  r       
 2 S H Q 6 : (     %   6 : (  $ J H Q W  r       
 2 S H Q 6 : (     %   2 S H Q + D Q G V  r       
Figure4: DatascalingcurvesforOpenSWEacrossmodelsizesandagentscaffoldsinlog-linearmode. Filled
markerswithsolidfitlinesdenoteSWE-Agent;hollowmarkerswithdashedfitlinesdenoteOpenHands. Blue
indicates72Bmodels;redindicates32Bmodels.
SWE-Agent CodeAct
TrainingData 32B 72B 32B 72B
SWE-rebench 50.2% 63.4% 51.4% 62.4%
OpenSWE 62.4% 66.0% 59.8% 65.0%
SWE-rebench+OpenSWE 61.4% 68.0% 60.3% 65.5%
Table4: ImpactofenvironmentsourceonSWE-BenchVerifiedPass@1(%)acrossmodelsizesandscaffolds.
ScaffoldComparison SWE-AgentconsistentlyoutperformsOpenHandsacrossbothmodelscales. Forthe72B
model,SWE-Agentachieves66.0%atthefinalcheckpointcomparedtoOpenHands’s65.0%;forthe32Bmodel,
SWE-Agentreaches62.4%versusOpenHands’s59.8%. This1–3%marginsuggeststhattheSWE-Agentscaffold’s
designprovidesaconsistentadvantage,thoughbothscaffoldsbenefitsimilarlyfromdatascaling.
NoSaturationObserved Importantly,noneofthefourcurvesshowsignsofsaturationwithinourcurrentbudget.
ThecontinuedupwardtrendatthelargesttrainingstepcountssuggeststhatfurtherscalingtheOpenSWEtraining
setwouldyieldadditionalperformancegains,motivatingfutureworkonevenlarger-scaleenvironmentsynthesis.
4.4 ImpactofEnvironmentSource
Tounderstandhowthechoiceofenvironmentaffectsdownstreamagentperformance,wetrainidenticalmodelson
environmentsfromdifferentsourcesandevaluateunderthesameprotocol. Table4reportstheresults.
OpenSWEEnvironmentsAreSubstantiallyMoreEffective TrainingonOpenSWEaloneyieldslargeim-
provements over SWE-Rebench across all four configurations. The most pronounced gain appears at the 32B
SWE-Agentsetting,whereOpenSWEoutperformsSWE-Rebenchby12.2%absolute(62.4%vs.50.2%). Evenfor
the72BCodeActconfigurationwhereSWE-Rebenchismostcompetitive,OpenSWEstillleadsby2.6%(65.0%
vs.62.4%). ThisdemonstratesthatthequalityanddiversityofOpenSWE’ssynthesizedenvironmentsprovidea
strongertrainingsignalthanSWE-Rebench.
ComplementaryValueofMixingSources CombiningSWE-RebenchwithOpenSWEyieldsfurthergainsfor
72Bmodels: the72BSWE-Agentconfigurationreaches68.0%,a2.0%improvementoverOpenSWEaloneandthe
bestresultacrossallsettings. ThissuggeststhatSWE-Rebenchintroducescomplementaryenvironmentpatterns
thatbenefitlargermodels. However,for32Bmodels,mixingslightlydegradesperformanceonSWE-Agent(61.4%
vs.62.4%),indicatingthatsmallermodelsmaybemoresensitivetodistributionshiftsintroducedbyheterogeneous
datasources.
RobustnessAcrossScaffolds TherelativeorderingofenvironmentsourcesisconsistentacrossbothSWE-Agent
andCodeActscaffolds: OpenSWEconsistentlyoutperformsSWE-Rebench,andmixingprovidesadditionalgains
primarilyforlargermodels. Thisscaffold-agnosticpatternreinforcesthattheperformancedifferencesstemfrom
thequalityofthetrainingenvironmentsratherthanscaffold-specificinteractions.
9
SII-GAIR
4.5 GeneralCapabilityEvaluation
4.5 GeneralCapabilityEvaluation
Qwen2.5-32B Qwen2.5-72B
Benchmark Base OpenSWE ∆ Base OpenSWE ∆
CodeBenchmarks
HumanEval(Chenetal.,2021) 61.43 90.52 +29.09 66.82 76.25 +9.43
HumanEval+(Liuetal.,2023) 54.01 85.24 +31.23 59.23 70.75 +11.52
Math&ReasoningBenchmarks
GSM8K(Cobbeetal.,2021) 80.82 86.96 +6.14 83.17 89.16 +5.99
MATH-500(Hendrycksetal.,2021b) 58.00 66.20 +8.20 60.40 72.60 +12.20
ScienceBenchmarks
SuperGPQA(Teametal.,2025b) 33.85 39.62 +5.77 37.76 45.86 +8.10
SciBench(Wangetal.,2024a) 18.50 23.30 +4.80 20.30 25.00 +4.70
GeneralCapabilityBenchmarks
MMLU(Hendrycksetal.,2021a) 83.57 83.57 +0.00 86.37 87.37 +1.00
MMLU-Pro(Wangetal.,2024b) 61.60 67.40 +5.80 63.80 72.70 +8.90
TriviaQA(Joshietal.,2017) 59.06 60.47 +1.41 74.29 77.14 +2.85
Table5: GeneralcapabilitybenchmarkscomparingbaseandOpenSWE.∆denotesabsoluteimprovement.
ToassesswhetherSWE-focusedtrainingaffectsbroadermodelcapabilities, weevaluateOpenSWEmodels
againsttheirbasecounterpartsonasuiteofgeneralbenchmarksspanningcodegeneration,mathematicalreasoning,
scientificknowledge,andgenerallanguageunderstanding. ResultsarereportedinTable5.
Thelargestgainsappearoncodebenchmarks,wherethe32Bmodelimprovesbyover29pointsonHumanEval
andHumanEval+;becauseSWEtasksinherentlyrequirereading,editing,andgeneratingcode,thisdirectskill
overlapyieldsthestrongesttransfer. Consistentimprovementsacrossallthreemathbenchmarkssuggestthatthe
multi-stepplanningandlogicaldecompositioncultivatedbySWEdebugginggeneralizetomathematicalreasoning,
evenwithoutexplicitmathtrainingdata. SuperGPQAandSciBenchshowmoderategains,likelybecausescientific
questions demand structured inference chains similar to those practiced during patch generation, though the
domaingaplimitsthemagnitude. Incontrast,MMLUremainsnearlyflatandTriviaQAimprovesonlymarginally,
confirmingthatSWEtrainingenhancesproceduralproblem-solvingcapacitywithoutaffectingfactualrecall,which
dependsonpre-trainingcoverageratherthanreasoningability.
5 Conclusion
We presented OpenSWE, the largest fully transparent framework for SWE agent training, comprising 45,320
executableDockerenvironmentsacross12.8krepositorieswithallinfrastructureopen-sourced. Throughamulti-
agentsynthesispipelinedeployedona64-nodeclusterandaquality-centricfilteringprocessaddressingPR-Issue
misalignmentandtriviality,wecuratedapproximately10,000high-qualityenvironmentsthatprovideastronger
trainingsignalthanexistingalternatives.
ExtensiveexperimentsvalidatetheeffectivenessofOpenSWE:OpenSWE-32BandOpenSWE-72Bachieve
62.4%and66.0%onSWE-benchVerified,establishingstate-of-the-artamongSFT-basedmethods. Modelstrained
onOpenSWEconsistentlyoutperformthosetrainedonSWE-rebenchacrossallmodelsizesandscaffolds,exhibita
log-lineardatascalingtrendwithnoobservedsaturation,andshowimprovedgeneralcapabilitiesincodegeneration,
mathematicalreasoning,andscientificknowledgewithoutdegradingfactualrecall.
References
[1] Alpay Ariyak, Junda Zhang, Junxiong Wang, Shang Zhu, Federico Bianchi, Sanjana Srivastava, Ashwinee
Panda,SiddhantBharti,ChenfengXu,JohnHeo,XiaoxiaShirleyWu,JamesZou,PercyLiang,LeonSong,
CeZhang,BenAthiwaratkun,ZhongzhuZhou,andQingyangWu.2026. Coderforge-preview: Sotaopendataset
fortrainingefficientagents. Projectcoreleads: AlpayAriyak;ZhongzhuZhou;QingyangWu.
[2] Ibragim Badertdinov, Alexander Golubev, Maksim Nekrashevich, Anton Shevtsov, Simon Karasik, Andrei
Andriushchenko,MariaTrofimova,DariaLitvintseva,andBorisYangel.2025. Swe-rebench: Anautomated
pipelinefortaskcollectionanddecontaminatedevaluationofsoftwareengineeringagents.
[3] IbragimBadertdinov,MaksimNekrashevich,AntonShevtsov,andAlexanderGolubev.2026. SWE-rebenchV2:
Language-AgnosticSWETaskCollectionatScale.
10
SII-GAIR
References
[4] GuoxinChen,FanzheMeng,JialeZhao,MinghaoLi,DaixuanCheng,HuatongSong,JieChen,YuzhiLin,Hui
Chen,XinZhao,RuihuaSong,ChangLiu,ChengChen,KaiJia,andJi-RongWen.2026a. Beyondswe: Can
currentcodeagentsurvivebeyondsingle-repobugfixing?
[5] MarkChen,JerryTworek,HeewooJun,QimingYuan,HenriquePondedeOliveiraPinto,JaredKaplan,Harri
Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael
Petrov,HeidyKhlaaf,GirishSastry,PamelaMishkin,BrookeChan,ScottGray,NickRyder,MikhailPavlov,
AletheaPower,LukaszKaiser,MohammadBavarian,ClemensWinter,PhilippeTillet,FelipePetroskiSuch,
DaveCummings,MatthiasPlappert,FotiosChantzis,ElizabethBarnes,ArielHerbert-Voss,WilliamHebgen
Guss,AlexNichol,AlexPaino,NikolasTezak,JieTang,IgorBabuschkin,SuchirBalaji,ShantanuJain,William
Saunders,ChristopherHesse,AndrewN.Carr,JanLeike,JoshAchiam,VedantMisra,EvanMorikawa,Alec
Radford,MatthewKnight,MilesBrundage,MiraMurati,KatieMayer,PeterWelinder,BobMcGrew,Dario
Amodei,SamMcCandlish,IlyaSutskever,andWojciechZaremba.2021. Evaluatinglargelanguagemodels
trainedoncode.
[6] MouxiangChen,LeiZhang,YunlongFeng,XuwuWang,WentingZhao,RuishengCao,JiaxiYang,Jiawei
Chen,MingzeLi,ZeyaoMa,etal.2026b. Swe-universe: Scalereal-worldverifiableenvironmentstomillions.
arXivpreprintarXiv:2602.02361.
[7] KarlCobbe,VineetKosaraju,MohammadBavarian,MarkChen,HeewooJun,LukaszKaiser,MatthiasPlappert,
JerryTworek,JacobHilton,ReiichiroNakano,ChristopherHesse,andJohnSchulman.2021. Trainingverifiers
tosolvemathwordproblems.
[8] DayuanFu,KeqingHe,YejieWang,WentaoHong,ZhuomaGongque,WeihaoZeng,WeiWang,JingangWang,
XunliangCai,andWeiranXu.2025. Agentrefine: Enhancingagentgeneralizationthroughrefinementtuning.
arXivpreprintarXiv:2501.01702.
[9] LianghongGuo,YanlinWang,CaihuaLi,WeiTao,PengyuYang,JiachiChen,HaoyuSong,DuyuTang,and
Zibin Zheng. 2026. Swe-factory: Your automated factory for issue resolution training data and evaluation
benchmarks.
[10] DanHendrycks,CollinBurns,StevenBasart,AndyZou,MantasMazeika,DawnSong,andJacobSteinhardt.
2021a. Measuringmassivemultitasklanguageunderstanding.
[11] DanHendrycks,CollinBurns,SauravKadavath,AkulArora,StevenBasart,EricTang,DawnSong,andJacob
Steinhardt.2021b. Measuringmathematicalproblemsolvingwiththemathdataset. NeurIPS.
[12] Naman Jain, Jaskirat Singh, Manish Shetty, Liang Zheng, Koushik Sen, and Ion Stoica. 2025. R2e-gym:
Proceduralenvironmentsandhybridverifiersforscalingopen-weightssweagents.
[13] Mohan Jiang, Dayuan Fu, Junhao Shi, Ji Zeng, Weiye Si, Keyu Li, Xuefeng Li, Yang Xiao, Wenjie Li,
DequanWang,etal.2026. davinci-agency: Unlockinglong-horizonagencydata-efficiently. arXivpreprint
arXiv:2602.02619.
[14] CarlosEJimenez,JohnYang,AlexanderWettig,ShunyuYao,KexinPei,OfirPress,andKarthikNarasimhan.
2023. Swe-bench: Canlanguagemodelsresolvereal-worldgithubissues? arXivpreprintarXiv:2310.06770.
[15] MandarJoshi,EunsolChoi,DanielS.Weld,andLukeZettlemoyer.2017. Triviaqa: Alargescaledistantly
supervisedchallengedatasetforreadingcomprehension.
[16] AixinLiu,AoxueMei,BangcaiLin,BingXue,BingxuanWang,BingzhengXu,BochaoWu,BoweiZhang,
ChaofanLin,ChenDong,etal.2025a. Deepseek-v3.2: Pushingthefrontierofopenlargelanguagemodels.
arXivpreprintarXiv:2512.02556.
[17] JiaweiLiu,ChunqiuStevenXia,YuyaoWang,andLingmingZhang.2023. IsyourcodegeneratedbychatGPT
reallycorrect? rigorousevaluationoflargelanguagemodelsforcodegeneration. InThirty-seventhConference
onNeuralInformationProcessingSystems.
[18] ShukaiLiu,JianYang,BoJiang,YizhiLi,JinyangGuo,XianglongLiu,andBryanDai.2025b. Contextasa
tool: Contextmanagementforlong-horizonswe-agents.
[19] Jiayi Pan, Xingyao Wang, Graham Neubig, Navdeep Jaitly, Heng Ji, Alane Suhr, and Yizhe Zhang. 2024.
Trainingsoftwareengineeringagentsandverifierswithswe-gym. arXivpreprintarXiv:2412.21139.
[20] HuatongSong,LishengHuang,ShuangSun,JinhaoJiang,RanLe,DaixuanCheng,GuoxinChen,YiwenHu,
ZongchaoChen,WayneXinZhao,etal.2026. Swe-master: Unleashingthepotentialofsoftwareengineering
agentsviapost-training. arXivpreprintarXiv:2602.03411.
11
SII-GAIR
References
[21] AtharvSonwane,IsadoraWhite,HyunjiLee,MatheusPereira,LucasCaccia,MinseonKim,ZhengyanShi,
ChinmaySingh,AlessandroSordoni,Marc-AlexandreCoˆte´,andXingdiYuan.2025. Bugpilot: Complexbug
generationforefficientlearningofsweskills.
[22] ShuangSun,HuatongSong,LishengHuang,JinhaoJiang,RanLe,ZhihaoLv,ZongchaoChen,YiwenHu,
WenyangLuo,WayneXinZhao,etal.2026. Swe-world: Buildingsoftwareengineeringagentsindocker-free
environments. arXivpreprintarXiv:2602.03419.
[23] Chaofan Tao, Jierun Chen, Yuxin Jiang, Kaiqi Kou, Shaowei Wang, Ruoyu Wang, Xiaohui Li, Sidi Yang,
YimingDu,JianboDai,ZhimingMao,XinyuWang,LifengShang,andHaoliBai.2026. Swe-lego: Pushingthe
limitsofsupervisedfine-tuningforsoftwareissueresolving.
[24] KimiTeam,YifanBai,YipingBao,GuanduoChen,JiahaoChen,NingxinChen,RuijueChen,YanruChen,
YuankunChen,YutianChen,etal.2025a. Kimik2: Openagenticintelligence. arXivpreprintarXiv:2507.20534.
[25] PTeam,XinrunDu,YifanYao,KaijingMa,BingliWang,TianyuZheng,KingZhu,MinghaoLiu,Yiming
Liang,XiaolongJin,ZhenlinWei,ChujieZheng,KaixinDeng,ShawnGavin,ShianJia,SichaoJiang,Yiyan
Liao,RuiLi,QinruiLi,SirunLi,YizhiLi,YunwenLi,DavidMa,YuanshengNi,HaoranQue,QiyaoWang,
ZhoufutuWen,SiweiWu,TyshawnHsing,MingXu,ZhenzhuYang,ZekunMooreWang,JuntingZhou,Yuelin
Bai,XingyuanBu,ChenglinCai,LiangChen,YifanChen,ChengtuoCheng,TianhaoCheng,KeyiDing,Siming
Huang,YunHuang,YaoruLi,YizheLi,ZhaoqunLi,TianhaoLiang,ChengdongLin,HongquanLin,Yinghao
Ma,TianyangPang,ZhongyuanPeng,ZifanPeng,QigeQi,ShiQiu,XingweiQu,ShanghaoranQuan,Yizhou
Tan,ZiliWang,ChenqingWang,HaoWang,YiyaWang,YuboWang,JiajunXu,KexinYang,RuibinYuan,
YuanhaoYue,TianyangZhan,ChunZhang,JinyangZhang,XiyueZhang,XingjianZhang,YueZhang,Yongchi
Zhao,XiangyuZheng,ChenghuaZhong,YangGao,ZhoujunLi,DayihengLiu,QianLiu,TianyuLiu,Shiwen
Ni, Junran Peng, Yujia Qin, Wenbo Su, Guoyin Wang, Shi Wang, Jian Yang, Min Yang, Meng Cao, Xiang
Yue,ZhaoxiangZhang,WangchunshuZhou,JiahengLiu,QunshuLin,WenhaoHuang,andGeZhang.2025b.
Supergpqa: Scalingllmevaluationacross285graduatedisciplines.
[26] JunhaoWang,DaoguangZan,ShulinXin,SiyaoLiu,YurongWu,andKaiShen.2025a. Swe-mirror: Scaling
issue-resolvingdatasetsbymirroringissuesacrossrepositories.
[27] Xiaoxuan Wang, Ziniu Hu, Pan Lu, Yanqiao Zhu, Jieyu Zhang, Satyen Subramaniam, Arjun R. Loomba,
ShichangZhang,YizhouSun,andWeiWang.2024a. Scibench: Evaluatingcollege-levelscientificproblem-
solvingabilitiesoflargelanguagemodels.
[28] XingyaoWang,BoxuanLi,YufanSong,FrankF.Xu,XiangruTang,MingchenZhuge,JiayiPan,YueqiSong,
BowenLi,JaskiratSingh,HoangH.Tran,FuqiangLi,RenMa,MingzhangZheng,BillQian,YanjunShao,
NiklasMuennighoff,YizheZhang,BinyuanHui,JunyangLin,RobertBrennan,HaoPeng,HengJi,andGraham
Neubig.2025b. Openhands:AnopenplatformforAIsoftwaredevelopersasgeneralistagents. InTheThirteenth
InternationalConferenceonLearningRepresentations.
[29] YuboWang,XueguangMa,GeZhang,YuanshengNi,AbhranilChandra,ShiguangGuo,WeimingRen,Aaran
Arulraj,XuanHe,ZiyanJiang,TianleLi,MaxKu,KaiWang,AlexZhuang,RongqiFan,XiangYue,andWenhu
Chen.2024b. Mmlu-pro: Amorerobustandchallengingmulti-tasklanguageunderstandingbenchmark.
[30] Chunqiu Steven Xia, Yinlin Deng, Soren Dunn, and Lingming Zhang. 2024. Agentless: Demystifying
llm-basedsoftwareengineeringagents. arXivpreprintarXiv:2407.01489.
[31] Chengxing Xie, Bowen Li, Chang Gao, He Du, Wai Lam, Difan Zou, and Kai Chen. 2025. Swe-fixer:
Trainingopen-sourcellmsforeffectiveandefficientgithubissueresolution. InFindingsoftheAssociationfor
ComputationalLinguistics: ACL2025,pages1123–1139.
[32] JohnYang,CarlosEJimenez,AlexanderWettig,KilianLieret,ShunyuYao,KarthikNarasimhan,andOfir
Press.2024. Swe-agent: Agent-computerinterfacesenableautomatedsoftwareengineering. AdvancesinNeural
InformationProcessingSystems,37:50528–50652.
[33] JohnYang,KilianLieret,CarlosE.Jimenez,AlexanderWettig,KabirKhandpur,YanzheZhang,BinyuanHui,
OfirPress,LudwigSchmidt,andDiyiYang.2025a. Swe-smith: Scalingdataforsoftwareengineeringagents.
[34] ZonghanYang, ShengjieWang, KelinFu, WenyangHe, WeiminXiong, YiboLiu, YiboMiao, BofeiGao,
YejieWang,YingweiMa,YanhaoLi,YueLiu,ZhenxingHu,KaitaiZhang,ShuyiWang,HuarongChen,Flood
Sung,YangLiu,YangGao,ZhilinYang,andTianyuLiu.2025b. Kimi-dev: Agentlesstrainingasskillpriorfor
swe-agents.
[35] ShunyuYao,JeffreyZhao,DianYu,NanDu,IzhakShafran,KarthikNarasimhan,andYuanCao.2023. React:
Synergizingreasoningandactinginlanguagemodels. InInternationalConferenceonLearningRepresentations
(ICLR).
12
SII-GAIR
A.SWEEnvironmentBuilder: ArchitectureandPromptExcerpts
[36] JiZeng,DayuanFu,TiantianMi,YuminZhuang,YaxingHuang,XuefengLi,LyumanshanYe,MuhangXie,
QishuoHua,ZhenHuang,etal.2026. davinci-dev: Agent-nativemid-trainingforsoftwareengineering. arXiv
preprintarXiv:2601.18418.
[37] LiangZeng, YongcongLi, YuzhenXiao, ChangshiLi, ChrisYuhaoLiu, RuiYan, TianwenWei, JujieHe,
Xuchen Song, Yang Liu, and Yahui Zhou. 2025. Skywork-swe: Unveiling data scaling laws for software
engineeringinllms.
[38] JialeZhao,GuoxinChen,FanzheMeng,MinghaoLi,JieChen,HuiXu,YongshuaiSun,XinZhao,Ruihua
Song,YuanZhang,PengWang,ChengChen,JirongWen,andKaiJia.2026. Immersioninthegithubuniverse:
Scalingcodingagentstomastery.
Appendix
A SWEEnvironmentBuilder: ArchitectureandPromptExcerpts
ThisappendixdocumentsthedesignofthebuildersubsystemresponsibleforsynthesizingreproducibleDocker-
basedevaluationenvironments.
Goal. Givenataskinstance,whichconsistsofarepositorysnapshotatafixedbase-committogetherwiththe
patchinformationusedforevaluation,ourbuilderproducesaDockerfilethatbuildsanisolatedruntimeenvironment
andabashevaluationscriptthatrunstherelevanttestswhileemittingmachine-readablesignals.
Iterativeloop. Thebuilderfollowsaniterativeprocedure. Itfirstperformscontextretrievalbyinspectingthe
repositorytoinferdependencies,Pythonconstraints,andtestentrypoints. Itthensynthesizesorretrieves,when
available,aDockerfileandanevaluationscript.Thenitexecutesandvalidatestheresultingenvironmentbybuilding
theimage,runningtheevaluationscript,andextractingstructuredmarkersfromthelogs. Finally,itrefinesthe
artifactsbyprovidingconcisefailurediagnosesandrepeatingtheloop.
A.1 PromptDesign
Belowwequoteonlythepromptfragmentsthatmostdirectlyenforcetheengineeringinvariantsrequiredforstable,
large-scalesynthesis.
RepoExplorationAgent. Theretrievalpromptenforcesagoal-drivenandnon-exhaustivepolicy. Itdiscourages
broadrepositorycrawlingandinsteadrequiresashort,actionablereportthatrecordsexactversionsandconcrete
testcommands.
Repoexplorationsystempromptexcerpt(verbatim)
You are a context_retrieval_agent responsible for gathering **precise and
necessary information** from the local repository to support environment
setup and test execution. After gathering the information, you will
**generate a concise report** summarizing the key findings related to
the setup and test execution.
Sometimes, another agent (such as a test analysis agent) may explicitly
request specific information to help fix issues like Dockerfile errors or
evaluation script failures.
Your primary goal is to:
- **If a specific request is provided by a calling agent, focus your
retrieval narrowly on that request, extracting only the explicitly
required files or data.**
- **If no explicit request is given by another agent, or if the request
is incomplete or unclear, perform a basic and limited exploration of
the repository to collect general environment and test execution
information. Avoid exhaustive or in-depth searches.**
- **Pay special attention to the following information when collecting
and summarizing:**
- **Exact versions** of dependencies, libraries, and programming
languages (e.g., ‘flask==2.0.3‘, ‘python3.9‘, ‘node 18‘)
- **Commands** for setting up the environment and executing tests
(e.g., ‘pip install -r requirements.txt‘, ‘pytest tests/test_api.py‘)
- Any environment configuration details (e.g., ‘.env‘ files, specific
OS package dependencies, etc.)
- Specific test commands for individual or specific test files, not
just generic test execution commands.
### Suggested Retrieval Areas
Only investigate the following areas **if explicitly requested** by
the calling agent. Focus your retrieval on the minimal set of files
or configurations needed to resolve the issue efficiently and accurately.
13
SII-GAIR
A.1 PromptDesign
1. **Environment Setup Information**
- **Exact dependencies and their versions**: This includes dependencies
listed in files like ‘requirements.txt‘, ‘pyproject.toml‘, etc.
Ensure that the exact version for each dependency is captured.
- **Programming language versions**: Ensure to capture version
information like Python (e.g., ‘python3.9‘), and others as specified
in relevant configuration files (‘.python-version‘, etc.)
- **Environment configuration files**: Collect details from ‘.env‘,
‘.bashrc‘, or ‘.zshrc‘ if applicable, focusing on version-dependent
environment variables and paths.
- **OS-specific requirements**: Note any OS-dependent configurations
(e.g., specific Linux package dependencies in ‘apt‘ or ‘yum‘).
2. **Test Execution Information**
- **Precise test commands**: Focus on specific commands or instructions
for running individual tests or specific test files, not just commands
for running all tests. Look for test commands in documentation like
‘README.md‘, ‘CONTRIBUTING.md‘, ‘tests/README.md‘, etc.
- **CI/CD configurations**: Look into files like ‘.github/workflows/‘,
‘.ci.yml‘, ‘travis.yml‘, or other pipeline configuration files that
might include commands for running tests or specific test environments.
- **Test execution in context**: Extract any specific instructions about
running tests, such as flags for specific test cases, test suites,
or environments. Also, pay attention to dependencies relevant to
testing like test frameworks (e.g., ‘pytest‘, ‘JUnit‘, ‘Mocha‘),
env frameworks (e.g. poetry, uv), and their versions.
3. **Organize Results for other agents**
- Present findings in a structured way so they can be used to generate
the Dockerfile and evaluation script accurately. The **final report**
should:
- Highlight the **specific versions** of dependencies, libraries, and
testing tools.
- Include **commands** for setup and testing (e.g., ‘pip install‘,
‘npm install‘, ‘pytest‘).
- Note any environment variables or configuration details relevant
to the environment setup and test execution.
- Provide clear, concise, and actionable information, making it easier
for other agents to proceed with resolving any setup or test execution
issues.
### Important Notes:
- The repository has already been **cloned locally**; you are working
within the local repository directory.
- You are **not expected to search broadly**; retrieve only the files
and information explicitly requested by the calling agent.
- Avoid redundant or speculative searches|**be goal-driven and
cost-efficient**.
DockerfileAgent. TheDockerfilepromptencodeshardconstraintsthatpreventcommonfailuremodes,suchas
selectinganincorrectbaseimage,omittingcondaactivation,oraccidentallyrunningtestsduringimageconstruction.
TheseconstraintscomplementthearchitecturalchoicesdescribedinSection3.4bymakingthemnon-negotiable
duringgeneration.
Dockerfileinitpromptexcerpt(verbatim)
Generate a **Dockerfile** based on the collected environment setup information.
The Dockerfile must ensure that the provided test files can be executed
correctly.
### **Requirements:**
1. **Copy the repository** inside the Docker container into ‘/testbed/‘ and set
‘WORKDIR‘ to ‘/testbed/‘.
2. **Checkout a specific commit SHA**, which will be provided by the user.
3. **Set up the environment** based on the information from the context
retrieval agent:
- Install necessary system dependencies and programming language versions.
- Set up a virtual environment (‘testbed‘) if required.
- Install all necessary libraries and dependencies.
4. **Ensure test execution** by setting up all necessary configurations.
### Important Notes:
1. You are FORBIDDEN to run tests in the dockerfile, tests will be run using
eval script.
2. When building the Dockerfile, you MUST prioritize using package managers such
as APT, Maven, or NPM etc to set up the environment efficiently.
3. Ensure shell compatibility by using ‘/bin/bash‘ as the default shell
environment to avoid runtime issues.
4. Instead of using Ubuntu/Debian Docker image, You **MUST** directly use our
provided ‘openswe-python-version‘ to setup python environment. It is built
14
SII-GAIR
A.1 PromptDesign
from
<dockerfile>
FROM continuumio/miniconda3:25.3.1-1
RUN sed -i ’s|deb.debian.org|mirrors.cloud.aliyuncs.com|g’
/etc/apt/sources.list.d/debian.sources && \\
apt update && \\
rm -rf /var/lib/apt/lists/*
RUN conda create -n testbed python={python_version} -y; \\
echo "conda activate testbed" >> ˜/.bashrc; \\
conda activate testbed; \\
pip config set global.index-url http://mirrors.cloud.aliyuncs.com/pypi/simple/; \\
pip config set global.trusted-host mirrors.cloud.aliyuncs.com; \\
</dockerfile>
- It provides conda on debian 12, a python env named ‘testbed‘ with given
version, and change mirror source.
- Available python versions include 2.7 and 3.5 to 3.14. Conda does not provide
other versions. Chose **best fit version** rather than minimal.
- If a different base image is really necessary, please also change mirror to
aliyun.
- It use a conda environment, so all python/pip related run must run with ‘bash
-lc‘ or ‘. /opt/conda/etc/profile.d/conda.sh && conda activate testbed‘
- If you are rewriting because of python version issue, you MUST NOT create new
conda env; instead change base image version.
- Simply ignore conda update / pip update warning, unless it is root cause of
error
5. It is recommended to use ‘COPY‘ to copy local files into the Docker
container, and use of well-known basic image (python, miniforge), to avoid
network stuff.
6. DO NOT run tests in the Dockerfile**.
- Do not include commands like ‘npm test‘, ‘pytest‘, or ‘mvn test‘, or ‘python
-m import xxx‘ in the Dockerfile.
- Tests will be executed separately, and running them during the Docker build
stage is an unnecessary overhead.
- You can skip tests during environment setup because this is not your job.
7. If there is a reference Dockerfile, use it as a guideline.
8. Do not use ENTRYPOINT.
9. When setting up dependencies for the target repository (e.g., ‘torch 3.33‘),
**DO NOT** install the package directly from external registries (e.g., PyPI,
NPM, Maven Central) using commands like ‘pip install <package>‘ (e.g., ‘pip
install torch‘).
Instead, **you can install the repository itself in development mode** (‘pip
install -e .‘ for Python, ‘npm link‘ for Node.js, or ‘mvn install‘ for Java) to
ensure that the local repository’s code is correctly referenced during
execution.
**Why is this important?**
- If you modify the repository’s source code but have already installed a
pre-built package from the registry, your system may load the installed package
instead of your local code, **leading to incorrect test results and making
debugging difficult**.
- Using development mode installation (‘pip install -e .‘, ‘npm link‘, ‘mvn
install‘) ensures that the system always references the latest local repository
code, preventing version mismatches and ensuring that modifications are properly
reflected in subsequent tests.
### **Example Format:**
The Dockerfile must be wrapped in ‘<dockerfile>‘ tags. Example:
<dockerfile>
# Base image specification. Defines the foundation OS and python version for the
container (Required)
FROM openswe-python-3.12
# Fetch source code. same as git clone {{task.repo_name}} && git reset --hard
{{task.commit}} but avoid network stuff; guarantee to ready
COPY repo /testbed
# set default workdir to testbed. (Required)
WORKDIR /testbed/
# The lines above should NEVER change (except python version), so as to reuse
layers.
# Install package and environment manager required by the repo. (Example)
ENV DEBIAN_FRONTEND=noninteractive
RUN apt install -qq -y g++
# Target Project setup. Configures it, and installs project-specific
dependencies (Example)
# Note for conda, ‘-lc‘ is required for env activate; multicommand can split by
‘;‘
RUN bash -lc ’pip install -r requirements.txt’ # install requirements from
context
RUN bash -lc ’pip install -e’ # install self; important for running test
RUN bash -lc ’pip install pytest "poetry>=1,<2"’ # special char need quote
</dockerfile>
Write Evaluation Script Agent. The evaluation-script prompt enforces a deterministic and judge-friendly
interface. Itrequiresnon-interactivepatchapplicationviaheredocplaceholdersandmandatesthattestexecution
15
SII-GAIR
A.1 PromptDesign
emitmachine-readablemarkerstosupportrule-basedextraction.
eval-scriptinitpromptexcerpt(verbatim)
Generate an **evaluation script** based on the collected environment setup and
test execution information.
The script must execute the provided test files inside the specified Docker
environment.
### **Requirements:**
1. **Activate the environment**: Ensure the correct environment (e.g., Conda,
venv) is activated before running the tests.
2. **Apply the patch**: The patch may need to be applied before running the
tests.
3. **Execute the given test files and unittests** using the correct command
found by the context retrieval agent.
### Important Notes:
1. You must **execute only the specified target test files and unittests**,
rather than running all tests in the repository.
- Running all tests can be highly time-consuming and unnecessary.
- Ensure that only the **required test files** are executed. You may refer to
golden patch, but please remain some already passed tests other than fixed in
golden patch.
2. **Optimize execution efficiency by combining multiple test commands into a
single command** whenever possible.
- Avoid running multiple separate test commands if they can be executed in one
batch.
- This reduces redundant initialization overhead and speeds up execution.
3. **Ensure that the output of the evaluation script is concise and
structured**, making it easier for the **test log analysis agent** to process.
- The test command **must output the names and pass/fail/skip status of each
target executed test file**.
- Avoid excessive debug information or unrelated output in eval script, but **do
not suppress key test execution details**.
- Avoid running all tests! **Just run the target unittests fixed by gold
patch**.
4. **Follow the structure of the reference evaluation script or eval script
skeleton whenever available.
- Use **a simple, minimalistic structure** similar to the reference eval script
to ensure clarity and maintainability.
- The script should be easy to modify and extend without unnecessary complexity.
5. **The actual test patch content is omitted here for brevity (marked with
[CONTENT OF TEST PATCH] placeholder).
- You must generate the complete git apply command structure, including the
heredoc syntax with delimiter (EOF_114329324912).
- The placeholder will be programmatically replaced with the actual patch content
during script execution.
- Example structure:
git apply -v - <<’EOF_114329324912’\n
[CONTENT OF TEST PATCH]\nEOF_114329324912
6. You MUST capture the exit code immediately after running the tests using
‘rc=$?‘, and then echo: ‘OPENSWE_EXIT_CODE=$rc‘. This ensures the judge can
determine whether the tests passed successfully. Also, you MUST NOT include ‘set
-e‘, which will truncate out error code.
7. You MUST print ">>>>> Start Test Output" exactly before test (pytest for
example), and ">>>>> End Test Output" after it, we will extract output with it
after run.
### **Example Format:**
The script must be wrapped in ‘<script>‘ tags. Example:
<script>
#!/bin/bash
# activate environment
. /opt/conda/etc/profile.d/conda.sh
conda activate testbed # already created by base image
cd /testbed
# Required: apply test patch to update target tests
git apply -v --allow-empty - <<’EOF_114329324912’
[CONTENT OF TEST PATCH]
EOF_114329324912
# Required: run target tests files instead of all tests!
echo ">>>>> Start Test Output"
pytest --no-header -rA --tb=no -p no:cacheprovider -n4
mypy/test/testcheck.py::TypeCheckSuite::check-functions.test
16
SII-GAIR
A.1 PromptDesign
mypy/test/testcheck.py::TypeCheckSuite::check-redefine.test
rc=$? # Required, save exit code
echo ">>>>> End Test Output"
echo "OPENSWE_EXIT_CODE=$rc" #Required, echo test status
</script>
TestAnalysisAgent. Theanalysispromptturnsverboselogsintoactionableiterationsignalsbyenforcinga
rule-basedvaliditycriterion,underwhichthetest-onlyrunmustfailwhiletherunwiththefixmustpass. Italso
specifiesexplicitrouting:whenafailureisattributedtotheDockerfileratherthantheevaluationscript,thefeedback
isdirectedtothecorrespondingwriteragent.
Testanalysispromptexcerpt(verbatim)
Given the test log and the target tests, analyze the results and determine the
next steps. But if the dockerfile is not built successfully, you should analyze
what issues happen.
### **Step 1: Verify Test Execution**
- Identify which test files were added or modified by the eval script.
- Confirm that those tests were actually executed (they appear in the test log).
- Check their return code:
- Return code for testOnly MUST BE non-0 and for testWithFix MUST BE 0.
- Check their pass/fail status:
- If all tests switch from fail to pass, report success.
- If there exists fail to fail or pass to fail, report fail. (MUST fix by write
eval agent)
- If there exists pass to pass, and every other thing is correct, you may report
success.
- Ensure there is at least some test output in the log:
- If no test output is found, set ‘is_finish = false‘ and include an instruction
for write_eval_script_agent to revise the eval script so that tests actually
run.
### **Step 2: Identify Problems**
- If the tests failed due to **environment setup issues**, analyze whether the
problem comes from:
- The **Dockerfile** (e.g., incorrect dependencies, wrong OS, missing
configurations).
- The **evaluation script** (e.g., incorrect test commands, wrong paths, missing
environment activation, mismatch with unit tests solved by the gold patch).
- Simply ignore conda update / pip update warning, unless it is root cause of
error
- Sometimes, tests may fail due to incorrect versions of specific dependencies.
Be sure to check the versions of critical dependencies to ensure compatibility.
- If there are missing dependencies or unknown errors, consider whether
additional context retrieval is required.
- Tests should not be run in the Dockerfile**; skip tests during environment
setup and run them in the evaluation script.
- Note that the eval script MUST catch exit code after running tests, and echo
"OPENSWE_EXIT_CODE=$rc". This is important for judge whether tests are run
successfully.
### **Step 3: Plan Corrective Actions**
- If a fix is needed in the **Dockerfile**, provide guidance to
‘write_dockerfile_agent‘ on how to fix it, always include the original error
message and a brief description of what is missing or suspected to be the cause.
- If a fix is needed in the **evaluation script**, provide guidance to
‘write_eval_script_agent‘ on how to fix it, always include the original error
message and a brief description of what is missing or suspected to be the cause.
- If more information from the target repository is needed, provide guidance to
‘context_retrieval_agent‘ on what to collect. Here are some instructions:
1. Always include the original error message and a brief description of what is
missing or suspected to be the cause.
2. Clearly specify what information or files should be searched for. For
environment or dependency issues, recommend files such as requirements.txt,
environment.yml, Dockerfile, setup.py, pyproject.toml, etc. For test or
evaluation issues, suggest looking for files such as eval*.sh, pytest.ini,
.github/workflows/*, etc.
3. Additionally, encourage reviewing documentation files like README.md,
CONTRIBUTING.md, or any docs in the root or docs/ directory for relevant setup
or testing instructions (Contributing file often contains some testing
instruction).
4. Always add guidance to at least one of dockerfile agent or eval script agent
if you guide to context retrival agent, otherwise nothing is rewritten and
error will replay.
- If you encounter network issue, simply put all guidance empty and set
is_finish to false; we will rerun it.
- If you think the issue is unsolvable, you may simply set is_finish to true,
sparing effort; for example:
1. Golden patch does not solve any unittest.
2. Dependency of project has unsolvable conflicts
17
SII-GAIR
B.ConstructionCostEstimate
3. Some dependency have become missing, like 404 file, super old versions (numpy
<= 1.8)...
### **Output Example**
Provide your answer in JSON format:
‘‘‘json
{
"is_finish": true/false, # If tests passed and everything is correct or the
issue is considered unsolvable, set this to true.
"guidance_for_write_dockerfile_agent": "<Provide detailed guidance if
modifications are needed>",
"guidance_for_write_eval_script_agent": "<Provide detailed guidance if
modifications are needed>",
"guidance_for_context_retrieval_agent": "<Specify what additional information
from the target repository is needed, if any>",
}
‘‘‘
**Important Notes:**
- If ‘is_finish‘ is ‘true‘, all guidance fields can be empty.
- Be specific in your guidance, providing detailed steps for the necessary
fixes. Only provide guidance to the relevant agent based on the actual issue.
For any agent not called, its guidance field must be empty.
- Calling context_retrieval_agent is expensive. Only suggest using it when there
is clearly missing information that is necessary to fix the Dockerfile or
evaluation script. Be precise and specific in what to retrieve (e.g., particular
files or configuration scripts) to avoid repeated or vague searches.
- Provide detailed error information to tell agent what errors happen.
B ConstructionCostEstimate
Basedonthe64-nodeconfigurationinTable1,weprovideanapproximate10-dayconstructioncostestimatein
Table6. ThetotalconstructionbudgetisprimarilysensitivetoeffectiveGPU-hourpriceandclusterutilization
efficiency. Inpractice,preemptiblepricing,committed-usediscounts,andschedulingefficiencycansubstantially
changethefinalamount.
CurationCost. Beyondenvironmentconstruction,thetrajectorysamplinganddifficulty-awarecurationprocess
requiresanadditionalcomputationalinvestmentofapproximately$576,000. ThiscostprimarilycomprisesLLM
API expenses for generating resolution trajectories using the GLM-4.7 model across the full OpenSWE and
SWE-rebenchdatasets(fourattemptsperinstanceundertheOpenHandsandSWE-Agentscaffolds),aswellasthe
associatedDockercomputecostsforexecutingeachtrajectorywithinitscorrespondingenvironment. Combined
withtheenvironmentconstructionbudget,thetotalcostoftheOpenSWEprojectexceeds$1.47million.
CostItem EstimatedCost(USD) CostperInstance(USD)
Storage $13,000 $0.29
CPU $7,000 $0.15
Network $3,000 $0.07
ContainerRegistryService $3,000 $0.07
GPU $865,000 $19.08
Total $891,000 $19.66
Table6: Approximateconstructioncostfora64-node,10-dayrun.
18