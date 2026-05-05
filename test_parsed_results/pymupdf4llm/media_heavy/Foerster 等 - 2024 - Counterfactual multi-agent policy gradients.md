# **Counterfactual Multi-Agent Policy Gradients** 

**Jakob N. Foerster**[1] _[,][†]_ jakob.foerster@cs.ox.ac.uk 

**Gregory Farquhar**[1] _[,][†]_ 

gregory.farquhar@cs.ox.ac.uk 

**Triantafyllos Afouras**[1] afourast@robots.ox.ac.uk 

**Nantas Nardelli**[1] nantas@robots.ox.ac.uk 

**Shimon Whiteson**[1] shimon.whiteson@cs.ox.ac.uk 

## 1University of Oxford, United Kingdom 

## _†_ Equal contribution 

## **Abstract** 

Many real-world problems, such as network packet routing and the coordination of autonomous vehicles, are naturally modelled as cooperative multi-agent systems. There is a great need for new reinforcement learning methods that can efficiently learn decentralised policies for such systems. To this end, we propose a new multi-agent actor-critic method called _counterfactual multi-agent_ (COMA) policy gradients. COMA uses a centralised critic to estimate the _Q_ -function and decentralised actors to optimise the agents’ policies. In addition, to address the challenges of multi-agent credit assignment, it uses a _counterfactual baseline_ that marginalises out a single agent’s action, while keeping the other agents’ actions fixed. COMA also uses a critic representation that allows the counterfactual baseline to be computed efficiently in a single forward pass. We evaluate COMA in the testbed of _StarCraft unit micromanagement_ , using a decentralised variant with significant partial observability. COMA significantly improves average performance over other multi-agent actorcritic methods in this setting, and the best performing agents are competitive with state-of-the-art centralised controllers that get access to the full state. 

## **1 Introduction** 

Many complex _reinforcement learning_ (RL) problems such as the coordination of autonomous vehicles (Cao et al. 2013), network packet delivery (Ye, Zhang, and Yang 2015), and distributed logistics (Ying and Dayong 2005) are naturally modelled as cooperative multi-agent systems. However, RL methods designed for single agents typically fare poorly on such tasks, since the joint action space of the agents grows exponentially with the number of agents. 

To cope with such complexity, it is often necessary to resort to _decentralised policies_ , in which each agent selects its own action conditioned only on its local action-observation history. Furthermore, partial observability and communication constraints during execution may necessitate the use of decentralised policies even when the joint action space is not prohibitively large. 

Hence, there is a great need for new RL methods that can efficiently learn decentralised policies. In some settings, the learning itself may also need to be decentralised. However, in many cases, learning can take place in a simulator 

Copyright © 2018, Association for the Advancement of Artificial Intelligence (www.aaai.org). All rights reserved. 

or a laboratory in which extra state information is available and agents can communicate freely. This _centralised training of decentralised policies_ is a standard paradigm for multi-agent planning (Oliehoek, Spaan, and Vlassis 2008; Kraemer and Banerjee 2016) and has recently been picked up by the deep RL community (Foerster et al. 2016; Jorge, K˚ageb¨ack, and Gustavsson 2016). However, the question of how best to exploit the opportunity for centralised learning remains open. 

Another crucial challenge is _multi-agent credit assignment_ (Chang, Ho, and Kaelbling 2003): in cooperative settings, joint actions typically generate only global rewards, making it difficult for each agent to deduce its own contribution to the team’s success. Sometimes it is possible to design individual reward functions for each agent. However, these rewards are not generally available in cooperative settings and often fail to encourage individual agents to sacrifice for the greater good. This often substantially impedes multi-agent learning in challenging tasks, even with relatively small numbers of agents. 

In this paper, we propose a new multi-agent RL method called _counterfactual multi-agent_ (COMA) policy gradients, in order to address these issues. COMA takes an _actor-critic_ (Konda and Tsitsiklis 2000) approach, in which the _actor_ , i.e., the policy, is trained by following a gradient estimated by a _critic_ . COMA is based on three main ideas. 

First, COMA uses a centralised critic. The critic is only used during learning, while only the actor is needed during execution. Since learning is centralised, we can therefore use a centralised critic that conditions on the joint action and all available state information, while each agent’s policy conditions only on its own action-observation history. 

Second, COMA uses a _counterfactual baseline_ . The idea is inspired by _difference rewards_ (Wolpert and Tumer 2002; Tumer and Agogino 2007), in which each agent learns from a shaped reward that compares the global reward to the reward received when that agent’s action is replaced with a _default action_ . While difference rewards are a powerful way to perform multi-agent credit assignment, they require access to a simulator or estimated reward function, and in general it is unclear how to choose the default action. COMA addresses this by using the centralised critic to compute an agent-specific _advantage function_ that compares the estimated return for the current joint action to a counterfactual 

baseline that marginalises out a single agent’s action, while keeping the other agents’ actions fixed. This is similar to calculating an _aristocrat utility_ (Wolpert and Tumer 2002), but avoids the problem of a recursive interdependence between the policy and utility function because the expected contribution of the counterfactual baseline to the policy gradient is zero. Hence, instead of relying on extra simulations, approximations, or assumptions regarding appropriate default actions, COMA computes a separate baseline for each agent that relies on the centralised critic to reason about counterfactuals in which only that agent’s action changes. 

Third, COMA uses a critic representation that allows the counterfactual baseline to be computed efficiently. In a single forward pass, it computes the _Q_ -values for all the different actions of a given agent, conditioned on the actions of all the other agents. Because a single centralised critic is used for all agents, all _Q_ -values for all agents can be computed in a single batched forward pass. 

We evaluate COMA in the testbed of _StarCraft unit micromanagement_[1] , which has recently emerged as a challenging RL benchmark task with high stochasticity, a large stateaction space, and delayed rewards. Previous works (Usunier et al. 2016; Peng et al. 2017) have made use of a centralised control policy that conditions on the entire state and can use powerful macro-actions, using StarCraft’s built-in planner, that combine movement and attack actions. To produce a meaningfully decentralised benchmark that proves challenging for scenarios with even relatively few agents, we propose a variant that massively reduces each agent’s field-of-view and removes access to these macro-actions. 

Our empirical results on this new benchmark show that COMA can significantly improve performance over other multi-agent actor-critic methods, as well as ablated versions of COMA itself. In addition, COMA’s best agents are competitive with state-of-the-art centralised controllers that are given access to full state information and macro-actions. 

## **2 Related Work** 

