from src.models.user import db
from src.models.category import Category
from src.models.channel import Channel
from src.models.movie import Movie
from src.models.series import Series
from src.models.episode import Episode

class ContentManager:
    @staticmethod
    def create_sample_content():
        """Create sample content for demonstration"""
        try:
            # Create sample categories
            categories_data = [
                {'name': 'Notícias', 'type': 'channel'},
                {'name': 'Esportes', 'type': 'channel'},
                {'name': 'Entretenimento', 'type': 'channel'},
                {'name': 'Ação', 'type': 'movie'},
                {'name': 'Comédia', 'type': 'movie'},
                {'name': 'Drama', 'type': 'movie'},
                {'name': 'Drama', 'type': 'series'},
                {'name': 'Comédia', 'type': 'series'},
                {'name': 'Ficção Científica', 'type': 'series'},
            ]
            
            category_map = {}
            for cat_data in categories_data:
                existing_cat = Category.query.filter_by(name=cat_data['name'], type=cat_data['type']).first()
                if not existing_cat:
                    new_cat = Category(name=cat_data['name'], type=cat_data['type'])
                    db.session.add(new_cat)
                    db.session.flush()
                    category_map[f"{cat_data['type']}_{cat_data['name']}"] = new_cat.id
                else:
                    category_map[f"{cat_data['type']}_{cat_data['name']}"] = existing_cat.id
            
            # Create sample channels
            channels_data = [
                {
                    'name': 'Globo News',
                    'stream_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4',
                    'logo_url': 'https://via.placeholder.com/200x150/FF6B6B/FFFFFF?text=Globo+News',
                    'category': 'Notícias'
                },
                {
                    'name': 'SporTV',
                    'stream_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4',
                    'logo_url': 'https://via.placeholder.com/200x150/4ECDC4/FFFFFF?text=SporTV',
                    'category': 'Esportes'
                },
                {
                    'name': 'Multishow',
                    'stream_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_5mb.mp4',
                    'logo_url': 'https://via.placeholder.com/200x150/45B7D1/FFFFFF?text=Multishow',
                    'category': 'Entretenimento'
                }
            ]
            
            for channel_data in channels_data:
                existing_channel = Channel.query.filter_by(name=channel_data['name']).first()
                if not existing_channel:
                    category_id = category_map[f"channel_{channel_data['category']}"]
                    new_channel = Channel(
                        name=channel_data['name'],
                        stream_url=channel_data['stream_url'],
                        logo_url=channel_data['logo_url'],
                        category_id=category_id
                    )
                    db.session.add(new_channel)
            
            # Create sample movies
            movies_data = [
                {
                    'title': 'Vingadores: Ultimato',
                    'description': 'Os heróis mais poderosos da Terra enfrentam Thanos.',
                    'poster_url': 'https://via.placeholder.com/200x300/FF6B6B/FFFFFF?text=Vingadores',
                    'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4',
                    'category': 'Ação'
                },
                {
                    'title': 'Se Beber, Não Case',
                    'description': 'Uma comédia sobre uma despedida de solteiro que deu errado.',
                    'poster_url': 'https://via.placeholder.com/200x300/4ECDC4/FFFFFF?text=Se+Beber',
                    'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_2mb.mp4',
                    'category': 'Comédia'
                },
                {
                    'title': 'Cidade de Deus',
                    'description': 'Drama brasileiro sobre a vida na favela.',
                    'poster_url': 'https://via.placeholder.com/200x300/45B7D1/FFFFFF?text=Cidade+de+Deus',
                    'video_url': 'https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_5mb.mp4',
                    'category': 'Drama'
                }
            ]
            
            for movie_data in movies_data:
                existing_movie = Movie.query.filter_by(title=movie_data['title']).first()
                if not existing_movie:
                    category_id = category_map[f"movie_{movie_data['category']}"]
                    new_movie = Movie(
                        title=movie_data['title'],
                        description=movie_data['description'],
                        poster_url=movie_data['poster_url'],
                        video_url=movie_data['video_url'],
                        category_id=category_id
                    )
                    db.session.add(new_movie)
            
            # Create sample series
            series_data = [
                {
                    'title': 'Breaking Bad',
                    'description': 'Um professor de química se torna fabricante de drogas.',
                    'poster_url': 'https://via.placeholder.com/200x300/FF6B6B/FFFFFF?text=Breaking+Bad',
                    'category': 'Drama'
                },
                {
                    'title': 'The Office',
                    'description': 'Comédia sobre o dia a dia de um escritório.',
                    'poster_url': 'https://via.placeholder.com/200x300/4ECDC4/FFFFFF?text=The+Office',
                    'category': 'Comédia'
                },
                {
                    'title': 'Stranger Things',
                    'description': 'Crianças enfrentam criaturas sobrenaturais.',
                    'poster_url': 'https://via.placeholder.com/200x300/45B7D1/FFFFFF?text=Stranger+Things',
                    'category': 'Ficção Científica'
                }
            ]
            
            for series_data_item in series_data:
                existing_series = Series.query.filter_by(title=series_data_item['title']).first()
                if not existing_series:
                    category_id = category_map[f"series_{series_data_item['category']}"]
                    new_series = Series(
                        title=series_data_item['title'],
                        description=series_data_item['description'],
                        poster_url=series_data_item['poster_url'],
                        category_id=category_id
                    )
                    db.session.add(new_series)
                    db.session.flush()
                    
                    # Add sample episodes
                    for season in range(1, 3):
                        for episode in range(1, 6):
                            new_episode = Episode(
                                series_id=new_series.id,
                                season_number=season,
                                episode_number=episode,
                                title=f'Episódio {episode}',
                                description=f'Descrição do episódio {episode} da temporada {season}',
                                video_url='https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4'
                            )
                            db.session.add(new_episode)
            
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"Error creating sample content: {e}")
            return False
    
    @staticmethod
    def get_content_stats():
        """Get content statistics"""
        return {
            'categories': Category.query.count(),
            'channels': Channel.query.count(),
            'movies': Movie.query.count(),
            'series': Series.query.count(),
            'episodes': Episode.query.count()
        }
    
    @staticmethod
    def clear_all_content():
        """Clear all content from database"""
        try:
            Episode.query.delete()
            Series.query.delete()
            Movie.query.delete()
            Channel.query.delete()
            Category.query.delete()
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing content: {e}")
            return False

