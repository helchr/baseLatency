#!/usr/bin/python3

import sqlite3 as lite
import glob
import sys
import statistics 

def getLatAndCount(filename,level):
  qLat = """select avg(weight), count(*) from samples where memory_level = """ + str(level) + """ and memory_opcode = 2
  and symbol_id = (select id from symbols where name like "%PermRead64UnrollLoop%")""" 
  con = lite.connect(filename, timeout=30)
  con.execute("PRAGMA journal_mode = memory")
  con.execute("PRAGMA synchronous = off")
  cur = con.cursor()
  cur.execute(qLat)
  data = cur.fetchall()
  return data[0][0], data[0][1]

def calcStats(files,memory):
  if memory == "Local":
    level = 16
  elif memory == "Remote":
    level = 32
  else:
    print("Error: Unknown memory level")
    exit()

  lats=[]
  counts=[]
  for filename in files:
    lat,count = getLatAndCount(filename,level)
    lats.append(lat)
    counts.append(count)
    
  print(memory+":")
  print("Latency =",round(statistics.mean(lats),1))
  print("Latency Standard Deviation =",round(statistics.stdev(lats),1))
  print("Number of Repetitions =",len(counts))
  print("Total Samples =",sum(counts))
  print("Average Samples =",round(statistics.mean(counts),1))
  print("\n")


files = glob.glob(sys.argv[1]+"/*.db")
sumData=[0,0,0]
calcStats(files,"Local")
calcStats(files,"Remote")


