DROP TABLE if exists books;
CREATE TABLE books(title text,
                   author text,
                   link text,
                   description text,
                   id text primary key);

CREATE TABLE votes (name text,
                    points int,
                    id text);

INSERT INTO books (title, author, link, description, id)
VALUES ('The Dispossessed', 'Ursula Leguin', '', '', 'b0997afa-cedb-fd6e-217b-63d597910272');

INSERT INTO books (title, author, link, description, id)
VALUES('Childhoods End',  'Arthur C. Clark', '', '', '60bc303a-eaf4-ba83-1bfc-ca4e12d38783');

INSERT INTO books (title, author, link, description, id)
VALUES('His Dark Materials','Philip Pullman', '', '', 'c1995ad8-407e-ca51-75cf-5642f84e34c4');

INSERT INTO books (title, author, link, description, id)
VALUES('The Dispossessed','Ursula Leguin', '', '', '12a71276-e9d5-c177-89de-d1db224eae49');

INSERT INTO books (title, author, link, description, id)
VALUES('Norse Mythology anything','Neil Gaiman', '', '', '7331bf92-47ac-cf32-662c-5ed34a695a2d');

INSERT INTO books (title, author, link, description, id)
VALUES('Dirk Gentlys Holistic Detective Agency & The Long Dark Tea Time of the Soul','Douglas Adams', '', '', 'e42583a0-86f1-611b-5ef3-9d5fb85e9be1');

INSERT INTO books (title, author, link, description, id)
VALUES('The Emperor of Maladies', 'Siddhartha Mukherjee', '', '', '58bbd5ec-68d3-b080-0f81-51f6bb7f286c');

INSERT INTO books (title, author, link, description, id)
VALUES('Neuromancer', 'William Gibson', '', '', 'a82d8e4f-91df-4207-89bc-0ac1cfe64105');

INSERT INTO books (title, author, link, description, id)
VALUES('Starship Troopers', 'Robert Heinlein', '', '', '65b84d9d-549a-404c-7161-814c83d958b2');

INSERT INTO books (title, author, link, description, id)
VALUES('The Postman', 'David Brin', '', '', '82b25955-c276-7e29-edaa-57adb2f35117');

INSERT INTO books (title, author, link, description, id)
VALUES('Fear and Loathing and The Rum Diaries', 'Hunter S Thompson', '', '', '9cba1258-65d7-ef10-2b2a-cb6c887ab52f');

INSERT INTO books (title, author, link, description, id)
VALUES('Distress', 'Greg Egan', '', '', 'b66ca302-bebd-331f-cdfe-da7849888d21');

INSERT INTO books (title, author, link, description, id)
VALUES('Childhoods End', 'Arthur C. Clarke', '', '', '2b6a4122-de40-4b3b-ef3b-7a24fd89d569');
