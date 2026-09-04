# 自定义3句英文
text = """
Python is a powerful programming language. It is easy to learn and use. 
Many people love Python because it is simple and versatile. 
Python can be used for web development, data science, and artificial intelligence.
"""

# 1. 清洗标点符号
cleaned_text = text.replace(",", " ").replace(".", " ").replace("\n", " ")
# 也可以加上其他标点：replace("!", " ").replace("?", " ")

# 2. 分割成单词列表（转小写统一）
words = cleaned_text.lower().split()

# 3. 统计词频
word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1

# 4. 按次数降序排序
sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)

# 5. 输出Top 10
print("=" * 40)
print("词频统计 Top 10")
print("=" * 40)
print(f"{'单词':<15} {'出现次数':>10}")
print("-" * 40)

for i, (word, count) in enumerate(sorted_words[:10], 1):
    print(f"{i:2}. {word:<15} {count:>10}")

print("=" * 40)

"""
========================================
词频统计 Top 10
========================================
单词                    出现次数
----------------------------------------
 1. python                   3
 2. is                       3
 3. and                      3
 4. it                       2
 5. a                        1
 6. powerful                 1
 7. programming              1
 8. language                 1
 9. easy                     1
10. to                       1
========================================
"""