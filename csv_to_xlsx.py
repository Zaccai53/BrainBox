import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd

# 选择 CSV 文件
def select_csv_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")],
        title="选择 CSV 文件"
    )
    if file_path:
        entry_csv.delete(0, tk.END)
        entry_csv.insert(0, file_path)

# 选择输出的 XLSX 文件
def select_xlsx_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel files", "*.xlsx")],
        title="保存为 Excel 文件"
    )
    if file_path:
        entry_xlsx.delete(0, tk.END)
        entry_xlsx.insert(0, file_path)

# 执行转换操作
def convert_csv_to_xlsx():
    csv_file = entry_csv.get()
    xlsx_file = entry_xlsx.get()

    if not csv_file or not xlsx_file:
        messagebox.showerror("错误", "请提供有效的 CSV 文件和输出路径！")
        return

    try:
        # 读取 CSV 文件
        df = pd.read_csv(csv_file)

        # 将数据保存为 Excel 文件
        df.to_excel(xlsx_file, index=False, engine='openpyxl')

        # 弹出成功消息
        messagebox.showinfo("成功", f"CSV 文件已成功转换为 {xlsx_file}")
    except Exception as e:
        # 异常处理
        messagebox.showerror("错误", f"转换过程中发生错误: {e}")

# 创建 GUI 窗口
root = tk.Tk()
root.title("CSV 转 Excel")
root.geometry("400x200")

# CSV 文件选择部分
label_csv = tk.Label(root, text="选择 CSV 文件:")
label_csv.pack(pady=5)

entry_csv = tk.Entry(root, width=40)
entry_csv.pack(pady=5)

button_browse_csv = tk.Button(root, text="浏览", command=select_csv_file)
button_browse_csv.pack(pady=5)

# XLSX 文件选择部分
label_xlsx = tk.Label(root, text="保存为 XLSX 文件:")
label_xlsx.pack(pady=5)

entry_xlsx = tk.Entry(root, width=40)
entry_xlsx.pack(pady=5)

button_browse_xlsx = tk.Button(root, text="浏览", command=select_xlsx_file)
button_browse_xlsx.pack(pady=5)

# 转换按钮
button_convert = tk.Button(root, text="转换", command=convert_csv_to_xlsx)
button_convert.pack(pady=20)

# 运行 GUI
root.mainloop()
