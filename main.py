import os
import time
import datetime
import requests
import json

import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, StringVar


# --------------------- ฟังก์ชันเมนูคลิกขวา (Copy/Paste/Cut/Select All) --------------------- #
def show_context_menu(event, widget, menu):
    menu.widget = widget  # บันทึกว่าเมนูถูกเรียกที่ widget ไหน
    menu.tk_popup(event.x_root, event.y_root)

def copy_text(menu, root):
    widget = menu.widget
    try:
        widget.event_generate("<<Copy>>")
    except:
        pass

def paste_text(menu, root):
    widget = menu.widget
    try:
        widget.event_generate("<<Paste>>")
    except:
        pass

def cut_text(menu, root):
    widget = menu.widget
    try:
        widget.event_generate("<<Cut>>")
    except:
        pass

def select_all_text(menu):
    widget = menu.widget
    try:
        widget.event_generate("<<SelectAll>>")
    except:
        pass
    return "break"

def bind_keys_for_textbox(text_widget):
    # ทำให้ใช้ Ctrl+A, Ctrl+X, Ctrl+C, Ctrl+V ได้
    text_widget.bind("<Control-a>", lambda e: text_widget.event_generate("<<SelectAll>>"))
    text_widget.bind("<Control-A>", lambda e: text_widget.event_generate("<<SelectAll>>"))
    text_widget.bind("<Control-x>", lambda e: text_widget.event_generate("<<Cut>>"))
    text_widget.bind("<Control-X>", lambda e: text_widget.event_generate("<<Cut>>"))
    text_widget.bind("<Control-c>", lambda e: text_widget.event_generate("<<Copy>>"))
    text_widget.bind("<Control-C>", lambda e: text_widget.event_generate("<<Copy>>"))
    text_widget.bind("<Control-v>", lambda e: text_widget.event_generate("<<Paste>>"))
    text_widget.bind("<Control-V>", lambda e: text_widget.event_generate("<<Paste>>"))
    # Undo/Redo (Ctrl+Z, Ctrl+Y) ยังไม่มีใน CTkTextbox โดยตรง

# --------------------- ฟังก์ชัน save_adb_script (ฟอร์มเดิม) --------------------- #
def save_adb_script(device, fb_post_url, text):
    print("🔹 กำลังสร้างไฟล์ ADB Script...")  # Debug

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    file_name = f"adb_script_{timestamp}.py"

    folder_path = "test"
    os.makedirs(folder_path, exist_ok=True)  
    save_path = rf"{folder_path}\{file_name}"
    script_content = f'''import os
import time

device = "{device}"
os.system(f"adb -s {{device}} shell ime set com.android.adbkeyboard/.AdbIME")
fb_post_url = "{fb_post_url}"
os.system(f'adb -s {{device}} shell am start -a android.intent.action.VIEW -d "{{fb_post_url}}" com.android.chrome')
time.sleep(5)
os.system(f"adb -s {{device}} shell input tap 720 1776")
time.sleep(5)
text = "{text}"
for char in text:
    adb_command = f'adb -s {device} shell am broadcast -a ADB_INPUT_TEXT --es msg "{{char}}"'
    os.system(adb_command)
    time.sleep(0.1)
time.sleep(0.5)
os.system(f"adb -s {device} shell input keyevent 61 66")
'''

    print(f"🔹 กำลังบันทึกไฟล์ที่: {save_path}")  # Debug

    with open(save_path, "w", encoding="utf-8") as file:
        file.write(script_content)

    print(f"บันทึกไฟล์ที่ {save_path} สำเร็จ!")


# --------------------- ข้อมูลภายในที่มีอยู่ (Local Data) --------------------- #
local_data = [
# {"id": 1, "userpc": "5200b4c053c8c4eb", "package_name": "com.android.chrome", "gender": "ชาย", "age": 50, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},
# {"id": 2, "userpc": "52003627eca9c45d", "package_name": "com.android.chromf", "gender": "หญิง", "age": 50, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},
# {"id": 3, "userpc": "5200a554ee0284fb", "package_name": "com.android.chrome", "gender": "หญิง", "age": 40, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},
# {"id": 4, "userpc": "5200a554ee0284fb", "package_name": "com.android.chromf", "gender": "ชาย", "age": 40, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},
# {"id": 5, "userpc": "52008dd8fec325dd", "package_name": "com.android.chrome", "gender": "หญิง", "age": 30, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},
# {"id": 6, "userpc": "52008dd8fec325dd", "package_name": "com.android.chromf", "gender": "ชาย", "age": 30, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},
# {"id": 7, "userpc": "5200ca24528715f5", "package_name": "com.android.chrome", "gender": "ชาย", "age": 20, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},
# {"id": 8, "userpc": "5200ca24528715f5", "package_name": "com.android.chromf", "gender": "หญิง", "age": 20, "occupation": "-", "personality": "-", "comment": "-", "political_orientation": "-", "link": "https://www.facebook.com/sorrayuth9115/posts/1255243385962598"},






]


