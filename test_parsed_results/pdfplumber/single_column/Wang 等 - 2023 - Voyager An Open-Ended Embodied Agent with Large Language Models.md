# Wang 等 - 2023 - Voyager An Open-Ended Embodied Agent with Large Language Models

VOYAGER: An Open-Ended Embodied Agent
with Large Language Models
GuanzhiWang12#,YuqiXie3,YunfanJiang4∗,AjayMandlekar1∗,
ChaoweiXiao15,YukeZhu13,Linxi“Jim”Fan1†#,AnimaAnandkumar12†
1NVIDIA,2Caltech,3UTAustin,4Stanford,5UWMadison
∗Equalcontribution †Equaladvising #Correspondingauthors
https://voyager.minedojo.org
Abstract
WeintroduceVOYAGER,thefirstLLM-poweredembodiedlifelonglearningagent
in Minecraft that continuously explores the world, acquires diverse skills, and
makesnoveldiscoverieswithouthumanintervention. VOYAGERconsistsofthree
keycomponents: 1)anautomaticcurriculumthatmaximizesexploration,2)an
ever-growingskilllibraryofexecutablecodeforstoringandretrievingcomplex
behaviors,and3)anewiterativepromptingmechanismthatincorporatesenviron-
mentfeedback,executionerrors,andself-verificationforprogramimprovement.
VOYAGERinteractswithGPT-4viablackboxqueries,whichbypassestheneedfor
modelparameterfine-tuning. TheskillsdevelopedbyVOYAGERaretemporally
extended,interpretable,andcompositional,whichcompoundstheagent’sabilities
rapidly and alleviates catastrophic forgetting. Empirically, VOYAGER shows
strongin-contextlifelonglearningcapabilityandexhibitsexceptionalproficiency
in playing Minecraft. It obtains 3.3× more unique items, travels 2.3× longer
distances,andunlockskeytechtreemilestonesupto15.3×fasterthanpriorSOTA.
VOYAGERisabletoutilizethelearnedskilllibraryinanewMinecraftworldto
solvenoveltasksfromscratch,whileothertechniquesstruggletogeneralize.
Figure1: VOYAGERdiscoversnewMinecraftitemsandskillscontinuallybyself-drivenexploration,
significantlyoutperformingthebaselines. X-axisdenotesthenumberofpromptingiterations.
1
3202
tcO
91
]IA.sc[
2v19261.5032:viXra
Automatic Curriculum Iterative Prompting Mechanism Skill Library
Mine Wood Log
Make Crafting Table
Make Crafting Table Craft Stone Sword
New Skill Make Furnace
Combat Task Retrieval
Craft Shield
Zombie
Cook Steak
Mine Wood Log Combat Zombie
Env Feedback
Code as Refine Program
Execution Errors Actions
Mine Diamond Update Add New Skill
Exploration
Progress
Environment Self-Verification
Figure 2: VOYAGER consists of three key components: an automatic curriculum for open-ended
exploration,askilllibraryforincreasinglycomplexbehaviors,andaniterativepromptingmechanism
thatusescodeasactionspace.
1 Introduction
Buildinggenerallycapableembodiedagentsthatcontinuouslyexplore,plan,anddevelopnewskills
in open-ended worlds is a grand challenge for the AI community [1–5]. Classical approaches
employreinforcementlearning(RL)[6,7]andimitationlearning[8–10]thatoperateonprimitive
actions,whichcouldbechallengingforsystematicexploration[11–15],interpretability[16–18],and
generalization[19–21]. Recentadvancesinlargelanguagemodel(LLM)basedagentsharnessthe
worldknowledgeencapsulatedinpre-trainedLLMstogenerateconsistentactionplansorexecutable
policies[16,22,19]. Theyareappliedtoembodiedtaskslikegamesandrobotics[23–27],aswellas
NLPtaskswithoutembodiment[28–30]. However,theseagentsarenotlifelonglearnersthatcan
progressivelyacquire,update,accumulate,andtransferknowledgeoverextendedtimespans[31,32].
Let us consider Minecraft as an example. Unlike most other games studied in AI [33, 34, 10],
Minecraftdoesnotimposeapredefinedendgoalorafixedstorylinebutratherprovidesaunique
playgroundwithendlesspossibilities[23]. Minecraftrequiresplayerstoexplorevast,procedurally
generated3Dterrainsandunlockatechtreeusinggatheredresources. Humanplayerstypicallystart
bylearningthebasics,suchasminingwoodandcookingfood,beforeadvancingtomorecomplex
taskslikecombatingmonstersandcraftingdiamondtools.Wearguethataneffectivelifelonglearning
agentshouldhavesimilarcapabilitiesashumanplayers: (1)proposesuitabletasksbasedonits
currentskilllevelandworldstate,e.g.,learntoharvestsandandcactusbeforeironifitfindsitselfin
adesertratherthanaforest;(2)refineskillsbasedonenvironmentalfeedbackandcommitmastered
skillstomemoryforfuturereuseinsimilarsituations(e.g. fightingzombiesissimilartofighting
spiders);(3)continuallyexploretheworldandseekoutnewtasksinaself-drivenmanner.
Towardsthesegoals,weintroduce VOYAGER,thefirstLLM-poweredembodiedlifelonglearning
agent to drive exploration, master a wide range of skills, and make new discoveries continually
withouthumaninterventioninMinecraft. VOYAGERismadepossiblethroughthreekeymodules
(Fig. 2): 1) an automatic curriculum that maximizes exploration; 2) a skill library for storing
andretrievingcomplexbehaviors; and3)anewiterativepromptingmechanismthatgenerates
executablecodeforembodiedcontrol. Weopttousecodeastheactionspaceinsteadoflow-level
motorcommandsbecauseprogramscannaturallyrepresenttemporallyextendedandcompositional
actions[16,22],whichareessentialformanylong-horizontasksinMinecraft. VOYAGERinteracts
withablackboxLLM(GPT-4[35])throughpromptingandin-contextlearning[36–38].Ourapproach
bypassestheneedformodelparameteraccessandexplicitgradient-basedtrainingorfinetuning.
Morespecifically,VOYAGERattemptstosolveprogressivelyhardertasksproposedbytheautomatic
curriculum,whichtakesintoaccounttheexplorationprogressandtheagent’sstate. Thecurriculum
is generated by GPT-4 based on the overarching goal of “discovering as many diverse things as
possible”.Thisapproachcanbeperceivedasanin-contextformofnoveltysearch[39,40]. VOYAGER
incrementallybuildsaskilllibrarybystoringtheactionprogramsthathelpsolveatasksuccessfully.
2
Inventory (5/36): {'oak_planks': 3, 'stick': Reasoning: Since you have a wooden pickaxe and some stones, it would be
4, 'crafting_table': 1, 'stone': 3, GPT-4 beneficial to upgrade your pickaxe to a stone pickaxe for better efficiency.
'wooden_pickaxe': 1} Task: Craft 1 stone pickaxe.
Biome: river
Reasoning: Since you have a fishing rod in your inventory and you are near a river
Inventory (4/36): {'sugar_cane': 3, 'paper': GPT-4 biome, it would be a good opportunity to catch some fish for food and experience.
3, 'fishing_rod': 1, 'wooden_pickaxe': 1} Task: Catch 1 fish.
Nearby entities: pig, cat, villager Reasoning: Your hunger is at 0, which means you need to find food to replenish
Health: 12/20 GPT-4 your hunger. Since there are pigs nearby, you can kill one to obtain raw porkchops.
Hunger: 0/20 Task: Kill 1 pig.
Inventory (6/36): {'furnace': 1, Reasoning: You have raw iron and coal, and you have a furnace. It's time to smelt
'stone_pickaxe': 1, 'oak_planks': 7, GPT-4 the iron to make iron ingots, which can be used to craft better tools and armor.
'crafting_table': 1, 'raw_iron': 4, 'coal': 1} Task: Smelt 4 raw iron.
Time: night
Reasoning: Since it's night and there's a zombie nearby, it's a good opportunity to
Nearby entities: zombie
GPT-4 try killing the zombie now that you have a stone sword and a shield equipped.
Equipment: 'stone_sword', 'shield' Task: Kill 1 zombie.
Figure3: Tasksproposedbytheautomaticcurriculum. Weonlydisplaythepartialpromptforbrevity.
SeeAppendix,Sec.A.3forthefullpromptstructure.
Each program is indexed by the embedding of its description, which can be retrieved in similar
situationsinthefuture. Complexskillscanbesynthesizedbycomposingsimplerprograms,which
compoundsVOYAGER’scapabilitiesrapidlyovertimeandalleviatescatastrophicforgettinginother
continuallearningmethods[31,32].
However,LLMsstruggletoproducethecorrectactioncodeconsistentlyinoneshot[41]. Toaddress
this challenge, we propose an iterative prompting mechanism that: (1) executes the generated
programtoobtainobservationsfromtheMinecraftsimulation(suchasinventorylistingandnearby
creatures)anderrortracefromthecodeinterpreter(ifany);(2)incorporatesthefeedbackintoGPT-4’s
promptforanotherroundofcoderefinement; and(3)repeatstheprocessuntilaself-verification
moduleconfirmsthetaskcompletion,atwhichpointwecommittheprogramtotheskilllibrary(e.g.,
craftStoneShovel()andcombatZombieWithSword())andquerytheautomaticcurriculumfor
thenextmilestone(Fig.2).
Empirically,VOYAGERdemonstratesstrongin-contextlifelonglearningcapabilities.Itcanconstruct
anever-growingskilllibraryofactionprogramsthatarereusable,interpretable,andgeneralizable
tonoveltasks. Weevaluate VOYAGER systematicallyagainstotherLLM-basedagenttechniques
(e.g.,ReAct[29],Reflexion[30],AutoGPT[28])inMineDojo[23],anopen-sourceMinecraftAI
framework. VOYAGERoutperformspriorSOTAbyobtaining3.3×moreuniqueitems,unlockingkey
techtreemilestonesupto15.3×faster,andtraversing2.3×longerdistances. Wefurtherdemonstrate
thatVOYAGERisabletoutilizethelearnedskilllibraryinanewMinecraftworldtosolvenoveltasks
fromscratch,whileothermethodsstruggletogeneralize.
2 Method
VOYAGERconsistsofthreenovelcomponents: (1)anautomaticcurriculum(Sec.2.1)thatsuggests
objectives for open-ended exploration, (2) a skill library (Sec. 2.2) for developing increasingly
complexbehaviors,and(3)aniterativepromptingmechanism(Sec.2.3)thatgeneratesexecutable
codeforembodiedcontrol. FullpromptsarepresentedinAppendix,Sec.A.
2.1 AutomaticCurriculum
Embodiedagentsencounteravarietyofobjectiveswithdifferentcomplexitylevelsinopen-ended
environments. Anautomaticcurriculumoffersnumerousbenefitsforopen-endedexploration,ensur-
ingachallengingbutmanageablelearningprocess,fosteringcuriosity-drivenintrinsicmotivation
foragentstolearnandexplore,andencouragingthedevelopmentofgeneralandflexibleproblem-
solvingstrategies[42–44]. Ourautomaticcurriculumcapitalizesontheinternet-scaleknowledge
containedwithinGPT-4bypromptingittoprovideasteadystreamofnewtasksorchallenges. The
curriculumunfoldsinabottom-upfashion,allowingforconsiderableadaptabilityandresponsiveness
totheexplorationprogressandtheagent’scurrentstate(Fig.3). AsVOYAGERprogressestoharder
self-drivengoals,itnaturallylearnsavarietyofskills,suchas“miningadiamond”.
3
Program Generated by GPT-4 Program Description Skill Library
Mine Wood Log
Make Crafting Table
Craft Wooden Pickaxe
GPT-3.5 Embedding Key Craft Stone Sword
Make Furnace
Add ...
Combat Cow
Cook Steak
Value Craft Iron Axe
Combat Zombie
Task: Craft Iron Pickaxe Top-5 Relevant Skills
To craft an iron pickaxe, you Smelt Iron Ingot
H M o in w e c to ra c ft r ? aft an iron pickaxe in GPT-3.5 n s th t e i e c e k d m s t a . o t O e 3 n r i c i a r e o ls n y , o . i . n u ..
g h o a t v s e a n g d at 2 h ered Embedding Query Skill Library Retrieve C M r a a k f e t S C t r ic a k
fting Table
----------------------------------
Make Furnace
Environment Feedback Craft Wooden Pickaxe
Figure4: Skilllibrary. Top: Addinganewskill. EachtimeGPT-4generatesandverifiesanew
skill,weaddittotheskilllibrary,representedbyavectordatabase. Thekeyistheembeddingvector
oftheprogramdescription(generatedbyGPT-3.5),whilethevalueistheprogramitself. Bottom:
Skillretrieval. Whenfacedwithanewtaskproposedbytheautomaticcurriculum,wefirstleverage
GPT-3.5togenerateageneralsuggestionforsolvingthetask,whichiscombinedwithenvironment
feedbackasthequerycontext.Subsequently,weperformqueryingtoidentifythetop-5relevantskills.
TheinputprompttoGPT-4consistsofseveralcomponents:
(1) Directives encouraging diverse behaviors and imposing constraints, such as
“My ultimate goal is to discover as many diverse things as possible
... The next task should not be too hard since I may not have the
necessary resources or have learned enough skills to complete it
yet.”;
(2) The agent’s current state, including inventory, equipment, nearby blocks and entities,
biome,time,healthandhungerbars,andposition;
(3) Previouslycompletedandfailedtasks,reflectingtheagent’scurrentexplorationprogress
andcapabilitiesfrontier;
(4) Additionalcontext: WealsoleverageGPT-3.5toself-askquestionsbasedontheagent’s
currentstateandexplorationprogressandself-answerquestions. WeopttouseGPT-3.5
insteadofGPT-4forstandardNLPtasksduetobudgetaryconsiderations.
2.2 SkillLibrary
Withtheautomaticcurriculumconsistentlyproposingincreasinglycomplextasks,itisessentialto
haveaskilllibrarythatservesasabasisforlearningandevolution. Inspiredbythegenerality,inter-
pretability,anduniversalityofprograms[45],werepresenteachskillwithexecutablecodethatscaf-
foldstemporallyextendedactionsforcompletingaspecifictaskproposedbytheautomaticcurriculum.
TheinputprompttoGPT-4consistsofthefollowingcomponents:
(1) Guidelines for code generation, such as “Your function will be reused
for building more complex functions. Therefore, you should make
it generic and reusable.”;
(2) Control primitive APIs, and relevant skills retrieved from the skill library, which are
crucialforin-contextlearning[36–38]toworkwell;
(3) Thegeneratedcodefromthelastround,environmentfeedback,executionerrors,and
critique,basedonwhichGPT-4canself-improve(Sec.2.3);
(4) The agent’s current state, including inventory, equipment, nearby blocks and entities,
biome,time,healthandhungerbars,andposition;
4
Environment Feedback Execution Error
throw new Error(`No item named ${name}`);
I cannot make stick because I need: 2 more planks
No item named acacia_axe
I cannot make stone_shovel because I need: 2 more stick
at line 18:await craftItem(bot, "acacia_axe", 1);
GPT-4 GPT-4
Figure5: Left: Environmentfeedback. GPT-4realizesitneeds2moreplanksbeforecraftingsticks.
Right: Executionerror. GPT-4realizesitshouldcraftawoodenaxeinsteadofanacaciaaxesince
thereisnoacaciaaxeinMinecraft. Weonlydisplaythepartialpromptforbrevity. Thefullprompt
structureforcodegenerationisinAppendix,Sec.A.4.
(5) Chain-of-thoughtprompting[46]todoreasoningbeforecodegeneration.
We iteratively refine the program through a novel iterative prompting mechanism (Sec. 2.3), in-
corporate it into the skill library as a new skill, and index it by the embedding of its description
(Fig.4,top). Forskillretrieval,wequerytheskilllibrarywiththeembeddingofself-generatedtask
plansandenvironmentfeedback(Fig.4,bottom). Bycontinuouslyexpandingandrefiningtheskill
library,VOYAGERcanlearn,adapt,andexcelinawidespectrumoftasks,consistentlypushingthe
boundariesofitscapabilitiesintheopenworld.
2.3 IterativePromptingMechanism
Weintroduceaniterativepromptingmechanismforself-improvementthroughthreetypesoffeedback:
(1) Environmentfeedback,whichillustratestheintermediateprogressofprogramexecution
(Fig.5,left). Forexample,“I cannot make an iron chestplate because I need:
7 more iron ingots”highlightsthecauseoffailureincraftinganironchestplate.Weuse
bot.chat()insidecontrolprimitiveAPIstogenerateenvironmentfeedbackandprompt
GPT-4tousethisfunctionaswellduringcodegeneration;
(2) Executionerrorsfromtheprograminterpreterthatrevealanyinvalidoperationsorsyntax
errorsinprograms,whicharevaluableforbugfixing(Fig.5,right);
(3) Self-verificationforcheckingtasksuccess. Insteadofmanuallycodingsuccesscheckers
for each new task proposed by the automatic curriculum, we instantiate another GPT-4
agentforself-verification. ByprovidingVOYAGER’scurrentstateandthetasktoGPT-4,
weaskittoactasacritic[47–49]andinformuswhethertheprogramachievesthetask.
Inaddition,ifthetaskfails,itprovidesacritiquebysuggestinghowtocompletethetask
(Fig.6). Hence,ourself-verificationismorecomprehensivethanself-reflection[30]byboth
checkingsuccessandreflectingonmistakes.
Duringeachroundofcodegeneration, weexecutethegeneratedprogramtoobtainenvironment
feedbackandexecutionerrorsfromthecodeinterpreter,whichareincorporatedintoGPT-4’sprompt
forthenextroundofcoderefinement. Thisiterativeprocessrepeatsuntilself-verificationvalidates
5
Inventory (8/36): {'oak_planks': 5, 'cobblestone': 2,
Reasoning: Mining coal_ore in Minecraft will get coal. You have 5 coal in your
'porkchop': 2, 'wooden_sword': 1, 'coal': 5, 'wooden_pickaxe':
GPT-4 inventory.
1, 'oak_log': 3, 'dirt': 9}
Success: True
Task: Mine 5 coal ores
Inventory (10/36): {'raw_copper': 9, 'copper_ingot': 3, Reasoning: To craft a spyglass, you need 2 copper ingots and 1 amethyst shard.
'acacia_planks': 1, 'raw_iron': 1, 'stick': 1, 'iron_sword': 1, You have 3 copper ingots, but you don't have any amethyst shards.
GPT-4
'iron_pickaxe': 1, 'iron_ingot': 3, 'crafting_table': 1, 'furnace': 1}
Success: False
Task: Craft a spyglass Critique: Find and mine an amethyst shard underground.
Inventory (7/36): {'oak_log': 5, 'oak_planks': 1, Reasoning: You have 2 white_wool and 6 mutton in your inventory, which indicates
'wooden_pickaxe': 1, 'wooden_sword': 1, 'porkchop': 2, GPT-4 that you killed 2 sheep. You needed to kill 3 sheep.
'white_wool': 2, 'mutton': 6}
Success: False
Task: Kill 3 sheep Critique: Find and kill one more sheep to complete the task.
Inventory (9/36): {'string': 4, 'coal': 1, 'rotten_flesh': 1,
Reasoning: You have 1 rotten_flesh in your inventory, which means you have killed
'iron_sword': 1, 'furnace': 1, 'dirt': 6, 'stone_shovel': 1,
GPT-4 at least 1 zombie.
'wooden_pickaxe': 1, 'granite': 5}
Success: True
Task: Kill 1 zombie
Figure6: Self-verificationexamples. Weonlydisplaythepartialpromptforbrevity. SeeAppendix,
Sec.A.5forthefullpromptstructure.
thetask’scompletion,atwhichpointweaddthisnewskilltotheskilllibraryandasktheautomatic
curriculumforanewobjective(Fig.2). Iftheagentgetsstuckafter4roundsofcodegeneration,then
wequerythecurriculumforanothertask. Thisiterativepromptingapproachsignificantlyimproves
programsynthesisforembodiedcontrol,enablingVOYAGERtocontinuouslyacquirediverseskills
withouthumanintervention.
3 Experiments
3.1 ExperimentalSetup
WeleverageOpenAI’sgpt-4-0314[35]andgpt-3.5-turbo-0301[50]APIsfortextcompletion,
alongwithtext-embedding-ada-002[51]APIfortextembedding. Wesetalltemperaturesto
0exceptfortheautomaticcurriculum,whichusestemperature=0.1toencouragetaskdiversity. Our
simulationenvironmentisbuiltontopofMineDojo[23]andleveragesMineflayer[52]JavaScript
APIsformotorcontrols. SeeAppendix,Sec.B.1formoredetails.
3.2 Baselines
BecausethereisnoLLM-basedagentsthatworkoutoftheboxforMinecraft,wemakeourbest
efforttoselectanumberofrepresentativealgorithmsasbaselines. Thesemethodsareoriginally
designed only for NLP tasks without embodiment, therefore we have to re-interpret them to be
executableinMineDojoandcompatiblewithourexperimentalsetting:
ReAct[29]useschain-of-thoughtprompting[46]bygeneratingbothreasoningtracesandaction
planswithLLMs. Weprovideitwithourenvironmentfeedbackandtheagentstatesasobservations.
Reflexion[30]isbuiltontopofReAct[29]withself-reflectiontoinfermoreintuitivefutureactions.
Weprovideitwithexecutionerrorsandourself-verificationmodule.
AutoGPT[28]isapopularsoftwaretoolthatautomatesNLPtasksbydecomposingahigh-level
goalintomultiplesubgoalsandexecutingtheminaReAct-styleloop. Were-implementAutoGPT
byusingGPT-4todotaskdecompositionandprovideitwiththeagentstates,environmentfeedback,
andexecutionerrorsasobservationsforsubgoalexecution. ComparedwithVOYAGER,AutoGPT
lackstheskilllibraryforaccumulatingknowledge,self-verificationforassessingtasksuccess,and
automaticcurriculumforopen-endedexploration.
NotethatwedonotdirectlycomparewithpriormethodsthattakeMinecraftscreenpixelsasinput
andoutputlow-levelcontrols[53–55]. Itwouldnotbeanapple-to-applecomparison,becausewerely
onthehigh-levelMineflayer[52]APItocontroltheagent. Ourwork’sfocusisonpushingthelimits
ofGPT-4forlifelongembodiedagentlearning,ratherthansolvingthe3Dperceptionorsensorimotor
controlproblems. VOYAGERisorthogonalandcanbecombinedwithgradient-basedapproacheslike
6
Table1: Techtreemastery. Fractionsindicatethenumberofsuccessfultrialsoutofthreetotalruns.
0/3meansthemethodfailstounlockalevelofthetechtreewithinthemaximalpromptingiterations
(160). Numbersarepromptingiterationsaveragedoverthreetrials. Thefewertheiterations, the
moreefficientthemethod.
Method WoodenTool StoneTool IronTool DiamondTool
ReAct[29] N/A(0/3) N/A(0/3) N/A(0/3) N/A(0/3)
Reflexion[30] N/A(0/3) N/A(0/3) N/A(0/3) N/A(0/3)
AutoGPT[28] 92±72(3/3) 94±72(3/3) 135±103(3/3) N/A(0/3)
VOYAGERw/oSkillLibrary 7±2(3/3) 9±4(3/3) 29±11(3/3) N/A(0/3)
VOYAGER(Ours) 6±2(3/3) 11±2(3/3) 21±7(3/3) 102(1/3)
Figure7: Mapcoverage: bird’seyeviewsofMinecraftmaps. VOYAGER isabletotraverse2.3×
longerdistancescomparedtobaselineswhilecrossingdiverseterrains.
VPT[8]aslongasthecontrollerprovidesacodeAPI.Wemakeasystem-levelcomparisonbetween
VOYAGERandpriorMinecraftagentsinTable.A.2.
3.3 EvaluationResults
We systematically evaluate VOYAGER and baselines on their exploration performance, tech tree
mastery,mapcoverage,andzero-shotgeneralizationcapabilitytonoveltasksinanewworld.
Significantly better exploration. Results of exploration performance are shown in Fig. 1.
VOYAGER’s superiority is evident in its ability to consistently make new strides, discovering 63
uniqueitemswithin160promptingiterations,3.3×manynovelitemscomparedtoitscounterparts.
Ontheotherhand,AutoGPTlagsconsiderablyindiscoveringnewitems,whileReActandReflexion
struggletomakesignificantprogress,giventheabstractnatureoftheopen-endedexplorationgoal
thatischallengingtoexecutewithoutanappropriatecurriculum.
Consistenttechtreemastery. TheMinecrafttechtreeteststheagent’sabilitytocraftandusea
hierarchyoftools. Progressingthroughthistree(woodentool→stonetool→irontool→diamond
tool)requirestheagenttomastersystematicandcompositionalskills. Comparedwithbaselines,
VOYAGERunlocksthewoodenlevel15.3×faster(intermsofthepromptingiterations),thestone
level8.5×faster,theironlevel6.4×faster,andVOYAGERistheonlyonetounlockthediamondlevel
ofthetechtree(Fig.2andTable.1). Thisunderscorestheeffectivenessoftheautomaticcurriculum,
whichconsistentlypresentschallengesofsuitablecomplexitytofacilitatetheagent’sprogress.
Extensivemaptraversal. VOYAGERisabletonavigatedistances2.3×longercomparedtobaselines
bytraversingavarietyofterrains,whilethebaselineagentsoftenfindthemselvesconfinedtolocal
areas,whichsignificantlyhamperstheircapacitytodiscovernewknowledge(Fig.7).
7
Table 2: Zero-shot generalization to unseen tasks. Fractions indicate the number of successful
trialsoutofthreetotalattempts. 0/3meansthemethodfailstosolvethetaskwithinthemaximal
promptingiterations(50). Numbersarepromptingiterationsaveragedoverthreetrials. Thefewer
theiterations,themoreefficientthemethod.
Method DiamondPickaxe GoldenSword LavaBucket Compass
ReAct[29] N/A(0/3) N/A(0/3) N/A(0/3) N/A(0/3)
Reflexion[30] N/A(0/3) N/A(0/3) N/A(0/3) N/A(0/3)
AutoGPT[28] N/A(0/3) N/A(0/3) N/A(0/3) N/A(0/3)
AutoGPT[28]w/OurSkillLibrary 39(1/3) 30(1/3) N/A(0/3) 30(2/3)
VOYAGERw/oSkillLibrary 36(2/3) 30±9(3/3) 27±9(3/3) 26±3(3/3)
VOYAGER(Ours) 19±3(3/3) 18±7(3/3) 21±5(3/3) 18±2(3/3)
Figure8: Zero-shotgeneralizationtounseentasks. Wevisualizetheintermediateprogressofeach
methodontwotasks. SeeAppendix,Sec.B.4.3fortheothertwotasks. WedonotplotReActand
Reflexionsincetheydonotmakeanymeaningfulprogress.
Efficientzero-shotgeneralizationtounseentasks. Toevaluatezero-shotgeneralization,weclear
theagent’sinventory,resetittoanewlyinstantiatedworld,andtestitwithunseentasks. Forboth
VOYAGERandAutoGPT,weutilizeGPT-4tobreakdownthetaskintoaseriesofsubgoals. Table.2
andFig.8showVOYAGERcanconsistentlysolveallthetasks,whilebaselinescannotsolveanytask
within50promptingiterations. What’sinterestingtonoteisthatourskilllibraryconstructedfrom
lifelonglearningnotonlyenhances VOYAGER’sperformancebutalsogivesaboosttoAutoGPT.
Thisdemonstratesthattheskilllibraryservesasaversatiletoolthatcanbereadilyemployedbyother
methods,effectivelyactingasaplug-and-playassettoenhanceperformance.
3.4 AblationStudies
Weablate6designchoices(automaticcurriculum,skilllibrary,environmentfeedback,execution
errors, self-verification, and GPT-4 for code generation) in VOYAGER and study their impact on
explorationperformance(seeAppendix,Sec.B.3fordetailsofeachablatedvariant). Resultsare
showninFig.9. Wehighlightthekeyfindingsbelow:
• Automaticcurriculumiscrucialfortheagent’sconsistentprogress. Thediscovereditem
countdropsby93%ifthecurriculumisreplacedwitharandomone,becausecertaintasks
maybetoochallengingifattemptedoutoforder. Ontheotherhand,amanuallydesigned
curriculumrequiressignificantMinecraft-specificexpertise,anddoesnottakeintoaccount
theagent’slivesituation. Itfallsshortintheexperimentalresultscomparedtoourautomatic
curriculum.
• VOYAGER w/o skill library exhibits a tendency to plateau in the later stages. This
underscoresthepivotalrolethattheskilllibraryplaysinVOYAGER. Ithelpscreatemore
complexactionsandsteadilypushestheagent’sboundariesbyencouragingnewskillstobe
builtuponolderones.
8
Figure9: Left: Ablationstudiesfortheautomaticcurriculum,skilllibrary,andGPT-4. GPT-3.5
meansreplacingGPT-4withGPT-3.5forcodegeneration. VOYAGERoutperformsallthealternatives,
demonstrating the critical role of each component. Right: Ablation studies for the iterative
promptingmechanism. VOYAGERsurpassesalltheotheroptions,therebyhighlightingtheessential
significanceofeachtypeoffeedbackintheiterativepromptingmechanism.
Figure10: VOYAGERbuilds3Dstructureswithhumanfeedback. Theprogressofbuildingdesigns
thatintegratehumaninputisdemonstratedfromlefttoright.
• Self-verificationisthemostimportantamongallthefeedbacktypes. Removingthe
moduleleadstoasignificantdrop(−73%)inthediscovereditemcount. Self-verification
serves as a critical mechanism to decide when to move on to a new task or reattempt a
previouslyunsuccessfultask.
• GPT-4significantlyoutperformsGPT-3.5incodegenerationandobtains5.7×more
uniqueitems,asGPT-4exhibitsaquantumleapincodingabilities.Thisfindingcorroborates
recentstudiesintheliterature [56,57].
3.5 MultimodalFeedbackfromHumans
VOYAGERdoesnotcurrentlysupportvisualperception,becausetheavailableversionofGPT-4API
istext-onlyatthetimeofthiswriting. However, VOYAGER hasthepotentialtobeaugmentedby
multimodalperceptionmodels[58,59]toachievemoreimpressivetasks. Wedemonstratethatgiven
humanfeedback,VOYAGERisabletoconstructcomplex3DstructuresinMinecraft,suchasaNether
Portalandahouse(Fig.10). Therearetwowaystointegratehumanfeedback:
(1) Human as a critic (equivalent to VOYAGER’s self-verification module): humans provide
visualcritiquetoVOYAGER,allowingittomodifythecodefromthepreviousround. This
feedbackisessentialforcorrectingcertainerrorsinthespatialdetailsofa3Dstructurethat
VOYAGERcannotperceivedirectly.
(2) Humanasacurriculum(equivalenttoVOYAGER’sautomaticcurriculummodule): humans
breakdownacomplexbuildingtaskintosmallersteps,guidingVOYAGERtocompletethem
incrementally. ThisapproachimprovesVOYAGER’sabilitytohandlemoresophisticated3D
constructiontasks.
9
4 LimitationsandFutureWork
Cost. TheGPT-4APIincurssignificantcosts. Itis15×moreexpensivethanGPT-3.5. Nevertheless,
VOYAGERrequiresthequantumleapincodegenerationqualityfromGPT-4(Fig.9),whichGPT-3.5
andopen-sourceLLMscannotprovide[60].
Inaccuracies. Despitetheiterativepromptingmechanism,therearestillcaseswheretheagentgets
stuckandfailstogeneratethecorrectskill. Theautomaticcurriculumhastheflexibilitytoreattempt
thistaskatalatertime. Occasionally,self-verificationmodulemayalsofail,suchasnotrecognizing
spiderstringasasuccesssignalofbeatingaspider.
Hallucinations. Theautomaticcurriculumoccasionallyproposesunachievabletasks. Forexample,it
mayasktheagenttocrafta“coppersword"or“copperchestplate",whichareitemsthatdonotexist
withinthegame. Hallucinationsalsooccurduringthecodegenerationprocess. Forinstance,GPT-4
tendstousecobblestoneasafuelinput,despitebeinganinvalidfuelsourceinthegame. Additionally,
itmaycallfunctionsabsentintheprovidedcontrolprimitiveAPIs,leadingtocodeexecutionerrors.
WeareconfidentthatimprovementsintheGPTAPImodelsaswellasnoveltechniquesforfinetuning
open-sourceLLMswillovercometheselimitationsinthefuture.
5 Relatedwork
Decision-makingAgents inMinecraft. Minecraftis anopen-ended 3Dworldwith incredibly
flexiblegamemechanicssupportingabroadspectrumofactivities. BuiltuponnotableMinecraft
benchmarks [23, 61–65], Minecraft learning algorithms can be divided into two categories: 1)
Low-levelcontroller: Manyprioreffortsleveragehierarchicalreinforcementlearningtolearnfrom
humandemonstrations[66–68]. Kanitscheideretal.[14]designacurriculumbasedonsuccessrates,
butitsobjectivesarelimitedtocurateditems. MineDojo[23]andVPT[8]utilizeYouTubevideos
forlarge-scalepre-training. DreamerV3[69],ontheotherhand,learnsaworldmodeltoexplore
theenvironmentandcollectdiamonds. 2)High-levelplanner: Volumetal.[70]leveragefew-shot
prompting with Codex [41] to generate executable policies, but they require additional human
interaction. Recent works leverage LLMs as a high-level planner in Minecraft by decomposing
ahigh-leveltaskintoseveralsubgoalsfollowingMinecraftrecipes[55,53,71], thuslackingfull
explorationflexibility. Liketheselatterworks,VOYAGERalsousesLLMsasahigh-levelplannerby
promptingGPT-4andutilizesMineflayer[52]asalow-levelcontrollerfollowingVolumetal.[70].
Unlikepriorworks,VOYAGERemploysanautomaticcurriculumthatunfoldsinabottom-upmanner,
drivenbycuriosity,andthereforeenablesopen-endedexploration.
LargeLanguageModelsforAgentPlanning. Inspiredbythestrongemergentcapabilitiesof
LLMs,suchaszero-shotpromptingandcomplexreasoning[72,37,38,36,73,74],embodiedagent
research[75–78]haswitnessedasignificantincreaseintheutilizationofLLMsforplanningpurposes.
Recent efforts can be roughly classified into two groups. 1) Large language models for robot
learning: ManypriorworksapplyLLMstogeneratesubgoalsforrobotplanning[27,27,25,79,80].
InnerMonologue[26]incorporatesenvironmentfeedbackforrobotplanningwithLLMs. Codeas
Policies [16] and ProgPrompt [22] directly leverage LLMs to generate executable robot policies.
VIMA [19] and PaLM-E [59] fine-tune pre-trained LLMs to support multimodal prompts. 2)
Largelanguagemodelsfortextagents: ReAct[29]leverageschain-of-thoughtprompting[46]and
generatesbothreasoningtracesandtask-specificactionswithLLMs. Reflexion[30]isbuiltupon
ReAct[29]withself-reflectiontoenhancereasoning. AutoGPT[28]isapopulartoolthatautomates
NLP tasks by crafting a curriculum of multiple subgoals for completing a high-level goal while
incorporating ReAct [29]’s reasoning and acting loops. DERA [81] frames a task as a dialogue
betweentwoGPT-4[35]agents. GenerativeAgents[82]leveragesChatGPT[50]tosimulatehuman
behaviorsbystoringagents’experiencesasmemoriesandretrievingthoseforplanning,butitsagent
actions are not executable. SPRING [83] is a concurrent work that uses GPT-4 to extract game
mechanicsfromgamemanuals,basedonwhichitanswersquestionsarrangedinadirectedacyclic
graphandpredictsthenextaction. Alltheseworkslackaskilllibraryfordevelopingmorecomplex
behaviors,whicharecrucialcomponentsforthesuccessofVOYAGERinlifelonglearning.
Code Generation with Execution. Code generation has been a longstanding challenge in
NLP [41, 84, 85, 73, 37], with various works leveraging execution results to improve program
10
synthesis. Execution-guidedapproachesleverageintermediateexecutionoutcomestoguideprogram
search[86–88]. Anotherlineofresearchutilizesmajorityvotingtochoosecandidatesbasedontheir
executionperformance[89,90]. Additionally,LEVER[91]trainsaverifiertodistinguishandreject
incorrectprogramsbasedonexecutionresults. CLAIRIFY[92],ontheotherhand,generatescode
for planning chemistry experiments and makes use of a rule-based verifier to iteratively provide
errorfeedbacktoLLMs. VOYAGERdistinguishesitselffromtheseworksbyintegratingenvironment
feedback,executionerrors,andself-verification(toassesstasksuccess)intoaniterativeprompting
mechanismforembodiedcontrol.
6 Conclusion
In this work, we introduce VOYAGER, the first LLM-powered embodied lifelong learning agent,
whichleveragesGPT-4toexploretheworldcontinuously,developincreasinglysophisticatedskills,
andmakenewdiscoveriesconsistentlywithouthumanintervention. VOYAGER exhibitssuperior
performanceindiscoveringnovelitems,unlockingtheMinecrafttechtree,traversingdiverseterrains,
andapplyingitslearnedskilllibrarytounseentasksinanewlyinstantiatedworld. VOYAGERserves
asastartingpointtodeveloppowerfulgeneralistagentswithouttuningthemodelparameters.
7 BroaderImpacts
OurresearchisconductedwithinMinecraft,asafeandharmless3Dvideogameenvironment. While
VOYAGERisdesignedtobegenerallyapplicabletootherdomains,suchasrobotics,itsapplicationto
physicalrobotswouldrequireadditionalattentionandtheimplementationofsafetyconstraintsby
humanstoensureresponsibleandsecuredeployment.
8 Acknowledgements
WeareextremelygratefultoZimingZhu,KaiyuYang,RafałKocielnik,ColinWhite,OrSharir,Sahin
Lale,De-AnHuang,JeanKossaifi,YuncongYang,CharlesZhang,MinchaoHuang,andmanyother
colleaguesandfriendsfortheirhelpfulfeedbackandinsightfuldiscussions. Thisworkisdoneduring
GuanzhiWang’sinternshipatNVIDIA.GuanzhiWangissupportedbytheKortschakfellowshipin
ComputingandMathematicalSciencesatCaltech.
References
[1] Eric Kolve, Roozbeh Mottaghi, Winson Han, Eli VanderBilt, Luca Weihs, Alvaro Herrasti,
Daniel Gordon, Yuke Zhu, Abhinav Gupta, and Ali Farhadi. Ai2-thor: An interactive 3d
environmentforvisualai. arXivpreprintarXiv: Arxiv-1712.05474,2017.
[2] Manolis Savva, Jitendra Malik, Devi Parikh, Dhruv Batra, Abhishek Kadian, Oleksandr
Maksymets, Yili Zhao, Erik Wijmans, Bhavana Jain, Julian Straub, Jia Liu, and Vladlen
Koltun. Habitat: A platform for embodied AI research. In 2019 IEEE/CVF International
ConferenceonComputerVision,ICCV2019,Seoul,Korea(South),October27-November2,
2019,pages9338–9346.IEEE,2019.
[3] Yuke Zhu, Josiah Wong, Ajay Mandlekar, and Roberto Martín-Martín. robosuite: A mod-
ular simulation framework and benchmark for robot learning. arXiv preprint arXiv: Arxiv-
2009.12293,2020.
[4] FeiXia,WilliamB.Shen,ChengshuLi,PriyaKasimbeg,MicaelTchapmi,AlexanderToshev,
LiFei-Fei,RobertoMartín-Martín,andSilvioSavarese. Interactivegibsonbenchmark(igibson
0.5): Abenchmarkforinteractivenavigationinclutteredenvironments. arXivpreprintarXiv:
Arxiv-1910.14442,2019.
[5] BokuiShen,FeiXia,ChengshuLi,RobertoMartín-Martín,LinxiFan,GuanzhiWang,Claudia
Pérez-D’Arpino,ShyamalBuch,SanjanaSrivastava,LyneP.Tchapmi,MicaelE.Tchapmi,Kent
Vainio,JosiahWong,LiFei-Fei,andSilvioSavarese. igibson1.0: asimulationenvironmentfor
interactivetasksinlargerealisticscenes. arXivpreprintarXiv: Arxiv-2012.02924,2020.
11
[6] JensKober,JAndrewBagnell,andJanPeters. Reinforcementlearninginrobotics: Asurvey.
TheInternationalJournalofRoboticsResearch,32(11):1238–1274,2013.
[7] KaiArulkumaran,MarcPeterDeisenroth,MilesBrundage,andAnilAnthonyBharath. Deep
reinforcementlearning: Abriefsurvey. IEEESignalProcessingMagazine,34(6):26–38,2017.
[8] BowenBaker,IlgeAkkaya,PeterZhokhov,JoostHuizinga,JieTang,AdrienEcoffet,Brandon
Houghton,RaulSampedro,andJeffClune. Videopretraining(vpt):Learningtoactbywatching
unlabeledonlinevideos. arXivpreprintarXiv: Arxiv-2206.11795,2022.
[9] DeepMindInteractiveAgentsTeam,JoshAbramson,ArunAhuja,ArthurBrussee,Federico
Carnevale, Mary Cassin, Felix Fischer, Petko Georgiev, Alex Goldin, Mansi Gupta, Tim
Harley,FelixHill,PeterCHumphreys,AldenHung,JessicaLandon,TimothyLillicrap,Hamza
Merzic,AlistairMuldal,AdamSantoro,GuyScully,TamaravonGlehn,GregWayne,Nathaniel
Wong, Chen Yan, and Rui Zhu. Creating multimodal interactive agents with imitation and
self-supervisedlearning. arXivpreprintarXiv: Arxiv-2112.03763,2021.
[10] Oriol Vinyals, Igor Babuschkin, Junyoung Chung, Michael Mathieu, Max Jaderberg, Wo-
jciech M Czarnecki, Andrew Dudzik, Aja Huang, Petko Georgiev, Richard Powell, et al.
Alphastar: Masteringthereal-timestrategygamestarcraftii. DeepMindblog,2,2019.
[11] AdrienEcoffet,JoostHuizinga,JoelLehman,KennethO.Stanley,andJeffClune. Go-explore:
anewapproachforhard-explorationproblems. arXivpreprintarXiv: Arxiv-1901.10995,2019.
[12] JoostHuizingaandJeffClune. Evolvingmultimodalrobotbehaviorviamanysteppingstones
with the combinatorial multiobjective evolutionary algorithm. Evolutionary computation,
30(2):131–164,2022.
[13] Rui Wang, JoelLehman, AdityaRawal, Jiale Zhi, Yulun Li, Jeffrey Clune, and KennethO.
Stanley. EnhancedPOET:open-endedreinforcementlearningthroughunboundedinventionof
learningchallengesandtheirsolutions. InProceedingsofthe37thInternationalConferenceon
MachineLearning,ICML2020,13-18July2020,VirtualEvent,volume119ofProceedingsof
MachineLearningResearch,pages9940–9951.PMLR,2020.
[14] IngmarKanitscheider,JoostHuizinga,DavidFarhi,WilliamHebgenGuss,BrandonHoughton,
RaulSampedro,PeterZhokhov,BowenBaker,AdrienEcoffet,JieTang,OlegKlimov,andJeff
Clune.Multi-taskcurriculumlearninginacomplex,visual,hard-explorationdomain:Minecraft.
arXivpreprintarXiv: Arxiv-2106.14876,2021.
[15] MichaelDennis,NatashaJaques,EugeneVinitsky,AlexandreM.Bayen,StuartRussell,Andrew
Critch, and Sergey Levine. Emergent complexity and zero-shot transfer via unsupervised
environmentdesign. InHugoLarochelle,Marc’AurelioRanzato,RaiaHadsell,Maria-Florina
Balcan,andHsuan-TienLin,editors,AdvancesinNeuralInformationProcessingSystems33:
AnnualConferenceonNeuralInformationProcessingSystems2020,NeurIPS2020,December
6-12,2020,virtual,2020.
[16] JackyLiang,WenlongHuang,FeiXia,PengXu,KarolHausman,BrianIchter,PeteFlorence,
andAndyZeng. Codeaspolicies: Languagemodelprogramsforembodiedcontrol. arXiv
preprintarXiv: Arxiv-2209.07753,2022.
[17] Shao-HuaSun,Te-LinWu,andJosephJ.Lim. Programguidedagent. In8thInternational
ConferenceonLearningRepresentations,ICLR2020,AddisAbaba,Ethiopia,April26-30,2020.
OpenReview.net,2020.
[18] ZelinZhao,KaranSamel,BinghongChen,andLeSong.Proto:Program-guidedtransformerfor
program-guidedtasks. InMarc’AurelioRanzato,AlinaBeygelzimer,YannN.Dauphin,Percy
Liang,andJenniferWortmanVaughan,editors,AdvancesinNeuralInformationProcessing
Systems 34: Annual Conference on Neural Information Processing Systems 2021, NeurIPS
2021,December6-14,2021,virtual,pages17021–17036,2021.
[19] Yunfan Jiang, Agrim Gupta, Zichen Zhang, Guanzhi Wang, Yongqiang Dou, Yanjun Chen,
LiFei-Fei,AnimaAnandkumar,YukeZhu,andLinxi(Jim)Fan. Vima: Generalrobotmanipu-
lationwithmultimodalprompts. ARXIV.ORG,2022.
12
[20] MohitShridhar,LucasManuelli,andDieterFox. Cliport: Whatandwherepathwaysforrobotic
manipulation. arXivpreprintarXiv: Arxiv-2109.12098,2021.
[21] LinxiFan,GuanzhiWang,De-AnHuang,ZhidingYu,LiFei-Fei,YukeZhu,andAnimashree
Anandkumar. SECANT:self-expertcloningforzero-shotgeneralizationofvisualpolicies. In
MarinaMeilaandTongZhang,editors,Proceedingsofthe38thInternationalConferenceon
MachineLearning,ICML2021,18-24July2021,VirtualEvent,volume139ofProceedingsof
MachineLearningResearch,pages3088–3099.PMLR,2021.
[22] IshikaSingh,ValtsBlukis,ArsalanMousavian,AnkitGoyal,DanfeiXu,JonathanTremblay,
DieterFox,JesseThomason,andAnimeshGarg. Progprompt: Generatingsituatedrobottask
plansusinglargelanguagemodels. arXivpreprintarXiv: Arxiv-2209.11302,2022.
[23] LinxiFan,GuanzhiWang,YunfanJiang,AjayMandlekar,YuncongYang,HaoyiZhu,Andrew
Tang, De-AnHuang, YukeZhu, andAnimaAnandkumar. Minedojo: Buildingopen-ended
embodiedagentswithinternet-scaleknowledge. arXivpreprintarXiv: Arxiv-2206.08853,2022.
[24] AndyZeng,AdrianWong,StefanWelker,KrzysztofChoromanski,FedericoTombari,Aveek
Purohit,MichaelRyoo,VikasSindhwani,JohnnyLee,VincentVanhoucke,andPeteFlorence.
Socraticmodels: Composingzero-shotmultimodalreasoningwithlanguage. arXivpreprint
arXiv: Arxiv-2204.00598,2022.
[25] MichaelAhn,AnthonyBrohan,NoahBrown,YevgenChebotar,OmarCortes,ByronDavid,
ChelseaFinn,KeerthanaGopalakrishnan,KarolHausman,AlexHerzog,DanielHo,Jasmine
Hsu,JulianIbarz,BrianIchter,AlexIrpan,EricJang,RosarioJaureguiRuano,KyleJeffrey,
SallyJesmonth,NikhilJJoshi,RyanJulian,DmitryKalashnikov,YuhengKuang,Kuang-Huei
Lee, Sergey Levine, Yao Lu, Linda Luu, Carolina Parada, Peter Pastor, Jornell Quiambao,
KanishkaRao,JarekRettinghouse,DiegoReyes,PierreSermanet,NicolasSievers,ClaytonTan,
AlexanderToshev,VincentVanhoucke,FeiXia,TedXiao,PengXu,SichunXu,andMengyuan
Yan. Doasican,notasisay: Groundinglanguageinroboticaffordances. arXivpreprintarXiv:
Arxiv-2204.01691,2022.
[26] Wenlong Huang, Fei Xia, Ted Xiao, Harris Chan, Jacky Liang, Pete Florence, Andy Zeng,
JonathanTompson,IgorMordatch,YevgenChebotar,PierreSermanet,NoahBrown,Tomas
Jackson, Linda Luu, Sergey Levine, Karol Hausman, and Brian Ichter. Inner monologue:
Embodied reasoning through planning with language models. arXiv preprint arXiv: Arxiv-
2207.05608,2022.
[27] WenlongHuang,PieterAbbeel,DeepakPathak,andIgorMordatch. Languagemodelsaszero-
shotplanners: Extractingactionableknowledgeforembodiedagents. InKamalikaChaudhuri,
StefanieJegelka,LeSong,CsabaSzepesvári,GangNiu,andSivanSabato,editors,International
ConferenceonMachineLearning,ICML2022,17-23July2022,Baltimore,Maryland,USA,
volume162ofProceedingsofMachineLearningResearch,pages9118–9147.PMLR,2022.
[28] Significant-gravitas/auto-gpt: An experimental open-source attempt to make gpt-4 fully au-
tonomous.,2023.
[29] ShunyuYao,JeffreyZhao,DianYu,NanDu,IzhakShafran,KarthikNarasimhan,andYuan
Cao. React: Synergizing reasoning and acting in language models. arXiv preprint arXiv:
Arxiv-2210.03629,2022.
[30] Noah Shinn, Beck Labash, and Ashwin Gopinath. Reflexion: an autonomous agent with
dynamicmemoryandself-reflection. arXivpreprintarXiv: Arxiv-2303.11366,2023.
[31] GermanIgnacioParisi,RonaldKemker,JoseL.Part,ChristopherKanan,andStefanWermter.
Continuallifelonglearningwithneuralnetworks: Areview. NeuralNetworks,113:54–71,2019.
[32] LiyuanWang,XingxingZhang,HangSu,andJunZhu. Acomprehensivesurveyofcontinual
learning: Theory,methodandapplication. arXivpreprintarXiv: Arxiv-2302.00487,2023.
[33] VolodymyrMnih,KorayKavukcuoglu,DavidSilver,AlexGraves,IoannisAntonoglou,Daan
Wierstra,andMartinRiedmiller. Playingatariwithdeepreinforcementlearning. arXivpreprint
arXiv: Arxiv-1312.5602,2013.
13
[34] OpenAI, :, Christopher Berner, Greg Brockman, Brooke Chan, Vicki Cheung, Przemysław
De˛biak,ChristyDennison,DavidFarhi,QuirinFischer,ShariqHashme,ChrisHesse,RafalJóze-
fowicz,ScottGray,CatherineOlsson,JakubPachocki,MichaelPetrov,HenriqueP.d.O.Pinto,
Jonathan Raiman, Tim Salimans, Jeremy Schlatter, Jonas Schneider, Szymon Sidor, Ilya
Sutskever,JieTang,FilipWolski,andSusanZhang. Dota2withlargescaledeepreinforcement
learning. arXivpreprintarXiv: Arxiv-1912.06680,2019.
[35] OpenAI. Gpt-4technicalreport. arXivpreprintarXiv: Arxiv-2303.08774,2023.
[36] JasonWei,YiTay,RishiBommasani,ColinRaffel,BarretZoph,SebastianBorgeaud,Dani
Yogatama,MaartenBosma,DennyZhou,DonaldMetzler,EdH.Chi,TatsunoriHashimoto,
OriolVinyals,PercyLiang,JeffDean,andWilliamFedus. Emergentabilitiesoflargelanguage
models. arXivpreprintarXiv: Arxiv-2206.07682,2022.
[37] TomB.Brown,BenjaminMann,NickRyder,MelanieSubbiah,JaredKaplan,PrafullaDhariwal,
ArvindNeelakantan,PranavShyam,GirishSastry,AmandaAskell,SandhiniAgarwal,Ariel
Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M.
Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz
Litwin,ScottGray,BenjaminChess,JackClark,ChristopherBerner,SamMcCandlish,Alec
Radford,IlyaSutskever,andDarioAmodei. Languagemodelsarefew-shotlearners. InHugo
Larochelle,Marc’AurelioRanzato,RaiaHadsell,Maria-FlorinaBalcan,andHsuan-TienLin,
editors,AdvancesinNeuralInformationProcessingSystems33: AnnualConferenceonNeural
InformationProcessingSystems2020,NeurIPS2020,December6-12,2020,virtual,2020.
[38] ColinRaffel,NoamShazeer,AdamRoberts,KatherineLee,SharanNarang,MichaelMatena,
YanqiZhou,WeiLi,andPeterJ.Liu. Exploringthelimitsoftransferlearningwithaunified
text-to-texttransformer. J.Mach.Learn.Res.,21:140:1–140:67,2020.
[39] BenjaminEysenbach,AbhishekGupta,JulianIbarz,andSergeyLevine. Diversityisallyou
need: Learningskillswithoutarewardfunction. In7thInternationalConferenceonLearning
Representations,ICLR2019,NewOrleans,LA,USA,May6-9,2019.OpenReview.net,2019.
[40] EdoardoConti,VashishtMadhavan,FelipePetroskiSuch,JoelLehman,KennethO.Stanley,
andJeffClune.Improvingexplorationinevolutionstrategiesfordeepreinforcementlearningvia
apopulationofnovelty-seekingagents. InSamyBengio,HannaM.Wallach,HugoLarochelle,
Kristen Grauman, Nicolò Cesa-Bianchi, and Roman Garnett, editors, Advances in Neural
Information Processing Systems 31: Annual Conference on Neural Information Processing
Systems2018,NeurIPS2018,December3-8,2018,Montréal,Canada,pages5032–5043,2018.
[41] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto,
JaredKaplan,HarriEdwards,YuriBurda,NicholasJoseph,GregBrockman,AlexRay,Raul
Puri,GretchenKrueger,MichaelPetrov,HeidyKhlaaf,GirishSastry,PamelaMishkin,Brooke
Chan,ScottGray,NickRyder,MikhailPavlov,AletheaPower,LukaszKaiser,Mohammad
Bavarian,ClemensWinter,PhilippeTillet,FelipePetroskiSuch,DaveCummings,Matthias
Plappert,FotiosChantzis,ElizabethBarnes,ArielHerbert-Voss,WilliamHebgenGuss,Alex
Nichol,AlexPaino,NikolasTezak,JieTang,IgorBabuschkin,SuchirBalaji,ShantanuJain,
WilliamSaunders,ChristopherHesse,AndrewN.Carr,JanLeike,JoshAchiam,VedantMisra,
EvanMorikawa,AlecRadford,MatthewKnight,MilesBrundage,MiraMurati,KatieMayer,
PeterWelinder,BobMcGrew,DarioAmodei,SamMcCandlish,IlyaSutskever,andWojciech
Zaremba. Evaluating large language models trained on code. arXiv preprint arXiv: Arxiv-
2107.03374,2021.
[42] RuiWang,JoelLehman,JeffClune,andKennethO.Stanley. Pairedopen-endedtrailblazer
(poet): Endlesslygeneratingincreasinglycomplexanddiverselearningenvironmentsandtheir
solutions. arXivpreprintarXiv: Arxiv-1901.01753,2019.
[43] RémyPortelas,CédricColas,LilianWeng,KatjaHofmann,andPierre-YvesOudeyer. Auto-
maticcurriculumlearningfordeepRL:Ashortsurvey.InChristianBessiere,editor,Proceedings
oftheTwenty-NinthInternationalJointConferenceonArtificialIntelligence,IJCAI2020,pages
4819–4825.ijcai.org,2020.
14
[44] Sébastien Forestier, Rémy Portelas, Yoan Mollard, and Pierre-Yves Oudeyer. Intrinsically
motivated goal exploration processes with automatic curriculum learning. The Journal of
MachineLearningResearch,23(1):6818–6858,2022.
[45] KevinEllis,CatherineWong,MaxwellNye,MathiasSable-Meyer,LucCary,LucasMorales,
Luke Hewitt, Armando Solar-Lezama, and Joshua B. Tenenbaum. Dreamcoder: Growing
generalizable, interpretable knowledge with wake-sleep bayesian program learning. arXiv
preprintarXiv: Arxiv-2006.08381,2020.
[46] JasonWei,XuezhiWang,DaleSchuurmans,MaartenBosma,EdChi,QuocLe,andDenny
Zhou. Chainofthoughtpromptingelicitsreasoninginlargelanguagemodels. arXivpreprint
arXiv: Arxiv-2201.11903,2022.
[47] VolodymyrMnih,AdriàPuigdomènechBadia,MehdiMirza,AlexGraves,TimothyP.Lillicrap,
Tim Harley, David Silver, and Koray Kavukcuoglu. Asynchronous methods for deep rein-
forcementlearning. InMaria-FlorinaBalcanandKilianQ.Weinberger,editors,Proceedings
ofthe33ndInternationalConferenceonMachineLearning,ICML2016,NewYorkCity,NY,
USA,June19-24,2016,volume48ofJMLRWorkshopandConferenceProceedings,pages
1928–1937.JMLR.org,2016.
[48] JohnSchulman,FilipWolski,PrafullaDhariwal,AlecRadford,andOlegKlimov. Proximal
policyoptimizationalgorithms. arXivpreprintarXiv: Arxiv-1707.06347,2017.
[49] Timothy P. Lillicrap, Jonathan J. Hunt, Alexander Pritzel, Nicolas Heess, Tom Erez, Yuval
Tassa,DavidSilver,andDaanWierstra. Continuouscontrolwithdeepreinforcementlearning.
InYoshuaBengioandYannLeCun,editors,4thInternationalConferenceonLearningRepre-
sentations,ICLR2016,SanJuan,PuertoRico,May2-4,2016,ConferenceTrackProceedings,
2016.
[50] Introducingchatgpt,2022.
[51] Newandimprovedembeddingmodel,2022.
[52] PrismarineJS. Prismarinejs/mineflayer: Createminecraftbotswithapowerful,stable,andhigh
leveljavascriptapi.,2013.
[53] KolbyNottingham,PrithvirajAmmanabrolu,AlaneSuhr,YejinChoi,HannaHajishirzi,Sameer
Singh, and Roy Fox. Do embodied agents dream of pixelated sheep?: Embodied decision
makingusinglanguageguidedworldmodelling. ARXIV.ORG,2023.
[54] ShaofeiCai, ZihaoWang, XiaojianMa, AnjiLiu, andYitaoLiang. Open-worldmulti-task
control through goal-aware representation learning and adaptive horizon prediction. arXiv
preprintarXiv: Arxiv-2301.10034,2023.
[55] ZihaoWang,ShaofeiCai,AnjiLiu,XiaojianMa,andYitaoLiang. Describe,explain,planand
select: Interactiveplanningwithlargelanguagemodelsenablesopen-worldmulti-taskagents.
arXivpreprintarXiv: Arxiv-2302.01560,2023.
[56] SébastienBubeck,VarunChandrasekaran,RonenEldan,JohannesGehrke,EricHorvitz,Ece
Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, Harsha Nori, Hamid Palangi,
MarcoTulioRibeiro,andYiZhang. Sparksofartificialgeneralintelligence: Earlyexperiments
withgpt-4. arXivpreprintarXiv: Arxiv-2303.12712,2023.
[57] YihengLiu,TianleHan,SiyuanMa,JiayueZhang,YuanyuanYang,JiamingTian,HaoHe,
AntongLi, MengshenHe, ZhengliangLiu, ZihaoWu, DajiangZhu, XiangLi, NingQiang,
DingangShen,TianmingLiu,andBaoGe. Summaryofchatgpt/gpt-4researchandperspective
towardsthefutureoflargelanguagemodels. arXivpreprintarXiv: Arxiv-2304.01852,2023.
[58] ShikunLiu,LinxiFan,EdwardJohns,ZhidingYu,ChaoweiXiao,andAnimaAnandkumar.
Prismer: Avision-languagemodelwithanensembleofexperts. arXivpreprintarXiv: Arxiv-
2303.02506,2023.
15
[59] DannyDriess,FeiXia,MehdiS.M.Sajjadi,CoreyLynch,AakankshaChowdhery,BrianIchter,
AyzaanWahid,JonathanTompson,QuanVuong,TianheYu,WenlongHuang,YevgenChebotar,
PierreSermanet,DanielDuckworth,SergeyLevine,VincentVanhoucke,KarolHausman,Marc
Toussaint,KlausGreff,AndyZeng,IgorMordatch,andPeteFlorence. Palm-e: Anembodied
multimodallanguagemodel. arXivpreprintarXiv: Arxiv-2303.03378,2023.
[60] HugoTouvron,ThibautLavril,GautierIzacard,XavierMartinet,Marie-AnneLachaux,Timo-
théeLacroix,BaptisteRozière,NamanGoyal,EricHambro,FaisalAzhar,AurelienRodriguez,
ArmandJoulin,EdouardGrave,andGuillaumeLample. Llama: Openandefficientfoundation
languagemodels. arXivpreprintarXiv: Arxiv-2302.13971,2023.
[61] WilliamH.Guss,BrandonHoughton,NicholayTopin,PhillipWang,CaydenCodel,Manuela
Veloso,andRuslanSalakhutdinov. Minerl: Alarge-scaledatasetofminecraftdemonstrations.
In Sarit Kraus, editor, Proceedings of the Twenty-Eighth International Joint Conference on
Artificial Intelligence, IJCAI 2019, Macao, China, August 10-16, 2019, pages 2442–2448.
ijcai.org,2019.
[62] WilliamH.Guss,CaydenCodel,KatjaHofmann,BrandonHoughton,NoboruKuno,Stephanie
Milani, Sharada Mohanty, Diego Perez Liebana, Ruslan Salakhutdinov, Nicholay Topin,
Manuela Veloso, and Phillip Wang. The minerl 2019 competition on sample efficient re-
inforcementlearningusinghumanpriors. arXivpreprintarXiv: Arxiv-1904.10079,2019.
[63] WilliamH.Guss,MarioYnocenteCastro,SamDevlin,BrandonHoughton,NoboruSeanKuno,
CrissmanLoomis,StephanieMilani,SharadaMohanty,KeisukeNakata,RuslanSalakhutdinov,
JohnSchulman,ShinyaShiroshita,NicholayTopin,AvinashUmmadisingu,andOriolVinyals.
Theminerl2020competitiononsampleefficientreinforcementlearningusinghumanpriors.
arXivpreprintarXiv: Arxiv-2101.11071,2021.
[64] AnssiKanervisto,StephanieMilani,KarolisRamanauskas,NicholayTopin,ZichuanLin,Jun-
youLi,JianingShi,DehengYe,QiangFu,WeiYang,WeijunHong,ZhongyueHuang,Haicheng
Chen,GuangjunZeng,YueLin,VincentMicheli,EloiAlonso,FrançoisFleuret,Alexander
Nikulin, Yury Belousov, Oleg Svidchenko, and Aleksei Shpilman. Minerl diamond 2021
competition: Overview,results,andlessonslearned. arXivpreprintarXiv: Arxiv-2202.10583,
2022.
[65] MatthewJohnson,KatjaHofmann,TimHutton,andDavidBignell. Themalmoplatformfor
artificialintelligenceexperimentation. InSubbaraoKambhampati,editor,Proceedingsofthe
Twenty-FifthInternationalJointConferenceonArtificialIntelligence,IJCAI2016,NewYork,
NY,USA,9-15July2016,pages4246–4247.IJCAI/AAAIPress,2016.
[66] ZichuanLin,JunyouLi,JianingShi,DehengYe,QiangFu,andWeiYang. Juewu-mc: Playing
minecraft with sample-efficient hierarchical reinforcement learning. arXiv preprint arXiv:
Arxiv-2112.04907,2021.
[67] Hangyu Mao, Chao Wang, Xiaotian Hao, Yihuan Mao, Yiming Lu, Chengjie Wu, Jianye
Hao,DongLi,andPingzhongTang. Seihai: Asample-efficienthierarchicalaifortheminerl
competition. arXivpreprintarXiv: Arxiv-2111.08857,2021.
[68] AlexeySkrynnik,AlekseyStaroverov,ErmekAitygulov,KirillAksenov,VasiliiDavydov,and
AleksandrI.Panov. Hierarchicaldeepq-networkfromimperfectdemonstrationsinminecraft.
Cogn.Syst.Res.,65:74–78,2021.
[69] DanijarHafner,JurgisPasukonis,JimmyBa,andTimothyLillicrap. Masteringdiversedomains
throughworldmodels. arXivpreprintarXiv: Arxiv-2301.04104,2023.
[70] Ryan Volum, Sudha Rao, Michael Xu, Gabriel DesGarennes, Chris Brockett, Benjamin
Van Durme, Olivia Deng, Akanksha Malhotra, and Bill Dolan. Craft an iron sword: Dy-
namicallygeneratinginteractivegamecharactersbypromptinglargelanguagemodelstunedon
code. InProceedingsofthe3rdWordplay: WhenLanguageMeetsGamesWorkshop(Wordplay
2022),pages25–43,Seattle,UnitedStates,2022.AssociationforComputationalLinguistics.
[71] HaoqiYuan,ChiZhang,HongchengWang,FeiyangXie,PenglinCai,HaoDong,andZongqing
Lu. Plan4mc: Skillreinforcementlearningandplanningforopen-worldminecrafttasks. arXiv
preprintarXiv: 2303.16563,2023.
16
[72] RishiBommasani,DrewA.Hudson,EhsanAdeli,RussAltman,SimranArora,SydneyvonArx,
MichaelS.Bernstein,JeannetteBohg,AntoineBosselut,EmmaBrunskill,ErikBrynjolfsson,
ShyamalBuch,DallasCard,RodrigoCastellon,NiladriChatterji,AnnieChen,KathleenCreel,
JaredQuincyDavis,DoraDemszky,ChrisDonahue,MoussaDoumbouya,EsinDurmus,Stefano
Ermon,JohnEtchemendy,KawinEthayarajh,LiFei-Fei,ChelseaFinn,TrevorGale,Lauren
Gillespie,KaranGoel,NoahGoodman,ShelbyGrossman,NeelGuha,TatsunoriHashimoto,
Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas
Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling,
FereshteKhani,OmarKhattab,PangWeiKoh,MarkKrass,RanjayKrishna,RohithKuditipudi,
AnanyaKumar,FaisalLadhak,MinaLee,TonyLee,JureLeskovec,IsabelleLevent,XiangLisa
Li, Xuechen Li, Tengyu Ma, Ali Malik, Christopher D. Manning, Suvir Mirchandani, Eric
Mitchell,ZaneleMunyikwa,SurajNair,AvanikaNarayan,DeepakNarayanan,BenNewman,
AllenNie,JuanCarlosNiebles,HamedNilforoshan,JulianNyarko,GirayOgut,LaurelOrr,
IsabelPapadimitriou,JoonSungPark,ChrisPiech,EvaPortelance,ChristopherPotts,Aditi
Raghunathan, Rob Reich, Hongyu Ren, Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack
Ryan,ChristopherRé,DorsaSadigh,ShioriSagawa,KeshavSanthanam,AndyShih,Krishnan
Srinivasan, Alex Tamkin, Rohan Taori, Armin W. Thomas, Florian Tramèr, Rose E. Wang,
WilliamWang,BohanWu,JiajunWu,YuhuaiWu,SangMichaelXie,MichihiroYasunaga,
JiaxuanYou,MateiZaharia,MichaelZhang,TianyiZhang,XikunZhang,YuhuiZhang,Lucia
Zheng,KaitlynZhou,andPercyLiang. Ontheopportunitiesandrisksoffoundationmodels.
arXivpreprintarXiv: Arxiv-2108.07258,2021.
[73] AakankshaChowdhery,SharanNarang,JacobDevlin,MaartenBosma,GauravMishra,Adam
Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker
Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes,
Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson,
Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin,
TojuDuke,AnselmLevskaya,SanjayGhemawat,SunipaDev,HenrykMichalewski,Xavier
Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David
Luan,HyeontaekLim,BarretZoph,AlexanderSpiridonov,RyanSepassi,DavidDohan,Shivani
Agrawal,MarkOmernick,AndrewM.Dai,ThanumalayanSankaranarayanaPillai,MariePellat,
AitorLewkowycz,EricaMoreira,RewonChild,OleksandrPolozov,KatherineLee,Zongwei
Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei,
KathyMeier-Hellstern,DouglasEck,JeffDean,SlavPetrov,andNoahFiedel. Palm: Scaling
languagemodelingwithpathways. arXivpreprintarXiv: Arxiv-2204.02311,2022.
[74] HyungWonChung,LeHou,ShayneLongpre,BarretZoph,YiTay,WilliamFedus,EricLi,
XuezhiWang, MostafaDehghani, SiddharthaBrahma, AlbertWebson, ShixiangShaneGu,
ZhuyunDai, MiracSuzgun, XinyunChen, AakankshaChowdhery, SharanNarang, Gaurav
Mishra, AdamsYu, VincentZhao, YanpingHuang, AndrewDai, HongkunYu, SlavPetrov,
EdH.Chi,JeffDean,JacobDevlin,AdamRoberts,DennyZhou,QuocV.Le,andJasonWei.
Scalinginstruction-finetunedlanguagemodels. arXivpreprintarXiv: Arxiv-2210.11416,2022.
[75] JiafeiDuan,SamsonYu,HuiLiTan,HongyuanZhu,andChestonTan. Asurveyofembodied
AI:fromsimulatorstoresearchtasks. IEEETrans.Emerg.Top.Comput.Intell.,6(2):230–244,
2022.
[76] DhruvBatra,AngelX.Chang,SoniaChernova,AndrewJ.Davison,JiaDeng,VladlenKoltun,
SergeyLevine,JitendraMalik,IgorMordatch,RoozbehMottaghi,ManolisSavva,andHaoSu.
Rearrangement: Achallengeforembodiedai. arXivpreprintarXiv: Arxiv-2011.01975,2020.
[77] Harish Ravichandar, Athanasios S Polydoros, Sonia Chernova, and Aude Billard. Recent
advances in robot learning from demonstration. Annual review of control, robotics, and
autonomoussystems,3:297–330,2020.
[78] JackCollins,ShelvinChand,AnthonyVanderkop,andDavidHoward. Areviewofphysics
simulatorsforroboticapplications. IEEEAccess,9:51416–51431,2021.
[79] SoYeonMin,DevendraSinghChaplot,PradeepRavikumar,YonatanBisk,andR.Salakhutdi-
nov. Film: Followinginstructionsinlanguagewithmodularmethods. InternationalConference
onLearningRepresentations,2021.
17
[80] ValtsBlukis,ChrisPaxton,DieterFox,AnimeshGarg,andYoavArtzi. Apersistentspatial
semanticrepresentationforhigh-levelnaturallanguageinstructionexecution. In5thAnnual
ConferenceonRobotLearning,2021.
[81] Varun Nair, Elliot Schumacher, Geoffrey Tso, and Anitha Kannan. Dera: Enhancing large
language model completions with dialog-enabled resolving agents. arXiv preprint arXiv:
Arxiv-2303.17071,2023.
[82] JoonSungPark,JosephC.O’Brien,CarrieJ.Cai,MeredithRingelMorris,PercyLiang,and
Michael S. Bernstein. Generative agents: Interactive simulacra of human behavior. arXiv
preprintarXiv: Arxiv-2304.03442,2023.
[83] Yue Wu, Shrimai Prabhumoye, So Yeon Min, Yonatan Bisk, Ruslan Salakhutdinov, Amos
Azaria,TomMitchell,andYuanzhiLi. Spring: Gpt-4out-performsrlalgorithmsbystudying
papersandreasoning. arXivpreprintarXiv: 2305.15486,2023.
[84] ErikNijkamp,BoPang,HiroakiHayashi,LifuTu,HuanWang,YingboZhou,SilvioSavarese,
andCaimingXiong. Aconversationalparadigmforprogramsynthesis. arXivpreprintarXiv:
Arxiv-2203.13474,2022.
[85] HungLe,YueWang,AkhileshDeepakGotmare,SilvioSavarese,andStevenC.H.Hoi. Coderl:
Masteringcodegenerationthroughpretrainedmodelsanddeepreinforcementlearning. arXiv
preprintarXiv: Arxiv-2207.01780,2022.
[86] XinyunChen,ChangLiu,andDawnSong. Execution-guidedneuralprogramsynthesis. In7th
InternationalConferenceonLearningRepresentations,ICLR2019,NewOrleans,LA,USA,
May6-9,2019.OpenReview.net,2019.
[87] XinyunChen,DawnSong,andYuandongTian. Latentexecutionforneuralprogramsynthesis.
arXivpreprintarXiv: Arxiv-2107.00101,2021.
[88] Kevin Ellis, Maxwell I. Nye, Yewen Pu, Felix Sosa, Josh Tenenbaum, and Armando Solar-
Lezama. Write,execute,assess: ProgramsynthesiswithaREPL. InHannaM.Wallach,Hugo
Larochelle, Alina Beygelzimer, Florence d’Alché-Buc, Emily B. Fox, and Roman Garnett,
editors,AdvancesinNeuralInformationProcessingSystems32: AnnualConferenceonNeural
InformationProcessingSystems2019,NeurIPS2019,December8-14,2019,Vancouver,BC,
Canada,pages9165–9174,2019.
[89] YujiaLi,DavidChoi,JunyoungChung,NateKushman,JulianSchrittwieser,RémiLeblond,
TomEccles,JamesKeeling,FelixGimeno,AgustinDalLago,ThomasHubert,PeterChoy,
CypriendeMassond’Autume,IgorBabuschkin,XinyunChen,Po-SenHuang,JohannesWelbl,
SvenGowal,AlexeyCherepanov,JamesMolloy,DanielJ.Mankowitz,EsmeSutherlandRobson,
PushmeetKohli,NandodeFreitas,KorayKavukcuoglu,andOriolVinyals. Competition-level
codegenerationwithalphacode. arXivpreprintarXiv: Arxiv-2203.07814,2022.
[90] KarlCobbe,VineetKosaraju,MohammadBavarian,MarkChen,HeewooJun,LukaszKaiser,
Matthias Plappert, Jerry Tworek, Jacob Hilton, Reiichiro Nakano, Christopher Hesse, and
JohnSchulman. Trainingverifierstosolvemathwordproblems. arXivpreprintarXiv: Arxiv-
2110.14168,2021.
[91] Ansong Ni, Srini Iyer, Dragomir Radev, Ves Stoyanov, Wen tau Yih, Sida I. Wang, and
XiVictoriaLin. Lever: Learningtoverifylanguage-to-codegenerationwithexecution. arXiv
preprintarXiv: Arxiv-2302.08468,2023.
[92] MartaSkreta,NarukiYoshikawa,SebastianArellano-Rubach,ZhiJi,LasseBjørnKristensen,
KouroshDarvish,AlánAspuru-Guzik,FlorianShkurti,andAnimeshGarg. Errorsareuseful
prompts: Instructionguidedtaskprogrammingwithverifier-assistediterativeprompting. arXiv
preprintarXiv: Arxiv-2303.14100,2023.
18
A Method
A.1 VOYAGERAlgorithm
Pseudocode1: VOYAGERalgorithm.
def voyager(
environment, # environment that uses code as action space
curriculum_agent, # curriculum agent for proposing the next task
action_agent, # action agent for code generation
critic_agent, # critic agent for self-verification
skill_manager, # skill manager for adding new skills and skill
retrieval
):
agent_state = environment.reset()
while True:
exploration_progress = (
curriculum_agent.get_exploration_progress(
curriculum_agent.get_completed_tasks(),
curriculum_agent.get_failed_tasks(),
)
)
task = curriculum_agent.propose_next_task(
agent_state, exploration_progress
)
code = None
environment_feedback = None
execution_errors = None
critique = None
success = False
# try at most 4 rounds before moving on to the next task
for i in range(4):
skills = skill_manager.retrieve_skills(
task, environment_feedback
)
code = action_agent.generate_code(
task,
code,
environment_feedback,
execution_errors,
critique,
skills,
)
(
agent_state,
environment_feedback,
execution_errors,
) = environment.step(code)
success, critique = critic_agent.check_task_success(
task, agent_state
)
if success:
break
if success:
skill_manager.add_skill(code)
curriculum_agent.add_completed_task(task)
else:
curriculum_agent.add_failed_task(task)
A.2 Prompting
GPT-4andGPT-3.5offeruserstheabilitytodesignatetheroleofeachpromptmessageamongthree
options:
19
• System:Ahigh-levelinstructionthatguidesthemodelbehaviorthroughouttheconversation.
Itsetstheoveralltoneandobjectivefortheinteraction.
• User: Adetailedinstructionthatguidestheassistantforthenextimmediateresponse.
• Assistant: Aresponsemessagegeneratedthemodel.
Seehttps://platform.openai.com/docs/guides/chat/introductionformoredetails.
Tosavetokenusage, insteadofengaginginmulti-roundconversations, weconcatenateasystem
promptandauserprompttoobtaineachassistant’sresponse.
A.3 AutomaticCurriculum
A.3.1 ComponentsinthePrompt
TheinputprompttoGPT-4consistsofseveralcomponents:
(1) Directivesencouragingdiversebehaviorsandimposingconstraints(sothattheproposed
taskisachievableandverifiable): SeeSec.A.3.4forthefullprompt;
(2) Theagent’scurrentstate:
• Inventory:Adictionaryofitemswithcounts,forexample,{‘cobblestone’:4,‘furnace’:
1,‘stone_pickaxe’: 1,‘oak_planks’: 7,‘dirt’: 6,‘wooden_pickaxe’: 1,‘crafting_table’:
1,‘raw_iron’: 4,‘coal’: 1};
• Equipment: Armorsorweaponsequippedbytheagents;
• Nearby blocks: A set of block names within a 32-block distance to the agent, for
example, ‘dirt’, ‘water’, ‘spruce_planks’, ‘grass_block’, ‘dirt_path’, ‘sugar_cane’,
‘fern’;
• Otherblocksthatarerecentlyseen: Blocksthatarenotnearbyorintheinventory;
• Nearbyentities: Asetofentitynameswithina32-blockdistancetotheagent,for
example,‘pig’,‘cat’,‘villager’,‘zombie’;
• Alistofcheststhatareseenbytheagent: Chestsareexternalcontainerswherethe
agent can deposit items. If a chest is not opened before, its content is “Unknown”.
Otherwise,theitemsinsideeachchestareshowntotheagent.
• Biome: For example, ‘plains’, ‘flower_forest’, ‘meadow’, ‘river’, ‘beach’, ‘for-
est’, ‘snowy_slopes’, ‘frozen_peaks’, ‘old_growth_birch_forest’, ‘ocean’, ‘sun-
flower_plains’,‘stony_shore’;
• Time: Oneof‘sunrise’,‘day’,‘noon’,‘sunset’,‘night’,‘midnight’;
• Healthandhungerbars: Themaxvalueis20;
• Position: 3Dcoordinate(x,y,z)oftheagent’spositionintheMinecraftworld;
(3) Previouslycompletedandfailedtasks;
(4) Additionalcontext: SeeSec.A.3.2;
(5) Chain-of-thoughtprompting[46]inresponse: WerequestGPT-4tofirstreasonaboutthe
currentprogressandthensuggestthenexttask.
A.3.2 AdditionalContext
WeleverageGPT-3.5toself-askquestionstoprovideadditionalcontext. Eachquestionispairedwith
aconceptthatisusedforretrievingthemostrelevantdocumentfromthewikiknowledgebase[23].
WefeedthedocumentcontenttoGPT-3.5forself-answeringquestions. Inpractice,usingawiki
knowledge base is optional since GPT-3.5 already possesses a good understanding of Minecraft
gamemechanics. However,theexternalknowledgebasebecomesadvantageousifGPT-3.5isnot
pre-trainedinthatspecificdomain. SeeSec.A.3.4forthefullprompt.
A.3.3 Warm-upSchedule
Inpractice,weadoptawarm-upscheduletograduallyincorporatetheagent’sstateandtheadditional
contextintothepromptbasedonhowmanytaskstheagenthascompleted. Thisensuresthatthe
promptisexposedtoincreasingamountsofinformationovertheexplorationprogressandtherefore
20
beginswithbasicskillsandprogressivelyadvancestowardsmoreintricateanddiverseones. The
warm-upsettingthatweuseacrossalltheexperimentsisshowninTable.A.1.
TableA.1: Warm-upscheduleforautomaticcurriculum.
Informationintheprompt Afterhowmanytasksarecompleted
coreinventory(onlyincludinglog,planks,stick,
craftingtable,furnace,dirt,coal,pickaxe,sword, 0
andaxe)
equipment 0
nearbyblocks 0
position 0
nearbyentities 5
fullinventory 7
otherblocksthatarerecentlyseen 10
biome 10
healthbar 15
hungerbar 15
time 15
additionalcontext 15
A.3.4 FullPrompt
Prompt1: Fullsystempromptforautomaticcurriculum. Thelistofquestion-answerpairsrepresents
theadditionalcontext.
You are a helpful assistant that tells me the next immediate task to
do in Minecraft. My ultimate goal is to discover as many diverse
things as possible, accomplish as many diverse tasks as possible
and become the best Minecraft player in the world.
I will give you the following information:
Question 1: ...
Answer: ...
Question 2: ...
Answer: ...
Question 3: ...
Answer: ...
...
Biome: ...
Time: ...
Nearby blocks: ...
Other blocks that are recently seen: ...
Nearby entities (nearest to farthest): ...
Health: Higher than 15 means I’m healthy.
Hunger: Higher than 15 means I’m not hungry.
Position: ...
Equipment: If I have better armor in my inventory, you should ask me
to equip it.
Inventory (xx/36): ...
Chests: You can ask me to deposit or take items from these chests.
There also might be some unknown chest, you should ask me to open
and check items inside the unknown chest.
Completed tasks so far: ...
Failed tasks that are too hard: ...
You must follow the following criteria:
1) You should act as a mentor and guide me to the next task based on
my current learning progress.
2) Please be very specific about what resources I need to collect,
what I need to craft, or what mobs I need to kill.
21
3) The next task should follow a concise format, such as "Mine [
quantity] [block]", "Craft [quantity] [item]", "Smelt [quantity] [
item]", "Kill [quantity] [mob]", "Cook [quantity] [food]", "Equip
[item]" etc. It should be a single phrase. Do not propose multiple
tasks at the same time. Do not mention anything else.
4) The next task should not be too hard since I may not have the
necessary resources or have learned enough skills to complete it
yet.
5) The next task should be novel and interesting. I should look for
rare resources, upgrade my equipment and tools using better
materials, and discover new things. I should not be doing the same
thing over and over again.
6) I may sometimes need to repeat some tasks if I need to collect more
resources to complete more difficult tasks. Only repeat tasks if
necessary.
7) Do not ask me to build or dig shelter even if it’s at night. I want
to explore the world and discover new things. I don’t want to
stay in one place.
8) Tasks that require information beyond the player’s status to verify
should be avoided. For instance, "Placing 4 torches" and "Dig a 2
x1x2 hole" are not ideal since they require visual confirmation
from the screen. All the placing, building, planting, and trading
tasks should be avoided. Do not propose task starting with these
keywords.
You should only respond in the format as described below:
RESPONSE FORMAT:
Reasoning: Based on the information I listed above, do reasoning about
what the next task should be.
Task: The next task.
Here’s an example response:
Reasoning: The inventory is empty now, chop down a tree to get some
wood.
Task: Obtain a wood log.
Prompt2: Fullsystempromptforaskingquestions. Weprovidebothgoodandbadexamplesas
few-shotexemplars.
You are a helpful assistant that asks questions to help me decide the
next immediate task to do in Minecraft. My ultimate goal is to
discover as many things as possible, accomplish as many tasks as
possible and become the best Minecraft player in the world.
I will give you the following information:
Biome: ...
Time: ...
Nearby blocks: ...
Other blocks that are recently seen: ...
Nearby entities (nearest to farthest): ...
Health: ...
Hunger: ...
Position: ...
Equipment: ...
Inventory (xx/36): ...
Chests: ...
Completed tasks so far: ...
Failed tasks that are too hard: ...
You must follow the following criteria:
1) You should ask at least 5 questions (but no more than 10 questions)
to help me decide the next immediate task to do. Each question
should be followed by the concept that the question is about.
2) Your question should be specific to a concept in Minecraft.
Bad example (the question is too general):
22
Question: What is the best way to play Minecraft?
Concept: unknown
Bad example (axe is still general, you should specify the type of
axe such as wooden axe):
What are the benefits of using an axe to gather resources?
Concept: axe
Good example:
Question: How to make a wooden pickaxe?
Concept: wooden pickaxe
3) Your questions should be self-contained and not require any context
.
Bad example (the question requires the context of my current biome):
Question: What are the blocks that I can find in my current biome?
Concept: unknown
Bad example (the question requires the context of my current
inventory):
Question: What are the resources you need the most currently?
Concept: unknown
Bad example (the question requires the context of my current
inventory):
Question: Do you have any gold or emerald resources?
Concept: gold
Bad example (the question requires the context of my nearby entities
):
Question: Can you see any animals nearby that you can kill for
food?
Concept: food
Bad example (the question requires the context of my nearby blocks):
Question: Is there any water source nearby?
Concept: water
Good example:
Question: What are the blocks that I can find in the sparse jungle
?
Concept: sparse jungle
4) Do not ask questions about building tasks (such as building a
shelter) since they are too hard for me to do.
Let’s say your current biome is sparse jungle. You can ask questions
like:
Question: What are the items that I can find in the sparse jungle?
Concept: sparse jungle
Question: What are the mobs that I can find in the sparse jungle?
Concept: sparse jungle
Let’s say you see a creeper nearby, and you have not defeated a
creeper before. You can ask a question like:
Question: How to defeat the creeper?
Concept: creeper
Let’s say you last completed task is "Craft a wooden pickaxe". You can
ask a question like:
Question: What are the suggested tasks that I can do after crafting a
wooden pickaxe?
Concept: wooden pickaxe
Here are some more question and concept examples:
Question: What are the ores that I can find in the sparse jungle?
Concept: sparse jungle
(the above concept should not be "ore" because I need to look up the
page of "sparse jungle" to find out what ores I can find in the
sparse jungle)
Question: How can you obtain food in the sparse jungle?
Concept: sparse jungle
23
(the above concept should not be "food" because I need to look up the
page of "sparse jungle" to find out what food I can obtain in the
sparse jungle)
Question: How can you use the furnace to upgrade your equipment and
make useful items?
Concept: furnace
Question: How to obtain a diamond ore?
Concept: diamond ore
Question: What are the benefits of using a stone pickaxe over a wooden
pickaxe?
Concept: stone pickaxe
Question: What are the tools that you can craft using wood planks and
sticks?
Concept: wood planks
You should only respond in the format as described below:
RESPONSE FORMAT:
Reasoning: ...
Question 1: ...
Concept 1: ...
Question 2: ...
Concept 2: ...
Question 3: ...
Concept 3: ...
Question 4: ...
Concept 4: ...
Question 5: ...
Concept 5: ...
...
Prompt3: Fullsystempromptforansweringquestions. Contextrepresentstheoptionalcontentfrom
awikiknowledgebase.
You are a helpful assistant that answer my question about Minecraft.
I will give you the following information:
Question: ...
You will answer the question based on the context (only if available
and helpful) and your own knowledge of Minecraft.
1) Start your answer with "Answer: ".
2) Answer "Answer: Unknown" if you don’t know the answer.
A.4 SkillLibrary
A.4.1 ComponentsinthePrompt
TheinputprompttoGPT-4consistsofthefollowingcomponents:
(1) Guidelinesforcodegeneration: SeeSecA.4.2forthefullprompt;
(2) ControlprimitiveAPIsimplementedbyus: TheseAPIsserveadualpurpose: theydemon-
stratetheusageofMineflayerAPIs,andtheycanbedirectlycalledbyGPT-4.
• exploreUntil(bot, direction, maxTime = 60, callback): Allowtheagent
toexploreinafixeddirectionformaxTime. Thecallbackisthestoppingcondition
implementedbytheagenttodeterminewhentostopexploring;
• mineBlock(bot, name, count = 1): Mine and collect the specified number of
blockswithina32-blockdistance;
• craftItem(bot, name, count = 1): Crafttheitemwithacraftingtablenearby;
• placeItem(bot, name, position): Placetheblockatthespecifiedposition;
• smeltItem(bot, itemName, fuelName, count = 1): Smelt the item with the
specifiedfuel. Theremustbeafurnacenearby;
24
• killMob(bot, mobName, timeout = 300): Attack the mob and collect its
droppeditem;
• getItemFromChest(bot, chestPosition, itemsToGet): Movetothechestat
thespecifiedpositionandgetitemsfromthechest;
• depositItemIntoChest(bot, chestPosition, itemsToDeposit): Move to
thechestatthespecifiedpositionanddeposititemsintothechest;
(3) ControlprimitiveAPIsprovidedbyMineflayer:
• await bot.pathfinder.goto(goal): Gotoaspecificposition. Seebelowforhow
tosetthegoal;
• new GoalNear(x, y, z, range): Move the bot to a block within the specified
rangeofthespecifiedblock;
• new GoalXZ(x, z): Forlong-rangegoalsthatdon’thaveaspecificYlevel;
• new GoalGetToBlock(x, y, z): Notgetintotheblock,butgetdirectlyadjacent
toit. Usefulforfishing,farming,fillingabucket,andusingabed.;
• new GoalFollow(entity, range): Followthespecifiedentitywithinthespecified
range;
• new GoalPlaceBlock(position, bot.world, {}): Positionthebotinorderto
placeablock;
• new GoalLookAtBlock(position, bot.world, {}): Path towards a position
whereafaceoftheblockatpositionisvisible;
• bot.isABed(bedBlock): ReturntrueifbedBlockisabed;
• bot.blockAt(position): Returntheblockatposition;
• await bot.equip(item, destination): Equiptheiteminthespecifieddestina-
tion. destinationmustbeoneof“hand”,“head”,“torso”,“legs”,“feet”,“off-hand”;
• await bot.consume(): Consumetheiteminthebot’shand. Youmustequipthe
itemtoconsumefirst. Usefulforeatingfood,drinkingpotions,etc.;
• await bot.fish(): Letbotfish. Beforecallingthisfunction,youmustfirstgettoa
waterblockandthenequipafishingrod. Thebotwillautomaticallystopfishingwhen
itcatchesafish;
• await bot.sleep(bedBlock): Sleep until sunrise. You must get to a bed block
first;
• await bot.activateBlock(block): Thisisthesameasright-clickingablockin
thegame. Usefulforbuttons,doors,etc. Youmustgettotheblockfirst;
• await bot.lookAt(position): Lookatthespecifiedposition. Youmustgonear
thepositionbeforeyoulookatit. Tofillabucketwithwater,youmustlookatitfirst;
• await bot.activateItem(): Thisisthesameasright-clickingtousetheitemin
thebot’shand. Usefulforusingabucket,etc. Youmustequiptheitemtoactivatefirst;
• await bot.useOn(entity): Thisisthesameasright-clickinganentityinthegame.
Usefulforshearingasheep. Youmustgettotheentityfirst;
(4) Retrievedskillsfromtheskilllibrary;
(5) Generatedcodefromthelastround;
(6) Environmentfeedback: Thechatlogintheprompt;
(7) Executionerrors;
(8) Critiquefromtheself-verificationmodule;
(9) Theagent’scurrentstate: SeeSec.A.3.1foreachelementoftheagent’sstate;
(10) Taskproposedbytheautomaticcurriculum;
(11) Taskcontext: WepromptGPT-3.5toaskforgeneralsuggestionsabouthowtosolvethe
task. Inpractice,thispartishandledbytheautomaticcurriculumsinceithasasystematic
mechanismforquestion-answering(Sec.A.3.2);
(12) Chain-of-thoughtprompting[46]inresponse: WeaskGPT-4tofirstexplainthereasonwhy
thecodefromthelastroundfails,thengivestep-by-stepplanstofinishthetask,andfinally
generatecode. SeeSec.A.4.2forthefullprompt.
25
A.4.2 FullPrompt
Prompt4: Fullsystempromptforcodegeneration.
You are a helpful assistant that writes Mineflayer javascript code to
complete any Minecraft task specified by me.
Here are some useful programs written with Mineflayer APIs.
/*
Explore until find an iron_ore, use Vec3(0, -1, 0) because iron ores
are usually underground
await exploreUntil(bot, new Vec3(0, -1, 0), 60, () => {
const iron_ore = bot.findBlock({
matching: mcData.blocksByName["iron_ore"].id,
maxDistance: 32,
});
return iron_ore;
});
Explore until find a pig, use Vec3(1, 0, 1) because pigs are usually
on the surface
let pig = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () => {
const pig = bot.nearestEntity((entity) => {
return (
entity.name === "pig" &&
entity.position.distanceTo(bot.entity.position) < 32
);
});
return pig;
});
*/
async function exploreUntil(bot, direction, maxTime = 60, callback) {
/*
Implementation of this function is omitted.
direction: Vec3, can only contain value of -1, 0 or 1
maxTime: number, the max time for exploration
callback: function, early stop condition, will be called each
second, exploration will stop if return value is not null
Return: null if explore timeout, otherwise return the return value
of callback
*/
}
// Mine 3 cobblestone: mineBlock(bot, "stone", 3);
async function mineBlock(bot, name, count = 1) {
const blocks = bot.findBlocks({
matching: (block) => {
return block.name === name;
},
maxDistance: 32,
count: count,
});
const targets = [];
for (let i = 0; i < Math.min(blocks.length, count); i++) {
targets.push(bot.blockAt(blocks[i]));
}
await bot.collectBlock.collect(targets, { ignoreNoPath: true });
}
// Craft 8 oak_planks from 2 oak_log (do the recipe 2 times):
craftItem(bot, "oak_planks", 2);
26
// You must place a crafting table before calling this function
async function craftItem(bot, name, count = 1) {
const item = mcData.itemsByName[name];
const craftingTable = bot.findBlock({
matching: mcData.blocksByName.crafting_table.id,
maxDistance: 32,
});
await bot.pathfinder.goto(
new GoalLookAtBlock(craftingTable.position, bot.world)
);
const recipe = bot.recipesFor(item.id, null, 1, craftingTable)[0];
await bot.craft(recipe, count, craftingTable);
}
// Place a crafting_table near the player, Vec3(1, 0, 0) is just an
example, you shouldn’t always use that: placeItem(bot, "
crafting_table", bot.entity.position.offset(1, 0, 0));
async function placeItem(bot, name, position) {
const item = bot.inventory.findInventoryItem(mcData.itemsByName[
name].id);
// find a reference block
const faceVectors = [
new Vec3(0, 1, 0),
new Vec3(0, -1, 0),
new Vec3(1, 0, 0),
new Vec3(-1, 0, 0),
new Vec3(0, 0, 1),
new Vec3(0, 0, -1),
];
let referenceBlock = null;
let faceVector = null;
for (const vector of faceVectors) {
const block = bot.blockAt(position.minus(vector));
if (block?.name !== "air") {
referenceBlock = block;
faceVector = vector;
break;
}
}
// You must first go to the block position you want to place
await bot.pathfinder.goto(new GoalPlaceBlock(position, bot.world,
{}));
// You must equip the item right before calling placeBlock
await bot.equip(item, "hand");
await bot.placeBlock(referenceBlock, faceVector);
}
// Smelt 1 raw_iron into 1 iron_ingot using 1 oak_planks as fuel:
smeltItem(bot, "raw_iron", "oak_planks");
// You must place a furnace before calling this function
async function smeltItem(bot, itemName, fuelName, count = 1) {
const item = mcData.itemsByName[itemName];
const fuel = mcData.itemsByName[fuelName];
const furnaceBlock = bot.findBlock({
matching: mcData.blocksByName.furnace.id,
maxDistance: 32,
});
await bot.pathfinder.goto(
new GoalLookAtBlock(furnaceBlock.position, bot.world)
);
const furnace = await bot.openFurnace(furnaceBlock);
for (let i = 0; i < count; i++) {
await furnace.putFuel(fuel.id, null, 1);
27
await furnace.putInput(item.id, null, 1);
// Wait 12 seconds for the furnace to smelt the item
await bot.waitForTicks(12 * 20);
await furnace.takeOutput();
}
await furnace.close();
}
// Kill a pig and collect the dropped item: killMob(bot, "pig", 300);
async function killMob(bot, mobName, timeout = 300) {
const entity = bot.nearestEntity(
(entity) =>
entity.name === mobName &&
entity.position.distanceTo(bot.entity.position) < 32
);
await bot.pvp.attack(entity);
await bot.pathfinder.goto(
new GoalBlock(entity.position.x, entity.position.y, entity.
position.z)
);
}
// Get a torch from chest at (30, 65, 100): getItemFromChest(bot, new
Vec3(30, 65, 100), {"torch": 1});
// This function will work no matter how far the bot is from the chest
.
async function getItemFromChest(bot, chestPosition, itemsToGet) {
await moveToChest(bot, chestPosition);
const chestBlock = bot.blockAt(chestPosition);
const chest = await bot.openContainer(chestBlock);
for (const name in itemsToGet) {
const itemByName = mcData.itemsByName[name];
const item = chest.findContainerItem(itemByName.id);
await chest.withdraw(item.type, null, itemsToGet[name]);
}
await closeChest(bot, chestBlock);
}
// Deposit a torch into chest at (30, 65, 100): depositItemIntoChest(
bot, new Vec3(30, 65, 100), {"torch": 1});
// This function will work no matter how far the bot is from the chest
.
async function depositItemIntoChest(bot, chestPosition, itemsToDeposit
) {
await moveToChest(bot, chestPosition);
const chestBlock = bot.blockAt(chestPosition);
const chest = await bot.openContainer(chestBlock);
for (const name in itemsToDeposit) {
const itemByName = mcData.itemsByName[name];
const item = bot.inventory.findInventoryItem(itemByName.id);
await chest.deposit(item.type, null, itemsToDeposit[name]);
}
await closeChest(bot, chestBlock);
}
// Check the items inside the chest at (30, 65, 100):
checkItemInsideChest(bot, new Vec3(30, 65, 100));
// You only need to call this function once without any action to
finish task of checking items inside the chest.
async function checkItemInsideChest(bot, chestPosition) {
await moveToChest(bot, chestPosition);
const chestBlock = bot.blockAt(chestPosition);
await bot.openContainer(chestBlock);
// You must close the chest after opening it if you are asked to
open a chest
28
await closeChest(bot, chestBlock);
}
await bot.pathfinder.goto(goal); // A very useful function. This
function may change your main-hand equipment.
// Following are some Goals you can use:
new GoalNear(x, y, z, range); // Move the bot to a block within the
specified range of the specified block. ‘x‘, ‘y‘, ‘z‘, and ‘range‘
are ‘number‘
new GoalXZ(x, z); // Useful for long-range goals that don’t have a
specific Y level. ‘x‘ and ‘z‘ are ‘number‘
new GoalGetToBlock(x, y, z); // Not get into the block, but get
directly adjacent to it. Useful for fishing, farming, filling
bucket, and beds. ‘x‘, ‘y‘, and ‘z‘ are ‘number‘
new GoalFollow(entity, range); // Follow the specified entity within
the specified range. ‘entity‘ is ‘Entity‘, ‘range‘ is ‘number‘
new GoalPlaceBlock(position, bot.world, {}); // Position the bot in
order to place a block. ‘position‘ is ‘Vec3‘
new GoalLookAtBlock(position, bot.world, {}); // Path into a position
where a blockface of the block at position is visible. ‘position‘
is ‘Vec3‘
// These are other Mineflayer functions you can use:
bot.isABed(bedBlock); // Return true if ‘bedBlock‘ is a bed
bot.blockAt(position); // Return the block at ‘position‘. ‘position‘
is ‘Vec3‘
// These are other Mineflayer async functions you can use:
await bot.equip(item, destination); // Equip the item in the specified
destination. ‘item‘ is ‘Item‘, ‘destination‘ can only be "hand",
"head", "torso", "legs", "feet", "off-hand"
await bot.consume(); // Consume the item in the bot’s hand. You must
equip the item to consume first. Useful for eating food, drinking
potions, etc.
await bot.fish(); // Let bot fish. Before calling this function, you
must first get to a water block and then equip a fishing rod. The
bot will automatically stop fishing when it catches a fish
await bot.sleep(bedBlock); // Sleep until sunrise. You must get to a
bed block first
await bot.activateBlock(block); // This is the same as right-clicking
a block in the game. Useful for buttons, doors, using hoes, etc.
You must get to the block first
await bot.lookAt(position); // Look at the specified position. You
must go near the position before you look at it. To fill bucket
with water, you must lookAt first. ‘position‘ is ‘Vec3‘
await bot.activateItem(); // This is the same as right-clicking to use
the item in the bot’s hand. Useful for using buckets, etc. You
must equip the item to activate first
await bot.useOn(entity); // This is the same as right-clicking an
entity in the game. Useful for shearing sheep, equipping harnesses
, etc. You must get to the entity first
{retrieved_skills}
At each round of conversation, I will give you
Code from the last round: ...
Execution error: ...
Chat log: ...
Biome: ...
Time: ...
Nearby blocks: ...
Nearby entities (nearest to farthest):
Health: ...
29
Hunger: ...
Position: ...
Equipment: ...
Inventory (xx/36): ...
Chests: ...
Task: ...
Context: ...
Critique: ...
You should then respond to me with
Explain (if applicable): Are there any steps missing in your plan? Why
does the code not complete the task? What does the chat log and
execution error imply?
Plan: How to complete the task step by step. You should pay attention
to Inventory since it tells what you have. The task completeness
check is also based on your final inventory.
Code:
1) Write an async function taking the bot as the only argument.
2) Reuse the above useful programs as much as possible.
- Use ‘mineBlock(bot, name, count)‘ to collect blocks. Do not
use ‘bot.dig‘ directly.
- Use ‘craftItem(bot, name, count)‘ to craft items. Do not use
‘bot.craft‘ directly.
- Use ‘smeltItem(bot, name count)‘ to smelt items. Do not use
‘bot.openFurnace‘ directly.
- Use ‘placeItem(bot, name, position)‘ to place blocks. Do not
use ‘bot.placeBlock‘ directly.
- Use ‘killMob(bot, name, timeout)‘ to kill mobs. Do not use ‘
bot.attack‘ directly.
3) Your function will be reused for building more complex
functions. Therefore, you should make it generic and reusable. You
should not make strong assumption about the inventory (as it may
be changed at a later time), and therefore you should always check
whether you have the required items before using them. If not,
you should first collect the required items and reuse the above
useful programs.
4) Functions in the "Code from the last round" section will not be
saved or executed. Do not reuse functions listed there.
5) Anything defined outside a function will be ignored, define all
your variables inside your functions.
6) Call ‘bot.chat‘ to show the intermediate progress.
7) Use ‘exploreUntil(bot, direction, maxDistance, callback)‘ when
you cannot find something. You should frequently call this before
mining blocks or killing mobs. You should select a direction at
random every time instead of constantly using (1, 0, 1).
8) ‘maxDistance‘ should always be 32 for ‘bot.findBlocks‘ and ‘bot
.findBlock‘. Do not cheat.
9) Do not write infinite loops or recursive functions.
10) Do not use ‘bot.on‘ or ‘bot.once‘ to register event listeners.
You definitely do not need them.
11) Name your function in a meaningful way (can infer the task
from the name).
You should only respond in the format as described below:
RESPONSE FORMAT:
Explain: ...
Plan:
1) ...
2) ...
3) ...
...
Code:
‘‘‘javascript
// helper functions (only if needed, try to avoid them)
...
30
// main function after the helper functions
async function yourMainFunctionName(bot) {
// ...
}
‘‘‘
Prompt5: Fullsystempromptforgeneratingfunctiondescriptions. Thisisusedwhenaddinganew
skilltotheskilllibrary. Wegiveaone-shotexampleintheprompt.
You are a helpful assistant that writes a description of the given
function written in Mineflayer javascript code.
1) Do not mention the function name.
2) Do not mention anything about ‘bot.chat‘ or helper functions.
3) There might be some helper functions before the main function, but
you only need to describe the main function.
4) Try to summarize the function in no more than 6 sentences.
5) Your response should be a single line of text.
For example, if the function is:
async function mineCobblestone(bot) {
// Check if the wooden pickaxe is in the inventory, if not, craft
one
let woodenPickaxe = bot.inventory.findInventoryItem(mcData.
itemsByName["wooden_pickaxe"].id);
if (!woodenPickaxe) {
bot.chat("Crafting a wooden pickaxe.");
await craftWoodenPickaxe(bot);
woodenPickaxe = bot.inventory.findInventoryItem(mcData.itemsByName
["wooden_pickaxe"].id);
}
// Equip the wooden pickaxe if it exists
if (woodenPickaxe) {
await bot.equip(woodenPickaxe, "hand");
// Explore until we find a stone block
await exploreUntil(bot, new Vec3(1, -1, 1), 60, () => {
const stone = bot.findBlock({
matching: mcData.blocksByName["stone"].id,
maxDistance: 32
});
if (stone) {
return true;
}
});
// Mine 8 cobblestone blocks using the wooden pickaxe
bot.chat("Found a stone block. Mining 8 cobblestone blocks.");
await mineBlock(bot, "stone", 8);
bot.chat("Successfully mined 8 cobblestone blocks.");
// Save the event of mining 8 cobblestone
bot.save("cobblestone_mined");
} else {
bot.chat("Failed to craft a wooden pickaxe. Cannot mine
cobblestone.");
}
}
The main function is ‘mineCobblestone‘.
Then you would write:
31
The function is about mining 8 cobblestones using a wooden pickaxe.
First check if a wooden pickaxe is in the inventory. If not, craft
one. If the wooden pickaxe is available, equip the wooden pickaxe
in the hand. Next, explore the environment until finding a stone
block. Once a stone block is found, mine a total of 8 cobblestone
blocks using the wooden pickaxe.
A.4.3 Examples
Skilllibraryexample1: craftWoodenPlanks.
async function craftWoodenPlanks(bot) {
const logNames = ["oak_log", "birch_log", "spruce_log", "jungle_log"
, "acacia_log", "dark_oak_log", "mangrove_log"];
const plankNames = ["oak_planks", "birch_planks", "spruce_planks", "
jungle_planks", "acacia_planks", "dark_oak_planks", "
mangrove_planks"];
const logInInventory = logNames.find(logName => bot.inventory.count(
mcData.itemsByName[logName].id) > 0);
if (!logInInventory) {
bot.chat("No wooden log in inventory. Mining a wooden log...");
await mineWoodLog(bot);
}
const logIndex = logNames.indexOf(logInInventory);
const plankName = plankNames[logIndex];
bot.chat(‘Crafting 4 ${plankName}...‘);
await craftItem(bot, plankName, 1);
bot.chat(‘4 ${plankName} crafted.‘);
}
Skilllibraryexample2: mineTenCobbledDeepslateBelowY0.
async function mineTenCobbledDeepslateBelowY0(bot) {
// Equip the iron pickaxe
const ironPickaxe = bot.inventory.findInventoryItem(mcData.
itemsByName["iron_pickaxe"].id);
await bot.equip(ironPickaxe, "hand");
// Find cobbled_deepslate blocks below Y=0
const cobbledDeepslateBlocks = await exploreUntil(bot, new Vec3(1,
-1, 1), 60, () => {
const cobbledDeepslate = bot.findBlock({
matching: mcData.blocksByName["cobbled_deepslate"].id,
maxDistance: 32,
position: pos => pos.y < 0
});
return cobbledDeepslate;
});
// Mine 10 cobbled_deepslate blocks
await mineBlock(bot, "cobbled_deepslate", 10);
bot.chat("10 cobbled_deepslate mined below Y=0.");
}
Skilllibraryexample3: smeltFiveRawIronV2.
async function findSuitablePosition(bot) {
const offsets = [new Vec3(1, 0, 0), new Vec3(-1, 0, 0), new Vec3(0,
0, 1), new Vec3(0, 0, -1)];
for (const offset of offsets) {
const position = bot.entity.position.offset(offset.x, offset.y,
offset.z);
const block = bot.blockAt(position);
32
if (block.name === "air") {
return position;
}
}
return null;
}
async function smeltFiveRawIron(bot) {
// Check if there is a furnace in the inventory
const furnaceItem = bot.inventory.findInventoryItem(mcData.
itemsByName.furnace.id);
// If not, craft a furnace using the available cobblestone
if (!furnaceItem) {
await craftFurnace(bot);
}
// Find a suitable position to place the furnace
const furnacePosition = await findSuitablePosition(bot);
if (!furnacePosition) {
bot.chat("Could not find a suitable position to place the furnace.
");
return;
}
// Place the furnace at the suitable position
await placeItem(bot, "furnace", furnacePosition);
// Smelt 5 raw iron using the available coal as fuel
await smeltItem(bot, "raw_iron", "coal", 5);
bot.chat("5 raw iron smelted.");
}
Skilllibraryexample4: fillBucketWithWater.
async function fillBucketWithWater(bot) {
// Find a water block nearby
const waterBlock = await exploreUntil(bot, new Vec3(1, 0, 1), 60, ()
=> {
const water = bot.findBlock({
matching: mcData.blocksByName.water.id,
maxDistance: 32
});
return water;
});
if (!waterBlock) {
bot.chat("Could not find water.");
return;
}
// Go to the water block
const adjacentBlock= waterBlock.position.offset(0, 1, 0);
await bot.pathfinder.goto(
new GoalGetToBlock(adjacentBlock.x, adjacentBlock.y,
adjacentBlock.z)
);
// Look at the water block
await bot.lookAt(waterBlock.position, true);
// Equip the bucket
const bucket = bot.inventory.findInventoryItem(mcData.itemsByName.
bucket.id);
await bot.equip(bucket, "hand");
33
// Activate the bucket to collect water
await bot.activateItem();
bot.chat("Filled the bucket with water.");
}
Skilllibraryexample5: catchFiveFishSafely.
async function catchFiveFishSafely(bot) {
// Check if the bot has a fishing rod in its inventory
let fishingRod = bot.inventory.findInventoryItem(mcData.itemsByName.
fishing_rod.id);
if (!fishingRod) {
await craftFishingRod(bot);
fishingRod = bot.inventory.findInventoryItem(mcData.itemsByName.
fishing_rod.id);
}
// Find a nearby water block
let waterBlock;
while (!waterBlock) {
waterBlock = await exploreUntil(bot, new Vec3(1, 0, 1), 60, () =>
{
const foundWaterBlock = bot.findBlock({
matching: mcData.blocksByName.water.id,
maxDistance: 32
});
return foundWaterBlock;
});
if (!waterBlock) {
bot.chat("No path to the water block. Trying to find another
water block...");
}
}
// Move to a block adjacent to the water block
const adjacentBlock = waterBlock.position.offset(0, 1, 0);
await bot.pathfinder.goto(new GoalBlock(adjacentBlock.x,
adjacentBlock.y, adjacentBlock.z));
// Look at the water block
await bot.lookAt(waterBlock.position);
// Equip the fishing rod
await bot.equip(fishingRod, "hand");
// Fish in the water 5 times
for (let i = 0; i < 5; i++) {
try {
await bot.fish();
bot.chat(‘Fish ${i + 1} caught.‘);
} catch (error) {
if (error.message === "Fishing cancelled") {
bot.chat("Fishing was cancelled. Trying again...");
i--; // Retry the same iteration
} else {
throw error;
}
}
}
}
34
A.5 Self-Verification
A.5.1 ComponentsinthePrompt
TheinputprompttoGPT-4consistsofthefollowingcomponents:
(1) Theagent’sstate:Weexcludeotherblocksthatarerecentlyseenandnearbyentitiesfromthe
agent’sstatesincetheyarenotusefulforassessingthetask’scompleteness. SeeSec.A.3.1
foreachelementoftheagent’sstate;
(2) Taskproposedbytheautomaticcurriculum;
(3) Taskcontext: WepromptGPT-3.5toaskforgeneralsuggestionsabouthowtosolvethe
task. Inpractice,thispartishandledbytheautomaticcurriculumsinceithasasystematic
mechanismforquestion-answering(Sec.A.3.2);
(4) Chain-of-thoughtprompting[46]inresponse: WerequestGPT-4toinitiallyreasonabout
thetask’ssuccessorfailure,thenoutputabooleanvariableindicatingthetask’soutcome,
andfinallyprovideacritiquetotheagentifthetaskfails.
(5) Few-shotexamplesforin-contextlearning[36–38].
A.5.2 FullPrompt
Prompt6: Fullsystempromptforself-verification.
You are an assistant that assesses my progress of playing Minecraft
and provides useful guidance.
You are required to evaluate if I have met the task requirements.
Exceeding the task requirements is also considered a success while
failing to meet them requires you to provide critique to help me
improve.
I will give you the following information:
Biome: The biome after the task execution.
Time: The current time.
Nearby blocks: The surrounding blocks. These blocks are not collected
yet. However, this is useful for some placing or planting tasks.
Health: My current health.
Hunger: My current hunger level. For eating task, if my hunger level
is 20.0, then I successfully ate the food.
Position: My current position.
Equipment: My final equipment. For crafting tasks, I sometimes equip
the crafted item.
Inventory (xx/36): My final inventory. For mining and smelting tasks,
you only need to check inventory.
Chests: If the task requires me to place items in a chest, you can
find chest information here.
Task: The objective I need to accomplish.
Context: The context of the task.
You should only respond in JSON format as described below:
{
"reasoning": "reasoning",
"success": boolean,
"critique": "critique",
}
Ensure the response can be parsed by Python ‘json.loads‘, e.g.: no
trailing commas, no single quotes, etc.
Here are some examples:
INPUT:
Inventory (2/36): {’oak_log’:2, ’spruce_log’:2}
35
Task: Mine 3 wood logs
RESPONSE:
{
"reasoning": "You need to mine 3 wood logs. You have 2 oak logs
and 2 spruce logs, which add up to 4 wood logs.",
"success": true,
"critique": ""
}
INPUT:
Inventory (3/36): {’crafting_table’: 1, ’spruce_planks’: 6, ’stick’:
4}
Task: Craft a wooden pickaxe
RESPONSE:
{
"reasoning": "You have enough materials to craft a wooden pickaxe,
but you didn’t craft it.",
"success": false,
"critique": "Craft a wooden pickaxe with a crafting table using 3
spruce planks and 2 sticks."
}
INPUT:
Inventory (2/36): {’raw_iron’: 5, ’stone_pickaxe’: 1}
Task: Mine 5 iron_ore
RESPONSE:
{
"reasoning": "Mining iron_ore in Minecraft will get raw_iron. You
have 5 raw_iron in your inventory.",
"success": true,
"critique": ""
}
INPUT:
Biome: plains
Nearby blocks: stone, dirt, grass_block, grass, farmland, wheat
Inventory (26/36): ...
Task: Plant 1 wheat seed.
RESPONSE:
{
"reasoning": "For planting tasks, inventory information is useless
. In nearby blocks, there is farmland and wheat, which means you
succeed to plant the wheat seed.",
"success": true,
"critique": ""
}
INPUT:
Inventory (11/36): {... ,’rotten_flesh’: 1}
Task: Kill 1 zombie
Context: ...
RESPONSE
{
36
"reasoning": "You have rotten flesh in your inventory, which means
you successfully killed one zombie.",
"success": true,
"critique": ""
}
INPUT:
Hunger: 20.0/20.0
Inventory (11/36): ...
Task: Eat 1 ...
Context: ...
RESPONSE
{
"reasoning": "For all eating task, if the player’s hunger is 20.0,
then the player successfully ate the food.",
"success": true,
"critique": ""
}
INPUT:
Nearby blocks: chest
Inventory (28/36): {’rail’: 1, ’coal’: 2, ’oak_planks’: 13, ’
copper_block’: 1, ’diorite’: 7, ’cooked_beef’: 4, ’granite’: 22, ’
cobbled_deepslate’: 23, ’feather’: 4, ’leather’: 2, ’
cooked_chicken’: 3, ’white_wool’: 2, ’stick’: 3, ’black_wool’: 1,
’stone_sword’: 2, ’stone_hoe’: 1, ’stone_axe’: 2, ’stone_shovel’:
2, ’cooked_mutton’: 4, ’cobblestone_wall’: 18, ’crafting_table’:
1, ’furnace’: 1, ’iron_pickaxe’: 1, ’stone_pickaxe’: 1, ’
raw_copper’: 12}
Chests:
(81, 131, 16): {’andesite’: 2, ’dirt’: 2, ’cobblestone’: 75, ’
wooden_pickaxe’: 1, ’wooden_sword’: 1}
Task: Deposit useless items into the chest at (81, 131, 16)
Context: ...
RESPONSE
{
"reasoning": "You have 28 items in your inventory after depositing
, which is more than 20. You need to deposit more items from your
inventory to the chest.",
"success": false,
"critique": "Deposit more useless items such as copper_block,
diorite, granite, cobbled_deepslate, feather, and leather to meet
the requirement of having only 20 occupied slots in your inventory
."
}
A.6 System-levelComparisonbetweenVOYAGERandPriorWorks
Wemakeasystem-levelcomparisoninTable.A.2. Voyagerstandsoutastheonlymethodfeaturinga
combinationofautomaticcurriculum,iterativeplanning,andaskilllibrary. Moreover,itlearnsto
playMinecraftwithouttheneedforanygradientupdate.
37
TableA.2: System-levelcomparisonbetweenVOYAGERandpriorworks.
VPT[8] DreamerV3[69] DECKARD[53]DEPS[55] Plan4MC[71] VOYAGER
Demos Videos None Videos None None None
Rewards Sparse Dense Sparse None Dense None
Observations PixelsOnly Pixels& Pixels& Feedback& Pixels& Feedback&
Meta Inventory Inventory Meta Meta&
Inventory
Actions Keyboard & Discrete Keyboard & Keyboard & Discrete Code
Mouse Mouse Mouse
Automatic ✓ ✓
Curriculum (in-context
GPT-4 pro-
posal)
IterativePlan- ✓ ✓
ning (3 types of
feedback)
SkillLibrary ✓ ✓
(pre-defined) (self-
generated)
Gradient-Free ✓
B Experiments
B.1 ExperimentalSetup
OursimulationenvironmentisbuiltuponMineDojo[23]andutilizesMineflayer[52]JavaScriptAPIs
formotorcontrols(Sec.A.4.2). Additionally,weincorporatemanybot.chat()intoMineflayer
functionstoprovideabundantenvironmentfeedbackandimplementvariousconditionchecksalong
withtry-catchexceptionsforcontinuousexecution. Ifthebotdies,itisresurrectedneartheclosest
ground,anditsinventoryispreservedforuninterruptedexploration. Thebotrecyclesitscraftingtable
andfurnaceafterprogramexecution. Fordetailedimplementations,pleaserefertoourcodebase.
B.2 Baselines
ReAct[29]useschain-of-thoughtprompting[46]bygeneratingbothreasoningtracesandaction
planswithLLMs. Weprovideitwithourenvironmentfeedbackandtheagentstatesasobservations.
ReAct undergoes one round of code generation from scratch, followed by three rounds of code
refinement. Thisprocessisthenrepeateduntilthemaximumpromptingiterationisreached.
Reflexion[30]isbuiltontopofReAct[29]withself-reflectiontoinfermoreintuitivefutureactions.
Weprovideitwithenvironmentfeedback,theagentstates,executionerrors,andourself-verification
module. SimilartoReAct,Reflexionundergoesoneroundofcodegenerationfromscratch,followed
bythreeroundsofcoderefinement. Thisprocessisthenrepeateduntilthemaximumprompting
iterationisreached.
AutoGPT[28]isapopularsoftwaretoolthatautomatesNLPtasksbydecomposingahigh-levelgoal
intomultiplesubgoalsandexecutingtheminaReAct-styleloop. Were-implementAutoGPTby
usingGPT-4todotaskdecompositionandprovideitwiththeagentstates,environmentfeedback,
andexecutionerrorsasobservationsforsubgoalexecution. ComparedwithVOYAGER,AutoGPT
lackstheskilllibraryforaccumulatingknowledge,self-verificationforassessingtasksuccess,and
automaticcurriculumforopen-endedexploration. Duringeachsubgoalexecution,ifnoexecution
erroroccurs,weconsiderthesubgoalcompletedandproceedtothenextone. Otherwise,werefine
theprogramuntilthreeroundsofcoderefinement(equivalenttofourroundsofcodegeneration)
arecompleted,andthenmoveontothenextsubgoal. Ifthreeconsecutivesubgoalsdonotresultin
acquiringanewitem,wereplanbyrerunningthetaskdecomposition.
Thetaskis“exploretheworldandgetasmanyitemsaspossible”forallbaselines.
38
TableA.3: ComparisonbetweenVOYAGERandbaselines.
ReAct[29] Reflexion[30] AutoGPT[28] VOYAGER
Chain-of-Thought[46] ✓ ✓ ✓ ✓
SelfVerification ✓ ✓
EnvironmentFeedback ✓ ✓ ✓ ✓
ExecutionErrors ✓ ✓ ✓
AgentState ✓ ✓ ✓ ✓
SkillLibrary ✓
AutomaticCurriculum ✓
FigureA.1: Minecraftitemiconswithcorrespondingnames.
B.3 Ablations
Weablate6designchoices(automaticcurriculum,skilllibrary,environmentfeedback,execution
errors, self-verification, and GPT-4 for code generation) in VOYAGER and study their impact on
explorationperformance.
• ManualCurriculum: Wesubstitutetheautomaticcurriculumwithamanuallydesigned
curriculum for mining a diamond: “Mine 3 wood log”, “Craft 1 crafting table”, “Craft
1woodenpickaxe”, “Mine11cobblestone”, “Craft1stonepickaxe”, “Craft1furnace”,
“Mine3ironore”,“Smelt3ironore”,“Craft1ironpickaxe”,“Mine1diamond”. Amanual
curriculumrequireshumanefforttodesignandisnotscalableforopen-endedexploration.
• RandomCurriculum: Wecurate101itemsobtainedbyVOYAGERandcreatearandom
curriculumbyrandomlyselectingoneitemasthenexttask.
• w/oSkillLibrary:Weremovetheskilllibrary,eliminatingskillretrievalforcodegeneration.
• w/oEnvironmentFeedback: Weexcludeenvironmentfeedback(chatlog)fromtheprompt
forcodegeneration.
• w/oExecutionErrors: Weexcludeexecutionerrorsfromthepromptforcodegeneration.
• w/o Self-Verification: For each task, we generate code without self-verification and it-
eratively refine the program for 3 rounds (equivalent to 4 rounds of code generation in
total).
• GPT-3.5: WereplaceGPT-4withGPT-3.5forcodegeneration. WeretainGPT-4forthe
automaticcurriculumandtheself-verificationmodule.
B.4 EvaluationResults
B.4.1 SignificantlyBetterExploration
ThemeaningofeachiconinFig.1isshowninFig.A.1.
Werunthreetrialsforeachmethod. TheitemscollectedbyVOYAGERineachtrialis
39
• Trial 1: ‘iron_ingot’, ‘stone_shovel’, ‘iron_leggings’, ‘fishing_rod’, ‘pufferfish’,
‘oak_log’, ‘cooked_mutton’, ‘green_dye’, ‘flint’, ‘chest’, ‘iron_sword’, ‘string’, ‘en-
der_pearl’, ‘raw_copper’, ‘crafting_table’, ‘cactus’, ‘lapis_lazuli’, ‘iron_pickaxe’, ‘cop-
per_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘scaffolding’, ‘stick’, ‘porkchop’, ‘cop-
per_block’, ‘gravel’, ‘grass_block’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’,
‘oak_sapling’, ‘coal’, ‘bamboo’, ‘wooden_pickaxe’, ‘rotten_flesh’, ‘cooked_porkchop’,
‘cod’,‘iron_boots’,‘lightning_rod’,‘diorite’,‘water_bucket’,‘shears’,‘furnace’,‘andesite’,
‘granite’,‘bucket’,‘wooden_sword’,‘sandstone’,‘iron_helmet’,‘raw_iron’,‘sand’,‘aca-
cia_log’,‘cooked_cod’,‘oak_planks’,‘azure_bluet’,‘iron_shovel’,‘acacia_planks’,‘shield’,
‘iron_axe’,‘iron_chestplate’,‘cobblestone’;
• Trial2:‘iron_ingot’,‘tuff’,‘stone_shovel’,‘iron_leggings’,‘fishing_rod’,‘cooked_mutton’,
‘spruce_planks’, ‘gunpowder’, ‘amethyst_shard’, ‘chest’, ‘string’, ‘cooked_salmon’,
‘iron_sword’,‘raw_copper’,‘crafting_table’,‘torch’,‘lapis_lazuli’,‘iron_pickaxe’,‘cop-
per_ingot’, ‘stone_pickaxe’, ‘wooden_hoe’, ‘stick’, ‘amethyst_block’, ‘salmon’, ‘cal-
cite’, ‘gravel’, ‘white_bed’, ‘bone’, ‘dirt’, ‘mutton’, ‘white_wool’, ‘spyglass’, ‘coal’,
‘wooden_pickaxe’, ‘cod’, ‘iron_boots’, ‘lily_pad’, ‘cobbled_deepslate’, ‘lightning_rod’,
‘snowball’,‘stone_axe’,‘smooth_basalt’,‘diorite’,‘water_bucket’,‘furnace’,‘andesite’,
‘bucket’, ‘granite’, ‘shield’, ‘iron_helmet’, ‘raw_iron’, ‘cobblestone’, ‘spruce_log’,
‘cooked_cod’,‘tripwire_hook’,‘stone_hoe’,‘iron_chestplate’,‘stone_sword’;
• Trial 3: ‘spruce_planks’, ‘dirt’, ‘shield’, ‘redstone’, ‘clock’, ‘diamond_sword’,
‘iron_chestplate’, ‘stone_pickaxe’, ‘leather’, ‘string’, ‘chicken’, ‘chest’, ‘diorite’,
‘iron_leggings’, ‘black_wool’, ‘cobblestone_wall’, ‘cobblestone’, ‘cooked_chicken’,
‘feather’,‘stone_sword’,‘raw_gold’,‘gravel’,‘birch_planks’,‘coal’,‘cobbled_deepslate’,
‘oak_planks’,‘iron_pickaxe’,‘granite’,‘tuff’,‘crafting_table’,‘iron_helmet’,‘stone_hoe’,
‘iron_ingot’, ‘stone_axe’, ‘birch_boat’, ‘stick’, ‘sand’, ‘bone’, ‘raw_iron’, ‘beef’, ‘rail’,
‘oak_sapling’,‘kelp’,‘gold_ingot’,‘birch_log’,‘wheat_seeds’,‘cooked_mutton’,‘furnace’,
‘arrow’, ‘stone_shovel’, ‘white_wool’, ‘andesite’, ‘jungle_slab’, ‘mutton’, ‘iron_sword’,
‘copper_ingot’, ‘diamond’, ‘torch’, ‘oak_log’, ‘cooked_beef’, ‘copper_block’, ‘flint’,
‘bone_meal’,‘raw_copper’,‘wooden_pickaxe’,‘iron_boots’,‘wooden_sword’.
TheitemscollectedbyReAct[29]ineachtrialis
• Trial1: ‘bamboo’,‘dirt’,‘sand’,‘wheat_seeds’;
• Trial2: ‘dirt’,‘rabbit’,‘spruce_log’,‘spruce_sapling’;
• Trial3: ‘dirt’,‘pointed_dripstone’;
TheitemscollectedbyReflexion[30]ineachtrialis
• Trial1: ‘crafting_table’,‘orange_tulip’,‘oak_planks’,‘oak_log’,‘dirt’;
• Trial2: ‘spruce_log’,‘dirt’,‘clay_ball’,‘sand’,‘gravel’;
• Trial3: ‘wheat_seeds’,‘oak_log’,‘dirt’,‘birch_log’,‘sand’.
TheitemscollectedbyAutoGPT[28]ineachtrialis
• Trial 1: ‘feather’, ‘oak_log’, ‘leather’, ‘stick’, ‘porkchop’, ‘chicken’, ‘crafting_table’,
‘wheat_seeds’,‘oak_planks’,‘dirt’,‘mutton’;
• Trial 2: ‘wooden_pickaxe’, ‘iron_ingot’, ‘stone’, ‘coal’, ‘spruce_planks’, ‘string’,
‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘andesite’, ‘furnace’, ‘torch’, ‘spruce_sapling’,
‘granite’,‘iron_pickaxe’,‘stone_pickaxe’,‘wooden_axe’,‘raw_iron’,‘stick’,‘spruce_log’,
‘dirt’,‘cobblestone’;
• Trial3: ‘wooden_shovel’,‘wooden_pickaxe’,‘iron_ingot’,‘stone’,‘cod’,‘coal’,‘oak_log’,
‘flint’, ‘raw_copper’, ‘crafting_table’, ‘diorite’, ‘furnace’, ‘andesite’, ‘torch’, ‘granite’,
‘lapis_lazuli’,‘iron_pickaxe’,‘stone_pickaxe’,‘raw_iron’,‘stick’,‘gravel’,‘oak_planks’,
‘dirt’,‘iron_axe’,‘cobblestone’.
40
FigureA.2: Mapcoverage: Twobird’seyeviewsofMinecraftmaps. VOYAGERisabletotraverse
2.3×longerdistancescomparedtobaselineswhilecrossingdiverseterrains. Trajectoriesareplotted
basedonthepositionswhereeachagentinteractswithGPT-4.
B.4.2 ExtensiveMapTraversal
AgenttrajectoriesformapcoveragearedisplayedinFig.A.2. Fig.7isplottedbasedonFig.A.2by
drawingthesmallestcircleenclosingeachtrajectory. TheterrainstraversedbyVOYAGERineach
trialis
• Trial1: ‘meadow’,‘desert’,‘river’,‘savanna’,‘forest’,‘plains’,‘bamboo_jungle’,‘drip-
stone_caves’;
• Trial2: ‘snowy_plains’,‘frozen_river’,‘dripstone_caves’,‘snowy_taiga’,‘beach’;
• Trial 3: ‘flower_forest’, ‘meadow’, ‘old_growth_birch_forest’, ‘snowy_slopes’,
‘frozen_peaks’,‘forest’,‘river’,‘beach’,‘ocean’,‘sunflower_plains’,‘plains’,‘stony_shore’.
TheterrainstraversedbyReAct[29]ineachtrialis
• Trial1: ‘plains’,‘desert’,‘jungle’;
• Trial2: ‘snowy_plains’,‘snowy_taiga’,‘snowy_slopes’;
• Trial3: ‘dark_forest’,‘dripstone_caves’,‘grove’,‘jagged_peaks’.
TheterrainstraversedbyReflexion[30]ineachtrialis
• Trial1: ‘plains’,‘flower_forest’;
• Trial2: ‘snowy_taiga’;
• Trial3: ‘old_growth_birch_forest’,‘river’,‘ocean’,‘beach’,‘plains’.
TheterrainstraversedbyAutoGPT[28]ineachtrialis
• Trial1: ‘plains’,‘dripstone_caves’,‘savanna’,‘meadow’;
• Trial2: ‘snowy_taiga’;
• Trial3: ‘plains’,‘stony_shore’,‘forest’,‘ocean’.
B.4.3 EfficientZero-ShotGeneralizationtoUnseenTasks
Theresultsofzero-shotgeneralizationtounseentasksfortheothertwotasksarepresentedinFig.A.3.
SimilartoFig.8,VOYAGERconsistentlysolvesalltasks,whilethebaselinesareunabletosolveany
41
FigureA.3: Zero-shotgeneralizationtounseentasks. Wevisualizetheintermediateprogressofeach
methodontheothertwotasks. WedonotplotReActandReflexionsincetheydonotmakeany
meaningfulprogress.
taskwithin50promptingiterations. Ourskilllibrary,constructedfromlifelonglearning,notonly
enhancesVOYAGER’sperformancebutalsoprovidesaboosttoAutoGPT[28].
B.4.4 AccurateSkillRetrieval
Weconductanevaluationofourskillretrieval(309samplesintotal)andtheresultsareinTable.A.4.
Thetop-5accuracystandingat96.5%suggestsourretrievalprocessisreliable(notethatweinclude
thetop-5relevantskillsinthepromptforsynthesizinganewskill).
TableA.4: Skillretrievalaccuracy.
Top-1Acc Top-2Acc Top-3Acc Top-4Acc Top-5Acc
80.2±3.0 89.3±1.8 93.2±0.7 95.2±1.8 96.5±0.3
B.4.5 RobusttoModelVariations
Inthemainpaper,allofVoyager’sexperimentsareconductedwithgpt-4-0314. Weadditionally
runnewexperimentswithgpt-4-0613andfindthattheperformanceisroughlythesame(Fig.A.4).
ItdemonstratesthatVoyagerisrobusttomodelvariations.
FigureA.4: VOYAGER’sperformancewithGPT-4-0314andGPT-4-0613.
42