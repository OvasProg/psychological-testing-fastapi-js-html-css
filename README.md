# Psychological Testing Web App

This is a full-stack web application for psychological testing through expressive drawing. Built with HTML, CSS, JavaScript, and Python (FastAPI), the app guides users through timed drawing tasks based on emotional prompts and displays results based on drawing data analysis.

---

## 🧠 Features

- Drawing tool testing page
- Color and brush size selection
- 13 psychological topics with timed drawing sessions
- Real-time data streaming using WebSocket
- Backend analysis (functionality excluded here)
- Final results displayed in a downloadable table
- Language translation support (i18n)

---

## ⚙️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, FastAPI
- **Real-time Data**: WebSocket
- **Language Support**: i18n

---

## 🚧 Missing Components

⚠️ Note: The backend calculation logic is excluded from this repository due to intellectual property and patent restrictions. The related function is intentionally left blank.

---

## 📄 Page Structure

- `drawing-page-1.html` – Test and get familiar with the drawing tools
- `palette-page.html` – Select from 13 colors and adjust pencil size
- `trialogue-page.html` – React to 13 emotional topics via timed drawings
- `results.html` – View and download the psychological testing results
- `main.py` – Backend FastAPI server (calculation function is blank)

---

## 📦 Installation & Run (Development)

1. Clone the repository:
```bash
git clone https://github.com/OvasProg/psychological-testing-fastapi-js-html-css.git
```
2.	Navigate to the project directory and install dependencies:
```bash
cd project
uvicorn main:app --reload
```
3.	Open the HTML files in a browser (e.g., start with drawing-page-1.html).

---

## 📝 License

This project is licensed under the MIT License. See the LICENSE file for details.


---

## 📬 Contact

For questions, suggestions, or collaborations, feel free to reach out via GitHub.
