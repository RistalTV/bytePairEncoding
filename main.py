import math
import os
import re
import collections

SEP = '</W>'
MAX_ROW_TABLE = 5
WIDTH = 100


def normalizeDictWords(dictWords) -> dict:
    global SEP
    result = {}
    for (word, frequency) in dictWords.items():
        word = str(word.upper().strip())
        word = word.replace(SEP, "")
        word = " ".join(word)
        if SEP not in word:
            word += " " + SEP
        result.update({word: int(frequency)})
    return result


def printTable(dataTable):
    global MAX_ROW_TABLE, WIDTH
    result = ""
    if len(dataTable) > MAX_ROW_TABLE:
        table = []
        countColumn = int(math.ceil(len(dataTable) / MAX_ROW_TABLE))
        maxCountElementsTable = MAX_ROW_TABLE * countColumn
        maxLen = len(max(dataTable, key=len))
        for numberWord in range(len(dataTable)):
            if len(dataTable[numberWord]) != maxLen:
                dataTable[numberWord] += ' ' * (maxLen - len(dataTable[numberWord]))
        if maxCountElementsTable != len(dataTable):
            for i in range(maxCountElementsTable - len(dataTable)):
                dataTable.append(' ' * maxLen)
        for column in range(countColumn):
            table.append(dataTable[column * MAX_ROW_TABLE:column * MAX_ROW_TABLE + MAX_ROW_TABLE])
        for row in range(MAX_ROW_TABLE):
            text = ""
            for column in range(countColumn):
                if column != 0:
                    text += " | "
                text += table[column][row]
            text = printWords(text=text)
            result += text if '\n' in text else text + '\n'
            result += '= ' + "-" * (WIDTH - 4) + ' =\n'
    else:

        for idx, word in enumerate(dataTable):
            text = printWords(f"{idx + 1}) {word}", 'left')
            result += text if '\n' in text else text + '\n'
    return result


def printWords(text, align='center'):
    global WIDTH
    result = ""
    widthText = WIDTH - 4
    align = align.strip().lower()
    if align == 'center':
        if len(text) > widthText:
            countIteration = len(text) / widthText
            countIteration = math.ceil(countIteration)
            countIteration = int(countIteration)
            for i in range(countIteration):
                textLine = text[i * widthText:i * widthText + widthText]
                if len(textLine) != widthText:
                    countSpace = (widthText - len(textLine))
                    if countSpace % 2 == 0:
                        countSpace = int(countSpace / 2)
                        textLine = ' ' * countSpace + textLine + ' ' * countSpace
                    else:
                        countSpace = int((countSpace - 1) / 2)
                        textLine = ' ' * countSpace + textLine + ' ' + ' ' * countSpace

                result += f"= {textLine} =\n"
        else:
            countSpace = (widthText - len(text))
            if countSpace % 2 == 0:
                countSpace = int(countSpace / 2)
                textLine = ' ' * countSpace + text + ' ' * countSpace
            else:
                countSpace = int((countSpace - 1) / 2)
                textLine = ' ' * countSpace + text + ' ' + ' ' * countSpace
            result += f"= {textLine} ="
    elif align == 'left':
        if len(text) > widthText:
            countIteration = len(text) / widthText
            countIteration = math.ceil(countIteration)
            countIteration = int(countIteration)
            for i in range(countIteration):
                textLine = text[i * widthText:i * widthText + widthText]
                if len(textLine) != widthText:
                    textLine += ' ' * (widthText - len(textLine))
                result += f"= {textLine} =\n"
        else:
            result += f"= {text}{' ' * (widthText - len(text))} ="
    else:
        result = text
    return result


def bpe_start(dictWords):
    pairs = collections.defaultdict(int)
    for (word, frequency) in dictWords.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += frequency
    return pairs


def marge_dictWords(pair, dictWords__in):
    dictWords__out = {}
    bigram = re.escape(' '.join(pair))
    pattern = re.compile(rf'(?<!\S){bigram}(?!\S)')
    for word in dictWords__in:
        word_out = pattern.sub(''.join(pair), word)
        dictWords__out[word_out] = dictWords__in[word]
    return dictWords__out


def main():
    global WIDTH, SEP
    dictWords = {
        'ЗАРОСЛИ': 2,
        'МОРЖ': 8,
        'МОРОЖЕННОЕ': 4,
        'ЛЕСОПОВАЛ': 9,
        'ЛЕС': 3,
        'ЛЕДОХОД': 7,
        'ГОРЕЦ': 23,
        'ГОРА': 7,
        'МОРОЗЫ': 4,
        'РОЗА': 2,
    }
    # dictWords = {
    #     'old': 7,
    #     'older': 3,
    #     'finest': 9,
    #     'lowest': 4,
    # }
    os.system('cls')
    print("=" * WIDTH)
    print(printWords(f"Byte Pair Encoding (BPE)"))
    print(printWords(f"By Skrebnev Leonid FITU 4-5Б"))
    print("=" * WIDTH)

    newListWords = input("new list words(yes or no)?: ")
    if 'yes' in newListWords or 'y' in newListWords:
        newListWords = {}
        while True:
            newWord = input("Enter 'word; frequency'(q - stop typing): ")
            if 'q' in newWord:
                if len(newListWords) != 0:
                    dictWords = newListWords
                break
            newWord = newWord.upper().split(';')
            if len(newWord) == 2:
                try:
                    newListWords.update({f'{newWord[0]}': int(newWord[1])})
                except Exception as e:
                    pass
    dictWords = normalizeDictWords(dictWords=dictWords)
    print("=" * WIDTH)
    print(printWords(f"list words"))
    print("=" * WIDTH)
    print(printTable(list(dictWords.keys())))
    print("=" * WIDTH)

    try:
        countIteration = int(input("How iteration?: "))
    except Exception as e:
        countIteration = 2
        print("=" * WIDTH)
        print(printWords(f"an error occurred while entering iterations so the default value was set {countIteration}",
                         'left'))
        print("=" * WIDTH)
    print("=" * WIDTH)
    for iterationNumber in range(1, countIteration + 1):
        pairs = bpe_start(dictWords=dictWords)
        best = max(pairs, key=pairs.get)
        dictWords = marge_dictWords(best, dictWords)

        print(printWords(f"iteration #{iterationNumber} token: {best}", 'left'))
    print("=" * WIDTH)


if __name__ == '__main__':
    main()
