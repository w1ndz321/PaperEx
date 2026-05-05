**==> picture [26 x 26] intentionally omitted <==**

**==> picture [81 x 21] intentionally omitted <==**

**==> picture [56 x 21] intentionally omitted <==**

**==> picture [53 x 21] intentionally omitted <==**

**==> picture [13 x 13] intentionally omitted <==**

Latest updates: hps://dl.acm.org/doi/10.1145/3690624.3709225 

## RESEARCH-ARTICLE 

## **From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive ery Generation** 

**ZHENYU TONG** , University of Chinese Academy of Sciences, Beijing, China 

**CHUAN QIN** , Chinese Academy of Sciences, Beijing, Beijing, China **CHUYU FANG** , Baidu, Inc., Beijing, China 

**PDF Download 3690624.3709225.pdf 26 March 2026 Total Citations:** 5 **Total Downloads:** 393 

**==> picture [21 x 20] intentionally omitted <==**

**Published:** 20 July 2025 

## **Citation in BibTeX format** 

KDD '25: The 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining _August 3 - 7, 2025 Toronto ON, Canada_ 

**Conference Sponsors:** SIGMOD SIGKDD 

**KAICHUN YAO** , Institute of Soware Chinese Academy of Sciences, Beijing, Beijing, China **XI CHEN** , University of Science and Technology of China, Hefei, Anhui, China **JINGSHUAI ZHANG** , Baidu, Inc., Beijing, China 

**View all** 

**Open Access Support** provided by: 

**University of Science and Technology of China** 

**Baidu, Inc.** 

**Chinese Academy of Sciences** 

**University of Chinese Academy of Sciences** 

**Institute of Soware Chinese Academy of Sciences** 

. 

KDD '25: Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.1 (July 2025) hps://doi.org/10.1145/3690624.3709225 ISBN: 9798400712456 

# **From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation** 

## Zhenyu Tong[∗] 

Chuyu Fang Baidu Inc. Beijing, China fangchuyu2022@gmail.com 

Chuan Qin[∗] 

University of the Chinese Academy of Sciences Beijing, China tongzhenyu123@gmail.com 

Computer Network Information Center, Chinese Academy of Sciences Beijing, China chuanqin0426@gmail.com 

Kaichun Yao 

Jingshuai Zhang Baidu Inc. Beijing, China zhangjingshuai0@gmail.com 

## Xi Chen 

Institute of Software, Chinese Academy of Sciences Beijing, China yaokaichun@outlook.com 

University of Science and Technology of China Hefei, China chenxi0401@mail.ustc.edu.cn 

## Hengshu Zhu[†] 

## Chen Zhu 

Computer Network Information Center, Chinese Academy of Sciences Beijing, China zhuhengshu@gmail.com 

University of Science and Technology of China Hefei, China zc3930155@gmail.com 

## **Abstract** 

fine-tuning process. Furthermore, we design a novel iterative optimization strategy that dynamically optimizes the query generator for producing more informative queries, thereby enhancing the efficacy of the entire framework. Finally, extensive experiments conducted on a series of publicly available retrieval benchmark datasets have demonstrated the effectiveness of the proposed iGFT. 

Document retrieval, designed to recall query-relevant documents from expansive collections, is essential for information-seeking tasks, such as web search and open-domain question-answering. Advances in representation learning and pretrained language models (PLMs) have driven a paradigm shift from traditional sparse retrieval methods to more effective dense retrieval approaches, forging enhanced semantic connections between queries and documents and establishing new performance benchmarks. However, reliance on extensive annotated document-query pairs limits their competitiveness in low-resource scenarios. Recent research efforts employing the few-shot capabilities of large language models (LLMs) and prompt engineering for synthetic data generation have emerged as a promising solution. Nonetheless, these approaches are hindered by the generation of lower-quality data within the conventional dense retrieval training process. To this end, in this paper, we introduce **iGFT** , a framework aimed at enhancing low-resource dense retrieval by integrating a three-phase process— **G** eneration, **F** iltering, and **T** uning—coupled with an **i** terative optimization strategy. Specifically, we first employ supervised fine-tuning on limited ground truth data, enabling an LLM to function as the generator capable of producing potential queries from given documents. Subsequently, we present a multi-stage filtering module to minimize noise in the generated data while retaining samples poised to significantly improve the dense retrieval model’s performance in the follow-up 

## **CCS Concepts** 

• **Information systems** → **Information retrieval** ; • **Computing methodologies** → _Natural language generation_ . 

## **Keywords** 

Dense retrieval; query generation; large language model 

## **ACM Reference Format:** 

Zhenyu Tong, Chuan Qin, Chuyu Fang, Kaichun Yao, Xi Chen, Jingshuai Zhang, Chen Zhu, and Hengshu Zhu. 2025. From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation. In _Proceedings of the 31st ACM SIGKDD Conference on Knowledge Discovery and Data Mining V.1 (KDD ’25), August 3–7, 2025, Toronto, ON, Canada._ ACM, New York, NY, USA, 12 pages. https://doi.org/10.1145/3690624.3709225 

## **1 Introduction** 

Document retrieval has played a significant role within modern information-seeking systems, aiming to identify the most relevant documents from vast corpora in response to user queries [12, 38, 58]. This foundational process underpins a wide range of applications, from established search engines [25] to the latest retrievalaugmented generation (RAG) frameworks [28]. 

∗Both are co-first authors and contribute equally to this work. †Corresponding author 

The field of document retrieval has a rich research history, with traditional approaches predominantly utilizing sparse retrievers, such as TF-IDF and BM25 [43], to match queries and documents through lexical overlap. With the advancement of deep learning, 

This work is licensed under a Creative Commons 4.0 International License. _KDD ’25, August 3–7, 2025, Toronto, ON, Canada_ 

© 2025 Copyright held by the owner/author(s). ACM ISBN 979-8-4007-1245-6/25/08 https://doi.org/10.1145/3690624.3709225 

1373 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Zhenyu Tong et al. 

**==> picture [242 x 71] intentionally omitted <==**

**----- Start of picture text -----**<br>
0.30 0.30<br>ColBERT<br>0.25 0.25<br>BM25<br>0.20 0.20<br>0.15 0.15<br>0.10 0.10 ColBERT + QG<br>ColBERT + QG + Denoisy<br>0.05 0.05 iGFT<br>0.00 0.00<br>3000 2000 1000 500 486 250 100 50 10 250 500 750 1000 1250 1500 1750<br>NDCG@10<br>**----- End of picture text -----**<br>


