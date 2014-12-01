/* starting database definition for our postgres examples */

/*
note the order of the drop table statements, we drop in order
of reverse dependencies as Postgres won't lets us drop the species
table while there are breed records referring to it.
*/
drop table if exists pet_person;
drop table if exists person;
drop table if exists pet;
drop table if exists shelter;
drop table if exists breed;
drop table if exists species;
/*
Note: we use the type 'serial' instead of integer for our primary 
*/

/*
CREATE SEQUENCE user_id_seq;
CREATE TABLE user (
    user_id smallint NOT NULL DEFAULT nextval('user_id_seq')
);
ALTER SEQUENCE user_id_seq OWNED BY user.user_id;
*/

CREATE SEQUENCE species_id_seq;
create table species (
    id integer not null primary key default nextval('species_id_seq'),
    name text UNIQUE not null
    );
ALTER SEQUENCE species_id_seq OWNED BY species.id;

CREATE SEQUENCE breed_id_seq;
create table breed (
    id smallint not null primary key default nextval('breed_id_seq'),
    name text UNIQUE not null,
    species_id integer references species(id)
    );
ALTER SEQUENCE breed_id_seq OWNED BY breed.id;

CREATE SEQUENCE shelter_id_seq;
create table shelter (
    id integer not null primary key default nextval('shelter_id_seq'),
    name text UNIQUE not null,
    website text,
    phone text
    );
ALTER SEQUENCE shelter_id_seq OWNED BY shelter.id;

CREATE SEQUENCE pet_id_seq;
create table pet (
    id integer not null primary key default nextval('pet_id_seq'),
    name text not null,
    age integer,
    shelter_name text,
    breed_name text,
    species_name text,
    adopted boolean,
    dead boolean,
    breed_id integer references breed(id),
    shelter_id integer references shelter(id),
    species_id integer references species(id)
    );
ALTER SEQUENCE pet_id_seq OWNED BY pet.id;

CREATE SEQUENCE person_id_seq;
create table person (
    id integer not null primary key default nextval('person_id_seq'),
    first_name text not null,
    last_name text not null,
    email text,
    phone text,
    unique( first_name, last_name)
    );
ALTER SEQUENCE person_id_seq OWNED BY person.id;

create table pet_person (
    pet_id integer references pet(id),
    person_id integer references person(id),
    primary key (pet_id, person_id)
    );

/* insert some data */
delete from pet_person where true;
delete from person where true;
delete from pet where true;
delete from shelter where true;
delete from breed where true;
delete from species where true;

/* note: we are not inserting id, the sequence will do it for us */
insert into species (name) values
    ('Cat'),
    ('Dog'),
    ('Parrot');

/* Because we are letting the sequences handle key generation,
   we need to get the species_id value for the species using a subquery */
insert into breed (name, species_id) values
    ('Persian', (select id from species where name='Cat') ),
    ('Tabby', (select id from species where name='Cat') ),
    ('Mixed', (select id from species where name='Cat') ),
    ('Labrador Retriever', (select id from species where name='Dog') ),
    ('Golden Retriever', (select id from species where name='Dog') ),
    ('Labradoodle', (select id from species where name='Dog') ),
    ('Mixed', (select id from species where name='Dog') ),
    ('Norwegian Blue', (select id from species where name='Parrot') ),
    ('African Grey', (select id from species where name='Parrot') );

insert into person (first_name, last_name) values
    ('Iain', 'Duncan'),
    ('Ben', 'White');

insert into shelter (name) values
    ('BCSPCA'),
    ('ASPCA');
    