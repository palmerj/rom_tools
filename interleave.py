import os
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-f",
        "--files",
        nargs="+",
        type=str,
        dest="infiles",
        required=True,
        help="list of ordered files you wish to interleave",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        dest="buffer_size",
        default=1,
        help="interleave size in bytes (default 1)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        dest="output_file",
        required=True,
        help="interleaved output file",
    )
    args = parser.parse_args()
    file_data = []
    last_size = None
    for file in args.infiles:
        if not os.path.isfile(file):
            raise IOError("{0} does not exist or is not accessible".format(file))
        file_size = os.path.getsize(file)
        if last_size and last_size != file_size:
            raise ValueError(
                "File {0} size ({1}) is not uniform with other files".format(
                    file, file_size
                )
            )
        last_size = file_size
        with open(file, "rb") as fs:
            file_data.append(fs.read())
    with open(args.output_file, "wb") as outfile:
        i = 0
        while i < last_size:
            for data in file_data:
                outfile.write(data[i : i + args.buffer_size])
            i += args.buffer_size


if __name__ == "__main__":
    main()