**Figure 1: Left: Declining performance of ColBERT on the FiQA dataset with reducing training data (hollow circle indicates training set used in the SPTAR [37] experimental setup. Right: Impact of fine-tuning the ColBERT model (pretrained using the same training set of SPTAR) with synthetic data generated by LLM-based query generator (QG), QG enhanced with data denoising, and our proposed iGFT across various augmented data volumes.** 

recent methods leveraging a dual-encoder architecture have transformed document retrieval by embedding queries and documents into low-dimensional dense vectors for relevance calculation, marking the emergence of dense retrieval [17, 58]. Due to their profound capability to capture intrinsic semantics, pretrained language models (PLMs) like BERT [9, 23] have emerged as the de-facto implementation for encoders in dense retrieval, consequently redefining performance benchmarks in the field [24]. 

Despite its superior performance over sparse retrieval methods across a broad range of benchmark datasets, dense retrieval heavily relies on a wealth of annotated document-query pairs for effective training and often exhibits poor generalization across domains [49]. This dependency is especially pronounced in low-resource scenarios, where the scarcity of annotated data and the labor-intensive process of collecting well-labeled document-query pairs [41] exacerbate the challenge of improving dense retrieval performance. In response, several researchers have begun constructing pseudo document-query pairs and leveraging contrastive learning techniques to train dense retrieval models, aiming to overcome this obstacle [26]. Recently, large language models (LLMs), including ChatGPT and GPT-4, have demonstrated remarkable capabilities in language understanding, generation, and few-shot learning across various NLP tasks [5, 6, 20]. This advancement introduces a data augmentation perspective for researchers to boost the performance of low-resource dense retrieval by generating potential queries from given documents [4, 19, 37, 44]. For instance, InPars capitalizes on GPT-3’s in context learning to generate queries for unlabeled documents [4], while SPTAR employs soft prompt tuning to optimize prompts based on limited ground truth data [37]. 

However, employing LLMs as query generators to enhance dense retrieval performance still presents several technical challenges. (1) _How can LLMs be enabled to generate high-quality queries?_ Current methods, such as InPars [4], InPars-v2 [19], and PROMPTAGATOR [8], primarily rely on prompt engineering to guide LLMs in generating queries, using a small set of positive document-query pairs as examples. These approaches depend heavily on the prompt quality and the LLMs’ few-shot learning capabilities, which often result in inconsistent query quality, thereby compromising the effectiveness of subsequent dense retrieval model training. Furthermore, these methods overlook the potential benefits of enhancing the 

LLM-based query generator by fine-tuning LLMs with annotated document-query pairs. (2) _How can generated queries be filtered to improve the performance of dense retrieval models?_ Since LLMs do not always generate high-quality queries, incorporating a data filtering module before training dense retrieval models becomes essential. Previous studies have typically relied on using the generation probability of queries [4] to weed out low-quality data. However, these methods overlook a critical perspective: the identification and selection of the most informative document-query pairs for improving retrieval effectiveness. (3) _How can the generator be optimized to more consistently produce high-quality document-query pairs?_ Although LLM-based generators can continuously generate new data, it is important to recognize that not all generated data contributes positively to the performance of dense retrieval models. As illustrated in Figure 1, the marginal utility of data from a static generator in enhancing retrieval model performance diminishes throughout the training process. Therefore, continuously optimizing generators to more reliably produce high-quality synthetic data, particularly to improve the performance of dense retrieval models, has become a critical challenge. 

To address the above challenges, in this paper, we introduce a novel framework named **iGFT** , designed to enhance dense retrieval through a three-phase, **i** teratively optimized process— **G** eneration, **F** iltering, and **T** uning. Specifically, we begin by leveraging supervised fine-tuning on limited ground truth data, enabling an LLM to serve as a generator capable of producing potential queries from given documents. Following this, we introduce a multi-stage filtering module designed to reduce noise in the generated data while preserving the most informative samples that can significantly enhance the performance of the dense retrieval model during subsequent fine-tuning. Additionally, we design a novel iterative optimization strategy aimed at augmenting the dense retrieval model’s training efficacy. In particular, we present a difficulty-guided reinforcement learning method, dynamically adapting the query generator to produce more informative synthetic data at each iteration. Finally, extensive experiments conducted on several publicly available retrieval benchmark datasets have demonstrated the effectiveness of the proposed framework. 

## **2 Related Works** 

## **2.1 Dense Retrieval** 

Compared with traditional bag-of-words-based sparse retrieval models [1, 43, 56], neural network-based dense retrieval [22, 24, 39] has the potential to capture deeper semantic information. Early explorations in dense retrieval focused on directly capturing latent semantic characteristics for matching through neural network training [13, 14]. Recently, the advent of pretrained models has significantly enhanced the language understanding ability of the model. A notable example is DPR [22] which employs a BERT-based encoder to independently encode queries and documents, calculating relevance via dot product similarity. Furthermore, MVR [57] introduced the strategy of inserting multiple tokens at the beginning of the text to obtain diverse representations. For more fine-grained vector interaction, ColBERT [24] innovatively generated independent vector representations for each word in queries and documents. In addition, 

1374 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation 

several studies have proposed learning phrase-level representations of queries when retrieving phrase-based answers [46, 47]. 

Research has also explored effective negative sampling methods for training retrieval models. For instance, _Xiong et al._ employed the retrieval model trained in the preceding iteration to identify new negative instances for the subsequent training iteration [54]. Additionally, RocketQA [39] enhanced dense retrieval performance by using knowledge distillation to denoise negative samples. Besides, Contriever [18] employed contrastive learning to achieve unsupervised training in dense retrieval. 

While dense retrieval demonstrates superior performance, prior research has primarily concentrated on learning from existing query labels. In low-resource scenarios, dense retrieval exhibits discernible limitations [59]. To address this issue, we propose a novel framework comprising a three-phase process: Generation, Filtering, and Tuning, aimed at enhancing low-resource dense retrieval. 

**==> picture [242 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Unlabeled documents LLM-QG+DR LLM-QG+DF+DR iGFT<br>Document : Many<br>services charge prices that do not scale linearly with  Query GeneratorLLM-based Query GeneratorLLM-based Adaptive LLM-basedQuery Generator<br>usage. This is be-<br>cause the service  Pseudo Document- Pseudo Document- Pseudo Document-<br>provider has ...  Query Pairs Query Pairs Query Pairs<br>document-query pairsLimited annotated Dense RetrievalModel Data Filtering(           ...) Data FilteringMulti-Stage<br>Document ing the 12 plus : Dur- Document Query Filtered Pseudo Scored, Filtered<br>hours the market  Document- Pseudo Document-<br>was closed news  Encoder Encoder Query Pairs Query Pairs<br>can change inve-<br>stors opinion of ...<br>Query:  What cau- Dense Retrieval Dense Retrieval<br>ses discontinuities  Score Model Model<br>with stock prices<br>**----- End of picture text -----**<br>


**Figure 2: Enhancing dense retrieval with LLM-based query generation: a comparison of paradigms.** 

## **3 Preliminary** 

## **2.2 Data Augmentation for Dense Retrieval** 

Leveraging data augmentation techniques to augment the availability of pseudo data can effectively enhance the robustness of the model [2, 42]. In the field of dense retrieval, several studies relied on handcrafted templates and features to extract more relevant paired data [36, 40]. Additionally, some researchers proposed using extraction to select portions of document content as queries or answers to achieve data enhancement [26, 45]. 

In recent years, researchers have utilized large language models to generate queries for unlabeled corpora, achieving favorable outcomes in information retrieval tasks [4, 8, 11, 33, 34, 44, 52]. InPars utilized prompts with a limited number of examples to generate paragraph-level queries based on GPT-3 [4]. Similarly, TQGen [31] explored query extraction and query generation to create pseudo document-query pairs for augmenting retriever training. In contrast to using the hard prompt for generation, SPTAR [37] introduced soft prompt tuning to optimize the quality of the generated query. Furthermore, to address the inconsistency of generated queries by LLMs, some studies have concentrated on designing various data selection methods to filter out qualified data for training [8, 44]. 

Beyond training a generator using labeled document-query pairs, some researchers have explored the direct generation of pseudo data based on pretrained models in zero-shot scenarios [15, 30, 48]. Additionally, SPAR [7] employed knowledge distillation from sparse retrieval models to train the data generator in zero-shot settings. Without training the data generator, methods like HyDE [10] and CSQE [27] achieved superior zero-shot information retrieval by supplementing queries or documents with generated information. 

However, current LLM-based data generators primarily rely on existing labeled data and powerful pretrained models, lacking the ability to improve autonomously in low-resource scenarios. Moreover, there is a significant deficiency in effective methods for assessing and selecting generated results. In this paper, we propose a multi-stage filtering module designed to minimize noise in the generated data and retain samples most likely to significantly improve the performance of dense retrieval models. Additionally, we introduce a difficulty-guided iterative optimization strategy to continuously enhance the capabilities of data generators. 

Given a large corpus D = { _𝑑𝑖_ } _𝑖[𝑁]_ =1[composed of] _[ 𝑁]_[documents, and] a natural language query _𝑞_ , the objective of document retrieval is to learn a model R capable of returning a ranked list of the _𝑛_ most relevant documents D _[𝑞]_ = [ _𝑑_ 1 _[𝑞][,𝑑]_ 2 _[𝑞][, ...,𝑑] 𝑛[𝑞]_[]][for the query] _[ 𝑞]_[.] Unlike traditional sparse retrieval methods like BM25, which depend on lexical matching, dense retrieval models employ two learnable functions that map queries and documents to dense vectors. Formally, let _𝐸𝑄_ (·) denote the query encoder, which produces a representation _𝐸𝑄_ ( _𝑞_ ) ∈ R _[𝑘]_[1] for each query _𝑞_ . Similarly, the document encoder _𝐸𝐷_ (·) is defined to map a document _𝑑_ to its representation _𝐸𝐷_ ( _𝑑_ ) ∈ R _[𝑘]_[2] . Along this line, the dense retrieval model R can be denoted by 

**==> picture [182 x 11] intentionally omitted <==**

where _𝜃_ denotes the parameters of R and the similarity measurement function _𝑓𝑠𝑖𝑚_ (·) can be implemented using an inner product, a multilayer perceptron network (MLP), or other neural network architectures. Typically, the representation dimensions of documents and queries are identical, i.e., _𝑘_ 1 = _𝑘_ 2. However, this is not always the case. For instance, in ColBERT [24], a well-known dense retrieval model, queries and documents are represented as _𝐸𝑄_ ( _𝑞_ ) ∈ R[|] _[𝑞]_[|×] _[𝑘]_ and _𝐸𝐷_ ( _𝑑_ ) ∈ R[|] _[𝑑]_[|×] _[𝑘]_ , respectively, where _𝑘_ represents the token representation dimension. Subsequently, the relevance score is calculated as follows, 

**==> picture [194 x 29] intentionally omitted <==**

where | _𝑞_ | and | _𝑑_ | denote the number of tokens in _𝑞_ and _𝑑_ , respectively. _𝐸𝑄_ ( _𝑞_ ) _𝑖_ and _𝐸𝐷_ ( _𝑑_ ) _𝑗_ correspond to the embedding vectors for the _𝑖_ -th token in _𝑞_ and the _𝑗_ -th token in _𝑑_ , respectively. 

As mentioned before, dense retrieval predominantly employs a supervised training setting. Given a training set T _𝑡𝑟𝑎𝑖𝑛_ , where each ( _𝑞,𝑑_ ) ∈T _𝑡𝑟𝑎𝑖𝑛_ represents a relevant document-query pair, the optimization of the dense retrieval model R( _𝑞,𝑑_ ; _𝜃_ ) can be formalized as: 

**==> picture [205 x 17] intentionally omitted <==**

1375 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Zhenyu Tong et al. 

where T[′] _𝑡𝑟𝑎𝑖𝑛_[is constructed based on the training set][ T] _[𝑡𝑟𝑎𝑖𝑛]_[. Specif-] ically, ∀( _𝑞,𝑑_[+] _,𝑑_[−] ) ∈T _𝑡𝑟𝑎𝑖𝑛_[′][,] _[ 𝑑]_[+][denotes a positive (relevant) docu-] ment, i.e., ( _𝑞,𝑑_[+] ) ∈T _𝑡𝑟𝑎𝑖𝑛_ , and _𝑑_[−] represents a sampled negative (irrelevant) document, i.e., _𝑑_[−] ∈D _,_ ( _𝑞,𝑑_[−] ) ∉ T _𝑡𝑟𝑎𝑖𝑛_ . The objective function L is crucial for model optimization, with the contrastive objective being a prevalent choice. Formally, this is defined as 

**==> picture [234 x 26] intentionally omitted <==**

In practice, for each query _𝑞_ , we sample _𝑙_ documents as negative examples to efficiently train the dense retrieval model R, and we use _𝑑 𝑗_[−][to denote the] _[𝑗]_[-th negative documents. Upon completing] the training of R, nearest neighbor search tools such as FAISS [21] can be employed to retrieve the top- _𝑛_ most relevant documents for any given query _𝑞_ with sublinear complexity. 

As highlighted in the introduction, collecting a sufficient number of document-query pairs for training in low-resource scenarios can be challenging, leading to suboptimal retrieval performance. Moreover, most retrieval datasets contain a vast number of unlabeled documents (i.e., documents not appearing in T _𝑡𝑟𝑎𝑖𝑛_ ). While dense retrieval models perform well on annotated documents, they may struggle to effectively recall these unlabeled ones. To address this issue, our study introduces a three-phase approach—Generation, Filtering, and Tuning—integrated with an iterative optimization strategy, which significantly enhances the performance of dense retrieval models in low-resource scenarios. 

## **4 Methodology** 

In this section, we elaborate on the details of the iGFT framework, incorporating three processes: LLM-based query generation, multistage data filtering, and fine-tuning of the dense retrieval model. Additionally, we introduce a dynamic iterative optimization strategy, specifically designed to refine the query generator. The framework overview is depicted in Figure 3. 

## **4.1 LLM-based Query Generation** 

To enhance the performance of dense retrieval model R in lowresource settings, recent studies [4, 44] have leveraged LLMs to generate appropriate queries for documents within corpora that lack sufficient annotations. However, the effectiveness of these methods relies heavily on the design of prompts, especially the quality of document-query examples used in in-context learning, which do not guarantee the consistent generation of high-quality queries across varied corpora. 

To address this challenge, we utilize Llama-2 [51], an open-source LLM, and apply Supervised Fine-Tuning (SFT) on a constrained dataset of annotated document-query pairs, T _𝑡𝑟𝑎𝑖𝑛_ , to develop a query generation model, G. Specifically, as illustrated in the top left corner of Figure 3, we first construct the SFT data based on T _𝑡𝑟𝑎𝑖𝑛_ . Subsequently, given the substantial computational resources required for full-parameter fine-tuning, we opt for LoRA [16], a parameter-efficient fine-tuning technique, which retains the core parameters of the LLM unchanged and focuses on training rank decomposition matrices specific to each layer of the Transformer architecture. Along this line, the learning objective for the generator 

is defined as follows: 

**==> picture [214 x 31] intentionally omitted <==**

where Θ _𝐿_ represents the LoRA parameters, we exclusively update these LoRA parameters throughout the training process. The notation _𝑞𝑡_ refers to the _𝑡_ -th token in _𝑞_ , and _𝑞<𝑡_ represents the sequence of tokens { _𝑞_ 1 _,𝑞_ 1 _, ...,𝑞𝑡_ −1}. Finally, the fine-tuned LLM G empowers us to generate queries for any given document, as represented by: 

**==> picture [155 x 10] intentionally omitted <==**

This capability facilitates the creation of a synthetic dataset T _𝐺_ to enhance the performance of dense retrieval model R. 

## **4.2 Multi-Stage Data Filtering** 

Despite the generator G, trained on annotated data, is capable of generating high-quality queries for constructing synthetic dataset T _𝐺_ , as highlighted in our introduction, T _𝐺_ unavoidably includes noise that may undermine the training efficacy of the dense retrieval model R. To mitigate this concern, we develop a multi-stage data filtering module that focuses on both the quality of pseudo data and its utility in training R. 

_4.2.1 Filtering with Sparse Retrieval._ Initially, we employ BM25 for filtering the T _𝐺_ . Specifically, for each pseudo document-query pair ( _𝑞𝑖,𝑑 𝑗_ ) ∈T _𝐺_ , we randomly select other _𝑚_ 1 documents D _𝑚_ = { _𝑑𝑘[𝑚]_[}] _[𝑚] 𝑘_ =[1] 1[from][the][corpus][D][as][negative][samples.][This][process] forms a candidate set D _𝑚_[′] = { _𝑑 𝑗_ } ∪D _𝑚_ . In our experiments, _𝑚_ 1 is set to 100. Subsequently, for each _𝑑𝑘_ ∈D _𝑚_[′] , ( _𝑞𝑖,𝑑𝑘_ ) is scored using BM25, denoted as BM25( _𝑞𝑖,𝑑𝑘_ ). If BM25( _𝑞𝑖,𝑑 𝑗_ ) yields the highest score, we retain this pseudo-pair in T _𝐺_ ; otherwise, it is excluded. By applying this criterion across T _𝐺_ , we refine it to T _𝐺_[1][.] 

_4.2.2 Filtering with Dense Retrieval._ Following the initial filtration with BM25, which eliminates some lower-quality document-query pairs, we recognize the limitation of BM25 to primarily lexical-level relevance. Consequently, we further employ a pretrained dense retrieval model R _𝑝𝑟𝑒_ for a second round of filtering. This subsequent step seeks to capture nuanced semantic relationships that BM25 might miss, ensuring a more discerning selection of training instances for our dense retrieval model R. 

Specifically, we first leverage the annotated data T _𝑡𝑟𝑎𝑖𝑛_ to train the pretrained dense retrieval model R _𝑝𝑟𝑒_ . In our experiments, R _𝑝𝑟𝑒_ is based on the Colbert model. Subsequently, mirroring the process of filtering with BM25, we construct corresponding negative samples for each query-document pair ( _𝑞𝑖,𝑑 𝑗_ ) ∈T _𝐺_[1][. Only those] pairs ranked as top-1 based on the score R _𝑝𝑟𝑒_ ( _𝑞𝑖,𝑑 𝑗_ ) are selected to form the filtered set T _𝐺_[2][. Additionally, to further enhance the] quality of T _𝐺_[2][, we sort all query-document pairs in descending order] based on the scores {R _𝑝𝑟𝑒_ ( _𝑞𝑖,𝑑 𝑗_ ) _,_ ∀( _𝑞𝑖,𝑑 𝑗_ ) ∈T _𝐺_[2][}][. We retain only] the top _𝑚_ 2% of these pairs to form the new filtered dataset T _𝐺_[3][. In] our experiments, through parameter analysis, we retain 40% of T _𝐺_[2] to ensure optimal performance. 

_4.2.3 Filtering with Loss Prediction Module._ In the previous stages, our focus was on removing the noisy data. Indeed, selecting samples that offer more informative value to the dense retrieval model R 

1376 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation 

**==> picture [506 x 170] intentionally omitted <==**

**Figure 3: The overview architecture of our proposed iGFT framework.** 

can significantly enhance the training process’s effectiveness. To realize this improvement, we introduce a loss prediction module aimed at creating the final filtered dataset. 

Specifically, given the filtered data T _𝐺_[3][, to train dense retrieval] model R more effectively, intuitively, we can select instances from T[3] _𝐺_[that exhibiting higher loss values:] 

**==> picture [213 x 13] intentionally omitted <==**

where ( _𝑞𝑖,𝑑 𝑗_ ) ∈T _𝐺_[3][and][L(R] _[,𝑞][𝑖][,𝑑][𝑗][,𝑑]_[−][)][can][be][determined][by] Equation 4. However, due to the high computational cost of sampling negative instances _𝑑_[−] , we employ a muti-head cross-attention mechanism to estimate Equation 7. Formally, we have _ℎ_ 1 = _𝑀𝑢𝑙𝑡𝑖𝐻𝑒𝑎𝑑𝐴𝑡𝑡_[�] _𝐸𝑄_ ( _𝑞𝑖_ ) _, 𝐸𝐷_ ( _𝑑 𝑗_ ) _, 𝐸𝐷_ ( _𝑑 𝑗_ )[�] _,_ (8) _ℎ_ 2 = _𝑓_ ( _ℎ_ 1) _, 𝑦𝑞𝑖,𝑑 𝑗_ = _𝑚𝑒𝑎𝑛_  𝑝𝑜𝑜𝑙𝑖𝑛𝑔_ ( _ℎ_ 2) _,_ 

where _ℎ_ 1 ∈ R[|] _[𝑞][𝑖]_[|×] _[𝑘]_[3] , _ℎ_ 2 ∈ R[|] _[𝑞][𝑖]_[|×][1] , _𝑀𝑢𝑙𝑡𝑖𝐻𝑒𝑎𝑑𝐴𝑡𝑡_ (· _,_ · _,_ ·) represents the multi-head attention network, _𝑓_ (·) is a learnable multilayer perceptron network, and _𝐸𝑄_ and _𝐸𝐷_ denote the document and query encoders of R, respectively. By uniformly sampling a set of ( _𝑞𝑖,𝑑 𝑗_ ) ∈T _𝐺_[3][, denoted as][ T] _𝐺_[ 3][′][, we can estimate the parameters in] the loss prediction module by minimizing the following loss: 

**==> picture [198 x 29] intentionally omitted <==**

Subsequently, we calculate and sort all _𝑦𝑞𝑖,𝑑 𝑗_ , where ( _𝑞𝑖,𝑑 𝑗_ ) ∈T _𝐺_[3][,] in descending order. We retain the top _𝑚_ 3 of these pairs, which we identify as the most informative instances for optimizing the dense retrieval model, to compose the final filtered dataset T _𝐺_[4][.] 

## **4.3 Tuning and Iterative Optimization** 

_4.3.1 Fine-Tuning Dense Retrieval Model._ As introduced in Section 3, the dense retrieval model can be trained using Equations 3 and 4. Given the annotated training dataset T _𝑡𝑟𝑎𝑖𝑛_ , we initially train a dense retrieval R _𝑖𝑛𝑖𝑡_ . Subsequently, leveraging the synthetic data T[4] _𝐺_[generated by our query generation model][ G][ and refined through] a multi-stage filtering process, we further fine-tune R _𝑖𝑛𝑖𝑡_ to produce our enhanced dense retrieval model R. 

_4.3.2 Iterative Optimization Strategy._ While G can continuously produce new data for training the dense retrieval model R, there is no assurance that G will consistently generate high-quality and informative data throughout the training process of R. Figure 1 also illustrates that even filtering out low-quality training data, R rapidly reaches a performance plateau. To address this challenge, we developed an iterative optimization strategy that dynamically updates our generator G. This strategy enables G to adaptively produce queries that significantly enhance the iterative updates of R, ensuring continuous improvement in retrieval performance. 

To clarify our methodology, we begin with the following definitions: R _𝑖𝑛𝑖𝑡_ represents the initial dense retrieval model trained on T _𝑡𝑟𝑎𝑖𝑛_ ; G1, derived from training on the SFT data, is identified as the first iteration of the updated generator; T _𝐺,_[4] 1[denotes the syn-] thetic data after multi-stage filtering; and R1, fine-tuned using T _𝐺,_[4] 1 from R _𝑖𝑛𝑖𝑡_ , is recognized as the first iteration of the updated dense retrieval model. Along this line, we denote the generator, synthetic data, and retriever updated in the _𝑡_ -th iteration through our iterative optimization strategy as G _𝑡_ , T _𝐺,𝑡_[4][, and][ R] _[𝑡]_[, respectively. Indeed,] our primary motivation for iteratively updating the generator is to enable the synthetic data T _𝐺,𝑡_[4][to include more][(] _[𝑞][𝑖][,𝑑][𝑗]_[)][pairs that] challenge R _𝑡_ −1, specifically those with a high L(R _𝑡_ −1 _,𝑞𝑖,𝑑 𝑗_ ). To this end, we develop a reward model and employ proximal policy optimization (PPO)-based reinforcement learning (RL) to enhance the query generator. 

**Reward Model Learning Phase:** The objective of the reward model V _𝑡_ at _𝑡_ -th iteration is to assign scores to any ( _𝑞𝑖,𝑑 𝑗_ ), ensuring that the pairs with a higher L(R _𝑡_ −1 _,𝑞𝑖,𝑑 𝑗_ ) achieve higher scores. The architecture of V _𝑡_ is similar to that of the generator G, but replaces the final output layer with a linear prediction head that outputs scalar reward values. Additionally, the reward model is initialized with the parameters of the generator G. We leverage T _𝐺,𝑡_[4] −1[to][construct][a][dataset][comprised][of][paired][comparisons] between two responses from G _𝑡_ −1 and employ a pairwise ranking loss to train V _𝑡_ in the following manner: 

**==> picture [230 x 12] intentionally omitted <==**

1377 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Zhenyu Tong et al. 

_𝜎_ denotes the activation sigmoid function. T _𝑟𝑚,𝑡_ = {( _𝑞𝑖,𝑞𝑘,𝑑 𝑗_ )}, where ( _𝑞𝑖,𝑑 𝑗_ ) ∈T _𝐺,𝑡_[4] −1[,][(] _[𝑞][𝑘][,𝑑][𝑗]_[)][∈T] _𝐺,𝑡_[ 4] −1[,][and] _[ 𝑦][𝑞] 𝑖[,𝑑] 𝑗[>][𝑦][𝑞] 𝑘[,𝑑] 𝑗_[.] _𝑦𝑞𝑖,𝑑 𝑗_ is calculated by the loss prediction module in Section 4.2.3. **PPO-based RL Fine-Tuning Phase:** We first use query generator G _𝑡_ −1 and reward model V _𝑡_ to initialize the actor model G _[𝑎]_ and critic model V _[𝑐]_ . During the RL fine-tuning, we sample the documentage G _[𝑎]_ to generate query, denoted as _𝑑 𝑗_ ∈D _𝐺,𝑡_[4] −1[=][{∀] _[𝑑][𝑗][,𝑠.𝑡.]_[∃(] _𝑞[𝑞]_ � _𝑖[𝑖]_ . Then, the reward can be _[,𝑑][𝑗]_[)][∈T] _𝐺,𝑡_[ 4] −1[}][and lever-] formulated as follows: 

**==> picture [231 x 13] intentionally omitted <==**

where _𝜆_ is the coefficient for the KL-divergence term that is used to limit the range of changes in the policy during each update [35]. Meanwhile, the advantage value is the difference between reward _𝑟_ and the value of the input _𝑑 𝑗_ estimated by the critic model as: _𝑎𝑞_ � _𝑖,𝑘 ,𝑑 𝑗_ = _𝑟𝑞_ � _𝑖,𝑑 𝑗_[−V] _[𝑐]_[(] _[𝑑][𝑗][,]_[ �] _[𝑞] 𝑖,<𝑘_ +1[)][, where][ �] _[𝑞] 𝑖,𝑘_[denotes the] _[ 𝑘]_[-th token] in � _𝑞𝑖_ . Then, we can optimize the actor model G _[𝑎]_ based on: 

**==> picture [234 x 65] intentionally omitted <==**

where function clip( _𝑥,_ 1 − _𝜀,_ 1 + _𝜀_ ) limits the value of _𝑥_ between (1 − _𝜀,_ 1 + _𝜀_ ). Finally, the critic model V _[𝑐]_ is optimized with loss function: L _𝑐_ = E( _𝑞_ � _𝑖,𝑑 𝑗_ ) ( _𝑟𝑞_ � _𝑖,𝑑 𝑗_[−V] _[𝑐]_[(] _[𝑑][𝑗][,]_[ �] _[𝑞][𝑖]_[))][2][.] **Difficulty-Guided Learning Strategy:** By leveraging the reward model and PPO-based RL algorithm, we can update the query generator from G _𝑡_ −1 to G _𝑡_ . Additionally, to improve the effectiveness of the RL algorithm, we introduce a difficulty-guided learning strategy, so that G _𝑡_ can exhibit better performance. 

Considering the varying capabilities of generator G _𝑡_ −1 to produce informative queries for different documents, the difficulty faced by the RL process to further enhance G _𝑡_ −1 to generate more informative queries varies across documents. Specifically, given the synthetic data T _𝐺,𝑡_[4] −1[, we estimate the difficulty of document] _[ 𝑑][𝑗]_[for] PPO by 

**==> picture [234 x 31] intentionally omitted <==**

## **5 Experiments** 

## **5.1 Experimental Setting** 

_5.1.1 Datasets._ To validate the effectiveness of the proposed iGFT in low-resource settings, we selected a series of datasets from the BEIR benchmark [50] to construct our experiments. Specifically, we first selected datasets from BEIR that include document-query training data, such as FiQA, MSMARCO, and NQ. We followed the experimental setup of SPTAR [37], using only 500 document-query pairs as the training set to simulate the low-resource conditions. In addition to the standard low-resource scenarios mentioned above, we followed the BEIR benchmark to validate the model’s zero-shot performance. Detailed descriptions of each dataset in BEIR can be found in Appendix A.1. 

_5.1.2 Evaluation Metrics._ The evaluation of document retrieval performance relies on assessing the ranking quality, measured through metrics including Mean Average Precision (MAP) [29], Recall [29], Normalized Discounted Cumulated Gains (NDCG) [29], and Mean Reciprocal Rank (MRR) [29]. In this paper, we report the top-10 retrieval performance employing the above metrics—specifically, MAP@10, Recall@10, NDCG@10, and MRR@10. 

_5.1.3 Implementation Details._ In the query generation phase of iGFT, we utilized Llama-2 as the generative model. In the SFT stage, the AdamW optimizer with a learning rate of 5 _𝑒_ − 5 was utilized. The training spanned across 3 epochs, with a batch size set to 4, incorporating the LoRA [16] technique to achieve parameter efficiency. Please note that in zero-shot scenarios, such as Arguana, due to the lack of document-query training data, we skipped the SFT process for the LLM-based query generation model and instead used the original Llama-2 model as G. Meanwhile, during each iteration of the optimization process, we set the learning rate as 1 _𝑒_ − 7 to train the reward model and update the generator. The batch size during this phase was established at 8, and the _𝜆_ in the PPO-based RL fine-tuning stage was fixed at 0 _._ 95. In the process of filtering with sparse retrieval, we employed the BM25 algorithm, adjusting the parameters to _𝑏_ = 0 _._ 75 and _𝑘_ = 1 _._ 5, setting _𝑚_ 1 = 100 to sieve through the synthetic data for quality. Concurrently, for the dense retrieval-based filtering phase, we selected the highestscoring _𝑚_ 2 = 40% of T _𝐺_[1][as determined by][ R] _[𝑝𝑟𝑒]_[, designating these] as meeting the filter’s cut-off. Furthermore, within the process of filtering with the loss prediction module, we set _𝑚_ 3 = 40% to obtain the final filtered data T _𝐺_[4][. In aligning with the experimental setup] of SPTAR, the ColBERT in iGFT was trained using a batch size of 32 and adhered to a learning rate of 2 _𝑒_ − 5. 

## **5.2 Performance in the Low-Resource Setting** 

where R _𝑡_ −1 ( _𝑞𝑖,𝑑 𝑗_ ) represents the relevance score of ( _𝑞𝑖,𝑑 𝑗_ ) calculated by the ( _𝑡_ − 1)-th iteration dense retrieval model and _𝑟𝑎𝑛𝑘𝑞𝑖,𝑑 𝑗_ denotes the ranking of _𝑑 𝑗_ within all the documents in the corpus D, determined by descending order of R _𝑡_ −1 ( _𝑞𝑖,𝑑 𝑗_ ). Indeed, diff( _𝑑 𝑗_ ) effectively estimates the current generator capacity to generate informative for _𝑑 𝑗_ . Thus, a higher diff( _𝑑 𝑗_ ) suggests that the generator G _𝑡_ −1 faces greater challenges in further improvement. Along this line, during the PPO-based RL fine-tuning process, instead of using random data shuffling on D _𝐺,𝑡_[4] −1[, we sequence the data based on] the difficulty level diff from lower to higher for all the _𝑑 𝑗_ ∈D _𝐺,𝑡_[4] −1[.] 

_5.2.1 Baseline Approaches._ To evaluate the effectiveness of iGFT in the low-resource setting, we meticulously selected a range of competitive baseline models for comparison. These include: (1) Sparse retrieval methods: BM25 [43] and its variant BM25-tuned [3], employing a Lucene index for enhanced retrieval efficiency; (2) Dense retrieval model via supervised learning with low resource data: ColBERT [24]; and (3) Dense retrieval model trained via unsupervised learning: ICT [26], MSS [45], and Contriever [18]. Moreover, we incorporated cutting-edge LLM-based query generation methods that aim to enhance dense retrieval models, including Doc2Query [34], 

1378 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation 

**Table 1: The performances in the low-resource setting of our model and baselines. The order of the top 10 predictions was considered in NDCG, MAP, Recall, and MRR. The best results are in bold, and the second-best results are in underscored.** 

||**Datasets**|**Datasets**|**Datasets**|**Datasets**|**Datasets**|**Datasets**|||||**FiQA**|**FiQA**|**FiQA**|**FiQA**|**FiQA**|**FiQA**||||||||**MSMARCO**|**MSMARCO**|**MSMARCO**|**MSMARCO**|**MSMARCO**|**MSMARCO**|**MSMARCO**|||||||**NQ**|**NQ**|**NQ**|**NQ**|**NQ**|**NQ**|**MRR**<br>0.0800<br>0.2634<br>0.2225<br>0.2077<br>0.2047<br>0.2155<br>0.2216<br>0.2529<br>0.2264<br>0.2134<br>0.2170<br>0.2701<br>0.3515<br>0.2607<br>0.2460<br>0.2567<br>**0.4222**<br> +20.11%|**MRR**<br>0.0800<br>0.2634<br>0.2225<br>0.2077<br>0.2047<br>0.2155<br>0.2216<br>0.2529<br>0.2264<br>0.2134<br>0.2170<br>0.2701<br>0.3515<br>0.2607<br>0.2460<br>0.2567<br>**0.4222**<br> +20.11%|**MRR**<br>0.0800<br>0.2634<br>0.2225<br>0.2077<br>0.2047<br>0.2155<br>0.2216<br>0.2529<br>0.2264<br>0.2134<br>0.2170<br>0.2701<br>0.3515<br>0.2607<br>0.2460<br>0.2567<br>**0.4222**<br> +20.11%|**MRR**<br>0.0800<br>0.2634<br>0.2225<br>0.2077<br>0.2047<br>0.2155<br>0.2216<br>0.2529<br>0.2264<br>0.2134<br>0.2170<br>0.2701<br>0.3515<br>0.2607<br>0.2460<br>0.2567<br>**0.4222**<br> +20.11%|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
||**Metrics**||||||**NDCG**<br>||||**MAP**||**Recall**||||**MRR**||||**NDCG**|||**MAP**|||**Recall**||||**MRR**|||**NDCG**|||**MAP**|||**Recall**|||||||
||BM25<br>BM25-tuned||||||0.1113<br><br>0.2361<br>||||0.0697<br>0.1784||0.1913<br>0.2951||||0.1103<br>0.2889||||0.0343<br>0.2084|||0.0151<br>0.1712|||0.1009<br>0.3787||||0.0158<br>0.1733|||0.0789<br>0.2855|||0.0721<br>0.2454|||0.0914<br>0.4555|||||||
||ColBERT||||||0.1149<br>||||0.0820||0.1547||||0.1675||||0.0786|||0.0619|||0.1301||||0.0639|||0.2560|||0.2029|||0.4015|||||||
||ICT<br>MSS<br>Contriever||||||0.1955<br><br>0.1660<br><br>0.2536<br>||||0.1515<br>0.1219<br>0.2002||0.2278<br>0.2167<br>0.2994||||0.2585<br>0.2067<br>0.3259||||0.1389<br>0.1465<br>0.2056|||0.1095<br>0.1180<br>0.1578|||0.2112<br>0.2344<br>0.3568||||0.0980<br>0.1212<br>0.1611|||0.2601<br>0.2414<br>0.2538|||0.1917<br>0.1892<br>0.1970|||0.4012<br>0.3875<br>0.4128|||||||
||Doc2Query<br>Doc2Query--<br>DocT5Query<br>GPL<br>UDAPDR<br>InPars<br>InPars-v2<br>SPTAR<br>Promptagator<br>ChatGPT||||||0.1884<br><br>0.2173<br><br>0.2046<br><br>0.2019<br><br>0.1732<br><br>0.2574<br><br>0.2714<br><br>0.2688<br><br>0.2351<br><br>0.2697<br>||||0.1392<br>0.1676<br>0.1586<br>0.1513<br>0.1333<br>0.2024<br>0.2158<br>0.2103<br>0.1752<br>0.2076||0.2362<br>0.2712<br>0.2385<br>0.2335<br>0.2185<br>0.3051<br>0.3283<br>0.3083<br>0.2737<br>0.2512||||0.2327<br>0.2416<br>0.2530<br>0.2431<br>0.2240<br>0.3179<br>0.3565<br>0.3039<br>0.2725<br>0.2507||||0.1827<br>0.2044<br>0.2026<br>0.2009<br>0.2012<br>0.1821<br>0.1890<br>0.2185<br>0.2007<br>0.2131|||0.1503<br>0.1758<br>0.1717<br>0.1751<br>0.1392<br>0.1444<br>0.1532<br>0.1872<br>0.1725<br>0.1828|||0.3671<br>0.3955<br>0.3914<br>0.3917<br>0.2208<br>0.2991<br>0.2999<br>0.3662<br>0.3927<br>0.3987||||0.1702<br>0.1818<br>0.1848<br>0.1837<br>0.1377<br>0.1480<br>0.1566<br>0.1704<br>0.1867<br>0.1974|||0.2648<br>0.2829<br>0.2767<br>0.2641<br>0.2620<br>0.3097<br>0.3412<br>0.3007<br>0.2814<br>0.2977|||0.2060<br>0.2359<br>0.2110<br>0.2017<br>0.2091<br>0.2531<br>0.2963<br>0.2517<br>0.2315<br>0.2417|||0.4673<br>0.4938<br>0.4661<br>0.4721<br>0.4503<br>0.4624<br>0.4892<br>0.4613<br>0.4894<br>0.5023|||||||
||Ours<br>_𝐼𝑚𝑝𝑟𝑜𝑣𝑒._||||||**0.3042**<br><br>+12.09%||||**0.2415**<br>+11.91%||**0.3666**<br> +11.67%||||**0.3731**<br> +4.66%||||**0.2550**<br>+16.70%|||**0.2044**<br> +9.19%|||**0.4108**<br>+3.03%||||**0.2085**<br>+5.62%|||**0.4252**<br>24.62%|||**0.3898**<br>+31.56%|||**0.5796**<br> +15.39%|||||||
||||||||||||||||||||||||||||||||||||||||||||||||
|NDCG@10|1<br>0.20<br>0.25<br>0.30|FiQA||||||FiQA|||||FiQA||||i|i||GFT|w/oSR & DR|||iGF|Tw/oLP||<br>iGFT|||||MSMA||RCO<br>|||MSMARCO||||||MSMARCO||||
||||||||||||||||||||||FiQA||||MS||MARCO||||||||||||||||||||
|||||||AP@10|0.20|||||0.30<br>0.35<br>ecall@10||||||0.30<br>0.35<br>RR@10||||||0.22<br>0.24<br>DCG@10||||||AP@10|0.18<br>0.20<br>|||||0.350<br>0.375<br>0.400<br>ecall@10|||||016<br>0.18<br>0.20<br>RR@10||||||
|||00%<br>80%<br>60%<br>40%<br>20%<br><br>M|||||1<br>0.15|00%<br>80%<br>60%<br>40|||%<br>20%<br>1<br>0.25<br>R||00%<br>80%<br>60%<br>40%||||20%<br>1<br>0.25<br>M|||00%<br>|80%<br>60%<br>40%<br>20|||%<br>1<br>0.20<br>N|00%<br>80%||60%<br>40%<br>20%<br>M||||10<br>0.16<br>|0%<br>80%<br>60||%<br>40%<br>20%<br>1<br>0.325<br>R|||00%<br>80%<br>60%<br>40|||%<br>20%<br>10<br>0.14<br>.<br>M||0%|80%<br>60%<br>40%<br>20||||
|||**Figure 4: Comparison of iGFT, iGFT w/o LP, and iGFT**|||||||||||||||||||||||**w/o SR & DR under various parameter settings.**||||||||||||||||||||||
|NDCG@10|0.26<br>0.28<br>0.30<br>0.32|FiQA||||||FiQA|||||FiQA|||||||iGFTw<br>1<br>iGFTw|||||RDS<br>iGFT|||||||MSMARCO<br>|||||MSMARCO||||||MSMARCO||||
||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||FiQA<br>|||||||||||||||||||||||||||
|||||||0.22<br>0.24<br>AP@10||||||0.325<br>0.350<br>0.375<br>ecall@10||||||0.30<br>0.35<br>RR@10||||||0.24<br>0.26<br>DCG@10||||||018<br>0.20<br>AP@10||||||0.40<br>0.41<br>0.42<br>ecall@10|||||0.20<br>0.22<br>RR@10||||||
|||1<br>2<br>3<br>4<br>5<br>0.20<br>M||||||1<br>2<br>3<br>4<br>5<br>0.300<br>R|||||1<br>2<br>3<br>4<br>5<br>0.25<br>M|||||||1<br>2<br>3<br>4<br>5<br>0.22<br>N|||||1<br>2<br>3<br>4<br>5<br>.<br>M|||||||1<br>2<br>3<br>4<br>5<br>0.38<br>0.39<br>R|||||1<br>2<br>3<br>4<br>5<br>0.18<br>M|||||1|2<br>3<br>4<br>||||



**Figure 5: Comparison of iGFT, iGFT w** G1 **, and iGFT w RDS at different iterations.** 

Doc2Query-- [11], DocT5Query [33], GPL [52], InPars [4], InParsv2 [19], UDAPDR [44], Promptagator [8], and SPTAR [37]. Furthermore, we utilized ChatGPT for the query generation process for comparative analysis. In our experimental setup, we applied both our iGFT and above LLM-based methods to a pre-trained ColBERT, which ensured a fair and direct comparison of performance. 

_5.2.2 Experimental Results._ Table 1 showcases the comparative performance analysis of the proposed iGFT framework against baseline models on the FiQA, MSMARCO, and NQ datasets. We highlighted the best results in boldface and underlined the suboptimal results. According to the results, there are the following 

observations: (1) Our iGPT consistently outperforms all baseline models across every dataset, marking significant advancements. Specifically, compared to the best performances of all baselines across various metrics, our iGFT achieves an average improvement of 17.80%, 17.55%, 10.03%, and 10.13% on the NDCG@10, MAP@10, Recall@10, and MRR@10, respectively, across the three datasets. (2) We can observe that ColBERT, relying on supervised learning, does not outperform all sparse retrieval methods. This indicates that dense retrieval models trained solely on annotated data struggle to effectively handle document retrieval tasks in low-resource settings. (3) The unsupervised dense retrieval approaches, including ICT, MSS, and Contriever, which train models by constructing pseudo 

1379 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Zhenyu Tong et al. 

**Table 2: The performance comparison of our model and baselines on NDCG@10 in the zero-shot setting. InPars-v2*, LaPraDoR*, and Ours* respectively represent the performances after adding a reranker to the corresponding original dense retrieval model.** 

|**Models**|QGen<br>LameR<br>DRAD<br>InPars-v2|Query2Doc<br>HyDE<br>CSQE|SPAR<br>LaPraDoR|Ours|InPars-v2*<br>LaPraDoR*|Ours*|
|---|---|---|---|---|---|---|
|**ArguAna**<br>**DBPedia-Entity**<br>**TREC-Covid**<br>**FiQA**<br>**SciFact**|0.4934<br>0.4021<br>0.4975<br>0.4725<br>0.3281<br>0.3957<br>0.4180<br>0.4192<br>0.6083<br>0.7481<br>0.7372<br>0.7184<br>0.3082<br>0.2580<br>0.3382<br>0.3243<br>0.6429<br>0.7251<br>0.6928<br>0.6825|0.4146<br>0.4662<br>0.4034<br>0.4247<br>0.3682<br>0.4137<br>0.7384<br>0.5933<br>0.7422<br>0.2912<br>0.2768<br>0.2794<br>0.7172<br>0.6916<br>0.6978|0.4591<br>0.5072<br>0.4275<br>0.4189<br>0.7326<br>0.7389<br>0.3258<br>0.3290<br>0.6962<br>0.6882|**0.5105**<br>**0.4624**<br>**0.7712**<br>**0.3628**<br>**0.7430**|0.4690<br>0.5274<br>0.4982<br>0.4904<br>0.8462<br>0.8518<br>0.5092<br>0.4973<br>0.7742<br>0.7523|**0.5883**<br>**0.5123**<br>**0.8794**<br>**0.5202**<br>**0.7962**|



**Table 3: The performances in the fully-supervised setting of our model and ColBERT.** 

|**Datasets**|**FiQA**|**MSMARCO**|**NQ**|
|---|---|---|---|
|**Metrics**|**NDCG**<br>**MAP**<br>**Recall**<br>**MRR**|**NDCG**<br>**MAP**<br>**Recall**<br>**MRR**|**NDCG**<br>**MAP**<br>**Recall**<br>**MRR**|
|ColBERT<br>Ours|0.3312<br>0.2578<br>0.3782<br>0.4193<br>**0.3572**<br>**0.2872**<br>**0.3968**<br>**0.4312**|0.3837<br>0.3381<br>0.5127<br>0.3454<br>**0.4016**<br>**0.3505**<br>**0.5680**<br>**0.3589**|0.5280<br>0.4169<br>0.6591<br>0.4382<br>**0.5412**<br>**0.4557**<br>**0.7094**<br>**0.4862**|



( _𝑞,𝑑_ ) pairs, utilizing strategies that include segment extraction from documents, have effectively enhanced model performance. Contriever, in particular, outperforms sparse retrieval models across a majority of metrics on the FiQA dataset and achieves competitive performance on the MSMARCO. (4) All enhanced dense retrieval approaches leveraging LLM-based query generation, including our iGFT framework, achieve superior performance compared to previous baseline models. This verifies the capability of LLMs to boost dense retrieval in low-resource scenarios through a data augmentation perspective. Furthermore, our approach outperforms these state-of-the-art LLM-based approaches, thereby demonstrating the effectiveness of our iGFT framework. Furthermore, our experimental results on NFCorpus and SciFact also demonstrate that our iGFT can achieve better performance. Due to space constraints, these results are presented in Appendix A.3. 

## **5.3 Analysis of Filtering Strategies** 

To evaluate the impact of different components within our multistage filtering phase, we introduced two variants of our iGFT: (1) **iGFT** _**w/o**_ **LP** , which excludes the loss prediction module for selecting synthetic data that offer more informative value for training the dense retrieval model, as detailed in Section 4.2.3; (2) **iGFT** _**w/o**_ **SR & DR** , which removes the processes described in Sections 4.2.1-4.2.2 for filtering out low-quality data via BM25 and R _𝑝𝑟𝑒_ . 

We reported the performance of our approach and its two variants FiQA and MSMARCO in Figure 4, with the setting of _𝑚_ 2 = _𝑚_ 3 ranging from 100% to 20%. As _𝑚_ 2 and _𝑚_ 3 values increase, the filtered data become more closer to the original synthetic data. Notably, when _𝑚_ 2 = _𝑚_ 3 = 100%, symbolizing a scenario devoid of any filtering processes, BM25 filtering is not implemented. As illustrated in Figure 1, we observed a decline in model performance upon the removal of any component, underscoring the importance of considering both the quality of the generated data and its influence on the dense retrieval model’s training within the filtering process. Furthermore, we determined that a configuration of _𝑚_ 2 = _𝑚_ 3 = 40% yields optimal results. Consequently, we adopted this setting for our iGFT in the experiments. 

## **5.4 Analysis of Iterative Optimization** 

We further investigated the effectiveness of the proposed iterative optimization strategy. Specifically, we introduced two variants of our approach: (1) **iGFT** _**w**_ G1, which maintains a static generator, i.e., G1 (trained on the SFT data), throughout the iterative learning process of iGFT; (2) **iGFT** _**w**_ **RDS** , which adopts a random data shuffle method instead of the proposed difficulty-guided learning strategy for implementing PPO algorithm to update the generator. 

Figure 5 presents the performance of our iGFT and its variants at different iterations. We standardized the quantity of data generated per iteration by G _𝑡_ , ensuring that |G _𝑡_ | remains constant. The x- axis denotes the iteration number, with the generator set to G1 at the first iteration. Results illustrated in Figure 5 reveal that iGFT significantly improves retrieval performance via adaptive updates to the generator throughout the iterative process. Furthermore, the implementation of the proposed difficulty-guided learning strategy in the PPO algorithm substantially elevates iGFT’s performance. Furthermore, the time cost analysis of the iterative optimization is presented in Appendix A.2. 

## **5.5 Performance in the Zero-Shot Setting** 

We selected several competitive baseline models known for their effectiveness in zero-shot scenarios, including (1) query-generation methods: QGen [30], LameR [48] and DRAD [15], which focus on generating domain-specific data using pre-trained models without any training data; (2) query expansion methods: Query2Doc [53], HyDE [10] and CSQE [27], which enhance query content by generating additional information to expand the original query; and (3) knowledge distillation methods: SPAR [7] and LaPraDoR [55]. Additionally, we compared the performance of different models after incorporating a reranker. Specifically, we followed InParsv2 [19], utilizing a pre-trained monoT5-3B model [32] for reranking. 

_5.5.1 Experimental Results._ In Table 2, we present a comparative performance analysis of the proposed iGFT method and baseline models on the ArguAna, DBPedia-Entity, TREC-Covid, FiQA, and SciFact datasets. The experimental results show that our method 

1380 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation 

**Table 4: Case study of query generation based on FiQA dataset.** 

|**Document**_𝑑_**(****_ID:527311)_**|So here’s the thing that everyone seems to forget: I bought Netfix to watch MOVIES. Original content is great and all<br>but they started of trying to provide a service and then just abandoned that service to essentially become their own TV<br>network. If I’m bored at home and want to watch A Few Good Men, for example, I can’t fre up my Netfix subscription<br>so I’m of to the video store instead, which is exactlythe thingI was tryingto avoid bysubscribingto Netfix.|
|---|---|
|**Generatedquery** _𝑞_**(associated with high** _𝑦𝑞,𝑑_**)**|Is Netfix worth it if I never watch streamingmovies?|
|**Generated query**_𝑞_**(associated with low**_𝑦𝑞,𝑑_**)**|What’s the problem on Netfix if I want to watch A Few Good Men?|
|**Document**_𝑑_**(****_ID:77792)_**|And that’s fne, it’s THEIR network that may or may not provide Internet access, they can do what they want with<br>your data (redirect requests or block certain access) while you’re using it just as landowners can tell you where you<br>can go and what you can do on their land. Sure, it’s shitty, but it’s their right to be shitty about it. If you don’t want to<br>be subject to that, don’t connect to their WiFi network.|
|**Generatedquery** _𝑞_**(associated with high** _𝑦𝑞,𝑑_**)**|What are the dangers of connectingto a network?|
|**Generated query**_𝑞_**(associated with low**_𝑦𝑞,𝑑_**)**|What can a network administrator do to me like a landowner?|



consistently achieves the best performance. Additionally, the models’ performance improves to varying degrees with the addition of a reranker. Due to space constraints, the results for the remaining datasets in the BEIR benchmark are provided in Appendix A.3. 

## **5.6 Performance in the Fully-Supervised Setting** 

To further demonstrate the effectiveness of iGFT, we evaluated its performance using fully supervised data. Unlike the previous low-resource experiments, where we sampled training data from FiQA, MSMARCO, and NQ, we used the complete training data to construct |T _𝑡𝑟𝑎𝑖𝑛_ |. The experimental results in Table 3 show that even with sufficient training data, our framework still enhances the performance of the dense retrieval model. 

## **5.7 Case Study** 

To enable a more intuitive analysis of the data quality produced by our query generator G _𝑡_ for fine-tuning the dense retrieval model, this case study presents examples of the generated queries for the FiQA dataset. As illustrated in Table 4, our query generator G _𝑡_ is capable of producing queries tailored to different documents. For instance, document #527311 outlines reasons a user might choose not to renew their Netflix subscription, primarily due to the inability to watch non-Netflix Original content, such as “A Few Good Men”. The generated queries demonstrate substantial relevance to the document _𝑑_ , further validating the effectiveness of the synthetic data in enhancing the training process of the dense retrieval model. Notably, the first generated query exhibits a higher _𝑦𝑑,𝑞_ value compared to the second. The second query directly targets the keyword “A Few Good Men" from the document, while the first requires a degree of inference to formulate an answer based on the document’s content, posing a greater challenge for the retrieval model. Consequently, in our iGFT framework, we implement an iterative optimization strategy to update the generator, encouraging it to produce such challenging instances, thereby significantly improving the performance of the dense retrieval model. 

Subsequently, we demonstrated that our iteratively optimized generator more easily produces informative synthetic data for dense retrieval models compared to a static generator. Specifically, we used both the initial generator G1 and its iteratively updated version, G2 (after one iteration), to generate 10 queries for each document _𝑑_ T� _𝐺,_ ∈D1 and. This process produced two corresponding synthetic datasetsT� _𝐺,_ 2. After applying our multi-stage filtering process, we 

**==> picture [74 x 80] intentionally omitted <==**

**Figure 6: Distribution of diff** ( _𝑑_ ) **calculated** T�[4] _𝐺,_ 1 **andfrom** T[�][4] _𝐺,_ **different** 2 **, which crafted by gen-synthetic data erators** G1 **and** G2 **, respectively. It can be observed that our iteratively updated generator is more likely to produce samples with higher diff** ( _𝑑_ ) **.** 

derived T[�][4] _𝐺,_ 1 and T[�][4] _𝐺,_ 2. Figure 6 presents the distribution of diff _𝑑_ , for each _𝑑_ ∈D, computed from T[�][4] _𝐺,_ 1 and T[�][4] _𝐺,_ 2, respectively. The results indicate that the iterative training of our generator significantly improves the likelihood of generating high-quality and informative synthetic queries, thereby validating the effectiveness of the iterative optimization strategy in enhancing the overall framework. 

## **6 Conclusion** 

In this paper, we introduced iGFT, a novel framework aimed at enhancing low-resource dense retrieval by integrating a three-phase process—Generation, Filtering, and Tuning—coupled with an iterative optimization strategy. To be more specific, we first employed an LLM to generate appropriate queries for documents with supervised fine-tuning on limited ground truth data. Subsequently, a multi-stage filtering module was present to mitigate noisy data while selecting samples that notably enhance the performance of dense retrieval models. To produce more informative queries, we devised a novel iterative optimization strategy capable of dynamically refining the LLM-based query generator. This strategy facilitated the gradual enhancement of the information retrieval capabilities of the entire framework. Finally, extensive experiments conducted on several publicly available retrieval benchmark datasets have demonstrated the effectiveness of the proposed iGFT. 

## **Acknowledgments** 

This work was partially supported by the National Natural Science Foundation of China (No.92470204), the Fundamental Research Project of CNIC (No.E4552304), the Postdoctoral Fellowship Program of CPSF (No.GZC20232811), and the China Postdoctoral Science Foundation (No.2024M753357). 

1381 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Zhenyu Tong et al. 

## **References** 

- [1] Akiko Aizawa. 2003. An information-theoretic perspective of tf–idf measures. _Information Processing & Management_ 39, 1 (2003), 45–65. 

- [2] Markus Bayer, Marc-André Kaufhold, and Christian Reuter. 2022. A Survey on Data Augmentation for Text Classification. _ACM Comput. Surv._ 55, 7, Article 146 (dec 2022), 39 pages. https://doi.org/10.1145/3544558 

- [3] Andrzej Białecki, Robert Muir, Grant Ingersoll, and Lucid Imagination. 2012. Apache lucene 4. In _SIGIR 2012 workshop on open source information retrieval_ . 17. 

- [4] Luiz Bonifacio, Hugo Abonizio, Marzieh Fadaee, Rodrigo Nogueira, et al. 2022. InPars: Unsupervised Dataset Generation for Information Retrieval. In _PROCEEDINGS OF THE 45TH INTERNATIONAL ACM SIGIR CONFERENCE ON RESEARCH AND DEVELOPMENT IN INFORMATION RETRIEVAL (SIGIR’22)_ . 6. 

- [5] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020. Language models are few-shot learners. _Advances in neural information processing systems_ 33 (2020), 1877–1901. 

- [6] Yupeng Chang, Xu Wang, Jindong Wang, Yuan Wu, Linyi Yang, Kaijie Zhu, Hao Chen, Xiaoyuan Yi, Cunxiang Wang, Yidong Wang, et al. 2023. A survey on evaluation of large language models. _ACM Transactions on Intelligent Systems and Technology_ (2023). 

- [7] Xilun Chen, Kushal Lakhotia, Barlas Oguz, Anchit Gupta, Patrick Lewis, Stan Peshterliev, Yashar Mehdad, Sonal Gupta, and Wen-tau Yih. 2022. Salient Phrase Aware Dense Retrieval: Can a Dense Retriever Imitate a Sparse One?. In _Findings of the Association for Computational Linguistics: EMNLP 2022_ . 250–262. 

- [8] Zhuyun Dai, Vincent Y Zhao, Ji Ma, Yi Luan, Jianmo Ni, Jing Lu, Anton Bakalov, Kelvin Guu, Keith Hall, and Ming-Wei Chang. 2022. Promptagator: Few-shot Dense Retrieval From 8 Examples. In _The Eleventh International Conference on Learning Representations_ . 

- [9] Chuyu Fang, Chuan Qin, Qi Zhang, Kaichun Yao, Jingshuai Zhang, Hengshu Zhu, Fuzhen Zhuang, and Hui Xiong. 2023. Recruitpro: A pretrained language model with skill-aware prompt learning for intelligent recruitment. In _Proceedings of the 29th ACM SIGKDD Conference on Knowledge Discovery and Data Mining_ . 3991–4002. 

- [10] Luyu Gao, Xueguang Ma, Jimmy Lin, and Jamie Callan. 2023. Precise Zero-Shot Dense Retrieval without Relevance Labels. In _Proceedings of the 61st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . 1762–1777. 

- [11] Mitko Gospodinov, Sean MacAvaney, and Craig Macdonald. 2023. Doc2Query–: when less is more. In _European Conference on Information Retrieval_ . Springer, 414–422. 

- [12] Jiafeng Guo, Yinqiong Cai, Yixing Fan, Fei Sun, Ruqing Zhang, and Xueqi Cheng. 2022. Semantic models for the first-stage retrieval: A comprehensive review. _ACM Transactions on Information Systems (TOIS)_ 40, 4 (2022), 1–42. 

- [13] Jiafeng Guo, Yixing Fan, Qingyao Ai, and W Bruce Croft. 2016. A deep relevance matching model for ad-hoc retrieval. In _Proceedings of the 25th ACM international on conference on information and knowledge management_ . 55–64. 

- [14] Jiafeng Guo, Yixing Fan, Liang Pang, Liu Yang, Qingyao Ai, Hamed Zamani, Chen Wu, W Bruce Croft, and Xueqi Cheng. 2020. A deep look into neural ranking models for information retrieval. _Information Processing & Management_ 57, 6 (2020), 102067. 

- [15] Helia Hashemi, Yong Zhuang, Sachith Sri Ram Kothur, Srivas Prasad, Edgar Meij, and W Bruce Croft. 2023. Dense retrieval adaptation using target domain description. In _Proceedings of the 2023 ACM SIGIR International Conference on Theory of Information Retrieval_ . 

- [16] Edward J Hu, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, Weizhu Chen, et al. 2021. LoRA: Low-Rank Adaptation of Large Language Models. In _International Conference on Learning Representations_ . 

- [17] Po-Sen Huang, Xiaodong He, Jianfeng Gao, Li Deng, Alex Acero, and Larry Heck. 2013. Learning deep structured semantic models for web search using clickthrough data. In _Proceedings of the 22nd ACM international conference on Information & Knowledge Management_ . 2333–2338. 

- [18] Gautier Izacard, Mathilde Caron, Lucas Hosseini, Sebastian Riedel, Piotr Bojanowski, Armand Joulin, and Edouard Grave. 2022. Unsupervised Dense Information Retrieval with Contrastive Learning. _Transactions on Machine Learning Research_ (2022). 

- [19] Vitor Jeronymo, Luiz Bonifacio, Hugo Abonizio, Marzieh Fadaee, Roberto Lotufo, Jakub Zavrel, and Rodrigo Nogueira. 2023. InPars-v2: Large Language Models as Efficient Dataset Generators for Information Retrieval. _arXiv preprint arXiv:2301.01820_ (2023). 

- [20] Feihu Jiang, Chuan Qin, Kaichun Yao, Chuyu Fang, Fuzhen Zhuang, Hengshu Zhu, and Hui Xiong. 2024. Enhancing question answering for enterprise knowledge bases using large language models. In _International Conference on Database Systems for Advanced Applications_ . Springer, 273–290. 

- [21] Jeff Johnson, Matthijs Douze, and Hervé Jégou. 2019. Billion-scale similarity search with gpus. _IEEE Transactions on Big Data_ 7, 3 (2019), 535–547. 

- [22] Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Danqi Chen, and Wen-tau Yih. 2020. Dense Passage Retrieval for OpenDomain Question Answering. In _Proceedings of the 2020 Conference on Empirical_ 

_Methods in Natural Language Processing (EMNLP)_ . Association for Computational Linguistics. 

- [23] Jacob Devlin Ming-Wei Chang Kenton and Lee Kristina Toutanova. 2019. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In _Proceedings of NAACL-HLT_ . 4171–4186. 

- [24] Omar Khattab and Matei Zaharia. 2020. Colbert: Efficient and effective passage search via contextualized late interaction over bert. In _Proceedings of the 43rd International ACM SIGIR conference on research and development in Information Retrieval_ . 39–48. 

- [25] Mei Kobayashi and Koichi Takeda. 2000. Information retrieval on the web. _ACM computing surveys (CSUR)_ 32, 2 (2000), 144–173. 

- [26] Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. 2019. Latent Retrieval for Weakly Supervised Open Domain Question Answering. In _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ . 6086–6096. 

- [27] Yibin Lei, Yu Cao, Tianyi Zhou, Tao Shen, and Andrew Yates. 2024. CorpusSteered Query Expansion with Large Language Models. In _Proceedings of the 18th Conference of the European Chapter of the Association for Computational Linguistics (Volume 2: Short Papers)_ . 393–401. 

- [28] Patrick Lewis, Ethan Perez, Aleksandra Piktus, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, et al. 2020. Retrieval-augmented generation for knowledge-intensive nlp tasks. _Advances in Neural Information Processing Systems_ 33 (2020), 9459–9474. 

- [29] Fangyuan Luo, Jun Wu, and Tao Wang. 2023. Discrete Listwise Content-aware Recommendation. _ACM Trans. Knowl. Discov. Data_ 18, 1, Article 7 (aug 2023), 20 pages. https://doi.org/10.1145/3609334 

- [30] Ji Ma, Ivan Korotkov, Yinfei Yang, Keith Hall, and Ryan McDonald. 2021. Zero-shot Neural Passage Retrieval via Domain-targeted Synthetic Question Generation. In _Proceedings of the 16th Conference of the European Chapter of the Association for Computational Linguistics: Main Volume_ . 

- [31] Rui Meng, Ye Liu, Semih Yavuz, Divyansh Agarwal, Lifu Tu, Ning Yu, Jianguo Zhang, Meghana Bhat, and Yingbo Zhou. 2022. Unsupervised Dense Retrieval Deserves Better Positive Pairs: Scalable Augmentation with Query Extraction and Generation. _arXiv preprint arXiv:2212.08841_ (2022). 

- [32] Rodrigo Nogueira, Zhiying Jiang, Ronak Pradeep, and Jimmy Lin. 2020. Document Ranking with a Pretrained Sequence-to-Sequence Model. In _Findings of the Association for Computational Linguistics: EMNLP 2020_ . 708–718. 

- [33] Rodrigo Nogueira, Jimmy Lin, and AI Epistemic. 2019. From doc2query to docTTTTTquery. _Online preprint_ 6, 2 (2019). 

- [34] Rodrigo Nogueira, Wei Yang, Jimmy Lin, and Kyunghyun Cho. 2019. Document expansion by query prediction. _arXiv preprint arXiv:1904.08375_ (2019). 

- [35] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al. 2022. Training language models to follow instructions with human feedback. _Advances in Neural Information Processing Systems_ 35 (2022), 27730–27744. 

- [36] Shivank Pandey and KC Rajeswari. 2013. Automatic question generation using software agents for technical institutions. _International Journal of Advanced Computer Research_ 3, 4 (2013), 307. 

- [37] Zhiyuan Peng, Xuyang Wu, and Yi Fang. 2023. Soft prompt tuning for augmenting dense retrieval with large language models. _arXiv preprint arXiv:2307.08303_ (2023). 

- [38] Chuan Qin, Le Zhang, Yihang Cheng, Rui Zha, Dazhong Shen, Qi Zhang, Xi Chen, Ying Sun, Chen Zhu, Hengshu Zhu, et al. 2023. A comprehensive survey of artificial intelligence techniques for talent analytics. _arXiv preprint arXiv:2307.03195_ (2023). 

- [39] Yingqi Qu, Yuchen Ding, Jing Liu, Kai Liu, Ruiyang Ren, Wayne Xin Zhao, Daxiang Dong, Hua Wu, and Haifeng Wang. 2021. RocketQA: An Optimized Training Approach to Dense Passage Retrieval for Open-Domain Question Answering. In _Proceedings of the 2021 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ . 5835–5847. 

- [40] Sheetal Rakangor and YR Ghodasara. 2015. Literature review of automatic question generation systems. _International journal of scientific and research publications_ 5, 1 (2015), 1–5. 

- [41] Ori Ram, Gal Shachaf, Omer Levy, Jonathan Berant, and Amir Globerson. 2022. Learning to Retrieve Passages without Supervision. In _Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ . 2687–2700. 

- [42] Sylvestre-Alvise Rebuffi, Sven Gowal, Dan Andrei Calian, Florian Stimberg, Olivia Wiles, and Timothy A Mann. 2021. Data Augmentation Can Improve Robustness. In _Advances in Neural Information Processing Systems_ , M. Ranzato, A. Beygelzimer, Y. Dauphin, P.S. Liang, and J. Wortman Vaughan (Eds.), Vol. 34. Curran Associates, Inc., 29935–29948. https://proceedings.neurips.cc/paper_files/paper/2021/file/ fb4c48608ce8825b558ccf07169a3421-Paper.pdf 

- [43] Stephen E Robertson, Steve Walker, Susan Jones, Micheline M Hancock-Beaulieu, Mike Gatford, et al. 1995. Okapi at TREC-3. _Nist Special Publication Sp_ 109 (1995), 109. 

- [44] Jon Saad-Falcon, Omar Khattab, Keshav Santhanam, Radu Florian, Martin Franz, Salim Roukos, Avirup Sil, Md Arafat Sultan, and Christopher Potts. 2023. UDAPDR: Unsupervised Domain Adaptation via LLM Prompting and Distillation 

1382 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

From Missteps to Mastery: Enhancing Low-Resource Dense Retrieval through Adaptive Query Generation 

of Rerankers. _arXiv preprint arXiv:2303.00807_ (2023). 

- [45] Devendra Sachan, Mostofa Patwary, Mohammad Shoeybi, Neel Kant, Wei Ping, William L Hamilton, and Bryan Catanzaro. 2021. End-to-End Training of Neural Retrievers for Open-Domain Question Answering. In _Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)_ . 6648–6662. 

- [46] Minjoon Seo, Tom Kwiatkowski, Ankur Parikh, Ali Farhadi, and Hannaneh Hajishirzi. 2018. Phrase-Indexed Question Answering: A New Challenge for Scalable Document Comprehension. In _Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing_ . 559–564. 

- [47] Minjoon Seo, Jinhyuk Lee, Tom Kwiatkowski, Ankur Parikh, Ali Farhadi, and Hannaneh Hajishirzi. 2019. Real-Time Open-Domain Question Answering with Dense-Sparse Phrase Index. In _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ . 4430–4441. 

- [48] Tao Shen, Guodong Long, Xiubo Geng, Chongyang Tao, Tianyi Zhou, and Daxin Jiang. 2023. Large language models are strong zero-shot retriever. _arXiv preprint arXiv:2304.14233_ (2023). 

- [49] Xiaoyu Shen, Svitlana Vakulenko, Marco Del Tredici, Gianni Barlacchi, Bill Byrne, and Adrià de Gispert. 2022. Low-resource dense retrieval for open-domain question answering: A comprehensive survey. _arXiv preprint arXiv:2208.03197_ (2022). 

- [50] Nandan Thakur, Nils Reimers, Andreas Rücklé, Abhishek Srivastava, and Iryna Gurevych. 2021. BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models. In _Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)_ . 

