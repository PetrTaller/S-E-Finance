# 💰 S&E Finance (Smart and Easy Finance)

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
create table user(
id INT AUTO_INCREMENT PRIMARY KEY,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL,
balance FLOAT NOT NULL
);
CREATE TABLE segment (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    parent_id INT DEFAULT NULL,
    name VARCHAR(255) NOT NULL,
    color VARCHAR(7) NOT NULL,
    percentage DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (parent_id) REFERENCES segment(id)
);
CREATE TABLE transaction(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    source VARCHAR(255) NOT NULL,
    date datetime NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(id)
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

### SCREENSHOT
![image](https://github.com/user-attachments/assets/ab5277e5-2c9f-4c1c-9658-9ed2ac343eac)


### 📌 TODOs & Ideas

 Edit transactions that will add only to a certain segment

 Add charts over time

 Mobile version with Kivy or web via Streamlit

 Sync with external bank APIs

 Add a new to segment creation, that uses money instead of percentage

 Config

 Goals of money for the user to add to

 Fix reccuring transactions

### 📄 License
MIT License

### 🙌 Credits
Created with 💙 by [PETR TALLER] — feel free to fork, improve, and share!








