import re

def main():
    pattern = re.compile(r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\w{3}[-\.\s]??\w{4}')
    input = open("test.txt", "r")
    textToBeChanged = input.read()

    results = pattern.findall(textToBeChanged)
    for i in results:
        print(i.replace("-", "."))
        # print(i)

        # print(matches)
        # for match in matches:
        #     print(match)


if __name__ == "__main__":
    main()