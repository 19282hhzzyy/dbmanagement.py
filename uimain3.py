import os
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Scrollbar, filedialog, messagebox
from uidase import *
# 数据库处理
db_data = DaseData()

def newmain():
    global tkui, select_folder_path, select_data_id, history_list

    # 当前选中的文件夹路径
    select_folder_path = None
    # 当前选中的数据id
    select_data_id = None
    history_list = []

    tkui = tk.Tk()
    tkui.title("xkjhzy")
    tkui.geometry(
        '%dx%d+%d+%d' % (800, 500, (tkui.winfo_screenwidth() - 800) / 2, (tkui.winfo_screenheight() - 500) / 2))

    menubar = tk.Menu(tkui, tearoff=False)

    # 创建文件子菜单
    fileMenu = Menu(menubar, tearoff=False)  # 关闭子菜单默认可单独拉出功能
    fileMenu.add_command(label='新建', command=on_new)  # 添加命令菜单项
    fileMenu.add_command(label='打开', command=on_open)
    fileMenu.add_command(label='保存', command=on_save_as)
    fileMenu.add_command(label='另存为', command=on_save_as)
    fileMenu.add_separator()
    fileMenu.add_command(label=u"最近打开", command=on_history)
    # 添加编辑子菜单并绑定事件处理函数
    editMenu = Menu(menubar, tearoff=False)  # 关闭子菜单默认可单独拉出功能
    editMenu.add_command(label='增加', command=on_new_row)
    editMenu.add_command(label='删除', command=on_delete)
    # 创建主菜单
    menubar.add_cascade(label='文件', menu=fileMenu)  # 与文件子菜单关联
    menubar.add_cascade(label='编辑', menu=editMenu)  # 与编辑子菜单关联

    tkui.config(menu=menubar)
    # 创建左侧文件夹树
    create_folder_tree()
    # 创建右侧数据库内容显示
    create_tree()

    tkui.mainloop()

# 创建左侧文件夹树
def create_folder_tree():
    f = Frame(tkui, width=210, height=396)
    f.place(x=20, y=20)

    pr_canvas = Canvas(f)
    pr_frame = Frame(pr_canvas, width=1000, height=396)
    pr_frame.place(x=10, y=10)
    # Y轴滚动条
    xbar = Scrollbar(f, orient=HORIZONTAL, command=pr_canvas.xview)
    xbar.pack(side="bottom", fill="x")
    # Y轴滚动条赋予给画布
    pr_canvas.configure(xscrollcommand=xbar.set)
    pr_canvas.pack(side="left")
    pr_canvas.create_window((0, 0), window=pr_frame, anchor='nw')

    # 绑定滚动条事件
    def on_xbar(event):
        pr_canvas.configure(scrollregion=pr_canvas.bbox("all"), width=210, height=396)

    pr_frame.bind("<Configure>", on_xbar)

    # 纵横滚动条
    sc_y = Scrollbar(tkui)
    # 全局变量 文件夹树
    global folder_tree
    folder_tree = ttk.Treeview(pr_frame, show="tree", yscrollcommand=sc_y.set)
    # 选中行
    folder_tree.bind('<<TreeviewOpen>>',
                     on_select_folder_tree)  # 在事件SEQUENCE中将FUNC函数的调用绑定到此小部件。SEQUENCE是一串串联的事件模式。事件模式是这样的:MODIFIER是Control, Mod2, M2, Shift, Mod3, M3, Lock, Mod4, M4, Button1, B1, Mod5, M5 Button2, B2, Meta, M, Button3, B3, Alt, Button4, B4, Double, Button5, B5 Triple, Mod1, M1。类型是一个激活，进入，地图，按钮，按钮，暴露，运动，按钮释放FocusIn, MouseWheel，循环，FocusOut，属性，Colormap，重力Reparent，配置，按键，键，取消映射，取消激活，KeyRelease可见性，破坏，离开和细节
    folder_tree.place(x=0, y=0, width=1000, height=400)
    # 设置滚动条方向
    sc_y.config(command=folder_tree.yview)  # ：配置小部件资源。资源的值被指定为关键字参数。要获得允许的关键字参数的概述，请调用方法keys。
    sc_y.place(x=220, y=20, height=400)

    # 全局变量 设置初始化文件夹路径
    global init_path
    init_path = os.path.abspath(r'.\\')
    update_folder_tree()
    # 美化遮挡黑边
    LabelFrame(tkui, width=201, height=3).place(x=20, y=20)
    LabelFrame(tkui, width=201, height=3).place(x=20, y=418)
    LabelFrame(tkui, width=3, height=399).place(x=20, y=20)
    LabelFrame(tkui, width=3, height=399).place(x=220, y=20)

    global folder_var
    folder_var = StringVar(value=init_path)
    Entry(tkui, textvariable=folder_var, width=23).place(x=20, y=451)  # 用父组件MASTER构造一个条目小部件。
    Button(tkui, text='选择', command=get_folder, width=5).place(x=189,
                                                               y=445)  # 标准选项活动背景，活动前景，锚，背景，位图，边框，光标，禁用前景，字体，前景高亮背景，高亮颜色，高亮厚度，图像，调整

