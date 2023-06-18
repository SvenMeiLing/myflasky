# -*- coding: utf-8 -*-
# FileName: newTable.py
# Time : 2023/6/14 22:57
# Author: zzy
import sqlite3
import random
import time

# 连接到数据库
conn = sqlite3.connect('../../data.db')
c = conn.cursor()

# 创建植物详情数据表
c.execute('''CREATE TABLE IF NOT EXISTS plant_details (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                real_time REAL NOT NULL,
                description TEXT NOT NULL,
                date TEXT NOT NULL,
                filename TEXT NOT NULL,
                recognition_rate REAL NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )''')

# 植物名称列表
plant_names = ['葡萄黑腐病', '番茄叶斑病', '苹果黑星病', "其他"]

# 插入数据
start_time = time.time()
for i in range(100):
    # 生成随机的植物名称
    plant_name = random.choice(plant_names)

    # 生成随机的日期
    year = random.randint(2020, 2023)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # 假设所有月份都是28天
    date = f"{year}-{month:02d}-{day:02d}"

    # 构造数据行
    row = (
        i + 1,  # id
        plant_name,  # title
        random.uniform(0.01, 1.999999999),  # real_time
        f"{plant_name}是一种植物病害，常见于...",  # description
        date,  # date
        f"{plant_name}.jpg",  # filename
        random.uniform(0.7, 1),  # recognition_rate
        random.randint(1, 10),  # user_id
    )

    # 插入数据到表中
    c.execute("INSERT INTO plant_details VALUES (?, ?, ?, ?, ?, ?, ?, ?)", row)

    # 模拟插入数据的耗时
    time.sleep(random.uniform(0.01, 1.67))

# 提交数据并关闭连接
conn.commit()
conn.close()

end_time = time.time()
print(f"插入100条数据用时 {end_time - start_time:.2f} 秒.")
