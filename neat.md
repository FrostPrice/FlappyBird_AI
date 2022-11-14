# NEAT_Python

NEAT will change the values of the weights in the Neuron Network, and even add randomly nodes to try to define a Architecture/Topology for the Neuron Network that bests resolve the presented problem

---

### Components

1º Inputs: It how the data will be inserted into the Neuron Network. The information we're going to add is the Bird Y axis, the distance between the bird and the next comming TOP & BOTTOM pipe

2º Output: It's the solution the AI found for the problem. In this case will be Jump or Do NOT Jump

3º Activation Funcion: Will be the function used to evaluate/determine the Output. Neat may choose this automatically if you want. In the FlappyBird will be used the TanH Function.
The TanH function will make it possible to make all the values be between 1 and -1 in the Y axis, making it easy to define if the bird should jump or not

4º Population Size: Amount of Birds running in each generation. We'll use 100 birds. Each generation will use the best birds in the last generation

5º Fitness Function: Most important part of the NEAT algorithm. It's basically how the Birds will improve themselves and evaluate how good the Birds really are. In this case will be the birds that moves the further on the game without hitting a pipe (or without losing)

6º Max Generations: Amount of generations for the AI to train, just like the Epochs in the Kera Module. We'll use 30 generations

---

### Neat_Config:

- **fitness_criterion:** Determine how we get rid of the worst Birds (max)
- **fitness_threshold:** If some Bird reach this threshold of fitness level, the program will end. Since the Bird will go forever in the game
- **pop_size:** Population Size
- **reset_on_extinction:** Each generation can have species, and if all specie goes extinct it will either create a new randon specie (True), or throw an exception (False)
- **Genome:** Diferent Populations are called Genomes, They can have Nodes (Like input and output Nodes), and Genes that are the connections between theses Nodes
- **activation_mutate_rate:** The percentage on which the activation function will change
- **activation_options:** Used by the activation_mutate_rate to chose the activation functions
- **bias**: These are the values to chose for the Nodes.
- **bias_max_value & bias_min_value:** Determine the initial weight of the nodes, and they will not be higher than the max or lower than the min
- **bias_mutate_power & bias_mutate_rate & bias_replace_rate:** The chance of when things will change on each generation and on each population
- **conn_add_prob & conn_delete_prob:** The percentage that a new connection will be create or a connection will be deleted
- **enabled_default:** The connections between nodes can be Enable or Disable
- **enabled_mutate_rate:** The chance that a connection can be Deativated or Activated
- **feed_forward:** Tells if the Neuron Network is Feed Forward, meaning that it's Nodes doesn't create a cicled connection
- **initial_connection:** Determine the inital connection when the Nodes are created
- **node_add_prob & node_delete_prob**: The probability that a Node will be added or deleted
- **num_hidden:** The amount of Hidden Nodes
- **num_inputs:** The amount of Input Nodes
- **num_outputs:** The amount of Output Nodes
- **species_fitness_func:** Compute the species fitness
- **max_stagnation:** The amount of generations to go without increasing the fitness