# 获得文件夹路径
def get_folder():
    global folder_var, init_path
    file = filedialog.askdirectory()
    if file != '':
        folder_var.set(file)
        init_path = file
        update_folder_tree()

# 刷新文件数
def update_folder_tree():
    on_clear(folder_tree)

    # 遍历文件夹
    def traverse_folder(root_dir, _myid):
        # 获得该文件夹下面的全部文件和文件夹
        ls = os.listdir(root_dir)
        # 遍历它们
        for i in ls:
            try:
                # 获取绝对路径
                ii = os.path.join(root_dir, i)
                # 插入文件夹树
                myid2 = folder_tree.insert(_myid, 'end', text=i, values=[ii])
                # 判断是不是文件夹， 如果是文件夹重新遍历
                if os.path.isdir(ii):
                    traverse_folder(ii, myid2)
            except:
                continue

    myid = folder_tree.insert("", 'end', text=init_path, values=[init_path])
    traverse_folder(init_path, myid)

# 清除所有数据,_tree: folder_tree 或者 tree
def on_clear(_tree):
    # 遍历列表, 删除所有数据
    for d in _tree.get_children():
        _tree.delete(d)

# 模拟双击文件夹路径
def on_select_folder_tree(event):
    global history_list
    try:
        # 判断选中的是不是.db后缀的文件
        select_folder_path = folder_tree.item(folder_tree.selection()[0], "values")[0]
        is_db = select_folder_path.endswith(".db") or select_folder_path.endswith(".DB")
        if is_db:
            # 满足要求进行处理
            db_data.open_dase(select_folder_path)
            on_update_tree()
            history_list.append(select_folder_path)
    except:
        return

# 创建右侧数据库内容显示
def create_tree():
    # 滚动条
    sc_y = Scrollbar(tkui)
    sc_x = Scrollbar(tkui, orient=HORIZONTAL)
    # 创建树对应的数据
    columns = ('1', '2', '3', '4', '5')
    columns_width = (1, 1, 1, 1, 90)
    columns_txt = ('用户名', '指纹', '密码', '权限', '用户类型（管理：0，普通：1）')
    global tree
    tree = ttk.Treeview(tkui, show="headings", columns=columns, yscrollcommand=sc_y.set,
                        xscrollcommand=sc_x.set)  # 用父master构造一个Ttk树视图。
    sc_y.config(command=tree.yview)
    sc_x.config(command=tree.xview)

    for i in range(len(columns)):
        tree.column(columns[i], width=columns_width[i], anchor='center')
        tree.heading(columns[i], text=columns_txt[i])

    tree.bind('<<TreeviewSelect>>', on_select_tree)
    tree.bind('<<TreeviewOpen>>', on_select_tree_edit)
    tree.place(x=250, y=20, width=520, height=440)
    sc_x.place(x=250, y=460, width=520)
    sc_y.place(x=540, y=20, height=440)

