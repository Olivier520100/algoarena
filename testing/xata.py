import base64

with open(f"rec_cp1qgir4f9p514bq67f0.mp4", "rb") as f:

    encodedvideo1 = base64.standard_b64encode(f.read())

a = base64.standard_b64encode(encodedvideo1)
print(type(a))
b = str(a).encode("utf-8")
c = bytes(b)
d = base64.standard_b64decode(c)