- [51] Hugo Touvron, Louis Martin, Kevin Stone, Peter Albert, Amjad Almahairi, Yasmine Babaei, Nikolay Bashlykov, Soumya Batra, Prajjwal Bhargava, Shruti Bhosale, et al. 2023. Llama 2: Open foundation and fine-tuned chat models. _arXiv preprint arXiv:2307.09288_ (2023). 

- [52] Kexin Wang, Nandan Thakur, Nils Reimers, and Iryna Gurevych. 2022. GPL: Generative Pseudo Labeling for Unsupervised Domain Adaptation of Dense Retrieval. In _Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ . 

- [53] Liang Wang, Nan Yang, and Furu Wei. 2023. Query2doc: Query Expansion with Large Language Models. In _The 2023 Conference on Empirical Methods in Natural Language Processing_ . 

- [54] Lee Xiong, Chenyan Xiong, Ye Li, Kwok-Fung Tang, Jialin Liu, Paul Bennett, Junaid Ahmed, and Arnold Overwijk. 2020. Approximate nearest neighbor negative contrastive learning for dense text retrieval. _arXiv preprint arXiv:2007.00808_ (2020). 

- [55] Canwen Xu, Daya Guo, Nan Duan, and Julian McAuley. 2022. LaPraDoR: Unsupervised Pretrained Dense Retriever for Zero-Shot Text Retrieval. In _Findings of the Association for Computational Linguistics: ACL 2022_ . 3557–3569. 

