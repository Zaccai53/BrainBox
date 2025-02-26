import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def process_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return
    
    try:
        # 读取CSV文件
        df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip')
        
        # 处理规则：删除拍一拍、撤回、emoji 和邀请记录
        mask = ~df['StrContent'].astype(str).str.contains(
            'tickled|recalled|<emoji|invited',  # 添加 invited 到排除条件
            case=False,
            na=False
        )
        filtered_df = df[mask]
        
        # 提取邀请记录（仍从原始数据中提取）
        invited_df = df[df['StrContent'].astype(str).str.contains('invited', case=False, na=False)]
        
        # 生成输出路径
        dir_path = os.path.dirname(file_path)
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # 保存处理后的文件
        filtered_output = os.path.join(dir_path, f"{base_name}_1st_processed.csv")
        invited_output = os.path.join(dir_path, f"{base_name}_invitation.csv")
        
        filtered_df.to_csv(filtered_output, index=False, encoding='utf-8-sig')
        invited_df.to_csv(invited_output, index=False, encoding='utf-8-sig')
        
        messagebox.showinfo("完成", f"处理完成！\n生成文件：\n{filtered_output}\n{invited_output}")
        
    except Exception as e:
        messagebox.showerror("错误", f"处理文件时发生错误：\n{str(e)}")

# 创建GUI界面
root = tk.Tk()
root.title("CSV处理器")
root.geometry("300x150")

frame = tk.Frame(root)
frame.pack(pady=20)

label = tk.Label(frame, text="选择要处理的CSV文件")
label.pack(pady=10)

browse_btn = tk.Button(
    frame, 
    text="选择文件并处理", 
    command=process_csv,
    bg="#4CAF50",
    fg="white"
)
browse_btn.pack(pady=5)

root.mainloop()