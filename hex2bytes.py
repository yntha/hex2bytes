import sys
import math
import re

from argparse import ArgumentParser, Namespace
from pathlib import Path


# change this number to change the indent size for the whole program
INDENT_SIZE = 4


def main(args: Namespace):
    if args.row_width % args.group_size:
        raise Exception("Column size must be a multiple of row width.")

    data = bytes.fromhex(args.hex_string)
    code = args.var_name + f"bytes.fromhex(  # size: {hex(len(data))}({len(data)}) bytes\n"

    # get the word size of data, then multiply by two to get the total number of nibbles in the word size
    data_nibbles = int((2 ** math.ceil(math.log2(len(data).bit_length() / 8))) * 2)

    last_line_len = 0

    d, m = divmod(len(data), args.row_width)
    chunks = []

    for i in range(d):
        chunks.append(data[i * args.row_width:(i + 1) * args.row_width])

    if m:  # add the remaining bytes as the final row
        chunks.append(data[d * args.row_width:])

    for i in range(len(chunks)):
        row = (" " * INDENT_SIZE) + '"'

        for j, b in enumerate(chunks[i]):
            if j != 0 and j % args.group_size == 0:
                row += " "
            row += "%02x" % b

        if len(row) < last_line_len:
            row += " " * (last_line_len - len(row))


        last_line_len = len(row)
        code += row + '"'

        if args.ascii or args.offsets:
            code += "  # "

            if args.ascii:
                for b in chunks[i]:
                    if b < 0x7f and b >= 0x20:
                        code += chr(b)
                    else:
                        code += "."

                if args.offsets:
                    if len(chunks[i]) != args.row_width:
                        code += " " * (args.row_width - len(chunks[i]))

                    code += " | "

            if args.offsets:
                offset = i * args.row_width
                code += f"0x{offset:0{data_nibbles}x}"

        code += "\n"

    code += ")"

    indent = ((" " * INDENT_SIZE) * args.indent_level)
    code = ''.join([indent + line + "\n" for line in code.split("\n")])

    print(code)


def sanitize_hex_string(hexstr: str) -> str:
    hexstr = hexstr.replace("0x", "")

    return re.sub(
        "[^a-fA-F0-9]",
        "",
        hexstr
    )


def parse_file_info(file_info: str) -> tuple[str, int, int]:
    file_path = file_info.rsplit(":", 1)

    if len(file_path) == 1:
        return (file_path[0], 0, 0)

    match = re.match(r"^(?:([a-fA-F0-9x]+))?(?:\[([a-fA-F0-9x]+)\])?$", file_path[1])

    if match is None:
        raise Exception("Failed to parse file info. Did you specify the offset and length correctly?")

    return (file_path[0], *match.groups())


def get_hex_from_file(file_info: str) -> tuple[str, int]:
    file_path, offset, length = parse_file_info(file_info)
    file_path = Path(file_path)

    if offset is not None and offset.startswith("0x"):
        offset = int(offset, base=16)
    elif offset is not None:
        offset = int(offset)
    else:
        offset = 0

    if length is not None and length.startswith("0x"):
        length = int(length, base=16)
    elif length is not None:
        length = int(length)
    else:
        length = 0

    if not file_path.is_file():
        raise Exception("File does not exist or is not a file.")

    file_data: bytes = file_path.read_bytes()

    if len(file_data) < offset:
        raise Exception("Offset goes past file size.")

    if len(file_data) < (offset + length):
        raise Exception("Length goes past file size.")

    stop = (offset + length) if length else None
    return (file_data[offset:stop].hex(), offset)


def parse_args() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "-g",
        help="how many bytes per column",
        type=int,
        metavar="",
        default=2
    )

    parser.add_argument(
        "-w",
        help="how many bytes per row",
        type=int,
        metavar="",
        default=16
    )

    parser.add_argument(
        "-i",
        help="indent the output by NUM indentations",
        type=int,
        metavar="NUM",
        default=0
    )

    parser.add_argument(
        "-o",
        help="display offsets",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "-v",
        help="variable name to assign the bytes to",
        type=str,
        metavar="",
        default=""
    )

    parser.add_argument(
        "--ascii",
        help="display an ascii dump at the end of each row",
        action="store_true",
        default=False
    )

    parser.add_argument(
        "hex_or_file",
        help="string of hex encoded bytes to convert or a file path + offset in the format file:offset[length]. length is optional",
        type=str
    )

    args = parser.parse_args()

    if not re.match(r"^[a-fA-F0-9x ]+$", args.hex_or_file):
        file_data, offset = get_hex_from_file(args.hex_or_file)

        if offset != 0 and len(args.v) == 0:
            args.v = "_" + hex(offset)

        args.hex_or_file = file_data
    else:
        args.hex_or_file = sanitize_hex_string(args.hex_or_file)

    if len(args.v) > 0:
        args.v += " = "

    return Namespace(
        group_size = args.g,
        row_width = args.w,
        indent_level = args.i,
        offsets = args.o,
        ascii = args.ascii,
        var_name = args.v,
        hex_string = args.hex_or_file
    )


if __name__ == "__main__":
    main(parse_args())