- [56] Peilin Yang, Hui Fang, and Jimmy Lin. 2017. Anserini: Enabling the use of lucene for information retrieval research. In _Proceedings of the 40th international ACM SIGIR conference on research and development in information retrieval_ . 1253–1256. 

- [57] Shunyu Zhang, Yaobo Liang, Ming Gong, Daxin Jiang, and Nan Duan. 2022. MultiView Document Representation Learning for Open-Domain Dense Retrieval. In _Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ . 5990–6000. 

- [58] Wayne Xin Zhao, Jing Liu, Ruiyang Ren, and Ji-Rong Wen. 2022. Dense text retrieval based on pretrained language models: A survey. _arXiv preprint arXiv:2211.14876_ (2022). 

- [59] Yutao Zhu, Huaying Yuan, Shuting Wang, Jiongnan Liu, Wenhan Liu, Chenlong Deng, Zhicheng Dou, and Ji-Rong Wen. 2023. Large language models for information retrieval: A survey. _arXiv preprint arXiv:2308.07107_ (2023). 

## **A Appendix** 

## **A.1 Dataset Descriptions** 

We conducted our experiments using a series of datasets included in the BEIR benchmark. The detailed descriptions are provided below: 

- **FiQA** : FiQA dataset concentrates on question-and-answer sessions related to financial matters, encompassing a diverse range of inquiries and responses sourced from financial forums. 

