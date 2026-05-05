# Ying 等 - 2024 - Feature selection as deep sequential generative learning

Feature Selection as Deep Sequential Generative Learning
W ANGYANG YING, School of Computing and Augmented Intelligence, Arizona State University,
Tempe, AZ, USA
DONGJIE W ANG, Department of Computer Science, University of Kansas, Lawrence, KS, USA
HAIFENG CHEN, NEC Laboratories America Inc, Princeton, NJ, USA
YANJIE FU, School of Computing and Augmented Intelligence, Arizona State University, Tempe, AZ, USA
Feature selection aims to identify the most pattern-discriminative feature subset. In prior literature, filter
(e.g., backward elimination) and embedded (e.g., LASSO) methods have hyperparameters (e.g., top- k, score
thresholding) and tie to specific models, thus, hard to generalize; wrapper methods search a feature subset
in a huge discrete space and is computationally costly. To transform the way of feature selection, we regard
a selected feature subset as a selection decision token sequence and reformulate feature selection as a deep
sequential generative learning task that distills feature knowledge and generates decision sequences. Our
method includes three steps: (1) We develop a deep variational transformer model over a joint of sequential
reconstruction, variational, and performance evaluator losses. Our model can distill feature selection knowledge
and learn a continuous embedding space to map feature selection decision sequences into embedding vectors
associated with utility scores. (2) We leverage the trained feature subset utility evaluator as a gradient provider
to guide the identification of the optimal feature subset embedding; (3) We decode the optimal feature subset
embedding to autoregressively generate the best feature selection decision sequence with autostop. Extensive
experimental results show this generative perspective is effective and generic, without large discrete search
space and expert-specific hyperparameters. The code is available at http://tinyurl.com/FSDSGL.
CCS Concepts: • Computing methodologies → Feature selection;
Additional Key Words and Phrases: Feature selection, automated feature engineering, deep sequential genera-
tive model
ACM Reference format:
Wangyang Ying, Dongjie Wang, Haifeng Chen, and Yanjie Fu. 2024. Feature Selection as Deep Sequential
Generative Learning. ACM Trans. Knowl. Discov. Data. 18, 9, Article 221 (October 2024), 21 pages.
https://doi.org/10.1145/3687485
This research was partially supported by the National Science Foundation (NSF) via the grant numbers (2421864, 2421803,
2421865), National Academy of Engineering, and Grainger Foundation Frontiers of Engineering Grants.
Authors’ Contact Information: Wangyang Ying (corresponding author), School of Computing and Augmented Intelligence,
Arizona State University, Tempe, AZ, USA; e-mail: yingwangyang@gmail.com; Dongjie Wang, Department of Computer
Science, University of Kansas, Lawrence, KS, USA; e-mail: wangdongjie@ku.edu; Haifeng Chen, NEC Laboratories America
Inc, Princeton, NJ, USA; e-mail: haifeng@nec-labs.com; Yanjie Fu, School of Computing and Augmented Intelligence,
Arizona State University, Tempe, AZ, USA; e-mail: yanjie.fu@asu.edu.
Permission to make digital or hard copies of all or part of this work for personal or classroom use is granted without fee
provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice and the
full citation on the first page. Copyrights for components of this work owned by others than the author(s) must be honored.
Abstracting with credit is permitted. To copy otherwise, or republish, to post on servers or to redistribute to lists, requires
prior specific permission and/or a fee. Request permissions from permissions@acm.org.
© 2024 Copyright held by the owner/author(s). Publication rights licensed to ACM.
ACM 1556-472X/2024/10-ART221
https://doi.org/10.1145/3687485
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:2 W. Ying et al.
1 Introduction
Feature selection aims to identify the best feature subset from an original feature set. Effective feature
selection methods reduce dataset dimensionality, shorten training time, prevent overfitting, enhance
generalization, and, moreover, improve the performance of downstream machine learning (ML)
tasks. This technique can be applied to multiple domains, including biomarker discovery [ 52], traffic
forecasting, financial analysis, urban computing, client selection [ 32], and so on.
Prior literature can be categorized as follows: (1) Filter methods [ 5, 48, 51] rank features based on
a score (e.g., relevance between feature and label) and select top- : features as the optimal feature
subset (e.g., univariate feature selection). (2) Embedded methods [ 39, 41] jointly optimize feature
selection and downstream prediction tasks. For instance, LASSO shrinks feature coefficients by
optimizing regression and regularization loss. (3) Wrapper methods [17, 19, 31, 47] formulate feature
selection as a searching problem in a large discrete feature combination space via evolutionary
algorithms or genetic algorithms that collaborate with a downstream ML model.
However, existing studies are not sufficient. Filter methods typically overlook relationships
between features, are sensitive to data distribution, and are non-learnable, hence they often perform
poorly. Embedded methods rely on strong structured assumptions (e.g., sparse coefficients of L
norm) and downstream models (e.g., regression), making them inflexible. Wrapper methods suffer
from exponentially growing discrete search space (e.g., around 2# if the feature number is N). Can
we develop a more effective learning framework without searching a large discrete space?
Our Perspective: Feature Selection as Sequential Generative AI . The emerging Artificial Generative
Intelligence and ChatGPT show it is possible to learn complex and mechanism-unknown knowledge
from historical experiences and make smart decisions in an autoregressive generative fashion.
Following a similar spirit, we believe that knowledge related to feature subsets can also be distilled
and embedded into a continuous space, where computation and optimization are enabled and,
thereafter, generate a feature selection decision sequence. This generative perspective regards
feature selection, e.g., 51 52, ..., 57 → 51525456, as a sequential generative learning task to generate an
autoregressive feature selection decision sequence (Figure 1(b)). This transforms the traditional
way we select features via an iterative subset selection process (Figure 1(a)). Under this generative
perspective, a feature subset is represented as a feature token sequence and subsequently embedded
in a differentiable continuous space. In this continuous embedding space, an embedding vector
corresponds to a feature subset, and we can (a) build an evaluator function to assess feature subset
utility; (b) search the optimal feature subset embedding; (c) decode an embedding vector to generate
a feature selection decision sequence. This generative learning perspective provides great potential
to distill feature knowledge from experiences and generalize well over various domain datasets.
Inspired by these findings, we propose a deep variational sequential generative feature
selection learning (VTFS) framework that includes three steps: (1) Embedding. We develop a
variational transformer model with joint optimization of sequence reconstruction loss, feature
subset accuracy evaluator loss, and variational distribution alignment (i.e., Kullback–Leibler (KL))
loss, in order to learn a feature subset embedding space. This strategy can strengthen the ability
of model denoising and reduce noise feature selection. (2) Optimization. After the convergence of
the embedding space, we leverage the evaluator to generate gradient and direction information,
enabling us to effectively steer gradient ascent-based search and identify the embedding for the
optimal feature subset. (3) Generation. We decode the optimal embedding and autoregressively
generate the optimal feature token sequence. Finally, we apply the optimal feature token sequence
to the original feature set to get the best feature subset. In addition, to prepare historical feature
selection experiences and corresponding model performance as training data, we leverage the
automation and exploration properties of reinforcement intelligence to develop a training data
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:3
Fig. 1. Our perspective can be viewed as a sequence generation (b) rather than as an iterative discrete
selection (a).
collector. The collector can explore and collect feature subset-predictive accuracy pairs as training
data. This strategy can avoid intensive manual labor and improve training data quality and diversity.
Our main contributions can be summarized as follows:
(1) Generative Perspective: We propose a formulation: feature selection as deep sequential gener-
ative AI to convert the discrete selection process into continuous optimization.
(2) Embedding-Optimization-Generation (EOG) framework: We develop the EOG framework:
embedding feature subsets to vectors, gradient-steered optimal embedding identification,
and feature token sequence generation. Extensive experiments show that this generative
framework improves the effectiveness and generalization of feature selection in various data
domains.
(3) Computing Techniques: We design interesting techniques to address computing issues: (a)
reinforcement as an automated feature selection training data collector, (b) variational
transformer with multi-losses as optimization supervision, and (c) performance evaluator
function as gradient generator.
(4) Extensive Experiments: We conduct extensive experiments and case studies across 16 real-
world datasets to demonstrate the effectiveness, robustness, and scalability of our framework.
2 Preliminaries and Problem Statement
Feature Token Sequence. We formulate a feature subset as a feature token sequence so that we can
encode it into an embedding space with a deep sequential model. Specifically, we treat each feature
as a token and construct a mapping table between features and tokens. For example, given a feature
subset [51, 52, 54, 57], we convert it to a feature token sequence denoted as [($(, C 1, C2, C4, C7, $( ].
Sequential Training Data. To construct a differential embedding space for feature selection, we
need to collect # different feature subset-accuracy pairs from the original feature set as training
data. Then we convert all feature subsets to feature token sequences. These data are denoted by
' = (t8, E8 )#
8=1, where t8 = [C1, C2, ..., C@] is the feature token sequence of the 8th feature subset and E8
is corresponding downstream predictive accuracy.
Problem Statement. Formally, given a tabular dataset  = (- , ~), where - is an original feature
set and y is the corresponding target label. We collect the sequential training data ' by conducting
automatically traditional feature selection algorithms on  and evaluating the performance of
feature subsets with a downstream ML model. Our goal is to (1) embed the knowledge of ' into a
differentiable continuous space and (2) generate the optimal feature subset. Regarding goal 1, we
learn an encoder q, an evaluator o, and a decoder k via joint optimization to get the feature subset
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:4 W. Ying et al.
Fig. 2. An overview of VTFS. First, we employ the variational transformer-based sequential model to construct
feature subset embedding space. Second, we search for better embeddings by moving local optimal embeddings
along the gradient direction maximizing the downstream predictive accuracy. Third, we generate the feature
token sequences in an autoregressive manner based on these better embeddings and keep the best one with
the highest downstream ML performance.
embedding space E. Regarding goal 2, we identify the best embedding based on a gradient search
method and generate the optimal feature token sequence t∗:
t∗ = k (∗) = arg max
 ∈ E
M (- [k ()], ~), (1)
where k is a decoder to generate a feature token sequence from any embedding of E; ∗ is the
optimal feature subset embedding; M is a downstream ML task. - [] means we use the mapping
table to convert a feature token sequence to a feature subset. Finally, we apply f ∗ to - to select the
optimal feature subset - [t∗].
3 Methodology
3.1 Framework Overview
Figure 2 shows our framework (VTFS), which includes three steps: (1) feature subset embedding
space construction, (2) gradient-steered optimization, and (3) optimal feature subset generation.
Specifically, Step 1 is to embed the knowledge of feature selection into a continuous embedding
space. To accomplish this, we develop an encoder–decoder–evaluator architecture, in which the
encoder encodes each feature token sequence into an embedding vector; the evaluator estimates the
downstream prediction task accuracy based on the corresponding embedding; the decoder recon-
structs the associated feature token sequence using the embedding. To construct a distinguishable
and smooth embedding space, we employ a variational transformer as the backbone of the sequen-
tial model. We jointly optimize the sequence reconstruction loss and the performance estimation
loss to learn such an embedding space. Then, we employ the gradient-steered search to find the
better embeddings in Step 2. We select the top- k feature token sequence from the collected data
based on predictive accuracy. They are converted into embeddings using the well-trained encoder.
After that, based on the gradient of the well-trained evaluator, we move these embeddings along
the direction maximizing the downstream task performance to get better ones. Finally, in Step 3, we
feed the better embeddings into the well-trained decoder to generate the feature token sequences
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:5
and then convert them to the feature subsets. The feature subset with the highest downstream ML
performance is regarded as the optimal result.
3.2 Feature Subset Embedding Space Construction via Variational Transformer
The success of ChatGPT illustrates that intricate human knowledge can be effectively embedded
within a large embedding space via sequential modeling. This inspiration encourages that feature
selection, as a form of human knowledge, can likewise be integrated into a continuous embedding
space. However, different from ChatGPT, we expect this embedding space should not only preserve
the knowledge of feature subsets but also maintain the quality of these subsets. This is crucial for
the effective identification of the optimal feature selection result. To achieve this, we develop an
encoder–decoder–evaluator learning paradigm. The advantages of this perspective are (1) convert
discrete search into continuous optimization in embedding space; (2) enable the integration of
generalization and robustness techniques.
Feature Subsets as Sequences with Shuffling-Based Augmentations . The sequential training data
are used to construct the continuous embedding space. We find that the order of the feature token
sequence doesn’t influence the predictive accuracy. Thus, we propose a shuffling-based strategy
to quickly collect more legal data samples. For instance, give one sample [C1, C2, C3] → 0.867. We
can shuffle the order of the sequence to generate more semantically equivalent data samples:
[C2, C1, C3] → 0.867, [C3, C2, C1] → 0.867. The shuffling augmentation strategy enhances both the
volume and diversity of data, enabling the construction of an empirical training set that more
accurately represents the true population. This strategy is significant in developing a more effective
continuous embedding space.
Variational Transformer-Based Feature Subset Embedding Model. We develop an encoder–decoder–
evaluator framework to embed complex feature learning knowledge into a continuous embedding
space. Such a space should preserve the influence of different feature subsets, while also maintaining
a smooth structure to facilitate the identification of superior embeddings. To accomplish this, we
adopt the variational transformer [ 18, 42] as the backbone of the sequential model to implement
this framework.
The Encoder aims to embed various observed feature subsets (e.g., feature token sequences)
into an embedding vector, each of which is associated with a corresponding utility. We use a
variational transformer to encode the observed feature subsets. The transformer encodes token
sequences with self-attention and constructs an embedding space more accurately. The variational
module regularizes the distribution of a latent embedding space into a normal distribution to
smooth the embedding space and advance downstream tasks. Formally, consider a training dataset
' = (t8, E8 )#
8=1, where t8 = [C1, C2, ..., C@] is a feature token sequence of the 8th feature subset, E8 is
the corresponding predictive accuracy, @ is the number tokens of the 8th feature token sequence,
and # is the number of training samples. To simplify the notation, we use the notation (t, E) to
represent any training sample. We first employ a transformer encoder q to learn the embedding of
the feature token sequence, denoted by e = q (t). We assume that the learned embeddings e follow
the format of normal distribution. Then, two fully connected layers are implemented to estimate
the mean m and variance f of this distribution. After that, we can sample an embedding vector e∗
from the distribution via the reparameterization technique. This process is denoted by
e∗ = m + Y ∗ 4G? (f), (2)
where Y refers to the noised vector sampled from a standard normal distribution. The sampled
vector e∗ is regarded as the input of the following decoder and evaluator.
The Decoder aims to reconstruct a feature token sequence using the embedding e∗. When the
best embedding point is obtained from the optimization step, the decoder can generate the optimal
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:6 W. Ying et al.
feature token sequence in an autoregressive manner. We utilize a transformer decoder to parse
the information of e∗ and add a softmax layer behind it to estimate the probability of the next
feature token based on the previous ones. Formally, the current token that needs to be decoded is
C 9 , and the previously completed feature token sequence is C1...C 9 −1. The probability of the 9th token
should be
%k (C 9 | e∗, [C1, C2, ..., C 9 −1]) = 4G? (I 9 )Í
@ 4G? (I) , (3)
where I 9 represents the 9th output of the softmax layer, k refers to the decoder. The joint estimated
likelihood of the entire feature token sequence should be
%k (t| e∗) =
@Ö
9=1
%k (C 9 | e∗, [C1, C2, ..., C 9 −1]) . (4)
The Evaluator aims to evaluate the predictive accuracy based on the embedding e∗ and then
provides a gradient to facilitate the identification of the best embedding points through gradient-
based search methods. More specifically, we implemented a single fully connected neural layer,
followed by a regressor as the evaluator. Each embedding corresponds with a downstream predictive
accuracy. The evaluator aims to predict the accuracies based on the embeddings when training the
EOG framework. After convergence, the well-trained evaluator will provide a gradient to guide the
search direction in the continuous space to identify the embedding with the highest accuracy. This
calculation process can be denoted by
¥E = o (e∗), (5)
where o refers to the evaluator and ¥E is the predicted accuracy via o.
The Joint Optimization.We jointly train the encoder, decoder, and evaluator to learn the continuous
embedding space. There are three objectives: (a) Minimizing the reconstruction loss between the
reconstructed feature token sequence and the real one, denoted by
LA42 = −;>6%k (t| e∗)
= −
@Õ
9=1
;>6%k (C 9 | e∗, [C1, C2, ..., C 9 −1]), (6)
(b) Minimizing the estimation loss between the predicted accuracy and the real one, denoted by
L4EC = "( (E, ¥E), (7)
(c) Minimizing the KL divergence between the learned distribution of the feature subset and the
standard normal distribution, denoted by
L:; = 4G? (f) − ( 1 + f) + ( <)2. (8)
The first two objectives ensure that each point within the embedding space is associated with a
specific feature subset and its corresponding predictive accuracy. The last objective smoothens the
embedding space, thereby enhancing the efficacy of the following gradient-steered search step. We
tradeoff these three losses and jointly optimize them by
L = U L4EC + VLA42 + W L:; , (9)
where U, V, and W are hyperparameters.
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:7
3.3 Gradient-Steered Optimization
After obtaining the feature subset embedding space, we employ a gradient-ascent search method to
find better feature subset embedding. More specifically, we initiate the process by selecting the top-:
feature token sequences from the collected data based on the corresponding predictive accuracies.
Subsequently, we leverage the encoder that has been well-trained in the last step to convert these
feature token sequences into local optimal embeddings. After that, we adopt a gradient-ascent
algorithm to move these embeddings along the direction maximizing the downstream predictive
accuracy. The gradient utilized in this process is derived from the well-trained evaluator o. Taking
the embedding e∗ as an illustrative example, the moving calculation process is as follows:
e+ = e∗ + [ mo
me∗ , (10)
where [ is the moving steps and e+ is the better embedding.
3.4 Optimal Feature Subset Generation
Once we identify the better embeddings, we will generate the better feature token sequences
based on them in an autoregressive manner. Formally, we take the embedding e+ as an example
to illustrate the generation process. In the 9-iteration, we assume that the previously generated
feature token sequence is C1...C 9 −1 and the waiting to generate token is C 9 . The estimation probability
for generating C 9 is to maximize the following likelihood based on the well-trained decoder k :
C 9 = arg max(%k (C 9 | e+, [C1, ..., C 9 −1]) . (11)
We will iteratively generate the possible feature tokens until finding the end token (i.e., <EOS>). For
instance, if the generated token sequence is “ [C2, C6, C5, < $( >, C8], we will cut from the <EOS>
token and keep [C2, C5, C6] as the final generation result. Finally, we select the corresponding features
according to these feature tokens and output the feature subset with the highest predictive accuracy
as the optimal feature subset. Algorithm 1 shows the pseudo-code of the entire optimization
procedure.
3.5 Improvements: Reinforced Data Collector for Sequential Training Data
The construction of embedding space needs to collect training data about observed experiences
on how generating a feature subset can lead to improved performance. The volume, quality, and
diversity of training data influence the quality of embeddings learned by the EOG framework,
thereafter, impact the utility of a generated feature subset. We choose Reinforcement Learning
(RL) to collect training data for three aspects: (1) Volume: we should collect a lot of training
data. The self-learning of RL enables automated data generation; (2) Quality: we should collect
high-performance cases as successful experiences. The exploitation of RL facilitates the generation
of more high-performance training data. (3) Diversity: training data should not ignore random,
exploratory, and failure cases as lessons. The exploration of RL can diversify the training data. Our
perspective is to view reinforcement intelligence as a training data collector in order to achieve
volume (self-learning enabled automation), diversity (exploration), and quality (exploitation).
To implement this idea, we design reinforcement agents to automatically decide how to select
crucial and effective features, as shown in Figure 3. The reinforcement exploration experiences
and corresponding accuracy will be used as training data. Specifically, the approach includes:
(1) Multi-Agents: We design agents for each feature. (2) Actions: In each reinforcement iteration,
each agent will determine whether to select the corresponding feature. Then the selected features
constitute a feature subset. (3) Environment: The environment is the feature space, representing an
updated feature subset. When agents take actions to select a new feature subset, the state of feature
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:8 W. Ying et al.
Algorithm 1: Entire Optimization Procedure
Input : The original dataset  = (- , ~)
Output :The Optimal Feature Subset - [t∗]
1 Collecting training data set ' = (t8, E8 )#
8=1.
2 Initialize the encoder q, decoder k and evaluator \ .
3 Feature Subset Embedding Space Construction:
4 for 8= 4?>2ℎ do
5 for 8= =D<14A > 5 10C2ℎ4B do
6 Encode: e = q (t).
7 Estimate: m, f.
8 Reparameterization: e∗ = m + Y ∗ 4G? (f).
9 Decode loss: LA42 = −;>6%k (t| e∗).
10 Evaluate loss: L4EC = "( (E, \ (e∗)) .
11 KL loss: L:; = 4G? (f) − ( 1 + f) + ( m)2.
12 Backward: L = U L4EC + VLA42 + W L:;
13 end
14 end
15 Gradient-steered Optimization:
16 Select top-: feature token sequences (t): from '.
17 Encode and Reparameterization: (e∗): = A4?0A0<4C4A8I0C8>= (q (( t): )).
18 Update (e∗): with [ steps: (e+): = (e∗): + [ ∗ mo
m (e∗ ): .
19 Optimal Feature Subset Generation:
20 Generation: (t+): = k (( e∗): ).
21 Optimal feature subset: X[ t∗] = arg max M (- [( t+): ], ~).
Fig. 3. Reinforcement data collector.
space (environment) changes. The state represents the statistical characteristics of the selected
feature subspace. (4) Reward Function: The reward is the predictive accuracy of the downstream
Random Forest (RF) model based on the current environment. (5) Training and Optimization :
Our reinforcement data collector includes two stages at each iteration: control and training. In
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:9
Table 1. Dataset Key Statistics
Dataset Task #Samples #Features
SpectF C 267 44
SVMGuid3 C 1243 21
German Credit C 1001 24
UCI Credit C 30,000 25
SpamBase C 4,601 57
Ap_omentum C 275 10,936
Ionosphere C 351 34
Activity C 10,299 561
Mice-Protein C 1,080 77
Openml-586 R 1,000 25
Openml-589 R 1,000 25
Openml-607 R 1,000 50
Openml-616 R 500 50
Openml-618 R 1,000 50
Openml-620 R 1,000 25
Openml-637 R 500 50
We reported F1-score for classification (C) and 1-RAE for regression (R), respectively. RAE, relative absolute error.
the control stage, each agent takes actions based on their policy networks, which take the current
state as input and output recommended actions and the next state. The agents will change the
size and contents of a new feature space. We regard the new feature space as an environment.
Meanwhile, the actions taken by feature agents generate an overall reward. This reward will then
be assigned to each participating agent. In the training stage, the agents train their policies via
experience replay independently. The agent uses its corresponding mini-batch samples to train its
Deep Q-Network [30], in order to obtain the maximum long-term reward based on the Bellman
Equation. The agents have naive policies in the beginning and explore diverse feature subsets with
randomness to collect various feature subsets and corresponding RF accuracy. As the agent policies
grow, we can collect more high-quality feature subsets with higher accuracy. In this way, we can
collect lots of training data samples during the iterative exploration process. The implementation
details of the data collector are included in the code released in the abstract.
4 Experiments
4.1 Experimental Setup
Data Description. We perform experiments using a diverse set of 16 datasets sourced from various
domains, including those from UCIrvine and OpenML. These datasets are classified based on their
task types into two categories: (1) classification (C) and (2) regression (R). The statistical details of
these datasets are presented in Table 1.
Evaluation Design. For each of the 16 domain datasets, we randomly constructed two independent
data subsets: A and B. Data subset A was seen by our method. We used this data subset to collect
feature subset-accuracy training data pairs (e.g., 515456 → 0.817) and construct feature subset
embedding space. Data subset B was never seen by our method. After determining the optimal
feature token sequence, such as 525556, using Data subset A, we directly applied this feature token
sequence to Data subset B, yielding the feature subset { 52, 55, 56} . This feature subset was used
to evaluate the effectiveness of our method. We use RF as the predictive model for all datasets.
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:10 W. Ying et al.
The RF is robust, stable, and widely used for evaluation in many feature selection methods. It
controls model-level performance variances in order to examine the impacts of feature selection.
F1-score and 1 -Relative Absolute Error are regarded as the evaluation metrics for classification and
regression tasks, respectively. For the two metrics, the higher the value is, the better the quality of
the feature subset is.
Baseline Algorithms . We compare our method ( VTFS) with 12 widely used feature selection
algorithms: (1) K-BEST [48] selects the top-: features with the highest importance scores; (2) mRMR
[33] selects a feature subset by maximizing relevance with labels and minimizing feature–feature
redundancy; (3) DNP [23] employs a greedy feature selection based on Deep Neural Network
(DNN); (4) DeepPink [29] combines knockoffs [ 1] and DNNs to address feature selection problems;
(5) KnockoffGAN [16] (short as GAN) utilizes GAN to generate knockoff features that are not limited
to Gaussian distribution, enabling feature selection; (6) MCDM [9] ensemble feature selection as a
Multi-Criteria Decision-Making problem, which uses the VIKOR sort algorithm to rank features
based on the judgment of multiple feature selection methods; (7) RFE [7] recursively deletes the
weakest features; (8) LASSO [41] shrinks the coefficients of useless features to zero by sparsity
regularization to select features; (9) LASSONet [21] (short as LNet) is a neural network with sparsity
to encourage the network to use only a subset of input features; (10) GFS [4] is a group-based feature
selection method via interactive RL; (11) MARLFS [25] uses RL to create an agent for each feature
to learn a policy to select or deselect the corresponding feature, and treat feature redundancy and
downstream task performance as rewards; (12) SARLFS [27] is a simplified version of MARLFS to
leverage a single agent to replace multiple agents to decide the selection actions of all features;
(13) GRACES [2] considers the relationship among samples, which transforms a tabular dataset
into a graph to select features. To evaluate the necessity of each technical component of VTFS, we
develop two model variants: (i) VTFS ∗ removes the variational inference component and solely
uses the Transformer to create the feature subset embedding space; (ii) VTFS − adopts LSTM [11] to
learn the feature subset embedding space.
Hyperparameters and Reproducibility. (1) Data Collector: We use the reinforcement data collector
to explore 300 epochs to collect feature subset-predictive accuracy data pairs and randomly shuffle
each feature sequence 25 times to augment the training data. (2) Feature Subset Embedding: We
map feature tokens to a 64-dimensional embedding and use a 2-layer network for both encoder
and decoder, with a multi-head setting of 8 and a feed-forward layer dimension of 256. The latent
dimension of the Variational AutoEncoder is set to 64. The estimator consists of a 2-layer feed-
forward network, with each layer having a dimension of 200. The values of U, V, and W are 0.8, 0.2,
and 0.001, respectively. We set the batch size as 1,024, the training epochs as 100, and the learning
rate as 0.0001. (3) Optimal Embedding Search and Reconstruction: We use the top 25 feature sets to
search for the feature subsets and keep the optimal feature subset.
Environmental Settings. All experiments are conducted on the Ubuntu 22.04.3 LTS operating
system, Intel(R) Core(TM) i9-13900KF CPU@ 3GHz, and 1 way RTX 4090 and 32GB of RAM, with
the Python 3.11.4 and PyTorch 2.0.1.
4.2 Overall Performance
In this experiment, we evaluate the performance of VTFS and baseline algorithms for feature
selection on 16 datasets in terms of F1-score or 1-RAE. Table 2 shows the comparison results. We
can find that VTFS consistently surpasses other baseline models across all datasets, achieving an
average performance improvement of 3% over the second-best baseline model. The underlying
driver of this observation is that VTFS can compress the feature learning knowledge into a large
embedding space. Such a compression facilitates a more effective search for the optimal feature
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:11
Table 2. Overall Performance
Dataset Original K-Best mRMR DNP DeepPink GAN MCDM RFE LASSO LNet GFS MARLFS SARLFS GRACES VTFS
SpectF 75.96 78.21 78.21 80.80 75.01 79.16 80.36 80.80 79.16 75.96 75.01 75.01 79.16 81.86 84.58 (+3.32%)
SVMGuide3 77.81 76.84 76.84 77.12 76.55 77.91 76.66 78.07 77.91 76.44 83.12 76.84 76.22 78.07 85.02 (+2.29%)
German Credit 64.88 66.79 66.79 68.43 64.88 66.31 70.85 64.86 66.4 63.97 67.54 66.31 63.12 69.85 73.50 (+3.74%)
UCI Credit 80.19 80.59 80.59 79.94 80.43 80.59 74.46 80.28 77.94 80.05 79.96 80.24 80.05 80.59 81.21 (+0.77%)
SpamBase 92.68 92.02 92.34 91.79 92.68 92.34 88.95 91.68 91.81 91.67 92.25 92.35 90.94 92.68 93.53 (+0.92%)
Ap_omentum 66.19 84.49 84.49 82.03 82.03 84.49 84.49 84.49 82.03 83.02 82.03 84.49 84.49 83.02 86.52 (+2.40%)
Ionosphere 92.85 91.32 94.27 94.12 92.85 94.27 88.64 95.69 88.17 88.38 91.34 89.92 88.51 95.69 97.13 (+1.50%)
Activity 96.17 96.07 95.92 95.87 96.12 96.17 96.12 95.87 95.92 96.17 96.12 95.87 95.87 96.17 97.33 (+1.21%)
Mice-Protein 74.99 77.32 78.68 77.29 77.47 78.68 78.69 77.29 78.71 76.4 77.35 76.4 74.53 78.68 81.96 (+4.13%)
Openml-586 54.95 57.68 57.64 60.74 58.47 60.74 57.95 58.1 60.67 58.28 62.27 58.27 56.98 62.27 63.99 (+2.76%)
Openml-589 50.95 57.17 57.17 54.68 57.42 57.17 55.43 54.25 58.74 57.55 44.72 57.39 53.48 55.43 61.13 (+4.07%)
Openml-607 51.73 54.64 55.17 55.14 55.68 57.88 55.56 54.39 58.10 55.38 45.7 54.99 53.28 57.88 62.72 (+7.95%)
Openml-616 15.63 26.95 25.45 25.93 26.74 28.56 22.92 24.08 28.98 25.98 22.93 26.29 23.06 28.56 33.85 (+16.8%)
Openml-618 46.89 51.79 51.08 51.73 51.46 52.40 50.9 50.64 47.41 51.11 52.40 51.87 48.54 51.73 55.91 (+6.69%)
Openml-620 51.01 55.03 55.03 55.66 55.66 55.94 55.66 53.96 57.99 55.94 58.99 55.42 53.98 57.99 62.58 (+6.09%)
Openml-637 14.95 21.06 20.49 20.45 20.47 21.12 22.16 17.82 26.02 19.43 39.12 20.75 19.45 26.02 42.18 (+7.82%)
The best and the second-best results are highlighted by bold and underlined fonts, respectively. We evaluate classification (C) and regression (R) tasks in terms of
F1-score and 1-RAE, respectively. The higher the value is, the better the feature space quality is. The bold percentage reflects the improvements of VT FS compared
with the best baseline model.
selection result. Moreover, another interesting observation is that the algorithm ranking second-
best varies across different datasets. A possible reason for the observation is that traditional feature
selection methods are designed based on varying criteria, resulting in a limited generalization
capability across different scenarios. In summary, this experiment shows the effectiveness of VTFS
in feature selection, underscoring the great potential of generative AI in this domain.
4.3 Study of the Influence of Variational Transformer for Continuous Space
Construction
One of the important novelties of VTFS involves a sequential model to embed feature learning
knowledge into an embedding space. To analyze the influence of the selection of the sequential
model, we develop two model variants: (1) VTFS −, which employs an LSTM model as the backbone
of the sequential model; (2) VTFS ∗, which removes the variational inference component and
exclusively uses a transformer model. Figure 4 shows the comparison results in terms of F1-score
and 1-RAE for classification and regression tasks, respectively. We can find that VTFS outperforms
VTFS∗ with a great performance gap across all datasets. The underlying driver for this observation
is that the variational inference component in VTFS enhances the smoothness of the learned
feature subset embedding space. This smoothness facilitates a more effective search for optimal
feature selection results. Additionally, another interesting observation is that VTFS ∗ surpasses
VTFS− across all datasets in both classification and regression tasks. A potential reason for this
observation is that the transformer architecture, compared to LSTM, is more adept at capturing
complex correlations between different feature combinations and their impact on downstream
ML task performance. Moreover, it is noticed that even when solely employing LSTM, VTFS −
still outperforms the second-best baseline algorithm across various datasets. This observation
underscores the success and effectiveness of the generative AI perspective of VTFS. In conclusion,
this experiment indicates the necessity of each technical component of VTFS.
4.4 Study of the Effectiveness of RL-Based Data Collector
In VTFS, we emphasize the capability of the RL-based data collector to gather higher-quality
and more diverse training data, thereby facilitating the construction of a better embedding space.
To assess the impact of the RL-based data collector, we established three control groups on four
datasets: (1) randomly collecting training data samples to construct the feature subset embedding
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:12 W. Ying et al.
Fig. 4. Analysis of the impact of different feature subset embedding modules on feature selection.
space and generate the feature subset; (2) using the second best baseline of each dataset to obtain
the feature subset; (3) directly using original feature set for prediction. Figure 5 shows that the
training data collected by the RL-data collector can help identify a feature subset superior to all
control groups. The underlying driver is that the RL-based data collector can produce higher-quality
and diverse data, contributing to the creation of a more effective embedding space. This enhanced
embedding space facilitates the identification of the best feature subset based on the gradient
search method. Another observation is when constructing the embedding space using randomly
collected data and subsequently searching for the optimal feature subset, the performance in the
downstream ML task significantly improves compared to the original feature set but in three cases
worse than the second-best baselines. This suggests that VTFS can learn feature subset knowledge,
thereby identifying an effective feature subset to improve downstream performance. However,
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:13
Fig. 5. Analysis of the effectiveness of data collector on selecting the effective feature subset.
Fig. 6. Analysis of the impact of data augmentation on selecting the effective feature subset.
collecting diverse training data is necessary and important, which makes the embedding space
more distinguishable to identify superior feature selection outcomes. In summary, this experiment
demonstrates that the RL-based data collector is an indispensable component to maintain the
excellent feature selection performance of VTFS.
4.5 Study of the Impact of Data Augmentation
Since the order of the feature token sequence does not influence the downstream predictive accu-
racy, we propose a data augmentation strategy by randomly shuffling the feature token sequence to
generate more legal training samples. To assess the impact of data augmentation, we incrementally
increase the number of shufflings and observe its impact on performance improvements. From
Figure 6, we can observe that with the increase of the shuffling number, the downstream ML perfor-
mance has also been improved across different datasets with great gaps. A potential explanation for
this observation is that the augmentation of shuffling epochs enhances data diversity and volume.
These enhancements significantly improve the construction of a distinguishable and informative
embedding space, yielding superior feature selection performance. In summary, the experiment
reflects the necessity of the data augmentation strategy in VTFS for keeping good performance.
4.6 Study of the Training Data Consistent Quality Collected by RL-Based Data Collector
and Shuffling
Since there is randomness in RL-based data collector and data shuffling, we develop variants to verify
the impact of potentially inconsistent training data: (1) VTFS-RL: using two different random seeds
to initial RL respectively and then collect the training data; (2) VTFS-Shuffle: using two different
random seeds to shuffle the training data of VTFS, respectively. Figure 7 shows that the final
performance of the best feature subset generated by our framework has slight fluctuations due to
the inconsistent quality of data samples. However, our method still achieves superior performance
compared to the best baselines. The underlying explanation is that despite the RL-based data
collector and shuffling operation causing potential data inconsistency, the collected training data
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:14 W. Ying et al.
Fig. 7. Analysis of the training data consistent quality.
Table 3. Time and Space Complexity Analysis in Terms of the Feature Size, Running Time, and
Parameter Size
#Features #Samples Data Collect
300 Epochs
Parameter
Size
Training Time
100 Epochs
Inference
Time
SpectF 44 267 66.15 0.387231 MB 67.68 0.29
SVMGuide3 21 1,243 140.45 0.382792 MB 55.15 0.13
German Credit 24 1,001 102.18 0.383371 MB 65.93 0.12
UCI Credit 25 30,000 2710.51 0.383371 MB 63.67 0.12
SpamBase 57 4601 390.88 0.38974 MB 66.95 0.40
Ap_omentum 10,936 275 10,315.71 2.489387 MB 1,118.52 22.08
Ionosphere 34 351 67.96 0.385301 MB 61.14 0.16
Activity 561 10,299 9052.31 0.487012 MB 762.85 4.53
Mice-Protein 77 1,080 634.77 0.3936 MB 68.35 0.51
Openml-586 25 1,000 225.42 0.383564 MB 61.74 0.12
Openml-589 25 1,000 209.02 0.383564 MB 61.53 0.12
Openml-607 50 1,000 326.04 0.388389 MB 70.12 0.32
Openml-616 50 500 165.69 0.388389 MB 68.17 0.32
Openml-618 50 1,000 341.57 0.388389 MB 70.56 0.32
Openml-620 25 1,000 209.22 0.383564 MB 62.89 0.12
Openml-637 50 500 164.20 0.388389 MB 68.87 0.32
remains high-quality. The continuous space constructed by our framework based on observed
diverse training datasets remains effective and robust, thereby generating the optimal feature
subset.
4.7 Study of the Time and Space Complexity
To assess the time and space complexity of VTFS, we report VTFS’s training time, inference time,
parameter size, and data collection time across all datasets. Table 3 shows the comparison results.
For a more clear comparison, we organized the dataset for comparison based on the feature number
and dataset category, as shown in Figures 8 and 9. In the model training stage, the model training
time and parameter size increase with the growth of the feature number. We can observe that as the
feature number increases from 21 (SVMGuide3) to 10,936 (AP _omentum) (520-fold increase), there
is only a 20-fold increase (55.15 s to 1118.52 s) in the training time and a 7-fold increase (0.3827
MB to 2.4894 MB) in model size. In other words, despite the substantial increase in the number of
features, the corresponding growth in training time and space complexity is relatively modest. In
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:15
Fig. 8. Time and space complexity analysis on classification task in terms of the feature size, training time,
inference time, parameter size, and data collection time.
Fig. 9. Time and space complexity analysis on regression task in terms of the feature size, training time,
inference time, parameter size, and data collection time.
the inference stage (from inputting a feature token sequence to outputting the best feature token
sequence), we can observe that the time cost still increases with the growth of the feature number.
However, the prediction time in this stage is in the millisecond range, resulting in a very short
time despite a huge number of features. The underlying driver is that we embed the feature token
sequence into a fixed and low-dimensional embedding, making the gradient-steered optimization
process complete within a very short time. Thus, this observation indicates that VTFS exhibits
exceptional scalability, especially when dealing with high-dimensional feature spaces. In the data
collection stage, we observe that the time required for RL-based data collection increases with
the growth of the feature number and sample number. For example, the feature number of the
UCI Credit dataset is relatively small (25), but the sample number is huge (30,000), resulting in a
high data collecting time compared to the dataset of a similar feature number (e.g., the German
Credit dataset). The reason is that the RL-based data collector uses a supervised downstream to
evaluate the utility of the feature subset in each iteration. The dataset with more samples needs
more time to train the downstream ML task. Despite taking relatively longer compared to model
training, this process is entirely automated, reducing the need for manual intervention. It can
learn and adapt to different data collection scenarios, thereby enhancing the adaptability and
effectiveness of data collection. Furthermore, We analyze the computation complexity between
VTFS and baselines. Figure 10 shows the K-best, mRMR, LASSO, RFE, and MCDM cost less time, but
are less accurate. Compared with other baselines such as DeepPink, GRACES, MARLSFS, and so on,
our method costs less and achieves superior performance. However, (1) feature selection is not a
data preparation/processing step and not timing critical for most tasks; (2) the time cost increase of
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:16 W. Ying et al.
Fig. 10. Time complexity analysis between VTFS and baselines. The x-axis and y-axis represent the perfor-
mance and time cost of each method, respectively.
Fig. 11. Analysis of the robustness of VTFS on different downstream ML models. DT, decision tree; KNN,
K-nearest neighborhood; SVM, support vector machine; XGB, XGBoost.
training our method is acceptable. Compared with the time costs (days or months level) of human
manual feature engineering, our method saves time. (3) Although our method costs a bit more time
compared to some baselines, it achieves much better feature engineering performance. (4) Based on
such encode–decode generative design, we can use the strategy of pretraining a foundation model
and then finetuning to reduce training time costs.
4.8 Robustness Check
To evaluate the robustness of different feature selection algorithms with varying downstream ML
models, we replace the RF model with support vector machine, XGBoost, K-nearest neighborhood,
and decision tree. The performance of these algorithms was then evaluated using the SVMGuide3
and German Credit datasets. Figure 11 shows the comparison results in terms of F1-score. We
can find that VTFS consistently beats other feature selection baselines regardless of the down-
stream ML model. The underlying driver is that VTFS can tailor the feature selection strategy
based on the specific characteristics of downstream ML models. This is achieved by collecting
suitable sequential training data that is most suitable for each model type. Moreover, VTFS embeds
feature learning knowledge into a continuous embedding space which enhances its robustness and
generalization capability across different ML models. In summary, this experiment demonstrates
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:17
Fig. 12. Case Study: Each dataset consists of 5 real features and 45 fake features. When compared to MARLFS,
VTFS demonstrates a superior ability to select feature subsets that are more closely to the real features in
both datasets and effectively avoid identifying fake features as real ones.
that VTFS can maintain its excellent and stable feature selection performance across different
ML models.
4.9 Case Study: VTFS Exhibits Noise Resistance and Quality Feature Attention
The OpenML datasets are simulated by human experts. So we know the real relevant features within
these datasets. Thus, we design a case study to show the overlap between the selected features
and the real ones. Here, we take openml _607 and openml _618 datasets as examples. Both of them
have 5 real features and 45 fake features. We employ MARLFS [ 25] to serve as a comparative model
alongside VTFS. Figure 12 shows the comparison results. Regarding the openml _607 dataset, we
can find that VTFS selects 7 features, of which 4 are real and 3 are fake. In contrast, MARLFS selects
27 features, with only 4 being real and the remaining 23 being fake. For the openml _618 dataset,
VTFS maintains a similar performance. While MARLFS successfully identifies all real features, it
also includes 19 fake features in its selection. These observations indicate that, in comparison to
MARLFS, VTFS is more effective at understanding the complex relationships within the feature
space. As a result, it is able to produce a feature subset that more closely aligns with the actual
features, thereby reducing the likelihood of making false-positive errors. In summary, this case
study demonstrates that VTFS exhibits robustness in filtering out noise within the feature space
and is capable of producing high-quality and reliable feature subsets.
5 Related Work
Feature selection methods are an important part of feature engineering [ 6, 12, 44, 45, 49, 50], which
can be divided into three categories according to the selection strategies [ 22]: (1) filter methods; (2)
wrapper methods; (3) embedded methods.
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:18 W. Ying et al.
The filter methods [10, 33, 48] evaluate features by calculating the correlation between features
based on statistical properties of data and selects the feature subset with the highest score. Univariate
statistical tests, such as variance analysis F-test [ 3], are widely used in filter methods. The F-statistic
values are used as ranking scores for each feature, where higher F-statistic values correspond to
more important features. Other classical statistical methods, including Student’s t-test [53], Pearson
correlation test [28], Chi-square test [ 40], Kolmogorov-Smirnov test [ 15], Wilks lambda test [ 14],
and Wilcoxon signed-rank test [ 35], can be similarly applied to feature selection. These methods
have low computational complexity and can efficiently select feature subsets from high-dimensional
datasets. However, they ignore the dependency and interaction among features, potentially leading
to suboptimal results.
The wrapper methods [20, 24, 27, 43, 52] are based on a specific dataset, define a ML model in
advance, and iteratively evaluate the candidate feature subset. For instance, RL-based methods
model the feature selection process with a multi-agent system, where agents decide whether to
select a particular feature, optimize the utility of selected feature subsets, and use the utility and
feature redundancy as reward feedback in each iteration. These methods often outperform filter
methods as they enumerate various combinations of feature subsets. However, due to the need
to enumerate all possible feature subsets, it is an NP-hard problem, and the evaluation using
downstream ML models after each iteration leads to lower computational efficiency. These methods
may suffer from convergence difficulties and instability, potentially making it difficult to identify
the optimal feature subset.
The embedded methods [7, 13, 21, 41] transform the feature selection task into a regularization
term in the prediction loss of a ML model to accelerate the selection process. For example, LASSO
assumes a linear dependency between input features and output, penalizing the L1 norm of feature
weights. LASSOasso produces a sparse solution where the weights of irrelevant features are set to
zero. However, LASSO fails to capture non-linear dependencies. The three types of methods have
excellent performance on specific ML models. However, the filter and embedded methods exhibit
limited generalization ability over various domain datasets and downstream predictive models.
The wrapper methods suffer from large search space and cannot ensure the identification of global
optimal.
In addition, other studies have proposed two types of hybrid feature selection methods: (1)
homogeneous methods [ 34, 36, 38]; (2) heterogeneous methods [ 8, 37, 46]. However, these methods
are limited by the basic aggregation strategies. Thus, it is critical to develop a new research
perspective to enhance the generalization and effectiveness. In contrast to the above existing works,
we propose a novel generative AI perspective that embeds the knowledge of feature selection into
a continuous embedding space and then effectively identifies feature subsets using the gradient-
steered search and autoregressive generation.
6 Conclusion
This article explores a new research perspective on the feature selection problem: embedding feature
selection knowledge into a continuous space and generating the best feature subsets based on a
gradient-ascent search method. We implement a three-step framework to map feature subset into
an embedding space for optimizing feature selection: (1) We develop a deep variational transformer-
based encoder–decoder–evaluator framework to learn a continuous embedding space that can map
feature subsets into embedding vectors associated with utility scores. (2) We leverage the well-
trained feature subset utility evaluator as a gradient provider to identify the optimal feature subset
embedding. (3) We decode the optimal feature subset embedding to generate the best feature subset
in an autoregressive manner. Our research findings indicate that (1) the encoder–decoder–evaluator
framework effectively constructs the feature subset embedding space and maintains the utility of
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:19
feature subsets; (2) the gradient-based search strategy generates gradient and direction information
to effectively steer the gradient ascent-based search and identify the optimal feature subset. In
the future, we aim to enhance the generalization capability of VTFS across various domains,
scenarios, and distributions, and validate the method in real-world application scenarios such as
bioinformatics.
References
[1] Emmanuel Jean Candès, Yingying Fan, Lucas Janson, and Jinchi Lv. 2016. Panning for gold: Model-free knockoffs for
high-dimensional controlled variable selection , Vol. 1610. Department of Statistics, Stanford University Stanford, CA,
USA.
[2] Can Chen, Scott T. Weiss, and Yang-Yu Liu. 2023. Graph convolutional network-based feature selection for high-
dimensional and low-sample size data. Bioinformatics 39, 4 (April 2023), btad135. DOI: https://doi.org/10.1093/
bioinformatics/btad135 https://academic.oup.com/bioinformatics/article-pdf/39/4/btad135/50087112/btad135.pdf
[3] Nadir Omer Fadl Elssied, Othman Ibrahim, and Ahmed Hamza Osman. 2014. A novel feature selection based on
one-way anova f-test for e-mail spam classification. Research Journal of Applied Sciences, Engineering and Technology
7, 3 (2014), 625–638.
[4] Wei Fan, Kunpeng Liu, Hao Liu, Ahmad Hariri, Dejing Dou, and Yanjie Fu. 2021. Autogfs: Automated group-based
feature selection via interactive reinforcement learning. In Proceedings of the SIAM International Conference on Data
Mining (SDM ’21). SIAM, 342–350.
[5] George Forman. 2003. An extensive empirical study of feature selection metrics for text classification. Journal of
Machine Learning Research 3 (March 2003), 1289–1305.
[6] Nanxu Gong, Wangyang Ying, Dongjie Wang, and Yanjie Fu. 2024. Neuro-symbolic embedding for short and effective
feature selection via autoregressive generation. arXiv: 2404.17157. Retrieved from https://doi.org/10.48550/arXiv.2404.
17157
[7] Pablo M. Granitto, Cesare Furlanello, Franco Biasioli, and Flavia Gasperi. 2006. Recursive feature elimination with
random forest for PTR-MS analysis of agroindustrial products. Chemometrics and Intelligent Laboratory Systems 83, 2
(2006), 83–90.
[8] Mohammad Nazmul Haque, Nasimul Noman, Regina Berretta, and Pablo Moscato. 2016. Heterogeneous ensemble
combination search using genetic algorithm for class imbalanced data classification. PLoS One 11, 1 (2016), e0146116.
[9] Amin Hashemi, Mohammad Bagher Dowlatshahi, and Hossein Nezamabadi-pour. 2022. Ensemble of feature selection
algorithms: A multi-criteria decision-making approach. International Journal of Machine Learning and Cybernetics 13,
1 (2022), 49–69.
[10] Xiaofei He, Deng Cai, and Partha Niyogi. 2005. Laplacian score for feature selection. Advances in Neural Information
Processing Systems 18 (2005), 507–514.
[11] Sepp Hochreiter and Jürgen Schmidhuber. 1997. Long short-term memory. Neural Computation 9, 8 (1997), 1735–1780.
[12] Xiaohan Huang, Dongjie Wang, Zhiyuan Ning, Ziyue Qiao, Qingqing Long, Haowei Zhu, Min Wu, Yuanchun Zhou,
and Meng Xiao. 2024. Enhancing tabular data optimization with a flexible graph-based reinforced exploration strategy.
arXiv:2406.07404. Retrieved from https://doi.org/10.48550/arXiv.2406.07404
[13] Yanyong Huang, Zongxin Shen, Yuxin Cai, Xiuwen Yi, Dongjie Wang, Fengmao Lv, and Tianrui Li. 2023. C2IMUFS:
Complementary and consensus learning-based incomplete multi-view unsupervised feature selection. IEEE Transac-
tions on Knowledge and Data Engineering 35, 10 (2023), 10681–10694. DOI: https://doi.org/10.1109/TKDE.2023.3266595
[14] Rianne Hupse and Nico Karssemeijer. 2010. The effect of feature selection methods on computer-aided detection of
masses in mammograms. Physics in Medicine & Biology 55, 10 (2010), 2893.
[15] Alexei Ivanov and Giuseppe Riccardi. 2012. Kolmogorov-Smirnov test for feature selection in emotion recognition
from speech. In Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP
’12). IEEE, 5125–5128.
[16] James Jordon, Jinsung Yoon, and Mihaela van der Schaar. 2018. KnockoffGAN: Generating knockoffs for feature selec-
tion using generative adversarial networks. In Proceedings of the International Conference on Learning Representations .
[17] YeongSeog Kim, W. Nick Street, and Filippo Menczer. 2000. Feature selection in unsupervised learning via evolutionary
search. In Proceedings of the 6th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining ,
365–369.
[18] Diederik P. Kingma and Max Welling. 2013. Auto-encoding variational bayes. https://doi.org/10.48550/arXiv.1312.6114
[19] Ron Kohavi and George H. John. 1997. Wrappers for feature subset selection. Artificial Intelligence 97, 1–2 (1997),
273–324.
[20] Riccardo Leardi. 1996. 3 - Genetic Algorithms in Feature Selection. In Genetic Algorithms in Molecular Modeling,
James Devillers (Ed.). Academic Press, London, 67–86. DOI: https://doi.org/10.1016/B978-012213810-2/50004-9
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
221:20 W. Ying et al.
[21] Ismael Lemhadri, Feng Ruan, and Rob Tibshirani. 2021. Lassonet: Neural networks with feature sparsity. In Proceedings
of the International Conference on Artificial Intelligence and Statistics. PMLR, 10–18.
[22] Jundong Li, Kewei Cheng, Suhang Wang, Fred Morstatter, Robert P. Trevino, Jiliang Tang, and Huan Liu. 2017. Feature
selection: A data perspective. ACM Computing Surveys (CSUR) 50, 6 (2017), 1–45.
[23] Bo Liu, Ying Wei, Yu Zhang, and Qiang Yang. 2017. Deep neural networks for high dimension, low sample size data.
In Proceedings of the International Joint Conference on Artificial Intelligence , 2287–2293.
[24] Dugang Liu, Pengxiang Cheng, Hong Zhu, Xing Tang, Yanyu Chen, Xiaoting Wang, Weike Pan, Zhong Ming, and
Xiuqiang He. 2023. DIWIFT: Discovering instance-wise influential features for tabular data. In Proceedings of the ACM
Web Conference 2023, 1673–1682.
[25] Kunpeng Liu, Yanjie Fu, Pengfei Wang, Le Wu, Rui Bo, and Xiaolin Li. 2019. Automating feature subspace exploration
via multi-agent reinforcement learning. In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge
Discovery & Data Mining , 207–215.
[26] Kunpeng Liu, Dongjie Wang, Wan Du, Dapeng Oliver Wu, and Yanjie Fu. 2023b. Interactive reinforced feature selection
with traverse strategy. Knowledge and Information Systems 65, 5 (2023), 1935–1962.
[27] Kunpeng Liu, Pengfei Wang, Dongjie Wang, Wan Du, Dapeng Oliver Wu, and Yanjie Fu. 2021. Efficient reinforced
feature selection via early stopping traverse strategy. In Proceedings of the IEEE International Conference on Data
Mining (ICDM ’21). IEEE, 399–408.
[28] Yaqing Liu, Yong Mu, Keyu Chen, Yiming Li, and Jinghuan Guo. 2020. Daily activity feature selection in smart homes
based on pearson correlation coefficient. Neural Processing Letters 51 (2020), 1771–1787.
[29] Yang Lu, Yingying Fan, Jinchi Lv, and William Stafford Noble. 2018. DeepPINK: Reproducible feature selection in
deep neural networks. Advances in Neural Information Processing Systems 31 (2018), 8676–8686.
[30] Volodymyr Mnih, Koray Kavukcuoglu, David Silver, Andrei A. Rusu, Joel Veness, Marc G. Bellemare, Alex Graves, Mar-
tin Riedmiller, Andreas K. Fidjeland, Georg Ostrovski, Stig Petersen, Charles Beattie, Amir Sadik, Ioannis Antonoglou,
Helen King, Dharshan Kumaran, Daan Wierstra, Shane Legg, and Demis Hassabis. 2015. Human-level control through
deep reinforcement learning. Nature 518, 7540 (2015), 529–533.
[31] Patrenahalli M. Narendra and Keinosuke Fukunaga. 1977. A branch and bound algorithm for feature subset selection.
IEEE Transactions on Computers 9 (1977), 917–922.
[32] Zhiyuan Ning, Chunlin Tian, Meng Xiao, Wei Fan, Pengyang Wang, Li Li, Pengfei Wang, and Yuanchun Zhou. 2024.
FedGCS: A generative framework for efficient client selection in federated learning via gradient-based optimization.
arXiv:2405.06312. Retrieved from https://doi.org/10.48550/arXiv.2405.06312
[33] Hanchuan Peng, Fuhui Long, and Chris Ding. 2005. Feature selection based on mutual information criteria of max-
dependency, max-relevance, and min-redundancy. IEEE Transactions on Pattern Analysis and Machine Intelligence 27,
8 (2005), 1226–1238.
[34] Barbara Pes, Nicoletta Dessì, and Marta Angioni. 2017. Exploiting the ensemble paradigm for stable feature selection:
A case study on high-dimensional genomic data. Information Fusion 35 (2017), 132–147.
[35] S. Fouzia Sayeedunnisa, Nagaratna P Hegde, and Khaleel Ur Rahman Khan. 2018. Wilcoxon signed rank based
feature selection for sentiment classification. In Proceedings of the Second International Conference on Computational
Intelligence and Informatics (ICCII ’17) . Springer, 293–310.
[36] Borja Seijo-Pardo, Verónica Bolón-Canedo, and Amparo Alonso-Betanzos. 2017. Testing different ensemble configura-
tions for feature selection. Neural Processing Letters 46, 3 (2017), 857–880.
[37] Borja Seijo-Pardo, Verónica Bolón-Canedo, and Amparo Alonso-Betanzos. 2019. On developing an automatic threshold
applied to feature selection ensembles. Information Fusion 45 (2019), 227–245.
[38] Borja Seijo-Pardo, Iago Porto-Díaz, Verónica Bolón-Canedo, and Amparo Alonso-Betanzos. 2017. Ensemble feature
selection: Homogeneous and heterogeneous approaches. Knowledge-Based Systems 118 (2017), 124–139.
[39] V. Sugumaran, V. Muralidharan, and K. I. Ramachandran. 2007. Feature selection using decision tree and classification
through proximal support vector machine for fault diagnostics of roller bearing. Mechanical Systems and Signal
Processing 21, 2 (2007), 930–942.
[40] Ikram Sumaiya Thaseen and Cherukuri Aswani Kumar. 2017. Intrusion detection model using fusion of chi-square
feature selection and multi class SVM. Journal of King Saud University-Computer and Information Sciences 29, 4 (2017),
462–472.
[41] Robert Tibshirani. 1996. Regression shrinkage and selection via the lasso. Journal of the Royal Statistical Society: Series
B (Methodological) 58, 1 (1996), 267–288.
[42] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia
Polosukhin. 2017. Attention is all you need. Advances in Neural Information Processing Systems 30 (2017), 5998–6008.
[43] João Vitorino, Miguel Silva, Eva Maia, and Isabel Praça. 2024. Reliable feature selection for adversarially robust
cyber-attack detection. Annals of Telecommunications abs/2404.04188 (2024), 1–15.
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.
Feature Selection as Deep Sequential Generative Learning 221:21
[44] Xinyuan Wang, Dongjie Wang, Wangyang Ying, Rui Xie, Haifeng Chen, and Yanjie Fu. 2024. Knockoff-guided feature
selection via a single pre-trained reinforced agent. arXiv:2403.04015.
[45] Meng Xiao, Dongjie Wang, Min Wu, Kunpeng Liu, Hui Xiong, Yuanchun Zhou, and Yanjie Fu. 2024. Traceable
group-wise self-optimizing feature transformation learning: A dual optimization perspective. ACM Transactions on
Knowledge Discovery from Data 18, 4 (2024), 1–22.
[46] Meng Xiao, Dongjie Wang, Min Wu, Pengfei Wang, Yuanchun Zhou, and Yanjie Fu. 2023. Beyond discrete selection:
Continuous embedding space optimization for generative feature selection. In Proceedings of the IEEE International
Conference on Data Mining (ICDM ’23). IEEE, 688–697.
[47] Jihoon Yang and Vasant Honavar. 1998. Feature Subset Selection Using a Genetic Algorithm. In Feature Extraction,
Construction and Selection: A Data Mining Perspective, Huan Liu and Hiroshi Motoda (Eds.), Springer, Boston, MA,
117–136. DOI: https://doi.org/10.1007/978-1-4615-5725-8_8
[48] Yiming Yang and Jan O. Pedersen. 1997. A comparative study on feature selection in text categorization. InInternational
Conference on Machine Learning ( ICML) , Vol. 97. Nashville, TN, USA, 35.
[49] Wangyang Ying, Dongjie Wang, Xuanming Hu, Yuanchun Zhou, Charu C. Aggarwal, and Yanjie Fu. 2024. Unsupervised
generative feature transformation via graph contrastive pre-training and multi-objective fine-tuning. arXiv:2405.16879.
[50] Wangyang Ying, Dongjie Wang, Kunpeng Liu, Leilei Sun, and Yanjie Fu. 2023. Self-optimizing feature generation via
categorical hashing representation and hierarchical reinforcement crossing. In Proceedings of the IEEE International
Conference on Data Mining (ICDM ’23). IEEE, 748–757.
[51] Lei Yu and Huan Liu. 2003. Feature selection for high-dimensional data: A fast correlation-based filter solution. In
Proceedings of the 20th International Conference on Machine Learning (ICML ’03) , 856–863.
[52] Weiliang Zhang, Zhen Meng, Dongjie Wang, Min Wu, Kunpeng Liu, Yuanchun Zhou, and Meng Xiao. 2024. Enhanced
gene selection in single-cell genomics: Pre-filtering synergy and reinforced optimization. arXiv:2406.07418. Retrieved
from https://doi.org/10.48550/arXiv.2406.07418
[53] Nina Zhou and Lipo Wang. 2007. A modified T-test feature selection method and its application on the HapMap
genotype data. Genomics, Proteomics & Bioinformatics 5, 3–4 (2007), 242–249.
Received 6 March 2024; revised 5 July 2024; accepted 5 August 2024
ACM Transactions on Knowledge Discovery from Data, Vol. 18, No. 9, Article 221. Publication date: October 2024.