# 更新数据
def on_update_tree():
    db_dic = db_data.get_database_dic()
    db_name = db_data.get_database_name()
    # 每次都要清空数据
    on_clear(tree)
    for i in range(len(db_dic[db_name])):
        d: DBData = db_dic[db_name][i]
        tree.insert('', 'end', values=[d.user_name, d.fingerprint, d.user_password, d.permissio, d.user_type])

# 选中
def on_select_tree(event):
    try:
        global select_data_id
        select_data_id = tree.item(tree.selection()[0], "values")[0]
    except:
        return

# 模拟双击
def on_select_tree_edit(event):
    try:
        global select_data_id
        select_data_id = tree.item(tree.selection()[0], "values")[0]
        on_edit()
    except:
        return

# 新建数据库
def on_new():
    global history_list
    file = filedialog.asksaveasfilename(title=u'创建文件', filetypes=[('数据库文件', 'db')], defaultextension='.db')
    if file:
        try:
            db_data.new_database(file)
            on_update_tree()
            update_folder_tree()
            history_list.append(file)
            messagebox.showinfo(title='提示', message="创建文件成功！")
        except Exception as e:
            messagebox.showinfo(title='提示', message="创建文件失败，请重试！")  # 显示信息消息
    else:
        messagebox.showinfo(title='提示', message="未创建文件！")
    pass

# 打开数据库
def on_open():
    global history_list
    file = filedialog.askopenfilename(title=u'打开文件', filetypes=[('数据库文件', 'db')])
    try:
        db_data.open_dase(file)
        on_update_tree()
        history_list.append(file)
    except Exception as e:
        messagebox.showinfo(title='提示', message="打开失败，请重试！")

# 保存数据库
def on_save_as():
    file = filedialog.asksaveasfilename(title=u'另存为', filetypes=[('数据库文件', 'db')], defaultextension='.db')
    if file:
        try:
            db_data.on_save_as(file)
            update_folder_tree()
            messagebox.showinfo(title='提示', message="另存文件成功！")
        except Exception as e:
            messagebox.showinfo(title='提示', message="另存文件失败，请重试！")

# 浏览记录
def on_history():
    history_view = Toplevel(
        tkui)  # 用父组件MASTER构造一个顶级小部件。有效的资源名:background, bd, bg, borderwidth, class, colormap, container, cursor, height, highlightbackground, highlightcolor, highlightthickness, menu, relief, screen, takefocus, use, visual, width
    history_view.title('浏览记录')
    # 窗体居中
    history_view.geometry(
        '%dx%d+%d+%d' % (360, 400, (tkui.winfo_screenwidth() - 360) / 2, (tkui.winfo_screenheight() - 400) / 2))

    # 滚动条
    sc_y = Scrollbar(history_view)
    # 创建树对应的数据
    history_tree = ttk.Treeview(history_view, show="headings", yscrollcommand=sc_y.set, columns=('1'))
    sc_y.config(command=history_tree.yview)
    history_tree.column('1', anchor='center')
    history_tree.heading('1', text='路径')
    history_tree.place(x=20, y=20, width=300, height=360)
    sc_y.place(x=320, y=20, height=360)

    for value in history_list:
        history_tree.insert('', 'end', values=[value])

