# hex2bytes
Convert any hex string into a formatted python bytes object.

## Usage and Examples
**ELF Header:**
```
$ python hex2bytes.py -v hdr -g 1 --ascii 7f454c460201010000000000000000000300b700010000000070850000000000400000000000000098367b02000000000000000040003800070040001800
hdr = bytes.fromhex(
    "7f 45 4c 46 02 01 01 00 00 00 00 00 00 00 00 00"  # .ELF............
    "03 00 b7 00 01 00 00 00 00 70 85 00 00 00 00 00"  # .........p......
    "40 00 00 00 00 00 00 00 98 36 7b 02 00 00 00 00"  # @........6{.....
    "00 00 00 00 40 00 38 00 07 00 40 00 18 00      "  # ....@.8...@...
)
```

**AArch64 Instructions:**
```
$ python hex2bytes.py -v insns -i 2 -g 2 --ascii e063029121018052f381fc97e10300aa60f7009000c0399167c3fb97e0630291f54efc97e0f4009002f500b0006c40f9420447f961f7009021c03991c650fc9
7e0a30291e1030032e2031faab6dcfc97e0a3029141018052df81fc97e10300aa60f7009000003a9153c3fb97
        insns = bytes.fromhex(
            "e063 0291 2101 8052 f381 fc97 e103 00aa"  # .c..!..R........
            "60f7 0090 00c0 3991 67c3 fb97 e063 0291"  # `.....9.g....c..
            "f54e fc97 e0f4 0090 02f5 00b0 006c 40f9"  # .N...........l@.
            "4204 47f9 61f7 0090 21c0 3991 c650 fc97"  # B.G.a...!.9..P..
            "e0a3 0291 e103 0032 e203 1faa b6dc fc97"  # .......2........
            "e0a3 0291 4101 8052 df81 fc97 e103 00aa"  # ....A..R........
            "60f7 0090 0000 3a91 53c3 fb97          "  # `.....:.S...
        )
```

**C String:**
```
$ python hex2bytes.py -v insns -w 8 -g 1 --ascii 4a6176615f636f6d5f496e766f6b6548656c7065725f4163636f756e744163636573734b657900
insns = bytes.fromhex(
    "4a 61 76 61 5f 63 6f 6d"  # Java_com
    "5f 49 6e 76 6f 6b 65 48"  # _InvokeH
    "65 6c 70 65 72 5f 41 63"  # elper_Ac
    "63 6f 75 6e 74 41 63 63"  # countAcc
    "65 73 73 4b 65 79 00   "  # essKey.
)
```

**Android Dex File Header:**
```
$ python hex2bytes.py 6465780A30333500A08D
bytes.fromhex(
    "6465 780a 3033 3500 a08d"
)
```