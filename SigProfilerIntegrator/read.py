import os

def read_signatures(signatures_txt_path:str) -> dict:
    """
    Returns a dataframe with "MutationType" and signature identifiers as keys
    """
    cols = None
    with open(signatures_txt_path, "rt") as f:
        for line in f.readlines():
            line = line.removesuffix("\n")
            fields = line.split("\t")
            if cols is None and fields[0] == "MutationType":
                cols = fields
                out = {c:list() for c in cols}

            elif cols is None:
                raise ValueError("Signatures text-file does not match expected format.")

            else:
                for c,f in zip(cols, fields):
                    if c != "MutationType":
                        f = float(f)
                    out[c].append(f)
    
    return out

def get_signatures_txt_path(extraction_path:str, context_type:str, solution:int=None) -> str:
    """
    Returns the path of the signatures text-file for a given SigProfilerExtractor
    output directory, context_type (i.e. SBS96 or SBS1536).
    If no solution is chosen (int from 1-n_extraction_iterations), the suggested solution is used.
    """
    if solution is not None:
        try:
            assert isinstance(solution, int)
            assert solution >= 1
        except AssertionError:
            raise ValueError("solution must be int of at least 1, up to the number of iterations of the chosen extraction run (inclusive).")
    
        out = os.path.join(
            extraction_path,
            context_type,
            "All_Solutions",
            context_type+"_"+str(solution)+"_Signatures",
            "Signatures",
            context_type+"_S"+str(solution)+"_Signatures.txt"
        )

    else:
        out = os.path.join(
            extraction_path,
            context_type,
            "Suggested_Solution",
            context_type+"_De-Novo_Solution",
            "Signatures",
            context_type+"_De-Novo_Signatures.txt"
        )

    if not os.path.isfile(out):
        raise ValueError("The signatures text-file does not exist in the expected location: "+out)
    
    return out