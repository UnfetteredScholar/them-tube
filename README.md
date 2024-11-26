# Them-Tube API 📹  
**Them-Tube** is a modern video streaming API designed for seamless integration with your projects. Built using **FastAPI**, it offers high performance, scalability, and ease of use. The backend leverages **MongoDB** for data storage, **UV (backed by Astral)** for dependency management, and **Docker** for streamlined deployment.  

## Features 🚀  
- **Video Uploading & Streaming**: Upload and stream videos in various formats.  
- **User Management**: User registration, authentication, and profile management.  
- **Video Metadata**: Store and retrieve metadata such as titles, descriptions, and tags.  
- **Search & Filtering**: Search videos based on keywords, tags, and more.  
- **Playlist Management**: Create and manage playlists for personalized viewing experiences.  
- **Scalable Architecture**: Built to handle growing traffic with ease.  

---

## Tech Stack 🛠️  
- **FastAPI**: High-performance Python web framework for API development.  
- **MongoDB**: NoSQL database for efficient storage and retrieval of video data and metadata.  
- **UV**: Dependency management for better environment consistency.  
- **Docker**: Containerization for simplified deployment and scalability.  

---

## Getting Started  

### Prerequisites  
- Python 3.9+  
- Docker  
- A MongoDB instance (local or cloud)  

### Installation  

1. **Clone the repository**:  
   ```bash  
   git clone https://github.com/UnfetteredScholar/them-tube.git 
   cd them-tube
   ```  

2. **Install Dependencies**:  
   Using **astral.sh UV**:  
   ```bash  
   uv sync  
   ```  

3. **Set up Environment Variables**:  
   Create a `.env` file in the root directory with the **.env.example** file 


4. **Run Locally**:  
   ```bash  
   uv run uvicorn main:app
   ```  
   This will start the FastAPI server on `http://localhost:8000`.  

---

## Deployment  

1. **Build Docker Image**:  
   ```bash  
   docker build -t them-tube-api .  
   ```  

2. **Run with Docker**:  
   ```bash  
   docker compose up 
   ```  

---

## API Documentation  

- Once the server is running, interactive API documentation is available at:  
  - **Swagger UI**: `http://localhost:8000/docs`  
  - **ReDoc**: `http://localhost:8000/redoc`  

---

## Contributing  

1. Fork the repository.  
2. Create a feature branch:  
   ```bash  
   git checkout -b feature/your-feature-name  
   ```  
3. Commit your changes and push:  
   ```bash  
   git commit -m "Add your feature"  
   git push origin feature/your-feature-name  
   ```  
4. Open a Pull Request.  

---

## License 📜  
This project is licensed under the [MIT License](LICENSE).  

---  

**Happy Streaming!** 🎥