"""
NEXORA - Smart Library Platform
Midnight Luxe Tkinter + MySQL redesign.

Install:
    py -m pip install mysql-connector-python matplotlib

Run:
    py main.py

Database defaults are retained from the uploaded project.
You can override them with environment variables:
    NEXORA_DB_HOST, NEXORA_DB_USER, NEXORA_DB_PASSWORD, NEXORA_DB_NAME
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from contextlib import closing

import mysql.connector
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ---------------------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------------------
DB_CONFIG = {
    "host": os.getenv("NEXORA_DB_HOST", "localhost"),
    "user": os.getenv("NEXORA_DB_USER", "root"),
    "password": os.getenv("NEXORA_DB_PASSWORD", "1234"),
    "database": os.getenv("NEXORA_DB_NAME", "library_db"),
}

# Original demo login retained from the uploaded application.
ADMIN_USERNAME = os.getenv("NEXORA_ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("NEXORA_ADMIN_PASSWORD", "admin123")


def db():
    """Open a MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


# ---------------------------------------------------------------------
# MIDNIGHT LUXE THEME
# ---------------------------------------------------------------------
C = {
    "app": "#080D19",
    "sidebar": "#0B1222",
    "panel": "#111B2E",
    "panel_alt": "#15223A",
    "panel_hover": "#1B2B47",
    "border": "#243550",
    "text": "#F2F5FC",
    "muted": "#91A0B8",
    "dim": "#65748D",
    "purple": "#9B7BFF",
    "purple_dark": "#7657E8",
    "cyan": "#39D5E8",
    "blue": "#579BFF",
    "green": "#35D39A",
    "orange": "#FFB45E",
    "red": "#FF6F85",
    "white": "#FFFFFF",
}

FONT = "Segoe UI"


class LibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NEXORA | Smart Library Platform")
        self.root.geometry("1440x850")
        self.root.minsize(1120, 700)
        self.root.configure(bg=C["app"])

        self.active_page = None
        self.nav_buttons = {}
        self._configure_styles()
        self._build_shell()
        self.show_dashboard()

    # ---------------------------- UI FOUNDATION ---------------------

    def _configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Nexora.Treeview",
            background=C["panel"],
            foreground=C["text"],
            fieldbackground=C["panel"],
            borderwidth=0,
            rowheight=38,
            font=(FONT, 10),
        )
        style.configure(
            "Nexora.Treeview.Heading",
            background=C["panel_alt"],
            foreground=C["cyan"],
            relief="flat",
            borderwidth=0,
            font=(FONT, 9, "bold"),
            padding=(10, 12),
        )
        style.map(
            "Nexora.Treeview",
            background=[("selected", "#34456C")],
            foreground=[("selected", C["white"])],
        )
        style.map(
            "Nexora.Treeview.Heading",
            background=[("active", C["panel_hover"])],
        )
        style.configure(
            "Nexora.TCombobox",
            fieldbackground=C["panel_alt"],
            background=C["panel_alt"],
            foreground=C["text"],
            arrowcolor=C["cyan"],
            bordercolor=C["border"],
            padding=9,
        )
        style.map(
            "Nexora.TCombobox",
            fieldbackground=[("readonly", C["panel_alt"])],
            foreground=[("readonly", C["text"])],
        )

    def _build_shell(self):
        self.sidebar = tk.Frame(self.root, bg=C["sidebar"], width=245)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = tk.Frame(self.root, bg=C["app"])
        self.main.pack(side="right", fill="both", expand=True)

        brand = tk.Frame(self.sidebar, bg=C["sidebar"])
        brand.pack(fill="x", padx=22, pady=(28, 30))

        tk.Label(
            brand, text="NEXORA", bg=C["sidebar"], fg=C["text"],
            font=(FONT, 25, "bold")
        ).pack(anchor="w")
        tk.Label(
            brand, text="✦  SMART LIBRARY PLATFORM",
            bg=C["sidebar"], fg=C["cyan"], font=(FONT, 8, "bold")
        ).pack(anchor="w", pady=(4, 0))

        tk.Frame(self.sidebar, bg=C["border"], height=1).pack(
            fill="x", padx=18, pady=(0, 18)
        )

        tk.Label(
            self.sidebar, text="WORKSPACE", bg=C["sidebar"],
            fg=C["dim"], font=(FONT, 8, "bold")
        ).pack(anchor="w", padx=24, pady=(0, 10))

        pages = [
            ("▦", "Dashboard", self.show_dashboard),
            ("▤", "Books", self.show_books),
            ("♙", "Members", self.show_members),
            ("⇄", "Borrow / Return", self.show_borrowing),
            ("◈", "Fine Management", self.show_fines),
            ("▥", "Analytics", self.show_analytics),
        ]

        for icon, label, command in pages:
            self._nav_button(icon, label, command)

        spacer = tk.Frame(self.sidebar, bg=C["sidebar"])
        spacer.pack(fill="both", expand=True)

        status = tk.Frame(
            self.sidebar, bg=C["panel"], highlightbackground=C["border"],
            highlightthickness=1
        )
        status.pack(fill="x", padx=15, pady=18)
        tk.Label(
            status, text="●  SYSTEM STATUS", bg=C["panel"],
            fg=C["green"], font=(FONT, 8, "bold")
        ).pack(anchor="w", padx=12, pady=(11, 3))
        tk.Label(
            status, text="MySQL connected on demand",
            bg=C["panel"], fg=C["muted"], font=(FONT, 8)
        ).pack(anchor="w", padx=12, pady=(0, 11))

    def _nav_button(self, icon, label, command):
        btn = tk.Button(
            self.sidebar,
            text=f"  {icon}     {label}",
            command=command,
            bg=C["sidebar"],
            fg=C["muted"],
            activebackground=C["panel_hover"],
            activeforeground=C["text"],
            relief="flat",
            bd=0,
            anchor="w",
            padx=18,
            pady=13,
            font=(FONT, 10, "bold"),
            cursor="hand2",
        )
        btn.pack(fill="x", padx=12, pady=3)
        self.nav_buttons[label] = btn

    def _set_active(self, page):
        self.active_page = page
        for name, button in self.nav_buttons.items():
            if name == page:
                button.configure(
                    bg=C["panel_hover"], fg=C["cyan"],
                    highlightthickness=1,
                    highlightbackground=C["purple_dark"],
                )
            else:
                button.configure(
                    bg=C["sidebar"], fg=C["muted"],
                    highlightthickness=0,
                )

    def clear(self):
        for widget in self.main.winfo_children():
            widget.destroy()

    def page_header(self, title, subtitle):
        self._set_active(title if title in self.nav_buttons else
                         ("Borrow / Return" if title == "Borrow / Return" else title))
        header = tk.Frame(self.main, bg=C["app"])
        header.pack(fill="x", padx=30, pady=(25, 20))

        left = tk.Frame(header, bg=C["app"])
        left.pack(side="left", fill="x", expand=True)

        tk.Label(
            left, text=title, bg=C["app"], fg=C["text"],
            font=(FONT, 24, "bold")
        ).pack(anchor="w")
        tk.Label(
            left, text=subtitle, bg=C["app"], fg=C["muted"],
            font=(FONT, 10)
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            header, text=date.today().strftime("%A  •  %d %B %Y"),
            bg=C["app"], fg=C["cyan"], font=(FONT, 9, "bold")
        ).pack(side="right", anchor="n", pady=7)

    def panel(self, parent, padx=0, pady=0):
        frame = tk.Frame(
            parent, bg=C["panel"],
            highlightbackground=C["border"], highlightthickness=1
        )
        if padx or pady:
            frame.pack(fill="both", expand=True, padx=padx, pady=pady)
        return frame

    def label(self, parent, text, size=10, color=None, bold=False, **kwargs):
        return tk.Label(
            parent, text=text, bg=kwargs.pop("bg", C["panel"]),
            fg=color or C["text"],
            font=(FONT, size, "bold" if bold else "normal"),
            **kwargs
        )

    def button(self, parent, text, command, color=None, fg=None, **kwargs):
        return tk.Button(
            parent, text=text, command=command,
            bg=color or C["purple_dark"],
            fg=fg or C["white"],
            activebackground=color or C["purple"],
            activeforeground=C["white"],
            relief="flat", bd=0, padx=15, pady=9,
            font=(FONT, 9, "bold"), cursor="hand2",
            **kwargs
        )

    def entry(self, parent, width=28, show=None):
        field = tk.Entry(
            parent, width=width, bg=C["panel_alt"], fg=C["text"],
            insertbackground=C["cyan"], relief="flat",
            highlightthickness=1, highlightbackground=C["border"],
            highlightcolor=C["purple"], font=(FONT, 10),
        )
        if show:
            field.configure(show=show)
        return field

    def tree(self, parent, columns, widths=None):
        wrapper = tk.Frame(parent, bg=C["panel"])
        wrapper.pack(fill="both", expand=True, padx=14, pady=14)

        tree = ttk.Treeview(
            wrapper, columns=columns, show="headings",
            style="Nexora.Treeview"
        )
        for index, column in enumerate(columns):
            tree.heading(column, text=column)
            tree.column(
                column,
                width=widths[index] if widths else 140,
                minwidth=65,
                anchor="w",
                stretch=True,
            )

        yscroll = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        xscroll = ttk.Scrollbar(wrapper, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        wrapper.rowconfigure(0, weight=1)
        wrapper.columnconfigure(0, weight=1)

        tree.tag_configure("even", background=C["panel"])
        tree.tag_configure("odd", background=C["panel_alt"])
        return tree

    def fill_tree(self, tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for index, row in enumerate(rows):
            tree.insert(
                "", "end", values=row,
                tags=("even" if index % 2 == 0 else "odd",)
            )

    # ---------------------------- DATABASE --------------------------

    def query(self, sql, args=()):
        conn = None
        cursor = None
        try:
            conn = db()
            cursor = conn.cursor()
            cursor.execute(sql, args)
            return cursor.fetchall()
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def execute(self, sql, args=(), many=False):
        conn = None
        cursor = None
        try:
            conn = db()
            cursor = conn.cursor()
            cursor.execute(sql, args)
            conn.commit()
            return cursor.lastrowid
        except Exception:
            if conn:
                conn.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if conn and conn.is_connected():
                conn.close()

    def db_error(self, error):
        messagebox.showerror(
            "Database connection / query error",
            f"{error}\n\nCheck that MySQL is running and the database "
            f"'{DB_CONFIG['database']}' exists."
        )

    # ---------------------------- DASHBOARD -------------------------

    def show_dashboard(self):
        self.clear()
        self.page_header("Dashboard", "Your library at a glance")

        try:
            total_books = self.query("SELECT COUNT(*) FROM Books")[0][0]
            members = self.query("SELECT COUNT(*) FROM Members")[0][0]
            borrowed = self.query(
                "SELECT COUNT(*) FROM Borrowing WHERE status='Borrowed'"
            )[0][0]
            returned = self.query(
                "SELECT COUNT(*) FROM Borrowing WHERE status='Returned'"
            )[0][0]
            fine = self.query(
                "SELECT COALESCE(SUM(amount),0) FROM Fine "
                "WHERE payment_status='Unpaid'"
            )[0][0] or 0
        except mysql.connector.Error as error:
            self.db_error(error)
            return

        stats = [
            ("TOTAL BOOKS", total_books, C["purple"], "▤"),
            ("MEMBERS", members, C["cyan"], "♙"),
            ("CURRENTLY BORROWED", borrowed, C["orange"], "⇄"),
            ("RETURNED BOOKS", returned, C["green"], "✓"),
            ("UNPAID FINES", f"₹{float(fine):,.2f}", C["red"], "₹"),
        ]

        cards = tk.Frame(self.main, bg=C["app"])
        cards.pack(fill="x", padx=25, pady=(0, 18))
        for name, value, accent, symbol in stats:
            card = tk.Frame(
                cards, bg=C["panel"], highlightbackground=C["border"],
                highlightthickness=1
            )
            card.pack(side="left", fill="both", expand=True, padx=5)
            tk.Frame(card, bg=accent, height=4).pack(fill="x")
            top = tk.Frame(card, bg=C["panel"])
            top.pack(fill="x", padx=14, pady=(13, 4))
            self.label(top, symbol, 16, accent, True).pack(side="right")
            self.label(card, name, 8, C["muted"], True).pack(
                anchor="w", padx=14, pady=(3, 2)
            )
            self.label(card, str(value), 20, C["text"], True).pack(
                anchor="w", padx=14, pady=(0, 15)
            )

        recent = self.panel(self.main)
        recent.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        heading = tk.Frame(recent, bg=C["panel"])
        heading.pack(fill="x", padx=18, pady=(16, 4))
        self.label(heading, "Recent Borrowing", 13, C["text"], True).pack(side="left")
        self.label(
            heading, "LATEST 10 RECORDS", 8, C["cyan"], True
        ).pack(side="right")

        tree = self.tree(
            recent,
            ("ID", "Member", "Book", "Borrow Date", "Return Date", "Status"),
            [65, 160, 270, 130, 130, 110],
        )
        try:
            rows = self.query(
                "SELECT b.borrow_id,m.member_name,bk.title,b.borrow_date,"
                "b.return_date,b.status FROM Borrowing b "
                "JOIN Members m ON b.member_id=m.member_id "
                "JOIN Books bk ON b.book_id=bk.book_id "
                "ORDER BY b.borrow_id DESC LIMIT 10"
            )
            self.fill_tree(tree, rows)
        except mysql.connector.Error as error:
            self.db_error(error)

    # ---------------------------- BOOKS ------------------------------

    def show_books(self):
        self.clear()
        self.page_header("Books", "Manage the collection, authors and available copies")

        toolbar = tk.Frame(self.main, bg=C["app"])
        toolbar.pack(fill="x", padx=30, pady=(0, 12))
        self.label(toolbar, "Search books", 9, C["muted"], True).pack(side="left")
        search = self.entry(toolbar, 28)
        search.pack(side="left", padx=(10, 8), ipady=8)

        panel = self.panel(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        tree = self.tree(
            panel, ("ID", "Title", "Author", "Category", "Available Copies"),
            [65, 300, 190, 170, 140]
        )

        def load():
            try:
                term = search.get().strip()
                if term:
                    rows = self.query(
                        "SELECT b.book_id,b.title,COALESCE(a.author_name,'Unknown'),"
                        "b.category,b.available_copies FROM Books b "
                        "LEFT JOIN Authors a ON b.author_id=a.author_id "
                        "WHERE b.title LIKE %s OR b.category LIKE %s "
                        "OR a.author_name LIKE %s ORDER BY b.book_id",
                        (f"%{term}%", f"%{term}%", f"%{term}%")
                    )
                else:
                    rows = self.query(
                        "SELECT b.book_id,b.title,COALESCE(a.author_name,'Unknown'),"
                        "b.category,b.available_copies FROM Books b "
                        "LEFT JOIN Authors a ON b.author_id=a.author_id "
                        "ORDER BY b.book_id"
                    )
                self.fill_tree(tree, rows)
            except mysql.connector.Error as error:
                self.db_error(error)

        self.button(toolbar, "Search", load, C["purple_dark"]).pack(side="left", padx=3)
        self.button(
            toolbar, "Clear",
            lambda: (search.delete(0, tk.END), load()),
            C["panel_hover"], C["text"]
        ).pack(side="left", padx=3)
        self.button(toolbar, "Refresh", load, C["blue"]).pack(side="left", padx=3)
        self.button(toolbar, "+ Add Book", self.add_book, C["green"], C["app"]).pack(
            side="right"
        )
        search.bind("<Return>", lambda _event: load())
        load()

    def add_book(self):
        window, body = self.dialog("Add a new book", "Enter the book information")
        fields = {}
        for name in ("Title", "Author", "Category", "Available Copies"):
            self.label(body, name, 9, C["muted"], True).pack(anchor="w", pady=(10, 4))
            field = self.entry(body, 35)
            field.pack(fill="x", ipady=8)
            fields[name] = field
        fields["Available Copies"].insert(0, "1")

        def save():
            values = {key: field.get().strip() for key, field in fields.items()}
            if not all(values.values()):
                messagebox.showwarning("Required", "Please complete all fields.", parent=window)
                return
            try:
                copies = int(values["Available Copies"])
                if copies < 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning(
                    "Invalid copies", "Available copies must be a non-negative whole number.",
                    parent=window
                )
                return

            conn = None
            cur = None
            try:
                conn = db()
                cur = conn.cursor()
                cur.execute(
                    "SELECT author_id FROM Authors WHERE author_name=%s",
                    (values["Author"],)
                )
                author = cur.fetchone()
                if author:
                    author_id = author[0]
                else:
                    cur.execute(
                        "INSERT INTO Authors(author_name) VALUES(%s)",
                        (values["Author"],)
                    )
                    author_id = cur.lastrowid

                cur.execute(
                    "INSERT INTO Books(title,author_id,category,available_copies) "
                    "VALUES(%s,%s,%s,%s)",
                    (values["Title"], author_id, values["Category"], copies)
                )
                conn.commit()
                window.destroy()
                self.show_books()
                messagebox.showinfo("Success", "Book added successfully.")
            except mysql.connector.Error as error:
                if conn:
                    conn.rollback()
                self.db_error(error)
            finally:
                if cur:
                    cur.close()
                if conn and conn.is_connected():
                    conn.close()

        self.button(body, "Save Book", save, C["purple_dark"]).pack(fill="x", pady=(22, 5))

    # ---------------------------- MEMBERS ----------------------------

    def show_members(self):
        self.clear()
        self.page_header("Members", "Manage library members and contact details")

        toolbar = tk.Frame(self.main, bg=C["app"])
        toolbar.pack(fill="x", padx=30, pady=(0, 12))
        self.label(toolbar, "Search members", 9, C["muted"], True).pack(side="left")
        search = self.entry(toolbar, 28)
        search.pack(side="left", padx=(10, 8), ipady=8)

        panel = self.panel(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=(0, 25))
        tree = self.tree(panel, ("ID", "Member Name", "Phone"), [80, 300, 200])

        def load():
            try:
                term = search.get().strip()
                if term:
                    rows = self.query(
                        "SELECT member_id,member_name,phone FROM Members "
                        "WHERE member_name LIKE %s OR phone LIKE %s "
                        "ORDER BY member_id DESC",
                        (f"%{term}%", f"%{term}%")
                    )
                else:
                    rows = self.query(
                        "SELECT member_id,member_name,phone FROM Members "
                        "ORDER BY member_id DESC"
                    )
                self.fill_tree(tree, rows)
            except mysql.connector.Error as error:
                self.db_error(error)

        self.button(toolbar, "Search", load).pack(side="left", padx=3)
        self.button(
            toolbar, "Clear",
            lambda: (search.delete(0, tk.END), load()),
            C["panel_hover"], C["text"]
        ).pack(side="left", padx=3)
        self.button(toolbar, "Refresh", load, C["blue"]).pack(side="left", padx=3)
        self.button(
            toolbar, "Delete Selected",
            lambda: self.delete_member(tree, load),
            C["red"]
        ).pack(side="right", padx=3)
        self.button(
            toolbar, "+ Add Member", self.add_member, C["green"], C["app"]
        ).pack(side="right", padx=3)
        search.bind("<Return>", lambda _event: load())
        load()

    def add_member(self):
        window, body = self.dialog("Add a library member", "Create a new member record")
        self.label(body, "Member Name", 9, C["muted"], True).pack(anchor="w", pady=(12, 4))
        name = self.entry(body, 35)
        name.pack(fill="x", ipady=8)
        self.label(body, "Phone", 9, C["muted"], True).pack(anchor="w", pady=(12, 4))
        phone = self.entry(body, 35)
        phone.pack(fill="x", ipady=8)

        def save():
            member_name = name.get().strip()
            if not member_name:
                messagebox.showwarning("Required", "Enter a member name.", parent=window)
                return
            try:
                self.execute(
                    "INSERT INTO Members(member_name,phone) VALUES(%s,%s)",
                    (member_name, phone.get().strip())
                )
                window.destroy()
                self.show_members()
                messagebox.showinfo("Success", "Member added successfully.")
            except mysql.connector.Error as error:
                self.db_error(error)

        self.button(body, "Save Member", save, C["purple_dark"]).pack(fill="x", pady=(22, 5))

    def delete_member(self, tree, reload_callback=None):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select member", "Select a member first.")
            return
        member_id = tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirm deletion", "Delete this member?"):
            return
        conn = None
        cur = None
        try:
            conn = db()
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM Borrowing WHERE member_id=%s",
                (member_id,)
            )
            if cur.fetchone()[0] > 0:
                messagebox.showerror(
                    "Cannot delete",
                    "This member has borrowing records and cannot be deleted."
                )
                return
            cur.execute("DELETE FROM Members WHERE member_id=%s", (member_id,))
            conn.commit()
            if reload_callback:
                reload_callback()
            messagebox.showinfo("Success", "Member deleted successfully.")
        except mysql.connector.Error as error:
            if conn:
                conn.rollback()
            self.db_error(error)
        finally:
            if cur:
                cur.close()
            if conn and conn.is_connected():
                conn.close()

    # ------------------------- BORROW / RETURN -----------------------

    def show_borrowing(self):
        self.clear()
        self.page_header("Borrow / Return", "Issue books and keep borrowing records up to date")

        toolbar = tk.Frame(self.main, bg=C["app"])
        toolbar.pack(fill="x", padx=30, pady=(0, 12))
        self.button(
            toolbar, "+ Borrow a Book", self.borrow_book, C["purple_dark"]
        ).pack(side="left")

        panel = self.panel(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=(0, 15))
        tree = self.tree(
            panel,
            ("ID", "Member", "Book", "Borrow Date", "Return Date", "Status"),
            [65, 180, 280, 135, 135, 110]
        )

        try:
            rows = self.query(
                "SELECT b.borrow_id,m.member_name,bk.title,b.borrow_date,"
                "b.return_date,b.status FROM Borrowing b "
                "JOIN Members m ON b.member_id=m.member_id "
                "JOIN Books bk ON b.book_id=bk.book_id "
                "ORDER BY b.borrow_id DESC"
            )
            self.fill_tree(tree, rows)
        except mysql.connector.Error as error:
            self.db_error(error)

        actions = tk.Frame(self.main, bg=C["app"])
        actions.pack(fill="x", padx=30, pady=(0, 22))
        self.button(
            actions, "Return Selected Book",
            lambda: self.return_book(tree), C["green"], C["app"]
        ).pack(side="right")

    def borrow_book(self):
        window, body = self.dialog("Borrow a book", "Choose a registered member and an available book")
        self.label(body, "Member", 9, C["muted"], True).pack(anchor="w", pady=(12, 4))
        member_box = ttk.Combobox(body, state="readonly", style="Nexora.TCombobox")
        member_box.pack(fill="x")
        self.label(body, "Book", 9, C["muted"], True).pack(anchor="w", pady=(14, 4))
        book_box = ttk.Combobox(body, state="readonly", style="Nexora.TCombobox")
        book_box.pack(fill="x")

        try:
            members = self.query(
                "SELECT member_id,member_name FROM Members ORDER BY member_name"
            )
            books = self.query(
                "SELECT book_id,title,available_copies FROM Books "
                "WHERE available_copies>0 ORDER BY title"
            )
        except mysql.connector.Error as error:
            window.destroy()
            self.db_error(error)
            return

        member_box["values"] = [f"{row[0]} - {row[1]}" for row in members]
        book_box["values"] = [
            f"{row[0]} - {row[1]} (Available: {row[2]})" for row in books
        ]

        def save():
            if not member_box.get() or not book_box.get():
                messagebox.showwarning(
                    "Required", "Select both a member and a book.", parent=window
                )
                return
            member_id = int(member_box.get().split(" - ", 1)[0])
            book_id = int(book_box.get().split(" - ", 1)[0])

            conn = None
            cur = None
            try:
                conn = db()
                cur = conn.cursor()
                cur.execute(
                    "SELECT available_copies FROM Books WHERE book_id=%s FOR UPDATE",
                    (book_id,)
                )
                available = cur.fetchone()
                if not available or available[0] <= 0:
                    messagebox.showerror(
                        "Unavailable", "This book is no longer available.", parent=window
                    )
                    return

                cur.execute(
                    "INSERT INTO Borrowing(book_id,member_id,borrow_date,status) "
                    "VALUES(%s,%s,%s,'Borrowed')",
                    (book_id, member_id, date.today())
                )
                borrow_id = cur.lastrowid
                cur.execute(
                    "UPDATE Books SET available_copies=available_copies-1 "
                    "WHERE book_id=%s",
                    (book_id,)
                )
                cur.execute(
                    "INSERT INTO Fine(borrow_id,amount,payment_status) "
                    "VALUES(%s,0,'No Fine')",
                    (borrow_id,)
                )
                conn.commit()
                window.destroy()
                self.show_borrowing()
                messagebox.showinfo("Success", "Book borrowed successfully.")
            except mysql.connector.Error as error:
                if conn:
                    conn.rollback()
                self.db_error(error)
            finally:
                if cur:
                    cur.close()
                if conn and conn.is_connected():
                    conn.close()

        self.button(body, "Confirm Borrowing", save, C["purple_dark"]).pack(
            fill="x", pady=(22, 5)
        )

    def return_book(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select borrowing", "Select a borrowing record.")
            return
        values = tree.item(selected[0], "values")
        borrow_id = values[0]
        if str(values[5]).lower() == "returned":
            messagebox.showinfo("Already returned", "This book has already been returned.")
            return
        if not messagebox.askyesno("Confirm return", "Mark this book as returned?"):
            return

        conn = None
        cur = None
        try:
            conn = db()
            cur = conn.cursor()
            cur.execute(
                "SELECT book_id,status FROM Borrowing WHERE borrow_id=%s FOR UPDATE",
                (borrow_id,)
            )
            record = cur.fetchone()
            if not record or record[1] == "Returned":
                messagebox.showinfo("Already returned", "This record is already returned.")
                return
            cur.execute(
                "UPDATE Borrowing SET return_date=%s,status='Returned' "
                "WHERE borrow_id=%s",
                (date.today(), borrow_id)
            )
            cur.execute(
                "UPDATE Books SET available_copies=available_copies+1 "
                "WHERE book_id=%s",
                (record[0],)
            )
            conn.commit()
            self.show_borrowing()
            messagebox.showinfo("Success", "Book returned successfully.")
        except mysql.connector.Error as error:
            if conn:
                conn.rollback()
            self.db_error(error)
        finally:
            if cur:
                cur.close()
            if conn and conn.is_connected():
                conn.close()

    # ---------------------------- FINES ------------------------------

    def show_fines(self):
        self.clear()
        self.page_header("Fine Management", "Review outstanding fines and payment status")

        panel = self.panel(self.main)
        panel.pack(fill="both", expand=True, padx=30, pady=(0, 15))
        tree = self.tree(
            panel, ("Fine ID", "Member", "Book", "Amount", "Payment Status"),
            [85, 210, 300, 130, 160]
        )
        try:
            rows = self.query(
                "SELECT f.fine_id,m.member_name,b.title,f.amount,f.payment_status "
                "FROM Fine f JOIN Borrowing br ON f.borrow_id=br.borrow_id "
                "JOIN Members m ON br.member_id=m.member_id "
                "JOIN Books b ON br.book_id=b.book_id ORDER BY f.fine_id DESC"
            )
            self.fill_tree(tree, rows)
        except mysql.connector.Error as error:
            self.db_error(error)

        actions = tk.Frame(self.main, bg=C["app"])
        actions.pack(fill="x", padx=30, pady=(0, 22))
        self.button(
            actions, "Mark Selected as Paid",
            lambda: self.pay_fine(tree), C["green"], C["app"]
        ).pack(side="right")

    def pay_fine(self, tree):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select fine", "Select a fine record first.")
            return
        values = tree.item(selected[0], "values")
        fine_id, status = values[0], values[4]
        if status in ("Paid", "No Fine"):
            messagebox.showinfo("Completed", "This fine is already completed.")
            return
        if not messagebox.askyesno("Confirm payment", "Mark this fine as paid?"):
            return
        try:
            self.execute(
                "UPDATE Fine SET payment_status='Paid' WHERE fine_id=%s",
                (fine_id,)
            )
            self.show_fines()
            messagebox.showinfo("Success", "Fine marked as paid.")
        except mysql.connector.Error as error:
            self.db_error(error)

    # ---------------------------- ANALYTICS --------------------------

    def show_analytics(self):
        self.clear()
        self.page_header("Analytics", "Visual insights into your library activity")

        area = tk.Frame(self.main, bg=C["app"])
        area.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        area.grid_columnconfigure(0, weight=1, uniform="chart")
        area.grid_columnconfigure(1, weight=1, uniform="chart")
        area.grid_rowconfigure(0, weight=1)

        borrowing_panel = self.panel(area)
        borrowing_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        category_panel = self.panel(area)
        category_panel.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        self.label(
            borrowing_panel, "Borrowing Status", 13, C["text"], True
        ).pack(anchor="w", padx=18, pady=(17, 2))
        self.label(
            borrowing_panel, "Current distribution of borrowing records",
            9, C["muted"]
        ).pack(anchor="w", padx=18)

        self.label(
            category_panel, "Books by Category", 13, C["text"], True
        ).pack(anchor="w", padx=18, pady=(17, 2))
        self.label(
            category_panel, "Collection breakdown by category",
            9, C["muted"]
        ).pack(anchor="w", padx=18)

        self.borrowing_chart_frame = tk.Frame(borrowing_panel, bg=C["panel"])
        self.borrowing_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.category_chart_frame = tk.Frame(category_panel, bg=C["panel"])
        self.category_chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_borrowing_chart()
        self.create_category_chart()

    def _chart_message(self, parent, message):
        self.label(parent, message, 10, C["muted"]).pack(expand=True)

    def create_borrowing_chart(self):
        for widget in self.borrowing_chart_frame.winfo_children():
            widget.destroy()
        try:
            data = self.query(
                "SELECT status,COUNT(*) FROM Borrowing GROUP BY status"
            )
        except mysql.connector.Error as error:
            self._chart_message(self.borrowing_chart_frame, str(error))
            return
        if not data:
            self._chart_message(self.borrowing_chart_frame, "No borrowing data available")
            return

        labels = [str(row[0]) for row in data]
        values = [int(row[1]) for row in data]
        fig = Figure(figsize=(5.5, 4.0), dpi=100, facecolor=C["panel"])
        ax = fig.add_subplot(111)
        ax.set_facecolor(C["panel"])
        bars = ax.bar(
            labels, values,
            color=[C["purple"], C["cyan"], C["orange"], C["green"]][:len(values)],
            width=0.55
        )
        ax.set_ylabel("Number of records", color=C["muted"], fontsize=9)
        ax.tick_params(colors=C["muted"], labelsize=9)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(C["border"])
        ax.spines["bottom"].set_color(C["border"])
        ax.grid(axis="y", color=C["border"], alpha=0.55, linewidth=0.7)
        ax.set_axisbelow(True)
        for bar, value in zip(bars, values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                str(value), ha="center", va="bottom",
                color=C["text"], fontsize=9, fontweight="bold"
            )
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.borrowing_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def create_category_chart(self):
        for widget in self.category_chart_frame.winfo_children():
            widget.destroy()
        try:
            data = self.query(
                "SELECT category,COUNT(*) FROM Books "
                "GROUP BY category ORDER BY COUNT(*) DESC"
            )
        except mysql.connector.Error as error:
            self._chart_message(self.category_chart_frame, str(error))
            return
        if not data:
            self._chart_message(self.category_chart_frame, "No category data available")
            return

        labels = [str(row[0] or "Uncategorised") for row in data]
        values = [int(row[1]) for row in data]
        palette = [
            C["purple"], C["cyan"], C["blue"], C["green"],
            C["orange"], C["red"], "#D28BFF", "#7BD9C5"
        ]
        fig = Figure(figsize=(5.5, 4.0), dpi=100, facecolor=C["panel"])
        ax = fig.add_subplot(111)
        ax.set_facecolor(C["panel"])
        wedges, _texts, _autotexts = ax.pie(
            values,
            labels=None,
            autopct="%1.0f%%",
            startangle=90,
            colors=palette[:len(values)] if len(values) <= len(palette) else None,
            pctdistance=0.72,
            textprops={"color": C["text"], "fontsize": 8},
            wedgeprops={"width": 0.42, "edgecolor": C["panel"], "linewidth": 2},
        )
        ax.legend(
            wedges, labels, loc="lower center",
            bbox_to_anchor=(0.5, -0.08), ncol=2,
            frameon=False, labelcolor=C["muted"], fontsize=8
        )
        ax.set_aspect("equal")
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.category_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    # ---------------------------- DIALOG -----------------------------

    def dialog(self, title, subtitle):
        window = tk.Toplevel(self.root)
        window.title(f"NEXORA | {title}")
        window.configure(bg=C["app"])
        window.geometry("500x560")
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()

        outer = tk.Frame(
            window, bg=C["panel"],
            highlightbackground=C["border"], highlightthickness=1
        )
        outer.pack(fill="both", expand=True, padx=18, pady=18)

        self.label(outer, "NEXORA", 9, C["cyan"], True).pack(
            anchor="w", padx=25, pady=(22, 5)
        )
        self.label(outer, title, 19, C["text"], True).pack(
            anchor="w", padx=25
        )
        self.label(outer, subtitle, 9, C["muted"]).pack(
            anchor="w", padx=25, pady=(4, 15)
        )
        body = tk.Frame(outer, bg=C["panel"])
        body.pack(fill="both", expand=True, padx=25, pady=(0, 22))
        window.bind("<Escape>", lambda _event: window.destroy())
        return window, body


# ---------------------------------------------------------------------
# LOGIN
# ---------------------------------------------------------------------
def launch_app(root):
    for widget in root.winfo_children():
        widget.destroy()
    root.geometry("1440x850")
    root.minsize(1120, 700)
    LibraryApp(root)


def show_login(root):
    root.title("NEXORA | Secure Access")
    root.geometry("540x650")
    root.minsize(540, 650)
    root.configure(bg=C["app"])
    root.resizable(False, False)

    background = tk.Frame(root, bg=C["app"])
    background.pack(fill="both", expand=True)

    tk.Label(
        background, text="✦", bg=C["app"], fg=C["purple"],
        font=(FONT, 28, "bold")
    ).pack(pady=(35, 0))
    tk.Label(
        background, text="NEXORA", bg=C["app"], fg=C["text"],
        font=(FONT, 31, "bold")
    ).pack(pady=(0, 2))
    tk.Label(
        background, text="SMART LIBRARY PLATFORM",
        bg=C["app"], fg=C["cyan"], font=(FONT, 9, "bold")
    ).pack(pady=(0, 22))

    card = tk.Frame(
        background, bg=C["panel"],
        highlightbackground=C["border"], highlightthickness=1
    )
    card.pack(fill="x", padx=55, pady=10)

    tk.Label(
        card, text="Welcome back", bg=C["panel"], fg=C["text"],
        font=(FONT, 20, "bold")
    ).pack(anchor="w", padx=35, pady=(32, 5))
    tk.Label(
        card, text="Sign in to continue to your library workspace.",
        bg=C["panel"], fg=C["muted"], font=(FONT, 9)
    ).pack(anchor="w", padx=35, pady=(0, 24))

    tk.Label(
        card, text="USERNAME", bg=C["panel"], fg=C["muted"],
        font=(FONT, 8, "bold")
    ).pack(anchor="w", padx=35)
    username = tk.Entry(
        card, bg=C["panel_alt"], fg=C["text"], insertbackground=C["cyan"],
        relief="flat", highlightthickness=1, highlightbackground=C["border"],
        highlightcolor=C["purple"], font=(FONT, 11)
    )
    username.pack(fill="x", padx=35, pady=(7, 18), ipady=11)

    tk.Label(
        card, text="PASSWORD", bg=C["panel"], fg=C["muted"],
        font=(FONT, 8, "bold")
    ).pack(anchor="w", padx=35)
    password = tk.Entry(
        card, show="•", bg=C["panel_alt"], fg=C["text"],
        insertbackground=C["cyan"], relief="flat",
        highlightthickness=1, highlightbackground=C["border"],
        highlightcolor=C["purple"], font=(FONT, 11)
    )
    password.pack(fill="x", padx=35, pady=(7, 22), ipady=11)

    def login(_event=None):
        if (
            username.get().strip() == ADMIN_USERNAME
            and password.get() == ADMIN_PASSWORD
        ):
            launch_app(root)
        else:
            messagebox.showerror(
                "Access denied", "The username or password is incorrect.",
                parent=root
            )
            password.delete(0, tk.END)
            password.focus_set()

    tk.Button(
        card, text="SIGN IN   →", command=login,
        bg=C["purple_dark"], fg=C["white"],
        activebackground=C["purple"], activeforeground=C["white"],
        relief="flat", bd=0, font=(FONT, 10, "bold"),
        cursor="hand2", pady=13
    ).pack(fill="x", padx=35, pady=(0, 28))

    tk.Label(
        background,
        text="SECURE LIBRARY WORKSPACE  •  MYSQL EDITION",
        bg=C["app"], fg=C["dim"], font=(FONT, 8, "bold")
    ).pack(pady=20)

    root.bind("<Return>", login)
    username.focus_set()


if __name__ == "__main__":
    app_root = tk.Tk()
    show_login(app_root)
    app_root.mainloop()