Although multi-agent RL has been applied in a variety of settings (Busoniu, Babuska, and De Schutter 2008; Yang and Gu 2004), it has often been restricted to tabular methods and simple environments. One exception is recent work in deep multi-agent RL, which can scale to high dimensional input and action spaces. Tampuu et al. (2015) use a combination of DQN with independent _Q_ -learning (Tan 1993; Shoham and Leyton-Brown 2009) to learn how to play twoplayer pong. More recently the same method has been used by Leibo et al. (2017) to study the emergence of collaboration and defection in sequential social dilemmas. 

Also related is work on the emergence of communication between agents, learned by gradient descent (Das et al. 2017; Mordatch and Abbeel 2017; Lazaridou, Peysakhovich, and Baroni 2016; Foerster et al. 2016; Sukhbaatar, Fergus, and others 2016). In this line of work, passing gradients between agents during training and sharing parameters are two common ways to take advantage of centralised training. How- 

> 1StarCraft and its expansion StarCraft: Brood War are trademarks of Blizzard Entertainment™. 

ever, these methods do not allow for extra state information to be used during learning and do not address the multi-agent credit assignment problem. 

Gupta, Egorov, and Kochenderfer (2017) investigate actor-critic methods for decentralised execution with centralised training. However, in their methods both the actors and the critic condition on local, per-agent, observations and actions, and multi-agent credit assignment is addressed only with hand-crafted local rewards. 

Most previous applications of RL to StarCraft micromanagement use a centralised controller, with access to the full state, and control of all units, although the architecture of the controllers exploits the multi-agent nature of the problem. Usunier et al. (2016) use a _greedy MDP_ , which at each timestep sequentially chooses actions for agents given all previous actions, in combination with zero-order optimisation, while Peng et al. (2017) use an actor-critic method that relies on RNNs to exchange information between the agents. 

The closest to our problem setting is that of Foerster et al. (2017), who also use a multi-agent representation and decentralised policies. However, they focus on stabilising experience replay while using DQN and do not make full use of the centralised training regime. As they do not report on absolute win-rates we do not compare performance directly. However, Usunier et al. (2016) address similar scenarios to our experiments and implement a DQN baseline in a fully observable setting. In Section 6 we therefore report our competitive performance against these state-of-the-art baselines, while maintaining decentralised control. Omidshafiei et al. (2017) also address the stability of experience replay in multi-agent settings, but assume a fully decentralised training regime. 

(Lowe et al. 2017) concurrently propose a multi-agent policy-gradient algorithm using centralised critics. Their approach does not address multi-agent credit assignment. Unlike our work, it learns a separate centralised critic for each agent and is applied to competitive environments with continuous action spaces. 

Our work builds directly off of the idea of _difference rewards_ (Wolpert and Tumer 2002). The relationship of COMA to this line of work is discussed in Section 4. 

## **3 Background** 

We consider a fully cooperative multi-agent task that can be described as a stochastic game _G_ , defined by a tuple _G_ = _⟨S, U, P, r, Z, O, n, γ⟩_ , in which _n_ agents identified by _a ∈ A ≡{_ 1 _, ..., n}_ choose sequential actions. The environment has a true state _s ∈ S_ . At each time step, each agent simultaneously chooses an action _u[a] ∈ U_ , forming a joint action **u** _∈_ **U** _≡ U[n]_ which induces a transition in the environment according to the state transition function _P_ ( _s[′] |s,_ **u** ) : _S ×_ **U** _× S →_ [0 _,_ 1]. The agents all share the same reward function _r_ ( _s,_ **u** ) : _S ×_ **U** _→_ R and _γ ∈_ [0 _,_ 1) is a discount factor. 

We consider a partially observable setting, in which agents draw observations _z ∈ Z_ according to the observation function _O_ ( _s, a_ ) : _S × A → Z_ . Each agent has an action-observation history _τ[a] ∈ T ≡_ ( _Z × U_ ) _[∗]_ , on which it 

conditions a stochastic policy _π[a]_ ( _u[a] |τ[a]_ ) : _T × U →_ [0 _,_ 1]. We denote joint quantities over agents in bold, and joint quantities over agents other than a given agent _a_ with the superscript _−a_ . 

The discounted return is _Rt_ =[�] _[∞] l_ =0 _[γ][l][r][t]_[+] _[l]_[. The agents’] joint policy induces a value function, i.e., an expectation over _Rt_ , _V_ _**[π]**_ ( _st_ ) = E _st_ +1: _∞,_ **u** _t_ : _∞_ [ _Rt|st_ ], and an actionvalue function _Q_ _**[π]**_ ( _st,_ **u** _t_ ) = E _st_ +1: _∞,_ **u** _t_ +1: _∞_ [ _Rt|st,_ **u** _t_ ]. The advantage function is given by _A_ _**[π]**_ ( _st,_ **u** _t_ ) = _Q_ _**[π]**_ ( _st,_ **u** _t_ ) _− V_ _**[π]**_ ( _st_ ). 

Following previous work (Oliehoek, Spaan, and Vlassis 2008; Kraemer and Banerjee 2016; Foerster et al. 2016; Jorge, K˚ageb¨ack, and Gustavsson 2016), our problem setting allows centralised training but requires decentralised execution. This is a natural paradigm for a large set of multi-agent problems where training is carried out using a simulator with additional state information, but the agents must rely on local action-observation histories during execution. To condition on this full history, a deep RL agent may make use of a recurrent neural network (Hausknecht and Stone 2015), typically with a gated model such as LSTM (Hochreiter and Schmidhuber 1997) or GRU (Cho et al. 2014). 

In Section 4, we develop a new multi-agent policy gradient method for tackling this setting. In the remainder of this section, we provide some background on single-agent policy gradient methods (Sutton et al. 1999). Such methods optimise a single agent’s policy, parameterised by _θ[π]_ , by performing gradient ascent on an estimate of the expected discounted total reward _J_ = E _π_ [ _R_ 0]. Perhaps the simplest form of policy gradient is REINFORCE (Williams 1992), in which the gradient is: 

**==> picture [207 x 31] intentionally omitted <==**

In _actor-critic_ approaches (Sutton et al. 1999; Konda and Tsitsiklis 2000; Schulman et al. 2015), the _actor_ , i.e., the policy, is trained by following a gradient that depends on a _critic_ , which usually estimates a value function. In particular, _Rt_ is replaced by any expression equivalent to _Q_ ( _st, ut_ ) _− b_ ( _st_ ), where _b_ ( _st_ ) is a baseline designed to reduce variance (Weaver and Tao 2001). A common choice is _b_ ( _st_ ) = _V_ ( _st_ ), in which case _Rt_ is replaced by _A_ ( _st, ut_ ). Another option is to replace _Rt_ with the _temporal difference_ (TD) error _rt_ + _γV_ ( _st_ +1) _− V_ ( _s_ ), which is an unbiased estimate of _A_ ( _st, ut_ ). In practice, the gradient must be estimated from trajectories sampled from the environment, and the (action-)value functions must be estimated with function approximators. Consequently, the bias and variance of the gradient estimate depends strongly on the exact choice of estimator (Konda and Tsitsiklis 2000). 

