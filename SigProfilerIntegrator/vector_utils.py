from numpy import dot
from numpy.linalg import norm
from numpy import ndarray

def cos_sim(a:list[float], b:list[float]) -> float:
    """Returns the cosine similaity between two lists of floats."""
    return dot(a, b)/(norm(a)*norm(b))

def vector_sum(vectors:list[list[float]]) -> list[float]:
    """Returns the sum of the given vectors"""
    return [sum(dim) for dim in zip(*vectors)]

def vector_norm(vector:list[float]) -> list[float]:
    return vector / norm(vector)

def combine_similar(vectors:list[list[float]], cos_sim_threshold:float) -> dict[tuple[int],list[float]]:
    """
    Description
    ---
    Combines vectors that have have a cosine similarity that is larger or equal
    to the given threshold. A dictionary is returned. Its keys are tuples containing integers matching
    the positions of vectors in the input list, and its values are are summed vectors.

    Parameters
    ---
    vectors : list[list[float]]
    cos_sim_threshold : float
        Float value between -1 and 1. Vectors with a similarity below the threshold are not combined.
    """

    # Calculate the cosine similarity between all vectors
    similarities = {
        (i,j): cos_sim(vectors[i],vectors[j]) 
        for i in range(len(vectors))
        for j in range(len(vectors))
        if i < j
        }
    
    v_simset_map = {i: i for i in range(len(vectors))}
    simsets = {i: {i} for i in range(len(vectors))}

    for sig_set_kv in sorted(similarities.items(), key=lambda x: x[1]):
        v_ids, v_similarity = sig_set_kv
        v_i, v_j = v_ids
        # Similarity-set of similar vectors are combined
        if v_similarity < cos_sim_threshold:
            continue

        # Continue if vectors are already part of the same similiarity set
        if v_simset_map[v_i] == v_simset_map[v_j]:
            continue

        simsets[v_simset_map[v_i]] = simsets[v_simset_map[v_i]] | simsets[v_simset_map[v_j]]
        simsets[v_simset_map[v_j]] = set()
        for v_id in simsets[v_i]:
            v_simset_map[v_id] = v_simset_map[v_i]

    out = dict()
    for simset_id in sorted(v_simset_map.values()):
        simset = simsets[simset_id]
        combined_key = tuple(sorted(list(simset)))
        if combined_key in out or combined_key == tuple():
            continue
        summed_vectors = vector_sum(
            [vectors[i] for i in simset]
        )
        out[combined_key] = summed_vectors
    
    return out