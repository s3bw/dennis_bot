/*************************************************************
 * This is the table for the postgresql-db.
 ************************************************************/


CREATE TABLE existential_corpus (
    text_id VARCHAR(40) PRIMARY KEY NOT NULL,
    text TEXT NOT NULL,
    subreddit VARCHAR(15) NOT NULL,
    length_text INTEGER NOT NULL CHECK(length_text > 0),
    entry_date TIMESTAMP NOT NULL
);

