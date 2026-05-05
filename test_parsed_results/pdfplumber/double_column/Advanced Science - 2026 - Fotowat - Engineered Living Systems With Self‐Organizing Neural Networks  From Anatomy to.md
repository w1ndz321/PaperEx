# Advanced Science - 2026 - Fotowat - Engineered Living Systems With Self‐Organizing Neural Networks  From Anatomy to

AdvancedScience
www.advancedscience.com
RESEARCH ARTICLE
Engineered Living Systems With Self-Organizing Neural
Networks: From Anatomy to Behavior and Gene Expression
Haleh Fotowat1 , 2 Laurie O’Neill1 , 2 Léo Pio-Lopez1 Megan M. Sperry2 Patrick Erickson1 Tiffany Lin2
Michael Levin1 , 2
1 Allen Discovery Center At Tufts University, Medford, Massachusetts, USA 2 Wyss Institute For Biologically Inspired Engineering, Harvard University, Boston,
Massachusetts, USA
Correspondence: Haleh Fotowat ( haleh.fotowat@wyss.harvard.edu) Michael Levin ( michael.levin@allencenter.tufts.edu)
Received: 17 May 2025 Revised: 4 February 2026 Accepted: 5 February 2026
Keywords: biorobotics | neuroengineering | plasticity | self-organizing neural nets
ABSTRACT
A great deal is known about the formation and architecture of biological neural networks in animal models, which have arrived
at their current structure-function relationship through evolution by natural selection. Little is known about the development of
such structure–function relationships in a scenario where neurons are allowed to grow within evolutionarily-novel, motile bodies.
Previous work showed that ectodermal tissue excised from Xenopus embryos, develops into a three-dimensional mucociliary
epidermal organoid ex vivo and exhibits movements distinct from age-matched tadpoles. These ‘biobots’ are autonomous, self-
powered, and able to move through aqueous environments. Here, we report a new type of biobot, the neurobot, composed of
mucociliary epidermis and neural tissue. We show that neural precursor cells implanted in explanted Xenopus ectodermal tissue
develop into mature neurons, extending processes both toward the surface and among each other. These self-organized neurobots
exhibit unique morphology, more complex movements, and different responses to neuroactive drugs compared to non-neuronal
counterparts. Calcium imaging confirms neuronal activity in neurobots. Transcriptomics reveals increased transcript variability,
expression of genes related to nervous system development, a shift toward ancient genes, and up-regulation of neuronal genes
linked to visual perception.
1 Introduction induced eyes in the tails of Xenopus tadpoles have been shown
to confer light sensitivity to otherwise eyeless hosts [ 5 ]. What
Sensing cues from the environment and translating them into are the limits of neuroplasticity in developing nervous systems?
appropriate responses is the fundamental function of the nervous And how might wild-type neurons establish coherent patterns
system in all animals. Critically, nervous systems endow animals and functional circuits when placed in an entirely new motile
with the ability to generate context- and experience-dependent embodiment? Creating truly novel configurations of biological
changes in their behavior. Nervous systems are also known to be material allows us to probe the plasticity of evolutionary hard-
plastic and adapt both structurally and functionally, on a much ware to adapt on developmental (not evolutionary) timescales to
shorter timescale, to changes in sensory and/or motor effectors truly novel circumstances and has applications for regenerative
that might occur in the lifetime of an organism, for example, medicine, human augmentation, and biological engineering.
as a result of injury, amputation, or sensory deprivation [ 1–4 ].
The capacity of an animal’s nervous system to adapt to a new Two-dimensional (2D) neuronal cell cultures grown in-vitro
body plan is especially striking when the underlying sensory- provide one of the earliest demonstrations of neurons developing
motor architecture is drastically altered. For example, ectopically and functioning in a completely non-native environment. These
This is an open access article under the terms of the Creative Commons Attribution License,whichpermitsuse,distributionandreproduction in any medium, provided the original work is properly
cited.
©2026 The Author(s). Advanced Science published by Wiley-VCH GmbH
Advanced Science , 2026; 0:e08967 1of25
https://doi.org/10.1002/advs.202508967
systems have been an extremely powerful tool for studying neural needed to build a nervous system. Previous theoretical work sug-
development, modeling emergent complex neural dynamics, and gests that nervous systems evolved primarily to coordinate and
investigating disease mechanisms [ 6, 7 ]. Although 2D neuronal modulate movement rather than to support complex cognition
cell cultures are powerful and highly accessible systems, they lack [ 30, 31 ]. From this perspective, introducing neurons into biobots
the three-dimensional (3D) architecture and cellular diversity of offers a unique opportunity to test whether even nascent neural
the brain, which limits their ability to model its complex circuit circuits can shape or enrich spontaneously generated behavior,
behaviors [ 8 ]. Recent advances in stem cell biology have enabled providing an experimentally tractable platform for probing early
the creation of brain organoids, 3D self-organizing neural tissues principles of neural organization. Moreover, it may offer a way
derived from pluripotent stem cells that can model some aspects of testing hypotheses linking neurons, ciliary function, and
of human neurodevelopment in vitro [ 8, 9 ]. These structures have movement trajectories in an accessible model, which otherwise
layered neural circuits, spontaneous oscillations, early cortical- have been limited to paleontological data [ 32, 33 ]. The availability
like activity [ 10 ], have been used as a powerful tool to investigate of ciliary biobots could help test models of motion patterns
neuropsychiatric disorders [ 11 ], and been more recently shown inferred from the geometry and microstructure of trails left on/in
to have the capacity for basic forms of learning and memory [ 12 ]. sediment by Cambrian ctenophores and fossil larvae with ciliary
Both 2D neural cultures and 3D brain organoids, however, remain swimming bands [ 34, 35 ].
non-motile, lack the capacity to generate sensorimotor behaviors
on their own, and have to be interfaced with computers or robotic We show that neural precursor cells harvested from Xenopus
systems via microelectrode arrays to perform simple tasks [ 13–16 ]. embryos and implanted into biobots indeed differentiate into
Self-contained biohybrid robots powered by muscular or neu- functional neurons that extend processes both within the con-
romuscular actuation have been created by embedding muscle struct and toward its outer surface. Neurobots exhibit marked
or combinations of neurons and muscle cells within synthetic differences in morphology and behavior relative to their non-
scaffolds [ 17–20 ]. These biohybrid robots, however, are not built neuronal counterparts, suggesting the emergence of neural
exclusively using biological tissue, are not fully embodied, do not influences on movement. Transcriptomic profiling further reveals
self-assemble, and require external stimulation for propulsion. significant upregulation of genes associated with nervous system
Another related field is that of hybrots - neural structures development in neurobots compared to non-neuronal biobots
repurposed to drive engineered bodies, such as brains and fungi [ 36–39 ], including, intriguingly, genes important for processing
operating robotic vehicles [ 21–24 ]. However, engineered robotics light stimuli. Through detailed characterization of this novel
doesn’t offer the full complexity and compatibility of biological composite system, we establish a platform that reveals its key
tissues. features while enabling the generation of future mechanistic
hypotheses.
We sought to establish a fully biological model system in which
we could investigate the morphology and function of self-
organizing neural networks in novel motile embodiments, gain 2 Results
deeper insight into the evolutionary developmental biology of
the nervous system, and inform the design of future innervated 2.1 Neurobots Can Be Constructed by
biological robots. Here, we provide the initial characterization of Implanting Exogenous Neural Precursors Into
an inexpensive, highly-accessible, self-assembling biobot model Xenopus Ectodermal Explants
to answer fundamental questions about the persistence, mor-
phology, and functional impact of wild-type neural cells in a To characterize the structure and function of nervous systems
non-standard body and identify possible sensory or behavioral that self-assemble within a novel embodiment, we established
endpoints for future investigation. an experimental procedure for implanting biobots with neural
precursor cells during the first few minutes of their formation. As
When ectodermal tissue is excised from the animal pole of a late shown previously, biobots can be constructed by excising tissue
blastula stage Xenopus embryo, and allowed to develop ex vivo , from the animal hemisphere of a Nieuwkoop and Faber stage
it will develop into a self-motile, self-powered 3D mucociliary 9 Xenopus laevis embryo (animal cap). Over the course of 30
epithelial organoid [ 25, 26 ], which we will refer to herein as minutes, the excised tissue gradually heals, initially forming a
biobot. These biobots express the four cell types normally present “bowl” shape before closing into a spherical structure [ 25 ]. We
in the embryonic skin of Xenopus tadpoles. These include mul- used this brief time window before tissue closure to introduce
ticiliated cells (MCCs), mucus-secreting goblet cells, ionocytes neuronal precursor cells into the interior of the healing tissue
that regulate ionic homeostasis of epidermis, and small secretory (Figure 1a (i, ii)-top left panel).
cells (SSCs) [ 27, 28 ]. MCCs function as motor effectors, generating
flow through the spontaneous beating of their cilia. As a result, To obtain neural cells, we took advantage of the fact that if
these biobots are capable of navigating aqueous environments, the animal cap is excised and dissociated at the late blastula
generating a suite of stereotyped movement trajectories and to early gastrula stage, and the dissociated cells are allowed to
velocities [ 25 ]. Ciliary beating frequency is thought to be under remain separated for 3 hours or more, they will assume a neural
serotonergic control, with the SSCs secreting serotonin and fate [ 40, 41 ]. To generate aggregates of neural precursors, we
stimulating an increase in ciliary beating frequency through dissociated animal caps from approximately 50 embryos, allowed
serotonergic receptors expressed on MCCs [ 29 ]. the cells to remain separated for 3 hours, and then reaggregated
them. Clumps of these reaggregated cells were subsequently
Building upon this knowledge, we set out to explore what would placed inside a freshly excised animal cap prior to its full closure
happen if we provided these biobots with the raw materials (Figure 1a (i, ii), top left panel, see Methods). Within 30 minutes
2of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 1 Construction and development of a neurobot. (a) Neural precursor clumps were placed in the center of an animal cap “bowl”, excised
from the animal pole of a Xenopus laevis embryo before it fully closed during healing. The composite forms gradually into first a sphere and then a more
elongated shape, which is mobile by Day 3. (b) Top panels: examples of two neurobots, one more rounded than the other. Bottom panel: Roundness
Index (RI) was calculated by fitting an ellipse on the image of the bot and calculating the ratio between the minor and major axes. Neurobots tended to
be less rounded than biobots (Kruskal–Wallis test, p = 0.047). (c) Neurobots were significantly larger than biobots (Kruskal–Wallis test , p = 0.0007). The
central line on the box plot shows the median, and the bottom and top edges of the box indicate the 25th and 75th percentiles, respectively. The whiskers
show the extent of the extreme data points not considered outliers, and the outliers are shown using the ‘ + ’ symbol.
the formed composite assumes a spherical shape, and by the that the implanted neural precursor cells indeed differentiate
second day, it is fully healed (Figure 1a (ii), top right panel). As into neurons (Figure 2 ). The neurons extend their processes not
with non-neuronal biobots, by the third day, multiciliated cells only within the neurobot, but also toward the outer surface (see
start appearing on their outer surface, and the bots start moving arrows in Figure 2c,d ). Such projections toward the cells lining the
around in the dish. Similar to biobots, neurobots have a lifespan surface of the bot suggest the possibility of neurons modulating
of about 9–10 days without being fed, and survive by consuming the activity of surface effectors including multiciliated cells
maternal yolk platelets present in all early Xenopus embryonic and/or the activity of those that modulate the ciliary beating
tissue [ 25 ]. frequency, for example, small secretory cells.
Comparison of the gross morphology of neurobots and biobots In a subset of neurobots, we performed co-labeling with acety-
revealed that, by Day 6, neurobots tend to exhibit a more lated α-tubulin and microtubule-associated protein 2 (MAP2).
elongated shape than biobots and become significantly larger MAP2 preferentially labels neuronal cell bodies and dendrites
(Figure 1b,c ). To investigate whether the difference in size and and is absent from axons [ 42 ], whereas acetylated α-tubulin is
elongation is simply due to implanting the animal caps with most abundant in stable microtubules within proximal axons and
additional cells, we generated a third type of bot (sham neurobots) present at lower levels in dendrites [ 43 ]. We observed clear MAP2
in a manner similar to neurobots, except that the implanted cells expression in neurobots, with distinct and partially overlapping
were not allowed to remain separated for 3 hours. Instead, they labeling patterns between MAP2 and acetylated α-tubulin. This
were reaggregated shortly after dissociation (within 30 minutes) differential distribution suggests that neurobots develop both
to prevent the induction of neural fate. We found that the sham axonal and dendritic compartments (Figure 3a–c ).
neurobots were not elongated and did not show a significant
size difference compared to biobots (Figure S1a,b ). These results To evaluate the presence of synaptic structures, we co-labeled
suggest that the elongation and increase in size may be due to neurobots with an anti-synapsin-1 antibody, which serves as
neuronal growth within neurobots. a presynaptic marker by labeling synaptic vesicles. Numerous
synapsin-1-positive puncta were detected throughout the neu-
robots, frequently colocalizing with regions positive for acetylated
2.2 Implanted Neural Precursor Cells α-tubulin (Figure 3d–f , Secondary-antibody-only control: Figure
Differentiate Into Neurons, Making Projections S2 ). This overlap suggests that stable microtubule-rich processes
Within the Neurobot as Well as Toward the Cells in the neurobots contain presynaptic specializations or vesicle
Lining the Outer Surface clusters, consistent with the formation of putative synaptic
contacts.
To determine whether the implanted cells had indeed differen-
tiated into neurons, we fixed and stained the neurobots with an There was considerable variability in the pattern of neural
antibody that specifically binds to acetylated α- tubulin, which is growth among different neurobots. No two neurobots showed
abundantly present in neurons and multiciliated cells (see Meth- identical neural architecture (Figure S3 ). This is not surprising
ods; neurons and multiciliated cells are readily distinguishable given the variability of initial conditions resulting from their
from each other due to their distinctive morphology). We found manual construction and the inevitable variability of the amount
AdvancedScience,2026 3of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 2 Implanted neural precursors develop into neurons and extend their processes throughout the neurobot. (a,b) Z- projection of confocal
image stack of a neurobot labeled with acetylated α-tubulin, which stains neurons and cilia of the multiciliated cells. (b) is the staining of the same
neurobot as shown in (a) with fewer projected planes, rendering neural processes inside the bot visible. Color code corresponds to depth within the bot
(confocal plane number). (c,d) Subregions of the same neurobot, showing neural processes projecting toward surface cells. Red shows the acetylated
α-tubulin stain, and cyan depicts a nuclear (Hoechst) co-label (Nuc). Yellow arrows point to neural processes (Neu) or multiciliated cells whose cilia are
stained (MCC). White arrows point to nuclear staining (Nuc).
of implanted tissue. This variability, however, allowed us to their expression was rather sparse (Figure S4b , green arrows;
investigate correlations between various physical and behavioral Figure S4e ). This space may therefore contain other ECM proteins
characteristics of neurobots, which we will discuss in more detail that do not form fibrils such as proteoglycans, laminins, or
in the following sections. Despite these variabilities, we found fibronectin [ 46 ]. Similarly, phalloidin staining was largely absent
that neural processes in most neurobots tended to emanate from this space and mostly overlapped with acetylated α-tubulin,
from one or more nuclear regions (labeled using a nuclear with only a few instances of differential labeling (Figure S4c,d ).
stain), presumably corresponding to the implanted clumps of These findings suggest that the space is predominantly acellular
cells (Figure 1a and Figure 2c,d ; Figure S3 ). Interestingly, these but may still contain a small number of neural processes, consis-
regions were often surrounded by regions with seemingly no tent with the observed sparse labeling of acetylated α-tubulin and
nuclear staining (Figure 2b–d ; Figure S3 ). The presence of these synapsin-1 within this region (Figure 3d–f ). Future experiments
seemingly empty spaces is intriguing. We hypothesize that these are needed to further investigate the molecular composition of
regions may be acellular, may contain support structures such this space.
as the extracellular matrix (ECM), and/or may be occupied by
neural processes that lack acetylated α-tubulin, a marker of stable
microtubules found in mature neurons but absent from immature 2.3 Neurobot Neurons Are Functional
ones. Support for the ECM hypothesis includes cases in which we
observed neurites traversing long distances in this empty space To assess whether neurons within neurobots are functional, we
along a straight line (Figure 2b , yellow arrow). built neurobots using neural cells extracted from embryos with
genetically encoded calcium indicators (GCaMP6s, see Methods);
In order to test these hypotheses, we stained neurobots with this tool is commonly used to study neural activity [ 47 ]. We used a
phalloidin dye, which stains F-actin filaments, which are present custom-built widefield fluorescence microscope with a large field
in all eukaryotic cells [ 44 ]. Additionally, we performed Second of view that enabled measurement of calcium activity in freely
Harmonic Generation imaging to assess the presence of collagen moving neurobots. Because the focal plane of the microscope was
fibers [ 45 ], which are the most common component of ECM. fixed in our setup, neural activity could only be recorded within a
Although we found some evidence for collagen fibers and puncta, single plane of focus. It was therefore critical to maintain regions
4of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 3 Immunostaining for acetylated α-tubulin, MAP2, and synapsin-1 reveals the presence of axons, dendrites, and synapses within
neurobots. (a–c) Z-projection of 11 confocal sections (total depth: 22 µm). Acetylated α-tubulin (red) and MAP2 (green) are shown as: (a) merged image,
(b) acetylated α-tubulin channel, and (c) MAP2 channel. Yellow arrowheads mark regions of overlap; white arrowheads indicate sites labeled only for
acetylated α-tubulin; pink arrows denote regions labeled only for MAP2. Scale bar, 40 µm. (d–f) Distribution of putative synapses in a neurobot. Green
puncta correspond to anti-synapsin-1 staining, red indicates acetylated α-tubulin, and blue denotes nuclei. (e) Higher magnification of the neurobot
shown in (d). (f) Enlarged view of the boxed region in (e). Scale bars, 40 µm (e) and 10 µm (f).
of interest within that focal plane, which proved challenging, regular ones. Consequently, we were unable to obtain repeated
particularly in neurobots exhibiting extensive rotational move- measurements of specific calcium activity sequences or move-
ments (See e.g., neurobot shown in Video S3 ). Neurobots with a ment patterns for statistical correlation analyses. Moreover, since
flatter, disc-like shape would be less likely to generate rotational every neurobot showed a different pattern of neural expression
movements and would therefore help maintain regions of interest (Figure S3 ), findings in one neurobot could not be reproduced
in focus [ 48 ] (see Methods). Figure 4 shows an example of and confirmed in others. An important future direction will
calcium signals recorded from a freely moving flattened neurobot, be to develop methods that enable consistent neural expression
which exhibited circular movements around its center (Video and experimental paradigms permitting repeated observation of
S1 ). Motion-corrected videos were then analyzed to extract the directional movement and controlled rotation of regular, non-
fluorescent activity (see Methods, Video S2 ). We found that the flattened neurobots. Achieving these capabilities will be essential
implanted cells indeed show calcium activity in all recorded for rigorously linking neural activity to behavior.
neurobots. We occasionally observed synchronized activity in
nearby or distant regions of interest (see e.g., arrowheads in
Figure 4c ), which may result from connectivity between these 2.4 Neurobots Tend to be More Active and Show
regions, although this could also be attributable to chance. an Increase in Their Movement Complexity,
Compared to Non-Neural Biobots
We found that keeping regions of interest in focus over longer
periods of time was still quite challenging even in flattened To investigate whether neural activity could influence bot move-
neurobots. Further, although we did not formally study the ment, we recorded the spontaneously generated movements of
impact of flattening on the movement patterns of neurobots, we both biobots and neurobots. We reasoned that if neurons exhibit
found that they were in general less likely to move compared to spontaneous and variable activity patterns, as observed in our
AdvancedScience,2026 5of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
distance traveled, the percentage of the well covered, and average
speed and acceleration (Figure S5 ). However, we found that the
minimum movement speed of neurobots was significantly higher
than that of biobots, indicating that neurobots tended to move
more than biobots, remaining idle less often.
We had observed that some bots show simpler circular movement
trajectories with relatively constant radii (e.g., Figure 5b-bot #3 ),
whereas others showed changes in their circling radius (e.g.,
Figure 5b-bot #4 ) or a generally more complex movement pattern
(e.g., Figure 5 - bot #5). More complex movement patterns in neu-
robots would support the hypothesis that neural activity may play
a modulatory role in their spontaneously generated movements.
To further investigate potential differences in the movement
patterns of neurobots and their non-neural counterparts, we used
a spectral analysis, calculating the Welch power spectral density
(PSD) of the trajectory time series along the x and y coordinates
(Figure 6a,b , two exemplar trajectories and their corresponding
time series on the x -coordinate, see Methods). We then detected
significant peaks in the x and y PSDs, summed the number of
unique peaks in x and y PSDs, and defined this number as the
FIGURE 4 Calcium imaging in freely moving neurobots shows Complexity Index (CI, Figure 6c ). In this analysis, a CI of one
that the implanted cells are indeed active. (a) Average fluorescence of a indicates a circular trajectory with constant diameter (where both
freely moving neurobot containing neurons expressing GCaMP6s after x and y PSD have one peak at the same location), and the number
motion correction (10 minutes of movement imaged at 5 frames per increases as the trajectory becomes more complex. A complexity
second). Colored circles correspond to regions of interest identified by the index of zero signifies non-moving bots. We further used a time-
suite2p software, which could be single or multiple units. (b) Movement frequency analysis (wavelet-transform) and surrogate data to
trajectory of the same neurobot. (c) The top curve shows the X-position confirm the significance of the power at the peaks identified in
of the neurobot over time. The 5 bottom curves show baseline-subtracted the Welch analysis (see Methods).
fluorescence activity of units labeled in panel (a). Arrowheads point to
synchronized activity in some nearby (two shades of blue) and more Interestingly, we found that neurobots showed a significantly
distant (red and pink) ROIs. higher degree of trajectory complexity compared to biobots
(Figure 7a ). This increased complexity could not be explained
by the roundness or size of the biobots and neurobots, as these
calcium imaging experiments, and if those neurons can modulate variables were not significantly correlated (Figure 7b,c ). The
the bot’s behavior, then neurobots should exhibit movement increased complexity of neurobots could be a result of increased
dynamics that differ from those of their non-neural counterparts. variability in the beating frequency of cilia in MCCs, changes
We Recorded the spontaneous movements of the bots in small in their spatial distribution, changes in the 3D structure of
8-well plates over 30 minute periods ( n = 46 neurobots and 48 the bot, or changes in the activity or distribution of other cell
biobots, Figure 5a , Video S3 : single neurobot moving, Video S4 : types (including neurons) that may modulate the ciliary beating
neurobots moving in an 8-well plate). We then used an automatic frequency, among other factors. When we measured this index in
tracking software [ 49 ] to measure the position of each bot at each sham neurobots, we also found an increase, albeit not significant,
video frame. Figure 5b shows the details of the 2D trajectories relative to biobots (Figure S1c ), indicating that the increased
of the 8 neurobots depicted in panel (a). There was a large complexity we observe in neurobots is at least partially due to
degree of variability in these trajectories, with some bots moving factors other than neural signaling. Like biobots, sham neurobots
in circular/oval trajectories with relatively constant diameter were more likely to show longer periods of immobility, and their
(Figure 5b , bots #3, #8); bots that followed circular trajectories minimum speeds were not significantly different from those of
varying in diameter over time (Figure 5b , bot#4); ones that made biobots (Figure S1d ). Finally, consistent with the finding that min-
more complex, sometimes spirograph-like patterns (Figure 5b , imum speed was significantly higher in neurobots (Figure 7d ), we
bots #1, #5, #6); those that were seemingly following the dish’s found that most inactive bots (Npeaks = 0) were in the biobot
boundaries (Figure 5b , bot #7); bots that circled over very small category, with 6 out of 48 (12.5%) biobots inactive, whereas only
areas (Figure 5b , bot #2); and those that did not move at all one out of 47 (2.1%) neurobots was inactive.
(data not shown). Interestingly, all moving bots tended to exhibit
repeating behavioral motifs.
2.5 A Seizure-Inducing Drug Differentially
With the positional information obtained from tracking, we used Affects the Behavior of Neurobots and Biobots
custom Python code to extract 4 kinematic parameters from
the bots to compare neurobots with biobots. These were the To further investigate whether neural activity could play a role in
total distance travelled, average speed, average acceleration, and modulating trajectory complexity, we performed pharmacologi-
the percentage of the well that was traversed in 30 minutes cal experiments, treating groups of neurobots and biobots with
(see Methods). We found no significant difference in the total entylenetetrazole (PTZ), a GABA
A
receptor antagonist used for
6of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 5 Neurobots show diverse and periodic patterns of spontaneous movement. (a) Exemplar trajectories of neurobots moving in an 8-well
plate over a 30-minute trial. (b) Details of the trajectories of the same bots as shown in panel (b). The color gradient indicates time during the trial.
FIGURE 6 The number of peaks in the power spectral density was used to quantify the complexity of movement trajectories. (a) Examples of
simple (top panel) and complex (bottom) trajectories. (b) Time series of the movement amplitudes projected on the x -axis. (c) Power spectral densities
corresponding to time series in panel (b) Red stars mark the location of significant peaks.
its seizure-inducing effects in animal studies [ 50 ]. Although we dishes containing 15 mM PTZ. To get an estimate on the baseline
do not know the identity of neuronal constituents of neurobots, complexity index and account for potential variability due the
we reasoned that a positive result, for example, an increase in transferring, we followed the experimental protocol depicted in
the complexity index after PTZ treatment, could be an indirect Figure 8a .
indication of the presence of GABAergic control of movement. To
test this, we performed experiments in which we video recorded The behavior of bots (16 neurobots and 16 biobots) was video
the movement of neurobots and biobots in regular media and recorded for 30 minutes in 8-well plates filled with regular media
compared the complexity indices after they were transferred to (control 1), after which the bots were transferred to the second
AdvancedScience,2026 7of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 7 Neurobots show differences in movement patterns compared to biobots. (a) Neurobots have more complex trajectories than biobots
(Kruskal–Wallis test, p = 0.039), and (b) this complexity is not correlated with their roundness (Pearson correlation coefficient = − 0.15, two tailed t -test
t (45) = 45, p = 0.2), or (c) their area (Pearson correlation coefficient = − 0.03, two tailed t -test t (df) = 45, p = 0.76). (d) Neurobots were more likely to be
active (have non-zero minimum speed) than biobots (Kruskal–Wallis test, p = 0.037).
and third sets of dishes containing regular media (control 2, we found a significant difference between neurobots and biobots,
control 3). The bots were then transferred to dishes containing with neurobots showing significantly higher values for relative
PTZ (Figure 8a ). For each bot, we calculated the CIs for the complexity (Figure 8b , right panel). This effect was not observed
three control conditions and used the average to calculate relative when we transferred bots to the control media a fourth time
complexity measures for PTZ and the wash. To control for non- (Figure 8c,d ), confirming that the observed effect was specific
specif ic effects that may occur upon the fourth transfer, we to PTZ. The variability of the impact of PTZ on neurobots is in
performed the same sequence of transfers for a second set of bots fact not surprising given the potential variability in the identity
(8 neurobots and 8 biobots), where the fourth transfer was into and the degree of expression of neurons (Figure S3 ). What is very
wells that contained regular media and not PTZ (Figure 8c ). interesting is the significant differential impact on the biobots
and neurobots. Because neurobots are biobots + neurons, the fact
We found that all except two biobots showed a relative decline that most of them showed an increase in their CI suggests a role
in their movement complexity while in PTZ (Figure 8b ), thereby for neural activity acting against the default inhibitory effect of
significantly reducing the CI relative to control (one-sample t - PTZ on the movement of biobots. Alternatively, neural expression
test, t (df) = 15, p = 0.009). The effect of PTZ on biobots suggests could indirectly contribute to these effects through its impact on
that PTZ may act on GABA receptors expressed by non-neuronal the expression of MCCs or other cell types present on the outer
cells or exert other off-target effects. Indeed, GABAergic receptors surface of the bots.
are present on goblet cells lining the surface of both biobots and
neurobots, which could indirectly modulate movement through
altered mucus secretion (see Discussion). 2.6 Neurobots Show Significant Differences in
the Distribution of MCCs, and Their Roundness Is
The majority of neurobots, on the other hand, showed increased Anti-Correlated With the Degree of Neural
complexity relative to control, although a few did show a decline Expression
(Figure 8b , left panel). As a result of this dichotomy in the impact
of PTZ, the average CI in neurobots was not significantly different To quantify the overall amount of neural expression and its
relative to control (one-sample t- test, t (df) = 15 p = 0.39). When we relationship with neurobot morphology and behavior, we used
compared the relative complexity after PTZ treatment, however, the confocal images of neurobots immunostained with acetylated
8of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 8 PTZ differentially impacted the movement of neurobots and biobots. (a) Experimental protocol for testing the effect of PTZ on the
movement of neurobots ( n = 16) and biobots ( n = 16). Movement of bots was measured in control media, across three transfers for 30 min. The bots were
then transferred to a dish containing 15 mM PTZ solution, and their behavior was measured for another 30 min. (b) Relative complexity was defined as
the complexity index measured while in PTZ, relative to the average complexity index measured for three consecutive controls. Although most biobots
reduced their complexity index relative to control (cyan lines: decreased complexity, purple lines: increased complexity), the relative complexity index
for neurobots was equally likely to increase or decrease (red and blue lines). The relative complexity of zero corresponds to the average CI for the three
controls (black). Filled circles indicate neurobots cultured in zolmitriptan prior to testing. Neurobots showed significantly higher relative complexity
compared to biobots (Kruskal–Wallis test, p = 0.01). (c,d) Show the results from control experiments where the PTZ treatment block was replaced with
another control step. Trajectory complexity was equally likely to increase or decrease in the absence of PTZ. There was no significant difference between
the relative complexity of biobots and neurobots (Kruskal–Wallis test, p = 0.01).
α-tubulin antibody, which labels neurons and cilia in the MCCs. ratio was calculated by dividing the area of the implanted clumps
Using this data, we traced the neural processes and quantified by that of the external shell (Figure 9c : Neu/Ect, Figure 1a (ii), see
the position of the MCCs using Imaris software (Figure 9a,b , see Methods).
Methods). In this analysis, we did not distinguish between axons
or dendrites and could not determine whether these processes Based on this analysis, we found that the total number of neuron
belonged to individual neurons. We could, however, obtain rough terminals was highly correlated with both absolute (Pearson
estimates of the total amount of neural tissue and the degree correlation coefficient = 0.9, t -test, t (df) = 20, p = 2.63e-09)
of branching by calculating the total length of neurites and the and area-normalized neural length (neurite density, Pearson
number of terminals, which were defined as the number of correlation coefficient = 0.9, t -test, t (df) = 17, p = 2.77e-06).
nerve endings, agnostic of their identity (i.e., axonal or dendritic). Interestingly, we found a significant negative correlation between
Figure 9 (top panels) shows two examples of such traces in cases neurite density and MCC expression density (Pearson correlation
of neurobots with very few and many neurites. We calculated the coefficient = − 0.6, t -test, t (df) = 12, p = 3.33e-02); neurobots
correlation between the degree of neural growth, expression of with higher neurite density tended to have lower overall density
MCCs, bot size, and shape, as well as the CI of the trajectories of MCCs. Consistent with this finding, we found that biobots
across all neurobots for which we had both behavioral and (which do not have neurons) have a significantly higher density
structural data (Figure 9c ). We also calculated the correlation of of MCCs compared to neurobots (Figure S6 , Kruskal–Wallis
all these parameters with the relative amount of neural tissue that test, p = 0.027). Additionally, we found a significant negative
was implanted on Day 1 as the neurobots were constructed. This correlation between the Roundness Index (RI) and neurites’
AdvancedScience,2026 9of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 9 Pair-wise correlations between size, shape, neural expression, and movement complexity in neurobots. (a,b) Examples of neurobots
stained with acetylated α- tubulin which labels multiciliated cells and neurons. Overlaid white curves show the neural processes traced using Imaris
software. Orange arrow heads point to exemplar multiciliated cells (a) Example of a neurobot with a high degree of innervation N
terminals
= 327,
L
Neurite
= 7635.9 mm. (b) Example of a neurobot with small degree of innervation N
terminals
= 40, L
Neurite
= 753.8 mm. (c) Pairwise correlation
between structural parameters of all stained neurobots and Complexity Index, N
terminals
= total number of endings, L
Neurite
= total length of neurites,
L
Neuritenorm
= total length of neurites normalized to area, N
MCC
= total number of multiciliated cells on the surface, N
MCCnorm
= N
MCC
normalized to area,
RI = Roundness Index, Neu/Ect = ratio of the areas of neural implant to ectoderm shell. White and yellow arrows point to the position of manually traced
neural processes and multiciliated cells. Pearson correlation coefficients are depicted for each pair. Values in red correspond to statistically significant
correlations (two-tailed Student’s t- test, P < 0.05). A robust linear regression was used for linear fits. The full model statistics are provided in Spreadsheet
S1 ).
absolute length (Pearson correlation coefficient = − 0.6, t- test, between CI and neural expression metrics although the neurobot
t (df) = 20, p = 5.09e-03), neurites’ normalized length (Pearson with the highest complexity index also had the largest number
correlation coefficient = − 0.5, t -test, t (df) = 17, p = 1.72e-02), and of terminals and neurite length (see the outlier data point in
total number of terminals (Pearson correlation coefficient = − 0.5, the panels). Similarly, we found only a small correlation (non-
t -test, t (df) = 20, p = 1.72e-02). That is, the more elongated the bot, signif icant) between the relative amount of implanted tissue and
the more neural expression, suggesting that the elongation could the degree of neural expression metrics.
be a result of neural processes growing within the neurobot. This
hypothesis is consistent with the finding that sham neurobots Previous studies showed that treatment with zolmitriptan, which
were not different from biobots in their RI (Figure S1a , Kruskal– is a selective 5-hydroxytryptamine (5-HT) 1B/1D receptor agonist,
Wallis test, p = 0.89). We did not find a significant correlation increased the degree of ectopic (but not native) neural growth in
10of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
Xenopus embryos [ 51 ]. We investigated whether this treatment We next compared the gene count variability across the samples of
would have an impact on the degree of neural growth in neu- biobots, neurobots, and sham neurobots on a gene-by-gene basis
robots, where the neurons are all ectopic. Interestingly, we found (Figure 10c–f ). We found that neurobots showed a significantly
that this treatment increased the degree of neural expression higher variability, quantified by coefficient of variation (CV,
in neurobots as well, although it did not have a significant see Methods) in their normalized gene counts (FPKM) across
effect on any of the behavioral measurements including trajectory neurobot samples, compared to both biobots and shams, and
complexity (Figure S7 ). In this group, we found a tight correlation samples of sham neurobots showed a higher variability compared
between the ratio of neural implant to ectoderm shell and total to samples of biobots (Figure 10c ). We then compared pairs of
number of terminals, as well as total neural length (Figure S7 ). groups (e.g., NB and BB) to determine the fraction of genes that
These results indicate that neurons in a neurobot behave as had a greater CV in normalized gene count in one group than
ectopic, not native, cells. Notably, 4 of the 16 neurobots in the the same gene in the other group. For the chosen pair of groups,
PTZ study presented in the previous section were cultured in genes were ranked by the mean count value across all pools of
zolmitriptan (filled circles Figure 8b ; Figure S7 ), three of which both groups, and the CV of each gene’s counts across the pools of
showed an increase in relative complexity. This result points to each group was calculated (Figure S10 , see Methods). The CV list
the possibility that this treatment may bias neural expression was split into 100 bins (percentiles) containing an equal number
toward those that respond to PTZ that is, GABAergic neurons. of genes, and the fraction of genes in the bin for which the CV
Further experiments are required to characterize the impact of of the first group was greater than that of the second group was
zolmitriptan treatment on the neural expression patterns within found and plotted.
neurobots.
We found that in all bins, more than half of the neurobot
In summary, neural growth in neurobots significantly impacts genes showed higher CV compared to the biobot and sham
their shape and the distribution of MCCs, and this growth could group (Figure 10d,f ; cyan horizontal line is at 0.5). For the sham
be potentially increased by modulating serotonergic signaling. neurobot group, genes in most, but not all bins showed higher CV
The degree to which neural expression contributes to trajectory compared to biobots (Figure 10c ). In addition, we found a trend
complexity remains elusive. The lack of observed correlation for genes with higher normalized counts showing a higher degree
between neurite growth and complexity index points to the of variability in their expression when comparing neurobots with
potential heterogeneities in cell type expression and connectivity biobots and shams (Figure 10d,f ). This pattern was significantly
profiles of neurites across neurobots. different from what is expected from chance in most bins (dark
blue bins), that is, relative to the average CV calculated across
all bins regardless of the order (orange line, see Methods). The
2.7 The Three Types of Bots Exhibit Significantly overall higher variability seen in neurobots and shams compared
Different Patterns of Gene Expression to biobots could be due to several factors. First, in both neurobots
and shams, the implanted cells are harvested from ∼ 50 embryos,
Like the structure and function of the central nervous system, whereas a biobot is made out of a single embryo. Moreover,
transcriptomes are typically viewed as products of a long evo- higher variability in the implanted bots is expected due to the
lutionary history of selection. In standard organisms, they are high variability in the size of the implants in both neurobots and
further shaped by ongoing neural inputs [ 52, 53 ]. What would the shams. However, these are likely not the only factors involved,
transcriptome of a novel construct with a nervous system look as neurobots showed significant differences in their gene count
like? With this question in mind, we next asked what changes to variability compared to shams. Neural differentiation, therefore,
default biobot transcriptomes, if any, would be induced by the likely plays an important role in the increased variability in gene
presence of neural tissue. To characterize the transcriptome of counts seen in neurobots.
neurobots and compare it to its non-neuronal counterparts (i.e.,
biobots and sham neurobots), we performed bulk RNA sequenc- Additionally, we found that neurobots included a significantly
ing of their tissue. For each bot type, four biological samples were larger number of genes that were differentially expressed relative
included (neurobots: NB1-4, biobots: BB1-4, sham neurobots: to biobots and sham neurobots (Figure 11a,b ), whereas biobots
SH1-4). Due to the small size of the bots, and, therefore, the small exhibited a smaller subset of differentially expressed genes rel-
amount of RNA, each sample comprised tissue from multiple bots ative to sham neurobots (Figure 11c ). Moreover, the number of
(see Methods). significantly upregulated genes ( p < 0.05, red dots with positive
fold change) in neurobots compared to biobots and shams (6774
We found a high degree of correlation between normalized and 6859 genes, respectively), were much higher than those
gene expression levels among all samples within each group that were significantly downregulated (red dots with negative
(Fragments Per Kilobase of transcript sequence per Millions log fold change, 3578 in neurobots vs biobots and 4010 in neu-
base pairs sequenced, FPKM [ 54 ]), indicating reliability and robots vs shams), resulting in highly asymmetric volcano plots
repeatability of the results (Figure 10a ). Moreover, we found that (Figure 11a,b ). This was not the case when comparing shams with
gene expression levels in biobots and sham neurobots were much biobots (Figure 11c , 1733 upregulated and 1429 downregulated
more correlated to one another than to neurobots (Figure 10a , see genes). These results are consistent with a gain-of-function as a
Methods). Similarly, neurobots could clearly be separated from result of neural growth in neurobots.
shams and biobots based on the principal component analysis
on the normalized gene expression value (FPKM) of all samples We next investigated which biological functions or pathways are
(Figure 10b , see Methods). significantly associated with the differentially expressed genes.
AdvancedScience,2026 11of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 10 Comparison of gene expression and its variability between neurobots, biobots, and sham neurobots. (a) Pearson correlation of gene
expression within and across groups of neurobots (NB), sham neurobots (SH), and biobots (BB). The closer the value to 1, the more similar the expression
patterns. (b) Principal component analysis of gene expression values. Each dot corresponds to one sample, which contained multiple bots of one kind.
(c) Histograms of coefficients of variation (CV) in gene counts (FPKM) in neurobots (red), biobots (blue), and sham neurobots (yellow). Neurobots
showed a significantly higher variability in their gene counts compared to both biobots and shams, and shams showed a higher variability compared
to biobots (Kruskal–Wallis test with multiple comparisons using Tukey’s honestly significant difference test; p < 0.00001). Genes with higher counts
showed a higher degree of variability in their expression when comparing neurobots with biobots and shams (d,e). Dark blue bars mark the bins where
the difference in CV was significantly different from what is expected if the ranking of genes were randomly shuffled. Similarly, genes with low levels of
expression showed lower coefficient of variation than expected by chance. The p -value of each bin was defined as the proportion of the bin fractions from
the distribution that were further in absolute value from the distribution mean than the true bin fraction. Bins with p -values of p < 0.05 were deemed
statistically significant and were colored dark blue. All other bins were colored light blue. The mean bin value from the distributions was plotted as an
orange line. (f) Same as (d,e) but comparing neurobots with shams. Bin values above 0.5 (light blue line) indicate that more than half of the CVs in that
bin had higher values in that comparison.
We used Gene Ontology (GO) enrichment analysis to annotate proteins involved in the regulation of Wnt and TGF-beta signaling
genes to biological processes (bp), molecular function (mf), and which is expressed in the Spemann organizer [ 55 ]. This suggests
cellular components (cc). Due to the large number of upregu- that the presence of neurons might exert an organizational
lated genes in neurobots, we focused on the highly overexpressed influence on the surrounding soma; this molecular signature
genes for this analysis (4 log-fold or more increase in expression, is consistent with known roles of the nervous system to direct
2445 genes when comparing neurobots to biobots and 2026 genes cell behavior in cancer suppression [ 56–58 ], regeneration [ 59 ],
when comparing neurobots to shams). The most significantly and embryonic morphogenesis [ 53, 60 ]. Trans-synaptic signaling
upregulated pathways in neurobots relative to biobots, as well and neurotransmitter receptor activity were also significantly
as in neurobots relative to shams, related to nervous system upregulated in neurobots. This included glutamatergic, GABAer-
development, and synapse and neuron projection (Figure 12a,b ). gic, cholinergic, dopaminergic, serotonergic, and glycinergic
One of the interesting genes we found up-regulated specifically receptors. Surprisingly, exclusively in neurobots, we also found
in neurobots relative to biobots and shams is Dact-4 , a member significant enrichment in pathways involved in visual perception
of an evolutionarily conserved family of Dishevelled-binding (Figure 12a ).
12of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 11 Distribution of differentially expressed genes between different bot groups. (a–c). The X -axis shows the fold change in gene expression
between samples of different groups, and the Y- axis shows the statistical significance of the difference. Red dots represent genes that were significantly
up (positive values on the X -axis) or downregulated (negative values on the X -axis); green dots represent genes with no significant change. Statistics
were evaluated by DESeq2, which employs the two-sided Wald test. Multiple hypothesis testing corrections were used to obtain adjusted p -values. Red
circles represent genes with adjusted p- values that were statistically significant ( p < 0.05).
Although pathways relating to neuron projection and trans- Neurobots contained genes encoding various neurotransmitter
synaptic signaling were slightly upregulated in sham neurobots receptors including glutamate (e.g., gria1-4 ), kainate receptors
compared to biobots, there were far fewer genes in each pathway, (e.g., grik1,2,3,5 ), GABAergic (e.g., gabara3,5; gabarb3 ), and
and they were less significant in their degree of upregulation glycinergic receptors (e.g., glra3; glrb ), genes encoding volt-
compared to those in neurobots (Figure S8a ). Further, there were age gated calcium channels ( cacng3,4,5,7,8 ), as well as those
relatively fewer genes downregulated when comparing neurobots involved in the uptake of neurotransmitters (e.g., slc1a1,2,3 ).
with biobots, and shams (63 and 116 genes respectively), and Genes with important roles in synaptic plasticity were also
very few genes were significantly downregulated by 4-log folds present in neurobots ( arc, camk2b , Cluster 15, Figure 13 , see
when comparing shams with biobots (38 genes). Our enrichment the NB vs. BB tab in Spreadsheet S2 ) [ 52 ]. Cholinergic and
analysis showed that the largest group of downregulated genes muscarinic ( chrna2,3,4,5,7; chrnb2,3,4, chrm2,4,5 ), serotonergic
in neurobots compared to biobots belonged to the cellular ( htr1a,b,e ; htr2a ), and dopaminergic ( drd1,2,4 ) were among other
component pathway (extracellular region in Figure S8b ). Inter- neurotransmitter receptors (Cluster 23, Figure 13b , see the NB vs
estingly, this pathway includes some of the genes expressed in the BB tab in Spreadsheet S2 ).
Xenopus skin, including glycoprotein 2 ( gp2 ), and mucin ( muc17 )
suggesting that the properties of the “skin”of neurobots might be Notably, one of the largest clusters (Cluster 1) contained genes
different from those of biobots. encoding various aspects of visual perception, phototransduction,
and photoreceptor development (Figure 13c , see the NB vs. BB
In order to identify functional biological modules of differen- tab in Spreadsheet S2 ). Specifically, this cluster included red
tially expressed genes, we extracted the largest protein–protein- and violet cone opsins ( opn1lw, opn1sw ), retinal G-protein couple
interaction (PPI) sub-network of these genes using the STRING receptors ( rgr ), melanopsin ( opn4, opn5 ), rhodopsin ( rho ), as well
database. We then performed network embedding and clustering as many other related genes that encode proteins involved in
using multi-nonnegative matrix factorization (MNMF) [ 61 ] to visual processing. In addition to Cluster 1, Cluster 12 (Figure
find specific functional biological modules. The clusters were S9c ) also included genes related to eye, lens, and retina devel-
subsequently enriched using g: Profiler [ 62 ]. Based on this opment, including genes found in major retinal cell types [ 63 ],
analysis, we identified 25 clusters for neurobots vs biobots that is, retinal ganglion cells ( neurod1,2; pou4f1 ), and horizontal
comparison and 5 clusters in neurobots vs sham neurobots cells ( onecut1, lhx1 ). Genes found in bipolar cells ( unc5d ), and
comparison (Spreadsheet S2 , Figures S9 and S10 ). There were amacrine cells ( prdm13 ) were also present in Clusters 21 and 22,
not enough upregulated genes between biobots and sham neu- respectively (Figure S9d,e , see the NB vs. BB tab in Spreadsheet
robots to allow for this analysis. Similarly, due to the low S2 ), suggesting that neurobots could potentially sense and process
number of downregulated genes, the network analysis could not light stimuli.
be performed at either a 4-fold or a 2-fold change threshold
level. Many other clusters included significant enrichment in genes
encoding various aspects of the nervous system. This included
Consistent with the findings from the enrichment analysis, we Cluster 5, which contained various synapsins, tubulins, and
found clusters containing genes critical for the development of microtubule-associated proteins, which are implicated in biolog-
the nervous system, cell fate commitment, and wnt signaling ical processes such as the synaptic vesicle cycle, neuron devel-
pathways (Cluster 3, Figure S9a , see the NB vs BB tab in opment, regulation of neurotransmitter secretion, and synaptic
Spreadsheet S2 ). A plethora of growth factors (e.g., various FGFs, vesicle localization (Figure S9f , see the NB vs. BB tab in
BDNF, and EGF), and their receptors were revealed by Cluster Spreadsheet S2 ). Cluster 9 revealed the presence of voltage-gated
17, which also showed enrichment in enzyme-linked receptor ion channels including various types of sodium and potassium
protein signaling pathways (Figure S9b , see the NB versus BB tab channels as well as voltage-gated calcium channels (Figure S9g ,
in Spreadsheet S2 ). see the NB vs. BB tab in Spreadsheet S2 ). Cluster 11 contained
AdvancedScience,2026 13of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 12 Enrichment analysis performed using Gene Ontology annotations on differentially expressed genes with at least 4-log fold
upregulation in expression. (a) neurobots versus biobots (b) neurobots versus shams, BP: Biological processes, CC: Cellular Components, MF: Molecular
Function.
genes encoding various G-protein coupled receptors, as well Moreover, we found that there was significant upregulation in
as those implicated in the modulation of chemical synaptic genes encoding ECM constituents (Figure 12a , Cluster 20, and
transmission (Figure S9h , see the NB vs. BB tab in Spreadsheet Figure S9j , see the NB vs. BB tab in Spreadsheet S2 ) including
S2 ). Cluster 14 revealed the presence of various hormones and collagen ( col17a, col4a2 ), which is the most abundant fibrous
neuropeptides and their receptors (Figure S9i , see the NB vs. BB protein and constitutes the main structural element of ECM [ 46 ],
tab in Spreadsheet S2 ). Cluster 21 included genes important for and fibulins [ 64 ], which are glycoproteins that are secreted in the
axonogenesis and neuron projection development (Figure S9d , ECM and provide mechanical support in connective tissue ( fbln1 ).
see the NB vs. BB tab in Spreadsheet S2 ). Our Second Harmonic Generation imaging indeed showed the
14of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 13 Cluster-based network connectivity patterns among genes that were upregulated in neurobots compared to biobots. (a) Cluster 15 (b)
Cluster 23 (c) Cluster 1. Network connectivity was calculated using the STRING online tool. The edges indicate both functional and physical protein
associations the line thickness indicates the strength of data support. Only nodes with interaction scores with confidence higher than 0.4 are shown.
Nodes of special interest are highlighted in color.
AdvancedScience,2026 15of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
presence of some collagen fibers within the central cavity of precursor cell clumps (due to the manual nature of their cre-
neurobots, although they were only detected at very low levels ation), could be a major contributing factor to the variability in
(Figure S4 ). Future experiments are required for assessing the neural growth and patterning. Indeed, we found a small positive
presence of fibulins and other potential constituents of the ECM correlation between the relative size of the implanted tissue and
in this space. the resulting neurite length and number of neural terminals
(see Figure 9c ). Another source of variability may stem from
As expected, network embedding and clustering analysis of the need to pool neural precursors from multiple embryos to
the upregulated genes in neurobots relative to shams similarly generate sufficiently large neuronal clumps for manual implanta-
revealed overexpression of genes relating to synapse organization, tion. Consequently, the individual cells within each clump were
regulation of neurotransmitter and receptor activity, chemical unlikely to be genetically identical and may have differed slightly
synaptic transmission (within Clusters 4,5), visual perception in their developmental stage. Developing automated methods
(within Cluster 3), neuron projection, and perineuronal nets to implant a defined number of cells, ideally derived from the
(within Cluster 2, Figure S10 ). These findings shed light on bio- same embryo, will facilitate more accurate quantification of
logical pathways/molecular functions that are innately present the relationship between implant size and subsequent growth,
in neurobots in the absence of any external manipulations and and will likely reduce variability across neurobots. Efforts are
will inform future work toward building specialized neurobots underway to develop robot scientist platforms for the field of
through selective enhancement of these pathways. synthetic morpho-engineering.
Finally, we tested the hypothesis that neurobots are expressing a We found that the majority of neural processes emanating
more ancient transcriptome as a result of their nascent evolution- from the implanted neural precursor clumps grew within the
ary history. We applied a phylostratigraphic analysis for the dif- central cavity of the bot. However, some processes clearly
ferentially expressed genes in the different conditions (Figure 14 , extended toward the outer epithelium (arrowheads Figure 2 ;
NB vs SH and NB vs BB). Interestingly, we found that more than Figure S3 ). Future experiments will investigate more thoroughly
54% of upregulated genes in neurobots fall into the two categories how neurons modulate the activity of outer epithelial cell types,
of most ancient genes (“All living organisms”and “Eukaryota”, including multiciliated cells, goblet cells, and serotonergic cells.
Figure 14a ). By comparison, very few ancient genes are downreg- For example, optogenetic activation of neurons combined with
ulated. In total 279 genes are downregulated in these two strata imaging of fluorescent microbead flow patterns could be used to
for the NB vs BB conditions, and 233 for the NB vs SH condition test the causal relationship between neural activity and ciliary
(Figure 14b ), while for the upregulated genes, we obtained 941 and beating frequency. When paired with genetic knockdown of
1109, respectively. Therefore, we conclude that the development relevant cell-surface receptors, such as serotonergic receptors
of neurobots involves a transcriptomic shift toward very ancient [ 29 ], such approaches could help elucidate the mechanisms by
genes for neurobots compared to biobots and shams. which neurons influence movement in neurobots. It is important
to note that, unlike in some invertebrates where ciliary beating
frequency, and thus cilia-driven movement, is under neural
3 Discussion control [ 32 ], the beating frequency of MCCs on tadpole skin has
not been shown to be under neural control. Instead, it is thought
In this study, we built and investigated behavioral, anatomical, to be controlled by molecules secreted by other epithelial cells
and transcriptional properties of novel living constructs with for example, serotonin (through small secretory cells) [ 29 ], and
incorporated neural tissue. Using Xenopus laevis embryonic cells, may also be controlled by factors known to influence beating
we built two types of living constructs: one using ectodermal cells frequency of motile cilia in other mucociliary epithelia such as
(biobots) as reported in prior studies [ 25, 48, 65 ], and another, extracellular ATP molecules secreted in the context of injury
novel construct, made using ectodermal and neural precursor or inflammation [ 66–68 ], and noxious sensory stimuli [ 69 ]. The
cells (neurobots, Figure 1a ). We showed that neurobots are viable emergence of neural regulation of ciliary beating frequency in
and self-motile like their non-neuronal counterparts (Videos S3 neurobots would therefore represent a novel property.
and S4 ), and that the implanted neural precursor cells indeed
differentiate into neurons and extend their processes throughout Despite variation in the shape and innervation patterns of
the construct (Figures 1 and 2 ; Figure S3 ). neurobots, we found that all of them exhibited a central cavity
largely devoid of cell bodies (as indicated by the absence of
We found that neurobots became significantly larger than biobots nuclear staining) and containing only a few neurites with sparse
and were significantly more elongated (Figure 1b,c ). In addition expression of the presynaptic marker synapsin-1 (Figures 2 and 3 ;
to overall changes in shape and size revealed by our two- Figure S3 ). We confirmed the largely acellular nature of this space
dimensional analysis, neurobots exhibited differences in the 3D through staining with phalloidin, which labels F-actin present in
distribution of multiciliated cells and in overall body morphology. all eukaryote cells (Figure S4 ). We speculated that this region may
In the future, a more advanced 3D analysis incorporating the be filled with extracellular matrix-like structures. The presence
spatial positions of MCCs will help quantify further differences of neurites extending in extremely straight courses points to
between neurobots and biobots and elucidate how these may the presence of such a supporting structure (Figure 2b , red
correlate with their behaviors. arrowhead). Further, our transcriptomic analysis demonstrated a
significant upregulation of genes encoding ECM proteins, includ-
Neurobots exhibited a large degree of variability in the amount ing both fibrillar collagens and non-fibrillar components such as
innervation and in neural architecture (Figure 9 ; Figure S3 ). fibulins. In order to assess whether this space contains fibrillar
The variability in the size and number of the implanted neural ECM proteins, we used Second Harmonic Generation, which is
16of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
FIGURE 14 Phylostratigraphic analysis of upregulated or downregulated transcripts in neurobots compared to biobots and shams. (a) 54% of
upregulated genes in neurobots fall into the two categories of most ancient genes (“All living organisms”and “Eukaryota”). (b) Very few ancient genes
are downregulated. In total 279 are downregulated in these two strata for the NB versus BB conditions and 233 for the NB versus SH condition, whereas
941 and 1109, genes are upregulated respectively.
a label-free method for visualizing fibrillar ECM proteins such will be important for future work to characterize the molecular
as collagen [ 45 ]. Although we found evidence for the presence composition of this region in greater detail.
of collagen fibers, these fibers were extremely sparse (Figure
S4 ). Other non-fibrillar ECM components, such as proteoglycans, Neurobots exhibited a diverse range of movement patterns, and
laminins, or fibronectins, may occupy much of this space. It these patterns tended to be more complex than those observed in
AdvancedScience,2026 17of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
their non-neuronal counterparts, indicating that neural expres- to off-target effects of PTZ. Although PTZ is a noncompetitive
sion may affect movement either directly, that is, through neural antagonist of GABA
A
receptors, it may also exert indirect effects
signaling to the motor effectors, or via changes in the expression on other targets at higher concentrations, including glutamate
patterns of motor effectors. Indeed, we observed a negative receptors and voltage-gated ion channels [ 74 ]. Future exper-
correlation between the degree of neural expression and the iments where the activity of all or a specific population of
density of multiciliated cells (Figure 9c ). Future modeling efforts neurons could be modulated pharmacologically or optogeneti-
could help determine the extent to which differences in the spatial cally could provide important insight on the causal relationship
distribution of MCCs alone contribute to the observed increase in between neural activity and behavior, as well as the underlying
movement complexity. mechanisms.
Simultaneous recording of neural activity and behavior could be We raised a group of neurobots in zolmitriptan, which is a
used to assess the potential neural correlates of the behavior. selective 5-hydroxytryptamine (5-HT) 1B/1D receptor agonist,
Indeed, our calcium imaging experiments indicated that the known to increase the degree of ectopic neural growth in
implanted neurons were spontaneously active; however, due Xenopus embryos [ 51 ]. Interestingly, three out of four of these
to technical difficulties in measuring calcium signals in freely neurobots showed an increase in movement complexity when
moving neurobots, we were not able to make conclusions about treated with PTZ (filled circles Figure 8b ; Figure S7 ). Moreover,
neural correlates of observed movements. Specifically, measuring these neurobots showed a tighter correlation between the amount
calcium in freely moving neurobots was complicated by their of implanted tissue and the degree of innervation (Figure S7 ).
rotational movements, which often resulted in losing track Interestingly, 5-HT
1B
receptors are shown to modulate GABA
of specific regions of interest (Video S3 ). Such 3D rotational release [ 75 ], and serotonergic signaling is thought to affect the
movements could be suppressed by making flattened, disk-like migration pattern of cortical interneurons [ 76 ]. Altered sero-
neurobots, however, these neurobots tended not to move as much tonergic signaling in neurobots treated with zolmitriptan may
(data not shown). Future experiments in which the 3D movement therefore impact the expression of GABAergic neurons during
of the bots can be better controlled without flattening, as well as their development. Further experiments are needed to discover
experimental setups that allow repeated measurements, will be the mechanisms underlying this effect and whether zolmitrip-
critical for establishing correlations between neural activity and tan treatment results in biased expression of specific neural
behavior. subtypes.
Albino, pigment-less Xenopus laevis embryos were used to gener- Our transcriptomics analysis revealed the landscape of differ-
ate the body of neurobots intended for calcium imaging, as the entially expressed genes between neurobots, biobots, and sham
lack of pigmentation facilitates visualization of neuronal calcium neurobots. Overall, neurobots showed a significant upregulation
activity in the interior. Albino embryos exhibit developmental in gene expression compared to biobots and sham neurobots,
trajectories similar to those of wild-type embryos [ 70 ], but whereas biobots and shams were more similar to one another
differences in visually evoked behaviors have been reported in (Figure 10a,b and Figure 11 ). Functional enrichment analysis
albino tadpoles [ 71, 72 ]. Thus, possible differences in the pattern revealed that neurobots, compared to both biobots and shams,
of neural growth and behavioral phenotypes of neurobots with exhibit a high level of enrichment in genes involved in nervous
and without body pigmentation, especially in the context of system development, synapse formation, neuron projection, and
visually-evoked behaviors, may be an interesting subject of future trans-synaptic signaling (Figure 12a,b ). Genes encoding major
investigation. neurotransmitter receptors were present in the transcriptome of
neurobots. This included glutamatergic, GABAergic, cholinergic,
Consistent with a role of neural activity in modulating behavior, dopaminergic, serotonergic, and glycinergic receptors.
we found that treatment of biobots and neurobots with the
GABA
A
receptor antagonist PTZ resulted in significantly different Our gene network analysis resulted in the identification of
outcomes. To our surprise, we found that most biobots decreased multiple functional clusters, allowing us to more deeply examine
their movement complexity with PTZ treatment, indicating the the genes and pathways that are upregulated in neurobots.
presence of non-neuronal drug targets. Indeed GABAergic recep- Notably, we found a large cluster containing genes with important
tors are found on the surface of the mucus-secreting goblet cells, roles in visual perception (Cluster 1, Figure 13c ; Figure S9c ).
and treating Xenopus embryos with bicuculline, which is also This cluster contained genes normally expressed exclusively in
a GABA
A
antagonist, was shown to inhibits mucus secretion Xenopus eyes, including various members of the opsin family
[ 73 ]. It is possible that treatment with PTZ changes the beating such as a retinal G protein-coupled receptor, various cone opsins,
frequency of MCCs through changes in mucus secretion. The rhodopsin, as well as genes encoding many other proteins
effect of PTZ on neurobots was significantly different from implicated in visual processing. This remarkable finding suggests
that on biobots (Figure 8 ). In fact, the majority of neurobots the possible presence of visually evoked behaviors in neurobots.
showed an increase in movement complexity, suggesting that The next and most exciting step will be to test this hypothesis
neural activity may contribute to the observed differential effect. and discover the ways that light could modulate motor output in
Additional experiments are required to identify the targeted neurobots. If present, this will be a completely novel emergent
cell types (neuronal or non-neuronal) and to assess whether behavior. Follow-up proteomic analyses will be necessary to
the effect we observed is caused by GABA signaling or is due determine whether the upregulated transcripts are translated
into corresponding proteins and to investigate their spatial
organization.
18of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
We showed that neurobots exhibit a significant increase in the 4 Methods
variability of their gene counts compared to their non-neuronal
counterparts (BBs and SHs, Figure 10c–f ). Although some of 4.1 Animal Husbandry and Construction of
this variability could be attributable to the manual nature of Biobots, Neurobots, and Shams
their creation, and/or pooling of implanted cells from multiple
embryos, the excess variability seen in neurobots relative to shams All experiments were approved by Tufts University Institutional
suggests that neurons may play an important role in guiding the Animal Care and Use Committee (IACUC) under the protocol
way cells explore the gene expression landscape. The nervous number M2023-18.
systems of animals are known to influence the behavior of
non-neural cells and tissues [ 60, 77 ], so it is possible that the Biobots were constructed as described previously [ 25 ], by excising
information processing activity of the neurons, in response to the tissue from the animal hemisphere of a Nieuwkoop and Faber
unique “life experiences”of individuals, or internally-generated stage 9 Xenopus laevis embryo (animal cap).
spontaneous signaling, might account for the neurobots exhibit-
ing the largest inter-individual gene expression variability of To construct neurobots and sham neurobots we excised 40–50
the groups. Moreover, studies show that when cells are exposed such animal caps and let them sit with external surface facing up
to novel stressors that they do not have existing homeostatic in 60 mm petri dishes filled with a calcium and magnesium free
mechanisms to resolve, they resort to making random changes in solution (50.3 mM NaCl, 0.7 mM KCl, 9.2 m M Na
2
HPO
4
, 0.9 m M
the expression levels of many genes. It is possible that the bots KH
2
PO
4
, 2.4 m M NaHCO
3
, 1 m M edetic acid (EDTA), pH 7.3), and
we report here are undergoing stressors that evolution did not coated with 1% agarose made in the same solution. After about 30–
prepare them for, and may be employing this kind of exploration 40 min the cells were fully dissociated. The dissociated cells were
of gene expression space [ 78–82 ]. Future single-cell RNA-seq transferred to a deep 60 mm petri dish containing 0.75 Marc’s
experiments, combined with methods for implanting defined Modified Ringer (MMR) solution, using a P200 pipette, taking
numbers of cells, ideally derived from a single embryo, will as little liquid as possible. For constructing sham neurobots, the
provide critical insight into cell-to-cell variability and determine dissociated cells were immediately reaggregated and formed into
whether increased transcriptional variability in neurobots is clumps (see below). For constructing neurobots, we dispersed the
confined to specific cell types. dissociated cells as far as possible by moving the solution in the
dish using a P1000 pipette. The cells were left still in the dish for
Finally, based on a phylostratigraphic analysis, we show that the ∼ 3–4 h. To reaggregate cells, the dish containing dissociated cells
majority of upregulated genes in neurobots consist of the most was placed on a shaker, and cells were thereby brought together in
ancient genes (Figure 14 ), a pattern that differs significantly from the middle of the dish. They were then allowed to reaggregate for
that observed in biobots and shams. In all cases, the cells were approximately 1 h, at which point various clumps of cells formed
wild-type, and no genomic editing, synthetic biology circuits, spontaneously.
scaffolds, or drugs were used. These results suggest that novel
configurations of cell types can have large-scale systemic effects Using a P1000 pipette, clumps of ∼ > 10 cells were moved into
on the transcriptome of the resulting multicellular construct and the wells of an agarose-coated 6-well plate. Larger clumps were
move it toward the gene expression profiles of the evolutionary broken into smaller ones that could fit inside the body of the
past. bot, that is animal caps excised from a new set of embryos (see
Figure 1a ). Depending on the size of the clumps, one or more were
Building neurobots with predictable nervous system architecture implanted.
and in large numbers is one of the major remaining challenges
of this study. Future automation and standardization efforts will Next, a new set of animal caps was dissociated from a second
enable higher throughput and consistency, allowing repeated batch of embryos from a later fertilization (at late blastula, early
measurements to be performed on neurobots with both identical gastrula stage), and were placed with the external surface facing
and distinct nervous system architectures. The impact of pharma- down individually in the wells of the same 6-well plate. The
cological, optical, and other types of stimulation on the neurobot excised animal caps slowly formed a bowl and eventually closed
behavior could be assessed. Additionally, the creation and neu- up within approximately 10–15 min. Clumps of neural precursor
roanatomical characterization of large numbers of identical bots cells (or non-neuronal clumps in the case of shams) were placed
will allow for the discovery of frequently emerging patterns and inside this bowl (Figure 1a (ii)) before it was closed using fine
motifs, thereby shedding light on the potential space for nervous forceps, and enough time was allowed for the animal cap to fully
system architectures in novel living constructs whose precise close before moving the dish to the incubator. Bots were housed
layout has not been shaped by selection for this specific behavioral in an incubator set to 14◦C, and experiments were performed in a
configuration. laboratory maintained at approximately 18◦C.
This study establishes a model system and experimental roadmap
to increase our understanding of the plasticity of evolutionarily 4.2 Immunohistochemistry
determined hardware of living beings to adapt on developmen-
tal (not evolutionary) timescales and to provide interfaces to Bots were fixed overnight at 4◦C in 4% paraformaldehyde
bioengineered living constructs that may provide novel con- (Thermo Fisher Scientific) with 0.25% gluteraldehyde (Electron
trol capabilities for useful synthetic living machines and shed Microscopy Sciences) individually in 96-well plates. The next
light on the origins of novelty in the evolution of nervous day, they were washed three times at room temperature in
systems. PBS-Triton X(PBT, 0.1% Triton X-100 (Sigma) in PBS-/- (Gibco))
AdvancedScience,2026 19of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
for at least 15 min and then incubated in the 10% Casblock created flattened neurobots as described previously [ 48 ]. Briefly,
(invitrogen) dissolved in PBT for at least 1 h. They were then on the day after their formation, neurobots were pressed down
transferred into the solution containing primary antibodies and using a glass coverslip, which was gradually lowered over them as
Hoescht (33342, Thermo Scientific). The plate was sealed using small amounts of MMR were removed from the dish. Neurobots
parafilm and covered in foil for light protection and placed on were left under pressure for 3 h, after which MMR was gradually
a shaker in the cold room for 3 days at 4◦C. The bots were added to the dish resulting in the release of the coverslip.
next washed 3 times in PBT at room temperature and then
transferred and incubated overnight at 4◦C in the secondary
antibodies, with the dish sealed with parafilm and covered in foil. 4.5 Quantification of the Bot Shape and Neural
Finally, the bots were washed again 3 times in PBT and either Tracing
stored in PBS at 4◦C or mounted into 15-slide 18-well flat dishes
(81821, Ibidi) in an antifade mounting medium (Vectashield, We used the brush tool in Fiji [ 83 ] to fill in the shape of the
Vectorlabs H-1000-10) for confocal imaging. Primary antibodies bot and calculated the area and roundness index defined as the
used were (Anti-acetylated tubulin antibody, Mouse monoclonal, major_axis / minor_axis. We used the same tool to estimate the
Sigma T7451; Anti-synapsin-1 antibody, Guinea pig monoclonal relative amount of implanted neural precursor tissue by dividing
recombinant antibody, Sysy Antibodies 106 308; MAP2 anti- the area of the implanted clumps to the outer shell (Figure 1a ).
body, Rabbit polyclonal antibody, Cell Signaling technologies We used Imaris software (Oxford Instruments) to quantify neural
4542), and the corresponding secondary antibodies were (Goat expression using confocal stacks acquired from the bots that
anti-mouse Alexa 594, Invitrogen A32742, Goat anti-guinea pig were stained with antibodies against acetylated α-tubulin, which
IgG (H + L) highly cross-adsorbed secondary antibody, Alexa labeled neurons and cilia in multiciliated cells. We manually
Fluor 488, ThermoFisher Scientific A-11073, Goat anti-rabbit traced neurites using the filament function and exported values
IgG (H + L) cross-adsorbed secondary antibody, Alexa Fluor 488, corresponding to the total length of neurites (dendrite length
ThermoFisher Scientific A-11008). For F-actin staining fixed sum parameter in Imaris) and the number of terminal points
and permeabilized neurobots were incubated with the F-actin- (number of dendrite terminal points parameter in Imaris). For
specif ic stain, Alexa Fluor 647 Phalloidin (Thermo Fisher Cat # the analysis of the multiciliated cell distribution, we estimated
A22287) at 1:50 in PBS (-/-) overnight at 4○C. Neurobots were the total number of MCCs by marking the center of each MCC
washed 3 ×with PBS (-/-) at room temperature and subsequently using the Spots tool in Imaris and calculated the total number of
mounted in Vectashield. multiciliated cells. We then used this value to calculate the MCC
density by dividing this number by the total area of the bot.
4.3 Confocal and Multiphoton Microscopy
4.6 Behavioral Analysis
Confocal images were acquired using the Stellaris 8 micro-
scope (Leica Microsystems), equipped with a Chameleon Vision Videos of bot movements were taken over 30 min under various
II (Coherent; 80 MHz repetition rate). Z-stacks were collected conditions and tracked with the DLTdv digitizing tool [ 49 ] in
at 2 µm intervals with a 25 ×/0.95 NA or a 40 ×/ 1.1 NA water- MATLAB, and the x and y coordinates of the center of mass were
immersion objectives. Each signal was acquired in series. To calculated. A custom Python code was used to extract various
ensure deep tissue penetration, Alexa 647-Phalloidin was excited kinematic variables using the time series of the coordinates. We
by two-photon excitation at 819 nm, with emission collected calculate total Euclidean distance travelled, average speed, and
between 636 and 746 nm. Second harmonic generation (SHG) average acceleration. Additionally, we calculated the percentage
imaging was performed at 890 nm excitation, with emission of the well that was traversed by the bots by dividing the space
detected between 465 and 616 nm, as previously described [ 45 ]. of each well into 0.1 mm bins. We then calculated the percent
Fiji (Image J), the LAS X (Leica Microsystems), and Imaris covered area by dividing the number of unique visited bins by
(Oxford Instruments) programs were used to process the images. the total number of bins. We calculated a complexity index by
first calculating the power spectral density (PSD) of the trajectory
time series along the x and y coordinates and identifying peaks in
4.4 Calcium Imaging the power. We calculated Welch’s power spectral density estimate
with a window size of 400 s and an overlap of 1 s between windows
Embryos at the four-cell stage were microinjected in all four for each of the x and y time series. We picked a threshold of
blastomeres with mRNA encoding the genetically encoded flu- 10 pixels2 /Hz ( ∼ 0.17 mm2 /Hz = 0.4 mm/Hz) to detect peaks in
orescent calcium indicator GCaMP6s. These embryos were used the PSD of the x and y coordinates. This threshold was chosen
for obtaining clumps of neural precursor cells for implantation. empirically to remove the baseline noise corresponding to the
Albino embryos were used as the outer shell of the neurobots in tracking of the center of mass of bots that had an average radius
these experiments so that the fluorescence signal from neurons of 0.4 mm. We then defined the complexity index as the total
could be visualized more easily as wild-type embryos are pig- number of unique peaks in the x and y PSDs.
mented. We used a custom-built microscope to measure calcium
activity in freely moving neurobots (Video S1 ). We used Fiji’s To further confirm the significance of power at the peak fre-
[ 83 ] Descriptor Based Series Registration plugin to correct for the quencies identified by Welch power analysis, we used the wavelet
motion of the neurobot (Video S2 ), then used Suite2p software transform and surrogate data. For each time series, we used
[ 84 ] to identify active units (Figure 5 ). To avoid movements in the MATLAB to calculate the continuous wavelet transform and from
Z -direction, which resulted in changes in the plane of focus, we there calculated the wavelet power spectrum across all time. To
20of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
assess the significance of dominant frequencies found from the then identifying the leading gene sets that give rise to other
Welch spectral analysis, we generated surrogate time series that significant functions in the ontology neighborhood.
preserve the original signal’s amplitude spectrum but randomize
its phase information in the wavelet space. These surrogates were For network analysis and clustering, we applied network analysis
used to compute a distribution of wavelet power spectra, from techniques to discover biological functional modules [ 91, 92 ]. By
which significance thresholds (95th percentile) were derived for integrating gene expression and interaction data, we extracted
hypothesis testing. Only 4 out of 243 peaks identified through PPI for the different biobots in their respective conditions and
Welch analysis across all bots did not pass the significance test in applied network embedding and clustering techniques similar
the wavelet space. This small difference is expected because the to those described by Cantini et al. [ 93 ] and Pio-Lopez et al.
two methods differ in their frequency resolution: Welch analysis [ 94 ]. Specifically, we used the MNMF algorithm developed by
uses uniform resolution across all frequencies, whereas wavelet Wang et al. [ 61 ] for network embedding and clustering. To
analysis employs logarithmic spacing, providing finer detail at create a network for the bots, we started by isolating genes of
lower frequencies and coarser resolution at higher frequencies. interest and identifying corresponding human orthologs under
various conditions using the HCOP database [ 95 ]. We then used
the STRING database [ 96 ] to extract relevant PPI networks.
4.7 RNA-Sequencing and Bioinformatics The clusters identified through our network embedding and
clustering method were further analyzed for enrichment using g:
We submitted 12 samples (4 samples per biobot type, 5–15 bots Profiler [ 62 ].
per sample: Number of bots per sample: {NB1 = 14, NB2 = 12,
NB3 = 12, NB4 = 12}, {BB1 = 16, BB2 = 6, BB3 = 6, BB4 = 5},
{NN1 = 5, NN2 = 6, NN3 = 6, NN4 = 5}) submerged in Trizol
(Invitrogen) in 2 mL Eppendorf tubes, to Novogene (Novogene 4.8 Analysis of Gene Expression Variability
Corporation Inc., Sacramento, CA) for low-input, high-lipid, bulk
RNA extraction. The first batch submitted to Novogene (NB1 and The normalized gene count variability was compared between
BB1) contained a larger number of bots to test the efficacy of groups (BBs, NBs, and SHs) using a MATLAB script and the
the low-input method. The next series of sample batches (NB2- method summarized in Figure S11 . We excluded NB1 and BB1
4, BB2-4, NN1-4) contained a smaller number of bots based on since they were sent to Novogene for sequencing as a different
the results from the first batch. Equal quantities of RNA were batch than other NBs (NB2-4) and BBs (BB2-4), and we wanted to
sequenced from each sample using the NovaSeq6000 sequencer, reduce the impact of inter-batch variability (see RNA-sequencing
resulting in consistent library size across samples. Clean reads and bioinformatics) . We kept all four NN groups as they were sent
were extracted from FASTQ files, removing reads with adapter as a part of the same batch (NN1-4). For each gene in each pair
contamination, when uncertain nucleotides constitute more than of groups being compared, the mean count value across all pools
10 percent of either read ( N > 10%), and when low-quality of both groups was found, and genes were ranked from greatest
nucleotides (Base Quality less than 5) constitute more than to least mean. Genes for which any of the counts across all pools
50 percent of the read. The index to the reference genome was 0 were discarded. Because the count value of a given gene in a
( Xenopus laevis version 10.1) was built using Hisat2 v2.0.5 [ 85 ], given pool represents the mean value of all the individuals in that
and clean reads were aligned to the reference. The mapped reads pool, the standard deviation of the pools gives the standard error
of each sample were assembled using StringTie (v1.3.3b) [ 86 ], and of the means (SE) of the group. The SE is related to the number
FeatureCounts v1.5.0-p3 [ 87 ] was used to count the read numbers of individuals per pool ( n ) and the standard deviation of the
mapped to each gene. FPKM of each gene was calculated based individuals within the pools ( σ) with the equation SE = σ/sqrt( n ).
on the length of the gene and read counts mapped to this gene. By multiplying the SE by sqrt( n ), σcan be calculated. Dividing
Differential expression analysis was performed using the DESeq2 σ by the mean count value of the pools gives the coefficient of
R package (1.20.0) [ 88 ], and the resulting p -values were adjusted variation (CV). The ranked gene CV lists were then split into
using Benjamini and Hochberg’s approach for controlling the 100 bins (percentiles) containing equal numbers of genes from
false discovery rate. highest to lowest counts. Within each bin, the number of genes
with greater CV for the first group than the second was counted
The webapp g: Profiler [ 62 ] was used to perform func- and divided by bin size to find the fraction of genes in the bin
tional enrichment analysis of differentially expressed genes. with greater CV in the first group. These fractions were then
For each comparison, upregulated genes ( p -adjusted < 0.05; plotted as bar graphs in Figure 10c–e , with a blue line marking
log2foldchange > 4) and downregulated genes ( p -adjusted < 0.05; 0.5. The bin values appeared to vary with gene count percentile,
log2foldchange < -4) were separately mapped from Xenopus so to determine the statistical significance of each bin’s departure
to human symbols using the HGNC Comparison of Orthology from its expected value, a permutation test was used. For each plot
Predictions (HCOP) tool [ 89 ]. Genes lacking an established gene (each pair of groups), the order of the gene pairs was randomly
symbol were removed from analysis. Each gene list was separately shuffled (keeping pairs together), and new bins were generated.
queried using g: Profiler across all data sources. The statistical This was repeated 1000 times for random shuffles to produce
data scope included only annotated genes, and the g: SCS method a distribution of bin fraction values for each bin. The p -value
was used for computing multiple testing corrections for p- values of each bin was defined as the proportion of the bin fractions
at a threshold of p < 0.05. The R package ggplot2 (v3.5.1) [ 90 ] from the distribution that were further in absolute value from the
was used to generate dot plots of gene ontology driver terms distribution mean than the true bin fraction. Bins with p -values
from g: Profiler. Driver terms were determined by grouping of p < 0.05 were deemed statistically significant and were colored
significant terms into sub-ontologies based on their relations, dark blue. in Figure 10d-f . All other bins were colored light blue.
AdvancedScience,2026 21of25
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
The mean bin value from the distributions was plotted as a yellow The statistical analysis for differential gene expression data was
line. performed using the R package DESeq2, which employed the two-
sided Wald test. Multiple hypothesis testing corrections were used
to obtain adjusted p -values. For the analysis of gene expression
4.9 Phylostratigraphic Analysis variability, the statistical significance of bin deviations from
expected values was assessed using a permutation test. For each
We employed the phylostrat package [ 97 ] to conduct a phy- group comparison, gene pairs were randomly shuffled 1000 times
lostratigraphic analysis on transcripts of all three bot types, (with pairs kept intact) to generate null distributions of bin
with Xenopus laevis (taxon ID 8355) designated as the reference fractions; bin p -values were defined as the proportion of permuted
species. This software automated several key steps in evolutionary values more extreme than the observed value, and bins with
analysis: (1) it built a clade tree using species from the UniProt p < 0.05 were considered significant.
database and aligned it with the latest NCBI taxonomy; (2) the
clade tree was trimmed to maintain a phylogenetically diverse
selection of representative species for each phylostratum; (3) a
comprehensive protein sequence database was constructed from
hundreds of species based on this clade tree, with additional Acknowledgements
data such as human and yeast proteomes manually added, We would like to thank Drs. Douglas Blackiston, Patrick McMillen, Jack
resulting in 329 species for our study; (4) a similarity search was Lindsay, Pai Vaibhav, Harini Rajendiran, and Russel Gould for their
performed by conducting pairwise BLAST comparisons between technical help and scientific insights, Meghan Short for statistical analysis
consultation, Susan Marquez, Thomas Ferrante, Ramses Martinez, and
the proteins encoded by Xenopus laevis and those of the target
Kostyantyn Shcherbina for their help with microscopy and engineering,
species; (5) the best hits were identified, and gene homology
Jeantine Lunshof for philosophical and ethics discussions, and Drs. Don-
was inferred between Xenopus laevis and the target species; (6)
ald Ingber, Florian Engert, and Michael Super for their input and support
each gene was assigned to a phylostratum that corresponded throughout the project. Thanks to Gordon Allen for copyediting, and
to the oldest clade for which a homolog was identified. Genes Julia Poirier and Tomika Gotch for assistance with the manuscript. This
specific to Xenopus laevis were classified as orphan genes and research was supported by HR0011-18-2-0022, W911NF1920027 awarded
placed within the Xenopus laevis phylostratum. The evolutionary by the Department of Defense, and grants from the John Templeton
Foundation (grant #62212) and Northpond Ventures.
stages we focused on include: All living organisms (bacte-
ria, eubacteria), Eukaryota, Opisthokonta, Metazoa, Eumetazoa,
Bilateria, Deuterostomia, Chordata, Vertebrata, Gnathostom- Funding
ata, Euteleostomi, Sarcopterygii, Tetrapoda, Anura, Xenopus , This research was supported by HR0011-18-2-0022, W911NF1920027,
and Xenopus laevis . This methodological approach enabled a awarded by the Department of Defense, and grants from the John
detailed examination of gene emergence and their evolutionary Templeton Foundation and Northpond Ventures.
trajectories across various taxa. By implementing Phylostratr,
we systematically mapped the age of the bot genes in the Conflicts of Interest
different conditions with a specific phylostrata to understand
M.L. is a scientific co-founder and consults for Fauna Systems, a company
the distribution of ages of the bots’ overexpressed genes. We seeking to commercialize frog cell-based biobot technology.
used the upregulated and downregulated genes in neurobots
(log2foldchange > 4 and log2foldchange < -2 respectively).
Data Availability Statement
RNA-sequencing data generated during this study are available in the
NCBI Gene Expression Omnibus (GEO) public repository under acces-
4.10 Statistical Analysis
sion number GSE295614. All other data supporting the findings of this
study are available from the corresponding authors upon reasonable
Statistical analyses of behavioral and shape data were performed request.
using the non-parametric Kruskal–Wallis test. When appropriate,
multiple comparisons conducted using Tukey’s honestly signifi-
References
cant difference test. For PTZ experiments, we used a one-sample
1 . X. Navarro, M. Vivó, and A. Valero-Cabré, “Neural Plasticity After
t -test to assess whether the population mean of the relative
Peripheral Nerve Injury and Regeneration,”Progress in Neurobiology 82
complexity index was significantly different from zero. Robust
(2007): 163–201, https://doi.org/10.1016/j.pneurobio.2007.06.005 .
linear regression was used to quantify relationships between
2 . A. Antonini and M. P. Stryker, “Rapid Remodeling of Axonal Arbors in
pairs of neurobots’ physical, neuroanatomical, and behavioral
the Visual Cortex,”Science 260 (1993): 1819–1821, https://doi.org/10.1126/
measures; the significance of regression coefficients and Pearson
science.8511592 .
correlation coefficients was assessed using two-tailed t -statistics.
3 . H. T. Cline, M. Lau, and M. Hiramoto, “Activity-Dependent Organi-
Significance of peak frequencies identified by Welch analysis
zation of Topographic Neural Circuits,” Neuroscience 508 (2023): 3–18,
was validated using continuous wavelet transforms and phase-
https://doi.org/10.1016/j.neuroscience.2022.11.032 .
randomized surrogate time series to generate null distributions of
4 . T. R. Makin and H. Flor, “Brain (re)Organisation Following Ampu-
wavelet power, with significance assessed at the 95th percentile.
tation: Implications for Phantom Limb Pain,” Neuroimage 218 (2020):
In box plots, whiskers showed the non-outlier extent, + signs 116943, https://doi.org/10.1016/j.neuroimage.2020.116943 .
depicted outliers, and the top and bottom of the box showed the
5 . D. J. Blackiston and M. Levin, “Ectopic Eyes Outside the Head in
upper and lower quartiles of the data. The horizontal bar inside
Xenopus Tadpoles Provide Sensory Data for Light-Mediated Learning,”
the box showed the median. MATLAB (Mathworks, Natick, MA) Journal of Experimental Biology 216 (2013): 1031–1040, https://doi.org/10.
functions were used for all statistical analyses. 1242/jeb.074963 .
22of25 AdvancedScience,2026
21983844,
0,
Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
6 . R. George, M. Chiappalone, M. Giugliano, et al., “Plasticity and Vitro Learning Studies,”in Proceedings of the 25th Annual International
Adaptation in Neuromorphic Biohybrid Systems,” iScience 23 (2020): Conference of the IEEE Engineering in Medicine and Biology Society (IEEE
101589. Cat. No.03CH37439) (IEEE, 2004), 3690–3693.
7 . J. Soriano, “Neuronal Cultures: Exploring Biophysics, Complex Sys- 25 . D. Blackiston, E. Lederer, S. Kriegman, S. Garnier, J. Bongard, and
tems, and Medicine in a Dish,”Biophysica 3 (2023): 181–202, https://doi. M. Levin, “A Cellular Platform for the Development of Synthetic Living
org/10.3390/biophysica3010012 . Machines,” Science Robotics 6 (2021): abf1571, https://doi.org/10.1126/
scirobotics.abf1571 .
8 . S. P. Pa șca, “The Rise of Three-Dimensional Human Brain Cultures,”
Nature 553 (2018): 437–445. 26 . H. J. Kang and H. Y. Kim, “Mucociliary Epithelial Organoids From
Xenopus Embryonic Cells: Generation, Culture and High-Resolution Live
9 . M. A. Lancaster, M. Renner, C. Martin, et al., “Cere bral Orga noids
Imaging,”Journal of Visualized Experiments 161 (2020): 61604, https://doi.
Model human Brain Development and Microcephaly,”Nature 501 (2013):
org/10.3791/61604 .
373–379, https://doi.org/10.1038/nature12517 .
27 . P. Walentek and I. K. Quigley, “What We Can Learn From a Tadpole
10 . C. A. Trujillo, R. Gao, P. D. Negraes, et al., “Complex Oscillatory Waves
About Ciliopathies and Airway Diseases: Using Systems Biology in
Emerging From Cortical Organoids Model Early human Brain Network
Xenopus to Study Cilia and Mucociliary Epithelia,” Genesis 55 (2017):
Development,” Cell Stem Cell 25 (2019): 558–569.e7, https://doi.org/10.
23001, https://doi.org/10.1002/dvg.23001 .
1016/j.stem.2019.08.002 .
28 . E. Dubaissi and N. Papalopulu, “Embryonic Frog Epidermis: A Model
11 . G. Quadrato, J. Brown, and P. Arlotta, “The Promises and Challenges of
for the Study of Cell-Cell Interactions in the Development of Mucociliary
Human Brain Organoids as Models of Neuropsychiatric Disease,”Nature
Disease,”Disease Models & Mechanisms 4 (2011): 179–192, https://doi.org/
Medicine 22 (2016): 1220–1228, https://doi.org/10.1038/nm.4214 .
10.1242/dmm.006494 .
12 . A. El Din, L. Moenkemoeller, A. Loeffler, et al., “Human Neural
29 . P. Walentek, S. Bogusch, T. Thumberger, et al., “A Novel Serotonin-
Organoid Microphysiological Systems Show the Building Blocks Neces-
Secreting Cell Type Regulates Ciliary Motility in the Mucociliary
sary for Basic Learning and Memory,”Communications Biology 8 (2025):
Epidermis of Xenopus Tadpoles,” Development 141 (2014): 1526–
1237, https://doi.org/10.1038/s42003- 025- 08632-5 .
1533.
13 . D. J. Bakkum, Z. C. Chao, and S. M. Potter, “Spatio-Temporal Electrical
30 . F. Keijzer, M. van Duijn, and P. Lyon, “What Nervous Systems Do:
Stimuli Shape Behavior of an Embodied Cortical Network in a Goal-
Early Evolution, Input–Output, and the Skin Brain Thesis,” Adaptive
Directed Learning Task,”Journal of Neural Engineering 5 (2008): 310–323,
Behavior 21 (2013): 67–85, https://doi.org/10.1177/1059712312465330 .
https://doi.org/10.1088/1741-2560/5/3/004 .
31 . F. Keijzer, “Moving and Sensing Without Input and Output: Early Ner-
14 . A. Novellino, P. D’Angelo, L. Cozzi, M. Chiappalone, V. Sanguineti,
vous Systems and the Origins of the Animal Sensorimotor Organization,”
and S. Martinoia, “Connecting Ne uro ns to a Mobile Robot: An In
Biology & Philosophy 30 (2015): 311–331, https://doi.org/10.1007/s10539-
Vitro Bidirectional Neural Interface,” Computational Intelligence and
015-9483-1 .
Neuroscience 2007 (2007): 12725, https://doi.org/10.1155/2007/12725 .
32 . C. Verasztó, N. Ueda, and L. A. Bezares-Calderón, “Ciliomotor
15 . B. J. Kagan, A. C. Kitchen, N. T. Tran, et al., “In Vitro Neurons Learn
Circuitry Underlying Whole-Body Coordination of Ciliary Activity in the
and Exhibit Sentience When Embodied in a Simulated Game-World,”
Platynereis Larva,”Elife 6 (2017): e26000, https://doi.org/10.7554/eLife. Neuron 110 (2022): 3952–3969.e8, https://doi.org/10.1016/j.neuron.2022.09.
26000 .
001 .
33 . G. O. Mackie, C. L. Singla, and C. Thiriot-Quievreux, “Nervous Control
16 . N. Rouleau, N. J. Murugan, and D. L. Kaplan, “Toward Studying
of Ciliary Activity in Gastropod Larvae,”The Biological Bulletin 151 (1976):
Cognition in a Dish,” Trends in Cognitive Sciences 25 (2021): 294–304,
182–199, https://doi.org/10.2307/1540713 .
https://doi.org/10.1016/j.tics.2021.01.005 .
34 . A. G. Collins, J. H. Lipps, and J. W. Valentine, “Modern Mucociliary
17 . O. Aydin, “Neuromuscular Actuation of Biohybrid Motile Bots,”
Creeping Trails and the Bodyplans of Neoproterozoic Trace-makers,”
Proceedings of the National Academy of Sciences of the United States of
Paleobiology 26 (2000): 47–55, https://doi.org/10.1666/0094-8373(2000)
America (2019), 19841–19847.
026%3c0047:MMCTAT%3e2.0.CO;2 .
18 . O. Aydin, A. P. Passaro, M. Elhebeary, et al., “Development of
35 . A. Ivantsov, A. Nagovitsyn, and M. Zakrevskaya, “Traces of Locomo-
3D Neuromuscular Bioactuators,”APL Bioengineering 4 (2020): 016107,
tion of Ediacaran Macroorganisms,”Geosciences 9 (2019): 395, https://doi.
https://doi.org/10.1063/1.5134477 .
org/10.3390/geosciences9090395 .
19 . S. Park, M. Gazzola, K. S. Park, et al., “Phototactic Guidance of a
36 . V. Pai, L. Pio-Lopez, M. Sperry, P. Erickson, and M. X. T. Levin, “Gene
Tissue-Engineered Soft-Robotic Ray,”Science 353 (2016): 158–162, https://
Expression Changes in Wild-Type Cells Comprising a Form of Biobot,”
doi.org/10.1126/science.aaf4292 .
preprint, bioRxiv, August (2024), https://doi.org/10.31219/osf.io/n2jre .
20 . J. Wang, X. Zhang, J. Park, et al., “Computationally Assisted
37 . Y. Satou-Kobayashi, J. Kim, A. Fukamizu, and M. Asashima, “Tem-
Design and Selection of Maneuverable Biological Walking Machines,”
poral Transcriptomic Profiling Reveals Dynamic Changes in Gene Advanced Intelligent Systems 3 (2021): 2000237, https://doi.org/10.1002/
Expression of Xenopus Animal Cap Upon Activin Treatment,”Scientific
aisy.202000237 .
Reports 11 (2021): 14537, https://doi.org/10.1038/s41598- 021- 93524-x.
21 . N. Ando and R. Kanzaki, “Insect-Machine Hybrid Robot,” Current
38 . J. Lee, A. F. Møller, S. Chae, et al., “A Single-Cell, Time-Resolved
Opinion in Insect Science 42 (2020): 61–69, https://doi.org/10.1016/j.cois.
Profiling of Xenopus Mucociliary Epithelium Reveals Nonhierarchical
2020.09.006 .
Model of Development,”Science Advances 9 (2023): add5745, https://doi.
22 . S. Tsuda, S. Artmann, and K. Zauner, Artificial Life Models in org/10.1126/sciadv.add5745 .
Hardware ed. M.-E. Faust and S. Carrier (Springer, 2009), 213–232, https://
39 . A. Angerilli, P. Smialowski, and R. A. Rupp, “The Xenopus Animal
doi.org/10.1007/978- 1- 84882- 530- 7 .
Cap Transcriptome: Building a Mucociliary Epithelium,”Nucleic Acids
23 . W. P. Clawson and M. Levin, “Endless Forms Most Beautiful 2.0: Research 46 (2018): 8772–8787, https://doi.org/10.1093/nar/gky771 .
Teleonomy and the Bioengineering of Chimaeric and Synthetic Organ-
40 . S. I. Wilson and T. Edlund, “Neural Induction: Toward a Unifying
isms,” Biological Journal of the Linnean Society 139 (2023): 457–486,
Mechanism,”Nature Neuroscience 4, no. 4 (2001): 1161–1168, https://doi.
https://doi.org/10.1093/biolinnean/blac073 .
org/10.1038/nn747 .
24 . S. M. Potter, D. A. Wagenaar, R. Madhavan, and T. B. DeMarse,
41 . H. Grunz and L. Tacke, “Neural Differentiation of Xenopus Laevis
“Long-Term Bidirectional Neuron Interfaces for Robotic Control, and In
Ectoderm Takes Place After Disaggregation and Delayed Reaggregation
AdvancedScience,2026 23of25
21983844,
0, Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
Without Inducer,”Cell Differentiation and Development 28 (1989): 211–217, 59 . A. Kumar and J. P. Brockes, “Nerve Dependence in Tissue, Organ, and
https://doi.org/10.1016/0922- 3371(89)90006- 3 . Appendage Regeneration,” Trends in Neurosciences 35 (2012): 691–699,
https://doi.org/10.1016/j.tins.2012.08.003 .
42 . L. Dehmelt and S. Halpain, “The MAP2/Tau Family of Microtubule-
Associated Proteins,” Genome Biology 6 (2005): 204, https://doi.org/10. 60 . C. Herrera-Rincon and M. Levin, “Booting up the Organism During
1186/gb- 2004- 6- 1- 204 . Development: Pre-Behavioral Functions of the Vertebrate Brain in Guid-
ing Body Morphogenesis,”Communicative & Integrative Biology 11 (2018):
43 . D. Perdiz, R. Mackeh, C. Poüs, and A. Baillet, “The Ins and Outs of
1433440, https://doi.org/10.1080/19420889.2018.1433440 .
Tubulin Acetylation: More Than Just a Post-Translational Modification?,”
Cellular Signalling 23 (2011): 763–771, https://doi.org/10.1016/j.cellsig. 61 . X. Wang, “Community Preserving Network Embedding,”in AAAI’17:
2010.10.014 . Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence
(AAAI Press, 2017), 203–209.
44 . R. Dominguez and K. C. Holmes, “Actin Structure and Function,”
Annual Review of Biophysics 40 (2011): 169–186, https://doi.org/10.1146/ 62 . L. Kolberg, U. Raudvere, I. Kuzmin, P. Adler, J. Vilo, and H. Peterson,
annurev-biophys-042910-155359 . “g:Profiler—Interoperable Web Service for functional enrichment Analy-
sis and Gene Identifier Mapping (2023 Update),”Nucleic Acids Research
45 . C. R. Esquibel, K. D. Wendt, H. C. Lee, et al., “Second Harmonic
51 (2023): W207–W212, https://doi.org/10.1093/nar/gkad347 .
Generation Imaging of Collagen in Chronically Implantable Electrodes
in Brain Tissue,”Frontiers in Neuroscience 14 (2020): 95, https://doi.org/ 63 . J. Hahn, A. Monavarfeshani, M. Qiao, et al., “Evolution of Neuronal
10.3389/fnins.2020.00095 . Cell Classes and Types in the Vertebrate Retina,”Nature 624 (2023): 415–
424, https://doi.org/10.1038/s41586- 023- 06638- 9 .
46 . C. Frantz, K. M. Stewart, and V. M. Weaver, “The Extracellular Matrix
at a Glance,”Journal of Cell Science 123 (2010): 4195–4200, https://doi.org/ 64 . W. S. Argraves, H. Tran, W. H. Burgess, and K. Dickerson, “Fibulin Is
10.1242/jcs.023820 . an Extracellular Matrix and Plasma Glycoprotein With Repeated Domain
Structure,”The Journal of Cell Biology 111 (1990): 3155–3164, https://doi.
47 . M. Z. Lin and M. J. Schnitzer, “Genetically Encoded Indicators of
org/10.1083/jcb.111.6.3155 .
Neuronal Activity,”Nature Neuroscience 19 (2016): 1142–1153, https://doi.
org/10.1038/nn.4359 . 65 . S. Kriegman, D. Blackiston, M. Levin, and J. Bongard, “A Scalable
Pipeline for Designing Reconfigurable Organisms,” Proceedings of the
48 . S. Kriegman, D. Blackiston, M. Levin, and J. Bongard, “Kinematic Self-
National Academy of Sciences of the United States of America 117 (2020):
Replication in Reconfigurable Organisms,” Proceedings of the National
1853–1859, https://doi.org/10.1073/pnas.1910837117 .
Academy of Sciences of the United States of America 118 (2021): 2112672118,
https://doi.org/10.1073/pnas.2112672118 . 66 . S. D. Joshi, T. R. Jackson, L. Zhang, C. Stuckenholz, and L. A.
Davidson, “Supracellular Contractility in Xenopus Embryo Epithelia
49 . T. L. Hedrick, “Software Techniques for Two- and Three-Dimensional
Regulated by Extracellular ATP and the Purinergic Receptor P2Y2,”
Kinematic Measurements of Biological and Biomimetic Systems,”Bioin-
Journal of Cell Science 138 (2025): jcs263877, https://doi.org/10.1242/jcs.
spiration & Biomimetics 3 (2008): 034001, https://doi.org/10.1088/1748-
263877 .
3182/3/3/034001 .
67 . M. Dosch, J. Gerber, F. Jebbawi, and G. Beldi, “Mechanisms of
50 . T. Shimada and K. Yamagata, “Pentylenetetrazole-Induced Kindling
ATP Release by Inflammatory Cells,”International Journal of Molecular
Mouse Model,” Journal of Visualized Experiments 136 (2018): 56573,
Sciences 19 (2018): 1222, https://doi.org/10.3390/ijms19041222 . https://doi.org/10.3791/56573 .
68 . L. Zhang and M. J. Sanderson, “Oscillations in Ciliary Beat Frequency
51 . D. J. Blackiston, K. Vien, and M. Levin, “Serotonergic Stimulation
and Intracellular Calcium Concentration in Rabbit Tracheal Epithelial
Induces Nerve Growth and Promotes Visual Learning via Posterior
Cells Induced by ATP,” The Journal of Physiology 546 (2003): 733–749,
Eye Grafts in a Vertebrate Model of Induced Sensory Plasticity,” npj
https://doi.org/10.1113/jphysiol.2002.028704 .
Regenerative Medicine 2 (2017): 8, https://doi.org/10.1038/s41536- 017- 0012-
5 . 69 . A. S. Shah, Y. Ben-Shahar, T. O. Moninger, J. N. Kline, and M. J. Welsh,
“Motile Cilia of Human Airway Epithelia Are Chemosensory,”Science 325
52 . S. W. Flavell and M. E. Greenberg, “Signaling Mechanisms Linking
(2009): 1131–1134, https://doi.org/10.1126/science.1173869 .
Neuronal Activity to Gene Expression and Plasticity of the Nervous
System,”Annual Review of Neuroscience 31 (2008): 563–590, https://doi. 70 . Z. Shan, S. Li, C. Yu, et al., “Embryonic and Skeletal Development of
org/10.1146/annurev.neuro.31.060407.125631 . the Albino African Clawed Frog (Xenopus laevis),”Journal of Anatomy
242 (2023): 1051–1066, https://doi.org/10.1111/joa.13835 .
53 . C. Herrera-Rincon, V. P. Pai, K. M. Moran, J. M. Lemire, and M.
Levin, “The Brain Is Required for Normal Muscle and Nerve Patterning 71 . G. T. Adebogun, et al., “Albino Xenopus Laevis Tadpoles Prefer Dark
During Early Xenopus Development,”Nature Communications 8 (2017): Environments Compared to Wild Type,”MicroPublication Biology 2023
587, https://doi.org/10.1038/s41467- 017- 00597- 2 . (2023): 750.
54 . N. L. Bray, H. Pimentel, P. Melsted, and L. Pachter, “Near-Optimal 72 . J. Tsui, N. Schwartz, and E. S. Ruthazer, “A Developmental Sensitive
Probabilistic RNA-Seq Quantification,”Nature Biotechnology 34 (2016): Period for Spike Timing-Dependent Plasticity in the Retinotectal Projec-
525–527, https://doi.org/10.1038/nbt.3519 . tion,”Frontiers in Synaptic Neuroscience 2 (2010): 13, https://doi.org/10.
3389/fnsyn.2010.00013 .
55 . G. Colozza and E. M. De Robertis, “Dact-4 Is a Xenopus laevis
Spemann Organizer Gene Related to the Dapper/Frodo Antagonist of β- 73 . H. J. Sim, S. Kim, K. Myung, T. Kwon, H. Lee, and T. J. Park, “Xenopus:
Catenin Family of Proteins,”Gene Expression Patterns 38 (2020): 119153, An Alternative Model System for Identifying Muco-Active Agents,”
https://doi.org/10.1016/j.gep.2020.119153 . PLoS One 13 (2018): 0193310, https://doi.org/10.1371/journal.pone.
0193310 . 56 . A. Pawlowski and G. Weddell, “Induction of Tumours in Denervated
Skin,”Nature213(1967):1234–1236,https://doi.org/10.1038/2131234a0 . 74 . Á. B. Monteiro, A. F. Alves, A. C. Ribeiro Portela, et al., “Pentylenete-
trazole: A Review,” Neurochemistry International 180 (2024): 105841,
57 . B. Scharrer, “Insect Tumors Induced by Nerve Severance: Incidence
https://doi.org/10.1016/j.neuint.2024.105841 . and Mortality,”Cancer Research 13 (1953): 73–76.
75 . D. A. N. Al-Halboosi, O. Savchenko, L. K. Heisler, and S. Sylantyev,
58 . B. Scharrer, “Experimental Tumors After Nerve Section in an Insect,”
Experimental Biology and Medicine 60 (1945): 184–189, https://doi.org/10.
“
A
M
M
o
P
d
A
u
-
l
R
at
e
i
c
o
e
n
p t
o
o
f
r
G
s
A
an
B
d
A
V
R
o
e
lt
l
a
e
g
a
e
s
-
e
G
b
a
y
t e
5
d
-H
C
T
a
1
2
B
+
R
C
e
h
c
a
e
n
p
n
to
e
r
l
s
s
:
, ”
A
N
n
e
I
u
n
r
t
o
e
p
r
h
p
a
la
r
y
m
W
ac
i
o
t
l
h
-
3181/00379727- 60- 15132 .
ogy 241 (2023): 109758, https://doi.org/10.1016/j.neuropharm.2023.109758 .
24of25 AdvancedScience,2026
21983844,
0, Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License
76 . S. Murthy, M. Niquille, N. Hurni, et al., “Serotonin Receptor 3A Con- ding Approach,”Scientific Reports 11 (2021): 8794, https://doi.org/10.1038/
trols Interneuron Migration Into the Neocortex,”Nature Communications s41598- 021- 87987-1 .
5 (2014): 5524, https://doi.org/10.1038/ncomms6524 .
95 . R. L. Seal, B. Braschi, K. Gray, et al., “Genenames.Org: The HGNC
77 . Y. Wenger, W. Buzgariu, and B. Galliot, “Loss of Neurogenesis in Resources in 2023,” Nucleic Acids Research 51 (2023): D1003–D1009,
Hydra Leads to Compensatory Regulation of Neurogenic and Neurotrans- https://doi.org/10.1093/nar/gkac888 .
mission Genes in Epithelial Cells,”Philosophical Transactions of the Royal
96 . D. Szklarczyk, R. Kirsch, M. Koutrouli, et al., “The STRING Database
Society B: Biological Sciences 371 (2016): 20150040, https://doi.org/10.1098/
in 2023: Protein–Protein Association Networks and Functional Enrich-
rstb.2015.0040 .
ment Analyses for Any Sequenced Genome of Interest,” Nucleic Acids
78 . H. I. Schreier, Y. Soen, and N. Brenner, “Exploratory Adaptation Research 51 (2023): D638–D646, https://doi.org/10.1093/nar/gkac1000 .
in Large Random Networks,” Nature Communications 8 (2017): 14826,
97 . Z. Arendsee, J. Li, U. Singh, A. Seetharam, K. Dorman, and E.
https://doi.org/10.1038/ncomms14826 .
S. Wurtele, “Phylostratr: A Framework for Phylostratigraphy,” Bioin-
79 . S. Stern, T. Dror, E. Stolovicki, N. Brenner, and E. Braun, “Genome- formatics 35 (2019): 3617–3627, https://doi.org/10.1093/bioinformatics/
wide Tra nscriptional Plasticity Underlies Cellular Adaptation to Novel btz171 .
Challenge,”Molecular Systems Biology 3 (2007): MSB4100147,https://doi.
org/10.1038/msb4100147 .
80 . E. Braun, “The Unforeseen Challenge: From Genotype-to-Phenotype Supporting Information
in Cell Populations,” Reports on Progress in Physics 78 (2015): 036602, Additional supporting information can be found online in the Supporting
https://doi.org/10.1088/0034-4885/78/3/036602 . Information section.
81 . C. Fields and M. Levin, “Competency in Navigating Arbitrary Spaces Supporting File 1 : advs74389-sup-0001-SuppMat.pdf.
as an Invariant for Analyzing Cognition in Diverse Embodiments,” Supporting File 2 : advs74389-sup-0002-SuppMat.docx.
Entropy 24 (2022): 819, https://doi.org/10.3390/e24060819 . Supporting File 3 : advs74389-sup-0003-VideoS1.mp4.
82 . M. Levin, “Technological Approach to Mind Everywhere: An Supporting File 4 : advs74389-sup-0004-VideoS2.mp4.
Experimentally-Grounded Framework for Understanding Diverse Bodies Supporting File 5 : advs74389-sup-0005-VideoS3.mp4.
and Minds,”Frontiers in Systems Neuroscience 16 (2022): 768201, https:// Supporting File 6 : advs74389-sup-0006-VideoS4.mp4.
doi.org/10.3389/fnsys.2022.768201 .
Supporting File 7 : advs74389-sup-0007-SuppMat.docx.
83 . J. Schindelin, I. Arganda-Carreras, E. Frise, et al., “Fiji: An Open- Supporting File 8 : advs74389-sup-0008-Data.zip.
Source Platform for Biological-Image Analysis,”Nature Methods 9 (2012):
676–682, https://doi.org/10.1038/nmeth.2019 .
84 . M. Pachitariu, C. Stringer, M. Dipoppa, et al., “Suite2p: Beyond 10,000
Neurons With Standard Two-Photon Microscopy,”BioRxiv (2016): 061507,
https://doi.org/10.1101/061507 .
85 . A. Mortazavi, B. A. Williams, K. McCue, L. Schaeffer, and B. Wold,
“Mapping and Quantifying Mammalian Transcriptomes by RNA-Seq,”
Nature Methods 5 (2008): 621–628, https://doi.org/10.1038/nmeth.1226 .
86 . M. Pertea, G. M. Pertea, C. M. Antonescu, T. Chang, J. T. Mendell,
and S. L. Salzberg, “StringTie Enables Improved Reconstruction of a
Transcriptome From RNA-Seq Reads,” Nature Biotechnology 33 (2015):
290–295, https://doi.org/10.1038/nbt.3122 .
87 . Y. Liao, G. K. Smyth, and W. Shi, “featureCounts: An Efficient General
Purpose Program for Assigning Sequence Reads to Genomic Features,”
Bioinformatics 30 (2014): 923–930, https://doi.org/10.1093/bioinformatics/
btt656 .
88 . M. I. Love, W. Huber, and S. Anders, “Moderated Estimation of Fold
Change and Dispersion for RNA-Seq Data With DESeq2,”Genome Biology
15 (2014): 550, https://doi.org/10.1186/s13059- 014- 0550- 8 .
89 . B. Yates, K. A. Gray, T. E. M. Jones, and E. A. Bruford, “Updates to
HCOP: The HGNC Comparison of Orthology Predictions Tool,”Briefings
in Bioinformatics 22 (2021): bbab155, https://doi.org/10.1093/bib/bbab155 .
90 . H. Wickham, Ggplot2: Elegant Graphics for Data Analysis (Springer
International Publishing, 2016).
91 . A. Barabási, N. Gulbahce, and J. Loscalzo, “Network Medicine: A
Network-Based Approach to Human Disease,”Nature Reviews Genetics
12 (2011): 56–68, https://doi.org/10.1038/nrg2918 .
92 . W. Nelson, M. Zitnik, B. Wang, J. Leskovec, A. Goldenberg, and
R. Sharan, “To Embed or Not: Network Embedding as a Paradigm in
Computational Biology,”Frontiers in Genetics 10 (2019): 381, https://doi.
org/10.3389/fgene.2019.00381 .
93 . L. Cantini, E. Medico, S. Fortunato, and M. Caselle, “Detection of
Gene Communities in Multi-Networks Reveals Cancer Drivers,”Scientific
Reports 5 (2015): 17386, https://doi.org/10.1038/srep17386 .
94 . L. Pio-Lopez, A. Valdeolivas, L. Tichit, É. Remy, and A. Baudot, “Mul-
tiVERSE: A Multiplex and Multiplex-Heterogeneous Network Embed-
AdvancedScience,2026 25of25
21983844,
0, Downloaded
from
https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202508967
by
<Shibboleth>-member@ucas.ac.cn,
Wiley
Online
Library
on
[03/04/2026].
See
the
Terms
and
Conditions
(https://onlinelibrary.wiley.com/terms-and-conditions)
on
Wiley
Online
Library
for
rules
of
use;
OA
articles
are
governed
by
the
applicable
Creative
Commons
License