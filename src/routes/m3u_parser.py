import re
import requests
from urllib.parse import urljoin, urlparse
from src.models.user import db
from src.models.category import Category
from src.models.channel import Channel
from src.models.movie import Movie
from src.models.series import Series

class M3UParser:
    def __init__(self):
        self.channels = []
        self.movies = []
        self.series = []

    def parse_m3u_content(self, content):
        """Parse M3U content and extract channel/movie/series information"""
        lines = content.strip().split('\n')
        current_item = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('#EXTINF:'):
                # Parse EXTINF line
                current_item = self._parse_extinf_line(line)
            elif line and not line.startswith('#') and current_item:
                # This is the URL line
                current_item['url'] = line
                self._categorize_item(current_item)
                current_item = {}

    def _parse_extinf_line(self, line):
        """Parse EXTINF line to extract metadata"""
        item = {}
        
        # Extract duration (not used but part of format)
        duration_match = re.search(r'#EXTINF:([^,]*),', line)
        
        # Extract title (everything after the last comma)
        title_match = re.search(r',(.*)$', line)
        if title_match:
            item['title'] = title_match.group(1).strip()
        
        # Extract attributes like tvg-logo, group-title, etc.
        attributes = re.findall(r'(\w+(?:-\w+)*)="([^"]*)"', line)
        for attr, value in attributes:
            if attr == 'tvg-logo':
                item['logo_url'] = value
            elif attr == 'group-title':
                item['category'] = value
            elif attr == 'tvg-name':
                item['name'] = value
        
        return item

    def _categorize_item(self, item):
        """Categorize item as channel, movie, or series based on patterns"""
        title = item.get('title', '').lower()
        category = item.get('category', '').lower()
        
        # Determine if it's a movie, series, or channel
        if any(keyword in title for keyword in ['filme', 'movie', 'cinema']):
            item['type'] = 'movie'
            self.movies.append(item)
        elif any(keyword in title for keyword in ['serie', 'series', 'temporada', 'season', 'episodio', 'episode']):
            item['type'] = 'series'
            self.series.append(item)
        else:
            item['type'] = 'channel'
            self.channels.append(item)

    def load_from_url(self, url):
        """Load M3U content from URL"""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            self.parse_m3u_content(response.text)
            return True
        except Exception as e:
            print(f"Error loading M3U from URL {url}: {e}")
            return False

    def load_from_file(self, file_path):
        """Load M3U content from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.parse_m3u_content(content)
            return True
        except Exception as e:
            print(f"Error loading M3U from file {file_path}: {e}")
            return False

    def save_to_database(self):
        """Save parsed content to database"""
        try:
            # Create default categories if they don't exist
            default_categories = {
                'channel': ['Geral', 'Notícias', 'Esportes', 'Entretenimento'],
                'movie': ['Ação', 'Comédia', 'Drama', 'Terror'],
                'series': ['Drama', 'Comédia', 'Ação', 'Documentário']
            }
            
            category_map = {}
            for content_type, cat_names in default_categories.items():
                for cat_name in cat_names:
                    existing_cat = Category.query.filter_by(name=cat_name, type=content_type).first()
                    if not existing_cat:
                        new_cat = Category(name=cat_name, type=content_type)
                        db.session.add(new_cat)
                        db.session.flush()
                        category_map[f"{content_type}_{cat_name}"] = new_cat.id
                    else:
                        category_map[f"{content_type}_{cat_name}"] = existing_cat.id
            
            # Save channels
            for channel_data in self.channels:
                category_name = channel_data.get('category', 'Geral')
                category_id = self._get_or_create_category(category_name, 'channel', category_map)
                
                channel = Channel(
                    name=channel_data.get('title', 'Canal sem nome'),
                    stream_url=channel_data.get('url', ''),
                    logo_url=channel_data.get('logo_url'),
                    category_id=category_id
                )
                db.session.add(channel)
            
            # Save movies
            for movie_data in self.movies:
                category_name = movie_data.get('category', 'Ação')
                category_id = self._get_or_create_category(category_name, 'movie', category_map)
                
                movie = Movie(
                    title=movie_data.get('title', 'Filme sem nome'),
                    video_url=movie_data.get('url', ''),
                    poster_url=movie_data.get('logo_url'),
                    category_id=category_id
                )
                db.session.add(movie)
            
            # Save series (simplified - treating each entry as a series)
            for series_data in self.series:
                category_name = series_data.get('category', 'Drama')
                category_id = self._get_or_create_category(category_name, 'series', category_map)
                
                series = Series(
                    title=series_data.get('title', 'Série sem nome'),
                    poster_url=series_data.get('logo_url'),
                    category_id=category_id
                )
                db.session.add(series)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error saving to database: {e}")
            return False

    def _get_or_create_category(self, category_name, content_type, category_map):
        """Get or create category and return its ID"""
        key = f"{content_type}_{category_name}"
        if key in category_map:
            return category_map[key]
        
        # Create new category
        new_cat = Category(name=category_name, type=content_type)
        db.session.add(new_cat)
        db.session.flush()
        category_map[key] = new_cat.id
        return new_cat.id