In this paper, we train critics _f[c]_ ( _·, θ[c]_ ) on-policy to estimate either _Q_ or _V_ , using a variant of TD( _λ_ ) (Sutton 1988) adapted for use with deep neural networks. TD( _λ_ ) uses a mixture of _n_ -step returns _G_[(] _t[n]_[)] =[�] _[n] l_ =1 _[γ][l][−]_[1] _[r][t]_[+] _[l]_[+] _γ[n] f[c]_ ( _·t_ + _n, θ[c]_ ). In particular, the critic parameters _θ[c]_ are updated by minibatch gradient descent to minimise the following loss: 

**==> picture [181 x 13] intentionally omitted <==**

where _y_[(] _[λ]_[)] = (1 _− λ_ )[�] _[∞] n_ =1 _[λ][n][−]_[1] _[G] t_[(] _[n]_[)] , and the _n_ -step returns _G_[(] _t[n]_[)] are calculated with bootstrapped values estimated by a _target network_ (Mnih et al. 2015) with parameters copied periodically from _θ[c]_ . 

## **4 Methods** 

In this section, we describe approaches for extending policy gradients to our multi-agent setting. 

## **Independent Actor-Critic** 

The simplest way to apply policy gradients to multiple agents is to have each agent learn independently, with its own actor and critic, from its own action-observation history. This is essentially the idea behind _independent Q- learning_ (Tan 1993), which is perhaps the most popular multi-agent learning algorithm, but with actor-critic in place of _Q_ -learning. Hence, we call this approach _independent actor-critic_ (IAC). 

In our implementation of IAC, we speed learning by sharing parameters among the agents, i.e., we learn only one actor and one critic, which are used by all agents. The agents can still behave differently because they receive different observations, including an agent-specific ID, and thus evolve different hidden states. Learning remains independent in the sense that each agent’s critic estimates only a local value function, i.e., one that conditions on _u[a]_ , not **u** . Though we are not aware of previous applications of this specific algorithm, we do not consider it a significant contribution but instead merely a baseline algorithm. 

We consider two variants of IAC. In the first, each agent’s critic estimates _V_ ( _τ[a]_ ) and follows a gradient based on the TD error, as described in Section 3. In the second, each agent’s critic estimates _Q_ ( _τ[a] , u[a]_ ) and follows a gradient based on the advantage: _A_ ( _τ[a] , u[a]_ ) = _Q_ ( _τ[a] , u[a]_ ) _− V_ ( _τ[a]_ ), where _V_ ( _τ[a]_ ) =[�] _u[a][ π]_[(] _[u][a][|][τ][ a]_[)] _[Q]_[(] _[τ][ a][, u][a]_[)][. Indepen-] dent learning is straightforward, but the lack of information sharing at training time makes it difficult to learn coordinated strategies that depend on interactions between multiple agents, or for an individual agent to estimate the contribution of its actions to the team’s reward. 

## **Counterfactual Multi-Agent Policy Gradients** 

The difficulties discussed above arise because, beyond parameter sharing, IAC fails to exploit the fact that learning is centralised in our setting. In this section, we propose _counterfactual multi-agent_ (COMA) policy gradients, which overcome this limitation. Three main ideas underly COMA: 1) centralisation of the critic, 2) use of a counterfactual baseline, and 3) use of a critic representation that allows efficient evaluation of the baseline. The remainder of this section describes these ideas. 

First, COMA uses a centralised critic. Note that in IAC, each actor _π_ ( _u[a] |τ[a]_ ) and each critic _Q_ ( _τ[a] , u[a]_ ) or _V_ ( _τ[a]_ ) conditions only on the agent’s own action-observation history _τ[a]_ . However, the critic is used only during learning and only the actor is needed during execution. Since learning is centralised, we can therefore use a centralised critic that conditions on the true global state _s_ , if it is available, as 

**==> picture [455 x 149] intentionally omitted <==**

**----- Start of picture text -----**<br>
A [1] t Critic A [2] t 𝜋 [a] t  [=][𝜋][(h][a] t [, ][𝜀][) ] A [a] t<br>𝜋(h [1] , 𝜀)  𝜋(h [2] , 𝜀)<br>(𝜀) (u [a] t [, ][𝜋][a] t [) ] COMA<br>h [1] u [1] u [2] h [2]<br>t  t  h [a] t {Q(u [a] =1,  u [-a] t [,..),. .,Q(u][a][=|U|, ] [u] [-a] t [,..)}]<br>Actor 1 Actor 2<br>(h [a] t-1 [)] GRU ( h [a] t [)]<br>o t, st      rt  , ht-1<br>o [1] t u [1] t  u [2] t  o [2] t<br>Environment (o [a] t [, a, u][a] t-1 [)] ( u [-a] t [, s] t [, o][a] t [, a, ] [u] t-1 [,] [h] t [)]<br>(a) (b) (c)<br>**----- End of picture text -----**<br>


Figure 1: In (a), information flow between the decentralised actors, the environment and the centralised critic in COMA; red arrows and components are only required during centralised learning. In (b) and (c), architectures of the actor and critic. 

well as the joint action-observation histories _**τ**_ . Each actor conditions on its own action-observation histories _τ[a]_ , with parameter sharing, as in IAC. Figure 1a illustrates this setup. 

A naive way to use this centralised critic would be for each actor to follow a gradient based on the TD error estimated from this critic: 

**==> picture [224 x 11] intentionally omitted <==**

However, such an approach fails to address a key credit assignment problem. Because the TD error considers only global rewards, the gradient computed for each actor does not explicitly reason about how that particular agent’s actions contribute to that global reward. Since the other agents may be exploring, the gradient for that agent becomes very noisy, particularly when there are many agents. 

Therefore, COMA uses a _counterfactual baseline_ . The idea is inspired by _difference rewards_ (Wolpert and Tumer 2002), in which each agent learns from a shaped reward _D[a]_ = _r_ ( _s,_ **u** ) _− r_ ( _s,_ ( **u** _[−][a] , c[a]_ )) that compares the global reward to the reward received when the action of agent _a_ is replaced with a _default action c[a]_ . Any action by agent _a_ that improves _D[a]_ also improves the true global reward _r_ ( _s,_ **u** ), because _r_ ( _s,_ ( **u** _[−][a] , c[a]_ )) does not depend on agent _a_ ’s actions. 

