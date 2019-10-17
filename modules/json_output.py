from json import dump

def create_mapping(ix, val, stacked=False):
    import IPython; IPython.embed(); raise
    return val.to_mapping(
        centered_array=None,
        sol=ix[0],
        image=ix[1],
        roi=ix[2],
        stacked=stacked)

def dump_json(frame, filename):
    with open(filename, 'w') as f:
        dump([
            create_mapping(i,v, stacked=i[1].startswith('stack'))
            for i,v in frame.items()
        ], f)