- **MSMARCO** : MSMARCO is a substantial question-answer and information retrieval dataset. It aims to foster advancements in machine reading comprehension and search engine algorithms. 

- **NQ** : NQ centers primarily on question-answering tasks. Each question is grounded in real-world information requirements and correlated with answers extracted from complete web pages. 

- **HotpotQA** : HotpotQA is a specialized dataset for studying multihop questions in natural language question answering, featuring comprehensive supervision of supporting facts. 

- **Quora** : Quora is sourced from the Quora Q&A platform, with questions and answers created by its users. It covers a wide range of topics and includes annotations indicating whether each question is semantically similar to existing questions. 

- **CQADupstack** : CQADupStack is a community question-answering dataset sourced from StackExchange, comprising Q&A posts across 12 subdomains, including programming (Stack Overflow), mathematics (Math Stack Exchange), and physics (Physics Stack Exchange). 

- **TREC-COVID** : The TREC-COVID dataset is specifically designed for the retrieval of information related to the COVID-19 pandemic. It aims to assist researchers in accessing reliable data about the virus and its impacts. 

- **NFCorpus** : NFCorpus is designed for medical information retrieval. It comprises non-technical natural language queries and corresponding complex, terminology-heavy documents. 

- **Trec-News** : TREC-News is a dataset for news information retrieval, aimed at enhancing the understanding of content relevance in news retrieval. 