Difference rewards are a powerful way to perform multiagent credit assignment. However, they typically require access to a simulator in order to estimate _r_ ( _s,_ ( **u** _[−][a] , c[a]_ )). When a simulator is already being used for learning, difference rewards increase the number of simulations that must be conducted, since each agent’s difference reward requires a separate counterfactual simulation. Proper and Tumer (2012) and Colby, Curran, and Tumer (2015) propose estimating difference rewards using function approximation rather than a simulator. However, this still requires a user-specified default action _c[a]_ that can be difficult to choose in many applications. In an actor-critic architecture, this approach would also introduce an additional source of approximation error. 

A key insight underlying COMA is that a centralised critic can be used to implement difference rewards in a 

way that avoids these problems. COMA learns a centralised critic, _Q_ ( _s,_ _**τ** ,_ **u** ) that estimates _Q_ -values for the joint action **u** conditioned on the central state _s_ and the joint actionobservation history. For each agent _a_ we can then compute an advantage function that compares the _Q_ -value for the current action _u[a]_ to a counterfactual baseline that marginalises out _u[a]_ , while keeping the other agents’ actions **u** _[−][a]_ fixed: 

**==> picture [252 x 33] intentionally omitted <==**

Hence, _A[a]_ ( _s,_ _**τ** , u[a]_ ) computes a separate baseline for each agent that uses the centralised critic to reason about counterfactuals in which only _a_ ’s action changes, learned directly from agents’ experiences instead of relying on extra simulations, a reward model, or a user-designed default action. 

This advantage has the same form as the _aristocrat utility_ (Wolpert and Tumer 2002). However, optimising for an aristocrat utility using value-based methods creates a selfconsistency problem because the policy and utility function depend recursively on each other. As a result, prior work focused on difference evaluations using default states and actions. COMA is different because the counterfactual baseline’s expected contribution to the gradient, as with other policy gradient baselines, is zero. Thus, while the baseline does depend on the policy, its expectation does not. Consequently, COMA can use this form of the advantage without creating a self-consistency problem. 

While COMA’s advantage function replaces potential extra simulations with evaluations of the critic, those evaluations may themselves be expensive if the critic is a deep neural network. Furthermore, in a typical representation, the number of output nodes of such a network would equal _|U |[n]_ , the size of the joint action space, making it impractical to train. To address both these issues, COMA uses a critic representation that allows for efficient evaluation of the baseline. In particular, the actions of the other agents, **u** _[−] t[a]_ , are part of the input to the network, which outputs a _Q_ -value for each of agent _a_ ’s actions, as shown in Figure 1c. Consequently, the counterfactual advantage can be calculated efficiently by a single forward pass of the actor and critic, for 

each agent. Furthermore, the number of outputs is only _|U |_ instead of ( _|U |[n]_ ). While the network has a large input space that scales linearly in the number of agents and actions, deep neural networks can generalise well across such spaces. 

In this paper, we focus on settings with discrete actions. However, COMA can be easily extended to continuous actions spaces by estimating the expectation in (4) with Monte Carlo samples or using functional forms that render it analytical, e.g., Gaussian policies and critic. 

The following lemma establishes the convergence of COMA to a locally optimal policy. The proof follows directly from the convergence of single-agent actor-critic algorithms (Sutton et al. 1999), and is subject to the same assumptions. Lyu et al. (2024, Appendix E.2) prove a related result, showing that a family of cooperative policy gradient methods with centralized critics, which includes COMA, converge to local optima assuming access to the correct policy values, i.e., a perfect critic. 

**Lemma 1.** _For an actor-critic algorithm with a compatible TD(1) critic following a COMA policy gradient_ 

**==> picture [214 x 31] intentionally omitted <==**

_at each iteration k,_ 

**==> picture [176 x 15] intentionally omitted <==**

_Proof._ See Appendix A. 

## **5 Experimental Setup** 

In this section, we describe the StarCraft problem to which we apply COMA, as well as details of the state features, network architectures, training regimes, and ablations. 

**Decentralised StarCraft Micromanagement.** StarCraft is a rich environment with stochastic dynamics that cannot be easily emulated. Many simpler multi-agent settings, such as Predator-Prey (Tan 1993) or Packet World (Weyns, Helleboogh, and Holvoet 2005), by contrast, have full simulators with controlled randomness that can be freely set to any state in order to perfectly replay experiences. This makes it possible, though computationally expensive, to compute difference rewards via extra simulations. In StarCraft, as in the real world, this is not possible. 

In this paper, we focus on the problem of _micromanagement_ in StarCraft, which refers to the low-level control of individual units’ positioning and attack commands as they fight enemies. This task is naturally represented as a multi-agent system, where each StarCraft unit is replaced by a decentralised controller. We consider several scenarios with symmetric teams formed of: 3 marines (3m), 5 marines (5m), 5 wraiths (5w), or 2 dragoons with 3 zealots (2d ~~3~~ z). The enemy team is controlled by the StarCraft AI, which uses reasonable but suboptimal hand-crafted heuristics. 

We allow the agents to choose from a set of discrete actions: move[direction], attack[enemy ~~i~~ d], stop, and noop. In the StarCraft game, when a unit selects an attack action, it first moves into attack range before firing, using the game’s built-in pathfinding to choose a 

route. These powerful _attack-move_ macro-actions make the control problem considerably easier. 

To create a more challenging benchmark that is meaningfully decentralised, we impose a restricted field of view on the agents, equal to the firing range of ranged units’ weapons, shown in Figure 2. This departure from the standard setup for centralised StarCraft control has three effects. 

**==> picture [240 x 113] intentionally omitted <==**

**----- Start of picture text -----**<br>
x<br>**----- End of picture text -----**<br>


Figure 2: Starting position with example local field of view for the 2d ~~3~~ z map. 

First, it introduces significant partial observability. Second, it means units can only attack when they are in range of enemies, removing access to the StarCraft macro-actions. Third, agents cannot distinguish between enemies who are dead and those who are out of range and so can issue invalid attack commands at such enemies, which results in no action being taken. This substantially increases the average size of the action space, which in turn increases the difficulty of both exploration and control. 

Under these difficult conditions, scenarios with even relatively small numbers of units become much harder to solve. As seen in Table 1, we compare against a simple hand-coded heuristic that instructs the agents to run forwards into range and then focus their fire, attacking each enemy in turn until it dies. This heuristic achieves a 98% win rate on 5m with a full field of view, but only 66% in our setting. To perform well in this task, the agents must learn to cooperate by positioning properly and focussing their fire, while remembering which enemy and ally units are alive or out of view. 

All agents receive the same global reward at each time step, equal to the sum of damage inflicted on the opponent units minus half the damage taken. Killing an opponent generates a reward of 10 points, and winning the game generates a reward equal to the team’s remaining total health plus 200. This damage-based reward signal is comparable to that used by Usunier et al. (2016). Unlike (Peng et al. 2017), our approach does not require estimating local rewards. 

