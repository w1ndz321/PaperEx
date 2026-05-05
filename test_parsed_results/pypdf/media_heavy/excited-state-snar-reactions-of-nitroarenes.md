# excited-state-snar-reactions-of-nitroarenes

Excited-State S
N
Ar Reactions of Nitroarenes
Zhen Lyu,
§
Tiantian Liang,
§
Gui-Juan Cheng,* and Fei Ye*
Cite This: https://doi.org/10.1021/jacs.5c21841
Read Online
ACCESS
Metrics & More
Article Recommendations *
sı Supporting Information
ABSTRACT: Nucleophilic aromatic substitution (S
N
Ar) tradi-
tionally requires ground-state dearomatization to form Meisen-
heimer intermediates, restricting the reactivity to arenes bearing
strong electron-withdrawing groups (EWGs). Here we disclose
excited-state S
N
Ar reactions of nitroarenes under visible light
irradiation, in which triplet-state electronic reorganization furnishes
a strong aromaticity-recovery driving force for C
Ar
−NO
2
substitution, enabling reaction pathways that are inaccessible in
the ground state. Following computational evaluation of common
nucleophiles, we developed a synthetically practical protocol that
enables denitrative substitution across diverse polycyclic arenes.
These findings demonstrate that photoexcitation can reshape the aromatic character of arenes, thereby offering a new strategy to
access previously inaccessible modes of arene functionalization.
1. INTRODUCTION
Nucleophilic aromatic substitution (S
N
Ar) is a fundamental
transformation in organic synthesis. It is the second most
frequently employed transformation in medicinal chemistry,
occurring at least once in the synthetic pathways of numerous
blockbuster pharmaceuticals.
1
It enables regioselective ipso-
substitution to construct C−C
2
and C−heteroatom
2−5
bonds
on aromatic scaffolds. Mechanistically, both stepwise and
concerted S
N
Ar pathways proceed through the formation of
Meisenheimer intermediates or Meisenheimer-like transition
states,
6,7
involving partial dearomatization and substantial
accumulation of negative charge on the aromatic ring.
8,9
Consequently, S
N
Ar reactions typically require electron-
deficient arenes bearing strong electron-withdrawing groups
(EWGs) at the ortho- or para-positions of the leaving group to
stabilize the intermediate and offset the energetic penalty of
dearomatization
10
(Scheme 1A, left). While transient elec-
tronic activation strategies, such as transition-metal coordina-
tion (e.g., Ru,
11,12
Rh,
13
Cr
14
), or alkali
7
/base-mediated
2,15
arene polarization, can facilitate nucleophilic substitution
without EWGs (Scheme 1A, right). These methods often
rely on strongly basic environments or expensive catalysts,
which limit their scalability and functional group tolerance.
Moreover, under such basic conditions, competing elimina-
tion-addition pathways may lead to the formation of aryne
intermediates,
16
often resulting in poor regioselectivity and
mixtures of ipso- and ortho-substituted products.
17
Thus, the
scope of S
N
Ar remains fundamentally constrained by the
electronic structure of the arene in its ground state. In contrast,
photoexcitation temporarily reshuffles electron density across a
π-conjugated framework, creating a reactive landscape that is
inaccessible thermally, such as photoinduced skeleton
Received: December 7, 2025
Revised: March 19, 2026
Accepted: March 23, 2026
Scheme 1. State-of-the-Art of S
N
Ar Reactions
Articlepubs.acs.org/JACS
© XXXX American Chemical Society
A
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
Downloaded via UNIV OF CHINESE ACADEMY OF SCIENCES on April 3, 2026 at 07:33:22 (UTC).
See https://pubs.acs.org/sharingguidelines for options on how to legitimately share published articles.
rearrangement,
18
isomerization,
19,20
cycloaddition,
20−23
and so
on.
23−26
However, the aromatic substitution reaction under the
excited state still remains scarce (Scheme 1B). Only isolated
examples of substitution reactions of nitroaromatics under
excited state have been reported since the 1970s,
27,28
yet the
applicable substrates were mostly nitronaphthalene, and
nucleophiles were large access amount of cyanide, boron
hydride, or hydroxide (usually more than 10 equiv).
29−32
Because the irradiation source was UV light, the substitution
reaction always occurred both on the C
Ar
-LG (leaving group)
bond and C
Ar
-H bond
33
with the formation of a complex
mixture. Herein, we report an excited-state S
N
Ar reaction of
nitroarenes without external electron-withdrawing groups
under visible light irradiation, and can replace the nitro moiety
with various nucleophiles, to construct C−H/C−D/C−O/C-
N/C−C bonds (Scheme 1C). Density functional theory
(DFT) calculations demonstrate that photoexcitation reconfig-
ures the electronic structure of the π-extended nitroarene,
thereby enabling the excited-state S
N
Ar to proceed with the
recovery of aromaticity.
Thermally, the NO
2
group behaves as a conventional
electron-withdrawing activator, and not a general leaving
group in arene transformations until 2017, the Nakao group
reported a Pd-catalyzed cross-coupling strategy to construct
C−C and C−N bond by using the nitro moiety as
pseudohalides.
34−36
In early 2025, our group reported a
visible-light-promoted denitrative chlorination of unactivated
nitroarenes.
37
FeCl
3
served as a photosensitizer to generate
chlorine radicals and thereby activated ground-state nitro-
arenes toward radical aromatic substitution (S
R
Ar). During the
reaction condition investigation, we observed ∼5% yield of
Figure 1. (A) Energy profiles of the denitrative chlorination reaction at the ground state and excited state, with pink numbers indicating DBV
values. (B) Left panel: Aromaticity analysis of the T
1
and S
0
states, showing ACID plots with DBV values displayed in the center. The S
0
state
shows a diatropic ring current characteristic of Hu ̈ckel aromaticity, whereas the T
1
state exhibits weakened and nondirectional ring currents,
indicating (anti or non)-aromaticity. Right panel: Calculated isosurface of the Dual Descriptor Δf(r) at the B3LYP-D3BJ/def2-TZVP level of
theory, illustrating nitrobiphenyl’s nucleophilic (green; Δf(r) > 0) and electrophilic sites (cyan; Δf(r) < 0) at isovalues of 0.06 (S
0
) and 0.015 (T
1
).
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
B
Figure 2. (A) Statistics of charge transfer from Nu
−
to nitrobiphenyl in
3
IM1 (
3
IM1′) complex, the results are arranged in descending order of
Δq
Nu.
The R group in the listed nucleophiles is a methyl group. RCOCH
2
−
and RC(�CH
2
)O
−
correspond to C- and O-nucleophilic modes of the
same enolate anion. (B) Reaction mechanism and two-dimensional PES for the S
N
Ar reactions with RNH
−
and Cl
−
. Contour maps are plotted as
functions of the C−Nu and C−NO
2
distances, with energies referenced to
3
IM
1
. IRC paths (dots, 30 steps) are traced from DFT-optimized
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
C
denitrative chlorination product even in the absence of iron
catalysts or external oxidants (Scheme 1C, initial result),
indicating that nitroarenes themselves are able to engage with
light under the photoirradiation conditions. The UV−vis
absorption spectrum also confirmed a non-negligible absorp-
tion onset of nitroarenes in about 390 nm (Figures S2 and
S22), indicating the possibility of excitation under light
irradiation. Motivated by our photocatalyst-free aromatic
denitrative chlorination reaction, and recently reported nitro-
arene mediated transformation under excited state,
38−43
we
hypothesized that nitroarenes might possess the intrinsic
potential to undergo S
N
Ar reaction from an excited state.
Through a combined computational and experimental
approach, we elucidate the mechanistic origin of this previously
uncharacterized denitrative reactivity and evaluate common
nucleophilic anions to identify substitution-competent nucle-
ophile classes under light irradiation conditions. Guided by
these insights, we developed a broadly applicable denitrative
functionalization protocol for π-extended arenes that proceeds
without the requirement of prior electronic activation. The
synthetically practical and scalable reaction is able to deliver
the products that are readily diversified in downstream
transformations. This work establishes an excited-state
manifold as a mechanistically distinct platform for S
N
Ar
reactivity, enabling rational nucleophile selection and extend-
ing denitrative substitution to structurally diverse polycyclic
arenes.
2. RESULTS AND DISCUSSION
2.1. Reaction Mechanism of Denitrative Chlorination:
Excited-State S
N
Ar
Despite the low reactivity of photoinduced denitrative
chlorination of nitroarenes (5% yield, Scheme 1C), its
potential for enabling excited-state substitution reactions
prompted our density functional theory (DFT) mechanistic
investigation to inform the development of more efficient
denitrative substitutions. As demonstrated in Figure 1A, the
denitrative chlorination of ground-state nitrobiphenyl (S
0
) via
a concerted S
N
Ar mechanism requires overcoming a
prohibitively high activation barrier of 49.3 kcal/mol, which
is related to the dearomatization feature of the transition state
(
1
TS0). Upon photoexcitation, nitrobiphenyl is promoted to
its singlet excited state (S1, Figure S3), followed by an
intersystem crossing (ISC, Table S2) to afford biradical triplet
species T
2
. T
2
then undergoes internal conversion (IC) to form
the lowest triplet-state species T
1
, which further forms van der
Waals complex
3
IM1 with the chloride. Subsequent concerted
S
N
Ar of
3
IM1 occurs with an activation barrier of 28.7 kcal/
mol, which is more favorable than that of ground state S
N
Ar by
20.6 kcal/mol.
The significantly lower barrier of the excited-state S
N
Ar
reaction could be attributed to two major factors. First, the
excited-state S
N
Ar is facilitated by the enhanced electrophilicity
of the ipso-carbon C4 in T
1
due to intramolecular charge
transfer
44,45
and π-electron density reorganization of the
nitrobiphenyl during the excitation-relaxation process. This is
evidenced by the calculated Dual Descriptor
46
Δf(r) for C4 in
T
1
(0.047) and S
0
(−0.0328), which suggests that C4 changes
from nucleophilic in S
0
to electrophilic in T
1
(right panel of
Figures 1B and S4). Consistent with its electrophilic property,
NPA charge
47
and spin density analysis unveil obvious radical
cation character for C4 in T
1
(q
C4
= 0.179, ρ
C4
= 0.304).
Second, the excited-state S
N
Ar is driven by aromaticity
recovery. We performed aromaticity analysis
48−52
on the key
structures along the reaction coordinate (Figure S5). Figure 1
presents the bifurcation value (DBV) of the electron
localization function (ELF), an aromaticity scale (aromatic:
DBV > 0.70; nonaromatic: DBV = 0.55−0.70; antiaromatic:
DBV < 0.55) defined in previous studies.
52−54
In T
1
, the
nonsubstituted phenyl ring (Ph1) and nitro-substituted phenyl
ring (Ph2) were identified as nonaromatic (DBV = 0.61,
Figure 1B, left and Table S3) and antiaromatic (DBV = 0.51,
Figure S5),
48−52
distinct from S
0
involving two aromatic
phenyl rings. In
3
IM1, the aromaticity of Ph1 (DBV = 0.64) is
partially recovered via partial charge transfer (Δq = 0.423)
from Cl
−
to nitrobiphenyl. With further electron transfer from
Cl
−
in
3
TS1, Ph1 becomes aromatic (DBV = 0.73). Finally,
Ph2 becomes aromatic when the nitro group is replaced with
Cl in
3
IM3. Overall, the S
N
Ar process of T
1
gradually recovers
the aromaticity of the two phenyl rings, differing from the S
N
Ar
of S
0.
In conclusion, the computational study unveils that the
denitrative chlorination reaction occurs via exited-state S
N
Ar
process, which is facilitated by the enhanced electrophilicity
and driven by aromaticity recovery.
55,56
2.2. Computational Identification of Nucleophile
Candidates
Based on the unveiled reaction mechanism, we further seek to
develop more efficient denitrative substitution reactions. As
computational analysis revealed, the excited-state S
N
Ar process
gradually restores the aromaticity of the phenyl rings via
electron donation from the nucleophile; thus, the electron-
transfer capacity of the nucleophiles may influence the reaction
pathway. To test this hypothesis, we first calculated the charge
change of nucleophile in
3
IM1 (Δq
Nu
) for 16 representative
carbon, hydrogen, halogen, oxygen, nitrogen, and sulfur
nucleophiles
57
(R is the methyl group in relevant nucleo-
philes). The computational results demonstrated that Δq
Nu
exhibits high correlations with the oxidation potential (R
2
=
0.86, Figure S6) and vertical ionization potential (R
2
= 0.80,
Figure S6), indicating that the charge transfer trend is related
to ground state properties of the nucleophiles. As shown in
Figure 2A, I
−
, Br
−
, RCOO
−
, F
−
, and CN
−
could transfer partial
charges (Δq
Nu
< 0.6) to the substrate, similar to Cl
−
. While,
other nucleophiles could transfer a single electron to T
1
(Δq
Nu
> 0.7), which may enable the electron-transfer promoted
S
N
Ar,
58
a distinct mechanism compared to the two-electron-
transfer process observed for Cl
−
. To test this possibility, we
analyzed the substitution reaction with RNH
−
. As depicted in
Figures 2B and S5, the single electron transfer of RNH
−
to T
1
generates
3
IM1′ in which Ph1 nearly recovers aromaticity
(DBV = 0.67, Figure S5) and Ph2 partially recovers aromaticity
(DBV = 0.58). The nitrobiphenyl in
3
IM1′ may further couple
with RNH
•
radical to form the σ-complex
3
IM3′�a
Meisenheimer complex analogue with delocalized radical�
Figure 2. continued
transition states. (C) Evaluation of relative reactivities. For Nu
−
with Δq
Nu
> 0.7, when ΔG
3IM3′
< ΔG
T1
, ΔG
3IM3′
= G
3IM3′
− G
3IM1′
; else ΔG
3IM3′
=
G
3IM3′
− G
T1
.
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
D
and finish the substitution in a stepwise manner (stepwise path
I). This proposed mechanism is supported by the two-
dimensional potential energy surface (PES, Figure 2C) scan,
which identifies two saddle points separated by the σ-complex.
Further DFT optimizations (Figures S7 and S8) confirm that
these saddle points correspond to the transition states (TSs) of
nucleophile addition (
3
TS1′) and nitro group dissociation
(
3
TS2′), respectively. On the other hand, the two-dimensional
PES of the denitrative chlorination reaction locates the saddle
point of the concerted pathway. Meanwhile, it identifies two
additional saddle points corresponding to the TSs of nitro
radical dissociation (
3
TS1) and nucleophile addition (
3
TS2).
This alternative stepwise path II is calculated to have an
activation barrier (28.3 kcal/mol, Figure S13) comparable to
that of the concerted pathway. Overall, initial computational
assessments suggest that the S
N
Ar reaction may proceed via a
concerted or stepwise mechanism depending on the nature of
nucleophiles.
To further evaluate the relative reactivity of nucleophiles
toward the S
N
Ar reaction of nitrobiphenyl, we examined the
three plausible mechanisms for the reactions of all of the
nucleophiles. It was found that nucleophiles with Δq
Nu
> 0.7
are able to form a σ-complex with T
1
, while the concerted TS
and the radical complex
3
IM3 cannot be located. Thus, they
are considered to undergo the electron-transfer-promoted
stepwise S
N
Ar reaction, and their relative reactivity was
assessed by the relative stabilities of the σ-complex. These
nucleophiles were classified into two groups (Figure 2C) based
on the formation energy of the σ-complex (ΔG
IM3′
). H
−
,
59
HO
−
, RCONH
−
, RO
−
, RCOCH
2
−
, and RNH
− 60
were
classified into the more reactive group as their ΔG
IM3′
values
are relatively smaller (<15.0 kcal/mol). (RCO)
2
CH
−
, RS
−
,
HS
−
, and RC(�CH
2
)O
−
were classified into the less reaction
group due to their larger ΔG
IM3′
values (>17.0 kcal/mol).
Nucleophiles with Δq
Nu
< 0.7 were found to undergo
concerted or (and) stepwise S
N
Ar (Figures S10−S15). Their
relative reactivity was assessed using the activation barriers of
their preferred pathway (ΔG
‡
). F
−
, CN
−
, and RCOO
−
were
calculated to be more reactive than Cl
−
, while Br
−
and I
−
show
comparable reactivity with Cl
−
. Together, H
−
, HO
−
,
RCONH
−
, RO
−
, RCOCH
2
−
, RNH
−
, F
−
, CN
−
, and RCOO
−
are potentially more efficient nucleophiles for the excited-state
S
N
Ar reaction of nitrobiphenyl.
2.3. Experimental Evaluation of S
N
Ar Reactions of
Nitrobiphenyls
The experiments began by testing the 9 nucleophilic anions
identified computationally. Upon experimental optimization, 8
nucleophilic patterns successfully afforded the corresponding
substitution products under external-photocatalyst-free con-
ditions (Table 1), which were proved inactive without light. As
suggested by DFT calculations, carboxylic acid should be
compatible for denitrative substitution. However, an oxidative
decarboxylation process can occur with the presence of
nitroarene under light irradiation, thus the denitrative
substitution can be hampered
61
(see Figure S19). Further-
more, control experiments confirmed that this reaction could
still proceed without oxone, albeit with diminished yield. We
believe the role of oxone was to suppress the formation of
reduction side products or intermediates of nitroaromatics (see
Figures S26−S28 for details). Radical trapping experiments
indicated that the reaction mechanism did not proceed via a
radical pathway (see Tables S13 and S14 for details).
Starting from these model reactions, this protocol was
further expanded and demonstrated broad applicability across
arenes featuring diverse scaffolds and substitution patterns
(Figure 3). 4-nitro-1,1′-biphenyls bearing electron-withdraw-
ing groups, such as trifluoromethyl or halides at the 4′-para
position, afforded the corresponding hydrogenated products
(2, 4, 6, 8, 10, 12, and 14) in 63−72% yields. Substrates
containing biphenyl motifs were converted to the correspond-
ing products (16, 18) in 70 and 55% isolated yields,
respectively. The method also tolerated para-phenylethynyl
nitroarenes and 2-nitrothiophenes, affording hydrogenation
products (20, 22) in 72 and 48% yields. Fused ring nitroarenes
engaged effectively as well, providing substitution products
(24, 26, and 28) in approximately 70% yields. The deuterated
analogues (3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, and
29) were obtained in comparable yields to their hydrogenated
counterparts, with a yield difference of less than 10%. Notably,
the deuteration incorporation rates were higher than 95%
across all cases, even in the presence of H
2
O. Beyond hydride
sources, denitrative etherification was achieved by using a weak
nucleophile (HFIP) to afford biaryl ether products (31).
Substrates bearing heterocyclic rings (32, 33, and 37−39) or
fused ring systems (34−36) afforded the corresponding
etherification products in 45−81% yields, and 2-nitro-
thiophenes participated efficiently to deliver 40 in 75% yield.
Furthermore, monocyclic compounds including pyridine (41),
thiophene (42), benzene ring (43), and benzamide-protected
benzene ring (44) can all undergo the reaction to afford the
corresponding etherification products with 41−60% yield.
Additionally, trifluoroethanol as nucleophile afforded the
product with 75% yield (30). The scope of the protocol was
further expanded to include nitrogen-based nucleophiles for
direct denitrative functionalization. A series of primary amines,
including ethanolamine (45, 46, 49), 2-methoxyethylamine
Table 1. Experimental Identification of Computational-
Evaluated Nucleophiles
a
entry
DFT suggested
Nu
−
nucleophiles
yield
(%)
b
without
light
1
c
H
−
NaBH
4
72% nd
d
2
e
OH TBAH 74% nd
3
f
RCONH
−
CF
3
CONH
2
75% nd
4
g
RO
−
CF
3
CH
2
OH 56% nd
5
h
RCOCH
2
−
(CH
3
)
3
SiOC(CH
3
)�CH
2
14% nd
6
i
RNH
−
ethanolamine 28% nd
7
j
CN
−
acetone cyanohydrine 70% nd
8
k
F
−
TBAF·H
2
O 15% nd
a
Reactions were conducted in 0.10 mmol under 390 nm LEDs with
argon.
b
Isolated yield.
c
1 (1.0 equiv), NaBH
4
(2.0 equiv), H
2
O (2.2
equiv), oxone (2.0 equiv), MeCN (0.10 M), r.t., 12 h.
d
nd, not
detected.
e
1 (1.0 equiv), TBAH (3.0 equiv), MeCN (0.10 M), r.t., 48
h.
f
1 (1.0 equiv), CF
3
CONH
2
(3.0 equiv), Cs
2
CO
3
(4.0 equiv), oxone
(1.0 equiv), MeCN (0.10 M), 75 °C, 48 h.
g
1 (1.0 equiv),
CF
3
CH
2
OH (10.0 equiv), K
3
PO
4
(5.0 equiv), oxone (1.0 equiv), 1,2-
dichloroethane (0.050 M), no fans, 24 h.
h
1 (1.0 equiv),
(CH
3
)
3
SiOC(CH
3
)�CH
2
(3.0 equiv), MeCN (0.10 M), r.t., 24 h.
i
Ethanolamine (2.0 equiv), trifluoroethanol (0.050 M), 75 °C, 24 h.
j
1
(1.0 equiv), acetone cyanohydrin (1.1 equiv), BTMG (1.2 equiv),
MeCN (0.10 M), r.t., 12 h.
k
1 (1.0 equiv), TBAF·H
2
O (4.0 equiv),
MeCN (0.10 M), 75 °C, 48 h.
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
E
Figure 3. Experimental design for proposed reaction patterns. Reactions were conducted in 0.10 mmol under 390 nm LEDs.
a
NaBH
4
(2.0 equiv)
or NaBD
4
(2.0 equiv), H
2
O (2.20 equiv), oxone (2.0 equiv), MeCN (0.10 M), r.t, 12 h.
b
HFIP (10.0 equiv), K
3
PO
4
(5.0 equiv), 1,2-dichloroethane
(0.05 M), oxone (1.0 equiv), no fans, 24 h.
c
CF
3
CONH
2
(3.0 equiv), Cs
2
CO
3
(4.0 equiv), oxone (1.0 equiv), MeCN (0.10 M), 75 °C or
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
F
(47), boc-protected amines (48), isobutylamine (50), and
pivalamine (51), were successful nucleophiles to produce the
corresponding aminoarenes in 28−66% yields, respectively.
Secondary amines failed to give out substitution products but
reduced nitroarene directly to aniline derivatives because of
their relatively stronger reducing ability. Trifluoroacetamides
also proved compatible, delivering C−N bond coupling
products without detectable C−O bonding byproducts (52).
Both electron-deficient nitroarenes (53) and electron-rich
(54−57) underwent denitrative amination, providing the
products in varying yields from 36 to 72%. Most importantly,
for monocyclic systems, acetyl (Ac)-protected nitroanilines
(58), as well as nitropyridines (59), can also afford the target
products. Nonfluorinated substituted alcohols or amides were
unsuccessful substrates because of the need of stronger base to
generate O/N based anion nucleophiles. However, such bases
can likely react with the acidic C−H bond on the ortho
position of the nitro group, thus leading to side reactions.
Finally, the protocol was expanded to other nucleophiles such
as tetrabutylammonium hydroxide (TBAH). Hydroxy- and
fluoro-biphenyl derivatives (60−63) were obtained in 42−74%
yields. The methodology was also applicable to the
polyaromatic ring, affording hydroxylated pyrene (64).
Trifluoromethoxylation (65), fluorination (66), enolization
(67), and cyanation (68−70) were also accomplished, albeit in
lower yield. Dissociated fluoride as well as enolate are
supposed to exist at a relatively lower concentration in the
reaction mixture, leading to lower conversion of denitrative
substitution. Trifluoromethoxide can decompose gradually,
62
therefore the yield of the substitution product is low. Those
experiments were then extended to models predicted as less
favorable, such as bromide, iodide, and so on. Most
nucleophiles were unreactive under the standard conditions
(see Figure S19), further supporting the computational model
as an effective predictor of the intrinsic reactivity of
nucleophiles. Furthermore, we carried out the reaction at
120 °C without light irradiation. For nitroarenes bearing one
more electron-withdrawing group (2, 22, 24, 30, 33, 34, 37,
38, 45, 52, 54, 55, 57, 60, 65, and 66), which are prone to
undergo a thermally induced S
N
Ar reaction, most of them
failed to give denitrative products, demonstrating fundamental
mechanistic distinction of our reaction with classical trans-
formations. To further demonstrate the applicability of the
protocol, 3.0 mmol scaled-up reactions were performed on
selected substrates, furnishing hydrogenation, etherification,
amination, and amidation products (24, 35, 37, 46, and 56) in
moderate yields (Figure 4A). Furthermore, the methodology
was successfully integrated with site-selective nitration,
enabling the consecutive modification of molecules (Figure
4B). 34 and 35 were subjected to a well-established nitration
procedure to introduce a nitro group. Subsequent denitrative
etherification and amination afforded the doubly functionalized
products 71 and 72 in 75 and 85% yields, respectively.
4. CONCLUSION
In summary, this work establishes an excited-state S
N
Ar
reaction for nitroarenes. Mechanistic studies revealed that
photoexcitation of nitrobiphenyl induces a redistribution of
electron density that transiently alters the substitution
landscape, enabling nucleophilic attack and rearomatization
without ground-state electronic penalties. Further reactivity
analysis highlights nucleophiles with favorable substitution
characteristics, which were subsequently examined and
developed experimentally. The resulting protocol proceeds
without preinstalled electron-withdrawing groups or external
photocatalysts, accommodates polycyclic arenes, and is
synthetically practical. More broadly, these findings demon-
strate that excited-state electronic reconfiguration can be
leveraged to unlock aromatic substitution pathways inacces-
Figure 3. continued
ethanolamine (2.0 equiv), trifluoroethanol (0.05 M), 75 °C, 48 h.
d
After 2 h of reaction, the starting material was completely consumed with 35%
NMR yield. 60 is converted to 2,6-dichloro-4-aminopyridine upon column chromatography purification, even in deuterated solvent.
e
TBAH (3.0
equiv), MeCN (0.10 M), r.t., 48 h.
f
Trifluoromethoxy reagent ((E)-4-(tert-butyl)benzaldehyde O-trifluoromethyl oxime) (2.0 equiv), Na
3
PO
4
(3.0
equiv), MeCN (0.10 M), 75 °C, 24 h.
g
TBAF·H
2
O (4.0 equiv), MeCN (0.1 M), 75 °C.
h
(CH
3
)
3
SiOC(CH
3
)�CH
2
(3.0 equiv), MeCN (0.10 M),
r.t., 24 h.
i
TMSCN (3.0 equiv), TBAF (4.0 equiv), MeCN (0.1 M), r.t.
Figure 4. Synthetic application of the denitrative substitution reaction. (A) 1.0−3.0 mmol scaled-up reactions. (B) Derivatization of the product 34
and 35.
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
G
sible in the ground state, opening new opportunities for light-
driven arene functionalization.
■
ASSOCIATED CONTENT
*
sı
Supporting Information
The Supporting Information is available free of charge at
https://pubs.acs.org/doi/10.1021/jacs.5c21841.
PES (ZIP)
Additional experimental and computational details,
materials, and methods, including photographs of the
experimental setup and spectral data for all compounds
(PDF)
■
AUTHOR INFORMATION
Corresponding Authors
Fei Ye − Engineering Research Center of Photoenergy
Utilization for Pollution Control and Carbon Reduction,
Ministry of Education, College of Chemistry, Central China
Normal University (CCNU), Wuhan 430079, P. R. China;
orcid.org/0000-0003-0034-3321; Email: yef@
ccnu.edu.cn
Gui-Juan Cheng − Warshel Institute for Computational
Biology, School of Medicine, The Chinese University of Hong
Kong, Shenzhen 518172, P. R. China;
orcid.org/0000-
0002-2818-2235; Email: chengguijuan@cuhk.edu.cn
Authors
Zhen Lyu − Warshel Institute for Computational Biology,
School of Medicine, The Chinese University of Hong Kong,
Shenzhen 518172, P. R. China
Tiantian Liang − Engineering Research Center of Photoenergy
Utilization for Pollution Control and Carbon Reduction,
Ministry of Education, College of Chemistry, Central China
Normal University (CCNU), Wuhan 430079, P. R. China
Complete contact information is available at:
https://pubs.acs.org/10.1021/jacs.5c21841
Author Contributions
§
Z.L. and T.L. contributed equally to this work.
Notes
The authors declare no competing financial interest.
■
ACKNOWLEDGMENTS
We thank Y. Xu (Peking University), R. C. Sang (University of
California), and G. J. Wu (Huazhong University of Science and
Technology) for helpful discussions about the project. We also
appreciate the advice provided by Y. Zhou (CUHKSZ), as well
as L. Liu (CCNU), for assistance in manuscript preparation.
We also thank the assistance of W. Y. Zhao (CCNU), J. L. Qiu
(CCNU), M. X. Han (CCNU), W. R. Sun (CCNU), F. Yang
(CCNU), and J. Zheng (CCNU) in the synthesis of substrates
and the performance of related experiments. W. H. Xu
(CCNU) for the assistance on NMR data collection, J. M.
Gong (CCNU) for the help on the IC test, L. Y. Chen
(CCNU) for electron paramagnetic resonance measurement.
Prof. W. J. Xiao (CCNU) for the help with high-resolution MS
testing. We are grateful to the Knowledge Innovation Program
of the Wuhan-Shuguang Project (2023020201020308, F.Y.);
the Cultivation Program of Wuhan Institute of Photochemistry
and Technology (GHY2023KF003, F.Y.); the Hubei Provin-
cial Natural Science Foundation of China (Grant
2022CFB682, F.Y.) CCNU for startup funding (F.Y.), the
National Natural Science Foundation of China (no. 22422110,
22573090, G.-J.C.), Warshel Institute for Computational
Biology funding from Shenzhen City and Longgang District
(LGKCSDPT2025001), and the Guangdong Basic and
Applied Basic Research Foundation (no. 2023B1515020052,
G.-J.C.).
■
REFERENCES
(1) Bunnett, J. F.; Zahler, R. E. Aromatic Nucleophilic Substitution
Reactions. Chem. Rev. 1951, 49 (2), 273−412.
(2) Shigeno, M.; Hayashi, K.; Sasamoto, O.; Hirasawa, R.; Korenaga,
T.; Ishida, S.; Nozawa-Kumada, K.; Kondo, Y. Catalytic Concerted
S
N
Ar Reactions of Fluoroarenes by an Organic Superbase. J. Am.
Chem. Soc. 2024, 146 (47), 32452−32462.
(3) Neumann, C. N.; Hooker, J. M.; Ritter, T. Concerted
Nucleophilic Aromatic Substitution with 19F
−
and 18F
−
. Nature
2016, 534 (7607), 369−373.
(4) Tay, N. E. S.; Nicewicz, D. A. Cation Radical Accelerated
Nucleophilic Aromatic Substitution via Organic Photoredox Catalysis.
J. Am. Chem. Soc. 2017, 139 (45), 16100−16104.
(5) Zhu, Z.; Wu, X.; Li, Z.; Nicewicz, D. A. Arene and Heteroarene
Functionalization Enabled by Organic Photoredox Catalysis. Acc.
Chem. Res. 2025, 58 (7), 1094−1108.
(6) Kwan, E. E.; Zeng, Y.; Besser, H. A.; Jacobsen, E. N. Concerted
Nucleophilic Aromatic Substitutions. Nat. Chem. 2018, 10 (9), 917−
923.
(7) Rohrbach, S.; Smith, A. J.; Pang, J. H.; Poole, D. L.; Tuttle, T.;
Chiba, S.; Murphy, J. A. Concerted Nucleophilic Aromatic
Substitution Reactions. Angew. Chem., Int. Ed. 2019, 58 (46),
16368−16388.
(8) Terrier, F. Rate and Equilibrium Studies in Jackson-
Meisenheimer Complexes. Chem. Rev. 1982, 82 (2), 77−152.
(9) The S
N
Ar Reactions: Mechanistic Aspects. In Modern
Nucleophilic Aromatic Substitution; John Wiley & Sons, Ltd, 2013;
pp 1−94.
(10) Miller, J. Aromatic Nucleophilic Substitution; Elsevier Publishing
Company, 1968.
(11) Chen, K.; Shi, H. Nucleophilic Aromatic Substitution of
Halobenzenes and Phenols with Catalysis by Arenophilic π Acids. Acc.
Chem. Res. 2024, 57 (15), 2194−2206.
(12) Chen, J.; Lin, Y.; Wu, W.-Q.; Hu, W.-Q.; Xu, J.; Shi, H.
Amination of Aminopyridines via Η6-Coordination Catalysis. J. Am.
Chem. Soc. 2024, 146 (33), 22906−22912.
(13) Su, J.; Chen, K.; Kang, Q.-K.; Shi, H. Catalytic S
N
Ar
Hexafluoroisopropoxylation of Aryl Chlorides and Bromides. Angew.
Chem. 2023, 135 (24), No. e202302908.
(14) Alemagna, A.; Cremonesi, P.; Del Buttero, P.; Licandro, E.;
Maiorana, S. Nucleophilic Aromatic Substitution of Cr(CO)
3
Complexed Dihaloarenes with Thiolates. J. Org. Chem. 1983, 48
(18), 3114−3116.
(15) Nitta, Y.; Nakashima, Y.; Sumimoto, M.; Nishikata, T. Directed
Nucleophilic Aromatic Substitution Reaction. Chem. Commun. 2024,
60 (96), 14284−14287.
(16) Himeshima, Y.; Sonoda, T.; Kobayashi, H. Fluoride-Induced
1,2-Elimination of O-Trimethylsilylphenyl Triflate to Benzyne under
Mild Conditions. Chem. Lett. 1983, 12 (8), 1211−1214.
(17) Im, G.-Y. J.; Bronner, S. M.; Goetz, A. E.; Paton, R. S.; Cheong,
P. H.-Y.; Houk, K. N.; Garg, N. K. Indolyne Experimental and
Computational Studies: Synthetic Applications and Origins of
Selectivities of Nucleophilic Additions. J. Am. Chem. Soc. 2010, 132
(50), 17933−17944.
(18) Allen, A. R.; Noten, E. A.; Stephenson, C. R. J. Aryl Transfer
Strategies Mediated by Photoinduced Electron Transfer. Chem. Rev.
2022, 122 (2), 2695−2751.
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
H
(19) Nevesely ́, T.; Wienhold, M.; Molloy, J. J.; Gilmour, R. Advances
in the E → Z Isomerization of Alkenes Using Small Molecule
Photocatalysts. Chem. Rev. 2022, 122 (2), 2650−2694.
(20) Großkopf, J.; Kratz, T.; Rigotti, T.; Bach, T. Enantioselective
Photochemical Reactions Enabled by Triplet Energy Transfer. Chem.
Rev. 2022, 122 (2), 1626−1653.
(21) Dutta, S.; Erchinger, J. E.; Strieth-Kalthoff, F.; Kleinmans, R.;
Glorius, F. Energy Transfer Photocatalysis: Exciting Modes of
Reactivity. Chem. Soc. Rev. 2024, 53 (3), 1068−1089.
(22) Kärkäs, M. D.; Porco, J. A., Jr.; Stephenson, C. R. J.
Photochemical Approaches to Complex Chemotypes: Applications
in Natural Product Synthesis. Chem. Rev. 2016, 116 (17), 9683−9747.
(23) Hoffmann, N. Photochemical Reactions as Key Steps in
Organic Synthesis. Chem. Rev. 2008, 108 (3), 1052−1103.
(24) Song, L.; Fu, D.-M.; Chen, L.; Jiang, Y.-X.; Ye, J.-H.; Zhu, L.;
Lan, Y.; Fu, Q.; Yu, D.-G. Visible-Light Photoredox-Catalyzed
Remote Difunctionalizing Carboxylation of Unactivated Alkenes
with CO
2
. Angew. Chem., Int. Ed. 2020, 59 (47), 21121−21128.
(25) Lu, F.-D.; Liu, D.; Zhu, L.; Lu, L.-Q.; Yang, Q.; Zhou, Q.-Q.;
Wei, Y.; Lan, Y.; Xiao, W.-J. Asymmetric Propargylic Radical
Cyanation Enabled by Dual Organophotoredox and Copper Catalysis.
J. Am. Chem. Soc. 2019, 141 (15), 6167−6172.
(26) Leng, L.; Fu, Y.; Liu, P.; Ready, J. M. Regioselective,
Photocatalytic α-Functionalization of Amines. J. Am. Chem. Soc.
2020, 142 (28), 11972−11977.
(27) Pintér, B.; De Proft, F.; Veszprémi, T.; Geerlings, P. Theoretical
Study of the Orientation Rules in Photonucleophilic Aromatic
Substitutions. J. Org. Chem. 2008, 73 (4), 1243−1252.
(28) Döpp, D. Reactions of Aromatic Nitro Compounds via Excited
Triplet States. In Triplet States II; Wild, U. P.; Döpp, D.; Du ̈rr, H.,
Eds.; Springer: Berlin, Heidelberg, 1975; pp 49−85.
(29) Fráter, G.; Havinga, E. Photosubstitution Reactions of
Nitronaphthalenes Leading to Chloronaphthalene. Tetrahedron Lett.
1969, 10, 4603−4604.
(30) Petersen, W. C.; Letsinger, R. L. Photoinduced Reactions of
Aromatic Nitro Compounds with Borohydride and Cyanide.
Tetrahedron Lett. 1971, 12 (24), 2197−2200.
(31) Vink, J. A. J.; Verheijdt, P. L.; Cornelisse, J.; Havinga, E.
Photoreactions of Aromatic Compounds�XXVI. Tetrahedron 1972,
28 (19), 5081−5087.
(32) Wubbels, G. G.; Danial, H.; Policarpio, D. Temperature
Dependence of Regioselectivity in Nucleophilic Photosubstitution of
4-Nitroanisole. The Activation Energy Criterion for Regioselectivity. J.
Org. Chem. 2010, 75 (22), 7726−7733.
(33) Letsinger, R. L.; Hautala, R. R. Solvent Effects in the
Photoinduced Reactions of Nitroaromatics with Cyanide Ion.
Tetrahedron Lett. 1969, 10 (48), 4205−4208.
(34) Inoue, F.; Kashihara, M.; Yadav, M. R.; Nakao, Y. Buchwald−
Hartwig Amination of Nitroarenes. Angew. Chem. 2017, 129 (43),
13492−13494.
(35) Kashihara, M.; Nakao, Y. Cross-Coupling Reactions of
Nitroarenes. Acc. Chem. Res. 2021, 54 (14), 2928−2935.
(36) Yadav, M. R.; Nagaoka, M.; Kashihara, M.; Zhong, R.-L.;
Miyazaki, T.; Sakaki, S.; Nakao, Y. The Suzuki−Miyaura Coupling of
Nitroarenes. J. Am. Chem. Soc. 2017, 139 (28), 9423−9426.
(37) Liang, T.; Lyu, Z.; Wang, Y.; Zhao, W.; Sang, R.; Cheng, G.-J.;
Ye, F. Light-Promoted Aromatic Denitrative Chlorination. Nat. Chem.
2025, 17 (4), 598−605.
(38) Gkizis, P. L.; Triandafillidi, I.; Kokotos, C. G. Nitroarenes: The
Rediscovery of their Photochemistry Opens New Avenues in Organic
Synthesis. Chem 2023, 9, 3401−3414.
(39) Sánchez-Bento, R.; Roure, B.; Llaveria, J.; Ruffoni, A.; Leonori,
D. A Strategy for Ortho-Phenylenediamine Synthesis via Dearomative-
Rearomative Coupling of Nitrobenzenes and Amines. Chem 2023, 9
(12), 3685−3695.
(40) Baranac-Stojanovic ́, M. Substituent Effect on Triplet State
Aromaticity of Benzene. J. Org. Chem. 2020, 85 (6), 4289−4297.
(41) Mdluli, V.; Lehnherr, D.; Lam, Y.; Ji, Y.; Newman, J. A.; Kim, J.
Copper-Enabled Photo-Sulfonylation of Aryl Halides Using Alkylsul-
finates. Adv. Synth. Catal. 2023, 365 (22), 3876−3886.
(42) Rihtars ̌ic ̌, M.; Kweon, B.; Błyszczyk, P. T.; Ruffoni, A.; Arpa, E.
M.; Leonori, D. Excited-State Configuration Controls the Ability of
Nitroarenes to Act as Energy Transfer Catalysts. Nat. Catal. 2025, 8
(12), 1361−1369.
(43) Olivier, W. J.; Błyszczyk, P.; Arpa, E. M.; Hitoshio, K.; Gomez-
Mendoza, M.; de la Pen ̃a O’Shea, V.; Marchand, I.; Poisson, T.;
Ruffoni, A.; Leonori, D. Excited-State Configuration of Nitroarenes
Enables Oxidative Cleavage of Aromatics over Alkenes. Science 2025,
387 (6739), 1167−1174.
(44) Ghosh, R.; Nandi, A.; Palit, D. K. Solvent Sensitive
Intramolecular Charge Transfer Dynamics in the Excited States of
4-N,N-Dimethylamino-4′-Nitrobiphenyl. Phys. Chem. Chem. Phys.
2016, 18 (11), 7661−7671.
(45) Lee, S.; Jen, M.; Jang, T.; Lee, G.; Pang, Y. Twisted
Intramolecular Charge Transfer of Nitroaromatic Push−Pull
Chromophores. Sci. Rep. 2022, 12 (1), No. 6557.
(46) Morell, C.; Grand, A.; Toro-Labbé, A. New Dual Descriptor for
Chemical Reactivity. J. Phys. Chem. A 2005, 109 (1), 205−212.
(47) Glendening, E. D.; Landis, C. R.; Weinhold, F. NBO 6.0:
Natural Bond Orbital Analysis Program. J. Comput. Chem. 2013, 34
(16), 1429−1437.
(48) Geuenich, D.; Hess, K.; Köhler, F.; Herges, R. Anisotropy of
the Induced Current Density (ACID), a General Method to Quantify
and Visualize Electronic Delocalization. Chem. Rev. 2005, 105 (10),
3758−3772.
(49) Savin, A.; Nesper, R.; Wengert, S.; Fässler, T. F. ELF: The
Electron Localization Function. Angew. Chem., Int. Ed. 1997, 36 (17),
1808−1832.
(50) Chen, Z.; Wannere, C. S.; Corminboeuf, C.; Puchta, R.;
Schleyer, P. V. R. Nucleus-Independent Chemical Shifts (NICS) as an
Aromaticity Criterion. Chem. Rev. 2005, 105 (10), 3842−3888.
(51) Szczepanik, D. W.; Andrzejak, M.; Dominikowska, J.; Pawełek,
B.; Krygowski, T. M.; Szatylowicz, H.; Sola ̀, M. The Electron Density
of Delocalized Bonds (EDDB) Applied for Quantifying Aromaticity.
Phys. Chem. Chem. Phys. 2017, 19 (42), 28970−28981.
(52) Zhu, Q.; Chen, S.; Chen, D.; Lin, L.; Xiao, K.; Zhao, L.; Sola ̀,
M.; Zhu, J. The Application of Aromaticity and Antiaromaticity to
Reaction Mechanisms. Fundam. Res. 2023, 3 (6), 926−938.
(53) Echeverri, A.; Leyva-Parra, L.; Santos, J. C.; Gómez, T.;
Tiznado, W.; Cardenas, C. Excited State Aromaticity Unveiled by
Electron Localization Function Topology. ChemPhysChem 2025, 26
(24), No. e202500335.
(54) Santos, J. C.; Tiznado, W.; Contreras, R.; Fuentealba, P.
Sigma−Pi Separation of the Electron Localization Function and
Aromaticity. J. Chem. Phys. 2004, 120 (4), 1670−1673.
(55) Slanina, T.; Ayub, R.; Toldo, J.; Sundell, J.; Rabten, W.; Nicaso,
M.; Alabugin, I.; Galván, I. F.; Gupta, A. K.; Lindh, R.; Orthaber, A.;
Lewis, R. J.; Grönberg, G.; Bergman, J.; Ottosson, H. Impact of
Excited-State Antiaromaticity Relief in a Fundamental Benzene
Photoreaction Leading to Substituted Bicyclo[3.1.0]Hexenes. J. Am.
Chem. Soc. 2020, 142 (25), 10942−10954.
(56) Sokolova, A. D.; Platonov, D. N.; Belyy, A. Y.; Salikov, R. F.;
Erokhin, K. S.; Tomilov, Y. V. The Antiaromatic Nucleophilic
Substitution Reaction (S
N
AAr) in Cycloheptatrienyl-Anion Contain-
ing Zwitterions with a Mo ̈bius-Aromatic Intermediate. Org. Lett.
2024, 26 (28), 5877−5882.
(57) The Anionic Form Is Used for All Nucleophiles to Keep
Consistency.
(58) Rossi, R. A.; Pierini, A. B.; Pen ̃én ̃ory, A. B. Nucleophilic
Substitution Reactions by Electron Transfer. Chem. Rev. 2003, 103
(1), 71−168.
(59) BH4−, −17.0 kcal/mol, Figure S9.
(60) RNH
2
, 9.1 kcal/mol, Figure S8.
(61) Duke, A. D.; Banerjee, S.; Thupili, A. P.; Pradhan, D. R.;
Vetticatt, M. J.; Parasram, M. PCET-Enabled Decarboxylative
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
I
Oxygenation Promoted by Photoexcited Nitroarenes Chem 2026
DOI: 10.1016/j.chempr.2025.102872.
(62) Li, Y.; Yang, Y.; Xin, J.; Tang, P. Nucleophilic Trifluor-
omethoxylation of Alkyl Halides without Silver. Nat. Commun. 2020,
11 (1), No. 755.
Journal of the American Chemical Society pubs.acs.org/JACS Article
https://doi.org/10.1021/jacs.5c21841
J. Am. Chem. Soc. XXXX, XXX, XXX−XXX
J