- **Robust04** : Robust04 consists of news articles and other texts, focusing on poorly performing topics to advance retrieval techniques. 

- **ArguAna** : ArguAna dataset is sourced from debate websites and forums, comprising a large number of speculative questions and responses with supporting and opposing arguments. 

- **Touche-2020** : The Touche-2020 dataset comprises contentious question-answer pairs in 2020, where each query includes multiple responses with supporting or opposing positions and arguments. 

- **DBPedia-Entity** : DBPedia is extracted from Wikipedia in a structured manner, containing a large number of entities along with their corresponding attributes and relationships. 

- **SciDocs** : SciDocs is composed of research papers from a wide range of academic fields, including structured information such as authors, titles, and abstracts. It aims to contribute to advancements in paper information retrieval. 

- **Fever** : Fever is a fact verification dataset sourced from Wikipedia. It consists of queries requiring validation, corresponding evidence, and labels indicating the truthfulness of the claims. In the field of information retrieval, it is treated as a task of retrieving evidence corresponding to the queries. 

- **Climate-Fever** : Climate-Fever is a fact verification dataset in the climate domain, sourced from scientific papers, news articles, government reports, and more. Similar to Fever, it includes climate-related queries, corresponding evidence, and truthfulness labels. 

- **SciFact** : SciFact is a fact verification dataset sourced from peerreviewed scientific papers. It includes science-related queries, corresponding evidence, and truthfulness labels. 

