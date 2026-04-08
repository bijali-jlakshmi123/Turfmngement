def fix_images():
    path = "templates/Owner/index.html"
    with open(path, "r", encoding="utf-8") as f:
        data = f.read()

    data = data.replace(r"\'", "'")

    with open(path, "w", encoding="utf-8") as f:
        f.write(data)

if __name__ == "__main__":
    fix_images()
    print("Done")
