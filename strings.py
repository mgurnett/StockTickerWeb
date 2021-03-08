txt = "banana,,,,,ssqqqww....."

x = txt.rstrip(",.qsw")

print(x)

stock = "Apple Inc. (AAPL)"

y = stock.rstrip("(.qsw")

print(y)

z = stock.index("(")

print(z)

txt = "apple, banana, cherry"

x = txt.rsplit(", ")

print(x)