- Please note that in our experiments, the BioASQ and Signal datasets from BEIR were not included. This is because these two datasets are not publicly available, and we have not yet succeeded in obtaining access to them. 

1383 

KDD ’25, August 3–7, 2025, Toronto, ON, Canada 

Zhenyu Tong et al. 

**Table S1: The performances in the zero-shot setting of our model and representative baselines on all accessible datasets in the BEIR benchmark.** 

|**benchmark.**|||||
|---|---|---|---|---|
|**Models**|QGen<br>InPars-v2<br>LaPraDoR|Ours|InPars-v2*<br>LaPraDoR*|Ours*|
|FiQA<br>NQ<br>HotPotQA<br>Quora<br>CQADupstack<br>TREC-COVID<br>NFCorpus<br>Trec-News<br>Robust04<br>ArguAna<br>Touche-2020<br>DBPedia-Entity<br>SciDocs<br>Fever<br>Climate-Fever<br>SciFact|0.3082<br>0.3243<br>0.3290<br>0.3583<br>0.4532<br>0.4872<br>0.5245<br>0.5406<br>0.6241<br>0.8129<br>0.8080<br>0.8692<br>0.3589<br>0.3019<br>0.2427<br>0.6083<br>0.7184<br>0.7389<br>0.3032<br>0.3341<br>0.3246<br>0.3872<br>0.3825<br>0.4481<br>0.3567<br>0.4285<br>0.4901<br>0.4934<br>0.4725<br>0.5072<br>0.1822<br>0.2845<br>0.3241<br>0.3281<br>0.4192<br>0.4189<br>0.1429<br>0.1129<br>0.1829<br>0.6693<br>0.6671<br>0.6821<br>0.1755<br>0.1725<br>0.2267<br>0.6429<br>0.6825<br>0.6882|0.3628<br>0.5221<br>0.6665<br>0.8468<br>0.3792<br>0.7712<br>0.3815<br>0.4323<br>0.4805<br>0.5105<br>0.3107<br>0.4624<br>0.1675<br>0.7894<br>0.1947<br>0.7430|0.5085<br>0.4973<br>0.6382<br>0.7072<br>0.7912<br>0.7832<br>0.8451<br>0.8946<br>0.4483<br>0.4672<br>0.8462<br>0.8518<br>0.3845<br>0.4409<br>0.4902<br>0.5241<br>0.6322<br>0.6018<br>0.4690<br>0.5273<br>0.2905<br>0.3305<br>0.4979<br>0.4902<br>0.2083<br>0.2472<br>0.8715<br>0.7894<br>0.3234<br>0.3371<br>0.7743<br>0.7523|0.5202<br>0.7119<br>0.8215<br>0.8889<br>0.4925<br>0.8792<br>0.4252<br>0.5135<br>0.6312<br>0.5583<br>0.3175<br>0.5123<br>0.2238<br>0.8714<br>0.3451<br>0.7962|
|Avg.|0.3913<br>0.4178<br>0.4461|0.4718|0.5637<br>0.5776|0.5943|