**State Features.** The actor and critic receive different input features, corresponding to local observations and global state, respectively. Both include features for allies and enemies. _Units_ can be either allies or enemies, while _agents_ are the decentralised controllers that command ally units. 

The local observations for every agent are drawn only from a circular subset of the map centred on the unit it controls and include for each unit within this field of view: distance, relative x, relative y, unit type 

**==> picture [406 x 321] intentionally omitted <==**

**----- Start of picture text -----**<br>
COMA central-QV IAC-V IAC-Q<br>central-V heuristic<br>90 90<br>80 80<br>70 70<br>60 60<br>50 50<br>40 40<br>30 30<br>20 20<br>10 10<br>0 0<br>20k 40k 60k 80k 100k 120k 140k 10k 20k 30k 40k 50k 60k 70k<br>#  Episodes #  Episodes<br>(a) 3m (b) 5m<br>90 70<br>80<br>60<br>70<br>50<br>60<br>50 40<br>40 30<br>30<br>20<br>20<br>10<br>10<br>0 0<br>5k 10k 15k 20k 25k 30k 35k 5k 10k 15k 20k 25k 30k 35k 40k<br>#  Episodes #  Episodes<br>(c) 5w (d) 2d 3 z<br>Average Win % Average Win %<br>Average Win % Average Win %<br>**----- End of picture text -----**<br>


Figure 3: Win rates for COMA and competing algorithms on four different scenarios. COMA outperforms all baseline methods. Centralised critics also clearly outperform their decentralised counterparts. The legend at the top applies across all plots. 

and shield.[2] All features are normalised by their maximum values. We do not include any information about the units’ current target. 

The global state representation consists of similar features, but for all units on the map regardless of fields of view. Absolute distance is not included, and _x_ - _y_ locations are given relative to the centre of the map rather than to a particular agent. The global state also includes health points and cooldown for all agents. The representation fed to the centralised _Q_ -function critic is the concatenation of the global state representation with the local observation of the agent whose actions are being evaluated. Our centralised critic that estimates _V_ ( _s_ ), and is therefore agent-agnostic, receives the global state concatenated with all agents’ observations. The observations contain no new information but include the egocentric distances relative to that agent. 

**Architecture & Training.** The actor consists of 128-bit _gated recurrent units_ (GRUs) (Cho et al. 2014) that use fully connected layers both to process the input and to produce the output values from the hidden state, _h[a] t_[.][The][IAC] 

> 2After firing, a unit’s cooldown is reset, and it must drop before firing again. Shields absorb damage until they break, after which units start losing health. Dragoons and zealots have shields but marines do not. 

critics use extra output heads appended to the last layer of the actor network. Action probabilities are produced from the final layer, **z** , via a bounded softmax distribution that lower-bounds the probability of any given action by _ϵ/|U |_ : _P_ ( _u_ ) = (1 _− ϵ_ )softmax( **z** ) _u_ + _ϵ/|U |_ ). We anneal _ϵ_ linearly from 0 _._ 5 to 0 _._ 02 across 750 training episodes. The centralised critic is a feedforward network with multiple ReLU layers combined with fully connected layers. Hyperparameters were coarsely tuned on the 5m scenario and then used for all other maps. We found that the most sensitive parameter was TD( _λ_ ), but settled on _λ_ = 0 _._ 8, which worked best for both COMA and our baselines. Our implementation uses TorchCraft (Synnaeve et al. 2016) and Torch 7 (Collobert, Kavukcuoglu, and Farabet 2011). Pseudocode and further details on the training procedure are in the supplementary material. 

We experimented with critic architectures that are factored at the agent level and further exploit internal parameter sharing. However, we found that the bottleneck for scalability was not the centralisation of the critic, but rather the difficulty of multi-agent exploration. Hence, we defer further investigation of factored COMA critics to future work. 

**Ablations.** We perform ablation experiments to validate three key elements of COMA. First, we test the importance of centralising the critic by comparing against two IAC vari- 

|map|Local Field of View (FoV)<br>heur.<br>IAC-_V_<br>IAC-_Q_<br>cnt-_V_<br>cnt-_QV_<br>COMA<br>mean<br>best|Full FoV, Central Control<br>heur.<br>DQN<br>GMEZO|
|---|---|---|
|3m<br>5m<br>5w<br>2d<br>~~3~~z|35<br>47 (3)<br>56 (6)<br>83 (3)<br>83 (5)<br>**87**(3)<br>98<br>66<br>63 (2)<br>58 (3)<br>67 (5)<br>71 (9)<br>**81**(5)<br>95<br>70<br>18 (5)<br>57 (5)<br>65 (3)<br>76 (1)<br>**82**(3)<br>98<br>**63**<br>27 (9)<br>19 (21)<br>36 (6)<br>39 (5)<br>47 (5)<br>65|74<br>-<br>-<br>98<br>99<br>100<br>82<br>70<br>743<br>68<br>61<br>90|



Table 1: Mean win percentage averaged across final 1000 evaluation episodes for the different maps, for all methods and the hand-coded heuristic in the decentralised setting with a limited field of view. The highest mean performances are in bold, while values in parentheses denote the 95% confidence interval, for example 87(3) = 87 _±_ 3. Also shown, maximum win percentages for COMA (decentralised), in comparison to the heuristic and published results (evaluated in the centralised setting). 

ants, IAC- _Q_ and IAC- _V_ . These critics take the same decentralised input as the actor, and share parameters with the actor network up to the final layer. IAC- _Q_ then outputs _|U | Q_ -values, one for each action, while IAC- _V_ outputs a single state-value. Note that we still share parameters between agents, using the egocentric observations and ID’s as part of the input to allow different behaviours to emerge. The cooperative reward function is still shared by all agents. 

Second, we test the significance of learning _Q_ instead of _V_ . The method _central-V_ still uses a central state for the critic, but learns _V_ ( _s_ ), and uses the TD error to estimate the advantage for policy gradient updates. 

Third, we test the utility of our counterfactual baseline. The method _central-QV_ learns both _Q_ and _V_ simultaneously and estimates the advantage as _Q − V_ , replacing COMA’s counterfactual baseline with _V_ . All methods use the same architecture and training scheme for the actors, and all critics are trained with TD( _λ_ ). 

## **6 Results** 

Figure 3 shows average win rates as a function of episode for each method and each StarCraft scenario. For each method, we conducted 35 independent trials and froze learning every 100 training episodes to evaluate the learned policies across 200 episodes per method, plotting the average across episodes and trials. Also shown is one standard deviation in performance. 