# 增加新数据库
def on_new_row():
    db_name = db_data.get_database_name()
    if db_name is None:
        messagebox.showinfo(title='提示', message="请选择数据库")
        return
    # 创建新增弹框
    new_and_edit_view = Toplevel(tkui)
    new_and_edit_view.title('增加')
    # 窗体居中
    new_and_edit_view.geometry(
        '%dx%d+%d+%d' % (360, 250, (tkui.winfo_screenwidth() - 360) / 2, (tkui.winfo_screenheight() - 250) / 2))
    global user_name, fingerprint, user_password, permissio, user_type
    user_name = StringVar()
    fingerprint = StringVar()
    user_password = StringVar()
    permissio = StringVar()
    user_type = StringVar()

    Label(new_and_edit_view, text='用户名').place(x=20, y=30)
    Entry(new_and_edit_view, textvariable=user_name, width=18).place(x=120, y=30)
    Label(new_and_edit_view, text='指纹').place(x=20, y=70)
    Entry(new_and_edit_view, textvariable=fingerprint, width=18).place(x=120, y=70)
    Label(new_and_edit_view, text='密码').place(x=20, y=110)
    Entry(new_and_edit_view, textvariable=user_password, width=18).place(x=120, y=110)
    Label(new_and_edit_view, text='权限').place(x=20, y=150)
    Entry(new_and_edit_view, textvariable=permissio, width=18).place(x=120, y=150)
    Label(new_and_edit_view, text='用户权限（1/2）').place(x=20, y=190)
    Entry(new_and_edit_view, textvariable=user_type, width=18).place(x=120, y=190)

    # 往数据库添加数据
    def on_add():
        new_and_edit_view.destroy()  # 销毁这个部件和所有的后代部件
        d = DBData(user_name.get(), fingerprint.get(), user_password.get(), permissio.get(), user_type.get())
        add_type = db_data.add_data(d)
        # 判断是否有重复用户名
        if add_type == 0:
            messagebox.showinfo(title='提示', message="增加失败，用户名已存在")
        else:
            on_update_tree()

    Button(new_and_edit_view, text='确定', command=on_add).place(x=270, y=185)

# 删除所选记录
def on_delete():
    # 改变成全局变量
    global select_data_id
    db_name = db_data.get_database_name()
    # 判断是否选中了数据库和记录
    if db_name is None:
        messagebox.showinfo(title='提示', message="请选择数据库")
        return
    if select_data_id is None:
        messagebox.showinfo(title='提示', message="请选择记录")
        return
    db_data.del_data(select_data_id)
    on_update_tree()
    select_data_id = None

# 编辑选中对象
def on_edit():
    db_name = db_data.get_database_name()
    # 判断是否选中了数据库和记录
    if db_name is None:
        messagebox.showinfo(title='提示', message="请选择数据库")
        return
    if select_data_id is None:
        messagebox.showinfo(title='提示', message="请选择记录")
        return
    # 弹窗编辑数据
    new_and_edit_view = Toplevel(tkui)
    new_and_edit_view.title('编辑')
    # 窗体居中
    new_and_edit_view.geometry(
        '%dx%d+%d+%d' % (360, 250, (tkui.winfo_screenwidth() - 360) / 2, (tkui.winfo_screenheight() - 250) / 2))
    global user_name, fingerprint, user_password, permissio, user_type
    user_name = StringVar(value=select_data_id)
    fingerprint = StringVar()
    user_password = StringVar()
    permissio = StringVar()
    user_type = StringVar()

    Label(new_and_edit_view, text='用户名').place(x=20, y=30)
    Entry(new_and_edit_view, textvariable=user_name, width=18, state='disabled').place(x=120, y=30)
    Label(new_and_edit_view, text='指纹').place(x=20, y=70)
    Entry(new_and_edit_view, textvariable=fingerprint, width=18).place(x=120, y=70)
    Label(new_and_edit_view, text='密码').place(x=20, y=110)
    Entry(new_and_edit_view, textvariable=user_password, width=18).place(x=120, y=110)
    Label(new_and_edit_view, text='权限').place(x=20, y=150)
    Entry(new_and_edit_view, textvariable=permissio, width=18).place(x=120, y=150)
    Label(new_and_edit_view, text='用户权限（1/2）').place(x=20, y=190)
    Entry(new_and_edit_view, textvariable=user_type, width=18).place(x=120, y=190)

    # 往数据库进行编辑数据
    def on_edit():
        new_and_edit_view.destroy()
        d = DBData(user_name.get(), fingerprint.get(), user_password.get(), permissio.get(), user_type.get())
        db_data.edit_data(d)
        on_update_tree()

    Button(new_and_edit_view, text='确定', command=on_edit).place(x=270, y=185)

newmain()