**Table S2: The efficiency of static generator and iterative updated generator.** 

|**dated generator.**|||||||
|---|---|---|---|---|---|---|
|**Models**|**NDCG**|**MAP**|**Recall**|**MRR**|**Time**|**FLOPS**|
|Static generator<br>Iterative updated generator|0.3262<br>0.3312|0.2568<br>0.2583|0.5225<br>0.5273|0.2826<br>0.2925|1.6h<br>2.1h|24.32 PFLOP<br>34.13 PFLOP|



**Table S3: The performance of static generator and iterative updated generator over iterations.** 

|**Models**|**Static generator**|
|---|---|
|**#Iteration**|**NDCG**<br>**MAP**<br>**Recall**<br>**MRR**|
|1<br>0.3281<br>0.2402<br>0.4817<br>0.3491<br>2<br>0.3581<br>0.2517<br>0.4991<br>0.3518<br>3<br>0.3579<br>0.2502<br>0.4969<br>0.3512||
|**Models**<br>**Iterative updated generator**||
|**#Iteration**|**NDCG**<br>**MAP**<br>**Recall**<br>**MRR**|
|1<br>2<br>3|0.3672<br>0.2549<br>0.5117<br>0.3682<br>0.4002<br>0.3434<br>0.5310<br>0.3940<br>0.4218<br>0.3842<br>0.5720<br>0.4182|



**A.2 The Time Cost of the Iterative Optimization** We conducted a detailed analysis of the iterative efficiency during the training process on the FiQA dataset. As illustrated in Table S2, while maintaining an equivalent total output of pseudo queries, we compared the training duration for the reinforcement learning (RL) process with the time and flops (floating point operations) required for each round of direct generation. Our findings reveal that generating an equivalent number of queries using the iterative method requires 31.25% more time and 40.33% more flops. Considering the additional training overhead of RL, coupled with the fact that the iterative updated generator is more adept at producing high-quality 

data, our proposed method is demonstrated to be more efficient. Moreover, we have conducted an additional experiment to illustrate the performance differences between the models when allocated the same time budget per iteration in Table S3. This highlights that our iterative optimization progressively unlocks the latent potential of the generator, enabling more efficient improvements in the performance of the dense retrieval model while maintaining the same computational resource constraints. In contrast, the static generator faces a performance bottleneck, limiting its effectiveness. 

Compared to other query generation models, which do not use iterative computations, our model is more computationally efficient in the non-iterative setting, with InPars [4], Promptagator [8], and UDAPDR [44] taking 2.03h, 2.5h, and 1.92h, respectively, while our model requires only 1.6h. With iterative computations, our model takes 2.1h, 9.38% more than the non-iterative approach. However, as shown in previous experiments, this additional cost is justified by the significant performance gains in dense retrieval achieved through iteration. 

## **A.3 Addtional Evaluation in the Zero-Shot Setting** 

Following the experimental setup in Section 5.5, we compared our method with several representative baselines on all accessible datasets in the BEIR benchmark. The results are presented in Table S1. Specifically, we found that our approach achieved an average improvement of 20.57%, 12.92%, and 5.76% in NDCG@10 across all accessible datasets in the BEIR Benchmark, compared to QGen, Inpars-v2, and LaPraDoR, respectively. After incorporating a reranker, our approach continues to achieve improvements of 5.43% and 2.89% for InPars-v2 and LaPraDoR, respectively. These experimental results provide strong evidence that our proposed iGFT method delivers superior performance in the vast majority of zero-shot scenarios. 

1384 

