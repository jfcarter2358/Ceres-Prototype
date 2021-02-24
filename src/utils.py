def merge_lists(A, B):
    out = []
    for i in range(0, len(A)):
        if len(B) == 0:
            out += A[i:]
            break
        while B[0] < A[i]:
            out.append(B[0])
            B.pop(0)
            if len(B) == 0:
                out += A[i:]
                break
        out.append(A[i])
    out += B
    return out

def extract_from_id(id):
    parts = id.split(':')
    return int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])