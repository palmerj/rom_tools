import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--inputfile",
        type=str,
        dest="infile",
        required=True,
        help="Input file",
    )
    parser.add_argument(
        "-o",
        "--outfiles",
        nargs="+",
        type=str,
        dest="outfiles",
        required=True,
        help="list of ordered files you output uninterleaved",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        dest="buffer_size",
        default=1,
        help="interleave size in bytes (default 1)",
    )
    args = parser.parse_args()

    with open(args.infile, "rb") as file:
        indata = file.read()
    if len(indata) % (len(args.outfiles) * args.buffer_size) != 0:
        raise ValueError(
            "Number of uninterleaved output files does not match the input file size"
        )

    file_objs = []
    try:
        for file in args.outfiles:
            file_objs.append(open(file, "wb"))
        i = 0
        try:
            while i < len(indata):
                for fh in file_objs:
                    fh.write(indata[i : i + args.buffer_size])
                    i += args.buffer_size
        finally:
            for fh in file_objs:
                fh.close()
    except IOError as e:
        raise IOError("Failed creating output file: " + str(e))


if __name__ == "__main__":
    main()
