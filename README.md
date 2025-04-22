# 💰 Segment Manager App

A desktop budgeting app built with [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) and MySQL that helps users manage financial segments and transactions visually. 

Each user can define **segments** (like "Savings", "Food", "Entertainment"), assign percentages of their total balance, and see it all in a dynamic pie chart — including sub-segments and nested breakdowns.

---

## 📦 Features

- ✅ **User Authentication**
  - Register, login, and session persistence.
  
- 🧾 **Transaction Management**
  - View and track user transactions with amount, source, and date.

- 🎯 **Segment Manager**
  - Create, update, delete, and nest segments.
  - Each segment has:
    - Name
    - Color
    - Percentage of total balance
    - Optional parent segment

- 🥧 **Pie Chart Visualization**
  - Real-time pie chart showing how balance is allocated.
  - Click a segment to drill down into its sub-segments.
  - Handles incomplete allocations with a "Remaining" slice.

- 🎨 **CustomTkinter UI**
  - Responsive layout with scrollable frames.
  - Styled segment buttons and color-coded UI.

---

## 🛠️ Tech Stack

- **Frontend:** CustomTkinter (Python)
- **Backend:** MySQL,PYTHON
- **Visualization:** Matplotlib

---

## 🧰 Installation

### 1. Clone the repository

```bash
git clone https://github.com/PetrTaller/S-E-Finance
cd S-E-Finance
```

### 2. Install dependencies

### 3. Set up the MySQL database
Create a database (e.g. segment_app)

Import the SQL schema:

```
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    balance DECIMAL(10, 2)
);

CREATE TABLE segments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(255),
    color VARCHAR(7),
    percentage DECIMAL(5, 2),
    parent_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (parent_id) REFERENCES segments(id)
);

CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    amount DECIMAL(10, 2),
    source VARCHAR(255),
    date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
Update your database credentials in the classes currently no config.

🚀 Running the App

python app.py

🧠 Design Structure
pgsql

/code
├── app.py              # Main app window
├── /window
│   ├── login.py        # Login/register screen
│   └── main.py         # Main dashboard (segment view)
├── /segments
│   └── segments.py     # Segment logic & database operations
├── /transactions
│   └── transactions.py # Transaction logic
├── /saved
│   ├── users.json      # (Optional) cached user data
│   └── session.json    # current session tracking



### 📌 TODOs & Ideas

 Edit transactions

 Add charts over time

 Mobile version with Kivy or web via Streamlit

 Sync with external bank APIs

### 📄 License
MIT License

### 🙌 Credits
Created with 💙 by [PETR TALLET] — feel free to fork, improve, and share!








