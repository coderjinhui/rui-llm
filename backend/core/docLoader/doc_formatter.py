from langchain_community.document_loaders import ImageCaptionLoader

img = ImageCaptionLoader(images=[
    "images/0e8ab27900ed67ac578d111f38366f02.png"
])
doc = img.load()
print(doc)