# --------------------- คลาสหลักของแอป --------------------- #
ctk.set_appearance_mode("blue") #สว่างเหมือน Messenger
ctk.set_default_color_theme("blue")

class APIDataApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("💬 Messenger-Style ADB Script Generator")
        self.geometry("900x600")

        # ---------- สร้างเมนูคลิกขวา (context menu) สำหรับ Text/Entry ---------- #
        self.widget_context_menu = tk.Menu(self, tearoff=0)
        self.widget_context_menu.add_command(
            label="คัดลอก (Copy)",
            command=lambda: copy_text(self.widget_context_menu, self)
        )
        self.widget_context_menu.add_command(
            label="วาง (Paste)",
            command=lambda: paste_text(self.widget_context_menu, self)
        )
        self.widget_context_menu.add_command(
            label="ตัด (Cut)",
            command=lambda: cut_text(self.widget_context_menu, self)
        )
        self.widget_context_menu.add_command(
            label="เลือกทั้งหมด (Select All)",
            command=lambda: select_all_text(self.widget_context_menu)
        )

        # ตัวแปรผูกกับ Entry
        self.device_var = StringVar()
        self.fb_url_var = StringVar()
        self.text_var = StringVar()

        # --------------------- Header Label --------------------- #
        self.header_label = ctk.CTkLabel(self, text="💬 API Data Merger & ADB Script Generator", font=("Arial", 18, "bold"))
        self.header_label.pack(pady=10)

        # --------------------- Entry: Device ID --------------------- #
        ctk.CTkLabel(self, text="Device ID (UserPC):").pack(pady=2)
        self.device_entry = ctk.CTkEntry(self, textvariable=self.device_var, state="readonly")
        self.device_entry.pack(pady=2)
        self.device_entry.bind("<Button-3>", lambda e: show_context_menu(e, self.device_entry, self.widget_context_menu))

        # --------------------- Entry: Facebook Post URL --------------------- #
        ctk.CTkLabel(self, text="Facebook Post URL:").pack(pady=2)
        self.fb_url_entry = ctk.CTkEntry(self, textvariable=self.fb_url_var, placeholder_text="กรอกลิงก์โพสต์ Facebook", width=700, height=30)
        self.fb_url_entry.pack(pady=2)
        self.fb_url_entry.bind("<Button-3>", lambda e: show_context_menu(e, self.fb_url_entry, self.widget_context_menu))

        # --------------------- Entry: ข้อความที่จะโพสต์ --------------------- #
        ctk.CTkLabel(self, text="ข้อความที่ต้องการโพสต์ (Comment):").pack(pady=2)
        self.text_entry = ctk.CTkEntry(self, textvariable=self.text_var, width=700, height=30)
        self.text_entry.pack(pady=2)
        self.text_entry.bind("<Button-3>", lambda e: show_context_menu(e, self.text_entry, self.widget_context_menu))

        # --------------------- ปุ่มบันทึกสคริปต์ ADB --------------------- #
        self.save_button = ctk.CTkButton(self, text="บันทึกสคริปต์ ADB", command=self.save_script)
        self.save_button.pack(pady=10)

        # --------------------- สร้างตารางข้อมูล --------------------- #
        frame = ctk.CTkFrame(self)
        frame.pack(pady=10, expand=True, fill="both")

        self.tree_scroll_y = ttk.Scrollbar(frame, orient="vertical")
        self.tree_scroll_y.pack(side="right", fill="y")

        self.tree_scroll_x = ttk.Scrollbar(frame, orient="horizontal")
        self.tree_scroll_x.pack(side="bottom", fill="x")


        # เพิ่มคอลัมน์ "Selected" ไว้ท้ายสุด เพื่อใช้เช็คบ็อกซ์ (✓ / ว่าง)
        self.columns = (
            "ID", "UserPC", "package_name", "Gender", "Age", 
            "Occupation", "Personality", "Comment", "Political", 
            "link", "Selected"
        )

        self.tree = ttk.Treeview(
            frame, 
            columns=self.columns, 
            show="headings",
            yscrollcommand=self.tree_scroll_y.set,
            xscrollcommand=self.tree_scroll_x.set
        )

        self.tree.tag_configure("selected_row", background="#CCE5FF")  # สีฟ้าอ่อน

        # ตั้งหัวและความกว้างของแต่ละคอลัมน์
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=40, anchor="center")

        self.tree.heading("UserPC", text="UserPC")
        self.tree.column("UserPC", width=120, anchor="center")

        self.tree.heading("package_name", text="package_name")
        self.tree.column("package_name", width=120, anchor="center")

        self.tree.heading("Gender", text="Gender")
        self.tree.column("Gender", width=60, anchor="center")

        self.tree.heading("Age", text="Age")
        self.tree.column("Age", width=40, anchor="center")

        self.tree.heading("Occupation", text="Occupation")
        self.tree.column("Occupation", width=40, anchor="center")

        self.tree.heading("Personality", text="Personality")
        self.tree.column("Personality", width=40, anchor="center")

        self.tree.heading("Comment", text="Comment")
        self.tree.column("Comment", width=200, anchor="center")

        self.tree.heading("Political", text="Political")
        self.tree.column("Political", width=10, anchor="center")

        self.tree.heading("link", text="link")
        self.tree.column("link", width=15, anchor="center")

        self.tree.heading("Selected", text="Selected")
        self.tree.column("Selected", width=60, anchor="center")

        self.tree.pack(expand=True, fill="both")
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)

        # เก็บสถานะ checkbox ของแต่ละ row
        self.check_states = {}

        # คลิกซ้าย single-click -> toggle checkbox ถ้าอยู่ใน "Selected"
        self.tree.bind("<Button-1>", self.on_tree_click)

        # คลิกซ้าย release -> เลือก row => อัปเดต entry
        self.tree.bind("<ButtonRelease-1>", self.select_row)

        # Double-click -> ถ้าคอลัมน์ Comment => เปิดหน้าต่างแก้ไข
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # --------------------- โหลดข้อมูลรอบแรก (Local data) --------------------- #
        self.full_data = []
        self.load_local_data()

        # --------------------- ปุ่มโหลดข้อมูลจาก API --------------------- #
        self.load_button = ctk.CTkButton(self, text="โหลดข้อมูลจาก API", command=self.fetch_json)
        self.load_button.pack(pady=5)
    # --------------------------------------------------------------------------------
    # ส่วนโหลดข้อมูล
    # --------------------------------------------------------------------------------
    def load_local_data(self):
        self.full_data = local_data
        self.update_table(self.full_data)

    def fetch_json(self):
        try:
            # อ่านไฟล์ JSON
            with open("local_data.json", "r", encoding="utf-8") as data_json:
                data = json.load(data_json)  # อ่านข้อมูลจากไฟล์ JSON
                
                # ตรวจสอบว่าเป็นลิสต์ของอ็อบเจ็กต์หรือไม่
                if isinstance(data, list):
                    print("\n✅ ข้อมูลจาก local_data.json:")
                    print(json.dumps(data, indent=4, ensure_ascii=False))  # แสดงข้อมูล JSON ทั้งหมด

                    #Test Case 
                    # selected = 1  # เลือก id ที่ต้องการค้นหา
                    # userpc = [item.get("userpc", "ไม่มีข้อมูล") for item in data if item["id"] == selected]
                    # comments = [item.get("comment", "ไม่มีข้อมูล") for item in data if item["id"] == selected]
                    # links = [item.get("link", "ไม่มีข้อมูล") for item in data if item["id"] == selected]
                    #data = json.dumps(data, indent=4, ensure_ascii=False)
                    # print("\n📝 รายการความคิดเห็น:")
                    # print("User PC:", userpc)
                    # print("Comments:", comments)
                    # print("Links:", links)
                    # print("ALL ================")
                    #print(data)

                    # self.save_script(self)
                    self.update_table(data) 

        except FileNotFoundError:
            print("❌ ไม่พบไฟล์ local_data.json")
        except json.JSONDecodeError:
            print("❌ เกิดข้อผิดพลาดในการแปลง JSON")
        except Exception as e:
            print(f"❌ Error: {e}")
            
    # --------------------------------------------------------------------------------
    # ส่วนอัปเดตตาราง
    # --------------------------------------------------------------------------------
    def update_table(self, data):
        # ลบข้อมูลเก่า
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.check_states.clear()
        # print("class update_table", data)

        # เพิ่มข้อมูลใหม่
        for d in data:
            values = (
                d["id"],
                d["userpc"],
                d["package_name"],
                d["gender"],
                d["age"],
                d["occupation"],
                d["personality"],
                d["comment"],
                d["political_orientation"],
                d["link"],
                " "  # เริ่มต้นว่าง
            )
            # print("class update for : ",values)
            row_id = self.tree.insert("", "end", values=values)
            self.check_states[row_id] = False

    # --------------------------------------------------------------------------------
    # ส่วนคลิกซ้าย single-click -> toggle checkbox
    # --------------------------------------------------------------------------------
    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            col = self.tree.identify_column(event.x)
            if col == "#11":  # คอลัมน์ Selected
                row_id = self.tree.identify_row(event.y)
                if row_id:
                    current_state = self.check_states[row_id]
                    new_state = not current_state
                    self.check_states[row_id] = new_state
                    self.tree.set(row_id, "Selected", "✓" if new_state else " ")

    # --------------------------------------------------------------------------------
    # ส่วนเลือกแถว -> อัปเดต Entry
    # --------------------------------------------------------------------------------
    def select_row(self, event):
        selected_item = self.tree.selection()  # ได้เป็น tuple เช่น ("I001",)

        # 1) ล้าง tag "selected_row" ออกหมดก่อน
        for item_id in self.tree.get_children():
            self.tree.item(item_id, tags="")

        # 2) ถ้ามีการเลือกจริง (ไม่ว่าง)
        if selected_item:
            # ดึงค่า row id ตัวแรก (เช่น "I001")
            row_id = selected_item[0]

            # กำหนด Tag "selected_row"
            self.tree.item(row_id, tags=("selected_row",))

            # --- ส่วนดึงค่าในตารางมากรอก Entry (โค้ดเดิมของคุณ) ---
            values = self.tree.item(row_id, "values")
            self.device_var.set(values[1])  # ตัวอย่าง
            self.text_var.set(values[7])
            self.fb_url_var.set(values[9])


    # --------------------------------------------------------------------------------
    # Double-click -> ถ้าคอลัมน์ Comment => เปิดหน้าต่างแก้ไข
    # --------------------------------------------------------------------------------
    def on_tree_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        col = self.tree.identify_column(event.x)
        row_id = self.tree.identify_row(event.y)

        if region == "cell" and col == "#8" and row_id:
            item_values = self.tree.item(row_id, "values")
            current_comment = item_values[7]
            self.open_comment_editor(row_id, current_comment)

    def open_comment_editor(self, row_id, current_text):
        editor_window = ctk.CTkToplevel(self)
        editor_window.title("แก้ไข Comment")
        editor_window.geometry("400x300")

        ctk.CTkLabel(editor_window, text="แก้ไข Comment:", font=("Arial", 14)).pack(pady=5)

        text_editor = ctk.CTkTextbox(editor_window, width=350, height=150)
        text_editor.pack(pady=5)

        text_editor.insert("1.0", current_text)
        bind_keys_for_textbox(text_editor)
        text_editor.bind("<Button-3>", lambda e: show_context_menu(e, text_editor, self.widget_context_menu))

        def save_edited_comment():
            new_comment = text_editor.get("1.0", "end-1c")
            item_values = list(self.tree.item(row_id, "values"))
            item_values[7] = new_comment
            self.tree.item(row_id, values=item_values)

            # อัปเดตใน self.full_data ด้วย
            data_id = item_values[0]
            for d in self.full_data:
                if str(d["id"]) == str(data_id):
                    d["comment"] = new_comment
                    break

            editor_window.destroy()

        save_button = ctk.CTkButton(editor_window, text="บันทึก", command=save_edited_comment)
        save_button.pack(pady=5)

    # --------------------------------------------------------------------------------
    # บันทึกสคริปต์ ADB (ตามฟอร์มเดิม) เฉพาะแถวที่ติ๊ก
    # --------------------------------------------------------------------------------
    def save_script(self):
        for row_id, checked in self.check_states.items():
            if checked:
                row_values = self.tree.item(row_id, "values")
                # (ID,UserPC,package,Gender,Age,Occup,Personality,Comment,Political,link,Selected)
                device = row_values[1]      # UserPC
                text = row_values[7]        # Comment
                fb_post_url = row_values[9] # link

                print("Device :", device)
                print("Test", text)
                print("fb_link", fb_post_url)

                # ใช้ฟังก์ชัน save_adb_script ที่เราแก้คืนให้เป็นฟอร์มเดิม
                save_adb_script(device, fb_post_url, text)


if __name__ == "__main__":
    app = APIDataApp()
    app.mainloop()