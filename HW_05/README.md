# Сборка:
```
  * python3 parse.py $file_name
```
# Грамматика
```
 ATOM1 -> ID | ID ATOM2
 ATOM2 -> ATOM1 | (ATOM 1) | (ATOM1) ATOM2 | (( ATOM3 ))
 ATOM3 -> ID | (ATOM3)
```
  * В файле test.txt лежат тесты.
