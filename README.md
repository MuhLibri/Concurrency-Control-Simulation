# Tugas Besar 1 IF3140 Manajemen Basis Data 2023 - Concurrency Control
In this repository, there are two concurency control: Two-Phase Locking (2PL) and Optimistic Concurrency Control (OCC)

## Requirements
1. Python

## How To run
1. Make `.txt` file containing the schedule in the input folder. Example can be seen on `tc1.txt`-`tc5.txt`
2. Ganti text pada readfile sesuai dengan nama file
3. Open terminal in the root folder of this repository
4. Type `python main.py`

## Valid Input
- R`transaction number`(`data`)
- W`transaction number`(`data`)
- C`transaction number`

example: `R1(A); R2(B); W1(B); C2; C1`
