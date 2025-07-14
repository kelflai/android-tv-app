class AndroidTVApp {
    constructor() {
        this.currentUser = null;
        this.currentSection = 'channels';
        this.currentCategory = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.checkAuth();
    }

    bindEvents() {
        // Login form
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        // Logout button
        document.getElementById('logoutBtn').addEventListener('click', () => {
            this.logout();
        });

        // Navigation tabs
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchSection(e.target.dataset.section);
            });
        });

        // Close modal
        document.getElementById('closeModal').addEventListener('click', () => {
            this.closeVideoModal();
        });

        // Close modal on background click
        document.getElementById('videoModal').addEventListener('click', (e) => {
            if (e.target.id === 'videoModal') {
                this.closeVideoModal();
            }
        });
    }

    async checkAuth() {
        try {
            const response = await fetch('/api/check');
            const data = await response.json();
            
            if (data.authenticated) {
                this.currentUser = data.user;
                this.showMainApp();
            } else {
                this.showLoginScreen();
            }
        } catch (error) {
            console.error('Error checking auth:', error);
            this.showLoginScreen();
        }
    }

    async login() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('loginError');

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                this.currentUser = data.user;
                this.showMainApp();
                errorDiv.style.display = 'none';
            } else {
                errorDiv.textContent = data.error;
                errorDiv.style.display = 'block';
            }
        } catch (error) {
            console.error('Login error:', error);
            errorDiv.textContent = 'Erro de conexão. Tente novamente.';
            errorDiv.style.display = 'block';
        }
    }

    async logout() {
        try {
            await fetch('/api/logout', { method: 'POST' });
            this.currentUser = null;
            this.showLoginScreen();
        } catch (error) {
            console.error('Logout error:', error);
        }
    }

    showLoginScreen() {
        document.getElementById('loginScreen').style.display = 'flex';
        document.getElementById('mainApp').style.display = 'none';
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
    }

    showMainApp() {
        document.getElementById('loginScreen').style.display = 'none';
        document.getElementById('mainApp').style.display = 'block';
        document.getElementById('welcomeUser').textContent = `Bem-vindo, ${this.currentUser.username}!`;
        this.loadContent();
    }

    switchSection(section) {
        // Update active tab
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-section="${section}"]`).classList.add('active');

        // Update active section
        document.querySelectorAll('.content-section').forEach(sec => {
            sec.classList.remove('active');
        });
        document.getElementById(section).classList.add('active');

        this.currentSection = section;
        this.currentCategory = null;
        this.loadContent();
    }

    async loadContent() {
        this.showLoading();
        
        try {
            await this.loadCategories();
            await this.loadItems();
        } catch (error) {
            console.error('Error loading content:', error);
            this.showError('Erro ao carregar conteúdo');
        } finally {
            this.hideLoading();
        }
    }

    async loadCategories() {
        const typeMap = {
            'channels': 'channel',
            'movies': 'movie',
            'series': 'series'
        };

        const response = await fetch(`/api/categories?type=${typeMap[this.currentSection]}`);
        const categories = await response.json();

        const containerMap = {
            'channels': 'channelCategories',
            'movies': 'movieCategories',
            'series': 'seriesCategories'
        };

        const container = document.getElementById(containerMap[this.currentSection]);
        container.innerHTML = '';

        // Add "All" button
        const allBtn = document.createElement('button');
        allBtn.className = 'category-btn active';
        allBtn.textContent = 'Todos';
        allBtn.addEventListener('click', () => {
            this.selectCategory(null);
        });
        container.appendChild(allBtn);

        // Add category buttons
        categories.forEach(category => {
            const btn = document.createElement('button');
            btn.className = 'category-btn';
            btn.textContent = category.name;
            btn.addEventListener('click', () => {
                this.selectCategory(category.id);
            });
            container.appendChild(btn);
        });
    }

    selectCategory(categoryId) {
        this.currentCategory = categoryId;
        
        // Update active category button
        const containerMap = {
            'channels': 'channelCategories',
            'movies': 'movieCategories',
            'series': 'seriesCategories'
        };
        
        const container = document.getElementById(containerMap[this.currentSection]);
        container.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        if (categoryId) {
            event.target.classList.add('active');
        } else {
            container.querySelector('.category-btn').classList.add('active');
        }

        this.loadItems();
    }

    async loadItems() {
        const endpointMap = {
            'channels': '/api/channels',
            'movies': '/api/movies',
            'series': '/api/series'
        };

        let url = endpointMap[this.currentSection];
        if (this.currentCategory) {
            url += `?category_id=${this.currentCategory}`;
        }

        const response = await fetch(url);
        const items = await response.json();

        const gridMap = {
            'channels': 'channelGrid',
            'movies': 'movieGrid',
            'series': 'seriesGrid'
        };

        const grid = document.getElementById(gridMap[this.currentSection]);
        grid.innerHTML = '';

        if (items.length === 0) {
            grid.innerHTML = '<p style="text-align: center; color: rgba(255,255,255,0.7); grid-column: 1/-1;">Nenhum conteúdo encontrado</p>';
            return;
        }

        items.forEach(item => {
            const itemElement = this.createContentItem(item);
            grid.appendChild(itemElement);
        });
    }

    createContentItem(item) {
        const div = document.createElement('div');
        div.className = 'content-item';
        
        const imageUrl = item.logo_url || item.poster_url || 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDIwMCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMTUwIiBmaWxsPSIjMzMzIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iNzUiIGZpbGw9IiM2NjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCI+U2VtIEltYWdlbTwvdGV4dD4KPC9zdmc+';
        
        div.innerHTML = `
            <img src="${imageUrl}" alt="${item.title || item.name}" onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDIwMCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHdpZHRoPSIyMDAiIGhlaWdodD0iMTUwIiBmaWxsPSIjMzMzIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iNzUiIGZpbGw9IiM2NjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGR5PSIuM2VtIiBmb250LWZhbWlseT0ic2Fucy1zZXJpZiIgZm9udC1zaXplPSIxNCI+U2VtIEltYWdlbTwvdGV4dD4KPC9zdmc+'">
            <div class="content-item-info">
                <div class="content-item-title">${item.title || item.name}</div>
                <div class="content-item-category">${item.category ? item.category.name : 'Sem categoria'}</div>
            </div>
        `;

        div.addEventListener('click', () => {
            this.playContent(item);
        });

        return div;
    }

    playContent(item) {
        const videoUrl = item.stream_url || item.video_url;
        
        if (!videoUrl) {
            this.showError('URL de vídeo não disponível');
            return;
        }

        const modal = document.getElementById('videoModal');
        const video = document.getElementById('videoPlayer');
        const title = document.getElementById('videoTitle');

        title.textContent = item.title || item.name;
        video.src = videoUrl;
        modal.classList.add('active');
    }

    closeVideoModal() {
        const modal = document.getElementById('videoModal');
        const video = document.getElementById('videoPlayer');
        
        video.pause();
        video.src = '';
        modal.classList.remove('active');
    }

    showLoading() {
        document.getElementById('loading').style.display = 'block';
        document.getElementById('error').style.display = 'none';
    }

    hideLoading() {
        document.getElementById('loading').style.display = 'none';
    }

    showError(message) {
        const errorDiv = document.getElementById('error');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        this.hideLoading();
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AndroidTVApp();
});

