from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from categories.models import Category
from authors.models import Author
from posts.models import Post


class Command(BaseCommand):
    help = 'Seed the database with sample blog data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting blog seed...'))
        
        # Limpiar datos existentes
        self.stdout.write('Clearing existing data...')
        Post.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        
        # Crear categorías
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Technology', 'is_active': True},
            {'name': 'Programming', 'is_active': True},
            {'name': 'DevOps', 'is_active': True},
            {'name': 'Cloud Computing', 'is_active': True},
            {'name': 'Security', 'is_active': True},
        ]
        
        categories = []
        for cat_data in categories_data:
            category = Category.objects.create(**cat_data)
            categories.append(category)
            self.stdout.write(f'  ✓ Created category: {category.name}')
        
        # Crear autores
        self.stdout.write('Creating authors...')
        authors_data = [
            {
                'display_name': 'John Developer',
                'email': 'john.dev@example.com',
                'bio': 'Senior software engineer with 10+ years of experience in web development.',
                'is_active': True
            },
            {
                'display_name': 'Jane Architect',
                'email': 'jane.arch@example.com',
                'bio': 'Cloud architect specializing in microservices and distributed systems.',
                'is_active': True
            },
            {
                'display_name': 'Mike DevOps',
                'email': 'mike.devops@example.com',
                'bio': 'DevOps engineer passionate about automation and CI/CD pipelines.',
                'is_active': True
            },
        ]
        
        authors = []
        for author_data in authors_data:
            author = Author.objects.create(**author_data)
            authors.append(author)
            self.stdout.write(f'  ✓ Created author: {author.display_name}')
        
        # Crear posts
        self.stdout.write('Creating posts...')
        posts_data = [
            {
                'title': 'Introduction to Microservices Architecture',
                'body': 'Microservices architecture is a design pattern where applications are structured as a collection of loosely coupled services. This approach offers several benefits including improved scalability, flexibility, and easier maintenance. In this post, we will explore the fundamental concepts of microservices and how they differ from monolithic architectures.',
                'status': 'published'
            },
            {
                'title': 'Getting Started with Docker Containers',
                'body': 'Docker has revolutionized the way we deploy applications by providing lightweight, portable containers. This comprehensive guide will walk you through the basics of containerization, including how to create Dockerfiles, build images, and run containers. We will also cover best practices for production deployments.',
                'status': 'published'
            },
            {
                'title': 'REST API Design Best Practices',
                'body': 'Designing robust and scalable REST APIs requires careful consideration of various factors. In this article, we discuss best practices including proper HTTP method usage, status codes, versioning strategies, and authentication patterns. Learn how to build APIs that are intuitive and easy to maintain.',
                'status': 'published'
            },
            {
                'title': 'Understanding JWT Authentication',
                'body': 'JSON Web Tokens (JWT) provide a stateless authentication mechanism that is widely used in modern web applications. This post explains how JWTs work, their structure, and how to implement them securely in your applications. We will also discuss common pitfalls and security considerations.',
                'status': 'published'
            },
            {
                'title': 'Redis Caching Strategies',
                'body': 'Redis is a powerful in-memory data store that can significantly improve application performance. This guide covers various caching strategies including cache-aside, write-through, and write-behind patterns. Learn when to use each strategy and how to implement them effectively.',
                'status': 'published'
            },
            {
                'title': 'PostgreSQL Performance Optimization',
                'body': 'Database performance is crucial for application success. This article explores PostgreSQL optimization techniques including index strategies, query optimization, and connection pooling. Discover how to identify and resolve performance bottlenecks in your database.',
                'status': 'published'
            },
            {
                'title': 'Building Scalable Django Applications',
                'body': 'Django is a powerful web framework that can scale to handle millions of requests. This comprehensive guide covers scaling strategies including database optimization, caching, asynchronous task processing, and horizontal scaling. Learn how to build Django apps that can grow with your business.',
                'status': 'published'
            },
            {
                'title': 'Introduction to Kubernetes',
                'body': 'Kubernetes has become the standard for container orchestration. This beginner-friendly guide introduces core Kubernetes concepts including pods, services, deployments, and ingress. Learn how to deploy and manage containerized applications at scale.',
                'status': 'published'
            },
            {
                'title': 'API Gateway Patterns',
                'body': 'API gateways serve as a single entry point for microservices architectures. This post explores common gateway patterns including request routing, authentication, rate limiting, and protocol translation. Understand how to design effective API gateway solutions.',
                'status': 'published'
            },
            {
                'title': 'Monitoring Microservices with Prometheus',
                'body': 'Effective monitoring is essential for microservices. This guide covers how to use Prometheus for metrics collection and Grafana for visualization. Learn how to set up alerts, create dashboards, and track the health of your distributed systems.',
                'status': 'published'
            },
            {
                'title': 'Implementing Service Discovery',
                'body': 'Service discovery is a critical component of microservices architecture. This article explains different service discovery patterns including client-side and server-side discovery. Learn how to implement service registration and health checking.',
                'status': 'published'
            },
            {
                'title': 'Event-Driven Architecture with Message Queues',
                'body': 'Event-driven architectures enable loose coupling between services. This post explores message queue patterns using RabbitMQ and Kafka. Learn how to design asynchronous communication patterns and handle event ordering and delivery guarantees.',
                'status': 'published'
            },
            {
                'title': 'Securing Microservices',
                'body': 'Security is paramount in distributed systems. This comprehensive guide covers microservices security including authentication, authorization, encryption, and secret management. Learn how to implement defense in depth and secure service-to-service communication.',
                'status': 'published'
            },
            {
                'title': 'CI/CD Pipelines for Microservices',
                'body': 'Continuous integration and deployment are essential for rapid development. This article covers how to build CI/CD pipelines for microservices using tools like Jenkins, GitLab CI, and GitHub Actions. Learn automated testing and deployment strategies.',
                'status': 'published'
            },
            {
                'title': 'Database Per Service Pattern',
                'body': 'The database per service pattern ensures service independence in microservices. This post explores the benefits and challenges of this pattern, including data consistency, transactions, and queries across services. Learn when and how to implement this pattern.',
                'status': 'published'
            },
            {
                'title': 'Load Balancing Strategies',
                'body': 'Load balancing distributes traffic across multiple service instances. This guide covers various load balancing algorithms including round-robin, least connections, and weighted distribution. Learn how to implement effective load balancing for high availability.',
                'status': 'published'
            },
            {
                'title': 'Distributed Tracing with Jaeger',
                'body': 'Understanding request flows in microservices requires distributed tracing. This article introduces Jaeger for tracing requests across services. Learn how to instrument your code, visualize traces, and identify performance bottlenecks.',
                'status': 'published'
            },
            {
                'title': 'GraphQL vs REST APIs',
                'body': 'Choosing between GraphQL and REST depends on your use case. This comparative analysis explores the strengths and weaknesses of both approaches. Learn when to use GraphQL and when REST is the better choice for your project.',
                'status': 'published'
            },
            {
                'title': 'Handling Failures in Distributed Systems',
                'body': 'Failures are inevitable in distributed systems. This post covers resilience patterns including circuit breakers, retries, timeouts, and bulkheads. Learn how to build fault-tolerant microservices that gracefully handle failures.',
                'status': 'published'
            },
            {
                'title': 'Serverless Architecture Patterns',
                'body': 'Serverless computing eliminates infrastructure management. This guide explores serverless patterns using AWS Lambda, Azure Functions, and Google Cloud Functions. Learn when serverless is appropriate and how to design serverless applications.',
                'status': 'published'
            },
            {
                'title': 'API Versioning Strategies',
                'body': 'API versioning ensures backward compatibility as your API evolves. This article discusses various versioning strategies including URL versioning, header versioning, and content negotiation. Learn how to manage API changes without breaking clients.',
                'status': 'draft'
            },
            {
                'title': 'Implementing CQRS Pattern',
                'body': 'Command Query Responsibility Segregation (CQRS) separates read and write operations. This post explains the CQRS pattern, its benefits, and implementation strategies. Learn when CQRS is appropriate for your architecture.',
                'status': 'draft'
            },
            {
                'title': 'Service Mesh with Istio',
                'body': 'Service meshes manage service-to-service communication. This comprehensive guide introduces Istio for traffic management, security, and observability. Learn how to implement a service mesh in your Kubernetes cluster.',
                'status': 'draft'
            },
            {
                'title': 'Zero Trust Security Model',
                'body': 'Zero trust security assumes no implicit trust. This article explores zero trust principles and how to implement them in microservices. Learn about mutual TLS, identity verification, and least privilege access.',
                'status': 'draft'
            },
            {
                'title': 'Chaos Engineering Principles',
                'body': 'Chaos engineering tests system resilience by introducing controlled failures. This post covers chaos engineering principles and tools like Chaos Monkey. Learn how to build confidence in your system\'s reliability through controlled experiments.',
                'status': 'draft'
            },
            {
                'title': 'Multi-Tenancy in Microservices',
                'body': 'Multi-tenancy allows serving multiple customers from a single deployment. This guide explores multi-tenancy patterns including database isolation, schema separation, and row-level security. Learn how to design secure multi-tenant systems.',
                'status': 'draft'
            },
            {
                'title': 'Blue-Green Deployments',
                'body': 'Blue-green deployments enable zero-downtime releases. This article explains the blue-green deployment pattern and how to implement it. Learn how to safely roll out new versions and quickly rollback if needed.',
                'status': 'draft'
            },
            {
                'title': 'API Rate Limiting Techniques',
                'body': 'Rate limiting protects APIs from abuse and ensures fair usage. This post covers rate limiting algorithms including token bucket, leaky bucket, and sliding window. Learn how to implement effective rate limiting.',
                'status': 'draft'
            },
            {
                'title': 'WebSocket Communication Patterns',
                'body': 'WebSockets enable real-time bidirectional communication. This guide explores WebSocket patterns for microservices including connection management, scaling, and fallback strategies. Learn how to build real-time features.',
                'status': 'draft'
            },
            {
                'title': 'Infrastructure as Code with Terraform',
                'body': 'Infrastructure as Code (IaC) treats infrastructure configuration as code. This comprehensive guide introduces Terraform for managing cloud resources. Learn how to version, test, and deploy infrastructure changes safely.',
                'status': 'draft'
            },
        ]
        
        now = timezone.now()
        for i, post_data in enumerate(posts_data):
            # Asignar autor y categoría aleatoriamente
            post_data['author'] = random.choice(authors)
            post_data['category'] = random.choice(categories)
            
            # Asignar fecha de publicación para posts publicados
            if post_data['status'] == 'published':
                days_ago = random.randint(1, 60)
                post_data['published_at'] = now - timedelta(days=days_ago)
                post_data['views'] = random.randint(50, 5000)
            
            post = Post.objects.create(**post_data)
            self.stdout.write(f'  ✓ Created post: {post.title} ({post.status})')
        
        # Estadísticas finales
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(status='published').count()
        draft_posts = Post.objects.filter(status='draft').count()
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('Seed completed successfully!'))
        self.stdout.write(self.style.SUCCESS('='*50))
        self.stdout.write(f'Categories created: {len(categories)}')
        self.stdout.write(f'Authors created: {len(authors)}')
        self.stdout.write(f'Total posts: {total_posts}')
        self.stdout.write(f'  - Published: {published_posts}')
        self.stdout.write(f'  - Drafts: {draft_posts}')
        self.stdout.write(self.style.SUCCESS('='*50))
