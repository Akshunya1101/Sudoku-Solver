import csv
with open ('tested.csv') as csvfile:
  rows = csv.reader(csvfile)
  sudoku = list(zip(*rows))
  print(sudoku)

from pysat.solvers import Solver
k = int(input())
s = Solver()
clause = []

#Adding clauses of input sudoku
for j in range(k*k):
  for i in range(k*k):
    if int(sudoku[i][j])!=0:
      clause.append([i*k**4+j*k**2+ int(sudoku[i][j])])
    if int(sudoku[i][j+k*k])!=0:
      clause.append([i*k**4+j*k**2+k**6+int(sudoku[i][j+k*k])])


#All cells shall have only 1 number
for i in range(k*k):
  for j in range(k*k):
    clause.append([int(i*k**4 + j*k**2 + dig + 1) for dig in range(k*k)])
    clause.append([int(i*k**4 + j*k**2 + dig + 1 + k**6) for dig in range(k*k)])
    for dig1 in range(k*k):
      for dig2 in range(dig1+1, k*k):
        clause.append([-(i*k**4 + j*k**2 + dig1 + 1), -(i*k**4 + j*k**2 + dig2 + 1)])
        clause.append([-(i*k**4 + j*k**2 + dig1 + 1 + k**6), -(i*k**4 + j*k**2 + dig2 + 1 + k**6)])

#All columns shall have any number only once
for i in range(k*k):
  for j in range(k*k):
    clause.append([int(dig*k**4 + j*k**2 + i + 1) for dig in range(k*k)])
    clause.append([int(dig*k**4 + j*k**2 + i + 1 + k**6) for dig in range(k*k)])
    for dig1 in range(k*k):
      for dig2 in range(dig1+1, k*k):
        clause.append([-(dig1*k**4 + j*k**2 + i + 1), -(dig2*k**4 + j*k**2 + i + 1)])
        clause.append([-(dig1*k**4 + j*k**2 + i + 1 + k**6), -(dig2*k**4 + j*k**2 + i + 1 + k**6)])

#All rows shall have any number only once
for i in range(k*k):
  for j in range(k*k):
    clause.append([int(i*k**4 + dig*k**2 + j + 1) for dig in range(k*k)])
    clause.append([int(i*k**4 + dig*k**2 + j + 1 + k**6) for dig in range(k*k)])
    for dig1 in range(k*k):
      for dig2 in range(dig1+1, k*k):
        clause.append([-(i*k**4 + dig1*k**2 + j + 1), -(i*k**4 + dig2*k**2 + j + 1)])
        clause.append([-(i*k**4 + dig1*k**2 + j + 1 + k**6), -(i*k**4 + dig2*k**2 + j + 1 + k**6)])

#All cells shall have any number only once
for i in range(0, k*k, k):
  for j in range(0, k*k, k):
    for num in range(k*k):
      clause.append([int(row*k**4 + col*k**2 +num + 1) for row in range(i,i+k) for col in range(j, j+k)])
      clause.append([int(row*k**4 + col*k**2 + num + k**6 + 1) for row in range(i,i+k) for col in range(j, j+k)])
      for row1 in range(i, i+k):
        for col1 in range(j, j+k):
          for row2 in range(row1+1, i+k):
            for col2 in range(col1+1, j+k):
              clause.append([-(row1*k**4 + col1*k**2 + num + 1), -(row2*k**4 + col2*k**2 + num + 1)])
              clause.append([-(row1*k**4 + col1*k**2 + k**6 + num + 1), -(row2*k**4 + col2*k**2 + num + k**6 + 1)])

#Any cell of sudoku one cannot have same element as sudoku 2
for i in range(k**6):
  clause.append([-(i+1), -(i + k**6 + 1)])

print(clause)
s.append_formula(clause)
print(s.solve())

res=s.get_model()
print(res)
outputstr=''
if res is None:
    print("Not possible")
else:
    x=0
    for i in range(0,k**6):
        if(res[i]>0):
            if(res[i]%(k*k)>0):
                outputstr=outputstr+str(res[i]%(k*k))
            else:
                outputstr=outputstr+str(k*k)
            x=x+1
            if(x%(k*k)==0):
                outputstr=outputstr+'\n'
            else:
                outputstr=outputstr+','
    x=0
    for i in range(k**6,2*(k**6)):
        if(res[i]>0):
            if(res[i]%(k*k)>0):
                outputstr=outputstr+str(res[i]%(k*k))
            else:
                outputstr=outputstr+str(k*k)
            x=x+1
            if(x%(k*k)==0):
                outputstr=outputstr+'\n'
            else:
                outputstr=outputstr+','
with open("Output.csv", "w") as text_file:
    text_file.write(outputstr)