The results show that COMA is superior to the IAC baselines in all scenarios. Interestingly, the IAC methods also eventually learn reasonable policies in 5m, although they need substantially more episodes to do so. This may seem counterintuitive since in the IAC methods, the actor and critic networks share parameters in their early layers (see Section 5), which could be expected to speed learning. However, these results suggest that the improved accuracy of policy evaluation made possible by conditioning on the global state outweighs the overhead of training a separate network. 

Furthermore, COMA strictly dominates central- _QV_ , both in training speed and in final performance across all settings. This is a strong indicator that our counterfactual baseline is crucial when using a central _Q_ -critic to train decentralised 

## policies. 

Learning a state-value function has the obvious advantage of not conditioning on the joint action. Still, we find that COMA outperforms the central- _V_ baseline in final performance. Furthermore, COMA typically achieves good policies faster, which is expected as COMA provides a shaped training signal. Training is also more stable than central- _V_ , which is a consequence of the COMA gradient tending to zero as the policy becomes greedy. Overall, COMA is the best performing and most consistent method. 

Usunier et al. (2016) report the performance of their best agents trained with their state-of-the-art centralised controller labelled GMEZO (greedy-MDP with episodic zeroorder optimisation), and for a centralised DQN controller, both given a full field of view and access to attack-move macro-actions. These results are compared in Table 1 against the best agents trained with COMA for each map. Clearly, in most settings these agents achieve performance comparable to the best published win rates despite being restricted to decentralised policies and local fields of view. 

## **7 Conclusions & Future Work** 

This paper presented COMA policy gradients, a method that uses a centralised critic in order to estimate a counterfactual advantage for decentralised policies in mutliagent RL. COMA addresses the challenges of multi-agent credit assignment by using a counterfactual baseline that marginalises out a single agent’s action, while keeping the other agents’ actions fixed. Our results in a decentralised _StarCraft unit micromanagement_ benchmark show that COMA significantly improves final performance and training speed over other multi-agent actor-critic methods and remains competitive with state-of-the-art centralised controllers under best-performance reporting. Future work will extend COMA to tackle scenarios with large numbers of agents, where centralised critics are more difficult to train and exploration is harder to coordinate. We also aim to develop more sample-efficient variants that are practical for real-world applications such as self-driving cars. 

35w DQN and GMEZO benchmark performances are of a policy trained on a larger map and tested on 5w 

## **Acknowledgements** 

This project has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme (grant agreement number 637713). It was also supported by the OxfordGoogle DeepMind Graduate Scholarship, the UK EPSRC CDT in Autonomous Intelligent Machines and Systems, and a generous grant from Microsoft for their Azure cloud computing services. We would like to thank Nando de Freitas, Yannis Assael, and Brendan Shillingford for helpful comments and discussion. We also thank Gabriel Synnaeve, Zeming Lin, and the rest of the TorchCraft team at FAIR for their work on the interface. 

## **Errata** 

An earlier version of this paper contained an error in the proof of Lemma 1 because the critic depended on the state _s_ but not the joint history _**τ**_ . In this version, Equation 4 and Figure 1 have been updated to add this dependence. In addition, the proof of Lemma 1 has been revised to show explicitly how existing policy gradient results apply to this modified setting. The proof also refers to the Sutton et al. (1999) result instead of that of Konda and Tsitsiklis (2000) as the latter requires that the Markov chain induced by the policy be irreducible, which does not hold for history-based state representations. Thanks to Frans Oliehoek and Chris Amato for pointing out these issues. Thanks also to Frans Oliehoek and Andrea Baisero for feedback on the revised proof. See also Lyu et al.; Lyu et al.; Lyu et al.; Lyu et al. (2021; 2022; 2023; 2024) for more details on this topic. 

## **References** 

Busoniu, L.; Babuska, R.; and De Schutter, B. 2008. A comprehensive survey of multiagent reinforcement learning. _IEEE Transactions on Systems Man and Cybernetics Part C Applications and Reviews_ 38(2):156. 

Cao, Y.; Yu, W.; Ren, W.; and Chen, G. 2013. An overview of recent progress in the study of distributed multi-agent coordination. _IEEE Transactions on Industrial informatics_ 9(1):427–438. 

Chang, Y.-H.; Ho, T.; and Kaelbling, L. P. 2003. All learning is local: Multi-agent learning in global reward games. In _NIPS_ , 807–814. 

Cho, K.; van Merri¨enboer, B.; Bahdanau, D.; and Bengio, Y. 2014. On the properties of neural machine translation: Encoder-decoder approaches. _arXiv preprint arXiv:1409.1259_ . 

Colby, M. K.; Curran, W.; and Tumer, K. 2015. Approximating difference evaluations with local information. In _Proceedings of the 2015 International Conference on Autonomous Agents and Multiagent Systems_ , 1659–1660. International Foundation for Autonomous Agents and Multiagent Systems. 

Collobert, R.; Kavukcuoglu, K.; and Farabet, C. 2011. Torch7: A matlab-like environment for machine learning. In _BigLearn, NIPS Workshop_ . 

Das, A.; Kottur, S.; Moura, J. M.; Lee, S.; and Batra, D. 2017. Learning cooperative visual dialog agents with deep reinforcement learning. _arXiv preprint arXiv:1703.06585_ . 

Foerster, J.; Assael, Y. M.; de Freitas, N.; and Whiteson, S. 2016. Learning to communicate with deep multi-agent reinforcement learning. In _Advances in Neural Information Processing Systems_ , 2137–2145. 

Foerster, J.; Nardelli, N.; Farquhar, G.; Torr, P.; Kohli, P.; Whiteson, S.; et al. 2017. Stabilising experience replay for deep multi-agent reinforcement learning. In _Proceedings of The 34th International Conference on Machine Learning_ . 

Gupta, J. K.; Egorov, M.; and Kochenderfer, M. 2017. Cooperative multi-agent control using deep reinforcement learning. 

Hausknecht, M., and Stone, P. 2015. Deep recurrent q-learning for partially observable mdps. _arXiv preprint arXiv:1507.06527_ . 

Hochreiter, S., and Schmidhuber, J. 1997. Long short-term memory. _Neural computation_ 9(8):1735–1780. 

Jorge, E.; K˚ageb¨ack, M.; and Gustavsson, E. 2016. Learning to play guess who? and inventing a grounded language as a consequence. _arXiv preprint arXiv:1611.03218_ . 

Konda, V. R., and Tsitsiklis, J. N. 2000. Actor-critic algorithms. In _Advances in neural information processing systems_ , 1008–1014. 

Kraemer, L., and Banerjee, B. 2016. Multi-agent reinforcement learning as a rehearsal for decentralized planning. _Neurocomputing_ 190:82–94. 

