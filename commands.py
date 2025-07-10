from models import db, Submission, User, Role

from datetime import datetime
def init_commands(app):
    @app.cli.command('db-init')
    def db_init():
        """Initialize the database."""
        db.create_all()
        print('Database initialized!')

    @app.cli.command('create-dummy-data')
    def create_dummy_data():
        """Create dummy submissions for testing without authentication."""
        # Create dummy submissions
        submissions = [
            Submission(
                artist_name='Obscure Artist 1',
                track_title='Hidden Gem 1',
                url='https://bandcamp.com/track1',
                description='A rare find from the underground.',
                genre='Experimental',
                region='USA'
            ),
            Submission(
                artist_name='Obscure Artist 2',
                track_title='Hidden Gem 2',
                url='https://soundcloud.com/track2',
                description='You probably never heard this.',
                genre='Ambient',
                region='UK'
            ),
            Submission(
                artist_name='Unknown Band',
                track_title='Lost in Time',
                url='https://youtube.com/watch?v=test123',
                description='A forgotten masterpiece.',
                genre='Post-Rock',
                region='Canada'
            ),
            Submission(
                artist_name='Underground Collective',
                track_title='Digital Dreams',
                url='https://spotify.com/track/underground',
                description='Electronic exploration.',
                genre='IDM',
                region='Germany'
            ),
        ]
        for sub in submissions:
            if not Submission.query.filter_by(url=sub.url).first():
                db.session.add(sub)
        db.session.commit()
        print('Dummy submissions created!')

    @app.cli.command('create-test-accounts')
    def create_test_accounts():
        """Create hardcoded test accounts for each role."""
        # Create roles if they don't exist
        admin_role = Role.query.filter_by(name='Admin').first()
        if not admin_role:
            admin_role = Role(name='Admin')
            db.session.add(admin_role)
        
        user_role = Role.query.filter_by(name='User').first()
        if not user_role:
            user_role = Role(name='User')
            db.session.add(user_role)
        
        db.session.commit()

        # Create test users for each role
        test_users = [
            {
                'username': 'user1',
                'email': 'user@test.com',
                'password': 'user1',
                'role': user_role,
                'description': 'Regular user account'
            },
            {
                'username': 'admin',
                'email': 'admin@test.com', 
                'password': 'admin1',
                'role': admin_role,
                'description': 'Admin account'
            },
            {
                'username': 'musiclover',
                'email': 'music@test.com',
                'password': 'music123',
                'role': user_role,
                'description': 'Music enthusiast account'
            },
            {
                'username': 'superadmin',
                'email': 'super@test.com',
                'password': 'super123',
                'role': admin_role,
                'description': 'Super admin account'
            }
        ]

        created_users = []
        for user_data in test_users:
            # Check if user already exists
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if not existing_user:
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=app.user_manager.password_manager.hash_password(user_data['password']),
                    active=True,
                    email_confirmed_at=datetime.utcnow()
                )
                db.session.add(user)
                db.session.commit()
                # Add role to user
                user.roles.append(user_data['role'])
                db.session.commit()
                created_users.append(user_data)
            else:
                print(f"User {user_data['email']} already exists, skipping...")

        # Print created accounts
        print(f"\n✅ Created {len(created_users)} test accounts:")
        for user_data in created_users:
            print(f"  👤 {user_data['description']}")
            print(f"     Email: {user_data['email']}")
            print(f"     Password: {user_data['password']}")
            print(f"     Role: {user_data['role'].name}")
            print()

        print("🔐 You can now test with these accounts:")
        print("   - Regular users: user@test.com / userpass123")
        print("   - Admin users: admin@test.com / adminpass123")
        print("   - Visit: http://localhost:5000/login") 