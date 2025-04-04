import json
import tkinter as tk
from tkinter import messagebox

# ฟังก์ชันโหลดข้อมูลจากไฟล์ JSON
def load_data(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# ฟังก์ชันบันทึกข้อมูลลงไฟล์ JSON
def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

# ฟังก์ชันบันทึกข้อมูลเมื่อกดปุ่ม "บันทึก"
def save_comments():
    global data
    new_comments = comment_text.get("1.0", tk.END).strip().split("\n")
    new_link = link_text.get("1.0", tk.END).strip().split("\n")
    
    if not new_comments or not new_link:
        messagebox.showwarning("คำเตือน", "กรุณากรอกคอมเมนต์และลิ้งอย่างน้อย 1 รายการ")
        return
    
    # Check that the number of comments and links match
    if len(new_comments) != len(new_link):
        messagebox.showwarning("คำเตือน", "จำนวนคอมเมนต์และลิ้งไม่ตรงกัน")
        return

    existing_ids = [int(entry['id']) for entry in data] if data else []
    next_id = max(existing_ids, default=0) + 1

    # Loop through both lists of comments and links
    for comment, link in zip(new_comments, new_link):
        if comment.strip() and link.strip():
            data.append({
                "id": int(next_id),
                "userpc": str("ยังไม่มี"),
                "package_name": str("ยังไม่มี"),
                "gender": str("ยังไม่มี"),
                "age": str("ยังไม่มี"),
                "occupation": str("ยังไม่มี"),
                "personality": str("ยังไม่มี"),
                "comment": comment.strip(),
                "political_orientation": str("ยังไม่มี"),
                "link": link.strip(),
            })
            next_id += 1
    
    save_data(file_path, data)
    messagebox.showinfo("สำเร็จ", "บันทึกคอมเมนต์สำเร็จ!")
    root.quit()

# โหลดข้อมูลจากไฟล์ JSON
file_path = 'local_data.json'
data = load_data(file_path)

# สร้างหน้าต่างหลักของ Tkinter
root = tk.Tk()
root.title("เพิ่มคอมเมนต์")

# ส่วนของอินพุตคอมเมนต์
tk.Label(root, text="เพิ่มคอมเมนต์ (พิมพ์หลายบรรทัดได้)").pack(pady=5)
comment_text = tk.Text(root, height=10, width=50)
comment_text.pack(pady=5)

tk.Label(root, text="เพิ่มลิ้ง (พิมพ์หลายบรรทัดได้)").pack(pady=5)
link_text = tk.Text(root, height=10, width=50)
link_text.pack(pady=5)

# ปุ่ม "บันทึก"
save_button = tk.Button(root, text="บันทึก", command=save_comments)
save_button.pack(pady=10)

# เริ่ม GUI
root.mainloop()