Lazaridou, A.; Peysakhovich, A.; and Baroni, M. 2016. Multi-agent cooperation and the emergence of (natural) language. _arXiv preprint arXiv:1612.07182_ . 

Leibo, J. Z.; Zambaldi, V.; Lanctot, M.; Marecki, J.; and Graepel, T. 2017. Multi-agent reinforcement learning in sequential social dilemmas. _arXiv preprint arXiv:1702.03037_ . 

Lowe, R.; Wu, Y.; Tamar, A.; Harb, J.; Abbeel, P.; and Mordatch, I. 2017. Multi-agent actor-critic for mixed cooperative-competitive environments. _arXiv preprint arXiv:1706.02275_ . 

Lyu, X.; Xiao, Y.; Daley, B.; and Amato, C. 2021. Contrasting centralized and decentralized critics in multi-agent reinforcement learning. _arXiv 2102.04402_ . 

Lyu, X.; Baisero, A.; Xiao, Y.; and Amato, C. 2022. A deeper understanding of state-based critics in multi-agent reinforcement learning. In _Proceedings of the AAAI conference on artificial intelligence_ , volume 36, 9396–9404. 

Lyu, X.; Baisero, A.; Xiao, Y.; Daley, B.; and Amato, C. 2023. On centralized critics in multi-agent reinforcement learning. _Journal of Artificial Intelligence Research_ 77:295– 354. 

Lyu, X.; Baisero, A.; Xiao, Y.; Daley, B.; and Amato, C. 2024. On centralized critics in multi-agent reinforcement learning. _arXiv 2408.14597_ . 

Mnih, V.; Kavukcuoglu, K.; Silver, D.; Rusu, A. A.; Veness, J.; Bellemare, M. G.; Graves, A.; Riedmiller, M.; 

Fidjeland, A. K.; Ostrovski, G.; et al. 2015. Humanlevel control through deep reinforcement learning. _Nature_ 518(7540):529–533. 

Mordatch, I., and Abbeel, P. 2017. Emergence of grounded compositional language in multi-agent populations. _arXiv preprint arXiv:1703.04908_ . 

Oliehoek, F. A.; Spaan, M. T. J.; and Vlassis, N. 2008. Optimal and approximate Q-value functions for decentralized POMDPs. 32:289–353. 

Omidshafiei, S.; Pazis, J.; Amato, C.; How, J. P.; and Vian, J. 2017. Deep decentralized multi-task multi-agent rl under partial observability. _arXiv preprint arXiv:1703.06182_ . 

Peng, P.; Yuan, Q.; Wen, Y.; Yang, Y.; Tang, Z.; Long, H.; and Wang, J. 2017. Multiagent bidirectionally-coordinated nets for learning to play starcraft combat games. _arXiv preprint arXiv:1703.10069_ . 

Proper, S., and Tumer, K. 2012. Modeling difference rewards for multiagent learning. In _Proceedings of the 11th International Conference on Autonomous Agents and Multiagent Systems-Volume 3_ , 1397–1398. International Foundation for Autonomous Agents and Multiagent Systems. 

Schulman, J.; Moritz, P.; Levine, S.; Jordan, M. I.; and Abbeel, P. 2015. High-dimensional continuous control using generalized advantage estimation. _CoRR_ abs/1506.02438. 

Weaver, L., and Tao, N. 2001. The optimal reward baseline for gradient-based reinforcement learning. In _Proceedings of the Seventeenth conference on Uncertainty in artificial intelligence_ , 538–545. Morgan Kaufmann Publishers Inc. 

Weyns, D.; Helleboogh, A.; and Holvoet, T. 2005. The packet-world: A test bed for investigating situated multiagent systems. In _Software Agent-Based Applications, Platforms and Development Kits_ . Springer. 383–408. 

Williams, R. J. 1992. Simple statistical gradient-following algorithms for connectionist reinforcement learning. _Machine learning_ 8(3-4):229–256. 

Wolpert, D. H., and Tumer, K. 2002. Optimal payoff functions for members of collectives. In _Modeling complexity in economic and social systems_ . World Scientific. 355–369. 

Yang, E., and Gu, D. 2004. Multiagent reinforcement learning for multi-robot systems: A survey. Technical report, tech. rep. 

Ye, D.; Zhang, M.; and Yang, Y. 2015. A multi-agent framework for packet routing in wireless sensor networks. _sensors_ 15(5):10026–10047. 

Ying, W., and Dayong, S. 2005. Multi-agent framework for third party logistics in e-commerce. _Expert Systems with Applications_ 29(2):431–436. 

Shoham, Y., and Leyton-Brown, K. 2009. _Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations_ . New York: Cambridge University Press. 

Sukhbaatar, S.; Fergus, R.; et al. 2016. Learning multiagent communication with backpropagation. In _Advances in Neural Information Processing Systems_ , 2244–2252. 

Sutton, R. S.; McAllester, D. A.; Singh, S. P.; Mansour, Y.; et al. 1999. Policy gradient methods for reinforcement learning with function approximation. In _NIPS_ , volume 99, 1057–1063. 

Sutton, R. S. 1988. Learning to predict by the methods of temporal differences. _Machine learning_ 3(1):9–44. 

Synnaeve, G.; Nardelli, N.; Auvolat, A.; Chintala, S.; Lacroix, T.; Lin, Z.; Richoux, F.; and Usunier, N. 2016. Torchcraft: a library for machine learning research on realtime strategy games. _arXiv preprint arXiv:1611.00625_ . 

Tampuu, A.; Matiisen, T.; Kodelja, D.; Kuzovkin, I.; Korjus, K.; Aru, J.; Aru, J.; and Vicente, R. 2015. Multiagent cooperation and competition with deep reinforcement learning. _arXiv preprint arXiv:1511.08779_ . 

Tan, M. 1993. Multi-agent reinforcement learning: Independent vs. cooperative agents. In _Proceedings of the tenth international conference on machine learning_ , 330–337. 

Tumer, K., and Agogino, A. 2007. Distributed agent-based air traffic flow management. In _Proceedings of the 6th international joint conference on Autonomous agents and multiagent systems_ , 255. ACM. 

Usunier, N.; Synnaeve, G.; Lin, Z.; and Chintala, S. 2016. Episodic exploration for deep deterministic policies: An application to starcraft micromanagement tasks. _arXiv preprint arXiv:1609.02993_ . 

## **A Proof of Lemma 1** 

The COMA gradient is given by 

**==> picture [345 x 31] intentionally omitted <==**

**==> picture [328 x 11] intentionally omitted <==**

where _θ_ are the parameters of all actor policies, e.g., _θ_ = _{θ_[1] _, . . . , θ[|][A][|] }_ , and _b_ ( _s,_ _**τ** ,_ **u** _[−][a]_ ) is the counterfactual baseline defined in equation 4. 

