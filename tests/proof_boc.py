import base64

from tonpylib.boc.builder import Builder
from tonpylib.boc.cell import Cell
from tonpylib.boc.exotic import check_proof, ProofError


boc = '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'

cell = Cell.one_from_boc(boc)
print(cell)
check_proof(cell, bytes.fromhex('1C1AF013CD33BA617C0DB1057F19AF136761FB433340BA038B1D4A4D4A61AEE4'))
print('passed')
try:
    check_proof(cell, bytes.fromhex('2C1AF013CD33BA617C0DB1057F19AF136761FB433340BA038B1D4A4D4A61AEE4'))
except ProofError:
    print('passed')
