# Underground Discovery Exchange

A platform for trading and discovering obscure music recommendations anonymously.

## Features

- Submit music tracks from various platforms (Bandcamp, YouTube, SoundCloud)
- Receive random track recommendations in exchange
- Anonymous submission system
- Admin interface for trade monitoring

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
flask db-init
```

5. Run the application:
```bash
flask run
```

The application will be available at `http://localhost:5000`

## Admin Access

To access the admin interface, go to `/admin` and use the credentials from your `.env` file.

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT License