First consider the expected contribution of the baseline: 

**==> picture [439 x 125] intentionally omitted <==**

**==> picture [427 x 10] intentionally omitted <==**

where _**τ**[−][a]_ is the joint action-observation history of all agents except _a_ , and _**π**[−][a]_ is the joint policy of all agents except _a_ . Clearly, the per-agent baseline, although it may reduce variance, does not change the expected gradient, and therefore does not affect the convergence of COMA. The key feature of the counterfactual baseline which allows this property is the independence for agent _a_ on the action _u[a]_ . 

The remainder of the expected policy gradient is given by: 

**==> picture [341 x 64] intentionally omitted <==**

By writing the joint policy as the product of the independent actors, 

**==> picture [304 x 22] intentionally omitted <==**

we can rewrite (15) as: 

**==> picture [325 x 11] intentionally omitted <==**

Furthermore, we can reinterpret _**π**_ as a single-agent policy in a corresponding MDP _M_ = _⟨Sm, Um, Pm, rm, γ⟩_ where, 

• _Sm_ = _S ×_ **T** ; 

- _Um_ = **U** ; 

• _Pm_ ( _s[′] m[|][s][m]_[)][=] _[P]_[(] _[s][′][,]_ _**[ τ]**[ ′][|][s,]_ _**[ τ]**_[)][=] _[P]_[(] _[s][′][|][s]_[)][1][=][(] **[z]** _[′][,]_ **[ z]**[)][,][where] _**[τ]**[ ′]_[is] _**[τ]**_[extended][with] **[z]** _[′]_[,] **[z]**[=][[] _[O]_[(] _[s][′][,]_[ 1)] _[, . . . , O]_[(] _[s][′][, n]_[)]][,][and] 1=( **z** _[′] ,_ **z** ) = 1 iff **z** _[′]_ = **z** ; and 

• _rm_ (( _s,_ _**τ**_ ) _,_ **u** ) = _r_ ( _s,_ **u** ). 

The gradient _g_ in the stochastic game _G_ corresponds to the standard policy gradient gradient in _M_ : 

**==> picture [342 x 11] intentionally omitted <==**

where _πm_ ( _um|sm_ ) = _πm_ ( _um|s,_ _**τ**_ ) = _**π**_ ( **u** _|_ _**τ**_ ), i.e., _πm_ follows the policy in (16), foregoing the option of depending on _s_ . Sutton et al. (1999) prove that an actor-critic following this gradient converges to a local maximum of the expected return, given several assumptions, including: 

1. the MDP has bounded rewards; 

2. the policy is differentiable; 

3. the critic is trained against unbiased targets, as in TD(1); 

4. the critic has converged to a local optimum before each policy gradient is estimated; and 

5. the critic uses a representation compatible with the policy. 

The policy parameterisation (i.e., the single-agent joint-action learner is decomposed into independent actors) is immaterial to convergence, as long as it remains differentiable. 

## **B Training Details and Hyperparameters** 

Training is performed in batch mode, with a batch size of 30. Due to parameter sharing, all agents can be processed in parallel, with each agent for each episode and time step occupying one batch entry. The training cycle progresses in three steps (completion of all three steps constitutes as one episode in our graphs): 1) _collect data_ : collect[30] _n_[episodes; 2)] _[ train critic]_[: for each] time step, apply a gradient step to the feed-forward critic, starting at the end of the episode; and 3) _train actor_ : fully unroll the recurrent part of the actor, aggregate gradients in the backward pass across all time steps, and apply a gradient update. 

We use a target network for the critic, which updates every 150 training steps for the feed-forward centralised critics and every 50 steps for the recurrent IAC critics. The feed-forward critic receives more learning steps, since it performs a parameter update for each timestep. Both the actor and the critic networks are trained using RMS-prop with learning rate 0 _._ 0005 and alpha 0 _._ 99, without weight decay. We set gamma to 0 _._ 99 for all maps. 

Although tuning the skip-frame in StarCraft can improve absolute performance (Peng et al. 2017), we use a default value of 7, since the main focus is a relative evaluation between COMA and the baselines. 

## **C Algorithm** 

**Algorithm 1** Counterfactual Multi-Agent (COMA) Policy Gradients 

Initialise _θ_ 1 _[c]_[,] _[θ]_[ˆ] 1 _[c][, θ][π]_ **for** each training episode _e_ **do** Empty buffer **for** _ec_ = 1 **to**[BatchSize] _n_ **do** _s_ 1 = initial state, _t_ = 0, _h[a]_ 0[=] **[ 0]**[ for each agent] _[ a]_ **while** _st_ = terminal **and** _t < T_ **do** _t_ = _t_ + 1 **for** each agent _a_ **do** _h[a] t_[=][ Actor] � _o[a] t[, h][a] t−_ 1 _[, u][a] t−_ 1 _[, a, u]_[;] _[ θ][i]_ � Sample _u[a] t_[from] _[ π]_[(] _[h][a] t[, ϵ]_[(] _[e]_[))] Get reward _rt_ and next state _st_ +1 Add episode to buffer Collate episodes in buffer into single batch **for** _t_ = 1 **to** _T_ **do** // from now processing all agents in parallel via single batch Batch unroll RNN using states, actions and rewards Calculate TD( _λ_ ) targets _yt[a]_[using] _[θ]_[ˆ] _i[c]_ **for** _t_ = _T_ **down to** 1 **do** ∆ _Q[a] t_[=] _[ y] t[a][−][Q]_ � _s[a] j[,]_ **[ u]** � ∆ _θ[c]_ = _∇θc_ (∆ _Q[a] t_[)][2][ // calculate critic gradient] _θi[c]_ +1[=] _[ θ] i[c][−][α]_[∆] _[θ][c]_[ // update critic weights] Every C steps reset _θ_[ˆ] _i[c]_[=] _[ θ] i[c]_ **for** _t_ = _T_ **down to** 1 **do** _A[a]_ ( _s[a] t[,]_ **[ u]**[) =] _[ Q]_[(] _[s][a] t[,]_ **[ u]**[)] _[ −]_[�] _u[Q]_[(] _[s] t[a][, u,]_ **[ u]** _[−][a]_[)] _[π]_[(] _[u][|][h][a] t_[)][ // calculate COMA] ∆ _θ[π]_ = ∆ _θ[π]_ + _∇θπ_ log _π_ ( _u|h[a] t_[)] _[A][a]_[(] _[s][a] t[,]_ **[ u]**[)][ // accumulate actor gradients] _θi[π]_ +1[=] _[ θ] i[π]_[+] _[ α]_[∆] _[θ][π]_[// update actor weights] 

