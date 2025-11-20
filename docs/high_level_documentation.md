# Introduction

This document details a high-level overview of the current strategy and architecture of our system. It is intended to act as a guide for stakeholders, developers, and new team members to understand the core components and their interactions.

## 1. Purpose

This system aims to streamline the process of data collection, storage, and retrieval of various assets. In other words, it is designed to efficiently retrieve similar CADs based on user-provided sketches and tags.

## 2. Data Collection

We are planning to develop a streamlit application that will facilitate the collection of data through interactive forms. This application will allow users to input data in a structured manner, ensuring *consistency* and *accuracy*.
We are mainly focused on collecting the following for each asset:

- Sketches: Hand-drawn or digital sketches received from the client.
- Tags: Keywords or labels that describe the asset's characteristics.
- CADs: Final CAD output file which was designed and delivered to the client.
- Metadata: Additional information such as creation date, author, and version.

## 3. Data Storage

The collected data will be stored in a MongoDB database. MongoDB is chosen for its flexibility in handling unstructured data and its scalability. Each asset will be stored as a document in a collection, with fields corresponding to the collected data types.

## 4. Designing a Library for Retrieval

To facilitate the retrieval of similar CADs based on user-provided sketches and tags, we will design a library that implements efficient search algorithms. We are collecting sketches (separate file per view), tags, and CADs (separate file per view) for each asset. The idea is to create a shared embedding space for both sketches and CADs such that similar sketches and CADs are close to each other in this space. This will allow us to perform similarity searches based on user-provided sketches and tags.

### 4.1 Data Preparation

For each asset, we receive the following triplet set $\{\mathcal{S}, \mathcal{T}, \mathcal{C}\}$, where:

- $\mathcal{S}$: Set of sketch views. $\{\mathcal{S}_1, \mathcal{S}_2, \ldots, \mathcal{S}_n\}$
- $\mathcal{T}$: Set of tags.
- $\mathcal{C}$: Set of CAD views. $\{\mathcal{C}_1, \mathcal{C}_2, \ldots, \mathcal{C}_n\}$

Currently, there are no models which can directly create embeddings for CAD files. Therefore, we will extract rasterized images for each CAD view to get a set of images, and we would extract block, layers, and other relevant information from the CAD views to get a textual description for each CAD view.
We will be using these triplet sets to train a model that learns to map sketches and CADs into a shared embedding space. This model will be trained using contrastive learning techniques to ensure that similar sketches and CADs are close in the embedding space, while dissimilar ones are far apart.

The key components of the model would be:

- CLIP Model: We will use a pre-trained CLIP model image encoder $f$ to extract embeddings from sketches $(\mathcal{S}')$ and rasterized CAD images $(\mathcal{C}')$. We will use CLIP model text encoder $g$ to extract embeddings from the tags $(\mathcal{T}')$ and textual descriptions of CADs $(\mathcal{O}')$.

$$
f : \mathbb{R}^{3 \times H \times W} \rightarrow \mathbb{R}^{512}, \qquad f(\mathcal{S}) = \mathcal{S}'
$$

$$
g : \mathbb{R}^{3 \times H \times W} \rightarrow \mathbb{R}^{512}, \qquad g(\mathcal{T}) = \mathcal{T}'
$$

$$
f : \mathbb{R}^{3 \times H \times W} \rightarrow \mathbb{R}^{512}, \qquad f(\mathcal{C}) = \mathcal{C}'
$$

$$
g : \mathbb{R}^{3 \times H \times W} \rightarrow \mathbb{R}^{512}, \qquad g(\mathcal{O}) = \mathcal{O}'
$$

- Preparing Input Output pairs: We will combine the sketch embeddings and tag embeddings to create a per-view sketch+tag embedding. This will be used as input to the model. We will combine the rasterized CAD image embeddings and textual description embeddings to create a per-view CAD embedding. This will be used as output to the model.

$$
\{\mathcal{I}, O\} = \{(\mathcal{S}'_i, \mathcal{T}'), (\mathcal{C}'_i, \mathcal{O}'_i)\} \quad \forall i \in [1, n]
$$

- Projection Heads: We will design two projection heads, one for the input embeddings and one for the output embeddings. These projection heads will be simple feed-forward neural networks that map the embeddings to a common dimensionality suitable for computing similarity. These projection heads will be trained using contrastive loss while the CLIP encoders will be kept frozen. We will use cartesian product to get all possible input-output pairs (view-wise), and use this to train the model (one pair at a time will be treated as positive pair, while all other pairs in the batch will be treated as negative pairs).

We will be saving the CAD embeddings in a FAISS index to facilitate efficient similarity search. During retrieval, user-provided sketches and tags will be processed through the same pipeline to obtain their embeddings, which will then be used to query the FAISS index for similar CADs.

## 5. Metric

We will be using **Recall@K** as the primary metric to evaluate the performance of our retrieval system. Recall@K measures the proportion of relevant items that are successfully retrieved within the top K results. This metric is particularly useful in scenarios where the goal is to ensure that users can find relevant CADs quickly and efficiently. The actual formula for Recall@K is given by:

$$
Recall@K = \frac{\text{Number of relevant items retrieved in top K}}{\text{Total number of relevant items}}
$$

We picked this metric because in retrieval tasks, especially in scenarios like ours where users are looking for similar CADs based on sketches and tags, it is crucial to ensure that the most relevant results are presented within the top K results. A high Recall@K indicates that our system is effective in retrieving relevant CADs, thereby enhancing user satisfaction and experience. Other metrics like Precision@K or Mean Average Precision (MAP) could also be considered, but Recall@K provides a clear indication of the system's ability to retrieve relevant items, which is our primary concern.
