

CREATE TABLE collection (
    id SERIAL PRIMARY KEY,
    users jsonb
);

INSERT INTO collection (users) VALUES (
    '[
        {
            "username": "bob",
            "movies": [
                {
                    "title": "Kingdom of the Planet of the Apes",
                    "movieId": 653346,
                    "poster": "/gKkl37BQuKTanygYQG1pyYgLVgf.jpg",
                    "releaseDate": "2024-05-08"
                }
            ],
            "shows": [
                {
                    "title": "Top Chef VIP",
                    "tvId": 209374,
                    "poster": "/cw6M4c2MpLSzqzmrrqpSJlEbwCF.jpg",
                    "airDate": "2022-08-09"
                }
            ]
        }
    ]'::jsonb
);
