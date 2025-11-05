# ⚛️ Frontend Service (React)

> 📋 **Estado**: Pendiente de implementación

Interfaz de usuario construida con React para interactuar con los microservicios.

## 🎯 Objetivos

- Interfaz moderna y responsive
- Autenticación con JWT
- CRUD de posts de blog
- Gestión de perfil de usuario
- Dashboard administrativo

## 🛠️ Stack Tecnológico Planeado

- **Framework**: React 18
- **Build Tool**: Vite
- **Routing**: React Router v6
- **State Management**: Zustand o Redux Toolkit
- **HTTP Client**: Axios
- **UI Framework**: Tailwind CSS + shadcn/ui
- **Forms**: React Hook Form + Zod
- **Auth**: JWT con refresh token rotation

## 📁 Estructura Propuesta

```
frontend/
├── public/
│   └── assets/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginForm.jsx
│   │   │   └── RegisterForm.jsx
│   │   ├── blog/
│   │   │   ├── PostCard.jsx
│   │   │   ├── PostList.jsx
│   │   │   └── PostEditor.jsx
│   │   ├── common/
│   │   │   ├── Header.jsx
│   │   │   ├── Footer.jsx
│   │   │   └── Navbar.jsx
│   │   └── layout/
│   │       └── MainLayout.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── Blog.jsx
│   │   ├── PostDetail.jsx
│   │   └── Profile.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   └── blogService.js
│   ├── store/
│   │   ├── authSlice.js
│   │   └── blogSlice.js
│   ├── utils/
│   │   ├── constants.js
│   │   └── validators.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── usePosts.js
│   ├── App.jsx
│   └── main.jsx
├── .env.example
├── Dockerfile
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## 🚀 Setup Inicial (Cuando se implemente)

```bash
# Crear proyecto con Vite
npm create vite@latest frontend -- --template react

cd frontend

# Instalar dependencias
npm install react-router-dom axios zustand
npm install -D tailwindcss postcss autoprefixer

# Configurar Tailwind
npx tailwindcss init -p

# Levantar servidor de desarrollo
npm run dev
```

## 🔗 Integración con Backend

### API Client (services/api.js)

```javascript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token JWT
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refreshToken');
        const { data } = await axios.post(
          `${API_BASE_URL}:8000/api/token/refresh/`,
          { refresh: refreshToken }
        );
        
        localStorage.setItem('accessToken', data.access);
        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        
        return api(originalRequest);
      } catch (err) {
        // Refresh token expirado, logout
        localStorage.clear();
        window.location.href = '/login';
      }
    }
    
    return Promise.reject(error);
  }
);

export default api;
```

### Auth Service (services/authService.js)

```javascript
import api from './api';

const AUTH_URL = 'http://localhost:8000/api';

export const authService = {
  async register(userData) {
    const { data } = await api.post(`${AUTH_URL}/register/`, userData);
    return data;
  },
  
  async login(credentials) {
    const { data } = await api.post(`${AUTH_URL}/token/`, credentials);
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);
    return data;
  },
  
  async getProfile() {
    const { data } = await api.get(`${AUTH_URL}/me/`);
    return data;
  },
  
  logout() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },
};
```

### Blog Service (services/blogService.js)

```javascript
import api from './api';

const BLOG_URL = 'http://localhost:8001/api';

export const blogService = {
  async getPosts(params = {}) {
    const { data } = await api.get(`${BLOG_URL}/posts/`, { params });
    return data;
  },
  
  async getPost(slug) {
    const { data } = await api.get(`${BLOG_URL}/posts/${slug}/`);
    return data;
  },
  
  async getCategories() {
    const { data } = await api.get(`${BLOG_URL}/categories/`);
    return data;
  },
  
  async createPost(postData) {
    const { data } = await api.post(`${BLOG_URL}/posts/`, postData);
    return data;
  },
  
  async updatePost(slug, postData) {
    const { data } = await api.put(`${BLOG_URL}/posts/${slug}/`, postData);
    return data;
  },
  
  async deletePost(slug) {
    await api.delete(`${BLOG_URL}/posts/${slug}/`);
  },
};
```

## 🎨 Componentes Principales

### LoginForm.jsx

```jsx
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../../services/authService';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    
    try {
      await authService.login({ email, password });
      navigate('/');
    } catch (err) {
      setError('Credenciales inválidas');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <div className="text-red-500">{error}</div>}
      
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        required
      />
      
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Contraseña"
        required
      />
      
      <button type="submit">Iniciar Sesión</button>
    </form>
  );
}
```

### PostList.jsx

```jsx
import { useEffect, useState } from 'react';
import { blogService } from '../../services/blogService';
import PostCard from './PostCard';

export default function PostList() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const data = await blogService.getPosts({ page });
        setPosts(data.results);
      } catch (error) {
        console.error('Error fetching posts:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchPosts();
  }, [page]);

  if (loading) return <div>Cargando...</div>;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {posts.map((post) => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
```

## 🐳 Dockerfile

```dockerfile
# Multi-stage build
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## ⚙️ Variables de Entorno

```env
# .env.example
VITE_API_URL=http://localhost
VITE_AUTH_SERVICE=http://localhost:8000
VITE_BLOG_SERVICE=http://localhost:8001
VITE_EMAIL_SERVICE=http://localhost:8002
```

## 🧪 Testing

```bash
# Instalar dependencias de testing
npm install -D vitest @testing-library/react @testing-library/jest-dom

# Ejecutar tests
npm run test

# Coverage
npm run test:coverage
```

## 📦 Build para Producción

```bash
# Build
npm run build

# Preview build localmente
npm run preview

# Docker build
docker build -t frontend:latest .
docker run -p 3000:80 frontend:latest
```

## 🔗 Referencias

- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [Tailwind CSS](https://tailwindcss.com/)
- [React Router](https://reactrouter.com/)

---

📌 **Nota**: Este servicio está pendiente de implementación. La estructura y código son propuestas iniciales.
