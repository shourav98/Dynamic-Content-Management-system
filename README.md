# Dynamic Content Management System

A high-performance, interactive educational platform built with **Django 5.2.13**. This system provides a seamless, Microsoft Word-style rich text experience with seamless, AJAX-driven multimedia integration natively connected to the article text.

## 🚀 Key Features
* **Hierarchical Structure:** Utilizes `django-mptt` for infinite nesting of Subjects/Categories with a drag-and-drop admin panel.
* **Rich Text Editing:** Full integration of `django-ckeditor` for advanced formatting (bold, italic, underline, highlighting, etc.).
* **Dynamic Multimedia Modals:** Universal Bootstrap 5 modal system fetching content (Text, Image, Audio, Local Video, YouTube) purely via AJAX on-demand.
* **Inline Interactivity:** Triggers secondary modal containing explanatory text and imagery completely built within the body paragraphs.
* **Streamlined UI:** Eliminates the static page reload mechanisms ensuring a flawless modern UX.
* **Instant Demo Data:** Simple management command to inject rich, interactive test data in one command.

## 🛠️ Technology Stack
* **Backend:** Python, Django 5.2.13
* **Database:** SQLite (default), extensible to PostgreSQL.
* **Frontend:** Vanilla JS, Bootstrap 5, Custom CSS
* **Core Libraries:** `django-mptt`, `django-ckeditor`, `Pillow`

## ⚙️ Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Dynamic-Content-Management-system.git
   cd Dynamic-Content-Management-system
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # source venv/bin/activate    # Mac/Linux
   ```

3. **Install Requirements:**
   ```bash
   pip install django django-mptt django-ckeditor pillow
   ```

4. **Initialize Database & Migrate:**
   ```bash
   cd content_management_system
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Load Interactive Demo Data:**
   ```bash
   python manage.py load_demo_data
   ```

6. **Create Superuser (Admin Access):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```
   *Visit `http://127.0.0.1:8000/` to test the frontend and `http://127.0.0.1:8000/admin/` to edit content!*

---
*Built as a professional Job Assignment demonstrating mastery of Django routing, AJAX, dynamic DOM updates, and MPTT hierarchy logic.*
