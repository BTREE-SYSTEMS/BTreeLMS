# BTree LMS - Learning Management System  

## 🚀 Introduction  
**BTree LMS** is a full-fledged Learning Management System designed for students at **BTree Systems**. It allows students to enroll in courses, track their progress, take assessments, and receive certifications.  

## 🛠️ Tech Stack  
- **Backend**: Django (Python)  
- **Frontend**: Html/CSS/JavaScript  
- **Database**: PostgreSQL 
- **Authentication**: OAuth  
- **Deployment**: Docker, AWS / Render  

## 🎯 Features  
✅ User Authentication & Role-Based Access  
✅ Course Management (Create, Update, Delete)  
✅ Student Enrollment & Progress Tracking  
✅ Video Lectures & Study Materials  
✅ Quizzes & Assessments  
✅ Certification upon Completion  
✅ Admin Dashboard for Monitoring  

## 📦 Installation  

### **Backend Setup (Django)**
1. Clone the repository:  
   ```sh
   git clone https://github.com/BtreeSystems/BTree-LMS.git
   cd BTree-LMS/backend
   ```
2. Create a virtual environment:  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:  
   ```sh
   pip install -r requirements.txt
   ```
4. Apply migrations:  
   ```sh
   python manage.py migrate
   ```
5. Run the development server:  
   ```sh
   python manage.py runserver
   ```

### **Frontend Setup (React)**
1. Navigate to the frontend directory:  
   ```sh
   cd ../frontend
   ```
2. Install dependencies:  
   ```sh
   npm install
   ```
3. Start the development server:  
   ```sh
   npm start
   ```

## 🔗 API Documentation  
The API documentation is available at:  
📌 `http://localhost:8000/api/docs` (If using Django REST Framework Swagger UI)  

## 📝 Contributing  
We welcome contributions! Follow these steps:  
1. Fork the repository  
2. Create a new branch: `git checkout -b feature-branch`  
3. Commit changes: `git commit -m "Added new feature"`  
4. Push to the branch: `git push origin feature-branch`  
5. Open a Pull Request  

## 📜 License  
This project is licensed under the MIT License.  

## 👨‍💻 DEV Team  
**Varun**,
**Valluvan**
