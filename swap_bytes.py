import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        type=str,
        dest="input_file",
        help="input file to swap bytes",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=int,
        dest="word_size",
        default=2,
        help="word size in bytes to swap (default 2)",
    )
    parser.add_argument(
        type=str,
        dest="output_file",
        help="output file with swapped bytes",
    )
    args = parser.parse_args()

    with open(args.input_file, "rb") as input, open(args.output_file, "wb") as output:
        bytes = input.read(args.word_size)
        while bytes != b"":
            output.write(bytes[::-1])
            bytes = input.read(args.word_size)


if __name__ == "__main__":
    main()
