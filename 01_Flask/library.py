p1 = """
alter table book add column author_id int;
alter table book add foreign key(author_id) references author(id);
"""

p2 = """
create table books_categories(
id serial, 
author_id int not null, 
category_id int not null, 
primary key(id), 
foreign key(author_id) references author(id), 
foreign key(category_id) references category(id)
);
"""

p3 = """
create table clients_books(
id serial, 
client_id int not null, 
book_id int not null, 
loan_date date, 
return_date date default NULL, 
primary key(id), 
foreign key(book_id) references book(id), 
foreign key(client_id) references client(id)
);
"""