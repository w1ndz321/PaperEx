# excited-state-snar-reactions-of-nitroarenes

pubs.acs.org/JACS Article
Excited-State S Ar Reactions of Nitroarenes
N
Zhen Lyu, § Tiantian Liang, § Gui-Juan Cheng,* and Fei Ye*
CiteThis:https://doi.org/10.1021/jacs.5c21841 ReadOnline
ACCESS *
Metrics&More ArticleRecommendations sı SupportingInformation
ABSTRACT: Nucleophilic aromatic substitution (S Ar) tradi-
N
tionally requires ground-state dearomatization to form Meisen-
heimer intermediates, restricting the reactivity to arenes bearing
strong electron-withdrawing groups (EWGs). Here we disclose
excited-state S Ar reactions of nitroarenes under visible light
N
irradiation,inwhichtriplet-stateelectronicreorganizationfurnishes
a strong aromaticity-recovery driving force for C −NO Ar 2
substitution, enabling reaction pathways that are inaccessible in
the ground state. Following computational evaluation of common
nucleophiles, we developed a synthetically practical protocol that
enables denitrative substitution across diverse polycyclic arenes.
These findings demonstrate that photoexcitation can reshape the aromatic character of arenes, thereby offering a new strategy to
access previously inaccessible modes of arene functionalization.
1. INTRODUCTION Scheme 1. State-of-the-Art of S Ar Reactions
N
Nucleophilic aromatic substitution (S Ar) is a fundamental
N
transformation in organic synthesis. It is the second most
frequently employed transformation in medicinal chemistry,
occurring at least once inthe synthetic pathways of numerous
blockbuster pharmaceuticals.1 It enables regioselective ipso-
substitution to construct C−C2 and C−heteroatom2−5 bonds
on aromatic scaffolds. Mechanistically, both stepwise and
concerted S Ar pathways proceed through the formation of
N
Meisenheimer intermediates or Meisenheimer-like transition
states,6,7 involving partial dearomatization and substantial
accumulation of negative charge on the aromatic ring.8,9
Consequently, S Ar reactions typically require electron-
N
deficient arenes bearing strong electron-withdrawing groups
(EWGs)attheortho-orpara-positionsoftheleavinggroupto
stabilize the intermediate and offset the energetic penalty of
dearomatization10 (Scheme 1A, left). While transient elec-
tronic activation strategies, such as transition-metal coordina-
tion (e.g., Ru,11,12 Rh,13 Cr14), or alkali7/base-mediated2,15
arene polarization, can facilitate nucleophilic substitution
without EWGs (Scheme 1A, right). These methods often
rely on strongly basic environments or expensive catalysts,
which limit their scalability and functional group tolerance.
Moreover, under such basic conditions, competing elimina-
tion-addition pathways may lead to the formation of aryne
intermediates,16 often resulting in poor regioselectivity and
mixtures of ipso- and ortho-substituted products.17 Thus, the Received: December7, 2025
scope of S Ar remains fundamentally constrained by the Revised: March19,2026
N
electronicstructureoftheareneinitsgroundstate.Incontrast, Accepted: March23,2026
photoexcitationtemporarilyreshuffleselectrondensityacrossa
π-conjugated framework, creating a reactive landscape that is
inaccessible thermally, such as photoinduced skeleton
©XXXXAmericanChemicalSociety https://doi.org/10.1021/jacs.5c21841
A J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
.)CTU(
22:33:70
ta
6202
,3 lirpA
no
SECNEICS
FO
YMEDACA
ESENIHC
FO
VINU
aiv
dedaolnwoD
.selcitra
dehsilbup
erahs
yletamitigel
ot
woh
no
snoitpo
rof
senilediuggnirahs/gro.sca.sbup//:sptth
eeS
Journal of the American Chemical Society pubs.acs.org/JACS Article
Figure 1. (A) Energy profiles of the denitrative chlorination reaction at the ground state and excited state, with pink numbers indicating DBV
values.(B) Leftpanel: Aromaticity analysis of the T and S states, showing ACID plots with DBV values displayedin the center. The S state
1 0 0
shows a diatropic ring current characteristic of Hückel aromaticity, whereas the T state exhibits weakened and nondirectional ring currents,
1
indicating (anti or non)-aromaticity. Right panel: Calculated isosurface of the Dual Descriptor Δf(r) at the B3LYP-D3BJ/def2-TZVP level of
theory,illustratingnitrobiphenyl’snucleophilic(green;Δf(r)>0)andelectrophilicsites(cyan;Δf(r)<0)atisovaluesof0.06(S)and0.015(T).
0 1
rearrangement,18isomerization,19,20cycloaddition,20−23andso N/C−C bonds (Scheme 1C). Density functional theory
on.23−26 (DFT)calculationsdemonstratethatphotoexcitationreconfig-
However, the aromatic substitution reaction under the ures the electronic structure of the π-extended nitroarene,
excited state still remains scarce (Scheme 1B). Only isolated thereby enabling the excited-state S Ar to proceed with the
N
examples of substitution reactions of nitroaromatics under recovery of aromaticity.
excited state have been reported since the 1970s,27,28 yet the Thermally, the NO group behaves as a conventional
2
applicable substrates were mostly nitronaphthalene, and electron-withdrawing activator, and not a general leaving
nucleophiles were large access amount of cyanide, boron group in arene transformations until 2017, the Nakao group
hydride, or hydroxide (usually more than 10 equiv).29−32 reported a Pd-catalyzed cross-coupling strategy to construct
Because the irradiation source was UV light, the substitution C−C and C−N bond by using the nitro moiety as
reaction always occurred both on the C -LG (leaving group) pseudohalides.34−36 In early 2025, our group reported a
Ar
bond and C -H bond33 with the formation of a complex visible-light-promoted denitrative chlorination of unactivated
Ar
mixture. Herein, we report an excited-state S Ar reaction of nitroarenes.37 FeCl served as a photosensitizer to generate
N 3
nitroarenes without external electron-withdrawing groups chlorine radicals and thereby activated ground-state nitro-
undervisiblelightirradiation,andcanreplacethenitromoiety arenestowardradicalaromaticsubstitution(S Ar).Duringthe
R
with various nucleophiles, to construct C−H/C−D/C−O/C- reaction condition investigation, we observed ∼5% yield of
B https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
Figure2.(A)Statisticsof chargetransferfromNu−tonitrobiphenylin3IM1(3IM1′)complex,theresultsarearrangedindescendingorderof
Δq TheRgroupinthelistednucleophilesisamethylgroup.RCOCH−andRC(�CH)O−correspondtoC-andO-nucleophilicmodesofthe
Nu. 2 2
sameenolateanion.(B)Reactionmechanismandtwo-dimensionalPESfortheS ArreactionswithRNH−andCl−.Contourmapsareplottedas
N
functions of the C−Nu and C−NOdistances, with energies referenced to 3IM. IRC paths (dots, 30 steps) are traced from DFT-optimized
2 1
C https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
Figure 2.continued
transitionstates.(C)Evaluationofrelativereactivities.ForNu−withΔq >0.7,whenΔG <ΔG ,ΔG =G −G ;elseΔG =
Nu 3IM3′ T1 3IM3′ 3IM3′ 3IM1′ 3IM3′
G −G .
3IM3′ T1
denitrative chlorination product even in the absence of iron T (0.047)andS (−0.0328),whichsuggeststhatC4changes
1 0
catalysts or external oxidants (Scheme 1C, initial result), from nucleophilic in S to electrophilic in T (right panel of
0 1
indicating that nitroarenes themselves are able to engage with Figures1B and S4).Consistentwith its electrophilic property,
light under the photoirradiation conditions. The UV−vis NPA charge47 and spin density analysis unveil obvious radical
absorption spectrum also confirmed a non-negligible absorp- cation character for C4 in T (q = 0.179, ρ = 0.304).
1 C4 C4
tion onset of nitroarenes in about 390 nm (Figures S2 and Second, the excited-state S Ar is driven by aromaticity
N
S22), indicating the possibility of excitation under light recovery. We performed aromaticity analysis48−52 on the key
irradiation. Motivated by our photocatalyst-free aromatic structures along the reaction coordinate (Figure S5). Figure 1
denitrative chlorination reaction, and recently reported nitro- presents the bifurcation value (DBV) of the electron
arene mediated transformation under excited state,38−43 we localization function (ELF), an aromaticity scale (aromatic:
hypothesized that nitroarenes might possess the intrinsic DBV > 0.70; nonaromatic: DBV = 0.55−0.70; antiaromatic:
potential to undergo S Ar reaction from an excited state. DBV < 0.55) defined in previous studies.52−54 In T , the
N 1
Through a combined computational and experimental nonsubstitutedphenylring(Ph1)andnitro-substitutedphenyl
approach,weelucidatethemechanisticoriginofthispreviously ring (Ph2) were identified as nonaromatic (DBV = 0.61,
uncharacterized denitrative reactivity and evaluate common Figure 1B, left and Table S3) and antiaromatic (DBV = 0.51,
nucleophilic anions to identify substitution-competent nucle- Figure S5),48−52 distinct from S involving two aromatic
0
ophile classes under light irradiation conditions. Guided by phenylrings.In3IM1,thearomaticityofPh1(DBV=0.64)is
these insights, we developed a broadly applicable denitrative partially recovered via partial charge transfer (Δq = 0.423)
functionalizationprotocol forπ-extendedarenes that proceeds from Cl−tonitrobiphenyl. Withfurtherelectrontransferfrom
without the requirement of prior electronic activation. The Cl− in 3TS1, Ph1 becomes aromatic (DBV = 0.73). Finally,
synthetically practical and scalable reaction is able to deliver Ph2 becomes aromatic when the nitro group is replaced with
the products that are readily diversified in downstream Clin3IM3.Overall,theS ArprocessofT graduallyrecovers
N 1
transformations. This work establishes an excited-state thearomaticityofthetwophenylrings,differingfromtheS Ar
N
manifold as a mechanistically distinct platform for S N Ar of S 0. In conclusion, the computational study unveils that the
reactivity, enabling rational nucleophile selection and extend- denitrative chlorination reaction occurs via exited-state S Ar
N
ing denitrative substitution to structurally diverse polycyclic process, which is facilitated by the enhanced electrophilicity
arenes. and driven by aromaticity recovery.55,56
2.2. Computational Identification of Nucleophile
2. RESULTS AND DISCUSSION
Candidates
2.1. Reaction Mechanism of Denitrative Chlorination: Basedontheunveiledreactionmechanism,wefurtherseekto
Excited-State S N Ar develop more efficient denitrative substitution reactions. As
Despite the low reactivity of photoinduced denitrative computationalanalysisrevealed,theexcited-stateS N Arprocess
chlorination of nitroarenes (5% yield, Scheme 1C), its gradually restores the aromaticity of the phenyl rings via
potential for enabling excited-state substitution reactions electron donation from the nucleophile; thus, the electron-
prompted our density functional theory (DFT) mechanistic transfercapacityofthenucleophilesmayinfluencethereaction
investigation to inform the development of more efficient pathway.Totestthishypothesis,wefirstcalculatedthecharge
denitrative substitutions. As demonstrated in Figure 1A, the change of nucleophile in 3IM1 (Δq Nu ) for 16 representative
denitrative chlorination of ground-state nitrobiphenyl (S ) via carbon, hydrogen, halogen, oxygen, nitrogen, and sulfur
0
a concerted S Ar mechanism requires overcoming a nucleophiles57 (R is the methyl group in relevant nucleo-
N
prohibitively high activation barrier of 49.3 kcal/mol, which philes). The computational results demonstrated that Δq Nu
is relatedto the dearomatizationfeature of thetransition state exhibits high correlations with the oxidation potential (R2 =
(1TS0). Upon photoexcitation, nitrobiphenyl is promoted to 0.86, Figure S6) and vertical ionization potential (R2 = 0.80,
its singlet excited state (S1, Figure S3), followed by an Figure S6), indicating that the charge transfer trend is related
intersystemcrossing(ISC,TableS2)toaffordbiradicaltriplet to ground state properties of the nucleophiles. As shown in
speciesT .T thenundergoesinternalconversion(IC)toform
Figure2A,I−,Br−,RCOO−,F−,andCN−couldtransferpartial
2 2
thelowesttriplet-statespeciesT ,whichfurtherformsvander charges (Δq < 0.6) to the substrate, similar to Cl−. While,
1 Nu
Waals complex 3IM1 with the chloride. Subsequent concerted othernucleophilescouldtransferasingleelectrontoT (Δq
1 Nu
S Ar of 3IM1 occurs with an activation barrier of 28.7 kcal/ > 0.7), which may enable the electron-transfer promoted
N
mol,whichismorefavorablethanthatofgroundstateS Arby S Ar,58 a distinct mechanism compared to the two-electron-
N N
20.6 kcal/mol. transfer process observed for Cl−. To test this possibility, we
The significantly lower barrier of the excited-state S Ar analyzed the substitution reaction with RNH−. As depicted in
N
reaction could be attributed to two major factors. First, the Figures2BandS5,thesingleelectrontransferofRNH−toT
1
excited-stateS Arisfacilitatedbytheenhancedelectrophilicity generates 3IM1′ in which Ph1 nearly recovers aromaticity
N
of the ipso-carbon C4 in T due to intramolecular charge (DBV=0.67,FigureS5)andPh2partiallyrecoversaromaticity
1
transfer44,45 and π-electron density reorganization of the (DBV=0.58).Thenitrobiphenylin3IM1′mayfurthercouple
nitrobiphenyl during the excitation-relaxation process. This is with RNH• radical to form the σ-complex 3IM3′�a
evidencedbythecalculatedDualDescriptor46Δf(r)forC4in Meisenheimer complex analogue with delocalized radical�
D https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
andfinishthesubstitutioninastepwisemanner(stepwisepath Table 1. Experimental Identification of Computational-
I). This proposed mechanism is supported by the two- Evaluated Nucleophilesa
dimensional potential energy surface (PES, Figure 2C) scan,
whichidentifiestwosaddlepointsseparatedbytheσ-complex.
Further DFT optimizations (Figures S7 and S8) confirm that
thesesaddlepointscorrespondtothetransitionstates(TSs)of
nucleophile addition (3TS1′) and nitro group dissociation DFTsuggested yield without
(3TS2′),respectively.Ontheotherhand,thetwo-dimensional entry Nu− nucleophiles (%)b light
PES of the denitrative chlorination reaction locates the saddle 1c H− NaBH 4 72% ndd
point of the concerted pathway. Meanwhile, it identifies two 2e OH TBAH 74% nd
additional saddle points corresponding to the TSs of nitro 3f RCONH− CF 3 CONH 2 75% nd
radical dissociation (3TS1) and nucleophile addition (3TS2). 4g RO− CF 3 CH 2 OH 56% nd
This alternative stepwise path II is calculated to have an 5h RCOCH 2 − (CH 3 ) 3 SiOC(CH 3 )�CH 2 14% nd
activation barrier (28.3 kcal/mol, Figure S13) comparable to 6i RNH− ethanolamine 28% nd
that of the concerted pathway. Overall, initial computational 7j CN− acetonecyanohydrine 70% nd
assessments suggest that the S Ar reaction may proceed via a 8k F− TBAF·H 2 O 15% nd
N
concerted or stepwise mechanism depending on the nature of aReactions wereconducted in 0.10 mmol under 390 nm LEDs with
nucleophiles. argon. bIsolated yield. c1 (1.0 equiv), NaBH 4 (2.0 equiv), H 2 O (2.2
equiv), oxone (2.0 equiv), MeCN (0.10 M), r.t., 12 h. dnd, not
To further evaluate the relative reactivity of nucleophiles
detected.e1(1.0equiv),TBAH(3.0equiv),MeCN(0.10M),r.t.,48
toward the S Ar reaction of nitrobiphenyl, we examined the
N h.f1(1.0equiv),CFCONH (3.0equiv),CsCO (4.0equiv),oxone
three plausible mechanisms for the reactions of all of the (1.0 equiv), MeCN 3 (0.10 2 M), 75 °C, 4 2 8 h 3 . g1 (1.0 equiv),
nucleophiles. It was found that nucleophiles with Δq > 0.7
Nu CF 3 CH 2 OH(10.0equiv),K 3 PO 4 (5.0equiv),oxone(1.0equiv),1,2-
are able to form a σ-complex with T 1 , while the concerted TS dichloroethane (0.050 M), no fans, 24 h. h1 (1.0 equiv),
and the radical complex 3IM3 cannot be located. Thus, they (CH)SiOC(CH)�CH (3.0 equiv), MeCN (0.10 M), r.t., 24 h.
3 3 3 2
are considered to undergo the electron-transfer-promoted iEthanolamine(2.0equiv),trifluoroethanol(0.050M),75°C,24h.j1
stepwise S Ar reaction, and their relative reactivity was (1.0 equiv), acetone cyanohydrin (1.1 equiv), BTMG (1.2 equiv),
assessed by N the relative stabilities of the σ-complex. These MeCN (0.10 M), r.t., 12 h. k1 (1.0 equiv), TBAF·H 2 O (4.0 equiv),
MeCN (0.10M),75°C, 48h.
nucleophileswereclassifiedintotwogroups(Figure2C)based
on the formation energy of the σ-complex (ΔG ). H−,59
IM3′
HO−, RCONH−, RO−, RCOCH −, and RNH−60 were Starting from these model reactions, this protocol was
2
classified into the more reactive group as their ΔG values further expanded and demonstrated broad applicability across
IM3′
are relatively smaller (<15.0 kcal/mol). (RCO) CH−, RS−, arenes featuring diverse scaffolds and substitution patterns
2
HS−,andRC(�CH )O−wereclassifiedintothelessreaction (Figure 3). 4-nitro-1,1′-biphenyls bearing electron-withdraw-
2
group due to their larger ΔG values (>17.0 kcal/mol). ing groups, such as trifluoromethyl or halides at the 4′-para
IM3′
Nucleophiles with Δq < 0.7 were found to undergo position, afforded the corresponding hydrogenated products
Nu
concerted or (and) stepwise S Ar (Figures S10−S15). Their (2, 4, 6, 8, 10, 12, and 14) in 63−72% yields. Substrates
N
relative reactivity was assessed using the activation barriers of containing biphenyl motifs were converted to the correspond-
their preferred pathway (ΔG‡). F−, CN−, and RCOO− were ing products (16, 18) in 70 and 55% isolated yields,
calculatedtobemorereactivethanCl−,whileBr−andI−show respectively. The method also tolerated para-phenylethynyl
comparable reactivity with Cl−. Together, H−, HO−, nitroarenes and 2-nitrothiophenes, affording hydrogenation
RCONH−, RO−, RCOCH −, RNH−, F−, CN−, and RCOO− products(20,22)in72and48%yields.Fusedringnitroarenes
2
arepotentiallymoreefficientnucleophilesfortheexcited-state engaged effectively as well, providing substitution products
S Ar reaction of nitrobiphenyl. (24,26,and28)inapproximately70%yields.Thedeuterated
N
analogues (3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, and
2.3. Experimental Evaluation of S Ar Reactions of
N 29)were obtainedincomparableyieldstotheirhydrogenated
Nitrobiphenyls
counterparts,withayielddifferenceoflessthan10%.Notably,
The experiments began by testing the 9 nucleophilic anions the deuteration incorporation rates were higher than 95%
identifiedcomputationally.Uponexperimentaloptimization,8 across all cases, even in the presence of H O. Beyond hydride
2
nucleophilic patterns successfully afforded the corresponding sources,denitrativeetherificationwasachievedbyusingaweak
substitution products under external-photocatalyst-free con- nucleophile (HFIP) to afford biaryl ether products (31).
ditions(Table1),whichwereprovedinactivewithoutlight.As Substrates bearing heterocyclic rings (32, 33, and 37−39) or
suggested by DFT calculations, carboxylic acid should be fused ring systems (34−36) afforded the corresponding
compatible for denitrative substitution. However, an oxidative etherification products in 45−81% yields, and 2-nitro-
decarboxylation process can occur with the presence of thiophenes participated efficiently to deliver 40 in 75% yield.
nitroarene under light irradiation, thus the denitrative Furthermore,monocycliccompoundsincludingpyridine(41),
substitution can be hampered61 (see Figure S19). Further- thiophene (42), benzene ring (43), and benzamide-protected
more, control experiments confirmed that this reaction could benzene ring (44) can all undergo the reaction to afford the
still proceed without oxone, albeit with diminished yield. We corresponding etherification products with 41−60% yield.
believe the role of oxone was to suppress the formation of Additionally, trifluoroethanol as nucleophile afforded the
reductionsideproductsorintermediatesofnitroaromatics(see product with 75% yield (30). The scope of the protocol was
Figures S26−S28 for details). Radical trapping experiments further expanded to include nitrogen-based nucleophiles for
indicated that the reaction mechanism did not proceed via a directdenitrativefunctionalization.Aseriesofprimaryamines,
radical pathway (see Tables S13 and S14 for details). including ethanolamine (45, 46, 49), 2-methoxyethylamine
E https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
Figure3.Experimentaldesignforproposedreactionpatterns.Reactionswereconductedin0.10mmolunder390nmLEDs.aNaBH (2.0equiv)
4
orNaBD (2.0equiv),HO(2.20equiv),oxone(2.0equiv),MeCN(0.10M),r.t,12h.bHFIP(10.0equiv),KPO (5.0equiv),1,2-dichloroethane
4 2 3 4
(0.05 M), oxone (1.0 equiv), no fans, 24 h. cCFCONH (3.0 equiv), CsCO (4.0 equiv), oxone (1.0 equiv), MeCN (0.10 M), 75 °C or
3 2 2 3
F https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
Figure 3.continued
ethanolamine(2.0equiv),trifluoroethanol(0.05M),75°C,48h.dAfter2hofreaction,thestartingmaterialwascompletelyconsumedwith35%
NMRyield.60isconvertedto2,6-dichloro-4-aminopyridineuponcolumnchromatographypurification,evenindeuteratedsolvent.eTBAH(3.0
equiv),MeCN(0.10M),r.t.,48h.fTrifluoromethoxyreagent((E)-4-(tert-butyl)benzaldehydeO-trifluoromethyloxime)(2.0equiv),NaPO (3.0
3 4
equiv),MeCN(0.10M),75°C,24h.gTBAF·HO(4.0equiv),MeCN(0.1M),75°C.h(CH)SiOC(CH)�CH (3.0equiv),MeCN(0.10M),
2 3 3 3 2
r.t.,24h. iTMSCN(3.0 equiv), TBAF(4.0 equiv), MeCN(0.1 M),r.t.
Figure4.Syntheticapplicationofthedenitrativesubstitutionreaction.(A)1.0−3.0mmolscaled-upreactions.(B)Derivatizationoftheproduct34
and35.
(47), boc-protected amines (48), isobutylamine (50), and nucleophiles. Furthermore, we carried out the reaction at
pivalamine (51), were successful nucleophiles to produce the 120 °C without light irradiation. For nitroarenes bearing one
corresponding aminoarenes in 28−66% yields, respectively. more electron-withdrawing group (2, 22, 24, 30, 33, 34, 37,
Secondary amines failed to give out substitution products but 38, 45, 52, 54, 55, 57, 60, 65, and 66), which are prone to
reduced nitroarene directly to aniline derivatives because of undergo a thermally induced S Ar reaction, most of them
N
their relatively stronger reducing ability. Trifluoroacetamides failedto givedenitrative products,demonstratingfundamental
also proved compatible, delivering C−N bond coupling mechanistic distinction of our reaction with classical trans-
products without detectable C−O bonding byproducts (52). formations. To further demonstrate the applicability of the
Both electron-deficient nitroarenes (53) and electron-rich protocol, 3.0 mmol scaled-up reactions were performed on
(54−57) underwent denitrative amination, providing the selected substrates, furnishing hydrogenation, etherification,
products in varying yields from 36 to 72%. Most importantly, amination,andamidationproducts(24,35,37,46,and56)in
for monocyclic systems, acetyl (Ac)-protected nitroanilines moderate yields (Figure 4A). Furthermore, the methodology
(58), as well as nitropyridines (59), can also afford the target was successfully integrated with site-selective nitration,
products. Nonfluorinated substituted alcohols or amides were enabling the consecutive modification of molecules (Figure
unsuccessfulsubstratesbecauseoftheneedofstrongerbaseto 4B). 34 and 35 were subjected to a well-established nitration
generate O/N based anion nucleophiles. However, such bases procedure to introduce a nitro group. Subsequent denitrative
can likely react with the acidic C−H bond on the ortho etherificationandaminationaffordedthedoublyfunctionalized
position of the nitro group, thus leading to side reactions. products 71 and 72 in 75 and 85% yields, respectively.
Finally, the protocol was expanded to other nucleophiles such
as tetrabutylammonium hydroxide (TBAH). Hydroxy- and
4. CONCLUSION
fluoro-biphenylderivatives(60−63)wereobtainedin42−74%
yields. The methodology was also applicable to the In summary, this work establishes an excited-state S N Ar
polyaromatic ring, affording hydroxylated pyrene (64). reaction for nitroarenes. Mechanistic studies revealed that
Trifluoromethoxylation (65), fluorination (66), enolization photoexcitation of nitrobiphenyl induces a redistribution of
(67),andcyanation(68−70)werealsoaccomplished,albeitin electron density that transiently alters the substitution
lower yield. Dissociated fluoride as well as enolate are landscape, enabling nucleophilic attack and rearomatization
supposed to exist at a relatively lower concentration in the without ground-state electronic penalties. Further reactivity
reaction mixture, leading to lower conversion of denitrative analysis highlights nucleophiles with favorable substitution
substitution. Trifluoromethoxide can decompose gradually,62 characteristics, which were subsequently examined and
therefore the yield of the substitution product is low. Those developed experimentally. The resulting protocol proceeds
experiments were then extended to models predicted as less without preinstalled electron-withdrawing groups or external
favorable, such as bromide, iodide, and so on. Most photocatalysts, accommodates polycyclic arenes, and is
nucleophiles were unreactive under the standard conditions synthetically practical. More broadly, these findings demon-
(see Figure S19), further supporting the computational model strate that excited-state electronic reconfiguration can be
as an effective predictor of the intrinsic reactivity of leveraged to unlock aromatic substitution pathways inacces-
G https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
sible in the ground state, opening new opportunities for light- cial Natural Science Foundation of China (Grant
driven arene functionalization. 2022CFB682, F.Y.) CCNU for startup funding (F.Y.), the
■ NationalNaturalScienceFoundationofChina(no.22422110,
ASSOCIATED CONTENT 22573090, G.-J.C.), Warshel Institute for Computational
* sı Supporting Information Biology funding from Shenzhen City and Longgang District
(LGKCSDPT2025001), and the Guangdong Basic and
The Supporting Information is available free of charge at
Applied Basic Research Foundation (no. 2023B1515020052,
https://pubs.acs.org/doi/10.1021/jacs.5c21841.
G.-J.C.).
PES (ZIP)
■
Additional experimental and computational details,
REFERENCES
materials, and methods, including photographs of the
experimental setup and spectral data for all compounds (1)Bunnett,J.F.;Zahler,R.E.AromaticNucleophilicSubstitution
(PDF) Reactions. Chem. Rev.1951, 49(2),273−412.
(2)Shigeno,M.;Hayashi,K.;Sasamoto,O.;Hirasawa,R.;Korenaga,
■
T.; Ishida, S.; Nozawa-Kumada, K.; Kondo, Y. Catalytic Concerted
AUTHOR INFORMATION
S Ar Reactions of Fluoroarenes by an Organic Superbase. J. Am.
N
Corresponding Authors Chem. Soc. 2024,146 (47),32452−32462.
(3) Neumann, C. N.; Hooker, J. M.; Ritter, T. Concerted
Fei Ye − Engineering Research Center of Photoenergy
Nucleophilic Aromatic Substitution with 19F− and 18F−. Nature
Utilization for Pollution Control and Carbon Reduction,
2016, 534 (7607),369−373.
Ministry of Education, College of Chemistry, Central China
(4) Tay, N. E. S.; Nicewicz, D. A. Cation Radical Accelerated
Normal University (CCNU), Wuhan 430079, P. R. China;
NucleophilicAromaticSubstitutionviaOrganicPhotoredoxCatalysis.
orcid.org/0000-0003-0034-3321; Email: yef@
J. Am. Chem. Soc. 2017,139 (45),16100−16104.
ccnu.edu.cn (5)Zhu,Z.;Wu,X.;Li,Z.;Nicewicz,D.A.AreneandHeteroarene
Gui-Juan Cheng − Warshel Institute for Computational Functionalization Enabled by Organic Photoredox Catalysis. Acc.
Biology, SchoolofMedicine,The ChineseUniversityof Hong Chem. Res. 2025,58 (7),1094−1108.
Kong, Shenzhen 518172, P. R. China; orcid.org/0000- (6)Kwan,E.E.;Zeng,Y.;Besser,H.A.;Jacobsen,E.N.Concerted
0002-2818-2235; Email: chengguijuan@cuhk.edu.cn NucleophilicAromaticSubstitutions.Nat.Chem.2018,10(9),917−
923.
Authors (7)Rohrbach,S.;Smith,A.J.;Pang,J.H.;Poole,D.L.;Tuttle,T.;
Zhen Lyu − Warshel Institute for Computational Biology, Chiba, S.; Murphy, J. A. Concerted Nucleophilic Aromatic
School of Medicine, The Chinese University of Hong Kong, Substitution Reactions. Angew. Chem., Int. Ed. 2019, 58 (46),
16368−16388.
Shenzhen 518172, P. R. China
(8) Terrier, F. Rate and Equilibrium Studies in Jackson-
TiantianLiang−EngineeringResearchCenterofPhotoenergy
Meisenheimer Complexes.Chem. Rev.1982, 82(2), 77−152.
Utilization for Pollution Control and Carbon Reduction,
(9) The S Ar Reactions: Mechanistic Aspects. In Modern
Ministry of Education, College of Chemistry, Central China N
Nucleophilic Aromatic Substitution; John Wiley & Sons, Ltd, 2013;
Normal University (CCNU), Wuhan 430079, P. R. China
pp 1−94.
Complete contact information is available at: (10)Miller,J.AromaticNucleophilicSubstitution;ElsevierPublishing
https://pubs.acs.org/10.1021/jacs.5c21841 Company, 1968.
(11) Chen, K.; Shi, H. Nucleophilic Aromatic Substitution of
Author Contributions
HalobenzenesandPhenolswithCatalysisbyArenophilicπAcids.Acc.
Chem. Res. 2024,57 (15),2194−2206.
§Z.L. and T.L. contributed equally to this work.
(12) Chen, J.; Lin, Y.; Wu, W.-Q.; Hu, W.-Q.; Xu, J.; Shi, H.
Notes Amination of Aminopyridines via Η6-Coordination Catalysis. J. Am.
Chem. Soc. 2024,146 (33),22906−22912.
The authors declare no competing financial interest.
(13) Su, J.; Chen, K.; Kang, Q.-K.; Shi, H. Catalytic S Ar
■ N
Hexafluoroisopropoxylation of Aryl Chlorides and Bromides. Angew.
ACKNOWLEDGMENTS
Chem. 2023, 135 (24),No. e202302908.
WethankY.Xu(PekingUniversity),R.C.Sang(Universityof (14) Alemagna, A.; Cremonesi, P.; Del Buttero, P.; Licandro, E.;
California),andG.J.Wu(HuazhongUniversityofScienceand Maiorana, S. Nucleophilic Aromatic Substitution of Cr(CO)
3
Technology)forhelpfuldiscussionsabouttheproject.Wealso Complexed Dihaloarenes with Thiolates. J. Org. Chem. 1983, 48
appreciatetheadviceprovidedbyY.Zhou(CUHKSZ),aswell (18),3114−3116.
as L. Liu (CCNU), for assistance in manuscript preparation. (15)Nitta,Y.;Nakashima,Y.;Sumimoto,M.;Nishikata,T.Directed
WealsothanktheassistanceofW.Y.Zhao(CCNU),J.L.Qiu NucleophilicAromatic SubstitutionReaction.Chem. Commun.2024,
(CCNU), M. X. Han (CCNU), W. R. Sun (CCNU), F. Yang
60(96),14284−14287.
(16) Himeshima, Y.; Sonoda, T.; Kobayashi, H. Fluoride-Induced
(CCNU),andJ.Zheng(CCNU)inthesynthesisofsubstrates
1,2-Elimination of O-Trimethylsilylphenyl Triflate to Benzyne under
and the performance of related experiments. W. H. Xu
Mild Conditions.Chem. Lett.1983, 12(8), 1211−1214.
(CCNU) for the assistance on NMR data collection, J. M.
(17)Im,G.-Y.J.;Bronner,S.M.;Goetz,A.E.;Paton,R.S.;Cheong,
Gong (CCNU) for the help on the IC test, L. Y. Chen
P. H.-Y.; Houk, K. N.; Garg, N. K. Indolyne Experimental and
(CCNU) for electron paramagnetic resonance measurement.
Computational Studies: Synthetic Applications and Origins of
Prof.W.J.Xiao(CCNU)forthehelpwithhigh-resolutionMS
Selectivities of Nucleophilic Additions. J. Am. Chem. Soc. 2010, 132
testing.WearegratefultotheKnowledgeInnovationProgram (50),17933−17944.
of the Wuhan-Shuguang Project (2023020201020308, F.Y.); (18) Allen, A. R.; Noten, E. A.; Stephenson, C. R. J. Aryl Transfer
theCultivationProgramofWuhanInstituteofPhotochemistry Strategies Mediated by Photoinduced Electron Transfer. Chem. Rev.
and Technology (GHY2023KF003, F.Y.); the Hubei Provin- 2022, 122 (2),2695−2751.
H https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
(19)Nevesely,́ T.;Wienhold,M.;Molloy,J.J.;Gilmour,R.Advances (41)Mdluli,V.;Lehnherr,D.;Lam,Y.;Ji,Y.;Newman,J.A.;Kim,J.
in the E → Z Isomerization of Alkenes Using Small Molecule Copper-EnabledPhoto-SulfonylationofArylHalidesUsingAlkylsul-
Photocatalysts.Chem. Rev.2022, 122 (2),2650−2694. finates. Adv.Synth.Catal. 2023, 365(22),3876−3886.
(20) Großkopf, J.; Kratz, T.; Rigotti, T.; Bach, T. Enantioselective (42)Rihtarsǐc,̌ M.;Kweon,B.;Błyszczyk,P.T.;Ruffoni,A.;Arpa,E.
PhotochemicalReactionsEnabledbyTripletEnergyTransfer.Chem. M.; Leonori, D. Excited-State Configuration Controls the Ability of
Rev.2022, 122(2), 1626−1653. Nitroarenes toActasEnergyTransferCatalysts.Nat.Catal.2025,8
(21) Dutta, S.; Erchinger, J. E.; Strieth-Kalthoff, F.; Kleinmans, R.; (12),1361−1369.
Glorius, F. Energy Transfer Photocatalysis: Exciting Modes of (43)Olivier,W.J.;Błyszczyk,P.;Arpa,E.M.;Hitoshio,K.;Gomez-
Reactivity.Chem. Soc.Rev.2024, 53(3),1068−1089. Mendoza, M.; de la Peña O’Shea, V.; Marchand, I.; Poisson, T.;
(22) Kärkäs, M. D.; Porco, J. A., Jr.; Stephenson, C. R. J. Ruffoni, A.; Leonori, D. Excited-State Configuration of Nitroarenes
Photochemical Approaches to Complex Chemotypes: Applications EnablesOxidativeCleavageofAromaticsoverAlkenes.Science2025,
inNaturalProductSynthesis.Chem.Rev.2016,116(17),9683−9747. 387 (6739),1167−1174.
(23) Hoffmann, N. Photochemical Reactions as Key Steps in (44) Ghosh, R.; Nandi, A.; Palit, D. K. Solvent Sensitive
OrganicSynthesis.Chem. Rev.2008, 108(3), 1052−1103. Intramolecular Charge Transfer Dynamics in the Excited States of
(24) Song, L.;Fu,D.-M.;Chen, L.;Jiang,Y.-X.; Ye,J.-H.; Zhu,L.; 4-N,N-Dimethylamino-4′-Nitrobiphenyl. Phys. Chem. Chem. Phys.
Lan, Y.; Fu, Q.; Yu, D.-G. Visible-Light Photoredox-Catalyzed 2016, 18(11),7661−7671.
Remote Difunctionalizing Carboxylation of Unactivated Alkenes (45) Lee, S.; Jen, M.; Jang, T.; Lee, G.; Pang, Y. Twisted
withCO.Angew. Chem.,Int. Ed. 2020,59(47), 21121−21128. Intramolecular Charge Transfer of Nitroaromatic Push−Pull
2
(25) Lu, F.-D.;Liu, D.; Zhu,L.;Lu, L.-Q.;Yang, Q.;Zhou,Q.-Q.; Chromophores. Sci.Rep.2022, 12(1), No. 6557.
Wei, Y.; Lan, Y.; Xiao, W.-J. Asymmetric Propargylic Radical (46)Morell,C.;Grand,A.;Toro-Labbé,A.NewDualDescriptorfor
Chemical Reactivity.J. Phys.Chem. A2005, 109 (1),205−212.
CyanationEnabledbyDualOrganophotoredoxandCopperCatalysis.
J. Am. Chem.Soc. 2019, 141(15),6167−6172. (47) Glendening, E. D.; Landis, C. R.; Weinhold, F. NBO 6.0:
Natural Bond Orbital Analysis Program. J. Comput. Chem. 2013, 34
(26) Leng, L.; Fu, Y.; Liu, P.; Ready, J. M. Regioselective,
Photocatalytic α-Functionalization of Amines. J. Am. Chem. Soc.
(16),1429−1437.
(48) Geuenich, D.; Hess, K.; Köhler, F.; Herges, R. Anisotropy of
2020, 142(28),11972−11977.
theInducedCurrentDensity(ACID),aGeneralMethodtoQuantify
(27)Pintér,B.;DeProft,F.;Veszprémi,T.;Geerlings,P.Theoretical
and Visualize Electronic Delocalization. Chem. Rev. 2005, 105 (10),
Study of the Orientation Rules in Photonucleophilic Aromatic
3758−3772.
Substitutions.J. Org. Chem.2008, 73(4), 1243−1252.
(49) Savin, A.; Nesper, R.; Wengert, S.; Fässler, T. F. ELF: The
(28)Döpp,D.ReactionsofAromaticNitroCompoundsviaExcited
ElectronLocalizationFunction.Angew.Chem.,Int.Ed.1997,36(17),
Triplet States. In Triplet States II; Wild, U. P.; Döpp, D.; Dürr, H.,
1808−1832.
Eds.;Springer:Berlin,Heidelberg,1975; pp 49−85.
(50) Chen, Z.; Wannere, C. S.; Corminboeuf, C.; Puchta, R.;
(29) Fráter, G.; Havinga, E. Photosubstitution Reactions of
Schleyer,P.V.R.Nucleus-IndependentChemicalShifts(NICS)asan
Nitronaphthalenes Leading to Chloronaphthalene. Tetrahedron Lett.
Aromaticity Criterion.Chem. Rev.2005, 105 (10),3842−3888.
1969, 10,4603−4604.
(51)Szczepanik,D.W.;Andrzejak,M.;Dominikowska,J.;Pawełek,
(30) Petersen, W. C.; Letsinger, R. L. Photoinduced Reactions of
B.;Krygowski,T.M.;Szatylowicz,H.;Sola,̀ M.TheElectronDensity
Aromatic Nitro Compounds with Borohydride and Cyanide.
of Delocalized Bonds (EDDB) Applied for Quantifying Aromaticity.
TetrahedronLett. 1971, 12(24),2197−2200.
Phys.Chem. Chem. Phys.2017, 19(42),28970−28981.
(31) Vink, J. A. J.; Verheijdt, P. L.; Cornelisse, J.; Havinga, E.
(52)Zhu,Q.;Chen,S.;Chen,D.;Lin,L.;Xiao,K.;Zhao,L.;Sola,̀
Photoreactions of Aromatic Compounds�XXVI. Tetrahedron 1972,
M.; Zhu, J. The Application of Aromaticity and Antiaromaticity to
28(19),5081−5087.
Reaction Mechanisms. Fundam.Res. 2023, 3(6), 926−938.
(32) Wubbels, G. G.; Danial, H.; Policarpio, D. Temperature
(53) Echeverri, A.; Leyva-Parra, L.; Santos, J. C.; Gómez, T.;
Dependence of Regioselectivity inNucleophilic Photosubstitution of
Tiznado, W.; Cardenas, C. Excited State Aromaticity Unveiled by
4-Nitroanisole.TheActivationEnergyCriterionforRegioselectivity.J.
Electron Localization Function Topology. ChemPhysChem 2025, 26
Org.Chem. 2010, 75(22),7726−7733.
(24),No. e202500335.
(33) Letsinger, R. L.; Hautala, R. R. Solvent Effects in the
(54) Santos, J. C.; Tiznado, W.; Contreras, R.; Fuentealba, P.
Photoinduced Reactions of Nitroaromatics with Cyanide Ion. Sigma−Pi Separation of the Electron Localization Function and
TetrahedronLett. 1969, 10(48),4205−4208. Aromaticity. J. Chem. Phys.2004, 120(4), 1670−1673.
(34)Inoue,F.;Kashihara,M.;Yadav,M.R.;Nakao,Y.Buchwald−
(55)Slanina,T.;Ayub,R.;Toldo,J.;Sundell,J.;Rabten,W.;Nicaso,
Hartwig Amination of Nitroarenes. Angew. Chem. 2017, 129 (43), M.;Alabugin,I.;Galván,I.F.;Gupta,A.K.;Lindh,R.;Orthaber,A.;
13492−13494.
Lewis, R. J.; Grönberg, G.; Bergman, J.; Ottosson, H. Impact of
(35) Kashihara, M.; Nakao, Y. Cross-Coupling Reactions of Excited-State Antiaromaticity Relief in a Fundamental Benzene
Nitroarenes.Acc.Chem. Res. 2021, 54(14),2928−2935. Photoreaction Leading to Substituted Bicyclo[3.1.0]Hexenes. J. Am.
(36) Yadav, M. R.; Nagaoka, M.; Kashihara, M.; Zhong, R.-L.; Chem. Soc. 2020,142 (25),10942−10954.
Miyazaki,T.;Sakaki,S.;Nakao,Y.TheSuzuki−MiyauraCouplingof
(56) Sokolova, A. D.; Platonov, D. N.; Belyy, A. Y.; Salikov, R. F.;
Nitroarenes.J. Am. Chem. Soc.2017, 139 (28),9423−9426. Erokhin, K. S.; Tomilov, Y. V. The Antiaromatic Nucleophilic
(37)Liang,T.;Lyu,Z.;Wang,Y.;Zhao,W.;Sang,R.;Cheng,G.-J.; Substitution Reaction (S AAr) in Cycloheptatrienyl-Anion Contain-
N
Ye,F.Light-PromotedAromaticDenitrativeChlorination.Nat.Chem. ing Zwitterions with a Möbius-Aromatic Intermediate. Org. Lett.
2025, 17(4),598−605. 2024, 26(28),5877−5882.
(38)Gkizis,P.L.;Triandafillidi,I.;Kokotos,C.G.Nitroarenes:The (57) The Anionic Form Is Used for All Nucleophiles to Keep
RediscoveryoftheirPhotochemistryOpensNewAvenuesinOrganic Consistency.
Synthesis.Chem2023, 9, 3401−3414. (58) Rossi, R. A.; Pierini, A. B.; Peñéñory, A. B. Nucleophilic
(39)Sánchez-Bento,R.;Roure,B.;Llaveria,J.;Ruffoni,A.;Leonori, Substitution Reactions by Electron Transfer. Chem. Rev. 2003, 103
D.AStrategyforOrtho-PhenylenediamineSynthesisviaDearomative- (1), 71−168.
Rearomative Coupling of Nitrobenzenes and Amines. Chem 2023, 9 (59) BH4−,−17.0 kcal/mol,FigureS9.
(12),3685−3695. (60) RNH,9.1kcal/mol, FigureS8.
2
(40) Baranac-Stojanovic,́ M. Substituent Effect on Triplet State (61) Duke, A. D.; Banerjee, S.; Thupili, A. P.; Pradhan, D. R.;
Aromaticityof Benzene.J. Org.Chem. 2020, 85(6),4289−4297. Vetticatt, M. J.; Parasram, M. PCET-Enabled Decarboxylative
I https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX
Journal of the American Chemical Society pubs.acs.org/JACS Article
Oxygenation Promoted by Photoexcited Nitroarenes Chem 2026
DOI:10.1016/j.chempr.2025.102872.
(62) Li, Y.; Yang, Y.; Xin, J.; Tang, P. Nucleophilic Trifluor-
omethoxylationofAlkylHalideswithoutSilver.Nat.Commun.2020,
11(1),No. 755.
J https://doi.org/10.1021/jacs.5c21841
J.Am.Chem.Soc.XXXX,XXX,XXX−XXX