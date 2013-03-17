entropie
========

Tool to calculate entropy on files


Usage
=====
NAME
  entropie.py

SYNOPSIS
  entropie.py [OPTIONS] FILE1 FILE2...

DESCRIPTION
  Calculates the shannon entropy of a file.

OPTIONS
  -h, --help
    This Help

  -l, --line
    Calculates the entropy of each line

  -b, --block
    Calculates the entropy of each bloc (16 bytes by default)

  -s SIZE, --size=SIZE
    Sets the block size to SIZE in bytes (16 bytes by default)

  -m METHOD, --method=METHOD
    Determines how to calculate the probabilities of the elements. METHOD
    can be 'local' or 'global'. If set to local (default) the probabilities
    are evaluated at each calculation. If set to global the probabilities
    are evaluated once with the whole file.

  -e, --entropy
    Outputs only the entropy (the number)


EXAMPLES
  entropie.py -l entropie.py
  entropie.py -s 32 -b -m local entropie.py
