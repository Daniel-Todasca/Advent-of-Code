from src.helper import IO


arr = [int(line) for line in IO.read_all()]
# sum_product = {x+y: x*y for x in arr for y in arr}
sum_product = {x+y+z: x*y*z for x in arr for y in arr for z in arr}
IO.write(sum_product[2020])
